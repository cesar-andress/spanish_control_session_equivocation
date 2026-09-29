"""Path and public/private separation tests."""

from __future__ import annotations

from pathlib import Path

from scse.paths import (
    INTERNAL_DIR,
    PROJECT_ROOT,
    ZENODO_ROOT,
    ensure_zenodo_layout,
)


def test_zenodo_root_is_package_root():
    assert ZENODO_ROOT.name == "zenodo"
    assert (ZENODO_ROOT / "pyproject.toml").is_file()
    assert (ZENODO_ROOT / "src" / "scse").is_dir()


def test_project_root_contains_paper_and_zenodo():
    assert (PROJECT_ROOT / "zenodo").resolve() == ZENODO_ROOT.resolve()
    assert (PROJECT_ROOT / "paper").is_dir()


def test_internal_is_sibling_not_under_zenodo():
    assert INTERNAL_DIR == PROJECT_ROOT / "_internal"
    assert not str(INTERNAL_DIR.resolve()).startswith(str(ZENODO_ROOT.resolve()))
    assert not (ZENODO_ROOT / "_internal").exists()


def test_ensure_zenodo_layout_keys():
    layout = ensure_zenodo_layout()
    assert layout["zenodo_root"] == ZENODO_ROOT
    for key in ("protocol", "data", "outputs", "manifests", "docs"):
        assert key in layout
        assert isinstance(layout[key], Path)
