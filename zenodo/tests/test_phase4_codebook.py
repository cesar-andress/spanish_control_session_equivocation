"""Phase-4 / 4.1 reply_status codebook and out-of-pool development gates."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yaml

from scse.paths import DATA_PRIVATE, PROTOCOL_DIR, ZENODO_ROOT

DEV_DIR = DATA_PRIVATE / "development"
OOP_DIR = DEV_DIR / "out_of_pool"
FORBIDDEN_PACKET_SUBSTRINGS = (
    "party",
    "alignment",
    "group",
    "questioner",
    "formation",
    "parliamentary",
    "vote",
)


def test_codebook_v02_exists_and_not_frozen():
    path = PROTOCOL_DIR / "reply_status_codebook_v0.2.md"
    text = path.read_text(encoding="utf-8")
    assert "DRAFT — NOT FROZEN" in text
    assert "Q1" in text
    assert "question_form" in text
    assert "question_confrontational" in text
    assert "question_target_type" in text
    assert "explicit_reply" in text


def test_development_manifest_yaml_out_of_pool():
    path = PROTOCOL_DIR / "development_set_manifest.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["exclusion_from_main_sampling"] is True
    assert data["n_units"] == 15
    assert data["legislature"]["preferred"] == "XIII"
    assert data.get("not_for_reliability_evaluation") is True
    assert len(data["unit_ids"]) == 15
    assert all(str(u).startswith("dev_") for u in data["unit_ids"])


def test_old_inpool_development_superseded():
    path = DEV_DIR / "DEVELOPMENT_SET_MANIFEST.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["status"] == "superseded"
    assert "must not overlap" in data["superseded_reason"].lower()


def test_oop_packet_blinded():
    packet = pd.read_csv(OOP_DIR / "DEVELOPMENT_PACKET_BLINDED.csv")
    assert list(packet.columns)[:4] == [
        "unit_id",
        "registered_question",
        "Q1",
        "R1",
    ]
    for col in packet.columns:
        assert not any(s in col.lower() for s in FORBIDDEN_PACKET_SUBSTRINGS)
    assert packet["unit_id"].is_unique
    assert len(packet) == 15


def test_xiv_pool_not_holding_development_exclusions():
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not pool.is_file():
        return
    df = pd.read_parquet(pool)
    assert "reply_status" not in df.columns
    assert not (df["sampling_exclusion_reason"] == "development_codebook").any()
    # phase0 + linkage QA still excluded
    assert (df["sampling_exclusion_reason"] == "linkage_QA").sum() == 30


def test_calibration_design_undrawn():
    text = (PROTOCOL_DIR / "CALIBRATION_DESIGN.md").read_text(encoding="utf-8")
    assert "not drawn" in text.lower() or "Units **not** drawn" in text
    assert "20" in text
    seeds = yaml.safe_load((PROTOCOL_DIR / "seeds.yaml").read_text(encoding="utf-8"))
    s = seeds.get("seeds", seeds)
    assert s.get("calibration") is None
    assert s.get("main_sample") is None


def test_annotation_schemas_include_question_fields():
    data = json.loads(
        (ZENODO_ROOT / "schemas" / "annotation_row.schema.json").read_text(encoding="utf-8")
    )
    props = data["properties"]
    assert "question_form" in props
    assert "question_confrontational" in props
    assert "question_target_type" in props
    assert "reply_status" in props


def test_packet_template_header():
    header = (
        PROTOCOL_DIR / "packet_templates" / "annotator_packet_header.csv"
    ).read_text(encoding="utf-8").strip()
    cols = header.split(",")
    assert cols[:4] == ["unit_id", "registered_question", "Q1", "R1"]
    assert "question_form" in cols
    assert "parliamentary_group" not in cols
