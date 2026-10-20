"""Release packaging: manifests, checksums, Zenodo archive helpers.

Not implemented until Phase 10. Must refuse if _internal/ material is present.
"""

from __future__ import annotations

from scse.phase_gate import stub_main


def main() -> int:
    return stub_main(
        __name__,
        "Phase 10",
        "This target depends on a later research phase that has not started.",
    )


if __name__ == "__main__":
    raise SystemExit(main())
