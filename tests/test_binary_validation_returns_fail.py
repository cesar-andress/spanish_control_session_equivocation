"""Binary validation returns: locked gate FAIL; no v1.0; no main outcomes."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

VAL = DATA_PRIVATE / "validation" / "binary_v1"
REP = PROJECT_ROOT / "_internal" / "reports"
RET = PROJECT_ROOT / "_internal" / "binary_validation" / "returns"


def test_returns_archived_and_complete():
    assert (RET / "validacion_binaria_daniel_returned.docx").is_file()
    assert (RET / "validacion_binaria_jose_jaime_returned.docx").is_file()
    codes = pd.read_csv(VAL / "BINARY_VALIDATION_CODES.csv")
    assert len(codes) == 12
    assert bool(codes["pair_complete"].all()) is True


def test_locked_gate_fail():
    agr = json.loads((REP / "BINARY_VALIDATION_AGREEMENT.json").read_text())
    gate = agr["locked_gate_decision"]
    assert gate["gate"] == "FAIL"
    assert gate["passed"] is False
    assert gate["n_agree"] == 8
    assert gate["kappa"] < 0.67
    assert gate["raw_ok"] is False
    assert gate["kappa_ok"] is False
    assert gate["automatic_further_round_on_fail"] is False
    assert gate["thresholds_not_optimised_after_returns"] is True
    assert set(agr["disagree_case_nos"]) == {1, 4, 7, 11}


def test_no_v1_freeze_no_xiv_labels():
    assert not (PROTOCOL_DIR / "direct_resolution_codebook_v1.0.md").is_file()
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if pool.is_file():
        df = pd.read_parquet(pool)
        assert "direct_resolution" not in df.columns
        assert "reply_status" not in df.columns
