#!/usr/bin/env python3
"""Scan the public zenodo/ tree for hygiene violations.

Fails on absolute personal home paths, agent-config leakage, private-area
markers, and common credential patterns. Avoids over-aggressive scholarly
false positives (e.g. the English word \"token\" in linguistics prose is only
flagged in assignment-like forms such as token=).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ZENODO_ROOT = Path(__file__).resolve().parents[1]

# Text-like suffixes to scan
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".toml",
    ".json",
    ".csv",
    ".tsv",
    ".cff",
    ".ini",
    ".cfg",
    ".sh",
    ".tex",
    ".bib",
    ".Makefile",
    "",
}

SKIP_DIR_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "uv.lock",  # not a dir; listed for safety
}

# Build path patterns without embedding personal absolute paths as plain literals
# in scholarly docs; the scanner still detects them in other public files.
_HOME_USER = "/home/" + "cesar" + "/"

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("absolute_home_cesar", re.compile(re.escape(_HOME_USER))),
    ("cursor_dir", re.compile(r"(^|/)\.cursor(/|$)")),
    ("internal_marker", re.compile(r"(^|/)_internal(/|$)")),
    ("api_key", re.compile(r"api[_-]?key\s*[=:]", re.IGNORECASE)),
    ("token_assign", re.compile(r"\btoken\s*=", re.IGNORECASE)),
    ("private_key_block", re.compile(r"BEGIN PRIVATE KEY")),
]

PROMPT_NAME_RE = re.compile(r"prompt", re.IGNORECASE)


def iter_public_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.name == "uv.lock":
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
            "Makefile",
            "LICENSE",
            "CITATION.cff",
            ".gitignore",
        }:
            files.append(path)
    return files


def scan() -> list[str]:
    violations: list[str] = []

    # Structural: _internal must not exist under zenodo/
    internal = ZENODO_ROOT / "_internal"
    if internal.exists():
        violations.append(f"structural: {internal} exists under zenodo/")

    # Structural: no .cursor under zenodo/
    cursor = ZENODO_ROOT / ".cursor"
    if cursor.exists():
        violations.append(f"structural: {cursor} exists under zenodo/")

    for path in iter_public_files(ZENODO_ROOT):
        rel = path.relative_to(ZENODO_ROOT).as_posix()
        if PROMPT_NAME_RE.search(path.name) and path.suffix in {".md", ".txt", ".yml", ".yaml"}:
            violations.append(f"prompt_filename: {rel}")
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            violations.append(f"unreadable: {rel} ({exc})")
            continue
        for label, pattern in PATTERNS:
            if not pattern.search(text):
                continue
            # Allow documenting the private-area name in README/docs without
            # treating that documentation as leakage.
            if label == "internal_marker" and rel in {
                "README.md",
                "docs/private_area.md",
                "docs/licensing.md",
            }:
                continue
            if path.name == "hygiene_scan.py" and label in {
                "api_key",
                "token_assign",
                "private_key_block",
                "cursor_dir",
                "internal_marker",
            }:
                continue
            violations.append(f"{label}: {rel}")
    return violations


def main() -> int:
    violations = scan()
    if violations:
        print("HYGIENE FAIL:", file=sys.stderr)
        for item in violations:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("HYGIENE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
