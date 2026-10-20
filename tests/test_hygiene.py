"""Public-tree hygiene tests."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from scse.paths import ZENODO_ROOT

HOME_PATTERN = re.compile(re.escape("/home/" + "cesar" + "/"))
PROMPT_NAME = re.compile(r"prompt", re.IGNORECASE)


def _text_files() -> list[Path]:
    skip = {".git", ".venv", "__pycache__", ".pytest_cache"}
    out: list[Path] = []
    for path in ZENODO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip for part in path.parts):
            continue
        if path.suffix in {
            ".py",
            ".md",
            ".txt",
            ".yml",
            ".yaml",
            ".toml",
            ".json",
            ".csv",
            ".cff",
            ".gitignore",
        } or path.name in {"Makefile", "LICENSE", "CITATION.cff"}:
            out.append(path)
    return out


def test_no_internal_directory_under_zenodo():
    assert not (ZENODO_ROOT / "_internal").exists()


def test_no_prompt_files_under_zenodo():
    offenders = [
        p
        for p in ZENODO_ROOT.rglob("*")
        if p.is_file() and PROMPT_NAME.search(p.name) and p.suffix in {".md", ".txt"}
    ]
    assert offenders == []


def test_no_absolute_home_paths_in_public_text():
    offenders: list[str] = []
    for path in _text_files():
        # Hygiene scanner constructs the forbidden string; skip its builder line
        if path.name == "hygiene_scan.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if HOME_PATTERN.search(text):
            offenders.append(str(path.relative_to(ZENODO_ROOT)))
    assert offenders == []


def test_hygiene_script_passes():
    script = ZENODO_ROOT / "scripts" / "hygiene_scan.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ZENODO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_make_data_and_pool_targets_exist():
    makefile = (ZENODO_ROOT / "Makefile").read_text(encoding="utf-8")
    assert "scse.cli data" in makefile
    assert "scse.cli pool" in makefile
