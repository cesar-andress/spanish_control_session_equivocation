"""Phase 6A pre-outcome infrastructure tests."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

from scse.analysis_scaffold import (
    category_distribution,
    confrontational_sensitivity,
    explicit_vs_nonexplicit,
    leave_one_questioner_out,
    make_synthetic_fixture,
    opposed_vs_nonopposed_contrast,
    per_questioner_explicit_rates,
    questioner_cluster_bootstrap,
    refuse_real_xiv_paths,
    topic_stratified_explicit,
)
from scse.main_frame import MAIN_PRIVATE, VOLUMES_DEFAULT, assert_no_outcome_columns, load_qa30_exchange_ids
from scse.paths import DATA_PRIVATE, DERIVED_DIR, FIGURES_DIR, PROTOCOL_DIR, TABLES_DIR


def test_qa30_ids_frozen():
    ids = load_qa30_exchange_ids()
    assert len(ids) == 30
    assert len(set(ids)) == 30


def test_main_frame_membership_and_no_outcomes():
    corpus_path = MAIN_PRIVATE / "MAIN_FRAME_CORPUS_FULL.parquet"
    if not corpus_path.is_file():
        pytest.skip("main corpus not built")
    df = pd.read_parquet(corpus_path)
    assert len(df) == 97
    assert df["exchange_id"].is_unique
    assert_no_outcome_columns(df)
    assert "reply_status" not in df.columns
    assert df["case_no"].tolist() == list(range(1, 98))
    # completeness
    for col in ("registered_question", "q1_text", "r1_text"):
        assert df[col].astype(str).str.strip().ne("").all()


def test_phase0_still_excluded_from_main():
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if not pool.is_file():
        pytest.skip("pool missing")
    df = pd.read_parquet(pool)
    probes = df[df["sampling_exclusion_reason"].eq("phase0_feasibility_probe")]
    assert len(probes) == 3
    assert probes["exclude_from_sampling"].all()
    # no active linkage_QA exclusions
    assert not (
        df["sampling_exclusion_reason"].eq("linkage_QA") & df["exclude_from_sampling"].fillna(False)
    ).any()
    main_n = int((df["eligible"] & ~df["exclude_from_sampling"].fillna(False)).sum())
    assert main_n == 97


def test_main_frame_manifest():
    path = PROTOCOL_DIR / "main_frame_manifest.yaml"
    if not path.is_file():
        pytest.skip("manifest missing")
    m = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert m["n"] == 97
    assert m["linkage_qa_restored_n"] == 30
    assert m["phase0_probes_excluded_n"] == 3
    assert m["reply_status_present"] is False
    assert m["human_packets_issued"] is False


def test_public_main_metadata_omits_full_text():
    path = DERIVED_DIR / "main_frame_metadata_preannotation.csv"
    if not path.is_file():
        pytest.skip("public main metadata missing")
    pub = pd.read_csv(path)
    for col in ("registered_question", "q1_text", "r1_text"):
        assert col not in pub.columns
    assert len(pub) == 97


def test_volume_plan_covers_all_once():
    path = MAIN_PRIVATE / "MAIN_FRAME_VOLUME_PLAN.json"
    if not path.is_file():
        pytest.skip("volume plan missing")
    plan = json.loads(path.read_text(encoding="utf-8"))
    cases = [c for v in plan["volumes"] for c in v["case_nos"]]
    assert cases == list(range(1, 98))
    assert [v["n"] for v in plan["volumes"]] == list(VOLUMES_DEFAULT)


def test_packet_templates_equal_order_not_issued():
    status = Path(__file__).resolve().parents[2].parent / "_internal" / "main_annotation" / "MAIN_PACKET_GENERATOR_STATUS.json"
    # paths from project root
    from scse.paths import PROJECT_ROOT

    status = PROJECT_ROOT / "_internal" / "main_annotation" / "MAIN_PACKET_GENERATOR_STATUS.json"
    if not status.is_file():
        pytest.skip("packet generator status missing")
    meta = json.loads(status.read_text(encoding="utf-8"))
    assert meta["issued"] is False
    assert meta["identical_case_order"] is True
    assert meta["n_cases"] == 97


def test_analysis_scaffold_synthetic_only():
    syn = make_synthetic_fixture(n=24, seed=2)
    dist = category_distribution(syn)
    assert dist.sum() == 24
    c = opposed_vs_nonopposed_contrast(syn)
    assert c.n_a + c.n_b == 24
    _ = explicit_vs_nonexplicit(syn)
    _ = questioner_cluster_bootstrap(syn, n_boot=20, seed=3)
    _ = per_questioner_explicit_rates(syn)
    _ = leave_one_questioner_out(syn)
    _ = topic_stratified_explicit(syn)
    _ = confrontational_sensitivity(syn)
    with pytest.raises(RuntimeError):
        refuse_real_xiv_paths("_internal/data_private/main/MAIN_FRAME_CORPUS_FULL.parquet")


def test_outcome_table_shells_are_placeholders():
    t2 = TABLES_DIR / "table2_reply_status_distribution_SHELL.csv"
    t3 = TABLES_DIR / "table3_explicit_contrast_SHELL.csv"
    if not t2.is_file() or not t3.is_file():
        pytest.skip("shells missing")
    d2 = pd.read_csv(t2)
    d3 = pd.read_csv(t3)
    assert d2["note"].str.contains("PLACEHOLDER").all()
    assert d3["note"].str.contains("PLACEHOLDER").all()


def test_study_flow_exists():
    path = FIGURES_DIR / "fig1_study_flow_preoutcome.svg"
    if not path.is_file():
        pytest.skip("study flow missing")
    text = path.read_text(encoding="utf-8")
    assert "N = 97" in text
    assert "No reply-status outcomes" in text
