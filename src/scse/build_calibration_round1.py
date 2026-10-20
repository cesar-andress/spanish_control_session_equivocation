"""Build Calibration Round 1 (Phase 5A).

Out-of-pool PM control exchanges only. Deterministic seed from documented
string. No XIV main units. No development overlap. No label inspection.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from scse.build_development_set import (
    PM_FORMULA_DEV_RE,
    _extract_registered,
    _is_pm_formula_chair,
    iter_session_files,
)
from scse.extract_exchanges import (
    EXPEDIENTE_RE,
    RawExchange,
    _is_chair,
    _notes_expediente,
    parse_session_utterances,
)
from scse.packet_validation import validate_packet_frame
from scse.paths import DATA_PRIVATE, PROTOCOL_DIR, PROJECT_ROOT

# Documented seed derivation (do not change after Round 1 starts)
SEED_SOURCE_STRING = (
    "spanish_control_session_equivocation|calibration_round1|reply_status_v0.3"
)
SEED_DIGEST = hashlib.sha256(SEED_SOURCE_STRING.encode("utf-8")).hexdigest()
# Conversion: first 16 hex digits as integer, reduced modulo 2^31-1 for RNG use
SEED_ROUND1 = int(SEED_DIGEST[:16], 16) % (2**31 - 1)

CAL1_N = 20
UNIT_PREFIX = "cal1_"

# Out-of-pool windows structurally comparable to PM oral control (not XIV)
WINDOWS: list[tuple[str, date, date]] = [
    ("X", date(2015, 1, 1), date(2015, 12, 31)),
    ("XI", date(2016, 1, 13), date(2016, 5, 2)),
    ("XII_pre", date(2016, 7, 19), date(2018, 6, 1)),
    ("XII_post", date(2018, 6, 2), date(2019, 5, 20)),
    ("XIII", date(2019, 5, 21), date(2019, 12, 2)),
]

PM_WHO_SET = frozenset(
    {
        "#PedroSánchezPérezCastejón",
        "#MarianoRajoyBrey",
    }
)

XIV_START = date(2019, 12, 3)
XIV_END = date(2023, 2, 23)

CAL_DIR = DATA_PRIVATE / "calibration" / "round1"
MANIFEST_YAML = PROTOCOL_DIR / "calibration_round1_manifest.yaml"
SEEDS_YAML = PROTOCOL_DIR / "seeds.yaml"


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_cal_unit_id(r: RawExchange) -> str:
    base = f"{r.legislature}|{r.session_id}|{r.q1_utterance_id}|{r.r1_utterance_id}"
    return UNIT_PREFIX + _sha256_text(base)[:16]


def extract_pm_cal_exchanges(path: Path, *, legislature: str) -> list[RawExchange]:
    """Q1–R1 extractor for any listed PM outside XIV."""
    from scse.paths import PARLAMINT_CACHE

    path = path.resolve()
    session_id, session_date, utts = parse_session_utterances(path)
    if not session_date:
        return []
    d = date.fromisoformat(str(session_date)[:10])
    if XIV_START <= d <= XIV_END:
        return []

    def _document_relpath(p: Path) -> str:
        try:
            return str(p.resolve().relative_to(PARLAMINT_CACHE.resolve()))
        except ValueError:
            return p.name

    exchanges: list[RawExchange] = []
    used_q1: set[str] = set()

    for i, u in enumerate(utts):
        if not _is_chair(u) or not _is_pm_formula_chair(u.text):
            continue
        reg_q, exp = _extract_registered(u.text)
        q_idx = None
        r_idx = None
        for j in range(i + 1, min(i + 12, len(utts))):
            uj = utts[j]
            if _is_chair(uj):
                if _is_pm_formula_chair(uj.text):
                    break
                continue
            if q_idx is None:
                if (uj.who or "") in PM_WHO_SET:
                    break
                q_idx = j
                continue
            if utts[q_idx].who == uj.who:
                continue
            if (uj.who or "") in PM_WHO_SET:
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
        notes = ["calibration_extractor_v1"]
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


def collect_calibration_candidates() -> list[dict]:
    rows: list[dict] = []
    for leg, start, end in WINDOWS:
        for path in iter_session_files(start, end):
            for r in extract_pm_cal_exchanges(path, legislature=leg):
                d = asdict(r)
                d["unit_id"] = make_cal_unit_id(r)
                rows.append(d)
    # Require registered + Q1 + R1 (v0.3 packet rule)
    usable = []
    for r in rows:
        reg = str(r.get("registered_question_from_chair") or "").strip()
        q1 = str(r.get("q1_text") or "").strip()
        r1 = str(r.get("r1_text") or "").strip()
        if reg and q1 and r1:
            usable.append(r)
    by_id = {r["unit_id"]: r for r in usable}
    return list(by_id.values())


def load_development_unit_bases() -> set[str]:
    """Development used dev_<hash16> from same utterance key without prefix swap.

    Exclude any calibration candidate that shares session+utterance ids with
    development, and also exclude by matching q1/r1 utterance ids.
    """
    path = PROTOCOL_DIR / "development_set_manifest.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return set(data["unit_ids"])


def development_utterance_keys() -> set[tuple[str, str]]:
    audit = (
        DATA_PRIVATE
        / "development"
        / "out_of_pool"
        / "DEVELOPMENT_SET_AUDIT.csv"
    )
    df = pd.read_csv(audit)
    return set(zip(df["q1_utterance_id"].astype(str), df["r1_utterance_id"].astype(str)))


def filter_out_development(candidates: list[dict]) -> list[dict]:
    keys = development_utterance_keys()
    out = []
    for r in candidates:
        k = (str(r["q1_utterance_id"]), str(r["r1_utterance_id"]))
        if k in keys:
            continue
        out.append(r)
    return out


def select_round1(candidates: list[dict], n: int = CAL1_N, seed: int = SEED_ROUND1) -> list[dict]:
    if len(candidates) < n:
        raise RuntimeError(
            f"Need {n} calibration candidates; only {len(candidates)} available"
        )
    ordered = sorted(candidates, key=lambda r: r["unit_id"])
    rng = random.Random(seed)
    rng.shuffle(ordered)
    return ordered[:n]


def write_artifacts(selected: list[dict], pool: list[dict]) -> dict:
    CAL_DIR.mkdir(parents=True, exist_ok=True)
    selected_ids = [r["unit_id"] for r in selected]
    remaining = [r for r in pool if r["unit_id"] not in set(selected_ids)]

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
                "answerer_who": r.get("answerer_who"),
                "q1_utterance_id": r["q1_utterance_id"],
                "r1_utterance_id": r["r1_utterance_id"],
                "purpose": "calibration_round1_only",
                "exclusion_from_main_sampling": True,
                "reuse_round2_forbidden": True,
                "reuse_main_forbidden": True,
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

    audit_path = CAL_DIR / "CALIBRATION_ROUND1_AUDIT.csv"
    packet_csv = CAL_DIR / "CALIBRATION_ROUND1_PACKET_BLINDED.csv"
    pd.DataFrame(audit_rows).to_csv(audit_path, index=False)
    pkt = pd.DataFrame(packet_rows)
    pkt.to_csv(packet_csv, index=False)
    validate_packet_frame(pkt[["unit_id", "registered_question", "Q1", "R1"]])

    remaining_path = CAL_DIR / "CALIBRATION_REMAINING_POOL_IDS.json"
    remaining_path.write_text(
        json.dumps(
            {
                "n": len(remaining),
                "reserved_for": "calibration_round2_or_later",
                "unit_ids": sorted(r["unit_id"] for r in remaining),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    meta = {
        "phase": "5A",
        "round": 1,
        "created_on": datetime.now(timezone.utc).date().isoformat(),
        "n_units": len(selected),
        "seed_source_string": SEED_SOURCE_STRING,
        "seed_sha256": SEED_DIGEST,
        "seed_conversion_rule": (
            "int(sha256(source_string).hexdigest()[:16], 16) % (2**31 - 1)"
        ),
        "seed": SEED_ROUND1,
        "selection_rule": (
            "Sort eligible candidates by unit_id; "
            "random.Random(seed).shuffle; take first 20"
        ),
        "source": (
            "ParlaMint-ES 5.0 PM FORMULA exchanges outside XIV "
            "(X 2015, XI, XII pre/post, XIII); answerer Sánchez or Rajoy"
        ),
        "exclusion_from_main_sampling": True,
        "not_for_main_analysis": True,
        "development_overlap_forbidden": True,
        "xiv_overlap_forbidden": True,
        "unit_ids": selected_ids,
        "case_order": selected_ids,
        "private_artifacts": {
            "audit": str(audit_path.relative_to(PROJECT_ROOT)),
            "blinded_packet_csv": str(packet_csv.relative_to(PROJECT_ROOT)),
            "remaining_pool": str(remaining_path.relative_to(PROJECT_ROOT)),
        },
        "human_packets": {
            "daniel": "_internal/calibration_round1/calibracion_ronda1_Daniel.docx",
            "jose_jaime": (
                "_internal/calibration_round1/calibracion_ronda1_Jose_Jaime.docx"
            ),
        },
        "codebook_version": "0.3.0",
        "pool_eligible_n_before_draw": len(pool),
        "remaining_n_after_draw": len(remaining),
    }
    manifest_json = CAL_DIR / "CALIBRATION_ROUND1_MANIFEST.json"
    manifest_json.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    yaml_doc = {
        "status": "calibration_round1_drawn",
        "phase": "5A",
        "created_on": meta["created_on"],
        "n_units": CAL1_N,
        "seed": SEED_ROUND1,
        "seed_source_string": SEED_SOURCE_STRING,
        "seed_sha256": SEED_DIGEST,
        "seed_conversion_rule": meta["seed_conversion_rule"],
        "exclusion_from_main_sampling": True,
        "not_for_main_analysis": True,
        "reuse_round2_forbidden": True,
        "unit_ids": selected_ids,
        "codebook_version": "0.3.0",
        "private_dir": "_internal/data_private/calibration/round1/",
        "human_dir": "_internal/calibration_round1/",
        "source_windows": [
            {"legislature": leg, "start": s.isoformat(), "end": e.isoformat()}
            for leg, s, e in WINDOWS
        ],
        "notes": [
            "Outside XIV eligible population.",
            "No overlap with the 15 development cases (utterance-id check).",
            "Registered + oral + first response required and displayed.",
            "Independent coding only until both packets returned.",
        ],
    }
    MANIFEST_YAML.write_text(
        yaml.safe_dump(yaml_doc, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Update seeds.yaml — only calibration becomes non-null
    seeds = yaml.safe_load(SEEDS_YAML.read_text(encoding="utf-8"))
    seeds["seeds"]["calibration"] = SEED_ROUND1
    seeds["status"] = "calibration_round1_seed_set"
    seeds["notes"] = (
        "calibration seed = Round 1 only "
        f"(derived from {SEED_SOURCE_STRING!r}). "
        "main_sample and bootstrap remain null. "
        "unit_test seed (42) is non-scientific."
    )
    SEEDS_YAML.write_text(
        yaml.safe_dump(seeds, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    return {
        "meta": meta,
        "packet_csv": packet_csv,
        "audit_path": audit_path,
        "manifest_json": manifest_json,
        "manifest_yaml": MANIFEST_YAML,
    }


def main() -> int:
    candidates = collect_calibration_candidates()
    pool = filter_out_development(candidates)
    selected = select_round1(pool)
    info = write_artifacts(selected, pool)
    print(json.dumps(
        {
            "n_candidates_with_registered": len(candidates),
            "n_after_dev_exclusion": len(pool),
            "n_selected": len(selected),
            "seed": SEED_ROUND1,
            "packet": str(info["packet_csv"]),
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
