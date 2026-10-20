"""Named scientific seeds.

Final seed integers are frozen in protocol/ only when the corresponding phase
freezes. Scripts must request seeds by name rather than scattering literals.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Final

# Registry of named seed slots. Values remain None until a phase freezes them
# in protocol/seeds.yaml (or equivalent) and this mapping is updated from that
# single source.
SEED_NAMES: Final[tuple[str, ...]] = (
    "development",
    "link_audit",
    "calibration",
    "main_sample",
    "bootstrap",
)

# In-code defaults are intentionally unset for scientific sampling slots.
# A non-scientific unit-test seed is provided only for determinism checks.
_UNIT_TEST_SEED: Final[int] = 42


class SeedNotFrozenError(RuntimeError):
    """Raised when a named scientific seed has not been frozen yet."""


def _load_frozen_seeds() -> Mapping[str, int | None]:
    """Load frozen seeds from protocol/seeds.yaml if present."""
    from scse.paths import PROTOCOL_DIR

    path = PROTOCOL_DIR / "seeds.yaml"
    if not path.is_file():
        return {name: None for name in SEED_NAMES}
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PyYAML is required to read protocol/seeds.yaml") from exc
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    seeds = data.get("seeds", data)
    out: dict[str, int | None] = {}
    for name in SEED_NAMES:
        value = seeds.get(name)
        out[name] = int(value) if value is not None else None
    return out


def get_seed(name: str, *, allow_unit_test_fallback: bool = False) -> int:
    """Return a frozen named seed.

    Parameters
    ----------
    name:
        One of SEED_NAMES, or ``unit_test`` for non-scientific tests.
    allow_unit_test_fallback:
        If True and name is ``unit_test``, return the fixed unit-test seed.
    """
    if name == "unit_test":
        if not allow_unit_test_fallback:
            raise SeedNotFrozenError(
                "unit_test seed is only available with allow_unit_test_fallback=True"
            )
        return _UNIT_TEST_SEED

    if name not in SEED_NAMES:
        raise KeyError(f"Unknown seed name {name!r}; expected one of {SEED_NAMES}")

    frozen = _load_frozen_seeds()
    value = frozen.get(name)
    if value is None:
        raise SeedNotFrozenError(
            f"Seed {name!r} is not frozen yet. "
            "Record it in protocol/seeds.yaml when the relevant phase freezes."
        )
    return value


def deterministic_draw(name: str, population: list[str], k: int) -> list[str]:
    """Deterministic sample without replacement for a frozen seed.

    Not used for scientific sampling until the named seed is frozen.
    """
    import random

    seed = get_seed(name)
    rng = random.Random(seed)
    if k > len(population):
        raise ValueError("k larger than population")
    items = list(population)
    rng.shuffle(items)
    return items[:k]


def seed_fingerprint(name: str, seed: int) -> str:
    """Stable short fingerprint for logging (not a secret)."""
    payload = f"{name}:{seed}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]
