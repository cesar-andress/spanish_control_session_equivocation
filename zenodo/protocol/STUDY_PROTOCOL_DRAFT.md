# Study protocol — DRAFT

**Status: DRAFT — NOT YET FROZEN OR PREREGISTERED**

This document records design intentions for scaffolding and planning. It is
**not** a preregistration. Hypotheses, N, seeds, codebook hashes, and analysis
code will be deposited only at protocol freeze (planned Phase 5).

**Working title (under review; not finalized):** *Answering Allies and
Adversaries: Equivocation in Prime-Ministerial Replies during Spanish
Parliamentary Control Sessions*

Neutral title options are listed in
`_internal/reports/PROTOCOL_REFINEMENT_AFTER_CLAUDE.md` (Phase 4A). Prefer
scoped wording that does not use allies/adversaries.

Project slug: `spanish_control_session_equivocation`

---

## Research question (Phase 4A revision)

In XIV Spanish Congress control sessions (within verified ParlaMint-ES
coverage), how does the rate of **explicit first responses** (`R1`) to oral
control questions vary by a fixed institutional baseline indicator of the
questioner’s **formation-vote alignment** (`primary_alignment`: opposed vs
non_opposed), and how does that **descriptive** pattern relate to independently
coded **question-side** features of the oral turn?

This is an observational **descriptive association / estimation** study. It is
**not** a causal claim about strategy, intent, honesty, ideology, or political
effectiveness.

Forbidden framing labels for the alignment contrast: allies, adversaries,
friendly, hostile (and left vs right as synonyms for the contrast).

---

## Population (concept)

Oral questions addressed to the Presidente del Gobierno in Congress plenary
control sessions, answered in person by the Prime Minister, with recoverable
registered question text and complete transcription of the questioner's opening
turn and the Prime Minister's first response.

**Accepted NARROW scope (Phase 2).** Primary population = XIV legislature only;
parliamentary control-session questions to the Presidente del Gobierno; Prime
Minister provides the relevant first response in person; answer date inside
verified ParlaMint-ES 5.0 coverage with operational upper bound **2023-02-23**.
XII post-censure is not in the primary pool.

Phase-0 feasibility-probe exchanges and Phase-2 linkage-QA rows are retained in
the master catalogue with `exclude_from_sampling = true` and are excluded from
all scientific samples drawn from the XIV pool.

Political alignment (`formation_vote_alignment`) uses a draft individual-MP
investiture rule (Phase 3) as a **January 2020 institutional baseline**, not as
a claim of current alliance. The draft **primary descriptive contrast**
(Phase 3.5 / 4A) is `primary_alignment`: **opposed** vs **non_opposed**
(supported + abstained). Raw categories supported / opposed / abstained are
retained for description. Nothing is protocol-frozen or preregistered yet.

---

## Intended unit

One exchange comprising:

1. the registered (written) oral question;
2. the questioner's opening oral turn (`Q1`);
3. the Prime Minister's **first** response (`R1`).

The réplica and dúplica are out of scope for the primary coding unit. Manuscript
and codebook claims must refer to the **first response**, not the full exchange
after réplica.

---

## Annotation target (Phase 4A)

**Evaluated target for `reply_status`:** the **oral question turn (`Q1`)**,
**anchored** by the registered question (institutional framing and slot
identification).

Draft accompanying field (not a primary outcome):

`question_target_type` ∈ {`match`, `oral_expansion`, `multiple_question`,
`oral_substitution`}

Draft multi-question rule: answering only one of several distinct oral asks is
at most `intermediate_reply` unless the remaining asks are restatements of the
same slot.

Detail: `_internal/reports/PROTOCOL_REFINEMENT_AFTER_CLAUDE.md`.

---

## Intended annotation constructs

### Primary outcome (reply side)

`reply_status` with a three-level structure conceptually based on the Bull
reply / non-reply tradition:

- explicit reply
- intermediate reply
- non-reply

Exact operational definitions are **not frozen**. Draft instrument:
`reply_status_codebook_v0.1.md` (**DRAFT — NOT FROZEN**; Phase 4A requires a
v0.2 revision for the Q1-target rule). Literature basis:
`_internal/literature/REPLY_STATUS_FRAMEWORK.md`.

Optional diagnostics (not primary outcomes): `borderline`; `confidence`;
`notes`.

### Question-side codes (covariates; coded before R1)

Not outcome variables:

- `question_form` ∈ {`yes_no`, `wh`, `evaluative`}
- `question_confrontational` ∈ {`no`, `yes`}

Purpose: allow descriptive stratification so that any opposed vs non_opposed
gap is not interpreted solely as “loaded questions get non-replies.”

---

## Annotators and workflow separation

Two independent expert annotators (authors A and B). A third author runs the
pipeline and does not annotate.

Intended sequence:

out-of-pool development → out-of-pool calibration → protocol freeze →
main XIV annotation → reliability → adjudication → analysis

Integrity constraints:

- XIV pool items must not be burned on development/calibration (Phase 4A);
- calibration items must not silently enter main evaluation;
- adjudicated labels must not overwrite original independent labels;
- sampling must not occur after outcome inspection;
- codebook changes after main annotation begins require a logged protocol
  deviation;
- post-hoc analyses must not be presented as pre-specified;
- exploratory outputs must not overwrite confirmatory outputs;
- at least one annotator should remain blind to the directional hypothesis where
  feasible; residual voice-recognition leakage must be acknowledged.

Adjudication occurs only after reliability metrics are computed and committed.

---

## Reliability (Phase 4A)

- Primary coding: three-level `reply_status`.
- Sensitivity: binary **explicit vs not-explicit**.
- Preserve independent labels; freeze codebook (hash) before main coding.
- Candidate numeric floors (review suggestion; **not locked**): α / κ around
  0.67 floor and 0.80 target — decide at freeze before main outcomes exist.
- See `CALIBRATION_DESIGN.md`.

---

## Intended primary estimand (descriptive)

Descriptive **risk difference** in explicit-reply rate for
`primary_alignment`: **non_opposed minus opposed**, on adjudicated labels for
the XIV analysis frame, with a **questioner-cluster** bootstrap confidence
interval, plus the full three-level `reply_status` distribution.

Definitions (draft, not frozen):

- `opposed` = individual MP investiture vote **no** (2020-01-07, DSCD-14-PL-4);
- `non_opposed` = investiture vote **sí** or **abstención** (raw categories
  `supported` and `abstained`).

Raw `formation_vote_alignment` ∈ {supported, opposed, abstained} remains the
descriptive variable. Exact decision rule, N, and freeze status are open.

### Concentration and sensitivity (documented)

Eligible pool: 100 exchanges / **19** questioners. Notable concentration:
Casado (≈25 exchanges; large share of opposed); Esteban (≈14; dominates
supported). Planned robustness: per-questioner displays;
leave-one-questioner-out (especially Casado, Esteban); estimates on each
annotator’s labels and on the adjudicated set; stratification by question-side
codes. Avoid mixed models as the primary analysis with this cluster structure.

---

## Protocol freeze (planned)

Before main XIV annotation: deposit research question wording, primary estimand,
analysis code, alignment rule, exclusions, attrition table, N/frame definition,
sampling seeds (if any), question-side codebook, reply codebook hash, and
reliability thresholds in a timestamped registry (OSF or Zenodo protocol
record). Annotators acknowledge the codebook hash.

---

## Phase 2 verified source and eligibility facts (2026-09-29)

Status remains **DRAFT — NOT PREREGISTERED**. These facts update Phase 0 pins
after acquisition. They do **not** freeze alignment, N, seeds, codebook, or the
primary estimand decision rule.

- **Corpus:** ParlaMint 5.0 / ParlaMint-ES; handle `http://hdl.handle.net/11356/2004`;
  archive `ParlaMint-ES.tgz`; MD5 `2ba1216f3fcf1300ee74f50efe42ec6a`;
  SHA-256 `b101c066a7770c80fcd835cc39282f29acd32883887306017cbd454c4d6eef68`;
  licence CC BY 4.0. Bulk cache: `_internal/source_cache/parlamint/`.
- **Temporal upper bound:** answer dates ≤ **2023-02-23**; XIV start 2019-12-03.
- **Congreso source:** initiative detail pages for type `180/######` via
  https://www.congreso.es/es/busqueda-de-iniciativas (HTML GET, cached).
- **Congreso reuse:** aviso legal
  https://www.congreso.es/es/cem/aviso-legal (*Reutilización de información*);
  public packaging remains **IDENTIFIER-BASED** for Congreso strings
  (`../docs/licensing.md`).
- **Exchange structure:** separately stored `registered_question`, `q1_text`,
  `r1_text`, and optional `q2_text`/`r2_text` (provenance only).
- **Eligibility:** XIV; PM oral-question section / PM FORMULA; R1 speaker
  `who = #PedroSánchezPérezCastejón`; non-empty registered question, Q1, R1;
  `link_status` in `{exact, high_confidence}`.
- **Linkage:** sitting date + questioner name against Congreso initiative
  records for that day's TEI/gap expedientes; TEI note expediente used only when
  name-confirmed (TEI notes are sometimes misaligned). No LLM / embedding
  linkage.
- **Answerer criterion:** first response utterance `who` equals ParlaMint person
  id for Pedro Sánchez Pérez-Castejón; ministerial substitutes are out of pool.
- **Exclusions from XIV scientific samples:** Phase-0 probe expedientes; Phase-2
  linkage-QA rows (hash-ranked, not a scientific seed); SPDB previous-paper
  sitting dates when any candidate falls on those dates (Phase 2 observed
  **zero** overlap). Phase-4 in-pool development exclusions are **superseded**
  by Phase 4A (restore planned; see refinement report).
- **Attrition (summary; full table pending):** raw PM-control extractions 139;
  eligible 100; link_status on raw: exact 46, high_confidence 54, unlinked 37,
  ambiguous 2. A detailed population → linked → eligible flow is required before
  freeze.
- **Canonical pool:** `_internal/data_private/eligible_pool_full.parquet`
  (private full text). Public projection:
  `data/derived/eligible_pool_metadata_preannotation.csv` (identifier-only).
- **Seeds:** `development`, `calibration`, and `main_sample` remain **null**.

---

## Phase 4 / 4A codebook and design status (2026-10-01)

**Status: DRAFT — NOT FROZEN.** No main annotation; no reply rates; no hypothesis
test.

- **Phase 4:** draft `reply_status_codebook_v0.1.md` (registered-anchored; to be
  revised for Q1 target).
- **Phase 4A:** target = oral turn anchored by registered; question-side fields;
  out-of-pool development/calibration plan; descriptive framing; title under
  review. Report:
  `_internal/reports/PROTOCOL_REFINEMENT_AFTER_CLAUDE.md`.
- **Development/calibration:** prefer previous-legislature (XIII) PM control
  sessions in ParlaMint; **do not** burn the XIV n=100. See
  `CALIBRATION_DESIGN.md`.
- **Packet schema:** blinded columns only (`unit_id`, `registered_question`,
  `Q1`, `R1`); provenance schema in `../schemas/annotation_row.schema.json`.

---

## Phase 0 verified factual constraints (2026-09-29)

These items are documentation-verified for planning. They are **not** a
protocol freeze.

- **Prospective corpus:** ParlaMint 5.0 / ParlaMint-ES; handle
  `http://hdl.handle.net/11356/2004`; licence **CC BY 4.0**.
- **ParlaMint-ES temporal coverage (docs):** Congreso plenary approximately
  2015-01 to **2023-02-23**.
- **Registered questions:** Congreso iniciativas type **Pregunta oral en Pleno**
  (`180/######`); registered wording available as initiative title; addressee
  must be filtered (PM vs ministers).
- **Linkage:** high-confidence rule-based using expediente + date + questioner +
  DS reference + ParlaMint session/speaker IDs (Phase-0 probe
  `_internal/link_audit_private/PHASE0_LINKAGE_PROBE.csv`, private).
- **Interaction unit:** Q_registered + Q1 + R1 extractable from Diario de
  Sesiones; réplica/dúplica present but out of primary coding unit.
- **Congreso redistribution terms:** aviso legal reuse conditions recorded in
  Phase 2; public packaging still identifier-based (`../docs/licensing.md`).

---

## Phase 3.5 confirmatory contrast design (2026-10-01)

**Status remains DRAFT — NOT PREREGISTERED.**

- **Primary descriptive contrast:** `primary_alignment` =
  **opposed** vs **non_opposed**.
- **Construction:** from raw individual-MP investiture categories;
  `non_opposed` = supported ∪ abstained.
- **Rationale:** single interpretable formation-opposition contrast; avoids two
  thin n≈18 primary strata; keeps sí vs abstención visible descriptively.
- **Secondary / descriptive:** report exchange and questioner counts (and later
  rates, only after annotation) by raw supported / opposed / abstained.
- **Planned lightweight robustness (at analysis, not yet frozen):**
  questioner-level displays; leave-one-questioner-out (Casado, Esteban);
  optional secondary contrast opposed vs supported only; question-side
  stratification.
- **Detail:** `_internal/reports/CONFIRMATORY_CONTRAST_DESIGN.md`

---

## Currently unresolved decisions

- Final working / submission title (options in Phase 4A report)
- Whether XII post-censure is included as secondary scope
- **Freeze** of `formation_vote_alignment` / `primary_alignment` mapping
  (`alignment_table.yaml` still `draft_not_frozen`)
- Whether opposed-vs-supported-only is a pre-specified secondary contrast at
  freeze
- Whether the XIV analysis uses the full eligible census vs a sample (review
  preferred census)
- Exact Bull-derived codebook definitions and Spanish examples (v0.2 after
  out-of-pool development)
- Operational definitions for `question_form` /
  `question_confrontational` / `question_target_type`
- Calibration performance gates (numeric thresholds to confirm at freeze)
- Final statistical decision rule (including any equivalence margin)
- Named scientific seed values for out-of-pool development/calibration
- Full attrition table (population → linked → eligible)
- Restore of superseded Phase-4 in-pool development exclusions
- Final Congreso full-text Zenodo packaging under aviso-legal conditions

---

## Related documents

- `DECISIONS.md` — append-only decision log
- `SOURCE_REGISTRY_DRAFT.yaml` — source pins (draft)
- `seeds.yaml` — named seeds (all pending until freeze)
- `reply_status_codebook_v0.1.md` — draft coding instrument (not frozen)
- `CALIBRATION_DESIGN.md` — calibration plan (out-of-pool under Phase 4A)
- `_internal/reports/PROTOCOL_REFINEMENT_AFTER_CLAUDE.md` — Phase 4A
- `_internal/reports/CLAUDE_DESIGN_REVIEW_2026-10-01.md` — external review archive
- `../docs/licensing.md` — licensing audit status
- `../manifests/release_manifest.schema.json` — release provenance schema
- `../schemas/annotation_row.schema.json` — future label provenance
- `../schemas/annotator_packet_row.schema.json` — blinded packet row schema
