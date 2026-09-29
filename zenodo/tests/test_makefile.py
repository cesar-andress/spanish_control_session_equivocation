"""Makefile smoke tests available at scaffold time."""

from __future__ import annotations

import subprocess

from scse.paths import ZENODO_ROOT


def test_make_help():
    result = subprocess.run(
        ["make", "help"],
        cwd=str(ZENODO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "make test" in result.stdout
