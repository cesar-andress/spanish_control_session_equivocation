"""Deterministic seed utilities."""

from __future__ import annotations

import pytest

from scse.sampling import sample_without_replacement
from scse.seeds import SeedNotFrozenError, get_seed, seed_fingerprint


def test_unit_test_seed_is_deterministic():
    a = get_seed("unit_test", allow_unit_test_fallback=True)
    b = get_seed("unit_test", allow_unit_test_fallback=True)
    assert a == b == 42


def test_scientific_seeds_not_frozen_yet():
    with pytest.raises(SeedNotFrozenError):
        get_seed("main_sample")
    with pytest.raises(SeedNotFrozenError):
        get_seed("calibration")


def test_sampling_helper_deterministic_for_fixed_seed():
    population = [f"u{i:03d}" for i in range(50)]
    a = sample_without_replacement(population, 10, seed=12345)
    b = sample_without_replacement(population, 10, seed=12345)
    c = sample_without_replacement(population, 10, seed=99999)
    assert a == b
    assert a != c
    assert len(a) == 10
    assert len(set(a)) == 10


def test_seed_fingerprint_stable():
    assert seed_fingerprint("unit_test", 42) == seed_fingerprint("unit_test", 42)
