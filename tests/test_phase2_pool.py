"""Phase-2 parser, linkage, pool, and hygiene tests."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from scse.extract_exchanges import extract_pm_exchanges_from_session, parse_session_utterances
from scse.ingest_congreso import parse_initiative_html
from scse.link_questions import make_exchange_id, names_match
from scse.validation import PoolValidationError, validate_pool_dataframe

FIXTURES = Path(__file__).parent / "fixtures"


def test_parlamint_fixture_extracts_pm_exchanges():
    path = FIXTURES / "parlamint" / "ParlaMint-ES_2020-05-13-CD200513.fragment.xml"
    rows = extract_pm_exchanges_from_session(path)
    assert len(rows) >= 1
    assert all(r.answerer_who == "#PedroSánchezPérezCastejón" for r in rows)
    assert all(r.q1_text and r.r1_text for r in rows)
    # Esteban exchange should carry expediente from TEI note
    esteban = [r for r in rows if r.questioner_who and "Esteban" in r.questioner_who]
    assert esteban
    assert esteban[0].expediente == "180/000127"


def test_parlamint_utterance_order_stable():
    path = FIXTURES / "parlamint" / "ParlaMint-ES_2020-05-13-CD200513.fragment.xml"
    _, _, utts = parse_session_utterances(path)
    assert [u.order for u in utts] == list(range(len(utts)))
    ids = [u.uid for u in utts]
    assert len(ids) == len(set(ids))


def test_congreso_fixture_parser():
    html = (FIXTURES / "congreso" / "XIV_180_000128.html").read_text(encoding="utf-8")
    rec = parse_initiative_html(
        html,
        expediente="180/000128",
        legislature="XIV",
        source_url="https://example.test/180/000128",
    )
    assert rec.title and "perspectivas económicas" in rec.title.lower()
    assert rec.questioner_name and "Casado" in rec.questioner_name
    assert rec.parliamentary_group == "GP"
    assert "DSCD-14-PL-22" in rec.ds_references


def test_names_match_casado():
    assert names_match("#PabloCasadoBlanco", "Casado Blanco, Pablo")
    assert not names_match("#AitorEstebanBravo", "Casado Blanco, Pablo")


def test_exchange_id_deterministic():
    from scse.extract_exchanges import RawExchange

    raw = RawExchange(
        session_id="ParlaMint-ES_2020-05-13-CD200513",
        document_path="x",
        date="2020-05-13",
        legislature="XIV",
        expediente="180/000127",
        registered_question_from_chair="¿Q?",
        questioner_who="#AitorEstebanBravo",
        answerer_who="#PedroSánchezPérezCastejón",
        q1_utterance_id="u13",
        r1_utterance_id="u15",
        q1_text="q",
        r1_text="r",
    )
    assert make_exchange_id(raw) == make_exchange_id(raw)


def test_schema_rejects_outcome_columns():
    df = pd.DataFrame(
        [
            {
                "exchange_id": "ex_1",
                "expediente": "180/000127",
                "legislature": "XIV",
                "date": "2020-05-13",
                "session_id": "s",
                "questioner_id": "#A",
                "answerer_id": "#PedroSánchezPérezCastejón",
                "registered_question": "¿Q?",
                "q1_text": "q",
                "r1_text": "r",
                "q1_utterance_id": "u1",
                "r1_utterance_id": "u2",
                "link_status": "exact",
                "eligible": True,
                "exclude_from_sampling": False,
                "sampling_exclusion_reason": None,
                "reply_status": "explicit",
            }
        ]
    )
    with pytest.raises(PoolValidationError, match="forbidden"):
        validate_pool_dataframe(df)


def test_public_safe_projection_omits_text():
    from scse.build_pool import PUBLIC_SAFE_COLUMNS

    assert "q1_text" not in PUBLIC_SAFE_COLUMNS
    assert "r1_text" not in PUBLIC_SAFE_COLUMNS
    assert "registered_question" not in PUBLIC_SAFE_COLUMNS
    assert "expediente" in PUBLIC_SAFE_COLUMNS


def test_seeds_main_remain_null_calibration_round1_set():
    from scse.paths import PROTOCOL_DIR
    import yaml

    data = yaml.safe_load((PROTOCOL_DIR / "seeds.yaml").read_text(encoding="utf-8"))
    seeds = data.get("seeds", data)
    assert seeds.get("development") is None
    assert seeds.get("calibration") == 2071684612
    assert seeds.get("main_sample") is None
    assert seeds.get("bootstrap") is None


def test_pool_determinism_if_present():
    from scse.paths import DATA_PRIVATE, DERIVED_DIR
    import hashlib

    private = DATA_PRIVATE / "eligible_pool_full.parquet"
    public = DERIVED_DIR / "eligible_pool_metadata_preannotation.csv"
    if not private.is_file() or not public.is_file():
        pytest.skip("pool artifacts not built in this environment")
    df = pd.read_parquet(private)
    assert "reply_status" not in df.columns
    assert "formation_vote_alignment" not in df.columns
    assert df["exchange_id"].is_unique
    # Public projection must not include spoken/registered text
    pub = pd.read_csv(public)
    for col in ("q1_text", "r1_text", "registered_question"):
        assert col not in pub.columns
