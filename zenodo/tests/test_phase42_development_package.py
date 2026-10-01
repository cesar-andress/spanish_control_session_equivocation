"""Phase 4.2 human development package checks."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yaml

from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

DEV_PKG = PROJECT_ROOT / "_internal" / "development"
OOP = DATA_PRIVATE / "development" / "out_of_pool"
FORBIDDEN = (
    "party",
    "parliamentary_group",
    "alignment",
    "formation_vote",
    "primary_alignment",
    "questioner",
    "legislature",
    "vote",
)


def test_development_packets_exist_and_blinded():
    prov = json.loads((DEV_PKG / "DEVELOPMENT_PACKAGE_PROVENANCE.json").read_text(encoding="utf-8"))
    assert prov["codebook_version"] == "v0.2"
    assert prov["n_units"] == 15
    assert prov["xiv_overlap"] is False
    assert "gold" not in prov["label"]
    for name, digest in prov["packet_hashes"].items():
        path = DEV_PKG / name
        assert path.is_file()
        assert len(digest) == 64

    for ann in ("A", "B"):
        xlsx = DEV_PKG / f"development_annotator_{ann}.xlsx"
        coding = pd.read_excel(xlsx, sheet_name="CODING")
        assert list(coding.columns) == [
            "unit_id",
            "registered_question",
            "Q1",
            "R1",
            "reply_status",
            "borderline",
            "confidence",
            "notes",
        ]
        assert len(coding) == 15
        assert all(str(u).startswith("dev_") for u in coding["unit_id"])
        for col in coding.columns:
            assert not any(f in col.lower() for f in FORBIDDEN)
        # labels empty
        assert coding["reply_status"].fillna("").astype(str).str.strip().eq("").all()
        feedback = pd.read_excel(xlsx, sheet_name="FEEDBACK")
        assert len(feedback) >= 4


def test_development_no_xiv_pool_ids():
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not pool.is_file():
        return
    xiv = set(pd.read_parquet(pool, columns=["exchange_id"])["exchange_id"].astype(str))
    coding = pd.read_excel(DEV_PKG / "development_annotator_A.xlsx", sheet_name="CODING")
    assert set(coding["unit_id"]).isdisjoint(xiv)


def test_development_schema_doc_exists():
    text = (PROTOCOL_DIR / "development_packet_schema.md").read_text(encoding="utf-8")
    assert "NOT" in text or "Not" in text
    assert "reply_status" in text
    assert "FEEDBACK" in text


def test_manifest_points_to_human_package():
    data = yaml.safe_load((PROTOCOL_DIR / "development_set_manifest.yaml").read_text(encoding="utf-8"))
    assert "human_development_package" in data
    assert data["human_development_package"]["codebook_version"] == "v0.2"
