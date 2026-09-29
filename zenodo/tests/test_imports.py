"""Package import smoke tests."""

from __future__ import annotations


def test_import_scse():
    import scse

    assert scse.__version__ == "0.0.0"
    assert "Equivocation" in scse.WORKING_TITLE


def test_import_modules():
    import scse.ingest_parlamint  # noqa: F401
    import scse.ingest_congreso  # noqa: F401
    import scse.extract_exchanges  # noqa: F401
    import scse.link_questions  # noqa: F401
    import scse.alignment  # noqa: F401
    import scse.sampling  # noqa: F401
    import scse.packets  # noqa: F401
    import scse.validation  # noqa: F401
    import scse.agreement  # noqa: F401
    import scse.adjudication  # noqa: F401
    import scse.analysis  # noqa: F401
    import scse.figures  # noqa: F401
    import scse.release  # noqa: F401
    import scse.seeds  # noqa: F401
    import scse.paths  # noqa: F401
