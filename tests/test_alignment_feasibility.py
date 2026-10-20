"""Phase-3 alignment feasibility checks (no outcomes)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scse.paths import DATA_PRIVATE, PROTOCOL_DIR, PROJECT_ROOT


FORBIDDEN = {
    "reply_status",
    "equivocation_type",
    "outcome",
    "ally",
    "adversary",
    "friendly",
    "hostile",
}


def test_alignment_table_draft_exists_and_is_not_frozen():
    path = PROTOCOL_DIR / "alignment_table.yaml"
    assert path.is_file()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["status"] == "draft_not_frozen"
    assert data["vote_event"]["date"] == "2020-01-07"
    cats = {e["alignment_category"] for e in data["entries"]}
    assert cats <= {"supported", "opposed", "abstained", "unknown"}
    text = path.read_text(encoding="utf-8").lower()
    # Allow a single prohibition note; forbid use as category values
    for e in data["entries"]:
        assert e["alignment_category"] not in {
            "ally",
            "adversary",
            "friendly",
            "hostile",
            "allies",
            "adversaries",
        }


def test_alignment_feasibility_csv_if_present():
    path = DATA_PRIVATE / "alignment_feasibility.csv"
    if not path.is_file():
        pytest.skip("alignment_feasibility.csv not built")
    import pandas as pd

    df = pd.read_csv(path)
    assert "formation_vote_alignment" in df.columns
    assert "reply_status" not in df.columns
    assert set(df["formation_vote_alignment"]) <= {
        "supported",
        "opposed",
        "abstained",
        "unknown",
    }
    assert df["formation_vote_alignment"].ne("unknown").all()
    for col in FORBIDDEN:
        assert col not in df.columns


def test_alignment_report_exists():
    report = PROJECT_ROOT / "_internal/reports/ALIGNMENT_FEASIBILITY_REPORT.md"
    assert report.is_file()
    text = report.read_text(encoding="utf-8")
    assert "formation_vote_alignment" in text
    assert "GO" in text
    assert "No reply coding" in text or "no reply" in text.lower()
