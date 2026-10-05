"""Draft question-side coding from registered_question + Q1 only.

Never uses R1 / reply_status / party / formation_vote_alignment for assignment.
Draft instrument for audit and calibration diversity — not gold annotation.
"""

from __future__ import annotations

import re
from typing import Any

QUESTION_TOPICS = (
    "economy_employment",
    "social_public_services",
    "territorial_institutional",
    "foreign_security",
    "governance_institutional_integrity",
    "other",
)

QUESTION_FORMS = ("yes_no", "wh", "evaluative")

# Topic cues: Spanish parliamentary register (draft heuristics).
# Order matters only within first-match priority lists below.
_TOPIC_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "foreign_security",
        re.compile(
            r"\b("
            r"otan|otan\b|otan|ue\b|uni[oó]n europea|europa\b|ucrania|rusia|"
            r"migraci[oó]n|inmigraci[oó]n|frontera|sahara|marruecos|gibraltar|"
            r"exteriores|diplom[aá]tica|geopol[ií]tic|defensa\b|ej[eé]rcito|"
            r"terrorismo|yihad|security|guerra\b|conflicto b[eé]lico|"
            r"sanci[oó]nes internacionales|refugiad"
            r")\b",
            re.I,
        ),
    ),
    (
        "territorial_institutional",
        re.compile(
            r"\b("
            r"catalu[nñ]a|catalan|euskadi|pa[ií]s vasco|navarra|galicia|"
            r"comunidad(?:es)? aut[oó]nom|"
            r"autogobierno|estatuto|competencias?|"
            r"financiaci[oó]n auton[oó]mica|cupo|concierto econ[oó]mico|"
            r"refer[eé]ndum|independen|"
            r"155\b|articulo 155|art[ií]culo 155|"
            r"recentraliz|plurinacional|territorial|"
            r"gobierno vasco|govern\b|generalitat|"
            r"inversiones en catalu|inversiones en euskadi"
            r")\b",
            re.I,
        ),
    ),
    (
        "economy_employment",
        re.compile(
            r"\b("
            r"econom[ií]a|empleo|desempleo|paro\b|laboral|trabajado|"
            r"inflaci[oó]n|precios|ipc\b|pib\b|d[eé]ficit|deuda p[uú]blica|"
            r"impuestos?|fiscal|presupuest|fondos europeos|nextgeneration|"
            r"empresas?|aut[oó]nomos|salario|erTE|erte\b|"
            r"pensiones?|jubilaci[oó]n|"
            r"industria|energ[eé]tica|luz\b|gas\b|carburante|"
            r"vivienda|alquiler|hipoteca|"
            r"banca|rescate|ibex|mercado|"
            r"ruina|miseria|crecimiento econ"
            r")\b",
            re.I,
        ),
    ),
    (
        "social_public_services",
        re.compile(
            r"\b("
            r"sanidad|salud|hospital|pandemia|covid|vacuna|"
            r"educaci[oó]n|universidad|escuela|becas|"
            r"dependencia|servicios sociales|pobreza|"
            r"igualdad|violencia de g[eé]nero|lgtbi|transexual|"
            r"vivienda social|sanitario|m[eé]dico|"
            r"cultura|ciencia|investigaci[oó]n"
            r")\b",
            re.I,
        ),
    ),
    (
        "governance_institutional_integrity",
        re.compile(
            r"\b("
            r"corrupci[oó]n|financiaci[oó]n ilegal|financiaci[oó]n irregular|"
            r"separaci[oó]n de poderes|estado de derecho|"
            r"transparencia|indultos?|amnist[ií]a|"
            r"parlamento|c[aá]maras?|decreto|"
            r"mentira|enga[nñ]o|dimisi[oó]n|moción de censura|"
            r"responsabilidad pol[ií]tica|fiscal[ií]a|juicio|"
            r"gobernar a espaldas|falta de medidas|"
            r"modelo policial|cuerpo(?:s)? policial|"
            r"investidura|pacto de gobierno|"
            r"error(?:es)?|disculpas"
            r")\b",
            re.I,
        ),
    ),
]

_YES_NO = re.compile(
    r"(?i)^\s*(?:¿\s*)?(?:"
    r"es\b|está\b|estan\b|están\b|ha\b|han\b|tiene\b|tienen\b|"
    r"va a\b|van a\b|piensa\b|piensan\b|cree\b|creen\b|"
    r"puede\b|pueden\b|quiere\b|quieren\b|debe\b|deben\b|"
    r"acepta\b|garantiza\b|cumplirá\b|cumplira\b|reconoc"
    r")",
)

_WH = re.compile(
    r"(?i)(?:¿\s*)?(?:"
    r"qué\b|que\b|quién\b|quien\b|quiénes\b|quienes\b|"
    r"cuándo\b|cuando\b|cuánto\b|cuanto\b|cuánta\b|cuanta\b|"
    r"cuántos\b|cuantos\b|cuántas\b|cuantas\b|"
    r"cómo\b|como\b|dónde\b|donde\b|por qué\b|porque\b|"
    r"cuál\b|cual\b|cuáles\b|cuales\b"
    r")",
)

_EVAL = re.compile(
    r"(?i)\b("
    r"valoraci[oó]n|valora\b|valorar|criterio|"
    r"opini[oó]n|considera\b|le parece|qu[eé] le parece|"
    r"apuesta\b|modelo\b|planteada la legislatura"
    r")\b",
)

# Face-threatening / accusatory discourse cues (linguistic, not partisan).
_CONFRONTATIONAL = re.compile(
    r"(?i)("
    r"mentira|miente|enga[nñ]|"
    r"corrupci[oó]n|corrupto|"
    r"financiaci[oó]n ilegal|financiaci[oó]n irregular|"
    r"delito|delincuente|criminal|"
    r"traici[oó]n|traidor|"
    r"incompetente|incapaz|"
    r"a espaldas|"
    r"falta de medidas|"
    r"cuesta? de\s+\w+\s+vidas?|"  # rare
    r"ruina y miseria|"
    r"antes de dimitir|"
    r"pedir disculpas|"
    r"reconocer alg[uú]n error|"
    r"es responsable de|"
    r"va a traer a espa[nñ]a|"
    r"empeorarlos|"
    r"sin verg[uü]enza|"
    r"hip[oó]crita|cinismo|c[ií]nico|"
    r"ha mentido|usted minti|"
    r"oculta\b|ocultando|"
    r"fraude|estafa"
    r")",
)


def _join_question_text(registered: str | None, q1: str | None) -> str:
    parts = []
    if registered and str(registered).strip():
        parts.append(str(registered).strip())
    if q1 and str(q1).strip():
        parts.append(str(q1).strip())
    return "\n".join(parts)


def classify_question_topic(registered: str | None, q1: str | None) -> str:
    """Draft topic from question text only. Prefer registered title, else Q1."""
    primary = (registered or "").strip() or (q1 or "").strip()
    secondary = (q1 or "").strip() if (registered or "").strip() else ""
    text = primary
    # score topics on primary; break ties with secondary
    scores: dict[str, int] = {t: 0 for t in QUESTION_TOPICS}
    for topic, pat in _TOPIC_PATTERNS:
        if pat.search(text):
            scores[topic] += 2
        if secondary and pat.search(secondary):
            scores[topic] += 1
    best = max(QUESTION_TOPICS[:-1], key=lambda t: scores[t])  # exclude other
    if scores[best] == 0:
        return "other"
    return best


def classify_question_form(registered: str | None, q1: str | None) -> str:
    """Draft form from the dominant oral ask; fall back to registered."""
    text = (q1 or "").strip() or (registered or "").strip()
    # Prefer last interrogative chunk if present
    parts = re.findall(r"¿[^?]+?\?", text)
    focus = parts[-1] if parts else text
    if _EVAL.search(focus) and not _YES_NO.match(focus.lstrip("¿ ")):
        # evaluative often uses qué/cómo valoración
        if re.search(r"(?i)valoraci|valora|le parece|criterio", focus):
            return "evaluative"
    if _YES_NO.match(focus.lstrip("¿ ")):
        # yes/no can still be evaluative ("¿cree que…?") — keep yes_no if polar
        if re.search(r"(?i)^(¿\s*)?(cree|considera|le parece|valora)\b", focus):
            if re.search(r"(?i)valoraci|c[oó]mo valora|qu[eé] valoraci", focus):
                return "evaluative"
            return "yes_no"
        return "yes_no"
    if _WH.search(focus):
        if re.search(r"(?i)qu[eé]\s+valoraci|c[oó]mo\s+valora|qu[eé]\s+opini", focus):
            return "evaluative"
        return "wh"
    if _EVAL.search(focus):
        return "evaluative"
    # default: polar-looking titles without clear wh
    if re.search(r"(?i)\b(s[ií]|no)\b\s*\?\s*$", focus):
        return "yes_no"
    return "wh"


def classify_question_confrontational(registered: str | None, q1: str | None) -> str:
    """Linguistic face-threat / accusation cues only. Not partisan."""
    text = _join_question_text(registered, q1)
    if _CONFRONTATIONAL.search(text):
        return "yes"
    # Adversarial presupposition templates
    if re.search(
        r"(?i)("
        r"en vez de empeorar|"
        r"antes de dimitir|"
        r"a espaldas del|"
        r"falta de medidas est[aá] generando|"
        r"cu[aá]nta ruina|"
        r"es responsable de los actos"
        r")",
        text,
    ):
        return "yes"
    return "no"


def code_question_side(registered: str | None, q1: str | None) -> dict[str, str]:
    return {
        "question_topic": classify_question_topic(registered, q1),
        "question_form": classify_question_form(registered, q1),
        "question_confrontational": classify_question_confrontational(registered, q1),
    }


def primary_alignment(raw: str) -> str:
    if raw == "opposed":
        return "opposed"
    if raw in {"supported", "abstained"}:
        return "non_opposed"
    return "unknown"


def code_frame(df, *, registered_col: str, q1_col: str) -> Any:
    """Add draft question-side columns; never reads R1."""
    import pandas as pd

    rows = []
    for _, r in df.iterrows():
        rows.append(code_question_side(r.get(registered_col), r.get(q1_col)))
    side = pd.DataFrame(rows, index=df.index)
    out = df.copy()
    for c in side.columns:
        out[c] = side[c]
    return out
