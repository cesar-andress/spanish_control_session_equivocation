"""Apply development-set sampling exclusions and refresh public pool projections.

Does not rebuild ParlaMint/Congreso acquisition. Does not annotate reply_status.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from scse.build_pool import PUBLIC_SAFE_COLUMNS, _sha256_file
from scse.paths import DATA_PRIVATE, DERIVED_DIR, MANIFESTS_DIR, PROJECT_ROOT
from scse.validation import validate_pool_dataframe

DEV_DIR = DATA_PRIVATE / "development"
DEV_MANIFEST = DEV_DIR / "DEVELOPMENT_SET_MANIFEST.json"


def development_unit_ids() -> list[str]:
    if not DEV_MANIFEST.is_file():
        return []
    data = json.loads(DEV_MANIFEST.read_text(encoding="utf-8"))
    return list(data.get("unit_ids") or [])


def apply_development_exclusions(df: pd.DataFrame) -> pd.DataFrame:
    """Mark codebook-development units as exclude_from_sampling."""
    df = df.copy()
    ids = set(development_unit_ids())
    if not ids:
        return df
    mask = df["exchange_id"].isin(ids)
    # Do not overwrite earlier exclusion reasons
    new = mask & ~df["exclude_from_sampling"].fillna(False)
    df.loc[new, "exclude_from_sampling"] = True
    df.loc[new, "sampling_exclusion_reason"] = "development_codebook"
    # If already excluded as development but reason missing, set reason
    already = mask & df["exclude_from_sampling"].fillna(False)
    need_reason = already & df["sampling_exclusion_reason"].isna()
    df.loc[need_reason, "sampling_exclusion_reason"] = "development_codebook"
    return df


def refresh_public_projections(df: pd.DataFrame) -> dict:
    private_path = DATA_PRIVATE / "eligible_pool_full.parquet"
    excl_path = DATA_PRIVATE / "exclusions_table.parquet"
    public_path = DERIVED_DIR / "eligible_pool_metadata_preannotation.csv"
    public_parquet = DERIVED_DIR / "eligible_pool_metadata_preannotation.parquet"

    df = df.sort_values(["date", "expediente", "exchange_id"], kind="mergesort").reset_index(
        drop=True
    )
    validate_pool_dataframe(df)
    private_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(private_path, index=False)

    excl = df[~df["eligible"] | df["exclude_from_sampling"].fillna(False)].copy()
    excl.to_parquet(excl_path, index=False)

    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    public = df[[c for c in PUBLIC_SAFE_COLUMNS if c in df.columns]].copy()
    public.to_csv(public_path, index=False)
    public.to_parquet(public_parquet, index=False)

    eligible_df = df[df["eligible"]]
    sampling_eligible = eligible_df[~eligible_df["exclude_from_sampling"].fillna(False)]

    commit = None
    try:
        import subprocess

        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(PROJECT_ROOT), text=True
        ).strip()
    except Exception:
        commit = None

    # Preserve prior human_linkage_validation block if present
    manifest_path = MANIFESTS_DIR / "eligible_pool_manifest.json"
    prior = {}
    if manifest_path.is_file():
        prior = json.loads(manifest_path.read_text(encoding="utf-8"))

    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pipeline_commit": commit,
        "eligibility_rule_version": prior.get("eligibility_rule_version", "phase2-xiv-v1"),
        "parlamint_release": prior.get("parlamint_release"),
        "parlamint_sha256": prior.get("parlamint_sha256"),
        "congreso_records_fetched": prior.get("congreso_records_fetched"),
        "gap_candidates_fetched": prior.get("gap_candidates_fetched"),
        "expedientes_recovered": prior.get("expedientes_recovered"),
        "raw_pm_exchanges": int(len(df)),
        "link_status_counts": [[k, int(v)] for k, v in df["link_status"].value_counts().items()],
        "eligible_count": int(eligible_df.shape[0]),
        "sampling_frame_count": int(sampling_eligible.shape[0]),
        "sessions_eligible": int(eligible_df["session_id"].nunique()),
        "questioners_eligible": int(eligible_df["questioner_id"].nunique()),
        "groups_eligible": int(eligible_df["parliamentary_group"].dropna().nunique()),
        "phase0_excluded": int(df["sampling_exclusion_reason"].eq("phase0_feasibility_probe").sum()),
        "spdb_overlap_rows": int(
            df["sampling_exclusion_reason"].eq("spdb_previous_paper_sitting_date").sum()
        ),
        "linkage_qa_n": int(df["sampling_exclusion_reason"].eq("linkage_QA").sum()),
        "development_codebook_n": int(
            df["sampling_exclusion_reason"].eq("development_codebook").sum()
        ),
        "private_pool_path": str(private_path.relative_to(PROJECT_ROOT)),
        "private_pool_sha256": _sha256_file(private_path),
        "public_pool_path": str(public_path.relative_to(PROJECT_ROOT)),
        "public_pool_sha256": _sha256_file(public_path),
        "exclusions_sha256": _sha256_file(excl_path),
        "qa_packet_path": prior.get("qa_packet_path"),
        "seeds": {"development": None, "calibration": None, "main_sample": None},
        "outcome_columns_present": [],
        "reply_status_codebook_status": "draft_v0.1_not_frozen",
        "refresh_reason": "phase4_development_exclusions",
    }
    if "human_linkage_validation" in prior:
        summary["human_linkage_validation"] = prior["human_linkage_validation"]
    if "human_linkage_validation_recorded_at" in prior:
        summary["human_linkage_validation_recorded_at"] = prior[
            "human_linkage_validation_recorded_at"
        ]

    core = {k: v for k, v in summary.items() if k not in {"created_at", "core_sha256"}}
    summary["core_sha256"] = hashlib.sha256(
        json.dumps(core, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA_PRIVATE / "pool_build_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    private_path = DATA_PRIVATE / "eligible_pool_full.parquet"
    df = pd.read_parquet(private_path)
    df = apply_development_exclusions(df)
    summary = refresh_public_projections(df)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
