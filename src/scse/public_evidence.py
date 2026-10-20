"""Public recomputation of locked agreement metrics from HUMAN_EVIDENCE_67_PUBLIC.csv.

Requires only files inside the public package root. No ``_internal/`` access.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

import pandas as pd

from scse.calibration_metrics import (
    CATEGORIES,
    _cohens_kappa,
    krippendorff_alpha_nominal,
    normalize_label,
    summarize_round1,
)
from scse.measurement_evidence import (
    BOOTSTRAP_N,
    BOOTSTRAP_SEED,
    ORDINAL_3,
    ORDINAL_BIN,
    bootstrap_metric_ci,
    kappa_max_from_labels,
)
from scse.paths import DATA_DIR, DERIVED_DIR, ZENODO_ROOT

PUBLIC_CSV = DATA_DIR / "HUMAN_EVIDENCE_67_PUBLIC.csv"
PUBLIC_SUMMARY_JSON = DERIVED_DIR / "measurement_agreement_summary.json"
PUBLIC_REPRO_JSON = DERIVED_DIR / "measurement_agreement_public_repro.json"

EXERCISE_COUNTS = {
    "development": 15,
    "calibration_round1": 20,
    "calibration_round2": 20,
    "binary_validation": 12,
}

# Locked point estimates (3 d.p. display values from evidence lock)
LOCKED = {
    "development": {
        "raw_agreement": 0.667,
        "cohen_kappa_3way": 0.510,
        "krippendorff_alpha": 0.498,
        "binary_collapse_kappa": 0.857,
    },
    "round1_initial_18": {
        "raw_agreement": 0.889,
        "cohen_kappa_3way": 0.815,
        "krippendorff_alpha": 0.815,
        "binary_collapse_kappa": 0.880,
    },
    "round1_final_20": {
        "raw_agreement": 0.800,
        "cohen_kappa_3way": 0.672,
        "krippendorff_alpha": 0.669,
        "binary_collapse_kappa": 0.783,
    },
    "round2": {
        "raw_agreement": 0.550,
        "cohen_kappa_3way": 0.159,
        "krippendorff_alpha": 0.126,
        "binary_collapse_kappa": 0.121,
    },
    "pooled_r1_r2": {
        "raw_agreement": 0.675,
        "cohen_kappa_3way": 0.470,
        "krippendorff_alpha": 0.463,
        "binary_collapse_kappa": 0.501,
    },
    "binary_validation": {
        "raw_agreement": 0.667,
        "cohen_kappa": 0.226,
        "kappa_max": 0.226,
        "n_agree": 8,
        "coder_A_yes": 11,
        "coder_B_yes": 7,
    },
    "directions": {
        "development": {"coder_A_more": 4, "coder_B_more": 1},
        "calibration_round1": {"coder_A_more": 0, "coder_B_more": 4},
        "calibration_round2": {"coder_A_more": 4, "coder_B_more": 5},
        "binary_validation": {"coder_A_more": 4, "coder_B_more": 0},
        "combined": {"coder_A_more": 12, "coder_B_more": 10, "n_disagree": 22},
    },
}


def load_public_evidence(path: Path | None = None) -> pd.DataFrame:
    p = path or PUBLIC_CSV
    df = pd.read_csv(p)
    if len(df) != 67:
        raise RuntimeError(f"expected 67 rows, got {len(df)}")
    counts = df["exercise"].value_counts().to_dict()
    for k, v in EXERCISE_COUNTS.items():
        if counts.get(k) != v:
            raise RuntimeError(f"{k}: expected {v}, got {counts.get(k)}")
    return df


def _direction_3(a: str, b: str) -> str:
    if a == b:
        return "agree"
    oa, ob = ORDINAL_3[a], ORDINAL_3[b]
    if ob > oa:
        return "coder_B_more_responsive"
    if oa > ob:
        return "coder_A_more_responsive"
    return "non_ordinal"


def _direction_bin(a: str, b: str) -> str:
    if a == b:
        return "agree"
    if ORDINAL_BIN[b] > ORDINAL_BIN[a]:
        return "coder_B_more_responsive"
    if ORDINAL_BIN[a] > ORDINAL_BIN[b]:
        return "coder_A_more_responsive"
    return "non_ordinal"


def direction_counts(a: Sequence[str], b: Sequence[str], *, binary: bool) -> dict:
    n_a = n_b = n_d = 0
    for x, y in zip(a, b):
        d = _direction_bin(x, y) if binary else _direction_3(x, y)
        if d == "coder_A_more_responsive":
            n_a += 1
            n_d += 1
        elif d == "coder_B_more_responsive":
            n_b += 1
            n_d += 1
        elif d != "agree":
            n_d += 1
    return {"coder_A_more": n_a, "coder_B_more": n_b, "n_disagree": n_d}


def metrics_3way_public(a_es: list[str], b_es: list[str]) -> dict:
    s = summarize_round1(a_es, b_es)
    a_en = [normalize_label(x) for x in a_es]
    b_en = [normalize_label(x) for x in b_es]
    k3 = bootstrap_metric_ci(
        a_en, b_en, lambda x, y: _cohens_kappa(x, y, CATEGORIES)
    )
    al = bootstrap_metric_ci(a_en, b_en, krippendorff_alpha_nominal)
    ba = ["explicit" if x == "explicit_reply" else "non_explicit" for x in a_en]
    bb = ["explicit" if x == "explicit_reply" else "non_explicit" for x in b_en]
    kb = bootstrap_metric_ci(
        ba, bb, lambda x, y: _cohens_kappa(x, y, ("explicit", "non_explicit"))
    )
    return {
        "n": s["n"],
        "raw_agreement": s["raw_agreement"],
        "cohen_kappa_3way": s["cohen_kappa_3way"],
        "cohen_kappa_3way_ci": k3,
        "krippendorff_alpha_nominal": s["krippendorff_alpha_nominal"],
        "krippendorff_alpha_ci": al,
        "cohen_kappa_explicit_vs_rest": s["cohen_kappa_explicit_vs_rest"],
        "cohen_kappa_explicit_vs_rest_ci": kb,
    }


def metrics_binary_public(a: list[str], b: list[str]) -> dict:
    import random

    labels = ["direct_resolution_yes", "direct_resolution_no"]
    n = len(a)
    n_agree = sum(x == y for x, y in zip(a, b))
    raw = n_agree / n
    k = _cohens_kappa(a, b, labels)
    k_ci = bootstrap_metric_ci(a, b, lambda x, y: _cohens_kappa(x, y, labels))
    # Extra diagnostic: count valid draws that yield exactly κ=0 (CI floor driver).
    rng = random.Random(BOOTSTRAP_SEED)
    n_zero = 0
    for _ in range(BOOTSTRAP_N):
        idx = [rng.randrange(n) for _ in range(n)]
        sa = [a[i] for i in idx]
        sb = [b[i] for i in idx]
        try:
            v = float(_cohens_kappa(sa, sb, labels))
            if v == v and abs(v) < 1e-12:
                n_zero += 1
        except Exception:
            pass
    k_ci = {**k_ci, "n_zero_kappa": n_zero}
    km = kappa_max_from_labels(a, b, labels)
    return {
        "n": n,
        "raw_agreement": raw,
        "n_agree": n_agree,
        "cohen_kappa": k,
        "cohen_kappa_ci": k_ci,
        "kappa_max": km,
        "coder_A_yes": sum(x == "direct_resolution_yes" for x in a),
        "coder_B_yes": sum(x == "direct_resolution_yes" for x in b),
        "observed_equals_kappa_max": km["observed_equals_kappa_max"],
        "po_max": km["po_max"],
        "max_agreements": km["max_agreements"],
    }


def _approx(a: float, b: float, tol: float = 5e-4) -> bool:
    return abs(float(a) - float(b)) <= tol


def reproduce_all(path: Path | None = None) -> dict:
    df = load_public_evidence(path)

    dev = df[df.exercise == "development"]
    r1 = df[df.exercise == "calibration_round1"]
    r1_18 = r1[r1["usable_in_initial_round1_18"] == 1]
    r2 = df[df.exercise == "calibration_round2"]
    pool = pd.concat([r1, r2], ignore_index=True)
    bv = df[df.exercise == "binary_validation"]

    m_dev = metrics_3way_public(list(dev.coder_A_label), list(dev.coder_B_label))
    m_r1_18 = metrics_3way_public(list(r1_18.coder_A_label), list(r1_18.coder_B_label))
    m_r1_20 = metrics_3way_public(list(r1.coder_A_label), list(r1.coder_B_label))
    m_r2 = metrics_3way_public(list(r2.coder_A_label), list(r2.coder_B_label))
    m_pool = metrics_3way_public(list(pool.coder_A_label), list(pool.coder_B_label))
    m_bin = metrics_binary_public(list(bv.coder_A_label), list(bv.coder_B_label))

    dirs = {
        "development": direction_counts(
            list(dev.coder_A_label), list(dev.coder_B_label), binary=False
        ),
        "calibration_round1": direction_counts(
            list(r1.coder_A_label), list(r1.coder_B_label), binary=False
        ),
        "calibration_round2": direction_counts(
            list(r2.coder_A_label), list(r2.coder_B_label), binary=False
        ),
        "binary_validation": direction_counts(
            list(bv.coder_A_label), list(bv.coder_B_label), binary=True
        ),
    }
    combined = {
        "coder_A_more": sum(d["coder_A_more"] for d in dirs.values()),
        "coder_B_more": sum(d["coder_B_more"] for d in dirs.values()),
        "n_disagree": sum(d["n_disagree"] for d in dirs.values()),
    }

    checks = {
        "development": {
            "raw": _approx(m_dev["raw_agreement"], LOCKED["development"]["raw_agreement"], 5e-4),
            "kappa3": _approx(m_dev["cohen_kappa_3way"], LOCKED["development"]["cohen_kappa_3way"]),
            "alpha": _approx(
                m_dev["krippendorff_alpha_nominal"], LOCKED["development"]["krippendorff_alpha"]
            ),
            "binary_kappa": _approx(
                m_dev["cohen_kappa_explicit_vs_rest"],
                LOCKED["development"]["binary_collapse_kappa"],
            ),
        },
        "round1_initial_18": {
            "n": len(r1_18) == 18,
            "raw": _approx(m_r1_18["raw_agreement"], LOCKED["round1_initial_18"]["raw_agreement"], 5e-4),
            "kappa3": _approx(
                m_r1_18["cohen_kappa_3way"], LOCKED["round1_initial_18"]["cohen_kappa_3way"]
            ),
            "alpha": _approx(
                m_r1_18["krippendorff_alpha_nominal"],
                LOCKED["round1_initial_18"]["krippendorff_alpha"],
            ),
            "binary_kappa": _approx(
                m_r1_18["cohen_kappa_explicit_vs_rest"],
                LOCKED["round1_initial_18"]["binary_collapse_kappa"],
            ),
        },
        "round1_final_20": {
            "n": len(r1) == 20,
            "raw": _approx(m_r1_20["raw_agreement"], LOCKED["round1_final_20"]["raw_agreement"], 5e-4),
            "kappa3": _approx(
                m_r1_20["cohen_kappa_3way"], LOCKED["round1_final_20"]["cohen_kappa_3way"]
            ),
            "alpha": _approx(
                m_r1_20["krippendorff_alpha_nominal"],
                LOCKED["round1_final_20"]["krippendorff_alpha"],
            ),
            "binary_kappa": _approx(
                m_r1_20["cohen_kappa_explicit_vs_rest"],
                LOCKED["round1_final_20"]["binary_collapse_kappa"],
            ),
        },
        "round2": {
            "raw": _approx(m_r2["raw_agreement"], LOCKED["round2"]["raw_agreement"], 5e-4),
            "kappa3": _approx(m_r2["cohen_kappa_3way"], LOCKED["round2"]["cohen_kappa_3way"]),
            "alpha": _approx(
                m_r2["krippendorff_alpha_nominal"], LOCKED["round2"]["krippendorff_alpha"]
            ),
            "binary_kappa": _approx(
                m_r2["cohen_kappa_explicit_vs_rest"], LOCKED["round2"]["binary_collapse_kappa"]
            ),
        },
        "pooled_r1_r2": {
            "raw": _approx(m_pool["raw_agreement"], LOCKED["pooled_r1_r2"]["raw_agreement"], 5e-4),
            "kappa3": _approx(
                m_pool["cohen_kappa_3way"], LOCKED["pooled_r1_r2"]["cohen_kappa_3way"]
            ),
            "alpha": _approx(
                m_pool["krippendorff_alpha_nominal"], LOCKED["pooled_r1_r2"]["krippendorff_alpha"]
            ),
            "binary_kappa": _approx(
                m_pool["cohen_kappa_explicit_vs_rest"],
                LOCKED["pooled_r1_r2"]["binary_collapse_kappa"],
            ),
        },
        "binary_validation": {
            "raw": _approx(
                m_bin["raw_agreement"], LOCKED["binary_validation"]["raw_agreement"], 5e-4
            ),
            "kappa": _approx(m_bin["cohen_kappa"], LOCKED["binary_validation"]["cohen_kappa"]),
            "kappa_max": _approx(
                m_bin["kappa_max"]["kappa_max"], LOCKED["binary_validation"]["kappa_max"]
            ),
            "equals_max": m_bin["observed_equals_kappa_max"] is True,
            "marginals": m_bin["coder_A_yes"] == 11 and m_bin["coder_B_yes"] == 7,
        },
        "directions": {
            "development": dirs["development"]["coder_A_more"] == 4
            and dirs["development"]["coder_B_more"] == 1,
            "round1": dirs["calibration_round1"]["coder_A_more"] == 0
            and dirs["calibration_round1"]["coder_B_more"] == 4,
            "round2": dirs["calibration_round2"]["coder_A_more"] == 4
            and dirs["calibration_round2"]["coder_B_more"] == 5,
            "binary": dirs["binary_validation"]["coder_A_more"] == 4
            and dirs["binary_validation"]["coder_B_more"] == 0,
            "combined": combined["n_disagree"] == 22
            and combined["coder_A_more"] == 12
            and combined["coder_B_more"] == 10,
        },
    }

    payload = {
        "title": "Public recomputation from HUMAN_EVIDENCE_67_PUBLIC.csv",
        "version": "1.0.1",
        "source_csv": str(PUBLIC_CSV.relative_to(ZENODO_ROOT)),
        "human_evidence_n": 67,
        "xiv_reply_outcomes_included": False,
        "ai_reply_labels_included": False,
        "coder_convention": (
            "coder_A and coder_B are stable anonymous labels for the two "
            "independent expert annotators across all 67 units."
        ),
        "bootstrap": {
            "n_resamples": BOOTSTRAP_N,
            "seed": BOOTSTRAP_SEED,
            "interval": "percentile_95",
        },
        "note_binary_instrument": (
            "The redesigned binary validation uses a DIFFERENT instrument "
            "(direct_resolution) and must not be pooled with the three-category "
            "explicit-versus-rest collapse."
        ),
        "exercises": {
            "development": {
                "n": m_dev["n"],
                "raw_agreement": round(m_dev["raw_agreement"], 3),
                "cohen_kappa_3way": round(m_dev["cohen_kappa_3way"], 3),
                "cohen_kappa_3way_ci": [
                    round(m_dev["cohen_kappa_3way_ci"]["ci_low"], 3),
                    round(m_dev["cohen_kappa_3way_ci"]["ci_high"], 3),
                ],
                "krippendorff_alpha": round(m_dev["krippendorff_alpha_nominal"], 3),
                "krippendorff_alpha_ci": [
                    round(m_dev["krippendorff_alpha_ci"]["ci_low"], 3),
                    round(m_dev["krippendorff_alpha_ci"]["ci_high"], 3),
                ],
                "binary_collapse_kappa": round(m_dev["cohen_kappa_explicit_vs_rest"], 3),
                "binary_collapse_kappa_ci": [
                    round(m_dev["cohen_kappa_explicit_vs_rest_ci"]["ci_low"], 3),
                    round(m_dev["cohen_kappa_explicit_vs_rest_ci"]["ci_high"], 3),
                ],
                "bootstrap_invalid_draws": {
                    "cohen_kappa_3way": m_dev["cohen_kappa_3way_ci"]["n_invalid"],
                    "krippendorff_alpha": m_dev["krippendorff_alpha_ci"]["n_invalid"],
                    "binary_collapse_kappa": m_dev["cohen_kappa_explicit_vs_rest_ci"][
                        "n_invalid"
                    ],
                },
            },
            "round1_initial_18": {
                "n": m_r1_18["n"],
                "raw_agreement": round(m_r1_18["raw_agreement"], 3),
                "cohen_kappa_3way": round(m_r1_18["cohen_kappa_3way"], 3),
                "cohen_kappa_3way_ci": [
                    round(m_r1_18["cohen_kappa_3way_ci"]["ci_low"], 3),
                    round(m_r1_18["cohen_kappa_3way_ci"]["ci_high"], 3),
                ],
                "krippendorff_alpha": round(m_r1_18["krippendorff_alpha_nominal"], 3),
                "binary_collapse_kappa": round(m_r1_18["cohen_kappa_explicit_vs_rest"], 3),
                "note": (
                    "Excludes Round-1 cases with administrative_clarification_flag=1 "
                    "(usable_in_initial_round1_18=0). Clarification is not adjudication."
                ),
                "bootstrap_invalid_draws": {
                    "cohen_kappa_3way": m_r1_18["cohen_kappa_3way_ci"]["n_invalid"],
                    "krippendorff_alpha": m_r1_18["krippendorff_alpha_ci"]["n_invalid"],
                    "binary_collapse_kappa": m_r1_18["cohen_kappa_explicit_vs_rest_ci"][
                        "n_invalid"
                    ],
                },
            },
            "round1_final_20": {
                "n": m_r1_20["n"],
                "raw_agreement": round(m_r1_20["raw_agreement"], 3),
                "cohen_kappa_3way": round(m_r1_20["cohen_kappa_3way"], 3),
                "cohen_kappa_3way_ci": [
                    round(m_r1_20["cohen_kappa_3way_ci"]["ci_low"], 3),
                    round(m_r1_20["cohen_kappa_3way_ci"]["ci_high"], 3),
                ],
                "krippendorff_alpha": round(m_r1_20["krippendorff_alpha_nominal"], 3),
                "krippendorff_alpha_ci": [
                    round(m_r1_20["krippendorff_alpha_ci"]["ci_low"], 3),
                    round(m_r1_20["krippendorff_alpha_ci"]["ci_high"], 3),
                ],
                "binary_collapse_kappa": round(m_r1_20["cohen_kappa_explicit_vs_rest"], 3),
                "binary_collapse_kappa_ci": [
                    round(m_r1_20["cohen_kappa_explicit_vs_rest_ci"]["ci_low"], 3),
                    round(m_r1_20["cohen_kappa_explicit_vs_rest_ci"]["ci_high"], 3),
                ],
                "bootstrap_invalid_draws": {
                    "cohen_kappa_3way": m_r1_20["cohen_kappa_3way_ci"]["n_invalid"],
                    "krippendorff_alpha": m_r1_20["krippendorff_alpha_ci"]["n_invalid"],
                    "binary_collapse_kappa": m_r1_20["cohen_kappa_explicit_vs_rest_ci"][
                        "n_invalid"
                    ],
                },
            },
            "round2": {
                "n": m_r2["n"],
                "raw_agreement": round(m_r2["raw_agreement"], 3),
                "cohen_kappa_3way": round(m_r2["cohen_kappa_3way"], 3),
                "cohen_kappa_3way_ci": [
                    round(m_r2["cohen_kappa_3way_ci"]["ci_low"], 3),
                    round(m_r2["cohen_kappa_3way_ci"]["ci_high"], 3),
                ],
                "krippendorff_alpha": round(m_r2["krippendorff_alpha_nominal"], 3),
                "krippendorff_alpha_ci": [
                    round(m_r2["krippendorff_alpha_ci"]["ci_low"], 3),
                    round(m_r2["krippendorff_alpha_ci"]["ci_high"], 3),
                ],
                "binary_collapse_kappa": round(m_r2["cohen_kappa_explicit_vs_rest"], 3),
                "binary_collapse_kappa_ci": [
                    round(m_r2["cohen_kappa_explicit_vs_rest_ci"]["ci_low"], 3),
                    round(m_r2["cohen_kappa_explicit_vs_rest_ci"]["ci_high"], 3),
                ],
                "bootstrap_invalid_draws": {
                    "cohen_kappa_3way": m_r2["cohen_kappa_3way_ci"]["n_invalid"],
                    "krippendorff_alpha": m_r2["krippendorff_alpha_ci"]["n_invalid"],
                    "binary_collapse_kappa": m_r2["cohen_kappa_explicit_vs_rest_ci"][
                        "n_invalid"
                    ],
                },
            },
            "pooled_r1_r2": {
                "n": m_pool["n"],
                "raw_agreement": round(m_pool["raw_agreement"], 3),
                "cohen_kappa_3way": round(m_pool["cohen_kappa_3way"], 3),
                "cohen_kappa_3way_ci": [
                    round(m_pool["cohen_kappa_3way_ci"]["ci_low"], 3),
                    round(m_pool["cohen_kappa_3way_ci"]["ci_high"], 3),
                ],
                "krippendorff_alpha": round(m_pool["krippendorff_alpha_nominal"], 3),
                "krippendorff_alpha_ci": [
                    round(m_pool["krippendorff_alpha_ci"]["ci_low"], 3),
                    round(m_pool["krippendorff_alpha_ci"]["ci_high"], 3),
                ],
                "binary_collapse_kappa": round(m_pool["cohen_kappa_explicit_vs_rest"], 3),
                "binary_collapse_kappa_ci": [
                    round(m_pool["cohen_kappa_explicit_vs_rest_ci"]["ci_low"], 3),
                    round(m_pool["cohen_kappa_explicit_vs_rest_ci"]["ci_high"], 3),
                ],
                "bootstrap_invalid_draws": {
                    "cohen_kappa_3way": m_pool["cohen_kappa_3way_ci"]["n_invalid"],
                    "krippendorff_alpha": m_pool["krippendorff_alpha_ci"]["n_invalid"],
                    "binary_collapse_kappa": m_pool["cohen_kappa_explicit_vs_rest_ci"][
                        "n_invalid"
                    ],
                },
                "note": "Same three-category v0.3 instrument only; excludes binary redesign.",
            },
            "binary_validation": {
                "n": m_bin["n"],
                "raw_agreement": round(m_bin["raw_agreement"], 3),
                "n_agree": m_bin["n_agree"],
                "cohen_kappa": round(m_bin["cohen_kappa"], 3),
                "cohen_kappa_ci": [
                    round(m_bin["cohen_kappa_ci"]["ci_low"], 3),
                    round(m_bin["cohen_kappa_ci"]["ci_high"], 3),
                ],
                "cohen_kappa_bootstrap_n_valid": m_bin["cohen_kappa_ci"]["n_valid"],
                "cohen_kappa_bootstrap_n_invalid": m_bin["cohen_kappa_ci"]["n_invalid"],
                "cohen_kappa_bootstrap_n_zero": m_bin["cohen_kappa_ci"]["n_zero_kappa"],
                "coder_A_yes": m_bin["coder_A_yes"],
                "coder_B_yes": m_bin["coder_B_yes"],
                "kappa_max": round(m_bin["kappa_max"]["kappa_max"], 3),
                "po_max": m_bin["po_max"],
                "max_agreements": m_bin["max_agreements"],
                "observed_equals_kappa_max": m_bin["observed_equals_kappa_max"],
                "ci_floor_note": (
                    "The reported CI lower bound 0.000 can arise from degenerate "
                    "resamples (e.g. near-ceiling Yes rates); invalid/degenerate "
                    "draws are counted in cohen_kappa_bootstrap_n_invalid and "
                    "excluded from the percentile."
                ),
            },
        },
        "disagreement_direction": {
            "development": {
                "coder_A_more": dirs["development"]["coder_A_more"],
                "coder_B_more": dirs["development"]["coder_B_more"],
            },
            "round1": {
                "coder_A_more": dirs["calibration_round1"]["coder_A_more"],
                "coder_B_more": dirs["calibration_round1"]["coder_B_more"],
            },
            "round2": {
                "coder_A_more": dirs["calibration_round2"]["coder_A_more"],
                "coder_B_more": dirs["calibration_round2"]["coder_B_more"],
            },
            "binary_validation": {
                "coder_A_more": dirs["binary_validation"]["coder_A_more"],
                "coder_B_more": dirs["binary_validation"]["coder_B_more"],
            },
            "combined": combined,
            "stable_coder_severity_trait_supported": False,
        },
        "lock_checks": checks,
        "all_lock_checks_pass": all(
            all(v.values()) if isinstance(v, dict) else v
            for block in checks.values()
            for v in (block.values() if isinstance(block, dict) else [block])
        ),
    }
    # flatten all_lock_checks_pass properly
    flat_ok = True
    for block in checks.values():
        for v in block.values():
            if not v:
                flat_ok = False
    payload["all_lock_checks_pass"] = flat_ok
    return payload


def write_public_outputs(payload: dict | None = None) -> dict:
    payload = payload or reproduce_all()
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_REPRO_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    # Update aggregate summary for README consumers (coder_A/B naming)
    summary = {
        "title": "Locked agreement summary (public recomputable from unit table)",
        "version": "1.0.1",
        "note": (
            "Unit-level independent labels are in data/HUMAN_EVIDENCE_67_PUBLIC.csv. "
            "Source full texts, free-text comments, and original return documents "
            "are not redistributed. No XIV reply outcomes and no AI reply labels."
        ),
        "human_evidence_n": 67,
        "xiv_frame_n_context_only": 100,
        "xiv_reply_outcomes_included": False,
        "bootstrap": payload["bootstrap"],
        "exercises": {
            "development": payload["exercises"]["development"],
            "round1_initial_18": {
                k: payload["exercises"]["round1_initial_18"][k]
                for k in (
                    "n",
                    "raw_agreement",
                    "cohen_kappa_3way",
                    "cohen_kappa_3way_ci",
                    "note",
                )
                if k in payload["exercises"]["round1_initial_18"]
            },
            "round1_final_20": payload["exercises"]["round1_final_20"],
            "round2": payload["exercises"]["round2"],
            "pooled_r1_r2": payload["exercises"]["pooled_r1_r2"],
            "binary_validation": {
                "n": payload["exercises"]["binary_validation"]["n"],
                "raw_agreement": payload["exercises"]["binary_validation"]["raw_agreement"],
                "n_agree": payload["exercises"]["binary_validation"]["n_agree"],
                "cohen_kappa": payload["exercises"]["binary_validation"]["cohen_kappa"],
                "cohen_kappa_ci": payload["exercises"]["binary_validation"][
                    "cohen_kappa_ci"
                ],
                "cohen_kappa_bootstrap_n_valid": payload["exercises"]["binary_validation"][
                    "cohen_kappa_bootstrap_n_valid"
                ],
                "cohen_kappa_bootstrap_n_invalid": payload["exercises"][
                    "binary_validation"
                ]["cohen_kappa_bootstrap_n_invalid"],
                "cohen_kappa_bootstrap_n_zero": payload["exercises"]["binary_validation"][
                    "cohen_kappa_bootstrap_n_zero"
                ],
                "coder_A_yes": payload["exercises"]["binary_validation"]["coder_A_yes"],
                "coder_B_yes": payload["exercises"]["binary_validation"]["coder_B_yes"],
                "kappa_max": payload["exercises"]["binary_validation"]["kappa_max"],
                "observed_equals_kappa_max": payload["exercises"]["binary_validation"][
                    "observed_equals_kappa_max"
                ],
            },
        },
        "disagreement_direction": payload["disagreement_direction"],
        "public_unit_table": "data/HUMAN_EVIDENCE_67_PUBLIC.csv",
        "public_data_dictionary": "data/HUMAN_EVIDENCE_67_PUBLIC_DATA_DICTIONARY.md",
    }
    # preserve round1_initial richer fields if present
    summary["exercises"]["round1_initial_18"] = {
        "n": payload["exercises"]["round1_initial_18"]["n"],
        "raw_agreement": payload["exercises"]["round1_initial_18"]["raw_agreement"],
        "cohen_kappa_3way": payload["exercises"]["round1_initial_18"]["cohen_kappa_3way"],
        "cohen_kappa_3way_ci": payload["exercises"]["round1_initial_18"][
            "cohen_kappa_3way_ci"
        ],
        "krippendorff_alpha": payload["exercises"]["round1_initial_18"][
            "krippendorff_alpha"
        ],
        "binary_collapse_kappa": payload["exercises"]["round1_initial_18"][
            "binary_collapse_kappa"
        ],
        "note": payload["exercises"]["round1_initial_18"]["note"],
    }
    PUBLIC_SUMMARY_JSON.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    p = write_public_outputs()
    print(
        json.dumps(
            {
                "all_lock_checks_pass": p["all_lock_checks_pass"],
                "binary_invalid": p["exercises"]["binary_validation"][
                    "cohen_kappa_bootstrap_n_invalid"
                ],
                "binary_valid": p["exercises"]["binary_validation"][
                    "cohen_kappa_bootstrap_n_valid"
                ],
            },
            indent=2,
        )
    )
