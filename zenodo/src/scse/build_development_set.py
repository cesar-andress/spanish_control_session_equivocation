"""Build out-of-pool reply_status development set (Phase 4.1).

Preferred source: XIII legislature PM control sessions in ParlaMint-ES.
Supplement: XII post-censure PM control (same answerer, outside XIV), only if
XIII volume is insufficient.

Does not touch XIV main annotation. Does not compute reliability or outcomes.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from scse.config import PM_WHO
from scse.extract_exchanges import (
    EXPEDIENTE_RE,
    PM_ONLY_FORMULA_RE,
    RawExchange,
    _is_chair,
    _is_pm,
    _notes_expediente,
    parse_session_utterances,
)
from scse.paths import DATA_PRIVATE, PARLAMINT_CACHE, PROJECT_ROOT, PROTOCOL_DIR
from scse.refresh_development_exclusions import refresh_public_projections

# XIII legislature dates (Congreso)
XIII_START = date(2019, 5, 21)
XIII_END = date(2019, 12, 2)
# XII post-censure Sánchez window (fallback supplement only)
XII_SUPPLEMENT_START = date(2018, 6, 2)
XII_SUPPLEMENT_END = date(2019, 5, 20)

DEV_N = 15
SELECTION_PREFIX = "development_oop|"

PM_FORMULA_DEV_RE = re.compile(
    r"QUE\s+FORMULA\s+AL\s+SE[NÑ]OR\s+PRESIDENTE\s+DEL\s+GOBIERNO"
    r"(?:\s+EN\s+FUNCIONES)?\s*:\s*(.+?)"
    r"(?:Número de expediente\s*180/\d{6}|$)",
    re.I | re.S,
)

DEV_DIR = DATA_PRIVATE / "development"
SUPERSEDED_DIR = DEV_DIR / "superseded_xiv_inpool_2026-10-01"
OOP_DIR = DEV_DIR / "out_of_pool"
MANIFEST_YAML = PROTOCOL_DIR / "development_set_manifest.yaml"


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _document_relpath(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PARLAMINT_CACHE.resolve()))
    except ValueError:
        return path.name


def _extract_registered(text: str) -> tuple[str | None, str | None]:
    if not PM_ONLY_FORMULA_RE.search(text) and not re.search(
        r"FORMULA\s+AL\s+SE[NÑ]OR\s+PRESIDENTE\s+DEL\s+GOBIERNO", text, re.I
    ):
        return None, None
    m = PM_FORMULA_DEV_RE.search(text)
    question = None
    if m:
        question = " ".join((m.group(1) or "").split()).strip(" -–")
        question = question or None
    exp = EXPEDIENTE_RE.search(text)
    return question, exp.group(0) if exp else None


def _is_pm_formula_chair(text: str) -> bool:
    return bool(
        re.search(
            r"FORMULA\s+AL\s+SE[NÑ]OR\s+PRESIDENTE\s+DEL\s+GOBIERNO(?:\s+EN\s+FUNCIONES)?",
            text,
            re.I,
        )
    )


def extract_pm_dev_exchanges_from_session(
    path: Path, *, legislature: str
) -> list[RawExchange]:
    """Lightweight Q1–R1 extractor for out-of-pool development only.

    Finds chair FORMULA-to-PM announcements, then the following questioner turn
    and first PM response. Not used for the XIV eligible pool.
    """
    path = path.resolve()
    session_id, session_date, utts = parse_session_utterances(path)
    if not session_date:
        return []

    exchanges: list[RawExchange] = []
    used_q1: set[str] = set()

    for i, u in enumerate(utts):
        if not _is_chair(u) or not _is_pm_formula_chair(u.text):
            continue
        reg_q, exp = _extract_registered(u.text)
        # Next non-chair speakers: questioner then PM
        q_idx = None
        r_idx = None
        for j in range(i + 1, min(i + 12, len(utts))):
            uj = utts[j]
            if _is_chair(uj):
                # skip short procedural chair lines
                if _is_pm_formula_chair(uj.text):
                    break
                continue
            if q_idx is None:
                if _is_pm(uj):
                    break
                q_idx = j
                continue
            # continue concatenating same questioner fragments
            if utts[q_idx].who == uj.who:
                continue
            if _is_pm(uj):
                r_idx = j
                break
            break
        if q_idx is None or r_idx is None:
            continue
        if utts[q_idx].uid in used_q1:
            continue

        # Skip réplica: if previous non-chair before formula was PM answering same who
        prev = None
        for j in range(i - 1, max(-1, i - 8), -1):
            if not _is_chair(utts[j]):
                prev = utts[j]
                break
        if prev is not None and _is_pm(prev):
            # likely start of réplica block after prior R1 — still allow if formula is new
            pass

        q_who = utts[q_idx].who
        q_parts = []
        for j in range(q_idx, r_idx):
            if not _is_chair(utts[j]) and utts[j].who == q_who:
                q_parts.append(utts[j].text)
        q1_text = " ".join(q_parts).strip()
        r1_text = utts[r_idx].text.strip()
        if not q1_text or not r1_text:
            continue

        if not exp:
            exp = _notes_expediente(utts[q_idx].notes) or _notes_expediente(
                utts[r_idx].notes
            )
        notes: list[str] = ["development_extractor_v1"]
        if not exp:
            notes.append("expediente_missing_in_tei")
        if not reg_q:
            notes.append("registered_question_missing_in_chair")

        exchanges.append(
            RawExchange(
                session_id=session_id,
                document_path=_document_relpath(path),
                date=session_date,
                legislature=legislature,
                expediente=exp,
                registered_question_from_chair=reg_q,
                questioner_who=q_who,
                answerer_who=PM_WHO,
                q1_utterance_id=utts[q_idx].uid,
                r1_utterance_id=utts[r_idx].uid,
                q1_text=q1_text,
                r1_text=r1_text,
                chair_announcement=u.text,
                extraction_notes=notes,
            )
        )
        used_q1.add(utts[q_idx].uid)

    return exchanges


def iter_session_files(start: date, end: date) -> list[Path]:
    tei = (PARLAMINT_CACHE / "ParlaMint-ES.TEI").resolve()
    out: list[Path] = []
    for path in sorted(tei.rglob("ParlaMint-ES_*.xml")):
        m = re.search(r"ParlaMint-ES_(\d{4}-\d{2}-\d{2})", path.name)
        if not m:
            continue
        d = date.fromisoformat(m.group(1))
        if start <= d <= end:
            out.append(path)
    return out


def make_dev_unit_id(r: RawExchange) -> str:
    base = f"{r.legislature}|{r.session_id}|{r.q1_utterance_id}|{r.r1_utterance_id}"
    return "dev_" + _sha256_text(base)[:16]


def collect_candidates() -> list[dict]:
    rows: list[dict] = []
    for path in iter_session_files(XIII_START, XIII_END):
        for r in extract_pm_dev_exchanges_from_session(path, legislature="XIII"):
            d = asdict(r)
            d["unit_id"] = make_dev_unit_id(r)
            d["source_priority"] = 1
            rows.append(d)
    for path in iter_session_files(XII_SUPPLEMENT_START, XII_SUPPLEMENT_END):
        for r in extract_pm_dev_exchanges_from_session(path, legislature="XII"):
            d = asdict(r)
            d["unit_id"] = make_dev_unit_id(r)
            d["source_priority"] = 2
            rows.append(d)
    # Prefer units with registered text; require q1+r1
    usable = [
        r
        for r in rows
        if str(r.get("q1_text") or "").strip() and str(r.get("r1_text") or "").strip()
    ]
    # Deduplicate by unit_id
    by_id = {r["unit_id"]: r for r in usable}
    return list(by_id.values())


def select_development(candidates: list[dict], n: int = DEV_N) -> list[dict]:
    # Prefer XIII (priority 1), then XII; within tier sort by hash
    def rank_key(r: dict) -> tuple:
        h = _sha256_text(SELECTION_PREFIX + r["unit_id"])
        return (int(r["source_priority"]), h, r["unit_id"])

    ordered = sorted(candidates, key=rank_key)
    # Take all XIII first up to n, then XII
    xiii = [r for r in ordered if r["legislature"] == "XIII"]
    xii = [r for r in ordered if r["legislature"] == "XII"]
    selected = xiii[:n]
    if len(selected) < n:
        selected.extend(xii[: n - len(selected)])
    return selected


def supersede_old_inpool_development() -> dict:
    """Mark XIV in-pool development set superseded; restore sampling eligibility."""
    DEV_DIR.mkdir(parents=True, exist_ok=True)
    SUPERSEDED_DIR.mkdir(parents=True, exist_ok=True)

    old_manifest = DEV_DIR / "DEVELOPMENT_SET_MANIFEST.json"
    old_audit = DEV_DIR / "DEVELOPMENT_SET_AUDIT.csv"
    old_pkt_csv = DEV_DIR / "DEVELOPMENT_PACKET_BLINDED.csv"
    old_pkt_xlsx = DEV_DIR / "DEVELOPMENT_PACKET_BLINDED.xlsx"

    meta = {
        "status": "superseded",
        "reason": "Development material must not overlap with main population.",
        "superseded_on": datetime.now(timezone.utc).date().isoformat(),
        "phase": "4.1",
        "original_files": [],
    }

    for path in (old_manifest, old_audit, old_pkt_csv, old_pkt_xlsx):
        if path.is_file():
            dest = SUPERSEDED_DIR / path.name
            dest.write_bytes(path.read_bytes())
            meta["original_files"].append(str(path.relative_to(PROJECT_ROOT)))
            # Keep originals in place but rewrite manifest status if present
    if old_manifest.is_file():
        data = json.loads(old_manifest.read_text(encoding="utf-8"))
        data["status"] = "superseded"
        data["superseded_reason"] = meta["reason"]
        data["superseded_on"] = meta["superseded_on"]
        data["replacement"] = "out_of_pool (see development_set_manifest.yaml)"
        old_manifest.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    (SUPERSEDED_DIR / "SUPERSEDED.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Restore XIV pool exclusions for development_codebook
    pool_path = DATA_PRIVATE / "eligible_pool_full.parquet"
    df = pd.read_parquet(pool_path)
    mask = df["sampling_exclusion_reason"].eq("development_codebook")
    n = int(mask.sum())
    df.loc[mask, "exclude_from_sampling"] = False
    df.loc[mask, "sampling_exclusion_reason"] = None
    summary = refresh_public_projections(df)
    summary["restored_development_codebook_n"] = n
    return {"restored_n": n, "pool_summary": summary, "supersede_meta": meta}


def write_oop_artifacts(selected: list[dict], candidates: list[dict]) -> dict:
    OOP_DIR.mkdir(parents=True, exist_ok=True)
    audit_rows = []
    packet_rows = []
    for r in selected:
        reg = (r.get("registered_question_from_chair") or "").strip()
        if not reg:
            reg = (
                f"[REGISTERED TEXT MISSING IN TEI — expediente {r.get('expediente')}; "
                "use chair formula / Congreso title during coding practice]"
            )
        audit_rows.append(
            {
                "unit_id": r["unit_id"],
                "legislature": r["legislature"],
                "date": r["date"],
                "session_id": r["session_id"],
                "expediente": r.get("expediente"),
                "questioner_who": r.get("questioner_who"),
                "q1_utterance_id": r["q1_utterance_id"],
                "r1_utterance_id": r["r1_utterance_id"],
                "source_priority": r["source_priority"],
                "selection_rule": f"sha256('{SELECTION_PREFIX}'+unit_id) within legislature preference XIII then XII",
                "purpose": "codebook_examples_and_refinement_only",
                "exclusion_from_main_sampling": True,
                "has_registered_in_tei": bool(
                    str(r.get("registered_question_from_chair") or "").strip()
                ),
            }
        )
        packet_rows.append(
            {
                "unit_id": r["unit_id"],
                "registered_question": reg,
                "Q1": r["q1_text"],
                "R1": r["r1_text"],
            }
        )

    audit = pd.DataFrame(audit_rows)
    packet = pd.DataFrame(packet_rows)
    audit_path = OOP_DIR / "DEVELOPMENT_SET_AUDIT.csv"
    packet_csv = OOP_DIR / "DEVELOPMENT_PACKET_BLINDED.csv"
    packet_xlsx = OOP_DIR / "DEVELOPMENT_PACKET_BLINDED.xlsx"
    audit.to_csv(audit_path, index=False)
    packet.to_csv(packet_csv, index=False)
    packet.to_excel(packet_xlsx, index=False)

    unit_ids = [r["unit_id"] for r in selected]
    content_hash = _sha256_text("\n".join(sorted(unit_ids)))
    private_manifest = {
        "purpose": "codebook development examples only — out of XIV population",
        "n": len(selected),
        "selection_rule": (
            f"Prefer XIII PM FORMULA exchanges; fill to n={DEV_N} from XII "
            f"post-censure; order by sha256('{SELECTION_PREFIX}'+unit_id)"
        ),
        "scientific_seed_used": None,
        "unit_ids": unit_ids,
        "legislature_counts": {
            "XIII": sum(1 for r in selected if r["legislature"] == "XIII"),
            "XII": sum(1 for r in selected if r["legislature"] == "XII"),
        },
        "candidates_available": {
            "XIII": sum(1 for r in candidates if r["legislature"] == "XIII"),
            "XII": sum(1 for r in candidates if r["legislature"] == "XII"),
        },
        "exclusion_from_main_sampling": True,
        "not_for_reliability": True,
        "content_sha256": content_hash,
    }
    (OOP_DIR / "DEVELOPMENT_SET_MANIFEST.json").write_text(
        json.dumps(private_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    yaml_doc = {
        "status": "draft_development_set",
        "phase": "4.1",
        "created_on": datetime.now(timezone.utc).date().isoformat(),
        "source": "ParlaMint-ES 5.0 TEI (PM oral-question FORMULA exchanges)",
        "legislature": {
            "preferred": "XIII",
            "supplement": "XII_post_censure",
            "counts": private_manifest["legislature_counts"],
        },
        "selection_rule": private_manifest["selection_rule"],
        "hash": content_hash,
        "n_units": len(selected),
        "exclusion_from_main_sampling": True,
        "not_for_reliability_evaluation": True,
        "unit_ids": unit_ids,
        "private_artifacts": {
            "audit": str(audit_path.relative_to(PROJECT_ROOT)),
            "blinded_packet_csv": str(packet_csv.relative_to(PROJECT_ROOT)),
            "blinded_packet_xlsx": str(packet_xlsx.relative_to(PROJECT_ROOT)),
            "manifest_json": str(
                (OOP_DIR / "DEVELOPMENT_SET_MANIFEST.json").relative_to(PROJECT_ROOT)
            ),
        },
        "date_windows": {
            "XIII": [XIII_START.isoformat(), XIII_END.isoformat()],
            "XII_supplement": [
                XII_SUPPLEMENT_START.isoformat(),
                XII_SUPPLEMENT_END.isoformat(),
            ],
        },
        "notes": [
            "Outside XIV eligible population.",
            "XIII alone has few PM FORMULA exchanges in ParlaMint; XII fills to n.",
            "Some TEI rows lack registered title; packet marks placeholder for practice.",
            "Do not mix these units into future XIV reliability or main samples.",
        ],
    }
    MANIFEST_YAML.write_text(
        yaml.safe_dump(yaml_doc, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return private_manifest


def main() -> int:
    restore = supersede_old_inpool_development()
    candidates = collect_candidates()
    selected = select_development(candidates, n=DEV_N)
    if len(selected) < DEV_N:
        raise SystemExit(
            f"insufficient out-of-pool candidates: got {len(selected)} need {DEV_N} "
            f"(available XIII+XII={len(candidates)})"
        )
    manifest = write_oop_artifacts(selected, candidates)
    out = {
        "restored_xiv_development_exclusions": restore["restored_n"],
        "sampling_frame_count": restore["pool_summary"].get("sampling_frame_count"),
        "development": manifest,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
