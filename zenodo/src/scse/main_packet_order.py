"""Deterministic distinct main-packet orderings (Phase 6B).

Same unit set for both annotators; different shuffle orders.
Packets are NOT issued here.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from scse.main_frame import MAIN_PRIVATE, load_main_corpus
from scse.paths import PROJECT_ROOT, PROTOCOL_DIR

SEED_STRING_DANIEL = (
    "spanish_control_session_equivocation|main_packet_order|Daniel|phase6b"
)
SEED_STRING_JOSE = (
    "spanish_control_session_equivocation|main_packet_order|Jose_Jaime|phase6b"
)


def derive_seed(text: str) -> int:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def build_main_orderings() -> dict:
    corpus = load_main_corpus()
    if len(corpus) != 100:
        raise ValueError(f"main corpus must be N=100 before order freeze, got {len(corpus)}")
    base = corpus["exchange_id"].tolist()
    seed_d = derive_seed(SEED_STRING_DANIEL)
    seed_j = derive_seed(SEED_STRING_JOSE)
    if seed_d == seed_j:
        raise ValueError("annotator order seeds collided")

    rng_d = np.random.default_rng(seed_d)
    rng_j = np.random.default_rng(seed_j)
    order_d = rng_d.permutation(base).tolist()
    order_j = rng_j.permutation(base).tolist()
    if order_d == order_j:
        raise ValueError("annotator permutations identical; change seed strings")
    if sorted(order_d) != sorted(base) or sorted(order_j) != sorted(base):
        raise ValueError("ordering lost units")

    payload = {
        "status": "pre_outcome_orders_frozen",
        "n": 100,
        "human_packets_issued": False,
        "daniel_seed": seed_d,
        "jose_jaime_seed": seed_j,
        "daniel_seed_string": SEED_STRING_DANIEL,
        "jose_jaime_seed_string": SEED_STRING_JOSE,
        "daniel_exchange_id_order": order_d,
        "jose_jaime_exchange_id_order": order_j,
        "same_set": True,
        "same_order": False,
        "note": (
            "Distinct deterministic random orders to reduce shared order/fatigue "
            "effects. Do not issue final human packets until codebook freeze."
        ),
    }
    MAIN_PRIVATE.mkdir(parents=True, exist_ok=True)
    path = MAIN_PRIVATE / "MAIN_PACKET_ORDERINGS.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Update seeds.yaml without setting a scientific main_sample draw seed
    seeds_path = PROTOCOL_DIR / "seeds.yaml"
    data = yaml.safe_load(seeds_path.read_text(encoding="utf-8"))
    seeds = data.setdefault("seeds", data)
    seeds["main_packet_order_daniel"] = seed_d
    seeds["main_packet_order_jose_jaime"] = seed_j
    # main_sample remains null: census, not a subsample draw
    seeds["main_sample"] = None
    note = data.get("notes") or ""
    extra = (
        " main_packet_order_daniel/jose_jaime = Phase 6B distinct presentation "
        "orders for future packets (not a sample draw)."
    )
    if "main_packet_order_daniel" not in str(note):
        data["notes"] = (str(note).rstrip() + extra).strip()
    data["status"] = "calibration_seeds_set_main_orders_phase6b"
    seeds_path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return {
        "path": str(path.relative_to(PROJECT_ROOT)),
        "daniel_seed": seed_d,
        "jose_jaime_seed": seed_j,
        "issued": False,
    }
