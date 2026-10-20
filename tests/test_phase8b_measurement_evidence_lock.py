"""Phase 8B: measurement-paper evidence lock gates."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scse.measurement_evidence import (
    BOOTSTRAP_SEED,
    build_human_evidence_67,
    kappa_max_from_labels,
    max_agreement_given_marginals,
)
from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

OUT = DATA_PRIVATE / "measurement_paper"
REP = PROJECT_ROOT / "_internal" / "reports"


def test_human_evidence_67_counts_and_labels():
    df = build_human_evidence_67()
    assert len(df) == 67
    assert df["exercise"].value_counts().to_dict() == {
        "development": 15,
        "calibration_round1": 20,
        "calibration_round2": 20,
        "binary_validation": 12,
    }
    # Original label systems preserved (no forced collapse of binary into 3-way)
    bin_rows = df[df.exercise == "binary_validation"]
    assert set(bin_rows["label_system"]) == {"binary_direct_resolution"}
    assert set(bin_rows["daniel_label"]).issubset(
        {"direct_resolution_yes", "direct_resolution_no"}
    )
    three = df[df.exercise != "binary_validation"]
    assert (three["label_system"] == "three_category").all()


def test_csv_and_lock_artifacts():
    csv = OUT / "HUMAN_EVIDENCE_67.csv"
    lock = OUT / "MEASUREMENT_PAPER_EVIDENCE_LOCK.json"
    report = REP / "MEASUREMENT_PAPER_EVIDENCE_LOCK.md"
    assert csv.is_file() and lock.is_file() and report.is_file()
    df = pd.read_csv(csv)
    assert len(df) == 67
    p = json.loads(lock.read_text(encoding="utf-8"))
    assert p["human_evidence_n"] == 67
    assert p["xiv_frame_n_verified"] == 100
    assert p["bootstrap"]["seed"] == BOOTSTRAP_SEED
    assert p["disagreement_inventory_n"] == 22
    assert p["stable_coder_severity_trait_supported"] is False
    assert p["no_xiv_reply_labels"] is True
    assert p["manuscript_not_rewritten"] is True


def test_binary_kappa_equals_kappa_max():
    p = json.loads((OUT / "MEASUREMENT_PAPER_EVIDENCE_LOCK.json").read_text())
    b = p["binary_validation"]
    assert b["daniel_yes"] == 11
    assert b["jose_jaime_yes"] == 7
    assert b["n_agree"] == 8
    assert b["observed_equals_kappa_max"] is True
    assert abs(b["cohen_kappa"] - b["kappa_max"]["kappa_max"]) < 1e-12


def test_kappa_max_function():
    assert max_agreement_given_marginals([11, 1], [7, 5]) == 8
    a = ["yes"] * 11 + ["no"]
    b = ["yes"] * 7 + ["no"] * 5
    # align length 12: need b with 7 yes and 5 no - but pairing matters for kappa_max
    # kappa_max uses marginals only
    km = kappa_max_from_labels(
        ["y"] * 11 + ["n"],
        ["y"] * 7 + ["n"] * 5,
        ("y", "n"),
    )
    assert km["max_agreements"] == 8
    assert abs(km["po_max"] - 8 / 12) < 1e-12


def test_round1_18_vs_20_documented():
    p = json.loads((OUT / "MEASUREMENT_PAPER_EVIDENCE_LOCK.json").read_text())
    assert p["round1_initial_18"]["n"] == 18
    assert p["round1_final_20"]["n"] == 20
    assert p["round1_initial_18"]["excluded_case_nos"] == [5, 10]


def test_no_xiv_reply_outcomes_no_v10_freeze():
    pool = pd.read_parquet(DATA_PRIVATE / "eligible_pool_full.parquet")
    assert "reply_status" not in pool.columns
    assert "direct_resolution" not in pool.columns
    assert not (PROTOCOL_DIR / "direct_resolution_codebook_v1.0.md").is_file()
    main = pd.read_csv(DATA_PRIVATE / "main" / "MAIN_FRAME_CORPUS_FULL.csv")
    assert len(main) == 100
    assert "reply_status" not in main.columns
