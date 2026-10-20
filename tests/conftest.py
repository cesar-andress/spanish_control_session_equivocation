"""Skip private-monorepo tests when running the standalone public package."""

from __future__ import annotations

import pytest

from scse.paths import INTERNAL_DIR, PAPER_DIR, STANDALONE_PUBLIC


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if not STANDALONE_PUBLIC:
        return
    skip_private = pytest.mark.skip(
        reason="requires private monorepo materials (_internal/) not shipped in the public package"
    )
    skip_paper = pytest.mark.skip(
        reason="requires manuscript tree (paper/) not shipped in the public package"
    )
    for item in items:
        node = item.nodeid
        if "test_phase8c_manuscript_pivot" in node or "paper/" in node:
            item.add_marker(skip_paper)
            continue
        # Private-dependent phase / returns / packet tests
        private_markers = (
            "phase4",
            "phase5",
            "phase6",
            "phase7",
            "phase8",
            "calibration_round",
            "binary_validation",
            "development_package",
            "alignment_feasibility",
            "question_side",
            "ai_simulation",
            "construct_rescue",
            "measurement_evidence",
        )
        if any(m in node for m in private_markers):
            item.add_marker(skip_private)


def pytest_report_header(config: pytest.Config) -> str:
    return (
        f"standalone_public={STANDALONE_PUBLIC} "
        f"internal_present={INTERNAL_DIR.is_dir()} "
        f"paper_present={PAPER_DIR.is_dir()}"
    )
