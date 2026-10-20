"""Phase 5A Calibration Round 1 gates."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import pandas as pd
import pytest
import yaml

from scse.calibration_metrics import summarize_round1
from scse.packet_validation import validate_packet_frame
from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

XIV_START = date(2019, 12, 3)
XIV_END = date(2023, 2, 23)
V02_SHA256 = "2b0c0398a7939d5ed45ff95ee66afb32d2ed48524d6db8819b7ad024e8eba823"
DANIEL_SHA256 = "2ff07e8d57d16798af4bc399d0c92c6cb3b0603d921f65253460d62bbc2bb1e1"
JOSE_SHA256 = "97bb754fdfb317bf48d2a8f090978613543e02748094baa5bc2bde46ea0b6930"

SEED_SOURCE = (
    "spanish_control_session_equivocation|calibration_round1|reply_status_v0.3"
)
EXPECTED_SEED = int(hashlib.sha256(SEED_SOURCE.encode()).hexdigest()[:16], 16) % (
    2**31 - 1
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v02_and_development_solutions_unchanged():
    assert _sha(PROTOCOL_DIR / "reply_status_codebook_v0.2.md") == V02_SHA256
    sol = PROJECT_ROOT / "_internal" / "development" / "solutions"
    assert _sha(sol / "daniel_pinto_solutions.json") == DANIEL_SHA256
    assert _sha(sol / "jose_jaime_baena_solutions.json") == JOSE_SHA256


def test_codebook_v03_is_calibration_version():
    text = (PROTOCOL_DIR / "reply_status_codebook_v0.3.md").read_text(encoding="utf-8")
    assert "VERSIÓN DE CALIBRACIÓN" in text or "CALIBRACIÓN" in text
    assert "0.3.0" in text
    assert "no congelado" in text.lower() or "NO CONGELADO" in text or "no congelado" in text


def test_calibration_seed_derivation_and_seeds_yaml():
    assert EXPECTED_SEED == 2071684612
    seeds = yaml.safe_load((PROTOCOL_DIR / "seeds.yaml").read_text(encoding="utf-8"))
    assert seeds["seeds"]["calibration"] == EXPECTED_SEED
    assert seeds["seeds"]["main_sample"] is None
    assert seeds["seeds"]["bootstrap"] is None


def test_calibration_round1_manifest_and_packet():
    man = yaml.safe_load(
        (PROTOCOL_DIR / "calibration_round1_manifest.yaml").read_text(encoding="utf-8")
    )
    assert man["n_units"] == 20
    assert man["seed"] == EXPECTED_SEED
    assert len(man["unit_ids"]) == 20
    assert all(str(u).startswith("cal1_") for u in man["unit_ids"])

    pkt = pd.read_csv(
        DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_PACKET_BLINDED.csv"
    )
    assert len(pkt) == 20
    validate_packet_frame(pkt[["unit_id", "registered_question", "Q1", "R1"]])
    assert list(pkt["case_no"]) == list(range(1, 21))


def test_no_development_or_xiv_overlap():
    aud = pd.read_csv(
        DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_AUDIT.csv"
    )
    dev = pd.read_csv(
        DATA_PRIVATE / "development" / "out_of_pool" / "DEVELOPMENT_SET_AUDIT.csv"
    )
    cal_keys = set(zip(aud.q1_utterance_id.astype(str), aud.r1_utterance_id.astype(str)))
    dev_keys = set(zip(dev.q1_utterance_id.astype(str), dev.r1_utterance_id.astype(str)))
    assert cal_keys.isdisjoint(dev_keys)
    for d in aud["date"].astype(str):
        dd = date.fromisoformat(d[:10])
        assert not (XIV_START <= dd <= XIV_END)


def test_human_packets_exist_same_order():
    ddir = PROJECT_ROOT / "_internal" / "calibration_round1"
    daniel = ddir / "calibracion_ronda1_Daniel.docx"
    jose = ddir / "calibracion_ronda1_Jose_Jaime.docx"
    assert daniel.is_file() and jose.is_file()
    prov = json.loads((ddir / "CALIBRATION_ROUND1_PACKET_PROVENANCE.json").read_text())
    assert prov["same_cases_same_order"] is True
    assert "codebook_sha256" in prov
    assert len(prov["packets"]["daniel"]["sha256"]) == 64
    assert len(prov["packets"]["jose_jaime"]["sha256"]) == 64


def test_calibration_metrics_prepared_but_not_run_on_empty():
    # smoke: function exists and works on toy labels; production must wait for returns
    a = ["explicit_reply"] * 10 + ["non_reply"] * 10
    b = ["explicit_reply"] * 8 + ["intermediate_reply"] * 2 + ["non_reply"] * 10
    out = summarize_round1(a, b)
    assert out["n"] == 20
    assert 0.0 <= out["raw_agreement"] <= 1.0
    assert "cohen_kappa_3way" in out
    assert "krippendorff_alpha_nominal" in out


def test_no_xiv_reply_outcomes():
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not pool.is_file():
        return
    df = pd.read_parquet(pool)
    assert "reply_status" not in df.columns
