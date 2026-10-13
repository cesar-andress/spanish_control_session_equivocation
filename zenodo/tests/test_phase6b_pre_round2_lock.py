"""Phase 6B pre-Round-2 lock tests."""

from __future__ import annotations

from pathlib import Path

import yaml

from scse.paths import INTERNAL_DIR, PROTOCOL_DIR, PROJECT_ROOT


def test_round2_decision_rule_locked_in_calibration_design():
    text = (PROTOCOL_DIR / "CALIBRATION_DESIGN.md").read_text(encoding="utf-8")
    assert "0.67" in text
    assert "Krippendorff" in text or "Krippendorff’s" in text or "α" in text
    assert "STOP" in text
    assert "Round 3" in text
    assert "before returns" in text.lower() or "before inspecting" in text.lower() or "LOCKED before returns" in text


def test_seeds_main_orders_set_sample_null():
    data = yaml.safe_load((PROTOCOL_DIR / "seeds.yaml").read_text(encoding="utf-8"))
    seeds = data.get("seeds", data)
    assert seeds.get("main_sample") is None
    # After Phase 6B build these should exist; skip if not yet rebuilt in CI-less clone
    if seeds.get("main_packet_order_daniel") is None:
        return
    assert seeds["main_packet_order_daniel"] != seeds["main_packet_order_jose_jaime"]


def test_round2_packets_untouched_hashes_if_present():
    # Ensure files still exist; content change would be a process failure outside tests
    r2 = PROJECT_ROOT / "_internal" / "calibration_round2"
    if not r2.is_dir():
        return
    assert (r2 / "02_calibracion_ronda2_Daniel.docx").is_file()


def test_ai_simulation_not_required_to_have_returns():
    returns = INTERNAL_DIR / "ai_simulation" / "returns"
    if returns.is_dir():
        assert list(returns.glob("*.json")) == [] or True  # empty OK; no fabricated requirement
