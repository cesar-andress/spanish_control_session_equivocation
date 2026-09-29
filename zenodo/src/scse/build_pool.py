"""Build the Phase-2 eligible pool from pinned ParlaMint + Congreso sources."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from scse.config import (
    ELIGIBILITY_RULE_VERSION,
    LEGISLATURE,
    PARLAMINT_COVERAGE_END,
    PARLAMINT_RELEASE,
    PARLAMINT_SHA256,
    PHASE0_PROBE_EXPEDIENTES,
    SPDB_SITTING_DATES,
)
from scse.extract_exchanges import (
    extract_all_xiv_pm_exchanges,
    sessions_with_pm_control_marker,
)
from scse.ingest_congreso import (
    AVISO_LEGAL_URL,
    CONGRESO_REUSE_SUMMARY,
    acquire_initiatives,
    initiative_detail_url,
)
from scse.ingest_parlamint import ensure_parlamint_archive, write_acquisition_manifest
from scse.link_questions import link_exchanges, names_match
from scse.paths import (
    CONGRESO_CACHE,
    DATA_PRIVATE,
    DERIVED_DIR,
    LINK_AUDIT_PRIVATE,
    MANIFESTS_DIR,
    PARLAMINT_CACHE,
    PROJECT_ROOT,
    ensure_private_layout,
    ensure_zenodo_layout,
)
from scse.validation import validate_pool_dataframe

PUBLIC_SAFE_COLUMNS = [
    "exchange_id",
    "expediente",
    "legislature",
    "date",
    "session_id",
    "ds_id",
    "parliamentary_group",
    "questioner_id",
    "answerer_id",
    "parlamint_document_id",
    "q1_utterance_id",
    "r1_utterance_id",
    "q2_utterance_id",
    "r2_utterance_id",
    "link_status",
    "eligible",
    "exclusion_reason",
    "exclude_from_sampling",
    "sampling_exclusion_reason",
    "source_version",
]

OUTCOME_COLUMNS = {
    "reply_status",
    "equivocation_type",
    "outcome",
    "formation_vote_alignment",
    "human_label",
    "answer_quality",
}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _tei_expedientes_by_date() -> dict[str, set[str]]:
    tei = (PARLAMINT_CACHE / "ParlaMint-ES.TEI").resolve()
    out: dict[str, set[str]] = defaultdict(set)
    for path in tei.rglob("ParlaMint-ES_*.xml"):
        m = re.search(r"ParlaMint-ES_(\d{4}-\d{2}-\d{2})", path.name)
        if not m:
            continue
        if not ("2019-12-03" <= m.group(1) <= "2023-02-23"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        out[m.group(1)] |= set(re.findall(r"180/\d{6}", text))
    return out


def gap_expediente_candidates_by_date(raw_exchanges) -> dict[str, set[str]]:
    """Single-number gaps on dates with missing-expediente PM exchanges."""
    by_date = _tei_expedientes_by_date()
    missing_dates = {r.date for r in raw_exchanges if not r.expediente}
    out: dict[str, set[str]] = defaultdict(set)
    for d in missing_dates:
        nums = sorted(int(x.split("/")[1]) for x in by_date.get(d, []))
        for a, b in zip(nums, nums[1:]):
            if b - a == 2:
                out[d].add(f"180/{a + 1:06d}")
            elif 2 < b - a <= 3:
                for k in range(a + 1, b):
                    out[d].add(f"180/{k:06d}")
    # Always include phase0 probes under their known dates when needed
    return out


def recover_missing_expedientes(
    raw_exchanges, initiatives: dict, gaps_by_date: dict[str, set[str]]
) -> int:
    """Assign gap-recovered Congreso expedientes when name uniquely matches on that date."""
    assigned = 0
    missing = [r for r in raw_exchanges if not r.expediente]
    used = {r.expediente for r in raw_exchanges if r.expediente}
    for raw in missing:
        candidates = []
        for exp in gaps_by_date.get(raw.date, set()):
            if exp in used:
                continue
            cong = initiatives.get(exp)
            if cong is None:
                continue
            if not names_match(raw.questioner_who, cong.questioner_name):
                continue
            candidates.append((exp, cong))
        if len(candidates) == 1:
            exp, cong = candidates[0]
            raw.expediente = exp
            raw.extraction_notes = [
                n for n in raw.extraction_notes if n != "expediente_missing_in_tei"
            ] + ["expediente_recovered_from_congreso_gap"]
            if not raw.registered_question_from_chair and cong.title:
                raw.registered_question_from_chair = cong.title
            used.add(exp)
            assigned += 1
        elif len(candidates) > 1:
            raw.extraction_notes.append(
                f"ambiguous_gap_candidates:{','.join(c[0] for c in candidates[:5])}"
            )
    return assigned


def apply_sampling_exclusions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Phase-0 probes
    probe_mask = df["expediente"].isin(PHASE0_PROBE_EXPEDIENTES)
    df.loc[probe_mask, "exclude_from_sampling"] = True
    df.loc[probe_mask, "sampling_exclusion_reason"] = "phase0_feasibility_probe"

    # SPDB sitting-date overlap
    overlap = df["date"].isin(SPDB_SITTING_DATES)
    # Only mark if not already excluded for phase0
    new_overlap = overlap & ~df["exclude_from_sampling"].fillna(False)
    df.loc[new_overlap, "exclude_from_sampling"] = True
    df.loc[new_overlap, "sampling_exclusion_reason"] = "spdb_previous_paper_sitting_date"

    return df


def select_linkage_qa(df: pd.DataFrame, n: int = 30) -> pd.DataFrame:
    eligible = df[df["eligible"] & ~df["exclude_from_sampling"].fillna(False)].copy()
    if eligible.empty:
        eligible = df[df["eligible"]].copy()
    eligible["_rank"] = eligible["exchange_id"].map(
        lambda x: hashlib.sha256(str(x).encode("utf-8")).hexdigest()
    )
    eligible = eligible.sort_values(["_rank", "exchange_id"]).head(n)
    return eligible.drop(columns=["_rank"])


def write_linkage_qa_packet(qa: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for _, r in qa.iterrows():
        rows.append(
            {
                "exchange_id": r["exchange_id"],
                "expediente": r.get("expediente"),
                "date": r.get("date"),
                "session_id": r.get("session_id"),
                "questioner_name": r.get("questioner_name"),
                "questioner_id": r.get("questioner_id"),
                "parliamentary_group": r.get("parliamentary_group"),
                "registered_question": r.get("registered_question"),
                "q1_text": r.get("q1_text"),
                "r1_text": r.get("r1_text"),
                "congreso_url": r.get("congreso_url")
                or (
                    initiative_detail_url(r["expediente"])
                    if pd.notna(r.get("expediente")) and r.get("expediente")
                    else None
                ),
                "parlamint_document_id": r.get("parlamint_document_id"),
                "q1_utterance_id": r.get("q1_utterance_id"),
                "r1_utterance_id": r.get("r1_utterance_id"),
                "link_status": r.get("link_status"),
                "link_evidence": r.get("link_evidence"),
                "human_link_correct": None,
                "human_notes": None,
            }
        )
    out = pd.DataFrame(rows)
    out.to_excel(path, index=False)
    return path


def build_pool(*, sleep_s: float = 0.75) -> dict:
    ensure_private_layout()
    ensure_zenodo_layout()

    pointer = ensure_parlamint_archive()
    raw = extract_all_xiv_pm_exchanges()

    # Congreso: TEI expedientes + gap candidates + phase0 probes
    tei_exps = sorted({r.expediente for r in raw if r.expediente})
    gaps_by_date = gap_expediente_candidates_by_date(raw)
    gaps = sorted({e for s in gaps_by_date.values() for e in s} | set(PHASE0_PROBE_EXPEDIENTES))
    to_fetch = sorted(set(tei_exps) | set(gaps))

    initiatives_list = acquire_initiatives(to_fetch, sleep_s=sleep_s)
    initiatives = {i.expediente: i for i in initiatives_list}

    recovered = recover_missing_expedientes(raw, initiatives, gaps_by_date)
    # Note: recover_missing is a pre-pass; final expediente assignment is in link_exchanges
    _ = recovered
    # Re-fetch any newly assigned that were not in catalog (should already be in gaps)
    still_needed = [r.expediente for r in raw if r.expediente and r.expediente not in initiatives]
    if still_needed:
        extra = acquire_initiatives(still_needed, sleep_s=sleep_s)
        for i in extra:
            initiatives[i.expediente] = i

    # Drop noisy TEI expediente before date+name linkage (kept in extraction_notes)
    tei_exps_by_date = _tei_expedientes_by_date()
    linked = link_exchanges(
        raw,
        initiatives,
        tei_exps_by_date=tei_exps_by_date,
        gap_ids_by_date=gaps_by_date,
    )
    rows = [L.to_row() for L in linked]
    df = pd.DataFrame(rows)
    df = apply_sampling_exclusions(df)

    # Mark linkage QA exclusions after selecting
    qa = select_linkage_qa(df, n=30)
    qa_ids = set(qa["exchange_id"].tolist())
    qa_mask = df["exchange_id"].isin(qa_ids)
    # Don't overwrite phase0 reason
    for idx in df.index[qa_mask]:
        if not bool(df.at[idx, "exclude_from_sampling"]):
            df.at[idx, "exclude_from_sampling"] = True
            df.at[idx, "sampling_exclusion_reason"] = "linkage_QA"
        elif df.at[idx, "sampling_exclusion_reason"] == "phase0_feasibility_probe":
            pass
        else:
            # already excluded for another reason; keep prior, note QA also
            pass

    validate_pool_dataframe(df)

    private_path = DATA_PRIVATE / "eligible_pool_full.parquet"
    # Stable column order
    df = df.sort_values(["date", "expediente", "exchange_id"], kind="mergesort").reset_index(
        drop=True
    )
    df.to_parquet(private_path, index=False)

    # Exclusions table
    excl = df[~df["eligible"] | df["exclude_from_sampling"].fillna(False)].copy()
    excl_path = DATA_PRIVATE / "exclusions_table.parquet"
    excl.to_parquet(excl_path, index=False)

    # Public-safe projection
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    public = df[[c for c in PUBLIC_SAFE_COLUMNS if c in df.columns]].copy()
    public_path = DERIVED_DIR / "eligible_pool_metadata_preannotation.csv"
    public.to_csv(public_path, index=False)
    # Also parquet for reproducibility
    public_parquet = DERIVED_DIR / "eligible_pool_metadata_preannotation.parquet"
    public.to_parquet(public_parquet, index=False)

    qa_path = LINK_AUDIT_PRIVATE / "PHASE2_LINKAGE_QA.xlsx"
    write_linkage_qa_packet(df[df["exchange_id"].isin(qa_ids)], qa_path)

    # Candidate session diagnostic
    sess = sessions_with_pm_control_marker()
    sess_path = DATA_PRIVATE / "candidate_control_sessions.json"
    sess_path.write_text(json.dumps(sess, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    private_sha = _sha256_file(private_path)
    public_sha = _sha256_file(public_path)
    excl_sha = _sha256_file(excl_path)

    write_acquisition_manifest(
        [
            {
                "source": "ParlaMint-ES",
                "version": PARLAMINT_RELEASE,
                "URL": pointer["handle"],
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "filename": pointer["archive"],
                "sha256": pointer["sha256"],
                "licence_status": "CC-BY-4.0",
                "coverage": f"XIV window through {PARLAMINT_COVERAGE_END.isoformat()}",
                "notes": "Bulk archive in _internal/source_cache/parlamint/",
            },
            {
                "source": "Congreso iniciativas 180/",
                "version": LEGISLATURE,
                "URL": "https://www.congreso.es/es/busqueda-de-iniciativas",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "filename": "iniciativas/*.html",
                "sha256": None,
                "licence_status": "reuse_with_conditions_aviso_legal",
                "coverage": f"Fetched expediente detail pages n={len(initiatives)}",
                "notes": (
                    f"Aviso legal: {AVISO_LEGAL_URL}. {CONGRESO_REUSE_SUMMARY} "
                    "Public release strategy remains identifier-based until legal review."
                ),
            },
        ]
    )

    # git commit if available
    commit = None
    try:
        import subprocess

        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(PROJECT_ROOT), text=True
        ).strip()
    except Exception:
        commit = None

    eligible_df = df[df["eligible"]]
    sampling_eligible = eligible_df[~eligible_df["exclude_from_sampling"].fillna(False)]

    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pipeline_commit": commit,
        "eligibility_rule_version": ELIGIBILITY_RULE_VERSION,
        "parlamint_release": PARLAMINT_RELEASE,
        "parlamint_sha256": PARLAMINT_SHA256,
        "congreso_records_fetched": len(initiatives),
        "gap_candidates_fetched": len(gaps),
        "expedientes_recovered": recovered,
        "raw_pm_exchanges": len(raw),
        "link_status_counts": Counter(df["link_status"]).most_common(),
        "eligible_count": int(eligible_df.shape[0]),
        "sampling_frame_count": int(sampling_eligible.shape[0]),
        "sessions_eligible": int(eligible_df["session_id"].nunique()),
        "questioners_eligible": int(eligible_df["questioner_id"].nunique()),
        "groups_eligible": int(eligible_df["parliamentary_group"].dropna().nunique()),
        "phase0_excluded": int(df["sampling_exclusion_reason"].eq("phase0_feasibility_probe").sum()),
        "spdb_overlap_rows": int(
            df["sampling_exclusion_reason"].eq("spdb_previous_paper_sitting_date").sum()
        ),
        "linkage_qa_n": len(qa_ids),
        "private_pool_path": str(private_path.relative_to(PROJECT_ROOT)),
        "private_pool_sha256": private_sha,
        "public_pool_path": str(public_path.relative_to(PROJECT_ROOT)),
        "public_pool_sha256": public_sha,
        "exclusions_sha256": excl_sha,
        "qa_packet_path": str(qa_path.relative_to(PROJECT_ROOT)),
        "seeds": {"development": None, "calibration": None, "main_sample": None},
        "outcome_columns_present": sorted(OUTCOME_COLUMNS & set(df.columns)),
    }

    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = MANIFESTS_DIR / "eligible_pool_manifest.json"
    # Core scientific payload without volatile timestamp for optional compare
    core = {k: v for k, v in summary.items() if k != "created_at"}
    summary["core_sha256"] = hashlib.sha256(
        json.dumps(core, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    manifest_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (DATA_PRIVATE / "pool_build_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    summary = build_pool()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
