# AGENTS.md — spanish_control_session_equivocation

## Paper identity

**Working title.** Answering the Question? Reply Explicitness in Spanish
Prime-Ministerial Control Sessions

**Primary question (observational, descriptive).** In XIV Spanish Congress
control sessions, how does the rate of explicit first responses to oral control
questions vary by a fixed formation-vote baseline (`primary_alignment`: opposed
vs non_opposed), and how does that descriptive pattern relate to independently
coded question-side features?

Do not sharpen this into a causal claim. Do not call opposed vs non_opposed a
“confirmatory” contrast. Do not use allies/adversaries as analytic labels.

**Analytic variable name (neutral):** `formation_vote_alignment` (descriptive
contextual grouping).

**Annotation target:** `reply_status` on **Q1**, anchored by the registered
question; unit = registered + Q1 + R1.

**Phase.** Calibration Round 2 ingested (20/20 complete). Locked decision rule → **Gate C (STOP)**: α≈0.126 and binary κ≈0.121 both < 0.67. Codebook remains v0.3 (no v0.4). **No main packets. No XIV reply_status labels. No automatic Round 3.** AI simulation deferred.


## Authors (byline order)

1. César Andrés (ORCID 0009-0001-8968-3404)
2. Jose Jaime Baena Rojas (ORCID 0000-0002-0915-4087)
3. Daniel Pinto Pajares (ORCID 0000-0001-9397-811X)

## Hard constraints

- No LLM labelling for the human study. AI simulation status: **DEFERRED — DO NOT RUN BEFORE HUMAN CODEBOOK FREEZE** (archived JSON/prompt only; no MODE A/B).
- No GPU / torch / transformers stack.
- Do not reanalyse the previous paper's N=100 pilot.
- Do not claim primacy / “first”.
- Do not push `_internal/` privately sensitive material into public releases.
- Do not burn XIV units on development/calibration (OOP only).
- Do not start main annotation until Round-2 rule A/B applied and codebook frozen.
- Do not optimise the Round-2 threshold after seeing returns.

## Round-2 locked rule (summary)

- Primary: nominal Krippendorff α (3-category) ≥ 0.67 → keep 3-way, freeze v0.4.
- Else if binary explicit/non-explicit κ ≥ 0.67 → binary primary; 3-way secondary.
- Else STOP; no automatic Round 3.

## Integrity sequence

out-of-pool development → out-of-pool calibration → protocol freeze → main
annotation → reliability → adjudication → analysis

## Next gate

Gate C STOP. Human scientific reconsideration of the measurement scheme is required before any main annotation. Do not invent Round 3 or freeze v0.4 automatically.
