"""Path and public/private separation tests."""

from __future__ import annotations

from pathlib import Path

from scse.paths import (
    INTERNAL_DIR,
    PROJECT_ROOT,
    STANDALONE_PUBLIC,
    ZENODO_ROOT,
    ensure_zenodo_layout,
)


def test_package_root_has_expected_layout():
    assert (ZENODO_ROOT / "pyproject.toml").is_file()
    assert (ZENODO_ROOT / "src" / "scse").is_dir()
    assert (ZENODO_ROOT / "protocol").is_dir()


def test_project_root_layout():
    if STANDALONE_PUBLIC:
        assert PROJECT_ROOT == ZENODO_ROOT
    else:
        assert (PROJECT_ROOT / "zenodo").resolve() == ZENODO_ROOT.resolve()
        assert (PROJECT_ROOT / "paper").is_dir()


def test_internal_is_not_under_package_root():
    assert INTERNAL_DIR == PROJECT_ROOT / "_internal"
    assert not (ZENODO_ROOT / "_internal").exists()
    if STANDALONE_PUBLIC:
        assert INTERNAL_DIR == ZENODO_ROOT / "_internal"
    else:
        assert not str(INTERNAL_DIR.resolve()).startswith(str(ZENODO_ROOT.resolve()) + "/")


def test_ensure_zenodo_layout_keys():
    layout = ensure_zenodo_layout()
    assert layout["zenodo_root"] == ZENODO_ROOT
    for key in ("protocol", "data", "outputs", "manifests", "docs"):
        assert key in layout
        assert isinstance(layout[key], Path)
