"""Ingest pinned ParlaMint-ES TEI releases.

Not implemented: Phase 2 must pin the exact release URL, version, and checksum
before any parsing logic is written against the real format.
"""

from __future__ import annotations

from scse.phase_gate import stub_main


def main() -> int:
    return stub_main(
        __name__,
        "Phase 2",
        "Phase 2 data acquisition has not yet been completed.",
    )


if __name__ == "__main__":
    raise SystemExit(main())
