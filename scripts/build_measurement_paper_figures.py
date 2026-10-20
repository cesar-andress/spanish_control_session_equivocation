#!/usr/bin/env python3
"""Build Phase 8C manuscript figures from the locked evidence JSON."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

    # Coefficient plot (Figure 2)
    rows = [
        ("Dev.\n3-way κ", p["development"]["cohen_kappa_3way"], p["development"]["cohen_kappa_3way_ci"], "three"),
        ("R1 final\n3-way κ", p["round1_final_20"]["cohen_kappa_3way"], p["round1_final_20"]["cohen_kappa_3way_ci"], "three"),
        ("R2\n3-way κ", p["round2"]["cohen_kappa_3way"], p["round2"]["cohen_kappa_3way_ci"], "three"),
        ("Pooled R1+R2\n3-way κ", p["pooled_r1_r2"]["cohen_kappa_3way"], p["pooled_r1_r2"]["cohen_kappa_3way_ci"], "three"),
        ("Dev.\nbinary collapse", p["development"]["cohen_kappa_explicit_vs_rest"], p["development"]["cohen_kappa_explicit_vs_rest_ci"], "collapse"),
        ("R1 final\nbinary collapse", p["round1_final_20"]["cohen_kappa_explicit_vs_rest"], p["round1_final_20"]["cohen_kappa_explicit_vs_rest_ci"], "collapse"),
        ("R2\nbinary collapse", p["round2"]["cohen_kappa_explicit_vs_rest"], p["round2"]["cohen_kappa_explicit_vs_rest_ci"], "collapse"),
        ("Pooled\nbinary collapse", p["pooled_r1_r2"]["cohen_kappa_explicit_vs_rest"], p["pooled_r1_r2"]["cohen_kappa_explicit_vs_rest_ci"], "collapse"),
        ("Binary redesign\nκ", p["binary_validation"]["cohen_kappa"], p["binary_validation"]["cohen_kappa_ci"], "binary"),
    ]

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
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
    ax.axvline(0.0, color="#888888", lw=0.8, ls=":")
    ax.axvline(0.67, color="#aaaaaa", lw=0.8, ls="--")
    ax.text(0.67, ys[0] + 0.55, "project gate 0.67", fontsize=7, color="#666666", ha="center")
    ax.set_xlabel("Estimate (percentile 95% bootstrap CI; seed 20261020, 5000 resamples)")
    ax.set_xlim(-0.45, 1.05)
    ax.set_title("Reliability estimates across measurement exercises")
    legend = [
        Line2D([0], [0], marker="o", color="#1f4e79", mfc="#1f4e79", ls="", label="Three-category κ"),
        Line2D([0], [0], marker="s", color="#5b7c99", mfc="white", ls="", label="Binary collapse (explicit vs rest)"),
        Line2D([0], [0], marker="D", color="#8b2e2e", mfc="#8b2e2e", ls="", label="Redesigned binary κ"),
    ]
    ax.legend(handles=legend, loc="lower right", fontsize=8, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    for dest in (OUT / "fig2_reliability_estimates.pdf", ZEN / "fig2_reliability_estimates.pdf"):
        fig.savefig(dest, bbox_inches="tight")
    plt.close(fig)

    # Simple PNG flow also saved as metadata companion (TikZ is primary in TeX)
    fig, ax = plt.subplots(figsize=(9.5, 2.8))
    ax.axis("off")
    boxes = [
        (0.05, "Development\nN=15\nindependent"),
        (0.22, "Round 1\nN=20\nindependent"),
        (0.39, "Joint review\n(not used as\noutcomes)"),
        (0.56, "Round 2\nN=20\nindependent\nGate C"),
        (0.73, "Binary redesign\nN=12\nindependent\nFAIL"),
        (0.90, "Methodological\npivot"),
    ]
    for x, text in boxes:
        ax.add_patch(
            mpatches.FancyBboxPatch(
                (x - 0.07, 0.35),
                0.14,
                0.45,
                boxstyle="round,pad=0.01,rounding_size=0.02",
                facecolor="#f3f6f9",
                edgecolor="#1f4e79",
                lw=1.2,
                transform=ax.transAxes,
                clip_on=False,
            )
        )
        ax.text(x, 0.57, text, ha="center", va="center", fontsize=7, transform=ax.transAxes)
    for x0, x1 in [(0.12, 0.15), (0.29, 0.32), (0.46, 0.49), (0.63, 0.66), (0.80, 0.83)]:
        ax.annotate(
            "",
            xy=(x1, 0.57),
            xytext=(x0, 0.57),
            xycoords=ax.transAxes,
            arrowprops=dict(arrowstyle="->", color="#333333", lw=1.0),
        )
    ax.set_title("Measurement programme (independent coding vs joint discussion)", fontsize=10)
    fig.tight_layout()
    for dest in (OUT / "fig1_measurement_flow.pdf", ZEN / "fig1_measurement_flow.pdf"):
        fig.savefig(dest, bbox_inches="tight")
    plt.close(fig)
    print("wrote figures to", OUT)


if __name__ == "__main__":
    main()
