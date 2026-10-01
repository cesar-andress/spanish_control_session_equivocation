"""Schema validation for the Phase-2 eligible pool."""

from __future__ import annotations

from datetime import date

import pandas as pd

from scse.config import (
    LEGISLATURE_START,
    PARLAMINT_COVERAGE_END,
    PHASE0_PROBE_EXPEDIENTES,
    PM_WHO,
)

VALID_LINK_STATUS = {"exact", "high_confidence", "ambiguous", "unlinked"}
FORBIDDEN_COLUMNS = {
    "reply_status",
    "equivocation_type",
    "outcome",
    "formation_vote_alignment",
    "human_label",
    "answer_quality",
}


class PoolValidationError(ValueError):
    pass


def validate_pool_dataframe(df: pd.DataFrame) -> None:
    errors: list[str] = []

    if df["exchange_id"].duplicated().any():
        errors.append("duplicate exchange_id")

    forbidden = FORBIDDEN_COLUMNS & set(df.columns)
    if forbidden:
        errors.append(f"forbidden outcome columns present: {sorted(forbidden)}")

    if not set(df["link_status"].dropna()) <= VALID_LINK_STATUS:
        errors.append(f"invalid link_status values: {set(df['link_status']) - VALID_LINK_STATUS}")

    eligible = df[df["eligible"]]
    if eligible.empty:
        errors.append("no eligible rows")

    for _, row in eligible.iterrows():
        if not str(row.get("registered_question") or "").strip():
            errors.append(f"{row['exchange_id']}: eligible but empty registered_question")
        if not str(row.get("q1_text") or "").strip():
            errors.append(f"{row['exchange_id']}: eligible but empty q1_text")
        if not str(row.get("r1_text") or "").strip():
            errors.append(f"{row['exchange_id']}: eligible but empty r1_text")
        if row.get("answerer_id") != PM_WHO:
            errors.append(f"{row['exchange_id']}: answerer_id not PM")
        if not row.get("q1_utterance_id") or not row.get("r1_utterance_id"):
            errors.append(f"{row['exchange_id']}: missing utterance ids")
        if row.get("link_status") not in {"exact", "high_confidence"}:
            errors.append(f"{row['exchange_id']}: eligible with weak link_status")
        try:
            d = date.fromisoformat(str(row["date"]))
        except Exception:
            errors.append(f"{row['exchange_id']}: invalid date")
            continue
        if d < LEGISLATURE_START or d > PARLAMINT_COVERAGE_END:
            errors.append(f"{row['exchange_id']}: date outside XIV/ParlaMint window")

    # Phase-0 / QA must not remain sampling-eligible
    bad_probe = df[
        df["expediente"].isin(PHASE0_PROBE_EXPEDIENTES)
        & df["eligible"]
        & ~df["exclude_from_sampling"].fillna(False)
    ]
    if not bad_probe.empty:
        errors.append("phase0 probe rows still sampling-eligible")

    qa = df[df["sampling_exclusion_reason"].eq("linkage_QA") & ~df["exclude_from_sampling"]]
    if not qa.empty:
        errors.append("linkage_QA rows not marked exclude_from_sampling")

    dev = df[
        df["sampling_exclusion_reason"].eq("development_codebook")
        & ~df["exclude_from_sampling"].fillna(False)
    ]
    if not dev.empty:
        errors.append("development_codebook rows not marked exclude_from_sampling")

    if errors:
        raise PoolValidationError("; ".join(errors[:20]) + (f" (+{len(errors)-20} more)" if len(errors) > 20 else ""))


def main() -> int:
    from scse.paths import DATA_PRIVATE

    path = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not path.is_file():
        print(f"missing {path}")
        return 2
    validate_pool_dataframe(pd.read_parquet(path))
    print("pool schema OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
