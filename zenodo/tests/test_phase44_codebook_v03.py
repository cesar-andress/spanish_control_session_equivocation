"""Phase 4.4 codebook v0.3 and packet-presentation gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

from scse.packet_validation import (
    PacketValidationError,
    validate_packet_frame,
    validate_packet_row,
)
from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR, ZENODO_ROOT

# Locked hashes from Phase 4.3 / pre-v0.3 state
V02_SHA256 = "2b0c0398a7939d5ed45ff95ee66afb32d2ed48524d6db8819b7ad024e8eba823"
DANIEL_SHA256 = "2ff07e8d57d16798af4bc399d0c92c6cb3b0603d921f65253460d62bbc2bb1e1"
JOSE_SHA256 = "97bb754fdfb317bf48d2a8f090978613543e02748094baa5bc2bde46ea0b6930"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_codebook_v02_preserved_unchanged():
    path = PROTOCOL_DIR / "reply_status_codebook_v0.2.md"
    assert path.is_file()
    assert _sha256(path) == V02_SHA256
    text = path.read_text(encoding="utf-8")
    assert "DRAFT — NOT FROZEN" in text


def test_codebook_v03_exists_draft_not_frozen():
    path = PROTOCOL_DIR / "reply_status_codebook_v0.3.md"
    text = path.read_text(encoding="utf-8")
    assert "VERSIÓN DE CALIBRACIÓN" in text or "CALIBRACIÓN" in text
    assert "0.3.0" in text
    assert "Pregunta registrada" in text
    assert "hablar del mismo tema" in text.lower() or "mismo tema" in text
    assert "ley" in text and "medida" in text and "fórmula" in text
    assert "Caso 7" in text or "caso 7" in text.lower() or "Caso frontera" in text
    assert "respuesta explícita" in text
    assert "respuesta parcial o intermedia" in text
    assert "ausencia de respuesta" in text
    # must not claim Case 7 consensus
    assert "no fuerza una categoría" in text.lower() or "No fuerza" in text


def test_v02_to_v03_changelog_exists():
    path = PROTOCOL_DIR / "reply_status_codebook_v0.2_to_v0.3_changes.md"
    text = path.read_text(encoding="utf-8")
    assert "topical" in text.lower() or "tema" in text.lower()
    assert "12" in text and "13" in text
    assert "Case 7" in text or "caso 7" in text.lower()


def test_development_original_judgements_preserved():
    root = PROJECT_ROOT / "_internal" / "development" / "solutions"
    assert _sha256(root / "daniel_pinto_solutions.json") == DANIEL_SHA256
    assert _sha256(root / "jose_jaime_baena_solutions.json") == JOSE_SHA256


def test_packet_validation_requires_three_texts():
    ok = {
        "unit_id": "dev_x",
        "registered_question": "¿Pregunta registrada?",
        "Q1": "Pregunta oral.",
        "R1": "Respuesta.",
    }
    validate_packet_row(ok)

    with pytest.raises(PacketValidationError):
        validate_packet_row(
            {
                "unit_id": "dev_bad",
                "registered_question": "   ",
                "Q1": "Oral",
                "R1": "Resp",
            }
        )

    with pytest.raises(PacketValidationError):
        validate_packet_row(
            {
                "unit_id": "dev_bad2",
                "registered_question": "Reg",
                "Q1": "",
                "R1": "Resp",
            }
        )


def test_packet_validation_registered_unavailable_flag():
    row = {
        "unit_id": "dev_flag",
        "registered_question": "",
        "Q1": "Oral",
        "R1": "Resp",
        "registered_unavailable": True,
    }
    with pytest.raises(PacketValidationError):
        validate_packet_row(row, allow_registered_unavailable=False)
    validate_packet_row(row, allow_registered_unavailable=True)


def test_packet_frame_rejects_forbidden_metadata():
    df = pd.DataFrame(
        [
            {
                "unit_id": "a",
                "registered_question": "r",
                "Q1": "q",
                "R1": "r1",
                "party": "X",
            }
        ]
    )
    with pytest.raises(PacketValidationError):
        validate_packet_frame(df)


def test_annotator_packet_schema_requires_three_fields():
    data = json.loads(
        (ZENODO_ROOT / "schemas" / "annotator_packet_row.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert set(data["required"]) >= {"unit_id", "registered_question", "Q1", "R1"}
    for field in ("registered_question", "Q1", "R1"):
        assert data["properties"][field]["minLength"] >= 1


def test_blinded_oop_packet_passes_v03_validation():
    packet = pd.read_csv(
        DATA_PRIVATE / "development" / "out_of_pool" / "DEVELOPMENT_PACKET_BLINDED.csv"
    )
    validate_packet_frame(packet)


def test_calibration_round1_drawn_after_v03():
    text = (PROTOCOL_DIR / "CALIBRATION_DESIGN.md").read_text(encoding="utf-8")
    assert "Round 1" in text or "DRAWN" in text
    seeds = yaml.safe_load((PROTOCOL_DIR / "seeds.yaml").read_text(encoding="utf-8"))
    s = seeds.get("seeds", seeds)
    assert s.get("calibration") == 2071684612
    assert s.get("main_sample") is None


def test_no_xiv_reply_outcomes_in_pool():
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not pool.is_file():
        return
    df = pd.read_parquet(pool)
    assert "reply_status" not in df.columns
