"""CLI entrypoints for make data / make pool."""

from __future__ import annotations

import json
import sys


def cmd_data() -> int:
    from scse.build_pool import build_pool
    from scse.ingest_parlamint import ensure_parlamint_archive

    # Acquire ParlaMint first (fast if cached); full pool build also fetches Congreso.
    pointer = ensure_parlamint_archive()
    print(json.dumps({"parlamint": pointer}, indent=2, ensure_ascii=False))
    summary = build_pool()
    print(json.dumps({"pool_summary_keys": list(summary.keys()), "eligible": summary["eligible_count"]}, indent=2))
    return 0


def cmd_pool() -> int:
    from scse.build_pool import build_pool

    summary = build_pool()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print("Usage: python -m scse.cli data|pool")
        return 2
    cmd = argv[0]
    if cmd == "data":
        return cmd_data()
    if cmd == "pool":
        return cmd_pool()
    print(f"Unknown command {cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
