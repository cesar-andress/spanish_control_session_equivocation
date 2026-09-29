"""Extract PM control-session exchanges from ParlaMint-ES TEI."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

from lxml import etree

from scse.config import (
    LEGISLATURE,
    LEGISLATURE_START,
    PARLAMINT_COVERAGE_END,
    PM_WHO,
)
from scse.paths import PARLAMINT_CACHE

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

EXPEDIENTE_RE = re.compile(r"180/\d{6}")
PM_FORMULA_RE = re.compile(
    r"QUE\s+FORMULA\s+AL\s+SE[NÑ]OR\s+PRESIDENTE\s+DEL\s+GOBIERNO\s*:\s*(.+?)"
    r"(?:Número de expediente\s*180/\d{6}|$)",
    re.I | re.S,
)
PM_ONLY_FORMULA_RE = re.compile(
    r"FORMULA\s+AL\s+SE[NÑ]OR\s+PRESIDENTE\s+DEL\s+GOBIERNO",
    re.I,
)
PM_FLOOR_RE = re.compile(
    r"Se[nñ]or\s+presidente\s+del\s+Gobierno\.?\s*$",
    re.I,
)


@dataclass
class Utterance:
    uid: str
    who: str | None
    ana: str
    text: str
    notes: list[str]
    order: int


@dataclass
class RawExchange:
    session_id: str
    document_path: str
    date: str
    legislature: str
    expediente: str | None
    registered_question_from_chair: str | None
    questioner_who: str | None
    answerer_who: str | None
    q1_utterance_id: str
    r1_utterance_id: str
    q2_utterance_id: str | None = None
    r2_utterance_id: str | None = None
    q1_text: str = ""
    r1_text: str = ""
    q2_text: str | None = None
    r2_text: str | None = None
    chair_announcement: str | None = None
    extraction_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _local_id(el: etree._Element) -> str:
    return el.get(XML_ID) or ""


def _utt_text_and_notes(u: etree._Element) -> tuple[str, list[str]]:
    """Keep inline note text (e.g. party abbreviations); collect note strings separately."""
    notes = [
        " ".join("".join(n.itertext()).split())
        for n in u.xpath(".//tei:note", namespaces=TEI_NS)
    ]
    raw = " ".join("".join(u.itertext()).split())
    # Drop expediente boilerplate from spoken/announcement display text
    text = EXPEDIENTE_RE.sub("", raw)
    text = re.sub(r"Número de expediente\s*", "", text, flags=re.I)
    text = " ".join(text.split()).strip()
    return text, notes


def parse_session_utterances(path: Path) -> tuple[str, str, list[Utterance]]:
    path = path.resolve()
    root = etree.parse(str(path)).getroot()
    session_id = path.stem
    m = re.search(r"ParlaMint-ES_(\d{4}-\d{2}-\d{2})", path.name)
    session_date = m.group(1) if m else ""
    utts: list[Utterance] = []
    for i, u in enumerate(root.xpath("//tei:u", namespaces=TEI_NS)):
        text, notes = _utt_text_and_notes(u)
        utts.append(
            Utterance(
                uid=_local_id(u),
                who=u.get("who"),
                ana=u.get("ana") or "",
                text=text,
                notes=notes,
                order=i,
            )
        )
    return session_id, session_date, utts


def _is_chair(u: Utterance) -> bool:
    return "#chair" in (u.ana or "")


def _is_pm(u: Utterance) -> bool:
    return (u.who or "") == PM_WHO


def _notes_expediente(notes: list[str]) -> str | None:
    for note in notes:
        m = EXPEDIENTE_RE.search(note)
        if m:
            return m.group(0)
    return None


def _extract_registered_from_formula(text: str) -> tuple[str | None, str | None]:
    if not PM_ONLY_FORMULA_RE.search(text):
        return None, None
    m = PM_FORMULA_RE.search(text)
    question = None
    if m:
        question = " ".join((m.group(1) or "").split()).strip(" -–")
        question = question or None
    exp = EXPEDIENTE_RE.search(text)
    return question, exp.group(0) if exp else None


def _is_pm_floor_cue(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    if "FORMULA" in t.upper():
        return False
    return bool(PM_FLOOR_RE.search(t))


def _prev_non_chair(utts: list[Utterance], idx: int) -> Utterance | None:
    for j in range(idx - 1, max(-1, idx - 8), -1):
        if not _is_chair(utts[j]):
            return utts[j]
    return None


def _prev_other_speaker(utts: list[Utterance], idx: int, who: str | None) -> Utterance | None:
    """Previous non-chair speaker whose who differs from ``who`` (skip split turns)."""
    for j in range(idx - 1, max(-1, idx - 12), -1):
        if _is_chair(utts[j]):
            continue
        if utts[j].who == who:
            continue
        return utts[j]
    return None


def _lookback_announcement(
    utts: list[Utterance], q_idx: int
) -> tuple[str | None, str | None, str | None]:
    reg_q = exp = ann = None
    for j in range(q_idx - 1, max(-1, q_idx - 8), -1):
        uj = utts[j]
        if not _is_chair(uj):
            if _is_pm(uj):
                break
            continue
        rq, e = _extract_registered_from_formula(uj.text)
        ne = _notes_expediente(uj.notes)
        if rq or e or ne or PM_ONLY_FORMULA_RE.search(uj.text):
            reg_q = rq or reg_q
            exp = e or ne or exp
            ann = uj.text
            if reg_q or exp:
                break
        if re.search(r"Pregunta\s+del\s+(?:diputad|señor|señora)", uj.text, re.I):
            ann = ann or uj.text
            ne = _notes_expediente(uj.notes)
            exp = exp or ne
    return reg_q, exp, ann


def _collect_exp_near(utts: list[Utterance], start: int, end: int) -> str | None:
    for j in range(max(0, start), min(end + 1, len(utts))):
        e = _notes_expediente(utts[j].notes)
        if e:
            return e
        m = EXPEDIENTE_RE.search(utts[j].text)
        if m:
            return m.group(0)
    return None


def _document_relpath(path: Path) -> str:
    path = path.resolve()
    cache = PARLAMINT_CACHE.resolve()
    try:
        return str(path.relative_to(cache))
    except ValueError:
        return path.name


_PM_SECTION_START = re.compile(
    r"Preguntas\s+dirigidas\s+al\s+se[nñ]or\s+presidente\s+del\s+Gobierno",
    re.I,
)
_OTHER_SECTION_START = re.compile(
    r"Preguntas\s+dirigidas\s+a\s+l[ao]\s+se[nñ]or[ao]\s+"
    r"(?:vicepresidente|vicepresidenta|ministro|ministra)",
    re.I,
)


def extract_pm_exchanges_from_session(path: Path) -> list[RawExchange]:
    path = path.resolve()
    session_id, session_date, utts = parse_session_utterances(path)
    if not session_date:
        return []
    d = date.fromisoformat(session_date)
    if d < LEGISLATURE_START or d > PARLAMINT_COVERAGE_END:
        return []

    # Restrict to the oral-questions block addressed to the PM when the
    # chair marks that section; otherwise allow FORMULA-anchored exchanges only.
    in_pm_section = False
    section_flags: list[bool] = []
    for u in utts:
        if _is_chair(u) and _PM_SECTION_START.search(u.text):
            in_pm_section = True
        if _is_chair(u) and _OTHER_SECTION_START.search(u.text):
            in_pm_section = False
        section_flags.append(in_pm_section)

    exchanges: list[RawExchange] = []
    used_q1: set[str] = set()

    for i, u in enumerate(utts):
        if not _is_chair(u) or not _is_pm_floor_cue(u.text):
            continue

        q_idx = None
        for j in range(i - 1, max(-1, i - 4), -1):
            if _is_chair(utts[j]):
                continue
            if _is_pm(utts[j]):
                break
            q_idx = j
            break
        if q_idx is None or utts[q_idx].uid in used_q1:
            continue

        # Collapse split questioner turns (chair "Silencio" between fragments)
        block_start = q_idx
        while True:
            prev_frag = _prev_non_chair(utts, block_start)
            if prev_frag is not None and prev_frag.who == utts[q_idx].who:
                block_start = prev_frag.order
                continue
            break
        q1_idx = block_start
        if utts[q1_idx].uid in used_q1:
            continue

        # Skip réplica: before this questioner block is a PM answering the same who
        prev_before = _prev_non_chair(utts, q1_idx)
        if prev_before is not None and _is_pm(prev_before):
            earlier_q = _prev_other_speaker(utts, prev_before.order, PM_WHO)
            if earlier_q is not None and earlier_q.who == utts[q1_idx].who:
                continue

        r1_idx = None
        for j in range(i + 1, min(i + 4, len(utts))):
            if _is_chair(utts[j]):
                continue
            if _is_pm(utts[j]):
                r1_idx = j
                break
            break
        if r1_idx is None:
            continue

        reg_q, exp_ann, chair_ann = _lookback_announcement(utts, q1_idx)

        # Eligibility: inside PM oral-question section OR explicit PM FORMULA
        has_formula = bool(reg_q) or bool(
            chair_ann and PM_ONLY_FORMULA_RE.search(chair_ann)
        )
        has_pregunta_line = bool(
            chair_ann
            and re.search(r"Pregunta\s+del\s+(?:diputad|señor|señora)", chair_ann, re.I)
        )
        if not (section_flags[q1_idx] or has_formula):
            continue
        if not (has_formula or has_pregunta_line or section_flags[q1_idx]):
            continue
        # Require a question announcement when section tracking is weak
        if not section_flags[q1_idx] and not (has_formula or has_pregunta_line):
            continue

        q2_idx = r2_idx = None
        questioner_who = utts[q1_idx].who
        for j in range(r1_idx + 1, min(r1_idx + 10, len(utts))):
            uj = utts[j]
            if _is_chair(uj):
                if PM_ONLY_FORMULA_RE.search(uj.text) or re.search(
                    r"FORMULA\s+AL\s+SE[NÑ]OR|FORMULA\s+A\s+LA\s+SE[NÑ]ORA",
                    uj.text,
                    re.I,
                ):
                    break
                continue
            if uj.who == questioner_who and q2_idx is None:
                q2_idx = j
                continue
            if q2_idx is not None and uj.who == questioner_who:
                continue  # split réplica fragments
            if q2_idx is not None and _is_pm(uj):
                r2_idx = j
                break
            if q2_idx is None and not _is_pm(uj) and uj.who != questioner_who:
                break
            if q2_idx is not None and not _is_pm(uj) and uj.who != questioner_who:
                break

        ann_start = q1_idx
        for j in range(q1_idx - 1, max(-1, q1_idx - 8), -1):
            if _is_chair(utts[j]) and (
                PM_ONLY_FORMULA_RE.search(utts[j].text)
                or re.search(r"Pregunta\s+del\s+", utts[j].text, re.I)
                or _notes_expediente(utts[j].notes)
            ):
                ann_start = j
                break
            if not _is_chair(utts[j]) and _is_pm(utts[j]):
                break
        span_end = r2_idx if r2_idx is not None else r1_idx
        exp = exp_ann or _collect_exp_near(utts, ann_start, span_end)
        # If still missing, check only the R2 utterance notes (common TEI placement)
        if not exp and r2_idx is not None:
            exp = _notes_expediente(utts[r2_idx].notes)

        # Concatenate split Q1 fragments up to the floor cue
        q1_parts = []
        for j in range(q1_idx, i):
            if not _is_chair(utts[j]) and utts[j].who == questioner_who:
                q1_parts.append(utts[j].text)
        q1_text = " ".join(q1_parts) if q1_parts else utts[q1_idx].text

        notes: list[str] = []
        if not exp:
            notes.append("expediente_missing_in_tei")
        if not reg_q:
            notes.append("registered_question_missing_in_chair")

        exchanges.append(
            RawExchange(
                session_id=session_id,
                document_path=_document_relpath(path),
                date=session_date,
                legislature=LEGISLATURE,
                expediente=exp,
                registered_question_from_chair=reg_q,
                questioner_who=questioner_who,
                answerer_who=PM_WHO,
                q1_utterance_id=utts[q1_idx].uid,
                r1_utterance_id=utts[r1_idx].uid,
                q2_utterance_id=utts[q2_idx].uid if q2_idx is not None else None,
                r2_utterance_id=utts[r2_idx].uid if r2_idx is not None else None,
                q1_text=q1_text,
                r1_text=utts[r1_idx].text,
                q2_text=utts[q2_idx].text if q2_idx is not None else None,
                r2_text=utts[r2_idx].text if r2_idx is not None else None,
                chair_announcement=chair_ann,
                extraction_notes=notes,
            )
        )
        used_q1.add(utts[q1_idx].uid)

    return exchanges


def iter_xiv_session_files() -> list[Path]:
    tei = (PARLAMINT_CACHE / "ParlaMint-ES.TEI").resolve()
    files = sorted(tei.rglob("ParlaMint-ES_*.xml"))
    out: list[Path] = []
    for path in files:
        m = re.search(r"ParlaMint-ES_(\d{4}-\d{2}-\d{2})", path.name)
        if not m:
            continue
        d = date.fromisoformat(m.group(1))
        if LEGISLATURE_START <= d <= PARLAMINT_COVERAGE_END:
            out.append(path)
    return out


def sessions_with_pm_control_marker() -> list[dict]:
    rows: list[dict] = []
    for path in iter_xiv_session_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"ParlaMint-ES_(\d{4}-\d{2}-\d{2})", path.name)
        rows.append(
            {
                "session_id": path.stem,
                "date": m.group(1) if m else "",
                "path": _document_relpath(path),
                "pm_formula_count": len(PM_ONLY_FORMULA_RE.findall(text)),
                "has_pm_questions_heading": bool(
                    re.search(
                        r"Preguntas\s+dirigidas\s+al\s+se[nñ]or\s+presidente\s+del\s+Gobierno",
                        text,
                        re.I,
                    )
                ),
            }
        )
    return rows


def extract_all_xiv_pm_exchanges() -> list[RawExchange]:
    results: list[RawExchange] = []
    for path in iter_xiv_session_files():
        results.extend(extract_pm_exchanges_from_session(path))
    return results


def main() -> int:
    rows = extract_all_xiv_pm_exchanges()
    print(f"extracted_pm_exchanges={len(rows)}")
    print(f"with_expediente={sum(1 for r in rows if r.expediente)}")
    print(f"with_reg_chair={sum(1 for r in rows if r.registered_question_from_chair)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
