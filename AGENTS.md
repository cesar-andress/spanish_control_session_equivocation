# AGENTS.md — spanish_control_session_equivocation

## Paper identity

**Working title.** Answering the Question? Reply Explicitness in Spanish
Prime-Ministerial Control Sessions

(Avoid allies/adversaries as the main title framing.)

**Primary question (observational, descriptive).** In XIV Spanish Congress
control sessions, how does the rate of explicit first responses to oral control
questions vary by a fixed formation-vote baseline (`primary_alignment`: opposed
vs non_opposed), and how does that descriptive pattern relate to independently
coded question-side features?

Do not sharpen this into a causal claim. Do not use allies/adversaries as
analytic labels. Operational codebook definitions are not frozen.

**Analytic variable name (neutral):** `formation_vote_alignment`.

**Annotation target:** `reply_status` judged on **Q1**, anchored by the
registered question; unit = registered + Q1 + R1.

**Phase.** Phase 6A: pre-outcome main-study infrastructure in parallel with
pending human Calibration Round 2. Codebook still v0.3 until joint
clarifications are returned and transcribed to v0.4. Main-frame N=97 (QA30
restored; 3 Phase-0 probes excluded). **No XIV reply_status labels. No main
annotation packets issued.**

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
- Do not start main annotation until codebook is frozen after calibration.
- Do not invent XIV reply_status outcomes while waiting for Round 2.

## Integrity sequence

out-of-pool development → out-of-pool calibration → protocol freeze → main annotation → reliability → adjudication → analysis

## Next gate

Await Round-2 returns (joint clarifications first, then independent packets).
On return: archive joint clarifications → compute Round-2 agreement before
discussion → transcribe into codebook v0.4 → freeze or reconsider → then issue
main packets for N=97. No Round 3 by default.
