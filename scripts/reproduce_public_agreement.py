#!/usr/bin/env python3
"""Recompute locked agreement metrics from the public 67-unit table only."""

from __future__ import annotations

import json
import sys

from scse.public_evidence import write_public_outputs


def main() -> int:
    payload = write_public_outputs()
    ok = payload["all_lock_checks_pass"]
    print(
        json.dumps(
            {
                "ok": ok,
                "n": payload["human_evidence_n"],
                "binary_kappa": payload["exercises"]["binary_validation"]["cohen_kappa"],
                "kappa_max": payload["exercises"]["binary_validation"]["kappa_max"],
                "binary_bootstrap_n_invalid": payload["exercises"]["binary_validation"][
                    "cohen_kappa_bootstrap_n_invalid"
                ],
                "n_disagree": payload["disagreement_direction"]["combined"]["n_disagree"],
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
