"""Phase-4 reply_status codebook development gates (no outcome coding)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yaml

from scse.paths import DATA_PRIVATE, PROTOCOL_DIR, ZENODO_ROOT

DEV_DIR = DATA_PRIVATE / "development"
FORBIDDEN_PACKET_SUBSTRINGS = (
    "party",
    "alignment",
    "group",
    "questioner",
    "formation",
    "parliamentary",
    "vote",
)


def test_draft_codebook_exists_and_not_frozen():
    path = PROTOCOL_DIR / "reply_status_codebook_v0.1.md"
    text = path.read_text(encoding="utf-8")
    assert "DRAFT — NOT FROZEN" in text
    assert "explicit_reply" in text
    assert "intermediate_reply" in text
    assert "non_reply" in text
    assert "responsiveness" in text.lower()


def test_literature_framework_exists():
    path = ZENODO_ROOT.parent / "_internal" / "literature" / "REPLY_STATUS_FRAMEWORK.md"
    text = path.read_text(encoding="utf-8")
    assert "Bull" in text
    assert "Adaptation" in text or "adaptation" in text.lower()


def test_calibration_design_exists():
    path = PROTOCOL_DIR / "CALIBRATION_DESIGN.md"
    text = path.read_text(encoding="utf-8")
    assert "Round 1" in text
    assert "Round 2" in text
    assert "20" in text
    assert "null" in text.lower()


def test_annotation_schemas_exist():
    for name in ("annotation_row.schema.json", "annotator_packet_row.schema.json"):
        path = ZENODO_ROOT / "schemas" / name
        assert path.is_file()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "properties" in data


def test_development_set_blinded_and_excluded():
    manifest = json.loads((DEV_DIR / "DEVELOPMENT_SET_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["n"] == 15
    assert manifest["scientific_seed_used"] is None
    assert manifest["not_for_reliability"] is True
    ids = set(manifest["unit_ids"])
    assert len(ids) == 15

    packet = pd.read_csv(DEV_DIR / "DEVELOPMENT_PACKET_BLINDED.csv")
    assert list(packet.columns) == ["unit_id", "registered_question", "Q1", "R1"]
    assert set(packet["unit_id"]) == ids
    for col in packet.columns:
        assert not any(s in col.lower() for s in FORBIDDEN_PACKET_SUBSTRINGS)

    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not pool.is_file():
        return
    df = pd.read_parquet(pool)
    assert "reply_status" not in df.columns
    sub = df[df["exchange_id"].isin(ids)]
    assert len(sub) == 15
    assert sub["exclude_from_sampling"].all()
    assert (sub["sampling_exclusion_reason"] == "development_codebook").all()


def test_seeds_still_null_after_phase4():
    data = yaml.safe_load((PROTOCOL_DIR / "seeds.yaml").read_text(encoding="utf-8"))
    seeds = data.get("seeds", data)
    assert seeds.get("development") is None
    assert seeds.get("calibration") is None
    assert seeds.get("main_sample") is None


def test_packet_template_header_blinded():
    header = (PROTOCOL_DIR / "packet_templates" / "annotator_packet_header.csv").read_text(
        encoding="utf-8"
    ).strip()
    cols = header.split(",")
    assert cols[:4] == ["unit_id", "registered_question", "Q1", "R1"]
    assert "parliamentary_group" not in cols
    assert "formation_vote_alignment" not in cols
