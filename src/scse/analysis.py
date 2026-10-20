"""Pre-registered primary and secondary analyses.

Confirmatory and exploratory outputs must remain distinguishable.
Not implemented until Phase 8.
"""

from __future__ import annotations

from scse.phase_gate import stub_main


def main() -> int:
    return stub_main(
        __name__,
        "Phase 8",
        "This target depends on a later research phase that has not started.",
    )


if __name__ == "__main__":
    raise SystemExit(main())
