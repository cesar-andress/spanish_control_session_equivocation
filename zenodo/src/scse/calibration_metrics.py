"""Calibration Round agreement diagnostics (prepare only; no labels yet).

Call these functions after both independent Round-1 returns are archived.
Do not interpret Round 1 as final validation.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Sequence

CATEGORIES = ("explicit_reply", "intermediate_reply", "non_reply")
ES_TO_EN = {
    "respuesta explícita": "explicit_reply",
    "respuesta parcial o intermedia": "intermediate_reply",
    "ausencia de respuesta": "non_reply",
}


def normalize_label(value: str) -> str:
    v = (value or "").strip().lower()
    if v in CATEGORIES:
        return v
    if v in ES_TO_EN:
        return ES_TO_EN[v]
    raise ValueError(f"Unknown reply_status label: {value!r}")


def raw_agreement(a: Sequence[str], b: Sequence[str]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("label sequences must be non-empty and aligned")
    aa = [normalize_label(x) for x in a]
    bb = [normalize_label(x) for x in b]
    return sum(x == y for x, y in zip(aa, bb)) / len(aa)


def confusion_matrix_3way(a: Sequence[str], b: Sequence[str]) -> dict[str, dict[str, int]]:
    aa = [normalize_label(x) for x in a]
    bb = [normalize_label(x) for x in b]
    mat = {r: {c: 0 for c in CATEGORIES} for r in CATEGORIES}
    for x, y in zip(aa, bb):
        mat[x][y] += 1
    return mat


def _cohens_kappa(a: Sequence[str], b: Sequence[str], labels: Iterable[str]) -> float:
    labels = list(labels)
    n = len(a)
    if n == 0:
        raise ValueError("empty")
    mat = {r: {c: 0 for c in labels} for r in labels}
    for x, y in zip(a, b):
        mat[x][y] += 1
    po = sum(mat[i][i] for i in labels) / n
    pa = Counter(a)
    pb = Counter(b)
    pe = sum((pa[i] / n) * (pb[i] / n) for i in labels)
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)


def cohen_kappa_3way(a: Sequence[str], b: Sequence[str]) -> float:
    aa = [normalize_label(x) for x in a]
    bb = [normalize_label(x) for x in b]
    return _cohens_kappa(aa, bb, CATEGORIES)


def binary_explicit(label: str) -> str:
    return "explicit" if normalize_label(label) == "explicit_reply" else "non_explicit"


def cohen_kappa_explicit_vs_rest(a: Sequence[str], b: Sequence[str]) -> float:
    aa = [binary_explicit(x) for x in a]
    bb = [binary_explicit(x) for x in b]
    return _cohens_kappa(aa, bb, ("explicit", "non_explicit"))


def krippendorff_alpha_nominal(a: Sequence[str], b: Sequence[str]) -> float:
    """Two-coder nominal Krippendorff's alpha (disagreement form)."""
    aa = [normalize_label(x) for x in a]
    bb = [normalize_label(x) for x in b]
    n_pairs = len(aa)
    if n_pairs == 0:
        raise ValueError("empty")
    do = sum(x != y for x, y in zip(aa, bb)) / n_pairs
    pooled = aa + bb
    n_lab = len(pooled)
    pk = Counter(pooled)
    de = 1.0 - sum((c / n_lab) ** 2 for c in pk.values())
    if de == 0:
        return 1.0
    return 1.0 - (do / de)


def summarize_round1(a: Sequence[str], b: Sequence[str]) -> dict:
    """Return planned Round-1 diagnostics. Do not call before returns exist."""
    aa = [normalize_label(x) for x in a]
    bb = [normalize_label(x) for x in b]
    ba = [binary_explicit(x) for x in aa]
    bb_bin = [binary_explicit(x) for x in bb]
    return {
        "n": len(aa),
        "raw_agreement": raw_agreement(aa, bb),
        "confusion_matrix_3way": confusion_matrix_3way(aa, bb),
        "cohen_kappa_3way": cohen_kappa_3way(aa, bb),
        "krippendorff_alpha_nominal": krippendorff_alpha_nominal(aa, bb),
        "binary_explicit_raw_agreement": sum(x == y for x, y in zip(ba, bb_bin))
        / len(ba),
        "cohen_kappa_explicit_vs_rest": cohen_kappa_explicit_vs_rest(aa, bb),
        "note": "Exploratory calibration diagnostics only; not final validation.",
    }
