"""Round-2 returns ingested; locked A/B/C → Gate C STOP."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

R2 = DATA_PRIVATE / "calibration" / "round2"
RET = PROJECT_ROOT / "_internal" / "calibration_round2" / "returns"
REPORTS = PROJECT_ROOT / "_internal" / "reports"


def test_round2_codes_and_returns_present():
    codes = pd.read_csv(R2 / "CALIBRATION_ROUND2_CODES.csv")
    assert len(codes) == 20
    assert list(codes["case_no"]) == list(range(1, 21))
    assert (RET / "calibracion_ronda2_daniel_returned.docx").is_file()
    assert (RET / "calibracion_ronda2_jose_jaime_returned.docx").is_file()
    assert (RET / "01_REVISION_CONJUNTA_CASOS_5_6_7_10_returned.docx").is_file()
    assert (R2 / "CALIBRATION_ROUND2_RETURNS.json").is_file()


def test_case_5_incomplete_not_imputed():
    codes = pd.read_csv(R2 / "CALIBRATION_ROUND2_CODES.csv")
    row = codes.loc[codes["case_no"] == 5].iloc[0]
    assert bool(row["pair_complete"]) is False
    assert pd.isna(row["jose_jaime_reply_status"]) or str(
        row["jose_jaime_reply_status"]
    ).strip() in {"", "nan"}
    assert "missing_reply_status" in str(row["jose_jaime_issues"])


def test_agreement_gate_c_locked():
    agr = json.loads((REPORTS / "CALIBRATION_ROUND2_AGREEMENT.json").read_text())
    gate = agr["locked_rule_decision"]
    assert gate["gate"] == "C"
    assert gate["rule_locked_before_returns"] is True
    assert gate["thresholds_not_optimised_after_returns"] is True
    assert gate["krippendorff_alpha_nominal"] < 0.67
    assert gate["cohen_kappa_explicit_vs_rest"] < 0.67
    assert agr["n_complete_pairs"] == 19
    assert agr["n_incomplete_pairs"] == 1
    assert 5 in agr["incomplete_case_nos"]


def test_no_codebook_v04_and_no_main_outcomes():
    assert not (PROTOCOL_DIR / "reply_status_codebook_v0.4.md").is_file()
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if pool.is_file():
        df = pd.read_parquet(pool)
        assert "reply_status" not in df.columns
    stop = (REPORTS / "CALIBRATION_ROUND2_GATE_C_STOP.md").read_text()
    assert "Gate C" in stop or "GATE C" in stop
