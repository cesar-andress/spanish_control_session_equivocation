"""Shared phase-gate helper: refuse to fabricate later-phase outputs."""

from __future__ import annotations

import sys


class PhaseNotReadyError(RuntimeError):
    """Raised when a Make/CLI target is called before its scientific phase."""


def require_phase(phase: str, message: str) -> None:
    """Abort with a clear message; never produce placeholder scientific outputs."""
    raise PhaseNotReadyError(f"[{phase}] {message}")


def stub_main(module_name: str, phase: str, message: str) -> int:
    print(f"{module_name}: {message}", file=sys.stderr)
    return 1
