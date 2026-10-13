"""Blinded Round-1 AI simulation package tests."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from scse.ai_simulation_round1 import (
    AI_DIR,
    R1_PACKET,
    analyse_available_returns,
    assert_blinded_payload,
    build_package,
    load_ai_return,
    load_round1_blinded_cases,
    within_ai_stability,
)
from scse.paths import PROJECT_ROOT


def test_blinded_cases_exactly_20_fixed_order():
    cases = load_round1_blinded_cases()
    assert [c["case"] for c in cases] == list(range(1, 21))
    pkt = pd.read_csv(R1_PACKET).sort_values("case_no")
    for c, (_, row) in zip(cases, pkt.iterrows()):
        assert c["registered_question"] == str(row["registered_question"]).strip()
        assert c["oral_question"] == str(row["Q1"]).strip()
        assert c["first_response"] == str(row["R1"]).strip()


def test_blinded_payload_keys_only():
    cases = load_round1_blinded_cases()
    assert_blinded_payload(cases)


def test_build_package_no_human_leakage():
    meta = build_package()
    assert meta["human_labels_in_ai_packet"] == "False" or meta["human_labels_in_ai_packet"] is False
    path = PROJECT_ROOT / meta["blinded_json"]
    text = path.read_text(encoding="utf-8").lower()
    for bad in (
        "daniel",
        "jose jaime",
        "kappa",
        "gold label",
        "pinto pajares",
        "baena rojas",
        "unit_id",
        "cal1_",
    ):
        assert bad not in text
    data = json.loads(path.read_text(encoding="utf-8"))
    assert len(data) == 20
    assert all(set(c) == {"case", "registered_question", "oral_question", "first_response"} for c in data)
    prompt = (AI_DIR / "ROUND1_AI_PROMPT.txt").read_text(encoding="utf-8").lower()
    assert "daniel" not in prompt
    assert "jose jaime" not in prompt
    assert "kappa" not in prompt
    assert "respuesta explícita" in prompt
    assert "v0.3" in prompt


def test_analyse_without_returns_does_not_fabricate():
    out = analyse_available_returns(AI_DIR / "returns")
    assert out.get("fabricated") is False
    assert out["status"] == "waiting_for_ai_returns" or out["status"] == "analysed"
    # empty dir → waiting
    empty = AI_DIR / "returns"
    # if only README, still waiting
    jsons = list(empty.glob("*.json")) if empty.is_dir() else []
    if not jsons:
        assert out["status"] == "waiting_for_ai_returns"


def test_analysis_with_synthetic_ai_return(tmp_path: Path):
    # Synthetic AI output for scaffold only — not written to project returns/
    rows = [
        {
            "case": i,
            "category": "respuesta explícita",
            "borderline": "no",
            "justification": "synthetic",
        }
        for i in range(1, 21)
    ]
    p = tmp_path / "MODE_A_run1.json"
    p.write_text(json.dumps(rows), encoding="utf-8")
    loaded = load_ai_return(p)
    assert len(loaded) == 20
    # stability helper
    runs = {"a": loaded, "b": loaded}
    stab = within_ai_stability(runs)
    assert stab["n_unstable"] == 0


def test_no_main_xiv_in_ai_dir():
    if not (AI_DIR / "ROUND1_AI_BLINDED_CASES.json").is_file():
        build_package()
    blob = (AI_DIR / "ROUND1_AI_BLINDED_CASES.json").read_text(encoding="utf-8")
    assert "ex_" not in blob  # Round-1 OOP units use cal1_ / no XIV exchange ids in blinded payload
    # Round-1 blinded packet has unit_id in source CSV but must not appear in AI JSON
    data = json.loads(blob)
    assert all("unit_id" not in c for c in data)
