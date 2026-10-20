"""Question-side topic audit and calibration diversity gates."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR
from scse.question_side import code_question_side


def test_question_side_never_needs_r1():
    side = code_question_side(
        "¿Qué medidas piensa adoptar el Gobierno para el empleo?",
        "Señor presidente, ¿qué medidas va a tomar para el empleo?",
    )
    assert side["question_topic"] == "economy_employment"
    assert side["question_form"] in {"yes_no", "wh", "evaluative"}
    assert side["question_confrontational"] in {"yes", "no"}


def test_confrontational_not_from_mere_disagreement_lexicon():
    # Polar policy disagreement without accusation cues
    side = code_question_side(
        "¿Va a subir el salario mínimo?",
        "Señor presidente, ¿va a subir el salario mínimo?",
    )
    assert side["question_confrontational"] == "no"


def test_xiv_audit_artifacts_exist_without_r1_outcomes():
    report = PROJECT_ROOT / "_internal" / "reports" / "QUESTION_SIDE_TOPIC_AND_DIVERSITY_AUDIT.md"
    text = report.read_text(encoding="utf-8")
    assert "MEDIUM" in text
    assert "R1 inspected for outcome purposes: **NO**" in text
    assert "Main pool altered: **NO**" in text or "unchanged" in text.lower()
    csv = DATA_PRIVATE / "question_side" / "xiv_eligible_question_side_audit.csv"
    df = pd.read_csv(csv)
    assert len(df) == 100
    assert "r1_text" not in df.columns
    assert "reply_status" not in df.columns
    assert set(df["question_topic"]) <= {
        "economy_employment",
        "social_public_services",
        "territorial_institutional",
        "foreign_security",
        "governance_institutional_integrity",
        "other",
    }


def test_calibration_diversity_rule_applied():
    path = DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_DIVERSITY.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["n"] == 20
    assert len(data["topics"]) >= 2
    assert len(data["forms"]) >= 2
    assert data["reply_labels_observed"] is False
    man = (PROTOCOL_DIR / "calibration_round1_manifest.yaml").read_text(encoding="utf-8")
    assert "diversity_rule" in man
