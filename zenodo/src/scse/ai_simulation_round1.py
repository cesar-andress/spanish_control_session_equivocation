"""AI simulation pilot on Calibration Round 1 (diagnostic only).

Build blinded packets; analyse AI outputs against human returns when supplied.
Does not fabricate AI labels. Does not touch Round 2 or XIV main outcomes.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

import pandas as pd

from scse.calibration_metrics import (
    CATEGORIES,
    cohen_kappa_3way,
    confusion_matrix_3way,
    normalize_label,
    raw_agreement,
)
from scse.paths import DATA_PRIVATE, INTERNAL_DIR, PROJECT_ROOT, PROTOCOL_DIR

AI_DIR = INTERNAL_DIR / "ai_simulation"
R1_PACKET = DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_PACKET_BLINDED.csv"
R1_CODES = DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_CODES.csv"
CODEBOOK_V03 = PROTOCOL_DIR / "reply_status_codebook_v0.3.md"

ES_LABELS = (
    "respuesta explícita",
    "respuesta parcial o intermedia",
    "ausencia de respuesta",
)

FORBIDDEN_AI_PACKET_KEYS = {
    "daniel",
    "jose",
    "jose_jaime",
    "agreement",
    "kappa",
    "disagreement",
    "gold",
    "consensus",
    "adjudicat",
    "reply_status",
    "human",
    "unit_id",
    "formation_vote",
    "primary_alignment",
    "question_topic",
    "question_form",
    "question_confrontational",
}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_round1_blinded_cases() -> list[dict[str, Any]]:
    pkt = pd.read_csv(R1_PACKET).sort_values("case_no", kind="mergesort")
    if list(pkt["case_no"]) != list(range(1, 21)):
        raise ValueError("Round-1 packet case_no must be 1..20 in order")
    cases = []
    for _, row in pkt.iterrows():
        cases.append(
            {
                "case": int(row["case_no"]),
                "registered_question": str(row["registered_question"]).strip(),
                "oral_question": str(row["Q1"]).strip(),
                "first_response": str(row["R1"]).strip(),
            }
        )
    return cases


def assert_blinded_payload(obj: Any) -> None:
    blob = json.dumps(obj, ensure_ascii=False).lower()
    for bad in FORBIDDEN_AI_PACKET_KEYS:
        if bad in blob:
            # allow ordinary Spanish words that are not leakage: none of these
            # should appear in the case texts as analytic metadata keys.
            # Check structure keys more carefully when obj is list of cases.
            pass
    if isinstance(obj, list):
        for item in obj:
            if not isinstance(item, dict):
                raise ValueError("each case must be an object")
            keys = set(item.keys())
            if keys != {"case", "registered_question", "oral_question", "first_response"}:
                raise ValueError(f"unexpected keys in case {item.get('case')}: {sorted(keys)}")
            for k in keys:
                for bad in (
                    "daniel",
                    "jose",
                    "agreement",
                    "kappa",
                    "gold",
                    "unit_id",
                    "reply_status",
                ):
                    if bad in k.lower():
                        raise ValueError(f"forbidden key {k}")


def write_blinded_json(path: Path | None = None) -> Path:
    AI_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (AI_DIR / "ROUND1_AI_BLINDED_CASES.json")
    cases = load_round1_blinded_cases()
    assert_blinded_payload(cases)
    path.write_text(
        json.dumps(cases, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    # Annotator / IRR leakage only (parliamentary prose may use ordinary words)
    text = path.read_text(encoding="utf-8").lower()
    for phrase in (
        "daniel",
        "jose jaime",
        "jose_jaime",
        "pinto pajares",
        "baena rojas",
        "cohen",
        "kappa",
        "gold label",
        "adjudica",
        "inter-annotator",
        "cal1_",  # unit ids must stay out of the AI-facing JSON
        "unit_id",
    ):
        if phrase in text:
            raise ValueError(f"blinded JSON contains forbidden phrase: {phrase}")
    return path


def write_ai_prompt(path: Path | None = None) -> Path:
    AI_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (AI_DIR / "ROUND1_AI_PROMPT.txt")
    text = """TAREA — Simulación exploratoria (calibración Ronda 1, guía v0.3)

Contexto
========
Vas a clasificar 20 intercambios parlamentarios españoles (pregunta registrada +
pregunta oral + primera respuesta del Presidente del Gobierno).

Esto es una simulación diagnóstica. No eres juez de verdad ni fuente de oro.
No uses conocimiento político externo para “corregir” lo dicho.

Material
========
Usa únicamente:
1) los 20 casos del archivo ROUND1_AI_BLINDED_CASES.json (en ese orden);
2) las definiciones de categoría de abajo (equivalentes a la guía v0.3).

No tienes etiquetas humanas. No inventes resultados de acuerdo entre personas.

Reglas de juicio (v0.3, sustanciales)
=====================================
- Objeto del juicio: la demanda comunicativa de la PREGUNTA ORAL.
- Ancla institucional: la PREGUNTA REGISTRADA (ayuda a interpretar elipses;
  no sustituye la oral como objeto principal).
- Hablar del mismo tema NO basta. La relevancia temática sola es insuficiente.
- No midas veracidad, persuasión, calidad política, moralidad ni ideología.
- Un rechazo de premisa puede contar como respuesta SI atiende directamente a
  lo que la pregunta exige comunicativamente.
- Réplica y dúplica no existen en estos casos: juzga solo la primera respuesta.

Categorías (elige exactamente una por caso)
===========================================
1) respuesta explícita
   La primera respuesta resuelve de forma directa la demanda principal de la
   pregunta oral (afirmar, negar, rechazar premisa cuando eso atiende al
   encargo, aportar la información o valoración pedidas, o un llenado
   alternativo claro del mismo encargo).

2) respuesta parcial o intermedia
   Aporta información que incide en la cuestión, pero no la resuelve del todo
   (componente atendido y otro relevante sin resolver; información pertinente
   incompleta; inferencia razonable acotada por lo dicho). No es “algo
   relacionado con el tema”.

3) ausencia de respuesta
   No aporta información que resuelva la demanda oral (solo tema general,
   cambio de foco, ataque sin atender a la cuestión, u otra pregunta).

Salida pedida
=============
Clasifica CADA caso de forma independiente (caso 1 … caso 20).

Para cada caso, devuelve SOLO:
- case: número
- category: una de las tres etiquetas anteriores (literal)
- borderline: "yes" o "no"
- justification: UNA frase breve (aprox. una oración) que cite la relación
  relevante entre la pregunta oral (y, si hace falta, la registrada) y la
  primera respuesta.

No reveles un razonamiento interno paso a paso. No escribas cadenas largas de
análisis. No añadas comentarios políticos.

Formato de salida (JSON)
========================
[
  {
    "case": 1,
    "category": "respuesta explícita",
    "borderline": "no",
    "justification": "..."
  }
]

Modos de ejecución
==================
MODE A (determinista / simple): una sola pasada independiente sobre los 20 casos.
MODE B (estabilidad): si el entorno lo permite, repetir la misma tarea ciega
tres veces en llamadas independientes (run_1, run_2, run_3). No agregues por
voto mayoritario; guarda las tres salidas por separado.

Prohibiciones
=============
- No uses ni pidas etiquetas humanas.
- No clasifiques casos del estudio principal (XIV).
- No modifiques la guía ni inventes categorías nuevas.
"""
    path.write_text(text.strip() + "\n", encoding="utf-8")
    return path


def write_run_instructions(path: Path | None = None) -> Path:
    path = path or (AI_DIR / "ROUND1_AI_RUN_INSTRUCTIONS.md")
    path.write_text(
        """# Round-1 AI simulation — run instructions

## Inputs (blinded)

- `ROUND1_AI_BLINDED_CASES.json` — 20 cases, fixed order
- `ROUND1_AI_PROMPT.txt` — task + v0.3 category definitions
- Codebook reference: `zenodo/protocol/reply_status_codebook_v0.3.md`
  (human document; do not paste human Round-1 labels into the model context)

## MODE A

One independent classification of all 20 cases.

Save as:

`_internal/ai_simulation/returns/MODE_A_run1.json`

## MODE B

Three independent calls with the same blinded materials.

Save as:

- `_internal/ai_simulation/returns/MODE_B_run1.json`
- `_internal/ai_simulation/returns/MODE_B_run2.json`
- `_internal/ai_simulation/returns/MODE_B_run3.json`

Do not majority-vote yet.

## After returns exist

```bash
cd zenodo
uv run python -c "from scse.ai_simulation_round1 import analyse_available_returns; print(analyse_available_returns())"
```

Do not fabricate returns. Do not change Round 2 or the codebook from AI output.
""",
        encoding="utf-8",
    )
    return path


def load_ai_return(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) != 20:
        raise ValueError(f"{path}: expected list of 20 objects")
    out = []
    for item in sorted(data, key=lambda x: int(x["case"])):
        cat = str(item["category"]).strip().lower()
        if cat not in ES_LABELS:
            raise ValueError(f"{path}: bad category for case {item.get('case')}: {cat!r}")
        border = str(item.get("borderline", "")).strip().lower()
        if border not in {"yes", "no", "sí", "si"}:
            raise ValueError(f"{path}: bad borderline for case {item.get('case')}")
        if border in {"sí", "si"}:
            border = "yes"
        out.append(
            {
                "case": int(item["case"]),
                "category": cat,
                "borderline": border,
                "justification": str(item.get("justification", "")).strip(),
            }
        )
    if [x["case"] for x in out] != list(range(1, 21)):
        raise ValueError(f"{path}: cases must be 1..20")
    return out


def load_human_codes() -> pd.DataFrame:
    """Human returns for comparison only — never write into AI packet."""
    df = pd.read_csv(R1_CODES).sort_values("case_no", kind="mergesort")
    return df


def pairwise_report(ai: Sequence[str], human: Sequence[str], label: str) -> dict[str, Any]:
    return {
        "comparison": label,
        "n": len(ai),
        "exact_agreement": raw_agreement(ai, human),
        "cohen_kappa": cohen_kappa_3way(ai, human),
        "confusion_matrix": confusion_matrix_3way(ai, human),
    }


def analyse_one_ai_run(ai_rows: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    humans = load_human_codes()
    ai_lab = [r["category"] for r in ai_rows]
    dan = humans["daniel_reply_status"].tolist()
    jose = humans["jose_jaime_reply_status"].tolist()

    concord_mask = [
        normalize_label(a) == normalize_label(b) for a, b in zip(dan, jose)
    ]
    discord_cases = [
        int(c)
        for c, ok in zip(humans["case_no"], concord_mask)
        if not ok
    ]

    ai_conc = [lab for lab, ok in zip(ai_lab, concord_mask) if ok]
    hum_conc = [lab for lab, ok in zip(dan, concord_mask) if ok]

    borderline_n = sum(1 for r in ai_rows if r["borderline"] == "yes")
    dist = Counter(normalize_label(x) for x in ai_lab)

    on_discord = []
    for case in discord_cases:
        row = next(r for r in ai_rows if r["case"] == case)
        h = humans[humans["case_no"] == case].iloc[0]
        on_discord.append(
            {
                "case": case,
                "ai": row["category"],
                "daniel": h["daniel_reply_status"],
                "jose_jaime": h["jose_jaime_reply_status"],
                "ai_borderline": row["borderline"],
            }
        )

    return {
        "run_id": run_id,
        "ai_vs_daniel": pairwise_report(ai_lab, dan, "ai_vs_daniel"),
        "ai_vs_jose_jaime": pairwise_report(ai_lab, jose, "ai_vs_jose_jaime"),
        "ai_vs_human_concordant": {
            "n_concordant_cases": int(sum(concord_mask)),
            "exact_agreement": raw_agreement(ai_conc, hum_conc) if ai_conc else None,
            "cohen_kappa": cohen_kappa_3way(ai_conc, hum_conc) if len(ai_conc) >= 2 else None,
            "note": "Human concordant subset is not gold truth.",
        },
        "ai_on_human_disagreement_cases": on_discord,
        "ai_category_distribution": dict(dist),
        "ai_borderline_frequency": {
            "n_yes": borderline_n,
            "n_total": len(ai_rows),
            "rate": borderline_n / len(ai_rows),
        },
    }


def within_ai_stability(runs: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Compare multiple AI runs; no majority vote."""
    if len(runs) < 2:
        return {"n_runs": len(runs), "note": "need ≥2 runs"}
    ids = sorted(runs)
    base = runs[ids[0]]
    unstable = []
    for case in range(1, 21):
        cats = []
        for rid in ids:
            row = next(r for r in runs[rid] if r["case"] == case)
            cats.append(normalize_label(row["category"]))
        if len(set(cats)) > 1:
            unstable.append({"case": case, "categories_by_run": dict(zip(ids, cats))})
    # pairwise agreement among runs
    pairs = []
    for i, a in enumerate(ids):
        for b in ids[i + 1 :]:
            la = [r["category"] for r in sorted(runs[a], key=lambda x: x["case"])]
            lb = [r["category"] for r in sorted(runs[b], key=lambda x: x["case"])]
            pairs.append(
                {
                    "pair": f"{a}_vs_{b}",
                    "exact_agreement": raw_agreement(la, lb),
                    "cohen_kappa": cohen_kappa_3way(la, lb),
                }
            )
    return {
        "n_runs": len(runs),
        "pairwise": pairs,
        "unstable_cases": unstable,
        "n_unstable": len(unstable),
    }


def analyse_available_returns(returns_dir: Path | None = None) -> dict[str, Any]:
    returns_dir = returns_dir or (AI_DIR / "returns")
    if not returns_dir.is_dir():
        return {
            "status": "waiting_for_ai_returns",
            "returns_dir": str(returns_dir.relative_to(PROJECT_ROOT)),
            "fabricated": False,
        }
    files = sorted(returns_dir.glob("*.json"))
    if not files:
        return {"status": "waiting_for_ai_returns", "fabricated": False}

    reports = {}
    run_map: dict[str, list[dict[str, Any]]] = {}
    for path in files:
        rows = load_ai_return(path)
        rid = path.stem
        run_map[rid] = rows
        reports[rid] = analyse_one_ai_run(rows, rid)

    out = {
        "status": "analysed",
        "fabricated": False,
        "runs": reports,
        "within_ai_stability": within_ai_stability(run_map) if len(run_map) >= 2 else None,
        "codebook": "v0.3",
        "human_consensus_is_gold": False,
    }
    out_path = AI_DIR / "ROUND1_AI_ANALYSIS.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def build_package() -> dict[str, str]:
    cases = write_blinded_json()
    prompt = write_ai_prompt()
    instr = write_run_instructions()
    (AI_DIR / "returns").mkdir(parents=True, exist_ok=True)
    (AI_DIR / "returns" / "README.md").write_text(
        "Place genuine AI return JSON files here. Do not fabricate labels.\n",
        encoding="utf-8",
    )
    meta = {
        "phase": "ai_simulation_pilot_round1",
        "n_cases": 20,
        "codebook": "v0.3",
        "codebook_path": str(CODEBOOK_V03.relative_to(PROJECT_ROOT)),
        "codebook_sha256": _sha256_file(CODEBOOK_V03),
        "packet_source": str(R1_PACKET.relative_to(PROJECT_ROOT)),
        "packet_sha256": _sha256_file(R1_PACKET),
        "blinded_json": str(cases.relative_to(PROJECT_ROOT)),
        "blinded_json_sha256": _sha256_file(cases),
        "prompt": str(prompt.relative_to(PROJECT_ROOT)),
        "human_labels_in_ai_packet": False,
        "main_xiv_used": False,
        "round2_modified": False,
    }
    meta_path = AI_DIR / "ROUND1_AI_PACKAGE_MANIFEST.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {k: str(v) for k, v in meta.items()}
