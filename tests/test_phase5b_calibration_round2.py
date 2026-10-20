"""Phase 5B Calibration Round 2 gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import yaml

from scse.build_calibration_round2 import (
    SEED_DIGEST,
    SEED_ROUND2,
    SEED_SOURCE_STRING,
    normalize_text,
)
from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

R2 = DATA_PRIVATE / "calibration" / "round2"
R1 = DATA_PRIVATE / "calibration" / "round1"
HUMAN = PROJECT_ROOT / "_internal" / "calibration_round2"


def test_round2_seed_derivation():
    assert (
        SEED_SOURCE_STRING
        == "spanish_control_session_equivocation|calibration_round2|fresh_diversity_draw"
    )
    assert hashlib.sha256(SEED_SOURCE_STRING.encode()).hexdigest() == SEED_DIGEST
    assert SEED_ROUND2 == int(SEED_DIGEST[:16], 16) % (2**31 - 1)
    assert SEED_ROUND2 == 322720977


def test_round2_packet_exists_and_valid():
    pkt = pd.read_csv(R2 / "CALIBRATION_ROUND2_PACKET_BLINDED.csv")
    aud = pd.read_csv(R2 / "CALIBRATION_ROUND2_AUDIT.csv")
    assert len(pkt) == 20
    assert list(pkt["case_no"]) == list(range(1, 21))
    assert pkt["unit_id"].nunique() == 20
    assert aud["q1_utterance_id"].nunique() == 20
    assert (pkt["registered_question"].astype(str).str.strip() != "").all()
    assert (pkt["Q1"].astype(str).str.strip() != "").all()
    assert (pkt["R1"].astype(str).str.strip() != "").all()
    assert pkt["Q1"].map(normalize_text).duplicated().sum() == 0


def test_round2_no_overlap_round1_or_development():
    r2 = pd.read_csv(R2 / "CALIBRATION_ROUND2_AUDIT.csv")
    r1 = pd.read_csv(R1 / "CALIBRATION_ROUND1_AUDIT.csv")
    dev = pd.read_csv(
        DATA_PRIVATE / "development" / "out_of_pool" / "DEVELOPMENT_SET_AUDIT.csv"
    )
    assert set(r2["unit_id"]).isdisjoint(set(r1["unit_id"]))
    assert set(r2["q1_utterance_id"].astype(str)).isdisjoint(
        set(r1["q1_utterance_id"].astype(str))
    )
    assert set(r2["q1_utterance_id"].astype(str)).isdisjoint(
        set(dev["q1_utterance_id"].astype(str))
    )


def test_round2_no_xiv_overlap():
    r2 = pd.read_csv(R2 / "CALIBRATION_ROUND2_AUDIT.csv")
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not pool.is_file():
        return
    xiv = pd.read_parquet(pool)
    xiv = xiv[xiv["legislature"] == "XIV"]
    assert set(r2["q1_utterance_id"].astype(str)).isdisjoint(
        set(xiv["q1_utterance_id"].astype(str))
    )


def test_round2_human_packets_exist():
    assert (HUMAN / "01_REVISION_CONJUNTA_CASOS_5_6_7_10.docx").is_file()
    assert (HUMAN / "02_calibracion_ronda2_Daniel.docx").is_file()
    assert (HUMAN / "02_calibracion_ronda2_Jose_Jaime.docx").is_file()
    assert (HUMAN / "EMAIL_UNICO_CALIBRACION_FINAL.txt").is_file()


def test_round2_manifest_and_seeds():
    man = yaml.safe_load(
        (PROTOCOL_DIR / "calibration_round2_manifest.yaml").read_text(encoding="utf-8")
    )
    assert man["n_units"] == 20
    assert man["seed"] == SEED_ROUND2
    assert man["round3_planned"] is False
    assert man["final_planned_calibration_round"] is True
    seeds = yaml.safe_load((PROTOCOL_DIR / "seeds.yaml").read_text(encoding="utf-8"))
    assert seeds["seeds"]["calibration"] == 2071684612
    assert seeds["seeds"]["calibration_round2"] == SEED_ROUND2
    assert seeds["seeds"]["main_sample"] is None


def test_round1_packet_unchanged():
    # Frozen Round-1 scientific packet from Phase 5A
    expected = "66c9f8f1ecbb34623ca05d09cfce9539bfa7339d49b8f6bc32a8b5c6d85723a6"
    got = hashlib.sha256(
        (R1 / "CALIBRATION_ROUND1_PACKET_BLINDED.csv").read_bytes()
    ).hexdigest()
    assert got == expected


def test_no_xiv_reply_outcomes_still():
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not pool.is_file():
        return
    df = pd.read_parquet(pool)
    assert "reply_status" not in df.columns


def test_diversity_summary_recorded():
    div = json.loads((R2 / "CALIBRATION_ROUND2_DIVERSITY.json").read_text())
    assert div["n"] == 20
    assert div["reply_labels_observed"] is False
    assert div["n_topics"] >= 4
    assert div["n_forms"] >= 2
    assert "max_per_questioner_le_2" in div["targets_missed"] or div[
        "targets_achieved"
    ]["max_per_questioner_le_2"]
