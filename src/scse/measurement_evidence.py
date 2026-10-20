"""Phase 8B: measurement-paper evidence lock from preserved independent labels.

Recomputes agreement, bootstrap CIs, kappa_max, bias diagnostics.
Does not create XIV outcomes or request new human coding.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Sequence

import pandas as pd

from scse.calibration_metrics import (
    ES_TO_EN,
    _cohens_kappa,
    cohen_kappa_3way,
    cohen_kappa_explicit_vs_rest,
    krippendorff_alpha_nominal,
    normalize_label,
    raw_agreement,
    summarize_round1,
)
from scse.paths import DATA_PRIVATE, PROJECT_ROOT
from scse.question_side import code_question_side

BOOTSTRAP_SEED = 20261020
BOOTSTRAP_N = 5000

OUT_DIR = DATA_PRIVATE / "measurement_paper"
REPORT = PROJECT_ROOT / "_internal" / "reports" / "MEASUREMENT_PAPER_EVIDENCE_LOCK.md"

ORDINAL_3 = {
    "ausencia de respuesta": 0,
    "non_reply": 0,
    "respuesta parcial o intermedia": 1,
    "intermediate_reply": 1,
    "respuesta explícita": 2,
    "explicit_reply": 2,
}
ORDINAL_BIN = {
    "direct_resolution_no": 0,
    "direct_resolution_yes": 1,
}

WORD_RE = re.compile(r"\S+")


def word_count(text: object) -> int:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return 0
    return len(WORD_RE.findall(str(text)))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# kappa_max / bias diagnostics
# ---------------------------------------------------------------------------


def max_agreement_given_marginals(
    marg_a: Sequence[int], marg_b: Sequence[int]
) -> int:
    """Maximum number of agreements given two label-count vectors (same order)."""
    if len(marg_a) != len(marg_b):
        raise ValueError("marginal vectors must align")
    if sum(marg_a) != sum(marg_b):
        raise ValueError("marginal totals must match")
    return int(sum(min(a, b) for a, b in zip(marg_a, marg_b)))


def kappa_max_from_labels(
    a: Sequence[str], b: Sequence[str], labels: Sequence[str]
) -> dict:
    """Cohen κ upper bound given observed marginals (categorical)."""
    n = len(a)
    if n == 0 or len(a) != len(b):
        raise ValueError("aligned non-empty sequences required")
    ca = Counter(a)
    cb = Counter(b)
    marg_a = [ca.get(lab, 0) for lab in labels]
    marg_b = [cb.get(lab, 0) for lab in labels]
    max_agree = max_agreement_given_marginals(marg_a, marg_b)
    po_max = max_agree / n
    pe = sum((ca.get(lab, 0) / n) * (cb.get(lab, 0) / n) for lab in labels)
    if pe == 1:
        k_max = 1.0
    else:
        k_max = (po_max - pe) / (1 - pe)
    po_obs = sum(x == y for x, y in zip(a, b)) / n
    k_obs = _cohens_kappa(list(a), list(b), labels)
    return {
        "n": n,
        "labels": list(labels),
        "marginal_a": dict(zip(labels, marg_a)),
        "marginal_b": dict(zip(labels, marg_b)),
        "max_agreements": max_agree,
        "po_max": po_max,
        "po_observed": po_obs,
        "pe": pe,
        "kappa_max": k_max,
        "kappa_observed": k_obs,
        "observed_equals_kappa_max": abs(k_obs - k_max) < 1e-12
        and abs(po_obs - po_max) < 1e-12,
    }


def binary_bias_prevalence_pabak(a: Sequence[str], b: Sequence[str], *, pos: str) -> dict:
    """Byrt, Bishop & Carlin (1993)-style indices for a binary coding.

    a, b are label sequences; ``pos`` is the positive category name.
    Prevalence index = (f1 - g1)/n where f1 = both pos, g1 = both neg
      (equivalently (n_pos_a + n_pos_b)/n - 1 in some forms — we use
      standard BI/PI from the 2x2 table).

    Let a=annotator1, b=annotator2; cells:
      a11 both pos, a00 both neg, a10 a=pos b=neg, a01 a=neg b=pos.
    Bias index BI = (a10 - a01) / n
    Prevalence index PI = (a11 - a00) / n
    PABAK = 2 * po - 1
    """
    n = len(a)
    a11 = sum(x == pos and y == pos for x, y in zip(a, b))
    a00 = sum(x != pos and y != pos for x, y in zip(a, b))
    a10 = sum(x == pos and y != pos for x, y in zip(a, b))
    a01 = sum(x != pos and y == pos for x, y in zip(a, b))
    po = (a11 + a00) / n
    return {
        "n": n,
        "a11": a11,
        "a00": a00,
        "a10": a10,
        "a01": a01,
        "po": po,
        "bias_index": (a10 - a01) / n,
        "prevalence_index": (a11 - a00) / n,
        "pabak": 2 * po - 1,
        "definition": (
            "BI=(a10-a01)/n; PI=(a11-a00)/n; PABAK=2*po-1 "
            "(Byrt, Bishop & Carlin 1993 style; diagnostic only)"
        ),
    }


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------


def bootstrap_metric_ci(
    a: Sequence[str],
    b: Sequence[str],
    metric_fn,
    *,
    n_resamples: int = BOOTSTRAP_N,
    seed: int = BOOTSTRAP_SEED,
    alpha: float = 0.05,
) -> dict:
    """Percentile bootstrap CI for a paired metric.

    Degenerate samples (exceptions or NaN) are counted as invalid and excluded
    from the percentile; counts are reported transparently.
    """
    n = len(a)
    aa = list(a)
    bb = list(b)
    point = metric_fn(aa, bb)
    rng = random.Random(seed)
    vals: list[float] = []
    invalid = 0
    for _ in range(n_resamples):
        idx = [rng.randrange(n) for _ in range(n)]
        sa = [aa[i] for i in idx]
        sb = [bb[i] for i in idx]
        try:
            v = float(metric_fn(sa, sb))
            if v != v:  # NaN
                invalid += 1
                continue
            vals.append(v)
        except Exception:
            invalid += 1
    if not vals:
        return {
            "point": point,
            "ci_low": None,
            "ci_high": None,
            "n_resamples": n_resamples,
            "n_valid": 0,
            "n_invalid": invalid,
            "seed": seed,
            "method": "percentile",
            "alpha": alpha,
        }
    vals.sort()
    lo_i = int((alpha / 2) * len(vals))
    hi_i = int((1 - alpha / 2) * len(vals)) - 1
    hi_i = max(0, min(hi_i, len(vals) - 1))
    return {
        "point": point,
        "ci_low": vals[lo_i],
        "ci_high": vals[hi_i],
        "n_resamples": n_resamples,
        "n_valid": len(vals),
        "n_invalid": invalid,
        "seed": seed,
        "method": "percentile",
        "alpha": alpha,
    }


def _fmt_ci(d: dict) -> str:
    if d["ci_low"] is None:
        return f"{d['point']:.3f} [CI unavailable; valid={d['n_valid']}]"
    return f"{d['point']:.3f} [{d['ci_low']:.3f}, {d['ci_high']:.3f}]"


# ---------------------------------------------------------------------------
# Load 67-unit table
# ---------------------------------------------------------------------------


def _direction_3(d_lab: str, j_lab: str) -> str:
    if d_lab == j_lab:
        return "agree"
    od, oj = ORDINAL_3[d_lab], ORDINAL_3[j_lab]
    if oj > od:
        return "jose_jaime_more_responsive"
    if od > oj:
        return "daniel_more_responsive"
    return "non_ordinal"


def _direction_bin(d_lab: str, j_lab: str) -> str:
    if d_lab == j_lab:
        return "agree"
    if ORDINAL_BIN[j_lab] > ORDINAL_BIN[d_lab]:
        return "jose_jaime_more_responsive"
    if ORDINAL_BIN[d_lab] > ORDINAL_BIN[j_lab]:
        return "daniel_more_responsive"
    return "non_ordinal"


def load_development() -> pd.DataFrame:
    comp = pd.read_csv(
        PROJECT_ROOT
        / "_internal"
        / "development"
        / "solutions"
        / "development_solutions_comparison.csv"
    )
    aud = pd.read_csv(
        DATA_PRIVATE / "development" / "out_of_pool" / "DEVELOPMENT_SET_AUDIT.csv"
    )
    pkt = pd.read_csv(
        DATA_PRIVATE / "development" / "out_of_pool" / "DEVELOPMENT_PACKET_BLINDED.csv"
    )
    m = comp.merge(aud, on=["unit_id"], how="left", suffixes=("", "_aud"))
    m = m.merge(pkt, on=["unit_id"], how="left", suffixes=("", "_pkt"))
    rows = []
    for _, r in m.iterrows():
        d_es = r["daniel_reply_status_es"]
        j_es = r["jose_reply_status_es"]
        side = code_question_side(r.get("registered_question"), r.get("Q1"))
        q1 = r.get("Q1")
        r1 = r.get("R1")
        rows.append(
            {
                "exercise": "development",
                "instrument": "reply_status_pre_v0.3_development",
                "case_no": int(r["case_no"]),
                "unit_id": r["unit_id"],
                "legislature": r.get("legislature"),
                "date": r.get("date"),
                "session_id": r.get("session_id"),
                "questioner_who": r.get("questioner_who"),
                "question_form": side["question_form"],
                "question_topic": side["question_topic"],
                "label_system": "three_category",
                "daniel_label": d_es,
                "jose_jaime_label": j_es,
                "daniel_dudoso": r.get("daniel_borderline"),
                "jose_jaime_dudoso": r.get("jose_borderline"),
                "daniel_comment": r.get("daniel_notes")
                if pd.notna(r.get("daniel_notes"))
                else None,
                "jose_jaime_comment": r.get("jose_notes")
                if pd.notna(r.get("jose_notes"))
                else None,
                "exact_agreement": bool(d_es == j_es),
                "disagreement_direction": _direction_3(d_es, j_es),
                "q1_word_count": word_count(q1),
                "r1_word_count": word_count(r1),
                "jose_jaime_admin_clarification": False,
                "round1_pair_usable_before_jj_adjust": None,
            }
        )
    return pd.DataFrame(rows)


def load_round1() -> pd.DataFrame:
    codes = pd.read_csv(
        DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_CODES.csv"
    )
    aud = pd.read_csv(
        DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_AUDIT.csv"
    )
    pkt = pd.read_csv(
        DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_PACKET_BLINDED.csv"
    )
    ret = json.loads(
        (
            DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_RETURNS.json"
        ).read_text(encoding="utf-8")
    )
    clarified = {c["case_no"] for c in ret["jose_jaime_adjustment"]["clarifications"]}
    m = codes.merge(aud, on=["case_no", "unit_id"], how="left")
    m = m.merge(pkt, on=["case_no", "unit_id"], how="left", suffixes=("", "_pkt"))
    rows = []
    for _, r in m.iterrows():
        d_es = r["daniel_reply_status"]
        j_es = r["jose_jaime_reply_status"]
        side = code_question_side(r["registered_question"], r["Q1"])
        cno = int(r["case_no"])
        rows.append(
            {
                "exercise": "calibration_round1",
                "instrument": "reply_status_v0.3",
                "case_no": cno,
                "unit_id": r["unit_id"],
                "legislature": r.get("legislature"),
                "date": r.get("date"),
                "session_id": r.get("session_id"),
                "questioner_who": r.get("questioner_who")
                if "questioner_who" in m.columns
                else None,
                "question_form": side["question_form"],
                "question_topic": side["question_topic"],
                "label_system": "three_category",
                "daniel_label": d_es,
                "jose_jaime_label": j_es,
                "daniel_dudoso": r.get("daniel_dudoso"),
                "jose_jaime_dudoso": r.get("jose_jaime_dudoso"),
                "daniel_comment": r.get("daniel_observaciones")
                if pd.notna(r.get("daniel_observaciones"))
                else None,
                "jose_jaime_comment": r.get("jose_jaime_observaciones")
                if pd.notna(r.get("jose_jaime_observaciones"))
                else None,
                "exact_agreement": bool(d_es == j_es),
                "disagreement_direction": _direction_3(d_es, j_es),
                "q1_word_count": word_count(r["Q1"]),
                "r1_word_count": word_count(r["R1"]),
                "jose_jaime_admin_clarification": cno in clarified,
                "round1_pair_usable_before_jj_adjust": cno not in clarified,
            }
        )
    return pd.DataFrame(rows)


def load_round2() -> pd.DataFrame:
    codes = pd.read_csv(
        DATA_PRIVATE / "calibration" / "round2" / "CALIBRATION_ROUND2_CODES.csv"
    )
    aud = pd.read_csv(
        DATA_PRIVATE / "calibration" / "round2" / "CALIBRATION_ROUND2_AUDIT.csv"
    )
    pkt = pd.read_csv(
        DATA_PRIVATE / "calibration" / "round2" / "CALIBRATION_ROUND2_PACKET_BLINDED.csv"
    )
    m = codes.merge(aud, on=["case_no", "unit_id"], how="left")
    m = m.merge(pkt, on=["case_no", "unit_id"], how="left", suffixes=("", "_pkt"))
    rows = []
    for _, r in m.iterrows():
        d_es = r["daniel_reply_status"]
        j_es = r["jose_jaime_reply_status"]
        side = code_question_side(r["registered_question"], r["Q1"])
        rows.append(
            {
                "exercise": "calibration_round2",
                "instrument": "reply_status_v0.3",
                "case_no": int(r["case_no"]),
                "unit_id": r["unit_id"],
                "legislature": r.get("legislature"),
                "date": r.get("date"),
                "session_id": r.get("session_id"),
                "questioner_who": r.get("questioner_who"),
                "question_form": side["question_form"],
                "question_topic": side["question_topic"],
                "label_system": "three_category",
                "daniel_label": d_es,
                "jose_jaime_label": j_es,
                "daniel_dudoso": r.get("daniel_dudoso"),
                "jose_jaime_dudoso": r.get("jose_jaime_dudoso"),
                "daniel_comment": r.get("daniel_observaciones")
                if pd.notna(r.get("daniel_observaciones"))
                else None,
                "jose_jaime_comment": r.get("jose_jaime_observaciones")
                if pd.notna(r.get("jose_jaime_observaciones"))
                else None,
                "exact_agreement": bool(d_es == j_es),
                "disagreement_direction": _direction_3(d_es, j_es),
                "q1_word_count": word_count(r["Q1"]),
                "r1_word_count": word_count(r["R1"]),
                "jose_jaime_admin_clarification": False,
                "round1_pair_usable_before_jj_adjust": None,
            }
        )
    return pd.DataFrame(rows)


def load_binary() -> pd.DataFrame:
    codes = pd.read_csv(
        DATA_PRIVATE / "validation" / "binary_v1" / "BINARY_VALIDATION_CODES.csv"
    )
    aud = pd.read_csv(
        DATA_PRIVATE / "validation" / "binary_v1" / "BINARY_VALIDATION_N12_AUDIT.csv"
    )
    pkt = pd.read_csv(
        DATA_PRIVATE
        / "validation"
        / "binary_v1"
        / "BINARY_VALIDATION_N12_PACKET_BLINDED.csv"
    )
    m = codes.merge(aud, on=["case_no", "unit_id"], how="left")
    m = m.merge(pkt, on=["case_no", "unit_id"], how="left", suffixes=("", "_pkt"))
    rows = []
    for _, r in m.iterrows():
        d = r["daniel_direct_resolution"]
        j = r["jose_jaime_direct_resolution"]
        rows.append(
            {
                "exercise": "binary_validation",
                "instrument": "direct_resolution_v1.0-validation",
                "case_no": int(r["case_no"]),
                "unit_id": r["unit_id"],
                "legislature": r.get("legislature"),
                "date": r.get("date"),
                "session_id": r.get("session_id"),
                "questioner_who": r.get("questioner_who"),
                "question_form": r.get("question_form"),
                "question_topic": r.get("question_topic"),
                "label_system": "binary_direct_resolution",
                "daniel_label": d,
                "jose_jaime_label": j,
                "daniel_dudoso": r.get("daniel_dudoso"),
                "jose_jaime_dudoso": r.get("jose_jaime_dudoso"),
                "daniel_comment": r.get("daniel_observaciones")
                if pd.notna(r.get("daniel_observaciones"))
                else None,
                "jose_jaime_comment": r.get("jose_jaime_observaciones")
                if pd.notna(r.get("jose_jaime_observaciones"))
                else None,
                "exact_agreement": bool(d == j),
                "disagreement_direction": _direction_bin(d, j),
                "q1_word_count": word_count(r["Q1"]),
                "r1_word_count": word_count(r["R1"]),
                "jose_jaime_admin_clarification": False,
                "round1_pair_usable_before_jj_adjust": None,
            }
        )
    return pd.DataFrame(rows)


def build_human_evidence_67() -> pd.DataFrame:
    parts = [load_development(), load_round1(), load_round2(), load_binary()]
    df = pd.concat(parts, ignore_index=True)
    if len(df) != 67:
        raise RuntimeError(f"expected 67 rows, got {len(df)}")
    counts = df["exercise"].value_counts().to_dict()
    expect = {
        "development": 15,
        "calibration_round1": 20,
        "calibration_round2": 20,
        "binary_validation": 12,
    }
    for k, v in expect.items():
        if counts.get(k) != v:
            raise RuntimeError(f"{k}: expected {v}, got {counts.get(k)}")
    return df


# ---------------------------------------------------------------------------
# Metrics bundles
# ---------------------------------------------------------------------------


def metrics_3way(a_es: list[str], b_es: list[str]) -> dict:
    from scse.calibration_metrics import CATEGORIES

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
    km = kappa_max_from_labels(a_en, b_en, CATEGORIES)
    km_bin = kappa_max_from_labels(ba, bb, ("explicit", "non_explicit"))
    bias = binary_bias_prevalence_pabak(ba, bb, pos="explicit")
    return {
        "n": s["n"],
        "raw_agreement": s["raw_agreement"],
        "cohen_kappa_3way": s["cohen_kappa_3way"],
        "cohen_kappa_3way_ci": k3,
        "krippendorff_alpha_nominal": s["krippendorff_alpha_nominal"],
        "krippendorff_alpha_ci": al,
        "binary_explicit_raw_agreement": s["binary_explicit_raw_agreement"],
        "cohen_kappa_explicit_vs_rest": s["cohen_kappa_explicit_vs_rest"],
        "cohen_kappa_explicit_vs_rest_ci": kb,
        "kappa_max_3way": km,
        "kappa_max_binary_explicit": km_bin,
        "binary_bias_diagnostics": bias,
        "confusion_matrix_3way": s["confusion_matrix_3way"],
    }


def metrics_binary_dr(a: list[str], b: list[str]) -> dict:
    labels = ["direct_resolution_yes", "direct_resolution_no"]
    n = len(a)
    raw = sum(x == y for x, y in zip(a, b)) / n
    k = _cohens_kappa(a, b, labels)
    k_ci = bootstrap_metric_ci(a, b, lambda x, y: _cohens_kappa(x, y, labels))
    km = kappa_max_from_labels(a, b, labels)
    bias = binary_bias_prevalence_pabak(a, b, pos="direct_resolution_yes")
    return {
        "n": n,
        "raw_agreement": raw,
        "n_agree": sum(x == y for x, y in zip(a, b)),
        "cohen_kappa": k,
        "cohen_kappa_ci": k_ci,
        "kappa_max": km,
        "bias_diagnostics": bias,
        "daniel_yes": sum(x == "direct_resolution_yes" for x in a),
        "jose_jaime_yes": sum(x == "direct_resolution_yes" for x in b),
        "observed_equals_kappa_max": km["observed_equals_kappa_max"],
    }


def direction_summary(df: pd.DataFrame) -> dict:
    sub = df[df["disagreement_direction"] != "agree"]
    return {
        "n_disagree": int(len(sub)),
        "daniel_more_responsive": int(
            (sub["disagreement_direction"] == "daniel_more_responsive").sum()
        ),
        "jose_jaime_more_responsive": int(
            (sub["disagreement_direction"] == "jose_jaime_more_responsive").sum()
        ),
        "other": int(
            (~sub["disagreement_direction"].isin(
                ["daniel_more_responsive", "jose_jaime_more_responsive"]
            )).sum()
        ),
    }


def xiv_composition() -> dict:
    m = pd.read_csv(DATA_PRIVATE / "main" / "MAIN_FRAME_CORPUS_FULL.csv")
    q1col = "q1_text" if "q1_text" in m.columns else "Q1"
    r1col = "r1_text" if "r1_text" in m.columns else "R1"
    return {
        "n": len(m),
        "legislature_counts": m["legislature"].value_counts().to_dict()
        if "legislature" in m.columns
        else {"XIV": len(m)},
        "question_form_counts": m["question_form"].value_counts(dropna=False).to_dict()
        if "question_form" in m.columns
        else {},
        "question_topic_counts": m["question_topic"].value_counts(dropna=False).to_dict()
        if "question_topic" in m.columns
        else {},
        "q1_word_median": float(m[q1col].map(word_count).median()),
        "q1_word_mean": float(m[q1col].map(word_count).mean()),
        "r1_word_median": float(m[r1col].map(word_count).median()),
        "r1_word_mean": float(m[r1col].map(word_count).mean()),
    }


def oop_composition(df: pd.DataFrame) -> dict:
    out = {}
    for ex, g in df.groupby("exercise"):
        out[ex] = {
            "n": len(g),
            "legislature_counts": g["legislature"].value_counts(dropna=False).to_dict(),
            "question_form_counts": g["question_form"].value_counts(dropna=False).to_dict(),
            "question_topic_counts": g["question_topic"].value_counts(dropna=False).to_dict(),
            "q1_word_median": float(g["q1_word_count"].median()),
            "q1_word_mean": float(g["q1_word_count"].mean()),
            "r1_word_median": float(g["r1_word_count"].median()),
            "r1_word_mean": float(g["r1_word_count"].mean()),
            "max_questioner_share": int(g["questioner_who"].value_counts().iloc[0])
            if g["questioner_who"].notna().any()
            else None,
        }
    return out


def disagreement_inventory(df: pd.DataFrame) -> list[dict]:
    rows = []
    for _, r in df[~df["exact_agreement"]].iterrows():
        rows.append(
            {
                "exercise": r["exercise"],
                "case_no": int(r["case_no"]),
                "unit_id": r["unit_id"],
                "daniel_label": r["daniel_label"],
                "jose_jaime_label": r["jose_jaime_label"],
                "question_form": r["question_form"],
                "question_topic": r["question_topic"],
                "direction": r["disagreement_direction"],
            }
        )
    return rows


def provisional_mechanism_taxonomy() -> list[dict]:
    """Lead/analytic qualitative coding from existing diagnostics only."""
    return [
        {
            "exercise": "binary_validation",
            "case_no": 1,
            "mechanism": "object_displacement",
            "note": "Evaluation of unemployment/government record vs situation of young people",
            "source": "Claude review §3; Phase 8A",
            "coding_type": "qualitative_analytic_not_reliability",
        },
        {
            "exercise": "binary_validation",
            "case_no": 4,
            "mechanism": "intent_for_outcome_substitution",
            "note": "Reform objective asserted; guarantee of equal opportunity not affirmed",
            "source": "Claude review §3; Phase 8A",
            "coding_type": "qualitative_analytic_not_reliability",
        },
        {
            "exercise": "binary_validation",
            "case_no": 7,
            "mechanism": "conditional_reframing",
            "note": "Respect election results vs respect results if independentism wins",
            "source": "Claude review §3; Phase 8A",
            "coding_type": "qualitative_analytic_not_reliability",
        },
        {
            "exercise": "binary_validation",
            "case_no": 11,
            "mechanism": "object_displacement",
            "note": "Generic crisis/growth narrative vs impact of policies on household spending",
            "source": "Claude review §3; Phase 8A",
            "coding_type": "qualitative_analytic_not_reliability",
        },
        {
            "exercise": "calibration_round2",
            "case_no": 10,
            "mechanism": "topical_relevance_vs_target_resolution",
            "note": "Extreme explícita↔ausencia; justification narrative vs formal slot",
            "source": "ROUND2_MEASUREMENT_FAILURE_DIAGNOSTIC",
            "coding_type": "qualitative_analytic_not_reliability",
        },
        {
            "exercise": "calibration_round2",
            "case_no": 14,
            "mechanism": "premise_handling",
            "note": "Dialogue/refusal narrative vs prospective solution stance",
            "source": "ROUND2_MEASUREMENT_FAILURE_DIAGNOSTIC",
            "coding_type": "qualitative_analytic_not_reliability",
        },
        {
            "exercise": "calibration_round2",
            "case_no": 18,
            "mechanism": "inferred_vs_overt_stance",
            "note": "Procedural dismissal vs required evaluative opinion",
            "source": "ROUND2_MEASUREMENT_FAILURE_DIAGNOSTIC",
            "coding_type": "qualitative_analytic_not_reliability",
        },
        {
            "exercise": "multiple",
            "case_no": None,
            "mechanism": "multipart_demand_ambiguity",
            "note": "Appears in development/R2 when co-equal asks compete; not forced on all 22",
            "source": "codebook v0.3 §7; Phase 6C",
            "coding_type": "qualitative_analytic_not_reliability",
        },
    ]


def run_evidence_lock() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = build_human_evidence_67()
    csv_path = OUT_DIR / "HUMAN_EVIDENCE_67.csv"
    df.to_csv(csv_path, index=False)

    # Development
    dev = df[df.exercise == "development"]
    m_dev = metrics_3way(list(dev.daniel_label), list(dev.jose_jaime_label))

    # Round 1 final 20
    r1 = df[df.exercise == "calibration_round1"]
    m_r1_20 = metrics_3way(list(r1.daniel_label), list(r1.jose_jaime_label))
    # Round 1 initial 18 (exclude administratively clarified cases)
    r1_18 = r1[r1["round1_pair_usable_before_jj_adjust"] == True]  # noqa: E712
    m_r1_18 = metrics_3way(list(r1_18.daniel_label), list(r1_18.jose_jaime_label))

    # Round 2
    r2 = df[df.exercise == "calibration_round2"]
    m_r2 = metrics_3way(list(r2.daniel_label), list(r2.jose_jaime_label))

    # Pooled R1+R2
    pool = pd.concat([r1, r2], ignore_index=True)
    m_pool = metrics_3way(list(pool.daniel_label), list(pool.jose_jaime_label))

    # Binary
    bv = df[df.exercise == "binary_validation"]
    m_bin = metrics_binary_dr(list(bv.daniel_label), list(bv.jose_jaime_label))

    directions = {
        "development": direction_summary(dev),
        "calibration_round1": direction_summary(r1),
        "calibration_round2": direction_summary(r2),
        "binary_validation": direction_summary(bv),
        "combined_all_disagreements": direction_summary(df),
    }
    # Stable trait test
    stable_claim_supported = (
        directions["development"]["daniel_more_responsive"]
        > directions["development"]["jose_jaime_more_responsive"]
        and directions["calibration_round1"]["daniel_more_responsive"]
        > directions["calibration_round1"]["jose_jaime_more_responsive"]
        and directions["calibration_round2"]["daniel_more_responsive"]
        > directions["calibration_round2"]["jose_jaime_more_responsive"]
        and directions["binary_validation"]["daniel_more_responsive"]
        > directions["binary_validation"]["jose_jaime_more_responsive"]
    ) or (
        directions["development"]["jose_jaime_more_responsive"]
        > directions["development"]["daniel_more_responsive"]
        and directions["calibration_round1"]["jose_jaime_more_responsive"]
        > directions["calibration_round1"]["daniel_more_responsive"]
        and directions["calibration_round2"]["jose_jaime_more_responsive"]
        > directions["calibration_round2"]["daniel_more_responsive"]
        and directions["binary_validation"]["jose_jaime_more_responsive"]
        > directions["binary_validation"]["daniel_more_responsive"]
    )

    inv = disagreement_inventory(df)
    xiv_n = len(pd.read_csv(DATA_PRIVATE / "main" / "MAIN_FRAME_CORPUS_FULL.csv"))

    payload = {
        "phase": "8B",
        "recorded_on": date.today().isoformat(),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "xiv_frame_n_verified": xiv_n,
        "human_evidence_n": 67,
        "exercise_counts": df["exercise"].value_counts().to_dict(),
        "bootstrap": {
            "n_resamples": BOOTSTRAP_N,
            "seed": BOOTSTRAP_SEED,
            "method": "percentile_95",
            "note": "Invalid/degenerate resamples counted and excluded from percentile",
        },
        "development": m_dev,
        "round1_initial_18": {
            **m_r1_18,
            "note": (
                "Excludes cases 5 and 10 where Jose Jaime marks were "
                "administratively clarified later (missing / multiple marks). "
                "Not adjudication; Daniel values not revealed."
            ),
            "excluded_case_nos": [5, 10],
        },
        "round1_final_20": {
            **m_r1_20,
            "jose_jaime_admin_clarification_cases": [5, 10],
        },
        "round2": m_r2,
        "pooled_r1_r2": m_pool,
        "binary_validation": m_bin,
        "directions": directions,
        "stable_coder_severity_trait_supported": stable_claim_supported,
        "disagreement_inventory_n": len(inv),
        "disagreement_inventory": inv,
        "oop_composition": oop_composition(df),
        "xiv_composition": xiv_composition(),
        "provisional_mechanism_taxonomy": provisional_mechanism_taxonomy(),
        "human_evidence_csv": str(csv_path.relative_to(PROJECT_ROOT)),
        "human_evidence_csv_sha256": sha256_file(csv_path),
        "no_xiv_reply_labels": True,
        "no_new_human_coding": True,
        "no_ai_reply_labels": True,
        "manuscript_not_rewritten": True,
    }

    json_path = OUT_DIR / "MEASUREMENT_PAPER_EVIDENCE_LOCK.json"
    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    write_report(payload, csv_path)
    return payload


def write_report(p: dict, csv_path: Path) -> None:
    def ci(block, key):
        return _fmt_ci(block[key])

    lines = [
        "# Measurement-paper evidence lock (Phase 8B)",
        "",
        f"**Recorded:** {p['recorded_on']}",
        f"**Verified XIV pre-outcome frame N:** {p['xiv_frame_n_verified']}",
        f"**Human evidence N:** {p['human_evidence_n']}",
        "",
        "Recomputed from preserved **original independent** labels. "
        "Joint/adjudicated decisions not used as outcomes.",
        "",
        f"Bootstrap: {p['bootstrap']['n_resamples']} resamples; seed "
        f"`{p['bootstrap']['seed']}`; percentile 95% CIs; invalid draws counted.",
        "",
        "## Exercise counts",
        "",
        f"- Development: {p['exercise_counts'].get('development')}",
        f"- Round 1: {p['exercise_counts'].get('calibration_round1')}",
        f"- Round 2: {p['exercise_counts'].get('calibration_round2')}",
        f"- Binary validation: {p['exercise_counts'].get('binary_validation')}",
        "",
        f"Table: `{csv_path.relative_to(PROJECT_ROOT)}`",
        f"SHA-256: `{p['human_evidence_csv_sha256']}`",
        "",
        "## Development (n=15)",
        "",
        f"- Raw agreement: {p['development']['raw_agreement']:.3f}",
        f"- Cohen κ 3-way: {ci(p['development'], 'cohen_kappa_3way_ci')}",
        f"- Krippendorff α: {ci(p['development'], 'krippendorff_alpha_ci')}",
        f"- Binary explicit κ: {ci(p['development'], 'cohen_kappa_explicit_vs_rest_ci')}",
        "",
        "## Round 1 — initial 18 usable pairs",
        "",
        p["round1_initial_18"]["note"],
        "",
        f"- Raw agreement: {p['round1_initial_18']['raw_agreement']:.3f}",
        f"- Cohen κ 3-way: {ci(p['round1_initial_18'], 'cohen_kappa_3way_ci')}",
        f"- Krippendorff α: {ci(p['round1_initial_18'], 'krippendorff_alpha_ci')}",
        f"- Binary explicit κ: {ci(p['round1_initial_18'], 'cohen_kappa_explicit_vs_rest_ci')}",
        "",
        "## Round 1 — final 20 (after JJ administrative clarification on cases 5, 10)",
        "",
        f"- Raw agreement: {p['round1_final_20']['raw_agreement']:.3f}",
        f"- Cohen κ 3-way: {ci(p['round1_final_20'], 'cohen_kappa_3way_ci')}",
        f"- Krippendorff α: {ci(p['round1_final_20'], 'krippendorff_alpha_ci')}",
        f"- Binary explicit κ: {ci(p['round1_final_20'], 'cohen_kappa_explicit_vs_rest_ci')}",
        "",
        "## Round 2 (n=20)",
        "",
        f"- Raw agreement: {p['round2']['raw_agreement']:.3f}",
        f"- Cohen κ 3-way: {ci(p['round2'], 'cohen_kappa_3way_ci')}",
        f"- Krippendorff α: {ci(p['round2'], 'krippendorff_alpha_ci')}",
        f"- Binary explicit κ: {ci(p['round2'], 'cohen_kappa_explicit_vs_rest_ci')}",
        "",
        "## Pooled Round 1 + Round 2 (n=40; same v0.3 instrument)",
        "",
        f"- Raw agreement: {p['pooled_r1_r2']['raw_agreement']:.3f}",
        f"- Cohen κ 3-way: {ci(p['pooled_r1_r2'], 'cohen_kappa_3way_ci')}",
        f"- Krippendorff α: {ci(p['pooled_r1_r2'], 'krippendorff_alpha_ci')}",
        f"- Binary explicit κ: {ci(p['pooled_r1_r2'], 'cohen_kappa_explicit_vs_rest_ci')}",
        "",
        "## Binary redesigned validation (n=12)",
        "",
        f"- Raw agreement: {p['binary_validation']['n_agree']}/12 = "
        f"{p['binary_validation']['raw_agreement']:.3f}",
        f"- Cohen κ: {ci(p['binary_validation'], 'cohen_kappa_ci')}",
        f"- Daniel YES: {p['binary_validation']['daniel_yes']}/12",
        f"- Jose Jaime YES: {p['binary_validation']['jose_jaime_yes']}/12",
        f"- κ_max given marginals: {p['binary_validation']['kappa_max']['kappa_max']:.6f}",
        f"- Observed κ equals κ_max: "
        f"**{'YES' if p['binary_validation']['observed_equals_kappa_max'] else 'NO'}**",
        f"- Bias index: {p['binary_validation']['bias_diagnostics']['bias_index']:.3f}",
        f"- Prevalence index: "
        f"{p['binary_validation']['bias_diagnostics']['prevalence_index']:.3f}",
        f"- PABAK: {p['binary_validation']['bias_diagnostics']['pabak']:.3f} "
        f"(diagnostic only; does not pass the locked gate)",
        "",
        "## Disagreement direction (independent labels only)",
        "",
    ]
    for ex, d in p["directions"].items():
        if ex == "combined_all_disagreements":
            continue
        lines.append(
            f"- **{ex}**: Daniel more-responsive {d['daniel_more_responsive']}; "
            f"Jose Jaime more-responsive {d['jose_jaime_more_responsive']}; "
            f"n_disagree={d['n_disagree']}"
        )
    comb = p["directions"]["combined_all_disagreements"]
    lines += [
        "",
        f"Combined disagreements: Daniel-more {comb['daniel_more_responsive']}; "
        f"JJ-more {comb['jose_jaime_more_responsive']}; total {comb['n_disagree']}",
        "",
        f"**Stable coder-severity trait supported: "
        f"{'YES' if p['stable_coder_severity_trait_supported'] else 'NO'}**",
        "",
        "Supersedes any project-state wording that claimed a stable "
        "Daniel-stricter / Jose-Jaime-more-permissive trait.",
        "",
        f"## Independent disagreements: {p['disagreement_inventory_n']}",
        "",
        "## OOP vs XIV composition (non-outcome)",
        "",
        f"XIV N={p['xiv_composition']['n']}; "
        f"Q1 median words={p['xiv_composition']['q1_word_median']:.0f}; "
        f"R1 median words={p['xiv_composition']['r1_word_median']:.0f}; "
        f"forms={p['xiv_composition']['question_form_counts']}",
        "",
    ]
    for ex, c in p["oop_composition"].items():
        lines.append(
            f"- {ex}: n={c['n']}; Q1 med={c['q1_word_median']:.0f}; "
            f"R1 med={c['r1_word_median']:.0f}; legis={c['legislature_counts']}; "
            f"forms={c['question_form_counts']}"
        )
    lines += [
        "",
        "OOP exercises are shorter and differently composed than the XIV target "
        "(longer Q1/R1; different form mix). Representativeness for transfer is limited.",
        "",
        "## Project status (prospective)",
        "",
        "- **NO MORE HUMAN CODING PLANNED**",
        "- **NO XIV RESPONSIVENESS OUTCOME** under failed instruments",
        "- Intended publication route: **MEASUREMENT / METHODOLOGICAL PAPER**",
        "- Feature-based rescue: **not planned** as next action",
        "",
        "## Compliance",
        "",
        "- XIV reply labels created: NO",
        "- New human coding requested: NO",
        "- AI reply labels created: NO",
        "- Manuscript substantially rewritten: NO",
        "",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> dict:
    p = run_evidence_lock()
    # slim stdout
    return {
        "xiv_n": p["xiv_frame_n_verified"],
        "n": p["human_evidence_n"],
        "pooled_kappa": p["pooled_r1_r2"]["cohen_kappa_3way"],
        "binary_kappa": p["binary_validation"]["cohen_kappa"],
        "binary_kappa_max": p["binary_validation"]["kappa_max"]["kappa_max"],
        "equals_max": p["binary_validation"]["observed_equals_kappa_max"],
        "stable_trait": p["stable_coder_severity_trait_supported"],
        "n_disagree": p["disagreement_inventory_n"],
        "csv": p["human_evidence_csv"],
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
