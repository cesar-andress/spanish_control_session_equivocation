"""Phase 6C: failed Round-2 result preserved; diagnostic recorded; no v0.4/main."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

REP = PROJECT_ROOT / "_internal" / "reports"
R2 = DATA_PRIVATE / "calibration" / "round2"


def test_failed_result_freeze_and_diagnostic_exist():
    freeze = json.loads((REP / "ROUND2_FAILED_RESULT_FREEZE.json").read_text())
    assert freeze["n_complete_pairs"] == 20
    assert freeze["v04_written"] is False
    assert freeze["metrics"]["krippendorff_alpha_nominal"] < 0.67
    assert freeze["metrics"]["cohen_kappa_explicit_vs_rest"] < 0.67
    diag = (REP / "ROUND2_MEASUREMENT_FAILURE_DIAGNOSTIC.md").read_text()
    assert "Gate C" in diag or "FAIL" in diag
    assert "Redesign option 1" in diag or "Option 1" in diag


def test_round2_labels_not_altered_to_force_pass():
    agr = json.loads((REP / "CALIBRATION_ROUND2_AGREEMENT.json").read_text())
    assert agr["locked_rule_decision"]["gate"] == "C"
    codes = pd.read_csv(R2 / "CALIBRATION_ROUND2_CODES.csv")
    assert len(codes) == 20
    assert int(codes["pair_complete"].sum()) == 20


def test_no_v04_no_xiv_reply_labels():
    assert not (PROTOCOL_DIR / "reply_status_codebook_v0.4.md").is_file()
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if pool.is_file():
        df = pd.read_parquet(pool)
        assert "reply_status" not in df.columns
