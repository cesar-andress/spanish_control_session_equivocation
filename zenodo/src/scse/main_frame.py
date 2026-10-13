"""Phase 6A: restore linkage-QA units and freeze the pre-outcome main frame.

No reply_status labels. No outcome inference.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from scse.build_pool import PUBLIC_SAFE_COLUMNS, _sha256_file
from scse.paths import (
    DATA_PRIVATE,
    DERIVED_DIR,
    INTERNAL_DIR,
    LINK_AUDIT_PRIVATE,
    MANIFESTS_DIR,
    PROJECT_ROOT,
    PROTOCOL_DIR,
)
from scse.refresh_development_exclusions import refresh_public_projections
from scse.validation import validate_pool_dataframe

OUTCOME_FORBIDDEN = {
    "reply_status",
    "equivocation_type",
    "outcome",
    "human_label",
    "answer_quality",
    "predicted_reply_status",
    "provisional_reply_status",
    "llm_reply_status",
}

QA_VALIDATION_JSON = LINK_AUDIT_PRIVATE / "PHASE2_LINKAGE_QA_HUMAN_VALIDATION.json"
QUESTION_SIDE_CSV = DATA_PRIVATE / "question_side" / "xiv_eligible_question_side_audit.csv"
MAIN_PRIVATE = DATA_PRIVATE / "main"
MAIN_PACKETS = INTERNAL_DIR / "main_packets"
MAIN_ANNOTATION = INTERNAL_DIR / "main_annotation"
VOLUMES_DEFAULT = (25, 24, 24, 24)  # sum 97


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_qa30_exchange_ids() -> list[str]:
    data = json.loads(QA_VALIDATION_JSON.read_text(encoding="utf-8"))
    ids = list(data["exchange_ids"])
    if len(ids) != 30:
        raise ValueError(f"expected 30 QA exchange_ids, got {len(ids)}")
    if data.get("reply_status_judgement_performed") is not False:
        raise ValueError("QA validation must record reply_status_judgement_performed=false")
    return ids


def restore_linkage_qa(df: pd.DataFrame, qa_ids: list[str] | None = None) -> pd.DataFrame:
    """Clear sampling exclusion for linkage-QA rows; keep Phase-0 probes excluded."""
    df = df.copy()
    qa_ids = qa_ids or load_qa30_exchange_ids()
    qa_set = set(qa_ids)
    mask = df["exchange_id"].isin(qa_set)
    if int(mask.sum()) != 30:
        raise ValueError(f"expected 30 QA rows in pool, found {int(mask.sum())}")
    # Do not touch phase0 probes even if somehow overlapping (none expected)
    probe = df["sampling_exclusion_reason"].eq("phase0_feasibility_probe")
    restore = mask & ~probe
    df.loc[restore, "exclude_from_sampling"] = False
    df.loc[restore, "sampling_exclusion_reason"] = pd.NA
    return df


def assert_no_outcome_columns(df: pd.DataFrame) -> None:
    bad = OUTCOME_FORBIDDEN & set(df.columns)
    if bad:
        raise ValueError(f"forbidden outcome columns: {sorted(bad)}")


def load_question_side_metadata() -> pd.DataFrame:
    qs = pd.read_csv(QUESTION_SIDE_CSV)
    keep = [
        "exchange_id",
        "question_topic",
        "question_form",
        "question_confrontational",
        "formation_vote_alignment",
        "primary_alignment",
        "questioner",
    ]
    return qs[[c for c in keep if c in qs.columns]].copy()


def build_main_frame(df: pd.DataFrame | None = None) -> dict:
    """Restore QA30, refresh pool projections, write main-frame artifacts."""
    private_path = DATA_PRIVATE / "eligible_pool_full.parquet"
    df = df if df is not None else pd.read_parquet(private_path)
    assert_no_outcome_columns(df)

    qa_ids = load_qa30_exchange_ids()
    df = restore_linkage_qa(df, qa_ids)
    validate_pool_dataframe(df)

    # Refresh public identifier projection + pool manifest
    summary = refresh_public_projections(df)
    summary["refresh_reason"] = "phase6a_restore_linkage_qa_preoutcome"
    summary["linkage_qa_restored_n"] = 30
    summary["linkage_qa_active_exclusion_n"] = int(
        df["sampling_exclusion_reason"].eq("linkage_QA").sum()
    )
    summary["phase0_still_excluded"] = int(
        df["sampling_exclusion_reason"].eq("phase0_feasibility_probe").sum()
    )
    summary["main_frame_n"] = int(
        (df["eligible"] & ~df["exclude_from_sampling"].fillna(False)).sum()
    )
    # rewrite summary files with Phase 6A fields
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    (MANIFESTS_DIR / "eligible_pool_manifest.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (DATA_PRIVATE / "pool_build_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    main = df[df["eligible"] & ~df["exclude_from_sampling"].fillna(False)].copy()
    main = main.sort_values(["date", "expediente", "exchange_id"], kind="mergesort").reset_index(
        drop=True
    )
    main.insert(0, "case_no", range(1, len(main) + 1))

    if len(main) != 97:
        raise ValueError(f"expected main-frame N=97, got {len(main)}")

    qs = load_question_side_metadata()
    main = main.merge(qs, on="exchange_id", how="left", validate="one_to_one")
    if main["formation_vote_alignment"].isna().any():
        raise ValueError("missing formation_vote_alignment for main-frame units")

    completeness = _completeness_report(main)
    if completeness["n_complete"] != len(main):
        raise ValueError(f"incomplete main-frame texts: {completeness}")

    MAIN_PRIVATE.mkdir(parents=True, exist_ok=True)
    MAIN_PACKETS.mkdir(parents=True, exist_ok=True)
    MAIN_ANNOTATION.mkdir(parents=True, exist_ok=True)

    corpus_cols = [
        "case_no",
        "exchange_id",
        "expediente",
        "legislature",
        "date",
        "session_id",
        "ds_id",
        "questioner_id",
        "questioner_name",
        "parliamentary_group",
        "answerer_id",
        "registered_question",
        "q1_text",
        "r1_text",
        "parlamint_document_id",
        "q1_utterance_id",
        "r1_utterance_id",
        "link_status",
        "link_evidence",
        "congreso_url",
        "source_version",
        "formation_vote_alignment",
        "primary_alignment",
        "question_topic",
        "question_form",
        "question_confrontational",
        "questioner",
    ]
    corpus = main[[c for c in corpus_cols if c in main.columns]].copy()
    assert_no_outcome_columns(corpus)

    corpus_parquet = MAIN_PRIVATE / "MAIN_FRAME_CORPUS_FULL.parquet"
    corpus_csv = MAIN_PRIVATE / "MAIN_FRAME_CORPUS_FULL.csv"
    corpus.to_parquet(corpus_parquet, index=False)
    corpus.to_csv(corpus_csv, index=False)

    public_cols = [
        c
        for c in [
            "case_no",
            "exchange_id",
            "expediente",
            "legislature",
            "date",
            "session_id",
            "ds_id",
            "questioner_id",
            "parliamentary_group",
            "answerer_id",
            "parlamint_document_id",
            "q1_utterance_id",
            "r1_utterance_id",
            "link_status",
            "formation_vote_alignment",
            "primary_alignment",
            "question_topic",
            "question_form",
            "question_confrontational",
            "source_version",
        ]
        if c in corpus.columns
    ]
    public = corpus[public_cols].copy()
    public_path = DERIVED_DIR / "main_frame_metadata_preannotation.csv"
    public_parquet = DERIVED_DIR / "main_frame_metadata_preannotation.parquet"
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    public.to_csv(public_path, index=False)
    public.to_parquet(public_parquet, index=False)

    volumes = assign_volumes(corpus["case_no"].tolist(), VOLUMES_DEFAULT)
    volume_path = MAIN_PRIVATE / "MAIN_FRAME_VOLUME_PLAN.json"
    volume_path.write_text(json.dumps(volumes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest = {
        "phase": "6A",
        "status": "pre_outcome_main_frame_frozen",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "n": int(len(corpus)),
        "phase0_probes_excluded_n": 3,
        "linkage_qa_restored_n": 30,
        "linkage_qa_exchange_ids": qa_ids,
        "completeness": completeness,
        "duplicates": {
            "exchange_id": int(corpus["exchange_id"].duplicated().sum()),
            "expediente_date_questioner": int(
                corpus.duplicated(["expediente", "date", "questioner_id"]).sum()
            ),
        },
        "volume_plan": volumes,
        "corpus_private_parquet": str(corpus_parquet.relative_to(PROJECT_ROOT)),
        "corpus_private_csv": str(corpus_csv.relative_to(PROJECT_ROOT)),
        "public_metadata_csv": str(public_path.relative_to(PROJECT_ROOT)),
        "corpus_sha256": _sha256_file(corpus_parquet),
        "public_sha256": _sha256_file(public_path),
        "reply_status_present": False,
        "human_packets_issued": False,
        "notes": (
            "Census of eligible XIV exchanges minus Phase-0 probes. "
            "Linkage-QA units restored after contamination audit. "
            "No reply_status labels."
        ),
    }
    manifest_path = PROTOCOL_DIR / "main_frame_manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (MAIN_PRIVATE / "MAIN_FRAME_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    unit_list = corpus[["case_no", "exchange_id", "expediente", "date", "questioner_id"]].copy()
    unit_list["volume"] = unit_list["case_no"].map(
        {c: v["volume"] for v in volumes["volumes"] for c in v["case_nos"]}
    )
    unit_list.to_csv(MAIN_PRIVATE / "MAIN_FRAME_UNIT_LIST.csv", index=False)

    return {
        "n": len(corpus),
        "manifest": manifest,
        "corpus_path": corpus_parquet,
        "public_path": public_path,
        "completeness": completeness,
        "volumes": volumes,
        "pool_summary": summary,
    }


def _completeness_report(df: pd.DataFrame) -> dict:
    def empty(series: pd.Series) -> pd.Series:
        s = series.astype(str).str.strip()
        return series.isna() | s.eq("") | s.str.lower().eq("nan")

    miss_reg = int(empty(df["registered_question"]).sum())
    miss_q1 = int(empty(df["q1_text"]).sum())
    miss_r1 = int(empty(df["r1_text"]).sum())
    n = len(df)
    n_complete = int((~empty(df["registered_question"]) & ~empty(df["q1_text"]) & ~empty(df["r1_text"])).sum())
    return {
        "n_total": n,
        "n_complete": n_complete,
        "n_missing_registered": miss_reg,
        "n_missing_oral": miss_q1,
        "n_missing_r1": miss_r1,
    }


def assign_volumes(case_nos: list[int], sizes: tuple[int, ...] = VOLUMES_DEFAULT) -> dict:
    if sum(sizes) != len(case_nos):
        raise ValueError(f"volume sizes {sizes} must sum to {len(case_nos)}")
    volumes = []
    i = 0
    for vol_i, size in enumerate(sizes, start=1):
        chunk = case_nos[i : i + size]
        volumes.append(
            {
                "volume": vol_i,
                "n": len(chunk),
                "case_nos": chunk,
                "case_no_first": chunk[0],
                "case_no_last": chunk[-1],
            }
        )
        i += size
    return {
        "scheme": "fixed_order_contiguous",
        "rationale": (
            "Split by fixed case_no order only (date/expediente/exchange_id). "
            "No outcome-based splitting. Target ~24–25 cases per volume for "
            "human burden (~one sitting of coding)."
        ),
        "recommended": "4 volumes (25+24+24+24)",
        "volumes": volumes,
    }


def load_main_corpus() -> pd.DataFrame:
    path = MAIN_PRIVATE / "MAIN_FRAME_CORPUS_FULL.parquet"
    df = pd.read_parquet(path)
    assert_no_outcome_columns(df)
    return df
