"""Phase 7A: binary redesign draft + fresh validation frame gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import yaml

from scse.build_binary_validation_frame import SEED_BINARY_VAL, SEED_SOURCE_STRING
from scse.build_calibration_round2 import (
    load_development_exclusions,
    load_round1_exclusions,
    load_xiv_and_qa_exclusions,
    normalize_text,
)
from scse.build_binary_validation_frame import load_round2_exclusions
from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

VAL = DATA_PRIVATE / "validation" / "binary_v1"
REP = PROJECT_ROOT / "_internal" / "reports"
R2_CODES = DATA_PRIVATE / "calibration" / "round2" / "CALIBRATION_ROUND2_CODES.csv"


def test_no_v04_new_instrument_lineage():
    assert not (PROTOCOL_DIR / "reply_status_codebook_v0.4.md").is_file()
    draft = PROTOCOL_DIR / "direct_resolution_codebook_v1.0-draft.md"
    assert draft.is_file()
    text = draft.read_text(encoding="utf-8")
    assert "resolución directa" in text.lower() or "resolucion directa" in text.lower()
    assert "Gate C" in text or "falló" in text or "fallo" in text


def test_round2_codes_unchanged_hash():
    # Frozen after case-5 completion re-ingest (Phase 6C)
    expected = "b3f5ef34733da4f588994ad27b8e960e508292361f40d3afaafc8a85f562b29e"
    got = hashlib.sha256(R2_CODES.read_bytes()).hexdigest()
    assert got == expected


def test_fresh_frame_zero_human_and_xiv_overlap():
    frame = pd.read_csv(VAL / "BINARY_VALIDATION_FRESH_FRAME.csv")
    sel = pd.read_csv(VAL / "BINARY_VALIDATION_N12_AUDIT.csv")
    assert len(frame) >= 12
    assert len(sel) == 12
    r1 = load_round1_exclusions()
    r2 = load_round2_exclusions()
    dev = load_development_exclusions()
    xq = load_xiv_and_qa_exclusions()
    exposed_q1 = (
        r1["q1"] | r2["q1"] | dev["q1"] | xq["xiv_q1"] | xq["qa_q1"] | xq["phase0_q1"]
    )
    assert set(frame["q1_utterance_id"].astype(str)).isdisjoint(exposed_q1)
    assert set(sel["q1_utterance_id"].astype(str)).isdisjoint(exposed_q1)
    pool = pd.read_parquet(DATA_PRIVATE / "eligible_pool_full.parquet")
    xiv_q1 = set(pool.loc[pool["legislature"] == "XIV", "q1_utterance_id"].astype(str))
    assert set(frame["q1_utterance_id"].astype(str)).isdisjoint(xiv_q1)


def test_prospective_gate_locked():
    gate = json.loads((VAL / "BINARY_VALIDATION_PROSPECTIVE_GATE.json").read_text())
    assert gate["kappa_threshold"] == 0.67
    assert gate["raw_agreement_threshold_n"] == 10
    assert gate["raw_agreement_threshold_of"] == 12
    assert gate["automatic_further_round_on_fail"] is False
    assert gate["locked_before_human_returns"] is True
    assert gate["seed"] == SEED_BINARY_VAL
    # Phase 7B sets annotator_docx_generated True once packets are issued
    assert "annotator_docx_generated" in gate


def test_seed_and_manifest():
    seeds = yaml.safe_load((PROTOCOL_DIR / "seeds.yaml").read_text(encoding="utf-8"))
    assert seeds["seeds"]["binary_validation_v1"] == SEED_BINARY_VAL
    man = json.loads((VAL / "BINARY_VALIDATION_MANIFEST.json").read_text())
    assert man["n_untouched_after_exclusions"] >= 12
    assert man["untouched_before_expansion"] == 4
    assert man["xiv_reply_labels_created"] is False
    assert man["ai_labels_created"] is False
    assert SEED_SOURCE_STRING in man["seed_source_string"]


def test_no_xiv_reply_labels_frame_reports_exist():
    pool = pd.read_parquet(DATA_PRIVATE / "eligible_pool_full.parquet")
    assert "reply_status" not in pool.columns
    assert "direct_resolution" not in pool.columns
    assert (REP / "FRESH_BINARY_VALIDATION_FRAME_AUDIT.md").is_file()
    assert (REP / "BINARY_REDESIGN_RATIONALE.md").is_file()


def test_selection_did_not_require_r1_meta_flag():
    man = json.loads((VAL / "BINARY_VALIDATION_MANIFEST.json").read_text())
    assert man["selection"]["r1_not_inspected_for_selection"] is True
    assert man["selection"]["single_seed_no_cherry_pick"] is True
