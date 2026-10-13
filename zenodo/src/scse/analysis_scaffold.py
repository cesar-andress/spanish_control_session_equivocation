"""Pre-outcome analysis scaffold.

All functions accept labelled frames. Tests must pass synthetic fixtures only.
Calling these on real XIV reply_status data is forbidden until Phase 8.
"""

from __future__ import annotations

from dataclasses import dataclass
from os import PathLike
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED_LABEL_COLS = {"unit_id", "reply_status", "questioner_id", "primary_alignment"}
EXPLICIT = {"respuesta explícita", "explicit", "explícita"}
PARTIAL = {"respuesta parcial o intermedia", "partial", "parcial"}
ABSENT = {"ausencia de respuesta", "absent", "ausencia", "non-reply", "non_reply"}


@dataclass(frozen=True)
class ContrastResult:
    group_a: str
    group_b: str
    p_a: float
    p_b: float
    risk_difference: float
    n_a: int
    n_b: int


def _require_labels(df: pd.DataFrame) -> None:
    missing = REQUIRED_LABEL_COLS - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")


def normalize_reply_status(value: object) -> str:
    s = str(value).strip().lower()
    if s in EXPLICIT or s == "explicit":
        return "explicit"
    if s in PARTIAL or "parcial" in s or s == "partial":
        return "partial"
    if s in ABSENT or "ausencia" in s or s in {"non-reply", "non_reply", "absent"}:
        return "absent"
    raise ValueError(f"unrecognised reply_status: {value!r}")


def category_distribution(df: pd.DataFrame) -> pd.Series:
    _require_labels(df)
    cats = df["reply_status"].map(normalize_reply_status)
    return cats.value_counts(dropna=False).reindex(
        ["explicit", "partial", "absent"], fill_value=0
    )


def explicit_vs_nonexplicit(df: pd.DataFrame) -> pd.DataFrame:
    _require_labels(df)
    out = df.copy()
    out["reply_norm"] = out["reply_status"].map(normalize_reply_status)
    out["explicit_bin"] = out["reply_norm"].eq("explicit")
    return out


def opposed_vs_nonopposed_contrast(df: pd.DataFrame) -> ContrastResult:
    labelled = explicit_vs_nonexplicit(df)
    groups = {}
    for g in ("opposed", "non_opposed"):
        sub = labelled[labelled["primary_alignment"].eq(g)]
        n = len(sub)
        p = float(sub["explicit_bin"].mean()) if n else float("nan")
        groups[g] = (p, n)
    p_a, n_a = groups["opposed"]
    p_b, n_b = groups["non_opposed"]
    return ContrastResult(
        group_a="opposed",
        group_b="non_opposed",
        p_a=p_a,
        p_b=p_b,
        risk_difference=p_b - p_a,
        n_a=n_a,
        n_b=n_b,
    )


def formation_vote_three_way(df: pd.DataFrame) -> pd.DataFrame:
    if "formation_vote_alignment" not in df.columns:
        raise ValueError("formation_vote_alignment required")
    labelled = explicit_vs_nonexplicit(df)
    rows = []
    for g, sub in labelled.groupby("formation_vote_alignment", dropna=False):
        rows.append(
            {
                "formation_vote_alignment": g,
                "n": len(sub),
                "p_explicit": float(sub["explicit_bin"].mean()) if len(sub) else float("nan"),
            }
        )
    return pd.DataFrame(rows).sort_values("formation_vote_alignment")


def risk_difference_explicit(df: pd.DataFrame) -> float:
    return opposed_vs_nonopposed_contrast(df).risk_difference


def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return (float("nan"), float("nan"))
    phat = successes / n
    denom = 1 + z**2 / n
    centre = phat + z**2 / (2 * n)
    margin = z * np.sqrt(phat * (1 - phat) / n + z**2 / (4 * n**2))
    return ((centre - margin) / denom, (centre + margin) / denom)


def uncertainty_intervals(df: pd.DataFrame) -> pd.DataFrame:
    labelled = explicit_vs_nonexplicit(df)
    rows = []
    for g, sub in labelled.groupby("primary_alignment"):
        k = int(sub["explicit_bin"].sum())
        n = len(sub)
        lo, hi = wilson_interval(k, n)
        rows.append({"primary_alignment": g, "n": n, "k_explicit": k, "p": k / n if n else np.nan, "lo": lo, "hi": hi})
    return pd.DataFrame(rows)


def questioner_cluster_bootstrap(
    df: pd.DataFrame,
    *,
    n_boot: int = 500,
    seed: int = 0,
    statistic: str = "risk_difference",
) -> dict:
    """Cluster bootstrap by questioner_id (synthetic-safe)."""
    labelled = explicit_vs_nonexplicit(df)
    rng = np.random.default_rng(seed)
    questioners = labelled["questioner_id"].dropna().unique().tolist()
    if not questioners:
        raise ValueError("no questioners")
    stats = []
    for _ in range(n_boot):
        draw = rng.choice(questioners, size=len(questioners), replace=True)
        parts = [labelled[labelled["questioner_id"].eq(q)] for q in draw]
        boot = pd.concat(parts, ignore_index=True)
        if statistic == "risk_difference":
            stats.append(risk_difference_explicit(boot))
        else:
            raise ValueError(statistic)
    arr = np.asarray(stats, dtype=float)
    return {
        "statistic": statistic,
        "n_boot": n_boot,
        "mean": float(np.nanmean(arr)),
        "lo": float(np.nanpercentile(arr, 2.5)),
        "hi": float(np.nanpercentile(arr, 97.5)),
    }


def per_questioner_explicit_rates(df: pd.DataFrame) -> pd.DataFrame:
    labelled = explicit_vs_nonexplicit(df)
    rows = []
    for q, sub in labelled.groupby("questioner_id"):
        rows.append(
            {
                "questioner_id": q,
                "n": len(sub),
                "p_explicit": float(sub["explicit_bin"].mean()),
                "primary_alignment": sub["primary_alignment"].iloc[0]
                if sub["primary_alignment"].nunique() == 1
                else "mixed",
            }
        )
    return pd.DataFrame(rows).sort_values("questioner_id")


def leave_one_questioner_out(df: pd.DataFrame) -> pd.DataFrame:
    labelled = explicit_vs_nonexplicit(df)
    qs = labelled["questioner_id"].dropna().unique()
    rows = []
    for q in qs:
        sub = labelled[labelled["questioner_id"] != q]
        c = opposed_vs_nonopposed_contrast(sub)
        rows.append(
            {
                "left_out": q,
                "n_remaining": len(sub),
                "risk_difference": c.risk_difference,
                "p_opposed": c.p_a,
                "p_non_opposed": c.p_b,
            }
        )
    return pd.DataFrame(rows)


def annotator_specific_distribution(df: pd.DataFrame, annotator_col: str = "annotator") -> pd.DataFrame:
    if annotator_col not in df.columns:
        raise ValueError(f"missing {annotator_col}")
    rows = []
    for ann, sub in df.groupby(annotator_col):
        dist = category_distribution(sub)
        rows.append({"annotator": ann, **dist.to_dict()})
    return pd.DataFrame(rows)


def adjudicated_or_final_analysis(df: pd.DataFrame, label_col: str = "reply_status") -> ContrastResult:
    """Run primary contrast on a chosen label column (e.g. adjudicated)."""
    tmp = df.copy()
    if label_col != "reply_status":
        tmp = tmp.rename(columns={label_col: "reply_status"})
    return opposed_vs_nonopposed_contrast(tmp)


def topic_stratified_explicit(df: pd.DataFrame) -> pd.DataFrame:
    if "question_topic" not in df.columns:
        raise ValueError("question_topic required")
    labelled = explicit_vs_nonexplicit(df)
    rows = []
    for (topic, align), sub in labelled.groupby(["question_topic", "primary_alignment"]):
        rows.append(
            {
                "question_topic": topic,
                "primary_alignment": align,
                "n": len(sub),
                "p_explicit": float(sub["explicit_bin"].mean()),
            }
        )
    return pd.DataFrame(rows)


def confrontational_sensitivity(df: pd.DataFrame) -> pd.DataFrame | None:
    """Optional sensitivity if protocol permits question_confrontational.

    Returns stratum-specific contrasts; does not claim causal identification.
    """
    if "question_confrontational" not in df.columns:
        return None
    labelled = explicit_vs_nonexplicit(df)
    rows = []
    for flag, sub in labelled.groupby("question_confrontational"):
        if sub["primary_alignment"].nunique() < 2:
            rows.append(
                {
                    "question_confrontational": flag,
                    "n": len(sub),
                    "risk_difference": float("nan"),
                    "note": "single alignment stratum",
                }
            )
            continue
        c = opposed_vs_nonopposed_contrast(sub)
        rows.append(
            {
                "question_confrontational": flag,
                "n": len(sub),
                "risk_difference": c.risk_difference,
                "note": "descriptive_only",
            }
        )
    return pd.DataFrame(rows)


def make_synthetic_fixture(n: int = 40, seed: int = 1) -> pd.DataFrame:
    """Synthetic labelled frame for tests only — not XIV data."""
    rng = np.random.default_rng(seed)
    questioners = [f"Q{i}" for i in range(1, 9)]
    topics = ["economy_employment", "foreign_security", "other"]
    rows = []
    for i in range(n):
        q = questioners[i % len(questioners)]
        align = "opposed" if (i % 8) < 5 else "non_opposed"
        status = ["explicit", "partial", "absent"][int(rng.integers(0, 3))]
        rows.append(
            {
                "unit_id": f"syn_{i:03d}",
                "reply_status": status,
                "questioner_id": q,
                "primary_alignment": align,
                "formation_vote_alignment": "opposed"
                if align == "opposed"
                else ("supported" if i % 2 == 0 else "abstained"),
                "question_topic": topics[i % len(topics)],
                "question_confrontational": "yes" if (align == "opposed" and i % 3 == 0) else "no",
                "annotator": "A" if i % 2 == 0 else "B",
            }
        )
    return pd.DataFrame(rows)


def refuse_real_xiv_paths(path: str | PathLike | Path) -> None:
    text = str(path).lower()
    banned = ("main_frame_corpus", "eligible_pool_full", "xiv_eligible")
    if any(b in text for b in banned) and "synthetic" not in text:
        raise RuntimeError(
            "Refusing to run analysis scaffold on real XIV corpus paths "
            "before Phase 8 outcomes exist"
        )
