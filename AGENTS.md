# AGENTS.md — spanish_control_session_equivocation

## Paper identity

**Working title (under review; not finalized).** Answering Allies and Adversaries: Equivocation in Prime-Ministerial Replies during Spanish Parliamentary Control Sessions

Neutral title options: `_internal/reports/PROTOCOL_REFINEMENT_AFTER_CLAUDE.md` (prefer scoped wording without allies/adversaries).

**Primary question (observational, descriptive — Phase 4A).** In XIV Spanish Congress control sessions, how does the rate of explicit first responses to oral control questions vary by a fixed formation-vote baseline (`primary_alignment`: opposed vs non_opposed), and how does that descriptive pattern relate to independently coded question-side features?

Do not sharpen this into a causal claim. Do not use allies/adversaries/friendly/hostile as analytic labels. Operational codebook definitions are not frozen.

**Analytic variable name (neutral):** `formation_vote_alignment` (institutional baseline indicator; not “allies/adversaries”).

**Annotation target (Phase 4A draft):** `reply_status` judged on **Q1**, anchored by the registered question; unit = registered + Q1 + R1 (first response).

**Phase.** Phase 4.3: joint discussion of the five development disagreements has been returned and recorded. No main annotation; no scientific sample draw; codebook remains DRAFT (v0.2 unchanged until optional v0.3).



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

Phase 4A:

- `_internal/reports/CLAUDE_DESIGN_REVIEW_2026-10-01.md`
- `_internal/reports/PROTOCOL_REFINEMENT_AFTER_CLAUDE.md`

## Hard constraints

- No LLM labelling or coding assistance.
- No GPU / torch / transformers stack.
- Do not reanalyse the previous paper's N=100 pilot.
- Do not claim primacy / “first”.
- Do not push `_internal/` or manuscript drafts to the public remote.
- Do not burn the XIV eligible pool on development/calibration (use out-of-pool sources).
- Do not start main annotation until codebook v0.2 + out-of-pool calibration plan are ready.

## Integrity sequence

out-of-pool development → out-of-pool calibration → protocol freeze → main annotation → reliability → adjudication → analysis

## Next gate

Optional codebook v0.3 from Phase 4.3 discussion reasoning → calibration seed freeze → Calibration Round 1. No XIV main coding yet.
