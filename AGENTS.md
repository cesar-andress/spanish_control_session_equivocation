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

**Annotation target (redesign):** binary `direct_resolution` on **Q1** (v0.3 `reply_status` failed Gate C; preserved as provenance).

**Legacy annotation target:** `reply_status` on **Q1**, anchored by the registered
question; unit = registered + Q1 + R1.

**Phase.** 7A: binary redesign approved (direct resolution v1.0-draft). Round-2 Gate C FAIL preserved. Fresh OOP validation frame ready (15 untouched; N=12 drawn). Annotator packets not issued. AI simulation deferred.


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

Generate minimal joint orientation + 12-case independent validation packets under the locked binary gate (κ≥0.67 and ≥10/12). Do not recode Round 2. Do not issue main XIV packets.
