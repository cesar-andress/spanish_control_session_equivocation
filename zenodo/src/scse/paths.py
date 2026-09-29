"""Project path helpers.

All paths are resolved relative to the zenodo/ package root so public code
never embeds absolute personal home directories.
"""

from __future__ import annotations

from pathlib import Path

# zenodo/ — public reproducibility root
ZENODO_ROOT = Path(__file__).resolve().parents[2]

# Project root (parent of zenodo/); may contain paper/ and _internal/
PROJECT_ROOT = ZENODO_ROOT.parent

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

# Private area lives beside zenodo/, never inside it
INTERNAL_DIR = PROJECT_ROOT / "_internal"

PAPER_DIR = PROJECT_ROOT / "paper"


def ensure_zenodo_layout() -> dict[str, Path]:
    """Return the canonical public paths (does not create missing parents)."""
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
