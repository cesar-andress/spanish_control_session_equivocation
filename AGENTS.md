# AGENTS.md — spanish_control_session_equivocation

## Paper identity

**Working title.** Answering Allies and Adversaries: Equivocation in Prime-Ministerial Replies during Spanish Parliamentary Control Sessions

**Primary question (observational).** In Spanish Congress control sessions, does the Prime Minister give explicit replies to pre-registered oral questions at different rates depending on the political alignment of the questioner's parliamentary group?

Do not sharpen this into a causal claim. Operational codebook definitions are not frozen.

**Analytic variable name (neutral):** `formation_vote_alignment` (not “allies/adversaries”).

**Phase.** Phase 0 complete: **NARROW** (conditional GO). No research corpus acquired; no sample; no annotation; no results.

## Authors (byline order)

1. César Andrés (ORCID 0009-0001-8968-3404)
2. Jose Jaime Baena Rojas (ORCID 0000-0002-0915-4087)
3. Daniel Pinto Pajares (ORCID 0000-0001-9397-811X)

## Phase-0 narrowing (required before Phase 2)

- Prospective transcripts: ParlaMint 5.0 / ParlaMint-ES (handle 11356/2004), CC BY 4.0; coverage ends **2023-02-23**.
- Preferred primary scope: **XIV** legislature PM control questions within ParlaMint dates; Jan 2020 investiture for alignment.
- Registered questions: Congreso iniciativas `180/######` with addressee = Presidente del Gobierno.
- Linkage: HIGH-CONFIDENCE RULE-BASED (expediente + date + questioner + DS + ParlaMint IDs).

## Design brief

`_internal/planning/design/project_design_brief.md`

Phase-0 reports:

- `_internal/reports/NOVELTY_FREEZE_REPORT.md`
- `_internal/reports/PHASE0_NOVELTY_AND_FEASIBILITY.md`

## Hard constraints

- No LLM labelling or coding assistance.
- No GPU / torch / transformers stack.
- Do not reanalyse the previous paper's N=100 pilot.
- Do not claim primacy / “first”.
- Do not push `_internal/` or manuscript drafts to the public remote.
- Do not start Phase 2 until the narrowing above is explicitly accepted.

## Integrity sequence

development → calibration → protocol freeze → main annotation → reliability → adjudication → analysis

## Next gate

Accept NARROW scope → Phase 2 data acquisition + pool (separate prompt). No sampling seeds yet.
