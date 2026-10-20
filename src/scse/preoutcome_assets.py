"""Pre-outcome tables, figure shells, and study-flow asset."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scse.main_frame import load_main_corpus
from scse.paths import FIGURES_DIR, PROJECT_ROOT, TABLES_DIR


def build_table1_composition() -> Path:
    """TABLE 1: corpus / questioner / alignment composition (pre-outcome OK)."""
    corpus = load_main_corpus()
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        {"item": "main_frame_N", "value": len(corpus)},
        {"item": "sessions", "value": int(corpus["session_id"].nunique())},
        {"item": "questioners", "value": int(corpus["questioner_id"].nunique())},
        {
            "item": "primary_alignment_opposed",
            "value": int(corpus["primary_alignment"].eq("opposed").sum()),
        },
        {
            "item": "primary_alignment_non_opposed",
            "value": int(corpus["primary_alignment"].eq("non_opposed").sum()),
        },
    ]
    for g, n in corpus["formation_vote_alignment"].value_counts().items():
        rows.append({"item": f"formation_vote_{g}", "value": int(n)})
    for t, n in corpus["question_topic"].value_counts().items():
        rows.append({"item": f"topic_{t}", "value": int(n)})
    for c, n in corpus["question_confrontational"].value_counts().items():
        rows.append({"item": f"confrontational_{c}", "value": int(n)})
    df = pd.DataFrame(rows)
    path = TABLES_DIR / "table1_corpus_composition.csv"
    df.to_csv(path, index=False)
    return path


def build_outcome_table_shells() -> dict[str, Path]:
    """TABLE 2–3 shells: outcome cells intentionally empty/NA."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    t2 = pd.DataFrame(
        {
            "reply_status": ["explicit", "partial", "absent"],
            "n": [pd.NA, pd.NA, pd.NA],
            "proportion": [pd.NA, pd.NA, pd.NA],
            "note": ["PLACEHOLDER_AWAITING_OUTCOMES"] * 3,
        }
    )
    t2_path = TABLES_DIR / "table2_reply_status_distribution_SHELL.csv"
    t2.to_csv(t2_path, index=False)

    t3 = pd.DataFrame(
        {
            "primary_alignment": ["opposed", "non_opposed", "difference_non_minus_opp"],
            "n": [pd.NA, pd.NA, pd.NA],
            "p_explicit": [pd.NA, pd.NA, pd.NA],
            "ci_lo": [pd.NA, pd.NA, pd.NA],
            "ci_hi": [pd.NA, pd.NA, pd.NA],
            "note": ["PLACEHOLDER_AWAITING_OUTCOMES"] * 3,
        }
    )
    t3_path = TABLES_DIR / "table3_explicit_contrast_SHELL.csv"
    t3.to_csv(t3_path, index=False)
    return {"table2": t2_path, "table3": t3_path}


def build_study_flow_svg() -> Path:
    """FIGURE 1: pre-outcome study flow with known counts only."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / "fig1_study_flow_preoutcome.svg"
    # Counts from Phase-2 report + Phase 6A restoration
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="720" height="640" viewBox="0 0 720 640">
  <style>
    .box { fill:#ffffff; stroke:#222; stroke-width:1.4; }
    .title { font: 700 15px 'Times New Roman', serif; fill:#111; }
    .body { font: 13px 'Times New Roman', serif; fill:#222; }
    .note { font: italic 12px 'Times New Roman', serif; fill:#444; }
    .arrow { stroke:#222; stroke-width:1.5; fill:none; marker-end:url(#arrow); }
  </style>
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#222"/>
    </marker>
  </defs>
  <text x="360" y="28" text-anchor="middle" class="title">Study flow (pre-outcome)</text>

  <rect class="box" x="180" y="48" width="360" height="52" rx="4"/>
  <text x="360" y="70" text-anchor="middle" class="body">Congreso registered oral-question records</text>
  <text x="360" y="88" text-anchor="middle" class="body">acquired for candidates ≈ 166</text>

  <path class="arrow" d="M360 100 V120"/>

  <rect class="box" x="180" y="120" width="360" height="52" rx="4"/>
  <text x="360" y="142" text-anchor="middle" class="body">PM-directed candidate exchanges</text>
  <text x="360" y="160" text-anchor="middle" class="body">ParlaMint-ES XIV PM FORMULA = 139</text>

  <path class="arrow" d="M360 172 V192"/>

  <rect class="box" x="180" y="192" width="360" height="52" rx="4"/>
  <text x="360" y="214" text-anchor="middle" class="body">Linked exchanges (exact ∪ high_confidence)</text>
  <text x="360" y="232" text-anchor="middle" class="body">complete registered + Q1 + R1 = 100</text>

  <path class="arrow" d="M360 244 V264"/>

  <rect class="box" x="80" y="264" width="250" height="70" rx="4"/>
  <text x="205" y="290" text-anchor="middle" class="body">Linkage QA reviewed</text>
  <text x="205" y="308" text-anchor="middle" class="body">n = 30 (linkage only)</text>
  <text x="205" y="324" text-anchor="middle" class="note">not reply-status contaminated</text>

  <rect class="box" x="390" y="264" width="250" height="70" rx="4"/>
  <text x="515" y="290" text-anchor="middle" class="body">Phase-0 feasibility probes</text>
  <text x="515" y="308" text-anchor="middle" class="body">n = 3 (linkage probe only)</text>
  <text x="515" y="324" text-anchor="middle" class="note">restored after Phase 6B audit</text>

  <path class="arrow" d="M205 334 V370"/>
  <path class="arrow" d="M515 334 V370"/>
  <path class="arrow" d="M205 370 H515"/>
  <path class="arrow" d="M360 370 V400"/>

  <rect class="box" x="160" y="400" width="400" height="70" rx="4"/>
  <text x="360" y="428" text-anchor="middle" class="title">Final pre-outcome main frame</text>
  <text x="360" y="450" text-anchor="middle" class="body">N = 100  (full linked eligible census)</text>

  <text x="360" y="500" text-anchor="middle" class="note">Unlinked / ambiguous mechanical attrition: 37 unlinked + 2 ambiguous (from 139).</text>
  <text x="360" y="520" text-anchor="middle" class="note">No reply-status outcomes. No outcome-based exclusions.</text>
  <text x="360" y="560" text-anchor="middle" class="note">QA30 + Phase-0 probes restored (Phase 6B contamination audit).</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")
    # also a tiny pdf via cairo if available is optional; SVG is publication-ready vector
    meta = {
        "figure": "fig1_study_flow_preoutcome",
        "path": str(path.relative_to(PROJECT_ROOT)),
        "counts": {
            "registered_approx": 166,
            "pm_candidates": 139,
            "linked_eligible": 100,
            "linkage_qa_reviewed": 30,
            "phase0_restored": 3,
            "phase0_excluded": 0,
            "main_frame": 100,
            "unlinked": 37,
            "ambiguous": 2,
        },
        "outcome_exclusions": 0,
    }
    (FIGURES_DIR / "fig1_study_flow_preoutcome.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    return path


def build_figure_shells() -> dict[str, Path]:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    shells = {}
    for name, title in [
        ("fig2_per_questioner_explicit_SHELL.txt", "FIGURE 2 — per-questioner explicit-response plot"),
        ("fig3_loo_questioner_SHELL.txt", "FIGURE 3 — leave-one-questioner-out sensitivity"),
        ("fig_topic_composition_OPTIONAL_SHELL.txt", "OPTIONAL — question-topic composition"),
    ]:
        path = FIGURES_DIR / name
        path.write_text(
            f"{title}\nSTATUS: PLACEHOLDER_AWAITING_OUTCOMES\n"
            "Do not invent values. Populate only after main annotation.\n",
            encoding="utf-8",
        )
        shells[name] = path
    return shells


def build_all_preoutcome_assets() -> dict:
    t1 = build_table1_composition()
    shells = build_outcome_table_shells()
    flow = build_study_flow_svg()
    fig_shells = build_figure_shells()
    return {
        "table1": str(t1.relative_to(PROJECT_ROOT)),
        "table2_shell": str(shells["table2"].relative_to(PROJECT_ROOT)),
        "table3_shell": str(shells["table3"].relative_to(PROJECT_ROOT)),
        "study_flow": str(flow.relative_to(PROJECT_ROOT)),
        "figure_shells": [str(p.relative_to(PROJECT_ROOT)) for p in fig_shells.values()],
    }
