"""Sampling helpers (calibration / main).

Scientific seeds are unset until protocol freeze. Helpers must be deterministic
for a fixed seed once frozen.
"""

from __future__ import annotations

import random

from scse.phase_gate import stub_main
from scse.seeds import get_seed


def sample_without_replacement(
    population: list[str],
    k: int,
    *,
    seed_name: str | None = None,
    seed: int | None = None,
) -> list[str]:
    """Deterministic sample for a fixed integer seed.

    Prefer ``seed_name`` once the named seed is frozen in protocol/seeds.yaml.
    Passing ``seed`` directly is allowed for unit tests only.
    """
    if seed is None:
        if seed_name is None:
            raise ValueError("Provide seed_name or seed")
        seed = get_seed(seed_name)
    rng = random.Random(seed)
    items = list(population)
    rng.shuffle(items)
    return items[:k]


def main() -> int:
    return stub_main(
        __name__,
        "Phase 4/5",
        "This target depends on a later research phase that has not started.",
    )


if __name__ == "__main__":
    raise SystemExit(main())
