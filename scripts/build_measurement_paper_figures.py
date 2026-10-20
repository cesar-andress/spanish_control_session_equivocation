#!/usr/bin/env python3
"""Build Phase 8C/8G manuscript figures from the locked evidence JSON."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
LOCK = (
    ROOT
    / "_internal"
    / "data_private"
    / "measurement_paper"
    / "MEASUREMENT_PAPER_EVIDENCE_LOCK.json"
)
OUT = ROOT / "paper" / "figures"
ZEN = ROOT / "zenodo" / "outputs" / "figures"


def main() -> None:
    p = json.loads(LOCK.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    ZEN.mkdir(parents=True, exist_ok=True)

    # Chronological within each coefficient family (three-way, collapse, redesign).
    rows = [
        ("Dev. 3-way κ", p["development"]["cohen_kappa_3way"], p["development"]["cohen_kappa_3way_ci"], "three"),
        ("R1 final 3-way κ", p["round1_final_20"]["cohen_kappa_3way"], p["round1_final_20"]["cohen_kappa_3way_ci"], "three"),
        ("R2 3-way κ", p["round2"]["cohen_kappa_3way"], p["round2"]["cohen_kappa_3way_ci"], "three"),
        ("Pooled R1+R2 3-way κ", p["pooled_r1_r2"]["cohen_kappa_3way"], p["pooled_r1_r2"]["cohen_kappa_3way_ci"], "three"),
        ("Dev. binary collapse", p["development"]["cohen_kappa_explicit_vs_rest"], p["development"]["cohen_kappa_explicit_vs_rest_ci"], "collapse"),
        ("R1 final binary collapse", p["round1_final_20"]["cohen_kappa_explicit_vs_rest"], p["round1_final_20"]["cohen_kappa_explicit_vs_rest_ci"], "collapse"),
        ("R2 binary collapse", p["round2"]["cohen_kappa_explicit_vs_rest"], p["round2"]["cohen_kappa_explicit_vs_rest_ci"], "collapse"),
        ("Pooled binary collapse", p["pooled_r1_r2"]["cohen_kappa_explicit_vs_rest"], p["pooled_r1_r2"]["cohen_kappa_explicit_vs_rest_ci"], "collapse"),
        ("Binary redesign κ", p["binary_validation"]["cohen_kappa"], p["binary_validation"]["cohen_kappa_ci"], "binary"),
    ]

    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    ys = list(range(len(rows)))[::-1]
    style = {
        "three": dict(fmt="o", color="#1f4e79", mfc="#1f4e79"),
        "collapse": dict(fmt="s", color="#5b7c99", mfc="white"),
        "binary": dict(fmt="D", color="#8b2e2e", mfc="#8b2e2e"),
    }
    for y, (lab, point, ci, kind) in zip(ys, rows):
        lo, hi = ci["ci_low"], ci["ci_high"]
        st = style[kind]
        ax.errorbar(
            point,
            y,
            xerr=[[point - lo], [hi - point]],
            fmt=st["fmt"],
            color=st["color"],
            ecolor=st["color"],
            elinewidth=1.2,
            capsize=3,
            markersize=7,
            mfc=st["mfc"],
            mec=st["color"],
        )
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    # Draw reference lines only within the data band (avoid touching the title).
    y_lo, y_hi = -0.35, len(rows) - 0.55
    ax.plot([0.0, 0.0], [y_lo, y_hi], color="#888888", lw=0.8, ls=":", zorder=0)
    ax.plot([0.67, 0.67], [y_lo, y_hi], color="#aaaaaa", lw=0.9, ls="--", zorder=0)
    # Concise in-panel labels (placed below the data band).
    ax.text(0.0, -0.48, "0 = chance", ha="center", va="top", fontsize=7, color="#666666")
    ax.text(0.67, -0.48, "0.67 = decision rule", ha="center", va="top", fontsize=7, color="#666666")
    ax.set_xlabel("Estimate (percentile 95% bootstrap CI; seed 20261020, 5000 resamples)")
    ax.set_xlim(-0.45, 1.05)
    ax.set_ylim(-0.72, len(rows) - 0.25)
    ax.set_title("Reliability estimates across measurement exercises", pad=18)
    legend = [
        Line2D([0], [0], marker="o", color="#1f4e79", mfc="#1f4e79", ls="", label="Three-category scheme"),
        Line2D([0], [0], marker="s", color="#5b7c99", mfc="white", ls="", label="Binary collapse (same scheme)"),
        Line2D([0], [0], marker="D", color="#8b2e2e", mfc="#8b2e2e", ls="", label="Yes/No scheme (direct resolution)"),
    ]
    ax.legend(
        handles=legend,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=3,
        fontsize=8,
        frameon=False,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.22)
    for dest in (OUT / "fig2_reliability_estimates.pdf", ZEN / "fig2_reliability_estimates.pdf"):
        fig.savefig(dest, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote figures to {OUT}")


if __name__ == "__main__":
    main()
