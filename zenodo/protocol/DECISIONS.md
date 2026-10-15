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

## 2026-10-02 — Development exercise solutions received (Daniel, Jose Jaime)

- **decision:** Record returned development booklets from Daniel Pinto Pajares
  and Jose Jaime Baena Rojas as **development solutions** for codebook
  refinement only (not gold, not calibration, not reliability, not main
  annotation). Persist structured JSON/CSV comparison under
  `_internal/development/solutions/` and report
  `_internal/reports/DEVELOPMENT_EXERCISE_SOLUTIONS.md`.
- **status:** accepted as development evidence
- **evidence:** raw DOCX returns archived; 15/15 labels each; pairwise
  reply-status agreement 10/15 on this exercise only
- **reason:** Need expert trial labels and free-text feedback before revising
  criteria / starting calibration.
- **effect on protocol:** Informs possible v0.3 wording; does not freeze
  codebook; does not authorize main XIV coding.

## 2026-10-02 — Phase 4.3 disagreement discussion document

- **decision:** Produce a Spanish joint-discussion booklet covering only the
  five development disagreements (cases 1, 6, 7, 12, 13). Experts supply
  linguistic reasoning; no adjudicated consensus category; no reliability
  coefficient; codebook v0.2 unchanged until that discussion returns.
- **status:** accepted as development workflow
- **evidence:** `_internal/development/REVISION_DE_DESACUERDOS_DESARROLLO.docx`;
  builder `zenodo/scripts/build_disagreement_review_docx.py`;
  `_internal/development/PHASE43_DISAGREEMENT_REVIEW_PROVENANCE.json`
- **reason:** Locate missing decision rules (especially partial vs absence, and
  case 13 target identification) before any v0.3 wording.
- **effect on protocol:** No freeze; no XIV coding; the 15 development cases
  remain outside calibration and main evaluation.

## 2026-10-05 — Phase 4.3 disagreement discussion returned

- **decision:** Archive and structure the joint discussion return for cases 1, 6,
  7, 12, 13 as development evidence for a possible codebook v0.3. Preserve
  original independent solution files; do not treat optional agreed categories
  as gold or adjudicated labels; leave `reply_status_codebook_v0.2.md`
  unchanged in this step.
- **status:** accepted as development evidence
- **evidence:**
  `_internal/development/solutions/raw_returns/daniel_jose_REVISION_DE_DESACUERDOS_DESARROLLO_v2_return.docx`;
  `_internal/development/solutions/phase43_disagreement_discussion_return.json`;
  `_internal/reports/PHASE43_DISAGREEMENT_DISCUSSION_RETURN.md`
- **reason:** Expert linguistic reasoning is required before revising decision
  rules (target identification, concreteness of generic nouns, packet display
  of registered questions).
- **effect on protocol:** Informs optional v0.3; does not freeze codebook; does
  not authorize main XIV coding. Case 7 remains unmarked; cases 12–13 partly
  attributed to missing registered question in the first booklet.

## 2026-10-05 — Phase 4.4 reply_status codebook v0.3 (DRAFT)

- **decision:** Create `reply_status_codebook_v0.3.md` from development lessons
  (topic vs communicative demand; generic-reference discourse rule; mandatory
  registered+Q1+R1 display; multi-demand and quantitative/qualitative worked
  rules; cautious premise rejection; Case 7 as known unresolved boundary;
  political-bias safeguards). Preserve v0.2 unchanged. Add packet validation
  requiring the three text fields. Do **not** freeze, draw calibration, assign
  seeds, or produce XIV reply outcomes.
- **status:** accepted as DRAFT instrument; NOT FROZEN
- **evidence:** `reply_status_codebook_v0.3.md`;
  `reply_status_codebook_v0.2_to_v0.3_changes.md`;
  `src/scse/packet_validation.py`;
  `_internal/reports/CODEBOOK_V03_READINESS_AUDIT.md`
- **reason:** Experts’ Phase 4.3 reasoning identified missing decision rules
  before calibration without justifying overfitting or fake consensus on Case 7.
- **effect on protocol:** Working instrument path → v0.3 draft; calibration
  design still undrawn; development Case 7 excluded from calibration/main.

## 2026-10-05 — Phase 5A Calibration Round 1 prepared

- **decision:** Without asking professors for another conceptual review, mark
  codebook v0.3 as the calibration version (still not frozen for the main
  study), derive Round-1 seed from the documented SHA-256 string, draw 20
  fresh out-of-pool PM FORMULA units (no development/XIV overlap), and issue
  two independent Spanish Word packets.
- **status:** accepted for Calibration Round 1 coding
- **evidence:** `calibration_round1_manifest.yaml`; `seeds.yaml` (calibration
  seed only); `_internal/calibration_round1/`;
  `src/scse/build_calibration_round1.py`; `scse.calibration_metrics` (prepared,
  not run)
- **reason:** Development reasoning already captured; need fresh independent
  coding evidence before any freeze.
- **effect on protocol:** Calibration Round 1 may begin; no discussion until
  both returns; no main XIV outcomes; Round 2 and main seeds remain unset.

## 2026-10-05 — Question-side topic audit + calibration diversity rule

- **decision:** Add draft `question_topic` (six-way neutral taxonomy) and
  tighten linguistic `question_confrontational`. Audit the XIV eligible pool on
  registered+Q1 only (no R1 / no reply rates). Do **not** rebalance or remove
  XIV units for topic. Classify topic×`primary_alignment` confound risk as
  MEDIUM. Fix a Calibration Round 1 diversity rule (≥2 topics and ≥2 forms)
  before any reply labels and redraw the 20 OOP units under that rule with the
  same documented seed.
- **status:** accepted
- **evidence:** `_internal/reports/QUESTION_SIDE_TOPIC_AND_DIVERSITY_AUDIT.md`;
  `scse.question_side`; `scse.question_side_audit`;
  `calibration_round1_manifest.yaml` diversity fields
- **reason:** Avoid conflating formation-vote alignment with question content;
  expose calibrators to linguistically varied asks without engineering
  agreement.
- **effect on protocol:** Main pool intact; Round 1 packets regenerated;
  sensitivity analyses may later use topic/confrontational strata.

## 2026-10-09 — Phase 5A Calibration Round 1 returns ingested

- **decision:** Archive the independent Round-1 Word returns from Daniel Pinto
  Pajares and Jose Jaime Baena Rojas; extract reply_status / dudoso /
  observaciones without imputing labels; compute exploratory agreement on the
  18 complete pairs **before** discussion; leave Jose Jaime cases 5 (no mark)
  and 10 (all three options marked) unusable until clarified.
- **status:** accepted as calibration diagnostics (not gold; not freeze)
- **evidence:** `_internal/calibration_round1/returns/`;
  `_internal/data_private/calibration/round1/CALIBRATION_ROUND1_CODES.csv`;
  `_internal/reports/CALIBRATION_ROUND1_AGREEMENT.md`;
  `zenodo/scripts/ingest_calibration_round1_returns.py`;
  `scse.calibration_metrics`
- **reason:** Integrity sequence requires agreement before discussion; two
  incomplete marks must not be silently repaired.
- **effect on protocol:** Round-1 draw/seed unchanged; codebook v0.3 still not
  frozen; next step is clarification of cases 5 and 10, then disagreement
  discussion (usable disagreements: cases 6 and 7); Round 2 still undrawn;
  no XIV main coding.

## 2026-10-13 — Jose Jaime Round-1 mark clarification ingested

- **decision:** Accept Jose Jaime’s adjusted Round-1 Word file as a
  clarification of previously unusable marks on cases 5 and 10 only; preserve
  the first return; recompute exploratory agreement on n=20; do not treat the
  adjustment as a fresh full coding pass.
- **status:** accepted as calibration diagnostics (not gold; not freeze)
- **evidence:** `_internal/calibration_round1/returns/` (pre_adjust + adjusted);
  `_internal/reports/CALIBRATION_ROUND1_AGREEMENT.md`;
  `_internal/data_private/calibration/round1/CALIBRATION_ROUND1_CODES.csv`
- **reason:** Cases 5 (blank) and 10 (triple mark) could not enter the
  agreement table; the adjusted file supplies one mark each without changing
  the other 18 cases.
- **effect on protocol:** Agreement n=20 is 16/20 (κ≈0.67); disagreements are
  cases 5, 6, 7, 10; next gate is disagreement discussion; Round 2 undrawn;
  no XIV main coding.

## 2026-10-13 — Phase 5B final calibration package (joint review + Round 2)

- **decision:** Issue one final calibration package: (1) short joint review of
  Round-1 cases 5, 6, 7, 10 only, recording two boundary clarifications in the
  professors’ own words; (2) independent Round-2 of 20 completely new OOP
  units under a new documented seed and diversity-constrained draw; (3) one
  short email covering joint-first then independent-second. Do **not** write
  codebook v0.4 before the joint return. Round 2 is the final planned
  calibration round (no Round 3 by default). No XIV outcomes.
- **status:** accepted for final calibration delivery
- **evidence:** `calibration_round2_manifest.yaml`; `seeds.yaml`
  (`calibration_round2`); `_internal/calibration_round2/`;
  `_internal/reports/CALIBRATION_ROUND2_SELECTION_AND_NOVELTY_AUDIT.md`;
  `src/scse/build_calibration_round2.py`;
  `scripts/build_calibration_round2_package.py`
- **reason:** Close calibration with minimal burden after Round-1 adjacent
  disagreements; preserve contemporaneous clarification before independent
  Round-2 coding.
- **effect on protocol:** Round-1 draw unchanged; Round-2 drawn (seed
  322720977); soft target max-2-per-questioner not feasible in OOP remainder
  (relaxed to 4, documented); after both Round-2 returns, compute agreement
  before discussion, then either freeze or reconsider the scheme.

## 2026-10-13 — Phase 6A: restore linkage-QA to main frame (pre-outcome)

- **decision:** After contamination audit, classify the 30 Phase-2 linkage-QA
  exchanges as **not contaminated** for reply-status annotation (linkage-only
  review by/to the project lead; Daniel and Jose Jaime did not see the cases;
  no reply_status judgement). Restore them to the main XIV population. Keep the
  3 Phase-0 feasibility probes excluded. Pre-outcome main-frame N = **97**.
- **status:** accepted for pre-outcome infrastructure
- **evidence:** `_internal/reports/MAIN_POPULATION_CONTAMINATION_AUDIT.md`;
  `_internal/reports/LINKAGE_QA_HUMAN_VALIDATION_REPORT.md`;
  `PHASE2_LINKAGE_QA_HUMAN_VALIDATION.json` (`reply_status_judgement_performed:
  false`); `protocol/main_frame_manifest.yaml`
- **reason:** Correct an unnecessarily conservative exclusion; not
  outcome-driven.
- **effect on protocol:** Sampling/main frame among eligible = 97; no XIV
  reply_status labels; main annotation still blocked until calibration freeze;
  Round-2 materials unchanged.

## 2026-10-13 — Phase 6A: pre-outcome main infrastructure

- **decision:** Build private main corpus, public metadata projection, internal
  source-review PDF, packet-generator templates (not issued), analysis scaffold
  with synthetic tests only, table/figure shells, and study-flow asset. Advance
  manuscript sections without Results outcomes.
- **status:** accepted for Phase 6A
- **evidence:** `_internal/data_private/main/`; `_internal/main_packets/`;
  `_internal/main_annotation/templates/`; `zenodo/outputs/`;
  `src/scse/main_frame.py`; `analysis_scaffold.py`; `preoutcome_assets.py`
- **reason:** Use waiting time during Round-2 without crossing the outcome
  firewall.
- **effect on protocol:** Generator ready; human packets **not** issued;
  codebook still v0.3 until Round-2 clarifications → v0.4.

## 2026-10-13 — Phase 6B: Round-2 decision rule locked (pre-returns)

- **decision:** Lock prospective Round-2 gate before inspecting returns.
  Primary metric = nominal Krippendorff α (3-category). A: α≥0.67 → keep
  3-category, no Round 3, v0.4 freeze, main annotation. B: α<0.67 but binary
  explicit vs non-explicit κ≥0.67 → no Round 3; binary primary; 3-category
  secondary with transparent weaker reliability. C: both <0.67 → STOP; no
  automatic Round 3; reconsider scheme. Always report raw agreement, 3-way κ,
  α, binary agreement, binary κ, confusion matrix.
- **status:** accepted; locked before Round-2 returns
- **evidence:** `CALIBRATION_DESIGN.md`; this entry
- **reason:** Prevent post-hoc threshold shopping.
- **effect on protocol:** Round 3 not planned by default; main annotation
  gated by A/B/C only.

## 2026-10-13 — Phase 6B: QA30 provenance + Phase-0 probes restored

- **decision:** Formalise QA30 provenance with evidence classes (exact
  reviewer personal name UNKNOWN in JSON; roles DOCUMENTED; Daniel/Jose
  non-appearance SUPPORTED BY CONTEMPORANEOUS RECORD). Keep QA30 restored
  (30/0). Reassess Phase-0 probes under the **same** reply-status
  contamination rule (not “continuity”): restore all three
  (`180/000041`, `180/000047`, `180/000128`). Final pre-outcome main frame
  **N=100**.
- **status:** accepted
- **evidence:** `_internal/reports/MAIN_POPULATION_CONTAMINATION_AUDIT.md`
  (Phase 6B); `PHASE0_LINKAGE_PROBE.csv`; linkage QA validation JSON
- **reason:** Continuity is not contamination; probes were linkage-feasibility
  only with no reply_status labels and no use in OOP development/calibration.
- **effect on protocol:** Main census = all linked eligible units; rebuild
  corpus/metadata/study-flow; no reply_status outcomes.

## 2026-10-13 — Phase 6B: descriptive alignment framing

- **decision:** Primary scientific framing = reply explicitness in first
  prime-ministerial responses. `formation_vote_alignment` /
  opposed vs non_opposed is a **descriptive contextual grouping**, not a
  confirmatory causal contrast. Drop “primary confirmatory contrast” wording
  for this variable.
- **status:** accepted for manuscript/protocol language
- **evidence:** Phase 6B task; confrontational imbalance audit
- **reason:** Avoid causal overclaim before outcomes.
- **effect on protocol:** Analysis remains descriptive risk-difference
  reporting with uncertainty; not a confirmatory political-effect test.

## 2026-10-13 — Phase 6B: question_confrontational exploratory-diagnostic

- **decision:** Reclassify `question_confrontational` as an
  **exploratory / diagnostic rule-based indicator** (keyword/regex; no human
  reliability). Not mandatory primary; not confirmatory covariate. Preserve
  audit for provenance; purpose = document why causal alignment interpretation
  is unsafe. No new human coding task.
- **status:** accepted
- **evidence:** `scse.question_side.classify_question_confrontational`;
  question-side audit report
- **reason:** Unvalidated rule coding must not be presented as human-validated.
- **effect on protocol:** `question_topic` / `question_form` remain descriptive
  if rules are deterministic; confrontational not primary.

## 2026-10-13 — Phase 6B: main adjudication + packet orders + AI deferral

- **decision:** (1) Dual independent coding of all main-frame units; preserve
  originals; agreement before discussion; adjudication after both finish;
  store adjudicated labels separately; report per-annotator and adjudicated
  analyses separately; no AI adjudication; neither annotator automatically
  authoritative. (2) Same main cases, different deterministic random orders
  (seeds frozen after N=100). Packets not issued yet. (3) AI simulation
  **deferred** until Round 2 complete, v0.4 frozen, and human protocol locked;
  no LLM reply-status labelling now.
- **status:** accepted
- **evidence:** `MAIN_PACKET_ORDERINGS.json`; `seeds.yaml` order seeds;
  `_internal/ai_simulation/` remains unused for new runs
- **reason:** Pre-outcome workflow clarity without starting main coding.
- **effect on protocol:** Generator/templates only; human packets blocked.

## 2026-10-13 — Pre-Round-2 cleanup: AI simulation must not be run

- **decision:** Mark Round-1 AI simulation materials as
  **DEFERRED — DO NOT RUN BEFORE HUMAN CODEBOOK FREEZE**. Archived JSON/prompt
  may remain. Do not execute MODE A/B; do not create AI reply-status labels;
  do not instruct the next agent to run the simulation now.
- **status:** accepted
- **evidence:** `_internal/ai_simulation/AI_SIMULATION_DEFERRED.md`;
  `_internal/reports/PROJECT_STATE.md`
- **reason:** Human calibration and codebook freeze first.
- **effect on protocol:** No change to Round-2 or main frame; AI path blocked.

## 2026-10-14 — Joint review return archived (cases 5, 6, 7, 10)

- **decision:** Archive the returned joint-review Word file for Round-1
  disagreements 5, 6, 7, 10; extract joint marks and the two boundary
  clarifications in the professors’ own words. Do **not** write codebook v0.4
  yet; do **not** inspect Round-2 independent returns in this step.
- **status:** accepted as calibration clarification evidence (not gold; not freeze)
- **evidence:**
  `_internal/calibration_round2/returns/01_REVISION_CONJUNTA_CASOS_5_6_7_10_returned.docx`
  (sha256 `84fde12c…`); `JOINT_REVIEW_RETURN.json`;
  `_internal/reports/JOINT_REVIEW_ROUND1_RETURN.md`
- **reason:** Contemporaneous joint wording is required before v0.4 transcription
  after the locked Round-2 A/B/C gate.
- **effect on protocol:** Issued blank joint DOCX preserved; Round-2 packets
  still outstanding; main annotation still blocked.

## 2026-10-15 — Calibration Round 2 returns ingested; Gate C STOP

- **decision:** Archive independent Round-2 Word returns (Daniel; Jose Jaime)
  and the joint-review file; compute agreement on complete pairs **before**
  discussion; apply the prospectively locked A/B/C rule. Result: **Gate C**
  (nominal α = 0.172 < 0.67 and binary explicit κ = 0.184 < 0.67). STOP before
  main annotation; **no** automatic Round 3; **no** codebook v0.4; **no** main
  packets. Case 5 incomplete (Jose Jaime unmarked reply_status); not imputed.
- **status:** accepted (calibration diagnostics; locked rule applied)
- **evidence:** `_internal/reports/CALIBRATION_ROUND2_AGREEMENT.md`;
  `_internal/reports/CALIBRATION_ROUND2_GATE_C_STOP.md`;
  `_internal/data_private/calibration/round2/CALIBRATION_ROUND2_CODES.csv`;
  `zenodo/scripts/ingest_calibration_round2_returns.py`
- **reason:** Thresholds were locked before returns; both floors missed.
- **effect on protocol:** Main annotation blocked; scheme reconsideration
  required; Round-2 draw/seed unchanged; XIV outcomes still absent.

## 2026-10-15 — Round-2 case 5 completed; Gate C confirmed on n=20

- **decision:** Re-ingest Jose Jaime Round-2 return with case 5 marked
  (respuesta parcial o intermedia). All 20 pairs complete. Locked A/B/C rule
  reapplied without threshold optimisation → still **Gate C** (α ≈ 0.126;
  binary κ ≈ 0.121). Case 5 is a disagreement (Daniel explícita vs Jose Jaime
  parcial). No v0.4; no main packets; no automatic Round 3.
- **status:** accepted
- **evidence:** `_internal/reports/CALIBRATION_ROUND2_AGREEMENT.md`;
  `_internal/data_private/calibration/round2/CALIBRATION_ROUND2_CODES.csv`
- **reason:** Completing the missing mark does not change the locked decision
  floors; both remain unmet on the full sample.
- **effect on protocol:** Confirms STOP; measurement-scheme reconsideration
  still required before any main annotation.

## 2026-10-15 — Phase 6C Round-2 measurement failure diagnostic

- **decision:** Preserve Gate C as final. Diagnose the measurement failure without
  relabelling, threshold search, v0.4, main packets, XIV outcomes, AI labels, or
  automatic Round 3. Recommend binary **direct resolution of the main
  communicative demand** as Redesign Option 1; keep a coverage trichotomy only
  if middle category is observational (multipart completeness). Fresh validation
  requires OOP extract expansion (only 4 untouched units remain in the current
  44-unit calibration frame).
- **status:** accepted (diagnostic)
- **evidence:** `_internal/reports/ROUND2_MEASUREMENT_FAILURE_DIAGNOSTIC.md`;
  `_internal/reports/ROUND2_FAILED_RESULT_FREEZE.json`
- **reason:** Locked reliability floors were missed; joint clarifications and
  v0.3 sufficiency language are not independently operational.
- **effect on protocol:** No main annotation; redesign decision pending project
  lead; Round-2 labels frozen as failed-calibration provenance.

## 2026-10-15 — Phase 7A binary redesign Option 1 + fresh validation frame

- **decision:** Adopt Redesign Option 1 as a new instrument lineage
  (`direct_resolution_codebook_v1.0-draft.md`), not v0.4. Expand OOP extract
  with date-aware PM answerer (70 usable; 15 untouched; human-exposure overlap
  0). Draw validation N=12 under locked seed `731954444` without inspecting R1
  for ease. Lock prospective PASS: κ≥0.67 AND raw agreement ≥10/12; FAIL → STOP
  (no automatic further round). Annotator DOCX not generated yet. Round-2
  failure preserved; no Round-2 recoding; no XIV outcomes; no AI labels.
- **status:** accepted (instrument draft + frame prepared)
- **evidence:** `zenodo/protocol/direct_resolution_codebook_v1.0-draft.md`;
  `_internal/reports/BINARY_REDESIGN_RATIONALE.md`;
  `_internal/reports/FRESH_BINARY_VALIDATION_FRAME_AUDIT.md`;
  `_internal/data_private/validation/binary_v1/`;
  `zenodo/src/scse/build_binary_validation_frame.py`
- **reason:** Gate C required substantive redesign; binary direct resolution is
  the approved minimum-complexity construct.
- **effect on protocol:** Main construct reframed as direct resolution /
  responsiveness; three-category scheme retired for future coding; validation
  packets await orientation materials generation.

## 2026-10-15 — Phase 7B binary validation materials issued

- **decision:** Freeze `direct_resolution_codebook_v1.0-validation.md` for the
  already-drawn N=12 fresh OOP sample (not redrawn). Issue one-page joint
  orientation (read only; no joint coding) and identical independent packets
  for Daniel and Jose Jaime. Prospective pass rule unchanged: κ≥0.67 and
  raw agreement ≥10/12; FAIL → STOP. This is fresh binary validation, **not**
  Calibration Round 3. No main XIV packets; no AI labels.
- **status:** accepted (materials issued; awaiting human returns)
- **evidence:** `_internal/binary_validation/`;
  `_internal/reports/BINARY_VALIDATION_PACKET_AUDIT.md`;
  `zenodo/protocol/direct_resolution_codebook_v1.0-validation.md`;
  `zenodo/scripts/build_binary_validation_package.py`
- **reason:** Approved redesign requires minimal-burden human validation before
  any main annotation.
- **effect on protocol:** Annotators may begin orientation + independent coding;
  returns handled under locked gate; no threshold changes after returns.
