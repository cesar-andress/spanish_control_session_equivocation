"""Build Calibration Round 2 (Phase 5B) — final planned calibration round.

Completely new out-of-pool units. No reply-status inspection.
Deterministic diversity-constrained draw under a fixed Round-2 seed.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from scse.build_calibration_round1 import (
    WINDOWS,
    collect_calibration_candidates,
    development_utterance_keys,
    filter_out_development,
)
from scse.config import PHASE0_PROBE_EXPEDIENTES
from scse.packet_validation import validate_packet_frame
from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR
from scse.question_side import code_question_side

SEED_SOURCE_STRING = (
    "spanish_control_session_equivocation|calibration_round2|fresh_diversity_draw"
)
SEED_DIGEST = hashlib.sha256(SEED_SOURCE_STRING.encode("utf-8")).hexdigest()
SEED_ROUND2 = int(SEED_DIGEST[:16], 16) % (2**31 - 1)
SEED_CONVERSION = "int(sha256(source_string).hexdigest()[:16], 16) % (2**31 - 1)"

CAL2_N = 20
UNIT_PREFIX_NOTE = "cal1_"  # same id scheme as Round 1 extractor

CAL_DIR = DATA_PRIVATE / "calibration" / "round2"
MANIFEST_YAML = PROTOCOL_DIR / "calibration_round2_manifest.yaml"
SEEDS_YAML = PROTOCOL_DIR / "seeds.yaml"

# Soft diversity targets (reported if not met)
TARGET_MIN_TOPICS = 4
TARGET_MAX_TOPIC_SHARE = 8
TARGET_MIN_FORMS = 2
TARGET_PREFER_ALL_FORMS = 3
TARGET_MAX_PER_QUESTIONER = 2
TARGET_MAX_PER_SITTING = 2


def normalize_text(text: object) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    s = unicodedata.normalize("NFKC", str(text))
    s = s.casefold()
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"[¿?¡!.,;:…\"'«»\-–—()/\[\]{}]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_round1_exclusions() -> dict:
    audit = DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_AUDIT.csv"
    pkt = DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_PACKET_BLINDED.csv"
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
    }


def load_development_exclusions() -> dict:
    audit = (
        DATA_PRIVATE
        / "development"
        / "out_of_pool"
        / "DEVELOPMENT_SET_AUDIT.csv"
    )
    pkt = (
        DATA_PRIVATE
        / "development"
        / "out_of_pool"
        / "DEVELOPMENT_PACKET_BLINDED.csv"
    )
    a = pd.read_csv(audit)
    p = pd.read_csv(pkt)
    return {
        "unit_ids": set(a["unit_id"].astype(str)),
        "q1_r1": development_utterance_keys(),
        "q1": set(a["q1_utterance_id"].astype(str)),
        "reg_norm": {normalize_text(t) for t in p["registered_question"]},
        "q1_norm": {normalize_text(t) for t in p["Q1"]},
    }


def load_xiv_and_qa_exclusions() -> dict:
    pool = pd.read_parquet(DATA_PRIVATE / "eligible_pool_full.parquet")
    xiv = pool[pool["legislature"] == "XIV"]
    qa = pd.read_csv(
        PROJECT_ROOT
        / "_internal"
        / "link_audit_private"
        / "PHASE2_LINKAGE_QA_HUMAN_VALIDATED.csv"
    )
    qa_exch = set(qa["exchange_id"].astype(str))
    qa_rows = pool[pool["exchange_id"].isin(qa_exch)]
    phase0 = pool[pool["expediente"].isin(PHASE0_PROBE_EXPEDIENTES)]
    return {
        "xiv_q1": set(xiv["q1_utterance_id"].astype(str)),
        "xiv_reg_norm": {normalize_text(t) for t in xiv["registered_question"]},
        "xiv_q1_norm": {normalize_text(t) for t in xiv["q1_text"]},
        "qa_q1": set(qa_rows["q1_utterance_id"].astype(str)),
        "qa_exp": set(qa["expediente"].astype(str)),
        "phase0_q1": set(phase0["q1_utterance_id"].astype(str)),
        "phase0_exp": set(PHASE0_PROBE_EXPEDIENTES),
    }


def filter_novelty(candidates: list[dict]) -> list[dict]:
    r1 = load_round1_exclusions()
    dev = load_development_exclusions()
    xq = load_xiv_and_qa_exclusions()
    out = []
    for r in candidates:
        uid = str(r["unit_id"])
        q1 = str(r["q1_utterance_id"])
        r1u = str(r["r1_utterance_id"])
        key = (q1, r1u)
        reg_n = normalize_text(r.get("registered_question_from_chair"))
        q1_n = normalize_text(r.get("q1_text"))
        exp = str(r.get("expediente") or "").strip()
        if uid in r1["unit_ids"] or uid in dev["unit_ids"]:
            continue
        if key in r1["q1_r1"] or key in dev["q1_r1"]:
            continue
        if q1 in r1["q1"] or q1 in dev["q1"]:
            continue
        if q1 in xq["xiv_q1"] or q1 in xq["qa_q1"] or q1 in xq["phase0_q1"]:
            continue
        if exp and (exp in xq["qa_exp"] or exp in xq["phase0_exp"]):
            continue
        if reg_n and (
            reg_n in r1["reg_norm"]
            or reg_n in dev["reg_norm"]
            or reg_n in xq["xiv_reg_norm"]
        ):
            continue
        if q1_n and (
            q1_n in r1["q1_norm"]
            or q1_n in dev["q1_norm"]
            or q1_n in xq["xiv_q1_norm"]
        ):
            continue
        out.append(r)
    return out


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


def diversity_select_round2(
    candidates: list[dict],
    *,
    n: int = CAL2_N,
    seed: int = SEED_ROUND2,
) -> tuple[list[dict], dict]:
    """Deterministic diversity-constrained draw.

    Ordering: sort by unit_id, shuffle with Random(seed).
    Selection walks the shuffled list once per attempt, keeping a unit iff it
    does not breach active caps. Caps start at the documented targets and are
    relaxed in a fixed order only if n cannot be reached.
    """
    coded = code_frame(candidates)
    if len(coded) < n:
        raise RuntimeError(f"Need {n} candidates; only {len(coded)} after novelty filter")

    ordered = sorted(coded, key=lambda r: r["unit_id"])
    rng = random.Random(seed)
    rng.shuffle(ordered)

    # Fixed relaxation ladder (document if used)
    ladders = [
        {"max_q": 2, "max_sit": 2, "max_topic": 8, "label": "targets_as_specified"},
        {"max_q": 3, "max_sit": 2, "max_topic": 8, "label": "relax_questioner_to_3"},
        {"max_q": 4, "max_sit": 2, "max_topic": 8, "label": "relax_questioner_to_4"},
        {"max_q": 5, "max_sit": 2, "max_topic": 8, "label": "relax_questioner_to_5"},
        {"max_q": 6, "max_sit": 2, "max_topic": 8, "label": "relax_questioner_to_6"},
        {"max_q": 99, "max_sit": 2, "max_topic": 8, "label": "relax_questioner_unlimited"},
        {"max_q": 99, "max_sit": 3, "max_topic": 8, "label": "relax_sitting_to_3"},
        {"max_q": 99, "max_sit": 99, "max_topic": 8, "label": "relax_sitting_unlimited"},
    ]

    def try_select(max_q: int, max_sit: int, max_topic: int) -> list[dict]:
        selected: list[dict] = []
        selected_ids: set[str] = set()
        topic_counts: Counter[str] = Counter()
        form_set: set[str] = set()
        q_counts: Counter[str] = Counter()
        sit_counts: Counter[str] = Counter()

        def can_add(u: dict, *, opening: bool) -> bool:
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
            if opening:
                # Prefer units that open a new topic or form while under target
                topics = set(topic_counts)
                forms = set(form_set)
                adds_topic = t not in topics and len(topics) < TARGET_MIN_TOPICS
                adds_form = u["question_form"] not in forms and len(forms) < TARGET_MIN_FORMS
                if len(selected) == 0:
                    return True
                return adds_topic or adds_form
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

        # Pass A — open diversity
        for u in ordered:
            if len(selected) >= n:
                break
            if can_add(u, opening=True):
                add(u)
            if (
                len(set(topic_counts)) >= TARGET_MIN_TOPICS
                and len(form_set) >= TARGET_MIN_FORMS
                and len(selected) >= TARGET_MIN_TOPICS
            ):
                # Enough opening; stop pass A early only if we already have
                # min topics and forms represented
                if len(set(topic_counts)) >= min(TARGET_MIN_TOPICS, 2) and len(
                    form_set
                ) >= TARGET_MIN_FORMS:
                    # Continue opening until we have at least 4 topics if possible
                    if len(set(topic_counts)) >= TARGET_MIN_TOPICS:
                        break

        # Continue opening for more topics if still short
        if len(set(topic_counts)) < TARGET_MIN_TOPICS:
            for u in ordered:
                if len(selected) >= n:
                    break
                if u["unit_id"] in selected_ids:
                    continue
                if u["question_topic"] in topic_counts:
                    continue
                if can_add(u, opening=False):
                    add(u)
                if len(set(topic_counts)) >= TARGET_MIN_TOPICS:
                    break

        # Pass B — fill under caps
        for u in ordered:
            if len(selected) >= n:
                break
            if can_add(u, opening=False):
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
        raise RuntimeError(
            f"Could not select {n} units even after full relaxation "
            f"(got {len(selected)})"
        )

    topics = Counter(u["question_topic"] for u in selected)
    forms = Counter(u["question_form"] for u in selected)
    questioners = Counter(str(u.get("questioner_who") or "") for u in selected)
    sittings = Counter(str(u.get("session_id") or "") for u in selected)
    legs = Counter(str(u.get("legislature") or "") for u in selected)

    achieved = {
        "min_topics_ge_4": len(topics) >= TARGET_MIN_TOPICS,
        "max_topic_share_le_8": max(topics.values()) <= TARGET_MAX_TOPIC_SHARE,
        "min_forms_ge_2": len(forms) >= TARGET_MIN_FORMS,
        "all_3_forms": len(forms) >= TARGET_PREFER_ALL_FORMS,
        "max_per_questioner_le_2": max(questioners.values()) <= TARGET_MAX_PER_QUESTIONER,
        "max_per_sitting_le_2": max(sittings.values()) <= TARGET_MAX_PER_SITTING,
        "multiple_legislatures": len(legs) >= 2,
    }
    missed = [k for k, v in achieved.items() if not v]

    summary = {
        "n": len(selected),
        "seed": seed,
        "seed_source_string": SEED_SOURCE_STRING,
        "seed_sha256": SEED_DIGEST,
        "seed_conversion_rule": SEED_CONVERSION,
        "selection_rule": (
            "Sort by unit_id; Random(seed).shuffle; two-pass diversity open then "
            "fill under caps; relax caps via fixed ladder if n unreachable"
        ),
        "ladder_used": used_ladder,
        "topics": dict(topics),
        "forms": dict(forms),
        "questioners": dict(questioners),
        "sittings": dict(sittings),
        "legislatures": dict(legs),
        "max_topic_share": int(max(topics.values())),
        "max_per_questioner": int(max(questioners.values())),
        "max_per_sitting": int(max(sittings.values())),
        "n_topics": len(topics),
        "n_forms": len(forms),
        "n_questioners": len(questioners),
        "n_sittings": len(sittings),
        "targets_achieved": achieved,
        "targets_missed": missed,
        "reply_labels_observed": False,
    }
    return selected, summary


def write_artifacts(selected: list[dict], pool: list[dict], summary: dict) -> dict:
    CAL_DIR.mkdir(parents=True, exist_ok=True)
    selected_ids = [r["unit_id"] for r in selected]

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
                "purpose": "calibration_round2_only",
                "exclusion_from_main_sampling": True,
                "reuse_main_forbidden": True,
                "final_calibration_round": True,
            }
        )
        packet_rows.append(
            {
                "case_no": i,
                "unit_id": r["unit_id"],
                "registered_question": str(
                    r["registered_question_from_chair"]
                ).strip(),
                "Q1": r["q1_text"],
                "R1": r["r1_text"],
            }
        )

    audit_path = CAL_DIR / "CALIBRATION_ROUND2_AUDIT.csv"
    packet_csv = CAL_DIR / "CALIBRATION_ROUND2_PACKET_BLINDED.csv"
    pd.DataFrame(audit_rows).to_csv(audit_path, index=False)
    pkt = pd.DataFrame(packet_rows)
    pkt.to_csv(packet_csv, index=False)
    validate_packet_frame(pkt[["unit_id", "registered_question", "Q1", "R1"]])

    div_path = CAL_DIR / "CALIBRATION_ROUND2_DIVERSITY.json"
    div_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    meta = {
        "phase": "5B",
        "round": 2,
        "created_on": datetime.now(timezone.utc).date().isoformat(),
        "n_units": len(selected),
        "seed_source_string": SEED_SOURCE_STRING,
        "seed_sha256": SEED_DIGEST,
        "seed_conversion_rule": SEED_CONVERSION,
        "seed": SEED_ROUND2,
        "final_planned_calibration_round": True,
        "round3_planned": False,
        "exclusion_from_main_sampling": True,
        "not_for_main_analysis": True,
        "unit_ids": selected_ids,
        "case_order": selected_ids,
        "diversity": summary,
        "private_artifacts": {
            "audit": str(audit_path.relative_to(PROJECT_ROOT)),
            "blinded_packet_csv": str(packet_csv.relative_to(PROJECT_ROOT)),
            "diversity": str(div_path.relative_to(PROJECT_ROOT)),
        },
        "human_packets": {
            "joint_review": (
                "_internal/calibration_round2/"
                "01_REVISION_CONJUNTA_CASOS_5_6_7_10.docx"
            ),
            "daniel": "_internal/calibration_round2/02_calibracion_ronda2_Daniel.docx",
            "jose_jaime": (
                "_internal/calibration_round2/02_calibracion_ronda2_Jose_Jaime.docx"
            ),
        },
        "codebook_version_at_draw": "0.3.0",
        "operative_clarification": (
            "Joint Round-1 boundary review completed immediately before "
            "independent Round-2 coding; v0.4 transcribed only after returns."
        ),
        "pool_eligible_n_before_draw": len(pool),
    }
    manifest_json = CAL_DIR / "CALIBRATION_ROUND2_MANIFEST.json"
    manifest_json.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    yaml_doc = {
        "status": "calibration_round2_drawn",
        "phase": "5B",
        "created_on": meta["created_on"],
        "n_units": CAL2_N,
        "seed": SEED_ROUND2,
        "seed_source_string": SEED_SOURCE_STRING,
        "seed_sha256": SEED_DIGEST,
        "seed_conversion_rule": SEED_CONVERSION,
        "final_planned_calibration_round": True,
        "round3_planned": False,
        "exclusion_from_main_sampling": True,
        "not_for_main_analysis": True,
        "unit_ids": selected_ids,
        "codebook_version_at_draw": "0.3.0",
        "private_dir": "_internal/data_private/calibration/round2/",
        "human_dir": "_internal/calibration_round2/",
        "diversity_ladder_used": summary["ladder_used"],
        "targets_missed": summary["targets_missed"],
        "notes": [
            "Outside XIV eligible population.",
            "No overlap with development, Round 1, Phase-0 probes, linkage QA, or XIV.",
            "Diversity from registered+Q1 only; no reply-status inspection.",
            "Independent Round-2 coding after joint review of Round-1 cases 5,6,7,10.",
            "No Round 3 planned by default.",
        ],
    }
    MANIFEST_YAML.write_text(
        yaml.safe_dump(yaml_doc, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Update seeds.yaml — add calibration_round2 without changing Round-1 seed
    seeds = yaml.safe_load(SEEDS_YAML.read_text(encoding="utf-8"))
    seeds["status"] = "calibration_round1_and_round2_seeds_set"
    seeds.setdefault("seeds", {})
    seeds["seeds"]["calibration"] = 2071684612  # Round 1 unchanged
    seeds["seeds"]["calibration_round2"] = SEED_ROUND2
    seeds["notes"] = (
        "calibration = Round 1 seed 2071684612; "
        f"calibration_round2 = {SEED_ROUND2} from "
        f"'{SEED_SOURCE_STRING}'. main_sample and bootstrap remain null."
    )
    SEEDS_YAML.write_text(
        yaml.safe_dump(seeds, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    return {
        "audit": str(audit_path),
        "packet": str(packet_csv),
        "manifest_json": str(manifest_json),
        "manifest_yaml": str(MANIFEST_YAML),
        "diversity": str(div_path),
        "summary": summary,
        "packet_sha256": hashlib.sha256(packet_csv.read_bytes()).hexdigest(),
    }


def build() -> dict:
    base = filter_out_development(collect_calibration_candidates())
    pool = filter_novelty(base)
    selected, summary = diversity_select_round2(pool, n=CAL2_N, seed=SEED_ROUND2)
    info = write_artifacts(selected, pool, summary)
    return info


def main() -> int:
    info = build()
    print(json.dumps({"seed": SEED_ROUND2, **info["summary"]}, indent=2, ensure_ascii=False))
    print("packet", info["packet"])
    print("packet_sha256", info["packet_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
