"""Phase 8C: measurement-paper manuscript pivot gates."""

from __future__ import annotations

from scse.paths import PROJECT_ROOT

PAPER = PROJECT_ROOT / "paper"
MAIN = PAPER / "main.tex"


def test_provisional_title_and_structure():
    t = MAIN.read_text(encoding="utf-8")
    assert "When Does a Reply Count as an Answer?" in t
    assert "Threshold Instability" in t
    for rel in [
        "sections/01_introduction.tex",
        "sections/03_study_origin_and_design.tex",
        "sections/05_analysis.tex",
        "sections/06_results.tex",
        "sections/08_limitations.tex",
        "tables/tab1_measurement_programme.tex",
        "tables/tab2_agreement_estimates.tex",
        "tables/tab3_disagreement_direction.tex",
        "figures/fig2_reliability_estimates.pdf",
    ]:
        assert (PAPER / rel).is_file(), rel


def test_locked_numbers_present():
    t = "\n".join(
        p.read_text(encoding="utf-8")
        for p in [
            MAIN,
            PAPER / "sections/01_introduction.tex",
            PAPER / "sections/06_results.tex",
        ]
    )
    assert "0.672" in t
    assert "0.159" in t
    assert "0.470" in t
    assert "0.226" in t
    assert r"\kappa_{\max}" in t
    assert "$N=100$" in t


def test_no_false_claims():
    blob = "\n".join(p.read_text(encoding="utf-8") for p in sorted(PAPER.rglob("*.tex")))
    low = blob.lower()
    assert "not preregistered" in low
    assert "was preregistered as" not in low
    assert "daniel is lenient" not in low
    assert "jose jaime is strict" not in low
    assert "stable coder-severity trait" not in low
    assert "xiv reply-status outcomes were created" not in low
    # Old substantive plan language must not remain as active plan
    assert "main annotation does not begin until" not in low


def test_qualitative_taxonomy_labelled_non_independent():
    # Taxonomy lives in the IJSRM supplement; keep the same non-independence label.
    candidates = [
        PAPER / "supplement" / "supplement.tex",
        PAPER / "tables" / "tab4_mechanism_taxonomy.tex",
    ]
    import re

    mech = " ".join(
        p.read_text(encoding="utf-8").lower()
        for p in candidates
        if p.is_file()
    )
    mech = re.sub(r"\s+", " ", mech)
    assert "not independent reliability evidence" in mech
