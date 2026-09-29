"""Pinned scientific constants for Phase-2 eligibility (XIV NARROW)."""

from __future__ import annotations

from datetime import date

# Accepted Phase-0 NARROW scope
LEGISLATURE = "XIV"
LEGISLATURE_START = date(2019, 12, 3)
PARLAMINT_COVERAGE_END = date(2023, 2, 23)

PARLAMINT_RELEASE = "5.0"
PARLAMINT_HANDLE = "http://hdl.handle.net/11356/2004"
PARLAMINT_ARCHIVE = "ParlaMint-ES.tgz"
PARLAMINT_MD5 = "2ba1216f3fcf1300ee74f50efe42ec6a"
# Observed SHA-256 of the CLARIN.SI ParlaMint-ES.tgz matching published MD5
PARLAMINT_SHA256 = "b101c066a7770c80fcd835cc39282f29acd32883887306017cbd454c4d6eef68"

PM_PERSON_ID = "PedroSánchezPérezCastejón"
PM_WHO = f"#{PM_PERSON_ID}"

# Phase-0 feasibility probe expedientes (exclude from all future samples)
PHASE0_PROBE_EXPEDIENTES = frozenset(
    {
        "180/000128",
        "180/000041",
        "180/000047",
        "180/000123",
        "180/000784",
    }
)

# SPDB previous-paper sitting dates (documented local TEI slice)
SPDB_SITTING_DATES = frozenset(
    {
        "2017-09-19",
        "2017-11-28",
        "2017-11-30",
        "2020-11-12",
        "2023-02-23",
    }
)

CONGRESO_USER_AGENT = (
    "spanish-control-session-equivocation/0.0.0 "
    "(research; contact: cesar.andres@unir.net)"
)

ELIGIBILITY_RULE_VERSION = "phase2-xiv-v1"
