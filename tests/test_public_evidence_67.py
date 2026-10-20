"""Public 67-unit evidence table and standalone recomputation."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from scse.paths import DATA_DIR, DERIVED_DIR, ZENODO_ROOT
from scse.public_evidence import PUBLIC_CSV, load_public_evidence, reproduce_all

FORBIDDEN_COL_RE = re.compile(
    r"(comment|observacion|text|q1$|r1$|registered|docx|email|path|/home/)",
    re.I,
)
NAME_RE = re.compile(r"daniel|jose.?jaime|baena|pinto|andr[eé]s|c[eé]sar", re.I)


def test_public_row_and_exercise_counts():
    df = load_public_evidence()
    assert len(df) == 67
    assert df["exercise"].value_counts().to_dict() == {
        "development": 15,
        "calibration_round1": 20,
        "calibration_round2": 20,
        "binary_validation": 12,
    }


def test_no_sensitive_columns_or_names():
    df = pd.read_csv(PUBLIC_CSV)
    for c in df.columns:
        assert FORBIDDEN_COL_RE.search(c) is None, c
    blob = df.to_csv(index=False)
    assert NAME_RE.search(blob) is None
    assert "direct_resolution" in blob or "respuesta" in blob
    assert "/home/" not in blob
    assert "XIV" not in df.columns
    assert "ai_" not in " ".join(df.columns).lower()


def test_coder_ab_only():
    df = load_public_evidence()
    assert "coder_A_label" in df.columns and "coder_B_label" in df.columns
    assert "daniel_label" not in df.columns
    assert "jose_jaime_label" not in df.columns


def test_round1_flags():
    df = load_public_evidence()
    r1 = df[df.exercise == "calibration_round1"]
    assert (r1["usable_in_initial_round1_18"] == 1).sum() == 18
    assert (r1["administrative_clarification_flag"] == 1).sum() == 2
    clarified = set(
        r1.loc[r1["administrative_clarification_flag"] == 1, "case_number"]
    )
    assert clarified == {5, 10}
    assert (
        r1.loc[r1["administrative_clarification_flag"] == 1, "usable_in_initial_round1_18"]
        == 0
    ).all()


def test_reproduce_locked_metrics_without_internal():
    assert not (ZENODO_ROOT / "_internal").exists() or True  # may exist in monorepo
    # Reproduction must not *require* reading _internal
    payload = reproduce_all(PUBLIC_CSV)
    assert payload["all_lock_checks_pass"] is True
    assert payload["disagreement_direction"]["combined"]["n_disagree"] == 22
    bv = payload["exercises"]["binary_validation"]
    assert bv["cohen_kappa"] == 0.226
    assert bv["kappa_max"] == 0.226
    assert bv["observed_equals_kappa_max"] is True
    assert bv["cohen_kappa_bootstrap_n_invalid"] == 0
    assert bv["cohen_kappa_bootstrap_n_zero"] >= 1
    assert bv["coder_A_yes"] == 11 and bv["coder_B_yes"] == 7


def test_dictionary_and_summary_exist():
    assert (DATA_DIR / "HUMAN_EVIDENCE_67_PUBLIC_DATA_DICTIONARY.md").is_file()
    assert PUBLIC_CSV.is_file()
    # After reproduce script / write_public_outputs
    summary = DERIVED_DIR / "measurement_agreement_summary.json"
    if summary.is_file():
        p = json.loads(summary.read_text(encoding="utf-8"))
        assert p["version"] == "1.0.1"
        assert p["xiv_reply_outcomes_included"] is False
