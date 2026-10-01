# Study protocol — DRAFT

**Status: DRAFT — NOT YET FROZEN OR PREREGISTERED**

This document records design intentions for scaffolding and planning. It is
**not** a preregistration. Hypotheses, N, seeds, codebook hashes, and analysis
code will be deposited only at protocol freeze (planned Phase 5).

Working title: *Answering Allies and Adversaries: Equivocation in
Prime-Ministerial Replies during Spanish Parliamentary Control Sessions*

Project slug: `spanish_control_session_equivocation`

---

## Research question

In Spanish Congress control sessions, does the Prime Minister give explicit
replies to pre-registered oral questions at different rates depending on the
political alignment of the questioner's parliamentary group?

This is an observational contrast. It is not a causal claim.

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
all development, calibration, and main samples.

Political alignment (`formation_vote_alignment`) uses a draft individual-MP
investiture rule (Phase 3). The draft **primary confirmatory contrast**
(Phase 3.5) is `primary_alignment`: **opposed** vs **non_opposed** (supported +
abstained). Raw categories supported / opposed / abstained are retained for
description. Nothing is protocol-frozen or preregistered yet.

---

## Intended unit

One exchange comprising:

1. the registered (written) oral question;
2. the questioner's opening turn;
3. the Prime Minister's first response.

The réplica and dúplica are out of scope for the primary coding unit.

---

## Intended annotation construct

`reply_status` with a three-level structure conceptually based on the Bull
reply / non-reply tradition:

- explicit reply
- intermediate reply
- non-reply

Exact operational definitions are **not frozen** and must not be invented in
the scaffold phase. A Spanish-adapted codebook is planned for Phase 3.

Additional planned fields (not yet operationalised): question form;
equivocation type for non-explicit responses; borderline flag; free-text note.

---

## Annotators and workflow separation

Two independent expert annotators (authors A and B). A third author runs the
pipeline and does not annotate.

Intended sequence:

development → calibration → protocol freeze → main annotation → reliability →
adjudication → analysis

Integrity constraints:

- calibration items must not silently enter main evaluation;
- adjudicated labels must not overwrite original independent labels;
- sampling must not occur after outcome inspection;
- codebook changes after main annotation begins require a logged protocol
  deviation;
- post-hoc analyses must not be presented as pre-specified;
- exploratory outputs must not overwrite confirmatory outputs.

Adjudication occurs only after reliability metrics are computed and committed.

---

## Intended primary endpoint

Risk difference in explicit-reply rate for the draft confirmatory contrast
`primary_alignment`: **non_opposed minus opposed**, on adjudicated labels for
the frozen main sample, with a questioner-cluster bootstrap confidence
interval.

Definitions (draft, not frozen):

- `opposed` = individual MP investiture vote **no** (2020-01-07, DSCD-14-PL-4);
- `non_opposed` = investiture vote **sí** or **abstención** (raw categories
  `supported` and `abstained`).

Raw `formation_vote_alignment` ∈ {supported, opposed, abstained} remains the
descriptive variable. Exact decision rule, equivalence margin, and N are not
frozen (see unresolved items).

---

## Protocol freeze (planned)

Before main sampling and main annotation: deposit hypotheses, primary endpoint,
analysis code, alignment rule, exclusions, N, sampling seeds, and codebook hash
in a timestamped registry (OSF or Zenodo protocol record). Annotators acknowledge
the codebook hash.

---

## Phase 2 verified source and eligibility facts (2026-09-29)

Status remains **DRAFT — NOT PREREGISTERED**. These facts update Phase 0 pins
after acquisition. They do **not** freeze alignment, N, seeds, codebook, or the
primary hypothesis decision rule.

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
  `r1_text`, and optional `q2_text`/`r2_text` (provenance only). Primary coding
  target remains registered + Q1 + R1.
- **Eligibility:** XIV; PM oral-question section / PM FORMULA; R1 speaker
  `who = #PedroSánchezPérezCastejón`; non-empty registered question, Q1, R1;
  `link_status` in `{exact, high_confidence}`.
- **Linkage:** sitting date + questioner name against Congreso initiative
  records for that day's TEI/gap expedientes; TEI note expediente used only when
  name-confirmed (TEI notes are sometimes misaligned). No LLM / embedding
  linkage.
- **Answerer criterion:** first response utterance `who` equals ParlaMint person
  id for Pedro Sánchez Pérez-Castejón; ministerial substitutes are out of pool.
- **Exclusions from sampling:** Phase-0 probe expedientes; Phase-2 linkage-QA
  rows (hash-ranked, not a scientific seed); SPDB previous-paper sitting dates
  when any candidate falls on those dates (Phase 2 observed **zero** overlap).
- **Canonical pool:** `_internal/data_private/eligible_pool_full.parquet`
  (private full text). Public projection:
  `data/derived/eligible_pool_metadata_preannotation.csv` (identifier-only).
- **Seeds:** `development`, `calibration`, and `main_sample` remain **null**.

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

- **Primary confirmatory contrast:** `primary_alignment` =
  **opposed** vs **non_opposed**.
- **Construction:** from raw individual-MP investiture categories;
  `non_opposed` = supported ∪ abstained.
- **Rationale:** single interpretable opposition contrast; avoids two thin
  n≈18 primary strata; keeps sí vs abstención visible descriptively; aligns
  with a single confirmatory risk difference.
- **Secondary / descriptive:** report exchange and questioner counts (and later
  rates, only after annotation) by raw supported / opposed / abstained.
- **Planned lightweight robustness (at analysis, not yet frozen):**
  questioner-level displays; optional leave-one-dominant-questioner-out
  sensitivity; optional secondary contrast opposed vs supported only.
- **Detail:** `_internal/reports/CONFIRMATORY_CONTRAST_DESIGN.md`

---

## Currently unresolved decisions

- Whether XII post-censure is included as secondary scope
- **Freeze** of `formation_vote_alignment` / `primary_alignment` mapping
  (`alignment_table.yaml` still `draft_not_frozen`)
- Whether opposed-vs-supported-only is a pre-specified secondary contrast at
  freeze
- Final sample size N
- Exact Bull-derived codebook definitions and Spanish examples
- Calibration performance gates (numeric thresholds to confirm at freeze)
- Final statistical decision rule (including any equivalence margin)
- Named scientific seed values (`calibration`, `main_sample`, etc.)
- Final Congreso full-text Zenodo packaging under aviso-legal conditions

---

## Related documents

- `DECISIONS.md` — append-only decision log
- `SOURCE_REGISTRY_DRAFT.yaml` — source pins (draft)
- `seeds.yaml` — named seeds (all pending until freeze)
- `../docs/licensing.md` — licensing audit status
- `../manifests/release_manifest.schema.json` — release provenance schema
