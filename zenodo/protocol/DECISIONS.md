# Decision log

Append-only. Do not rewrite past entries. Use ISO dates.

Format per entry:

- **date**
- **decision**
- **status**
- **evidence**
- **reason**
- **effect on protocol**

---

## 2026-09-29 — Project creation

- **decision:** Create project `spanish_control_session_equivocation` with
  `paper/`, `zenodo/`, and private `_internal/` areas.
- **status:** accepted
- **evidence:** Phase 1 scaffold task; design brief archived under
  `_internal/planning/design/`
- **reason:** Separate manuscript, public reproducibility package, and private
  working material.
- **effect on protocol:** Establishes repository layout; no empirical protocol
  freeze.

## 2026-09-29 — Working research question

- **decision:** Adopt the observational primary question comparing explicit-reply
  rates across a pre-defined political-alignment contrast of the questioner's
  group; do not frame a causal claim.
- **status:** accepted (draft; not preregistered)
- **evidence:** Design brief §4; Phase 1 scientific-identity freeze
- **reason:** One inspectable confirmatory question for a reply-rate study.
- **effect on protocol:** Recorded in `STUDY_PROTOCOL_DRAFT.md`; operational
  alignment rule still unresolved.

## 2026-09-29 — Public / private separation

- **decision:** Public reproducibility content lives under `zenodo/`; private
  material under `_internal/` must never enter public releases; manuscript under
  `paper/`.
- **status:** accepted
- **evidence:** Workspace public-release hygiene rules; design brief §21
- **reason:** Prevent leakage of prompts, raw packets, and private notes.
- **effect on protocol:** Hygiene tests and docs enforce the split.

## 2026-09-29 — No LLM component

- **decision:** No LLM labelling, baselines, or assistance in coding for the
  empirical study.
- **status:** accepted
- **evidence:** Design brief §18
- **reason:** Keep the study human-centred and reviewable without model-as-coder
  complications.
- **effect on protocol:** Computational stack excludes LLM / GPU frameworks.

## 2026-09-29 — No GPU requirement

- **decision:** Pipeline is CPU-only (XML parsing, linkage, bootstrap, plots).
- **status:** accepted
- **evidence:** Design brief §17
- **reason:** Design does not require neural training or inference.
- **effect on protocol:** Environment omits torch / transformers.

## 2026-09-29 — No data sampled yet

- **decision:** Phase 1 scaffold only; no corpus acquisition, no sample draw, no
  annotation, no empirical results.
- **status:** accepted
- **evidence:** Phase 1 task gate
- **reason:** Reproducibility infrastructure before data work.
- **effect on protocol:** Make targets for later phases fail safely; seeds unset.

## 2026-09-29 — Phase 0 novelty freeze (NARROW)

- **decision:** Treat the exact multi-component design as DISTINCT WITH NARROWING;
  no directly matching Spanish study was identified in the documented search.
  Do not claim “first”.
- **status:** accepted for planning
- **evidence:** `_internal/reports/NOVELTY_FREEZE_REPORT.md`;
  `_internal/literature/LITERATURE_MATRIX.csv`
- **reason:** Closest work is UK PMQs reply-rate (Bull) or Spanish qualitative
  control-session pragmatics / interview evasiveness — not the full design.
- **effect on protocol:** Contribution statement constrained; Related Work must
  credit Fuentes/Santos López/Sánchez Villanueva and Bull PMQs tradition.

## 2026-09-29 — Phase 0 ParlaMint pin (prospective)

- **decision:** Prospective transcript source = ParlaMint 5.0 ParlaMint-ES
  (handle 11356/2004), licence CC BY 4.0; coverage ends 2023-02-23 per docs.
- **status:** accepted as Phase-0 fact; checksum freeze deferred to Phase 2
- **evidence:** CLARIN.SI deposit page; Samples README-ES / LINDAT documentation
- **reason:** Authoritative comparable TEI corpus already used in related work.
- **effect on protocol:** Eligible dates cannot exceed 2023-02-23 without a new
  transcript source decision.

## 2026-09-29 — Phase 0 preferred population narrowing

- **decision:** Prefer primary scope = XIV legislature PM control questions with
  answer dates inside ParlaMint-ES (through 2023-02-23), using January 2020
  investiture roll-call for alignment. XII post-censure optional only.
- **status:** recommended (not frozen)
- **evidence:** Coverage docs; investiture DS DSCD-14-PL-4; confound audit
- **reason:** Single formation-vote mapping reduces alignment ambiguity and
  period confounding.
- **effect on protocol:** Population concept updated in STUDY_PROTOCOL_DRAFT.md;
  final freeze still pending Phase 2 pool counts.

## 2026-09-29 — Phase 0 linkage feasibility

- **decision:** Classify linkage as HIGH-CONFIDENCE RULE-BASED using expediente
  180/###### + date + questioner + DS reference + ParlaMint session/speaker IDs.
- **status:** accepted for planning
- **evidence:** `_internal/link_audit_private/PHASE0_LINKAGE_PROBE.csv` (private)
- **reason:** Official initiative pages and Diario de Sesiones recover registered
  text and Q1/R1 structure; addressee filter required.
- **effect on protocol:** Phase 2 may proceed to acquisition/pool under narrowing;
  probe expedientes excluded from later samples.

## 2026-09-29 — Phase 0 alignment variable naming

- **decision:** Analytic variable name = `formation_vote_alignment` (neutral);
  title rhetoric “Allies and Adversaries” may remain working title but must not
  be the operational term.
- **status:** accepted for planning
- **evidence:** Terminology audit in Phase-0 feasibility report
- **reason:** Avoid implying ideological closeness; map cleanly to vote records.
- **effect on protocol:** Codebook/protocol language should use the neutral term.

## 2026-09-29 — Phase 0 licensing posture

- **decision:** ParlaMint-derived text releasable under CC BY 4.0 with attribution;
  Congreso full-text deposit deferred to identifier-based strategy until reuse
  notice is pinned.
- **status:** accepted interim
- **evidence:** `docs/licensing.md`; CLARIN.SI deposit; Congreso open-data portal
- **reason:** Do not overclaim Congreso redistribution rights.
- **effect on protocol:** Zenodo data release plan remains mixed FULL TEXT
  (ParlaMint) / IDENTIFIER-BASED (Congreso) until updated.

## 2026-09-29 — Author order

- **decision:** Byline order is César Andrés, Jose Jaime Baena Rojas, Daniel Pinto Pajares.
- **status:** accepted
- **evidence:** Explicit user instruction
- **reason:** Correct authorship sequence for manuscript and package metadata.
- **effect on protocol:** Updated `paper/main.tex`, `CITATION.cff`, `pyproject.toml`, `LICENSE`.
