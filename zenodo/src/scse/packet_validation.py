"""Validate annotator packet rows for required linguistic fields.

From codebook v0.3 onwards, every ordinary annotation unit must present:

1. registered_question (pregunta registrada)
2. Q1 (pregunta oral)
3. R1 (primera respuesta del Presidente del Gobierno)

Empty or whitespace-only values fail validation unless the row is explicitly
flagged as registered-unavailable before annotation.
"""

from __future__ import annotations

from typing import Any, Mapping

import pandas as pd

REQUIRED_TEXT_FIELDS = ("registered_question", "Q1", "R1")
FORBIDDEN_METADATA_SUBSTRINGS = (
    "party",
    "parliamentary_group",
    "formation_vote",
    "primary_alignment",
    "alignment",
    "questioner",
    "legislature",
    "vote",
)

# Optional explicit flag when the registered question is genuinely unavailable.
REGISTERED_UNAVAILABLE_FLAG = "registered_unavailable"


class PacketValidationError(ValueError):
    """Raised when a packet row or frame violates presentation rules."""


def _is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    return str(value).strip() == ""


def validate_packet_row(
    row: Mapping[str, Any],
    *,
    allow_registered_unavailable: bool = False,
) -> None:
    """Validate one packet row.

    Parameters
    ----------
    row:
        Mapping with at least registered_question, Q1, R1.
    allow_registered_unavailable:
        If True and row[REGISTERED_UNAVAILABLE_FLAG] is truthy, an empty
        registered_question is permitted, but Q1 and R1 remain required.
    """
    errors: list[str] = []
    unit = str(row.get("unit_id") or "<unknown>")

    flagged = bool(row.get(REGISTERED_UNAVAILABLE_FLAG))
    if flagged and not allow_registered_unavailable:
        errors.append(
            f"{unit}: registered_unavailable set but allow_registered_unavailable=False"
        )

    for field in REQUIRED_TEXT_FIELDS:
        if field not in row:
            errors.append(f"{unit}: missing field {field}")
            continue
        blank = _is_blank(row.get(field))
        if field == "registered_question" and flagged and allow_registered_unavailable:
            continue
        if blank:
            errors.append(f"{unit}: empty required field {field}")

    for key in row.keys():
        low = str(key).lower()
        if any(s in low for s in FORBIDDEN_METADATA_SUBSTRINGS):
            errors.append(f"{unit}: forbidden metadata column {key}")

    if errors:
        raise PacketValidationError("; ".join(errors))


def validate_packet_frame(
    df: pd.DataFrame,
    *,
    allow_registered_unavailable: bool = False,
) -> None:
    """Validate every row of a packet DataFrame."""
    missing_cols = [c for c in REQUIRED_TEXT_FIELDS if c not in df.columns]
    if missing_cols:
        raise PacketValidationError(
            f"packet missing required columns: {missing_cols}"
        )
    for col in df.columns:
        low = str(col).lower()
        if any(s in low for s in FORBIDDEN_METADATA_SUBSTRINGS):
            raise PacketValidationError(f"forbidden metadata column: {col}")

    errors: list[str] = []
    for _, row in df.iterrows():
        try:
            validate_packet_row(
                row.to_dict(),
                allow_registered_unavailable=allow_registered_unavailable,
            )
        except PacketValidationError as exc:
            errors.append(str(exc))
    if errors:
        head = "; ".join(errors[:20])
        more = f" (+{len(errors) - 20} more)" if len(errors) > 20 else ""
        raise PacketValidationError(head + more)
