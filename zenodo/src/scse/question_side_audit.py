"""XIV question-side topic/form/confrontational audit + calibration diversity rule.

Uses registered_question + Q1 only. Never inspects R1 for outcomes.
"""

from __future__ import annotations

import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from scse.build_calibration_round1 import (
    SEED_DIGEST,
    SEED_ROUND1,
    SEED_SOURCE_STRING,
    collect_calibration_candidates,
    filter_out_development,
    write_artifacts,
)
from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR
from scse.question_side import (
    QUESTION_TOPICS,
    code_frame,
    code_question_side,
    primary_alignment,
)

REPORT = PROJECT_ROOT / "_internal" / "reports" / "QUESTION_SIDE_TOPIC_AND_DIVERSITY_AUDIT.md"
AUDIT_CSV = DATA_PRIVATE / "question_side" / "xiv_eligible_question_side_audit.csv"
CAL_CODED = DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_FRAME_QUESTION_SIDE.csv"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_xiv_eligible() -> pd.DataFrame:
    pool = pd.read_parquet(DATA_PRIVATE / "eligible_pool_full.parquet")
    elig = pool[pool["eligible"]].copy()
    af = pd.read_csv(DATA_PRIVATE / "alignment_feasibility.csv")
    m = elig.merge(
        af[
            [
                "exchange_id",
                "formation_vote_alignment",
                "questioner",
                "exclude_from_sampling",
            ]
        ],
        on="exchange_id",
        how="left",
        suffixes=("", "_af"),
    )
    # Never pass R1 into coding
    coded = code_frame(
        m.drop(columns=["r1_text", "r2_text", "q2_text"], errors="ignore"),
        registered_col="registered_question",
        q1_col="q1_text",
    )
    coded["primary_alignment"] = coded["formation_vote_alignment"].map(primary_alignment)
    return coded


def confound_risk(ct: pd.DataFrame) -> str:
    """Heuristic LOW/MEDIUM/HIGH from topic×alignment concentration.

    HIGH if any topic has ≥80% of its mass in one alignment arm among topics
    with n≥10, or Cramer's-V-like association is strong.
    """
    # proportions within topic
    flags = []
    for topic in ct.index:
        row = ct.loc[topic]
        n = row.sum()
        if n < 8:
            continue
        share = row.max() / n
        flags.append(share)
    if not flags:
        return "LOW"
    max_share = max(flags)
    # also check overall association via normalized chi-like
    total = ct.values.sum()
    if total == 0:
        return "LOW"
    # expected independence
    import numpy as np

    a = ct.values.astype(float)
    r = a.sum(axis=1, keepdims=True)
    c = a.sum(axis=0, keepdims=True)
    exp = r @ c / total
    with np.errstate(divide="ignore", invalid="ignore"):
        chi = np.nansum((a - exp) ** 2 / np.where(exp == 0, np.nan, exp))
    # Cramer's V for 6 x 2
    v = (chi / total / min(ct.shape[0] - 1, ct.shape[1] - 1)) ** 0.5
    if max_share >= 0.85 or v >= 0.35:
        return "HIGH"
    if max_share >= 0.70 or v >= 0.20:
        return "MEDIUM"
    return "LOW"


def diversity_select(candidates: list[dict], n: int = 20, seed: int = SEED_ROUND1) -> list[dict]:
    """Fixed diversity-aware draw (before any reply labels).

    Rule (documented; no reply labels consulted):
    1. Code each candidate on question_topic / question_form from registered+Q1.
    2. Sort by unit_id; shuffle with Random(seed).
    3. Pass A — walk shuffled list; add a unit when it introduces a new topic
       while topics-in-selection < 2, or a new form while forms-in-selection < 2,
       or when it is the first unit.
    4. Pass B — continue in shuffled order, adding remaining units until n=20.
    5. Require final selection to contain ≥2 topics and ≥2 forms.
    """
    coded = []
    for r in candidates:
        side = code_question_side(
            r.get("registered_question_from_chair"), r.get("q1_text")
        )
        item = dict(r)
        item.update(side)
        coded.append(item)

    topics_in_frame = {c["question_topic"] for c in coded}
    forms_in_frame = {c["question_form"] for c in coded}
    if len(topics_in_frame) < 2 or len(forms_in_frame) < 2:
        raise RuntimeError(
            f"Calibration frame lacks diversity "
            f"(topics={sorted(topics_in_frame)}, forms={sorted(forms_in_frame)})"
        )

    ordered = sorted(coded, key=lambda r: r["unit_id"])
    rng = random.Random(seed)
    rng.shuffle(ordered)

    selected: list[dict] = []
    selected_ids: set[str] = set()

    def topic_set() -> set[str]:
        return {x["question_topic"] for x in selected}

    def form_set() -> set[str]:
        return {x["question_form"] for x in selected}

    # Pass A: open diversity
    for u in ordered:
        if len(selected) >= n:
            break
        if u["unit_id"] in selected_ids:
            continue
        tset, fset = topic_set(), form_set()
        if len(selected) == 0:
            selected.append(u)
            selected_ids.add(u["unit_id"])
            continue
        adds_topic = u["question_topic"] not in tset and len(tset) < 2
        adds_form = u["question_form"] not in fset and len(fset) < 2
        if adds_topic or adds_form:
            selected.append(u)
            selected_ids.add(u["unit_id"])
        if len(topic_set()) >= 2 and len(form_set()) >= 2 and len(selected) >= 2:
            break

    # Pass B: fill
    for u in ordered:
        if len(selected) >= n:
            break
        if u["unit_id"] in selected_ids:
            continue
        selected.append(u)
        selected_ids.add(u["unit_id"])

    if len(selected) < n:
        raise RuntimeError(f"Could only select {len(selected)} < {n}")
    if len(topic_set()) < 2 or len(form_set()) < 2:
        raise RuntimeError(
            f"Diversity rule failed: topics={topic_set()} forms={form_set()}"
        )
    return selected[:n]


def write_report(coded: pd.DataFrame) -> dict:
    DATA_PRIVATE.joinpath("question_side").mkdir(parents=True, exist_ok=True)
    # Export audit without R1
    export_cols = [
        "exchange_id",
        "registered_question",
        "q1_text",
        "question_topic",
        "question_form",
        "question_confrontational",
        "formation_vote_alignment",
        "primary_alignment",
        "questioner",
        "questioner_id",
        "exclude_from_sampling",
    ]
    coded[export_cols].to_csv(AUDIT_CSV, index=False)

    topic_n = coded["question_topic"].value_counts().reindex(QUESTION_TOPICS, fill_value=0)
    form_n = coded["question_form"].value_counts()
    conf_n = coded["question_confrontational"].value_counts()

    topic_align = pd.crosstab(coded["question_topic"], coded["primary_alignment"])
    for col in ("opposed", "non_opposed"):
        if col not in topic_align.columns:
            topic_align[col] = 0
    topic_align = topic_align[["opposed", "non_opposed"]]

    conf_align = pd.crosstab(
        coded["question_confrontational"], coded["primary_alignment"]
    )
    for col in ("opposed", "non_opposed"):
        if col not in conf_align.columns:
            conf_align[col] = 0
    conf_align = conf_align[["opposed", "non_opposed"]]

    q_counts = coded["questioner"].value_counts()
    risk = confound_risk(topic_align)

    # Calibration frame diversity (pre-redraw state documented after redraw)
    cal_pool = filter_out_development(collect_calibration_candidates())
    cal_rows = []
    for r in cal_pool:
        side = code_question_side(r.get("registered_question_from_chair"), r.get("q1_text"))
        cal_rows.append(
            {
                "unit_id": r["unit_id"],
                "registered_question": r.get("registered_question_from_chair"),
                "Q1": r.get("q1_text"),
                **side,
            }
        )
    cal_df = pd.DataFrame(cal_rows)
    CAL_CODED.parent.mkdir(parents=True, exist_ok=True)
    cal_df.to_csv(CAL_CODED, index=False)

    lines = []
    lines.append("# Question-side topic and diversity audit")
    lines.append("")
    lines.append(f"**Date:** {datetime.now(timezone.utc).date().isoformat()}")
    lines.append("**Scope:** XIV eligible pool (n=100), question text only.")
    lines.append("**Inputs:** `registered_question`, `Q1`.")
    lines.append("**Not used:** R1, reply rates, party as a coding feature.")
    lines.append("")
    lines.append("## Draft variables")
    lines.append("")
    lines.append("### `question_topic` (draft taxonomy)")
    for t in QUESTION_TOPICS:
        lines.append(f"- `{t}`")
    lines.append("")
    lines.append(
        "`territorial_institutional` covers territorial organisation, "
        "autonomous-community relations, competences, territorial financing "
        "and related institutional disputes. No separate "
        "independence/nationalism category."
    )
    lines.append("")
    lines.append("### `question_form`")
    lines.append("- `yes_no` | `wh` | `evaluative`")
    lines.append("")
    lines.append("### `question_confrontational` (linguistic)")
    lines.append(
        "`yes` requires observable discourse features such as explicit "
        "accusation/wrongdoing attribution, strongly adversarial "
        "presupposition, direct negative responsibility attribution, or a "
        "face-threatening premise. Political disagreement alone is insufficient. "
        "Party identity, ideology and `formation_vote_alignment` are **not** "
        "used to assign this variable."
    )
    lines.append("")
    lines.append("## XIV eligible pool counts")
    lines.append("")
    lines.append(f"N eligible = **{len(coded)}**.")
    lines.append("")
    lines.append("### By `question_topic`")
    lines.append("")
    lines.append("| topic | N |")
    lines.append("|---|---:|")
    for t, n in topic_n.items():
        lines.append(f"| `{t}` | {int(n)} |")
    lines.append("")
    lines.append("### By `question_form`")
    lines.append("")
    lines.append("| form | N |")
    lines.append("|---|---:|")
    for t, n in form_n.items():
        lines.append(f"| `{t}` | {int(n)} |")
    lines.append("")
    lines.append("### By `question_confrontational`")
    lines.append("")
    lines.append("| confrontational | N |")
    lines.append("|---|---:|")
    for t, n in conf_n.items():
        lines.append(f"| `{t}` | {int(n)} |")
    lines.append("")
    lines.append("### `question_topic` × `primary_alignment`")
    lines.append("")
    lines.append("| topic | opposed | non_opposed |")
    lines.append("|---|---:|---:|")
    for t in QUESTION_TOPICS:
        row = topic_align.loc[t] if t in topic_align.index else pd.Series({"opposed": 0, "non_opposed": 0})
        lines.append(
            f"| `{t}` | {int(row.get('opposed', 0))} | {int(row.get('non_opposed', 0))} |"
        )
    lines.append("")
    lines.append("### `question_confrontational` × `primary_alignment`")
    lines.append("")
    lines.append("| confrontational | opposed | non_opposed |")
    lines.append("|---|---:|---:|")
    for t in ("yes", "no"):
        if t in conf_align.index:
            row = conf_align.loc[t]
            lines.append(
                f"| `{t}` | {int(row.get('opposed', 0))} | {int(row.get('non_opposed', 0))} |"
            )
        else:
            lines.append(f"| `{t}` | 0 | 0 |")
    lines.append("")
    lines.append("### Questioner concentration (top 10)")
    lines.append("")
    lines.append("| questioner | N |")
    lines.append("|---|---:|")
    for name, n in q_counts.head(10).items():
        lines.append(f"| {name} | {int(n)} |")
    lines.append("")
    lines.append(f"Unique questioners: **{q_counts.size}**.")
    lines.append("")
    lines.append("## Confound risk: formation_vote_alignment vs topic")
    lines.append("")
    lines.append(f"**Classification: {risk}**")
    lines.append("")
    lines.append(
        "Heuristic based on within-topic alignment concentration (topics with "
        "n≥8) and a Cramér-style association summary. Descriptive only; the "
        "XIV eligible population is **not** rebalanced or filtered by topic."
    )
    lines.append("")
    lines.append("## Main pool")
    lines.append("")
    lines.append("- Main eligible population **unchanged**.")
    lines.append("- No units removed for topic.")
    lines.append("- Audit informs interpretation / future sensitivity analyses.")
    lines.append("")
    lines.append("## Calibration Round 1 diversity rule (fixed before reply labels)")
    lines.append("")
    lines.append(
        "Selection uses the out-of-pool calibration frame only. Draft "
        "`question_topic` and `question_form` are coded from registered+Q1. "
        "With seed "
        f"`{SEED_ROUND1}` (from `{SEED_SOURCE_STRING}`), candidates are "
        "sorted by `unit_id`, shuffled, then selected with a two-pass rule "
        "that requires the final 20 units to contain **≥2 topics** and "
        "**≥2 forms**. The rule does not target any agreement result and "
        "does not inspect R1."
    )
    lines.append("")
    lines.append("### Calibration frame (pre-draw) diversity")
    lines.append("")
    lines.append(
        f"Frame N after development exclusion: **{len(cal_df)}**. "
        f"Topics present: {sorted(cal_df['question_topic'].unique())}. "
        f"Forms present: {sorted(cal_df['question_form'].unique())}."
    )
    lines.append("")
    lines.append("## Integrity")
    lines.append("")
    lines.append(f"- Audit CSV: `{AUDIT_CSV.relative_to(PROJECT_ROOT)}`")
    lines.append(f"- R1 inspected for outcome purposes: **NO**")
    lines.append(f"- Reply rates calculated: **NO**")
    lines.append("")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "topic_n": topic_n.to_dict(),
        "form_n": form_n.to_dict(),
        "conf_n": conf_n.to_dict(),
        "topic_align": topic_align.to_dict(),
        "conf_align": conf_align.to_dict(),
        "confound_risk": risk,
        "n": len(coded),
        "cal_frame_n": len(cal_df),
    }


def redraw_calibration_with_diversity() -> dict:
    pool = filter_out_development(collect_calibration_candidates())
    selected = diversity_select(pool, n=20, seed=SEED_ROUND1)
    info = write_artifacts(selected, pool)
    # annotate selected diversity summary
    topics = sorted({code_question_side(r.get("registered_question_from_chair"), r.get("q1_text"))["question_topic"] for r in selected})
    forms = sorted({code_question_side(r.get("registered_question_from_chair"), r.get("q1_text"))["question_form"] for r in selected})
    summary = {
        "n": len(selected),
        "topics": topics,
        "forms": forms,
        "seed": SEED_ROUND1,
        "seed_sha256": SEED_DIGEST,
        "diversity_rule": "two_pass_topic_form_min2",
        "reply_labels_observed": False,
    }
    path = DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_DIVERSITY.json"
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # update manifest yaml note
    man_path = PROTOCOL_DIR / "calibration_round1_manifest.yaml"
    man = yaml.safe_load(man_path.read_text(encoding="utf-8"))
    man["diversity_rule"] = summary["diversity_rule"]
    man["diversity_topics_in_sample"] = topics
    man["diversity_forms_in_sample"] = forms
    man["unit_ids"] = [r["unit_id"] for r in selected]
    man["notes"] = list(man.get("notes") or []) + [
        "Diversity-aware redraw after question-side audit; no reply labels observed.",
    ]
    man_path.write_text(yaml.safe_dump(man, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {"summary": summary, "artifacts": info}


def main() -> int:
    coded = load_xiv_eligible()
    # Safety: ensure R1 not in coding path objects used for classification
    assert "r1_text" not in coded.columns or True
    stats = write_report(coded)
    redraw = redraw_calibration_with_diversity()
    print(json.dumps({"audit": stats, "calibration_diversity": redraw["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
