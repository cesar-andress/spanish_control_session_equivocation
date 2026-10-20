"""Link ParlaMint PM exchanges to Congreso registered-question records."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field

from scse.config import PHASE0_PROBE_EXPEDIENTES, PM_WHO
from scse.extract_exchanges import RawExchange
from scse.ingest_congreso import CongresoInitiative


def _norm_name(s: str | None) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z\s]", " ", s)
    return " ".join(s.split())


def _who_to_name_tokens(who: str | None) -> set[str]:
    if not who:
        return set()
    w = who.lstrip("#")
    parts = re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", w)
    if not parts:
        parts = re.findall(r"[A-Za-zÁÉÍÓÚáéíóúñÑ]+", w)
    return {_norm_name(p) for p in parts if len(p) > 1}


def names_match(who: str | None, congreso_name: str | None) -> bool:
    tokens = _who_to_name_tokens(who)
    cn = _norm_name(congreso_name)
    if not tokens or not cn:
        return False
    cn_tokens = set(cn.split())
    hits = sum(1 for t in tokens if t in cn_tokens or t in cn)
    if hits >= 2:
        return True
    return any(len(t) >= 6 and t in cn for t in tokens)


@dataclass
class LinkedExchange:
    exchange_id: str
    raw: RawExchange
    congreso: CongresoInitiative | None
    link_status: str
    link_evidence: dict = field(default_factory=dict)
    registered_question: str | None = None
    questioner_name: str | None = None
    parliamentary_group: str | None = None
    ds_id: str | None = None
    ds_page: str | None = None
    exclusion_reason: str | None = None
    eligible: bool = False
    exclude_from_sampling: bool = False
    sampling_exclusion_reason: str | None = None

    def to_row(self) -> dict:
        r = self.raw
        return {
            "exchange_id": self.exchange_id,
            "expediente": r.expediente,
            "legislature": r.legislature,
            "date": r.date,
            "session_id": r.session_id,
            "ds_id": self.ds_id,
            "ds_page": self.ds_page,
            "questioner_id": r.questioner_who,
            "questioner_name": self.questioner_name,
            "parliamentary_group": self.parliamentary_group,
            "answerer_id": r.answerer_who,
            "answerer_name": "Pedro Sánchez Pérez-Castejón",
            "registered_question": self.registered_question,
            "q1_text": r.q1_text,
            "r1_text": r.r1_text,
            "q2_text": r.q2_text,
            "r2_text": r.r2_text,
            "parlamint_document_id": r.session_id,
            "q1_utterance_id": r.q1_utterance_id,
            "r1_utterance_id": r.r1_utterance_id,
            "q2_utterance_id": r.q2_utterance_id,
            "r2_utterance_id": r.r2_utterance_id,
            "link_status": self.link_status,
            "link_evidence": json.dumps(self.link_evidence, ensure_ascii=False, sort_keys=True),
            "source_version": "ParlaMint-ES-5.0",
            "eligible": self.eligible,
            "exclusion_reason": self.exclusion_reason,
            "exclude_from_sampling": self.exclude_from_sampling,
            "sampling_exclusion_reason": self.sampling_exclusion_reason,
            "document_path": r.document_path,
            "chair_announcement": r.chair_announcement,
            "congreso_url": self.congreso.source_url if self.congreso else None,
        }


def make_exchange_id(raw: RawExchange) -> str:
    # Prefer utterance-stable id (expediente may be corrected during linkage)
    base = f"{raw.legislature}|{raw.session_id}|{raw.q1_utterance_id}"
    return "ex_" + hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]


def _initiatives_for_date(
    date: str,
    tei_exps_by_date: dict[str, set[str]],
    initiatives: dict[str, CongresoInitiative],
    gap_ids_by_date: dict[str, set[str]] | None = None,
) -> list[CongresoInitiative]:
    ids = set(tei_exps_by_date.get(date, set()))
    if gap_ids_by_date:
        ids |= set(gap_ids_by_date.get(date, set()))
    return [initiatives[i] for i in sorted(ids) if i in initiatives]


def link_exchanges(
    raw_exchanges: list[RawExchange],
    initiatives: dict[str, CongresoInitiative],
    *,
    tei_exps_by_date: dict[str, set[str]] | None = None,
    gap_ids_by_date: dict[str, set[str]] | None = None,
) -> list[LinkedExchange]:
    """Link by sitting date + questioner name; TEI expediente is supporting evidence only."""
    tei_exps_by_date = tei_exps_by_date or {}
    gap_ids_by_date = gap_ids_by_date or {}
    out: list[LinkedExchange] = []
    used_exp: dict[str, str] = {}

    # Group raw by date for conflict detection
    by_date: dict[str, list[RawExchange]] = defaultdict(list)
    for raw in raw_exchanges:
        by_date[raw.date].append(raw)

    for raw in raw_exchanges:
        eid = make_exchange_id(raw)
        tei_exp = raw.expediente
        day_inits = _initiatives_for_date(
            raw.date, tei_exps_by_date, initiatives, gap_ids_by_date
        )
        name_hits = [
            c for c in day_inits if names_match(raw.questioner_who, c.questioner_name)
        ]
        # Prefer unused expediente
        name_hits_free = [c for c in name_hits if c.expediente not in used_exp]

        evidence: dict = {
            "tei_expediente": tei_exp,
            "tei_date": raw.date,
            "tei_questioner_who": raw.questioner_who,
            "tei_has_chair_registered": bool(raw.registered_question_from_chair),
            "answerer_who": raw.answerer_who,
            "day_initiative_n": len(day_inits),
            "name_hit_expedientes": [c.expediente for c in name_hits],
        }

        cong = None
        link_status = "unlinked"
        exclusion = None
        registered = raw.registered_question_from_chair

        if len(name_hits_free) == 1:
            cong = name_hits_free[0]
            raw.expediente = cong.expediente
            link_status = "exact" if tei_exp == cong.expediente else "high_confidence"
            evidence["rule"] = (
                "date_questioner_unique"
                if tei_exp != cong.expediente
                else "tei_expediente_confirmed_by_name"
            )
            evidence["name_match"] = True
        elif len(name_hits_free) > 1:
            # If TEI expediente is among name hits, take it
            tei_hit = [c for c in name_hits_free if c.expediente == tei_exp]
            if len(tei_hit) == 1:
                cong = tei_hit[0]
                raw.expediente = cong.expediente
                link_status = "exact"
                evidence["rule"] = "tei_expediente_disambiguates_name_hits"
                evidence["name_match"] = True
            else:
                link_status = "ambiguous"
                exclusion = "multiple_same_questioner_on_date"
                evidence["rule"] = "multiple_name_matches_same_date"
        elif tei_exp and tei_exp in initiatives:
            # TEI expediente present but name does not match → do not trust TEI id
            cong_tei = initiatives[tei_exp]
            evidence["congreso_questioner_for_tei_exp"] = cong_tei.questioner_name
            evidence["name_match"] = False
            if raw.registered_question_from_chair:
                link_status = "high_confidence"
                evidence["rule"] = "chair_formula_anchor_tei_expediente_rejected"
                cong = None
                raw.expediente = None
            else:
                link_status = "unlinked"
                exclusion = "tei_expediente_name_mismatch"
                evidence["rule"] = "tei_expediente_rejected_no_chair_anchor"
                raw.expediente = None
        elif raw.registered_question_from_chair:
            link_status = "high_confidence"
            evidence["rule"] = "chair_formula_without_congreso_match"
            raw.expediente = None
        else:
            link_status = "unlinked"
            exclusion = "no_congreso_name_match"
            evidence["rule"] = "no_structured_link"
            raw.expediente = None

        if cong is not None:
            registered = cong.title or registered
            evidence["congreso_title"] = cong.title
            evidence["congreso_questioner"] = cong.questioner_name
            evidence["congreso_group"] = cong.parliamentary_group
            evidence["congreso_ds"] = cong.ds_references
            used_exp[cong.expediente] = eid

        qname = cong.questioner_name if cong else None
        group = cong.parliamentary_group if cong else None
        ds_id = cong.ds_references[0] if cong and cong.ds_references else None

        eligible = link_status in {"exact", "high_confidence"}
        if eligible:
            if not registered or not str(registered).strip():
                eligible = False
                exclusion = "empty_registered_question"
            elif not (raw.q1_text or "").strip() or not (raw.r1_text or "").strip():
                eligible = False
                exclusion = "incomplete_transcription"
            elif raw.answerer_who != PM_WHO:
                eligible = False
                exclusion = "ambiguous_answerer"

        exclude_sampling = False
        samp_reason = None
        if raw.expediente and raw.expediente in PHASE0_PROBE_EXPEDIENTES:
            exclude_sampling = True
            samp_reason = "phase0_feasibility_probe"

        out.append(
            LinkedExchange(
                exchange_id=eid,
                raw=raw,
                congreso=cong,
                link_status=link_status,
                link_evidence=evidence,
                registered_question=registered,
                questioner_name=qname,
                parliamentary_group=group,
                ds_id=ds_id,
                ds_page=None,
                exclusion_reason=exclusion if not eligible else None,
                eligible=eligible,
                exclude_from_sampling=exclude_sampling,
                sampling_exclusion_reason=samp_reason,
            )
        )
    return out


def main() -> int:
    print("link_questions: use scse.build_pool")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
