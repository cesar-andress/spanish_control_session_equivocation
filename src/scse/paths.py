"""Project paths.

Supports two layouts:

1. Monorepo: ``<project>/zenodo/`` beside ``paper/`` and ``_internal/``.
2. Standalone public package: this directory is the repository root.
"""

from __future__ import annotations

from pathlib import Path

ZENODO_ROOT = Path(__file__).resolve().parents[2]


def _detect_project_root(zenodo_root: Path) -> Path:
    parent = zenodo_root.parent
    # Monorepo layout: parent contains this zenodo/ directory and usually paper/
    if (parent / "zenodo").resolve() == zenodo_root.resolve() and (
        (parent / "paper").is_dir() or (parent / "AGENTS.md").is_file()
    ):
        return parent
    return zenodo_root


PROJECT_ROOT = _detect_project_root(ZENODO_ROOT)
STANDALONE_PUBLIC = PROJECT_ROOT == ZENODO_ROOT

PROTOCOL_DIR = ZENODO_ROOT / "protocol"
DATA_DIR = ZENODO_ROOT / "data"
RAW_PINNED_DIR = DATA_DIR / "raw_pinned"
DERIVED_DIR = DATA_DIR / "derived"
LABELS_DIR = DATA_DIR / "labels"
OUTPUTS_DIR = ZENODO_ROOT / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
FIGURES_DIR = OUTPUTS_DIR / "figures"
MANIFESTS_DIR = ZENODO_ROOT / "manifests"
DOCS_DIR = ZENODO_ROOT / "docs"
TESTS_DIR = ZENODO_ROOT / "tests"

INTERNAL_DIR = PROJECT_ROOT / "_internal"
SOURCE_CACHE = INTERNAL_DIR / "source_cache"
PARLAMINT_CACHE = SOURCE_CACHE / "parlamint"
CONGRESO_CACHE = SOURCE_CACHE / "congreso"
DATA_PRIVATE = INTERNAL_DIR / "data_private"
LINK_AUDIT_PRIVATE = INTERNAL_DIR / "link_audit_private"
PAPER_DIR = PROJECT_ROOT / "paper"


def ensure_zenodo_layout() -> dict[str, Path]:
    return {
        "zenodo_root": ZENODO_ROOT,
        "protocol": PROTOCOL_DIR,
        "data": DATA_DIR,
        "raw_pinned": RAW_PINNED_DIR,
        "derived": DERIVED_DIR,
        "labels": LABELS_DIR,
        "outputs": OUTPUTS_DIR,
        "tables": TABLES_DIR,
        "figures": FIGURES_DIR,
        "manifests": MANIFESTS_DIR,
        "docs": DOCS_DIR,
    }


def ensure_private_layout() -> None:
    """Create private sibling dirs only in monorepo layout."""
    if STANDALONE_PUBLIC:
        return
    for path in (
        SOURCE_CACHE,
        PARLAMINT_CACHE,
        CONGRESO_CACHE / "iniciativas",
        DATA_PRIVATE,
        LINK_AUDIT_PRIVATE,
    ):
        path.mkdir(parents=True, exist_ok=True)
