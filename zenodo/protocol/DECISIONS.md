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

## 2026-09-29 — Phase 2: NARROW scope accepted

- **decision:** Accept Phase-0 NARROW recommendation as the prospective primary
  population for subsequent phases: Spanish Congreso; XIV only; control-session
  questions to the Presidente del Gobierno; PM in-person R1; answer dates within
  ParlaMint-ES 5.0 through 2023-02-23; Phase-0 probes excluded from all samples.
- **status:** accepted
- **evidence:** Phase-2 task instruction; Phase-0 feasibility report
- **reason:** Coverage and alignment confounding make open-ended premiership
  scope infeasible under the pinned corpus.
- **effect on protocol:** Population section updated; XII left optional/out.

## 2026-09-29 — Phase 2: ParlaMint-ES 5.0 checksum pin

- **decision:** Pin ParlaMint-ES archive SHA-256
  `b101c066a7770c80fcd835cc39282f29acd32883887306017cbd454c4d6eef68`
  (MD5 matches CLARIN.SI published `2ba1216f3fcf1300ee74f50efe42ec6a`).
- **status:** accepted
- **evidence:** Local archive verification; `docs/licensing.md`;
  `manifests/source_acquisition.json`
- **reason:** Reproducible corpus identity.
- **effect on protocol:** Source pin complete for transcripts.

## 2026-09-29 — Phase 2: Congreso source and reuse

- **decision:** Acquire type `180/` initiative detail HTML from Congreso búsqueda
  de iniciativas; record reuse conditions from
  https://www.congreso.es/es/cem/aviso-legal; keep public release
  **IDENTIFIER-BASED** for Congreso strings until packaging review.
- **status:** accepted interim
- **evidence:** Aviso legal text; `docs/licensing.md`
- **reason:** Reuse is conditioned, not a CC licence URI; do not overclaim.
- **effect on protocol:** Private full pool + public metadata projection.

## 2026-09-29 — Phase 2: Linkage algorithm

- **decision:** Link PM exchanges to Congreso records by sitting date + questioner
  name over that day's TEI/gap expedientes; accept TEI note expediente only when
  name-confirmed; statuses `exact` / `high_confidence` / `ambiguous` / `unlinked`.
  No LLM or embedding linkage.
- **status:** accepted for pool construction; human QA pending
- **evidence:** `src/scse/link_questions.py`; Phase-2 pool report
- **reason:** TEI expediente notes are sometimes misaligned across adjacent turns.
- **effect on protocol:** Eligible pool requires exact or high_confidence links.

## 2026-09-29 — Phase 2: Sampling exclusions

- **decision:** Exclude Phase-0 probe expedientes and Phase-2 linkage-QA rows
  (`exclude_from_sampling`); check SPDB previous-paper sitting dates (zero
  overlap observed in Phase-2 candidates).
- **status:** accepted
- **evidence:** `PHASE0_LINKAGE_PROBE.csv`; `PHASE2_LINKAGE_QA.xlsx`; pool flags
- **reason:** Prevent contamination of future samples by inspected cases.
- **effect on protocol:** Sampling frame = eligible minus these exclusions.

## 2026-10-01 — Linkage QA accepted

- **decision:** Linkage QA accepted.
- **status:** accepted
- **evidence:** 30 human-reviewed cases, all confirmed (YES=30, NO=0,
  UNCERTAIN=0). Report:
  `_internal/reports/LINKAGE_QA_HUMAN_VALIDATION_REPORT.md`; processed packet:
  `_internal/link_audit_private/PHASE2_LINKAGE_QA_HUMAN_VALIDATED.xlsx`.
- **reason:** Human verification of linkage correctness met the ≥95% target
  (100%). No reply-status judgement was performed.
- **effect on protocol:** Proceed to political-alignment feasibility
  (`formation_vote_alignment`). Sampling seeds remain null; no scientific
  sample draw; no reply coding.

## 2026-10-01 — Linkage QA modality clarification

- **decision:** Record that linkage QA was performed by oral/verbal human
  confirmation of the 30 packet exchanges, not by physically annotating the
  Excel cells.
- **status:** accepted (provenance clarification)
- **evidence:** Project-lead confirmation 2026-10-01; original
  `PHASE2_LINKAGE_QA.xlsx` remains blank in `human_link_correct`; processed
  copies hold the aggregate YES=30 result.
- **reason:** Avoid implying spreadsheet-cell annotation that did not occur.
- **effect on protocol:** No change to the PASS outcome or next gate; provenance
  wording only.

## 2026-10-01 — Formation-vote alignment feasibility (draft rule)

- **decision:** Adopt draft operational rule for `formation_vote_alignment`:
  individual MP named vote on the XIV second investiture vote (2020-01-07,
  DSCD-14-PL-4 / expediente 080/000001); map sí→supported, no→opposed,
  abstención→abstained. Unit = MP, not parliamentary group. Status remains
  **DRAFT — NOT FROZEN**. Feasibility recommendation: **GO** (HIGH confound risk).
- **status:** accepted for planning; not protocol-frozen
- **evidence:** Named roll-call in DSCD-14-PL-4; all 19 eligible questioners
  classified; `_internal/reports/ALIGNMENT_FEASIBILITY_REPORT.md`;
  `protocol/alignment_table.yaml`
- **reason:** Grupo Plural / Mixto votes split; group-level coding is not
  reproducible for those seats. Official named list removes subjectivity for
  the current pool.
- **effect on protocol:** Alignment table draft available; freeze deferred to
  protocol freeze. No reply coding / sampling. Primary contrast among
  supported/opposed/abstained still open.

## 2026-10-01 — Confirmatory contrast design (opposed vs non_opposed)

- **decision:** Draft primary confirmatory contrast = `primary_alignment`
  **opposed** vs **non_opposed**, where `non_opposed` = raw
  `formation_vote_alignment` ∈ {supported, abstained}. Retain supported /
  opposed / abstained for descriptive reporting. Do not use a three-level
  primary confirmatory endpoint. Status remains DRAFT — NOT PREREGISTERED /
  not frozen.
- **status:** accepted for planning
- **evidence:** Eligible-pool stratum sizes (opposed 64 / supported 18 /
  abstained 18); `_internal/reports/CONFIRMATORY_CONTRAST_DESIGN.md`
- **reason:** Balances institutional clarity of an opposition contrast, avoids
  unstable dual n≈18 primary strata, and preserves trichotomy in description.
  Not chosen to favour any reply outcome (none exist yet).
- **effect on protocol:** Primary endpoint draft updated to non_opposed minus
  opposed; lightweight questioner-level robustness planned; freeze still later.

## 2026-10-01 — Reply_status codebook development (DRAFT v0.1)

- **decision:** Adopt draft three-level `reply_status` instrument (explicit /
  intermediate / non-reply) measuring responsiveness to the registered
  question; create development set n=15 for examples only; design two-round
  calibration (20+20) without drawing units or freezing seeds; keep codebook
  **DRAFT — NOT FROZEN**.
- **status:** accepted for development; not frozen
- **evidence:** `reply_status_codebook_v0.1.md`;
  `_internal/literature/REPLY_STATUS_FRAMEWORK.md`;
  `_internal/reports/REPLY_STATUS_CODEBOOK_DEVELOPMENT_REPORT.md`;
  `_internal/data_private/development/DEVELOPMENT_SET_MANIFEST.json`;
  `CALIBRATION_DESIGN.md`
- **reason:** Need an operational annotation framework before calibration/
  reliability; Bull (1994) three-way structure adapted to Spanish control-
  session units without main-sample coding or outcome calculation.
- **effect on protocol:** Development units marked `exclude_from_sampling`
  (`development_codebook`); sampling frame reduced; primary contrast
  unchanged; no main annotation; seeds remain null.

## 2026-10-01 — Phase 4A protocol refinement after hostile design review

- **decision:** Accept GO-WITH-MODIFICATIONS design updates without starting
  annotation: (1) reframe RQ as descriptive variation in first-response
  explicitness by formation-vote baseline; (2) keep
  `formation_vote_alignment` / opposed vs non_opposed with neutral labels;
  (3) evaluate `reply_status` against **Q1** anchored by registered text and
  add draft `question_target_type`; (4) plan question-side covariates
  `question_form` and `question_confrontational` before R1; (5) move
  development/calibration **out of** the XIV n=100 (prefer prior-legislature
  PM control); (6) keep dual independent coding, freeze-before-main, and add
  explicit-vs-not sensitivity; (7) document questioner concentration /
  leave-one-out; (8) list neutral title options without finalizing.
- **status:** accepted for planning; protocol remains DRAFT — NOT PREREGISTERED
- **evidence:** `_internal/reports/CLAUDE_DESIGN_REVIEW_2026-10-01.md`;
  `_internal/reports/PROTOCOL_REFINEMENT_AFTER_CLAUDE.md`; updated
  `STUDY_PROTOCOL_DRAFT.md`; updated `CALIBRATION_DESIGN.md`
- **reason:** Close true design blockers identified by external review before
  any further instrument burn of the XIV pool.
- **effect on protocol:** Phase-4 registered-only target and in-pool
  development strategy superseded; codebook v0.2 required before calibration;
  no main packets/sample/outcomes; title under review.

## 2026-10-01 — Phase 4.1 out-of-pool development set + codebook v0.2

- **decision:** Supersede XIV in-pool development_codebook (n=15) with reason
  “Development material must not overlap with main population”; restore those
  XIV units to the sampling frame; build out-of-pool development set (n=15)
  from ParlaMint PM FORMULA exchanges (XIII preferred; XII post-censure
  supplement); deposit `development_set_manifest.yaml`; publish draft
  `reply_status_codebook_v0.2.md` (Q1 target, question-side fields, hard
  cases). Calibration units remain undrawn; codebook not frozen.
- **status:** accepted for development; DRAFT — NOT PREREGISTERED / not frozen
- **evidence:** `development_set_manifest.yaml`;
  `reply_status_codebook_v0.2.md`; `CALIBRATION_DESIGN.md`;
  `_internal/reports/EXPECTED_REPLY_STATUS_DISAGREEMENTS.md`;
  `_internal/data_private/development/out_of_pool/`
- **reason:** Close the out-of-pool development blocker before calibration
  without burning the XIV eligible census.
- **effect on protocol:** sampling_frame restores former development exclusions;
  instrument path points to v0.2; no XIV reply coding; no reliability yet.

## 2026-10-01 — Phase 4.2 human development package

- **decision:** Prepare blinded out-of-pool development workbooks for annotators
  A and B (n=15) with coding + codebook feedback sheets; document schema and
  instructions; record packet hashes. Exercise is for codebook intelligibility
  only — not calibration, reliability, gold, or main-study use.
- **status:** accepted for development workflow; codebook remains DRAFT
- **evidence:** `development_packet_schema.md`;
  `_internal/development/DEVELOPMENT_PACKAGE_PROVENANCE.json`;
  `_internal/reports/DEVELOPMENT_EXERCISE_INSTRUCTIONS.md`
- **reason:** Need structured human feedback on v0.2 before drawing calibration.
- **effect on protocol:** No XIV units used; no agreement metrics; freeze still
  deferred.
