"""Phase 7A: expand fresh OOP frame and draw binary-validation N=12.

Date-aware PM answerer (fixes opposition-Sánchez false PM breaks).
Does not inspect R1 for selection. Does not generate human DOCX.
Does not touch Round-1/2 labels or XIV outcomes.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from collections import Counter
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from scse.build_calibration_round1 import WINDOWS, make_cal_unit_id
from scse.build_calibration_round2 import (
    load_development_exclusions,
    load_round1_exclusions,
    load_xiv_and_qa_exclusions,
    normalize_text,
)
from scse.build_development_set import (
    _extract_registered,
    _is_pm_formula_chair,
    iter_session_files,
)
from scse.extract_exchanges import (
    RawExchange,
    _is_chair,
    _notes_expediente,
    parse_session_utterances,
)
from scse.paths import DATA_PRIVATE, PARLAMINT_CACHE, PROJECT_ROOT, PROTOCOL_DIR
from scse.question_side import code_question_side

SEED_SOURCE_STRING = (
    "spanish_control_session_equivocation|binary_validation_v1|fresh_oop_n12"
)
SEED_DIGEST = hashlib.sha256(SEED_SOURCE_STRING.encode("utf-8")).hexdigest()
SEED_BINARY_VAL = int(SEED_DIGEST[:16], 16) % (2**31 - 1)
SEED_CONVERSION = "int(sha256(source_string).hexdigest()[:16], 16) % (2**31 - 1)"

VAL_N = 12
RAJOY = "#MarianoRajoyBrey"
SANCHEZ = "#PedroSánchezPérezCastejón"
CENSURE = date(2018, 6, 1)
XIV_START = date(2019, 12, 3)
XIV_END = date(2023, 2, 23)

OUT_DIR = DATA_PRIVATE / "validation" / "binary_v1"
REPORT = PROJECT_ROOT / "_internal" / "reports" / "FRESH_BINARY_VALIDATION_FRAME_AUDIT.md"
SEEDS_YAML = PROTOCOL_DIR / "seeds.yaml"

TARGET_MIN_TOPICS = 4
TARGET_MIN_FORMS = 2
TARGET_MAX_PER_QUESTIONER = 2
TARGET_MAX_PER_SITTING = 2
TARGET_MAX_TOPIC_SHARE = 5


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def answerer_for(d: date) -> str:
    return SANCHEZ if d >= CENSURE else RAJOY


def _document_relpath(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PARLAMINT_CACHE.resolve()))
    except ValueError:
        return path.name


def extract_pm_binary_frame_exchanges(
    path: Path, *, legislature: str
) -> list[RawExchange]:
    """PM FORMULA Q1–R1 with date-aware sitting PM as sole answerer."""
    path = path.resolve()
    session_id, session_date, utts = parse_session_utterances(path)
    if not session_date:
        return []
    d = date.fromisoformat(str(session_date)[:10])
    if XIV_START <= d <= XIV_END:
        return []
    pm_answerer = answerer_for(d)
    exchanges: list[RawExchange] = []
    used_q1: set[str] = set()

    for i, u in enumerate(utts):
        if not _is_chair(u) or not _is_pm_formula_chair(u.text):
            continue
        reg_q, exp = _extract_registered(u.text)
        q_idx = None
        r_idx = None
        for j in range(i + 1, min(i + 20, len(utts))):
            uj = utts[j]
            if _is_chair(uj):
                if _is_pm_formula_chair(uj.text):
                    break
                continue
            if q_idx is None:
                if (uj.who or "") == pm_answerer:
                    break
                q_idx = j
                continue
            if utts[q_idx].who == uj.who:
                continue
            if (uj.who or "") == pm_answerer:
                r_idx = j
                break
            break
        if q_idx is None or r_idx is None:
            continue
        if utts[q_idx].uid in used_q1:
            continue

        q_who = utts[q_idx].who
        q_parts = []
        for j in range(q_idx, r_idx):
            if not _is_chair(utts[j]) and utts[j].who == q_who:
                q_parts.append(utts[j].text)
        q1_text = " ".join(q_parts).strip()
        r1_text = utts[r_idx].text.strip()
        if not q1_text or not r1_text:
            continue
        if not exp:
            exp = _notes_expediente(utts[q_idx].notes) or _notes_expediente(
                utts[r_idx].notes
            )
        notes = ["binary_validation_extractor_v1"]
        if not reg_q:
            notes.append("registered_question_missing_in_chair")

        exchanges.append(
            RawExchange(
                session_id=session_id,
                document_path=_document_relpath(path),
                date=session_date,
                legislature=legislature,
                expediente=exp,
                registered_question_from_chair=reg_q,
                questioner_who=q_who,
                answerer_who=utts[r_idx].who or "",
                q1_utterance_id=utts[q_idx].uid,
                r1_utterance_id=utts[r_idx].uid,
                q1_text=q1_text,
                r1_text=r1_text,
                chair_announcement=u.text,
                extraction_notes=notes,
            )
        )
        used_q1.add(utts[q_idx].uid)
    return exchanges


def collect_expanded_oop_candidates() -> list[dict]:
    rows: list[dict] = []
    for leg, start, end in WINDOWS:
        for path in iter_session_files(start, end):
            for r in extract_pm_binary_frame_exchanges(path, legislature=leg):
                d = asdict(r)
                d["unit_id"] = make_cal_unit_id(r)
                reg = str(d.get("registered_question_from_chair") or "").strip()
                q1 = str(d.get("q1_text") or "").strip()
                r1 = str(d.get("r1_text") or "").strip()
                if reg and q1 and r1:
                    rows.append(d)
    return list({r["unit_id"]: r for r in rows}.values())


def load_round2_exclusions() -> dict:
    audit = DATA_PRIVATE / "calibration" / "round2" / "CALIBRATION_ROUND2_AUDIT.csv"
    pkt = DATA_PRIVATE / "calibration" / "round2" / "CALIBRATION_ROUND2_PACKET_BLINDED.csv"
    a = pd.read_csv(audit)
    p = pd.read_csv(pkt)
    return {
        "unit_ids": set(a["unit_id"].astype(str)),
        "q1_r1": set(
            zip(a["q1_utterance_id"].astype(str), a["r1_utterance_id"].astype(str))
        ),
        "q1": set(a["q1_utterance_id"].astype(str)),
        "reg_norm": {normalize_text(t) for t in p["registered_question"]},
        "q1_norm": {normalize_text(t) for t in p["Q1"]},
        "session_ids": set(a["session_id"].astype(str)),
        "expedientes": {
            str(x).strip() for x in a["expediente"].dropna().astype(str) if str(x).strip()
        },
    }


def filter_all_human_exposure(candidates: list[dict]) -> tuple[list[dict], dict]:
    """Exclude every exchange ever shown to annotators / used in prior phases."""
    r1 = load_round1_exclusions()
    r2 = load_round2_exclusions()
    dev = load_development_exclusions()
    xq = load_xiv_and_qa_exclusions()

    # Superseded XIV in-pool development (if present)
    sup_path = (
        DATA_PRIVATE
        / "development"
        / "superseded_xiv_inpool_2026-10-01"
        / "DEVELOPMENT_SET_AUDIT.csv"
    )
    sup_q1: set[str] = set()
    if sup_path.is_file():
        sup = pd.read_csv(sup_path)
        if "q1_utterance_id" in sup.columns:
            sup_q1 = set(sup["q1_utterance_id"].astype(str))

    exposed_unit = r1["unit_ids"] | r2["unit_ids"] | dev["unit_ids"]
    exposed_q1 = r1["q1"] | r2["q1"] | dev["q1"] | xq["xiv_q1"] | xq["qa_q1"] | xq[
        "phase0_q1"
    ] | sup_q1
    exposed_q1_r1 = r1["q1_r1"] | r2["q1_r1"] | dev["q1_r1"]
    exposed_reg = r1["reg_norm"] | r2["reg_norm"] | dev["reg_norm"] | xq["xiv_reg_norm"]
    exposed_q1n = r1["q1_norm"] | r2["q1_norm"] | dev["q1_norm"] | xq["xiv_q1_norm"]
    exposed_exp = r2["expedientes"] | xq["qa_exp"] | xq["phase0_exp"]

    out = []
    drop_reasons: Counter[str] = Counter()
    for r in candidates:
        uid = str(r["unit_id"])
        q1 = str(r["q1_utterance_id"])
        r1u = str(r["r1_utterance_id"])
        key = (q1, r1u)
        reg_n = normalize_text(r.get("registered_question_from_chair"))
        q1_n = normalize_text(r.get("q1_text"))
        exp = str(r.get("expediente") or "").strip()
        if uid in exposed_unit:
            drop_reasons["unit_id"] += 1
            continue
        if key in exposed_q1_r1:
            drop_reasons["q1_r1"] += 1
            continue
        if q1 in exposed_q1:
            drop_reasons["q1"] += 1
            continue
        if exp and exp in exposed_exp:
            drop_reasons["expediente"] += 1
            continue
        if reg_n and reg_n in exposed_reg:
            drop_reasons["reg_norm"] += 1
            continue
        if q1_n and q1_n in exposed_q1n:
            drop_reasons["q1_norm"] += 1
            continue
        out.append(r)

    audit = {
        "n_candidates_expanded": len(candidates),
        "n_untouched": len(out),
        "n_dropped": len(candidates) - len(out),
        "drop_reasons": dict(drop_reasons),
        "human_exposure_overlap_in_untouched": 0,
        "xiv_overlap_in_untouched": 0,
    }
    # Hard assert overlap
    for r in out:
        assert str(r["q1_utterance_id"]) not in exposed_q1
        assert str(r["unit_id"]) not in exposed_unit
    return out, audit


def code_frame(candidates: list[dict]) -> list[dict]:
    coded = []
    for r in candidates:
        side = code_question_side(
            r.get("registered_question_from_chair"), r.get("q1_text")
        )
        item = dict(r)
        item.update(side)
        coded.append(item)
    return coded


def diversity_select(
    candidates: list[dict],
    *,
    n: int = VAL_N,
    seed: int = SEED_BINARY_VAL,
) -> tuple[list[dict], dict]:
    coded = code_frame(candidates)
    if len(coded) < n:
        raise RuntimeError(f"Need {n} fresh candidates; only {len(coded)} available")

    ordered = sorted(coded, key=lambda r: r["unit_id"])
    rng = random.Random(seed)
    rng.shuffle(ordered)

    ladders = [
        {"max_q": 2, "max_sit": 2, "max_topic": 5, "label": "targets_as_specified"},
        {"max_q": 3, "max_sit": 2, "max_topic": 5, "label": "relax_questioner_to_3"},
        {"max_q": 4, "max_sit": 2, "max_topic": 6, "label": "relax_questioner_to_4"},
        {"max_q": 99, "max_sit": 2, "max_topic": 6, "label": "relax_questioner_unlimited"},
        {"max_q": 99, "max_sit": 3, "max_topic": 8, "label": "relax_sitting_to_3"},
        {"max_q": 99, "max_sit": 99, "max_topic": 99, "label": "full_relaxation"},
    ]

    def try_select(max_q: int, max_sit: int, max_topic: int) -> list[dict]:
        selected: list[dict] = []
        selected_ids: set[str] = set()
        topic_counts: Counter[str] = Counter()
        form_set: set[str] = set()
        q_counts: Counter[str] = Counter()
        sit_counts: Counter[str] = Counter()

        def can_add(u: dict) -> bool:
            if u["unit_id"] in selected_ids:
                return False
            t = u["question_topic"]
            q = str(u.get("questioner_who") or "")
            s = str(u.get("session_id") or "")
            if topic_counts[t] >= max_topic:
                return False
            if q and q_counts[q] >= max_q:
                return False
            if s and sit_counts[s] >= max_sit:
                return False
            return True

        def add(u: dict) -> None:
            selected.append(u)
            selected_ids.add(u["unit_id"])
            topic_counts[u["question_topic"]] += 1
            form_set.add(u["question_form"])
            q = str(u.get("questioner_who") or "")
            s = str(u.get("session_id") or "")
            if q:
                q_counts[q] += 1
            if s:
                sit_counts[s] += 1

        # Open topics/forms
        for u in ordered:
            if len(selected) >= n:
                break
            if not can_add(u):
                continue
            adds_topic = u["question_topic"] not in topic_counts and len(topic_counts) < TARGET_MIN_TOPICS
            adds_form = u["question_form"] not in form_set and len(form_set) < TARGET_MIN_FORMS
            if len(selected) == 0 or adds_topic or adds_form:
                add(u)

        for u in ordered:
            if len(selected) >= n:
                break
            if u["unit_id"] in selected_ids:
                continue
            if u["question_topic"] in topic_counts:
                continue
            if can_add(u):
                add(u)

        for u in ordered:
            if len(selected) >= n:
                break
            if can_add(u):
                add(u)
        return selected

    used_ladder = None
    selected: list[dict] = []
    for ladder in ladders:
        selected = try_select(ladder["max_q"], ladder["max_sit"], ladder["max_topic"])
        used_ladder = ladder
        if len(selected) >= n:
            selected = selected[:n]
            break
    else:
        raise RuntimeError(f"Could not select {n} (got {len(selected)})")

    topics = Counter(u["question_topic"] for u in selected)
    forms = Counter(u["question_form"] for u in selected)
    questioners = Counter(str(u.get("questioner_who") or "") for u in selected)
    sittings = Counter(str(u.get("session_id") or "") for u in selected)
    legs = Counter(str(u.get("legislature") or "") for u in selected)

    meta = {
        "n": len(selected),
        "seed": seed,
        "seed_source_string": SEED_SOURCE_STRING,
        "seed_sha256": SEED_DIGEST,
        "seed_conversion_rule": SEED_CONVERSION,
        "ladder_used": used_ladder["label"] if used_ladder else None,
        "topics": dict(topics),
        "forms": dict(forms),
        "questioners": dict(questioners),
        "sittings": dict(sittings),
        "legislatures": dict(legs),
        "targets_achieved": {
            "min_topics_ge_4": len(topics) >= TARGET_MIN_TOPICS,
            "min_forms_ge_2": len(forms) >= TARGET_MIN_FORMS,
            "max_per_questioner_le_2": (not questioners)
            or max(questioners.values()) <= TARGET_MAX_PER_QUESTIONER,
            "max_per_sitting_le_2": (not sittings)
            or max(sittings.values()) <= TARGET_MAX_PER_SITTING,
        },
        "r1_not_inspected_for_selection": True,
        "outcome_balancing": False,
        "single_seed_no_cherry_pick": True,
    }
    return selected, meta


def write_artifacts(
    expanded: list[dict],
    untouched: list[dict],
    selected: list[dict],
    frame_audit: dict,
    select_meta: dict,
) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    frame_rows = []
    for r in code_frame(untouched):
        frame_rows.append(
            {
                "unit_id": r["unit_id"],
                "legislature": r["legislature"],
                "date": r["date"],
                "session_id": r["session_id"],
                "expediente": r.get("expediente"),
                "questioner_who": r.get("questioner_who"),
                "answerer_who": r.get("answerer_who"),
                "q1_utterance_id": r["q1_utterance_id"],
                "r1_utterance_id": r["r1_utterance_id"],
                "registered_question": str(r["registered_question_from_chair"]).strip(),
                "Q1": r["q1_text"],
                # R1 stored privately for packet build later; NOT used in selection
                "R1": r["r1_text"],
                "question_topic": r["question_topic"],
                "question_form": r["question_form"],
                "in_validation_sample_n12": r["unit_id"]
                in {x["unit_id"] for x in selected},
            }
        )
    frame_df = pd.DataFrame(frame_rows).sort_values("unit_id")
    frame_csv = OUT_DIR / "BINARY_VALIDATION_FRESH_FRAME.csv"
    frame_df.to_csv(frame_csv, index=False)

    # Selection audit: question-side only in public-facing projection
    audit_rows = []
    packet_rows = []
    for i, r in enumerate(selected, start=1):
        audit_rows.append(
            {
                "case_no": i,
                "unit_id": r["unit_id"],
                "legislature": r["legislature"],
                "date": r["date"],
                "session_id": r["session_id"],
                "expediente": r.get("expediente"),
                "questioner_who": r.get("questioner_who"),
                "answerer_who": r.get("answerer_who"),
                "q1_utterance_id": r["q1_utterance_id"],
                "r1_utterance_id": r["r1_utterance_id"],
                "question_topic": r["question_topic"],
                "question_form": r["question_form"],
                "purpose": "binary_direct_resolution_validation_v1",
                "exclusion_from_main_sampling": True,
                "not_reliability_evidence_until_returns": True,
            }
        )
        packet_rows.append(
            {
                "case_no": i,
                "unit_id": r["unit_id"],
                "registered_question": str(r["registered_question_from_chair"]).strip(),
                "Q1": r["q1_text"],
                "R1": r["r1_text"],
            }
        )

    audit_csv = OUT_DIR / "BINARY_VALIDATION_N12_AUDIT.csv"
    packet_csv = OUT_DIR / "BINARY_VALIDATION_N12_PACKET_BLINDED.csv"
    pd.DataFrame(audit_rows).to_csv(audit_csv, index=False)
    pd.DataFrame(packet_rows).to_csv(packet_csv, index=False)

    # Prospective gate lock
    gate = {
        "phase": "7A",
        "instrument": "direct_resolution_v1.0-draft",
        "locked_before_human_returns": True,
        "n_validation": VAL_N,
        "primary_metric": "cohen_kappa_binary_direct_resolution",
        "kappa_threshold": 0.67,
        "raw_agreement_threshold_n": 10,
        "raw_agreement_threshold_of": 12,
        "pass_rule": "kappa >= 0.67 AND raw_agreement >= 10/12",
        "fail_rule": "either criterion unmet",
        "automatic_further_round_on_fail": False,
        "threshold_optimisation_after_returns_forbidden": True,
        "round2_recoding_forbidden": True,
        "seed": SEED_BINARY_VAL,
        "seed_source_string": SEED_SOURCE_STRING,
        "seed_sha256": SEED_DIGEST,
        "annotator_docx_generated": False,
    }
    gate_path = OUT_DIR / "BINARY_VALIDATION_PROSPECTIVE_GATE.json"
    gate_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "phase": "7A",
        "created_on": datetime.now(timezone.utc).date().isoformat(),
        "n_expanded_oop_usable": len(expanded),
        "n_untouched_after_exclusions": len(untouched),
        "n_validation_selected": len(selected),
        "untouched_before_expansion": 4,
        "extractor": "binary_validation_extractor_v1_date_aware_pm_answerer",
        "seed": SEED_BINARY_VAL,
        "seed_source_string": SEED_SOURCE_STRING,
        "seed_sha256": SEED_DIGEST,
        "seed_conversion_rule": SEED_CONVERSION,
        "selection": select_meta,
        "frame_audit": frame_audit,
        "unit_ids_selected": [r["unit_id"] for r in selected],
        "private_artifacts": {
            "fresh_frame_csv": str(frame_csv.relative_to(PROJECT_ROOT)),
            "audit_csv": str(audit_csv.relative_to(PROJECT_ROOT)),
            "packet_csv": str(packet_csv.relative_to(PROJECT_ROOT)),
            "gate_json": str(gate_path.relative_to(PROJECT_ROOT)),
        },
        "annotator_docx_generated": False,
        "xiv_reply_labels_created": False,
        "ai_labels_created": False,
    }
    man_path = OUT_DIR / "BINARY_VALIDATION_MANIFEST.json"
    man_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Update seeds.yaml
    seeds = yaml.safe_load(SEEDS_YAML.read_text(encoding="utf-8"))
    seeds.setdefault("seeds", {})
    seeds["seeds"]["binary_validation_v1"] = SEED_BINARY_VAL
    seeds["status"] = "binary_validation_seed_locked_phase7a"
    note = (
        f" binary_validation_v1 = {SEED_BINARY_VAL} from '{SEED_SOURCE_STRING}'."
    )
    prev = str(seeds.get("notes") or "")
    if "binary_validation_v1" not in prev:
        seeds["notes"] = (prev.rstrip() + note).strip()
    SEEDS_YAML.write_text(
        yaml.safe_dump(seeds, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    # Markdown audit (no R1 content)
    untouched_coded = code_frame(untouched)
    t_topics = Counter(r["question_topic"] for r in untouched_coded)
    t_forms = Counter(r["question_form"] for r in untouched_coded)
    t_legs = Counter(r["legislature"] for r in untouched_coded)
    lines = [
        "# Fresh binary validation frame audit (Phase 7A)",
        "",
        f"**Recorded:** {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Expansion",
        "",
        "Extractor fix: sitting PM is date-aware (Rajoy before censure;",
        "Sánchez after). Opposition deputies who later become PM are no longer",
        "misclassified as the answerer.",
        "",
        f"- Untouched OOP before expansion: **4**",
        f"- Expanded usable OOP (reg+Q1+R1): **{len(expanded)}**",
        f"- Untouched after hard exclusions: **{len(untouched)}**",
        f"- Dropped as previously exposed / XIV / QA / Phase-0: "
        f"**{frame_audit['n_dropped']}**",
        f"- Human-exposure overlap in untouched frame: **0**",
        f"- XIV overlap in untouched frame: **0**",
        "",
        "### Untouched frame composition",
        "",
        f"- Legislatures: `{dict(t_legs)}`",
        f"- Topics: `{dict(t_topics)}`",
        f"- Forms: `{dict(t_forms)}`",
        "",
        "## Validation sample (N=12) — drawn, packets not issued",
        "",
        f"- Seed source: `{SEED_SOURCE_STRING}`",
        f"- Seed: `{SEED_BINARY_VAL}`",
        f"- Ladder: `{select_meta.get('ladder_used')}`",
        f"- Topics: `{select_meta.get('topics')}`",
        f"- Forms: `{select_meta.get('forms')}`",
        f"- Targets: `{select_meta.get('targets_achieved')}`",
        f"- R1 inspected for selection: **no**",
        f"- Annotator DOCX generated: **no**",
        "",
        "## Prospective gate (LOCKED before returns)",
        "",
        "- Cohen κ (binary) ≥ **0.67**",
        "- Raw agreement ≥ **10/12**",
        "- PASS only if both met; else FAIL and STOP (no automatic further round)",
        "- Thresholds not to be optimised after returns",
        "",
        "## Artifacts",
        "",
        f"- `{frame_csv.relative_to(PROJECT_ROOT)}`",
        f"- `{audit_csv.relative_to(PROJECT_ROOT)}`",
        f"- `{packet_csv.relative_to(PROJECT_ROOT)}`",
        f"- `{gate_path.relative_to(PROJECT_ROOT)}`",
        "",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "n_expanded": len(expanded),
        "n_untouched": len(untouched),
        "n_selected": len(selected),
        "seed": SEED_BINARY_VAL,
        "manifest": str(man_path),
    }


def main() -> dict:
    expanded = collect_expanded_oop_candidates()
    untouched, frame_audit = filter_all_human_exposure(expanded)
    # Near-duplicate within untouched: drop later duplicates by normalized Q1
    seen_q1n: set[str] = set()
    deduped = []
    for r in sorted(untouched, key=lambda x: x["unit_id"]):
        qn = normalize_text(r.get("q1_text"))
        if qn in seen_q1n:
            continue
        seen_q1n.add(qn)
        deduped.append(r)
    frame_audit["n_untouched_after_near_dup_q1"] = len(deduped)
    selected, select_meta = diversity_select(deduped, n=VAL_N, seed=SEED_BINARY_VAL)
    return write_artifacts(expanded, deduped, selected, frame_audit, select_meta)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
