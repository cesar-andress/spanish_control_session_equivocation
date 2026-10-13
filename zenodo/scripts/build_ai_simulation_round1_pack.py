"""Build blinded Round-1 AI simulation package (no fabricated returns)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from scse.ai_simulation_round1 import build_package  # noqa: E402


def main() -> int:
    meta = build_package()
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
