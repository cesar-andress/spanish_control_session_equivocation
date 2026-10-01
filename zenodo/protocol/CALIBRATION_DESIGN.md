# Calibration design (reply_status) — DRAFT

**Status:** design only. Seeds unset. Units **not** drawn yet.  
**Updated:** 2026-10-01 (Phase 4A — out-of-pool development/calibration)  
**Related:** `reply_status_codebook_v0.1.md` (DRAFT — NOT FROZEN; revise to v0.2
for Q1-target rule); `_internal/reports/PROTOCOL_REFINEMENT_AFTER_CLAUDE.md`

This document prepares the two-round calibration workflow. It does **not**
execute calibration coding or freeze the codebook.

---

## Hard rule (Phase 4A)

**Do not** use the XIV PM eligible pool (n=100) for development or calibration.
Every XIV pool item burned on instrument work is lost to the primary study.

---

## Development / calibration corpus (plan only)

| Preference | Source | Notes |
|------------|--------|-------|
| **Preferred** | Previous legislature PM control sessions in ParlaMint-ES (candidate **XIII**) | Same institutional genre; different population from XIV primary pool |
| Fallback | XIV oral questions to **ministers** (not PM) | Practice only; answerer differs — document caveat |

Acquisition, linkage, and packet build for the out-of-pool corpus are **not**
executed in Phase 4A.

**Superseded:** Phase-4 in-pool development set (n=15,
`development_codebook`). Those units were not reply-coded for outcomes;
restoration to the XIV sampling frame is recommended so the obsolete plan does
not permanently shrink the census.

---

## Separation of sets

| Set | N (planned) | Source | Purpose | Reliability? | Seed |
|-----|-------------|--------|---------|---------------|------|
| Development | TBD (e.g. 15–20) | Out-of-pool (XIII PM preferred) | Codebook examples / hard-case refinement | **No** | null until freeze |
| Calibration Round 1 | 20 | Out-of-pool, fresh | Independent coding → discussion → revision | Exploratory only | null until freeze |
| Calibration Round 2 | 20 fresh | Out-of-pool | Independent coding → discussion → revision | Pre-freeze check | null until freeze |
| Main XIV frame | census or sample TBD | XIV eligible pool | Study labels | Yes (after freeze) | null until freeze |

**Hard exclusions from XIV scientific samples:** Phase-0 probes; linkage QA
(n=30). Out-of-pool development/calibration units never enter the XIV frame.

---

## Coding order within a unit

1. Question-side pass (no R1, or R1 hidden): `question_form`,
   `question_confrontational`, and draft `question_target_type`.
2. Reply pass: three-level `reply_status` against **Q1** (registered as anchor).

---

## Round 1 (n=20, out-of-pool)

1. Draw 20 units from the out-of-pool development corpus using a frozen
   calibration seed (still unset).
2. Build **blinded** packets (`unit_id`, `registered_question`, `Q1`, `R1` only;
   no party/alignment/questioner meta).
3. Two annotators code **independently** with the current draft codebook.
4. Compute provisional agreement for discussion only — **not** a freeze gate yet.
5. Discuss disagreements; revise guideline text → draft v0.2+.

## Round 2 (n=20 fresh, out-of-pool)

1. Draw 20 **new** out-of-pool units (no overlap with Round 1 / development).
2. Blinded packets; independent coding with the revised draft.
3. Discussion; further guideline edits allowed.
4. Then: decide freeze thresholds, hash codebook, deposit, annotator acknowledge.

Do **not** draw rounds until the relevant seed is explicitly set in
`seeds.yaml` and the out-of-pool corpus exists.

---

## Proposed reliability metrics (thresholds TBD at freeze)

| Metric | Role |
|--------|------|
| Krippendorff’s α on three-level `reply_status` | Primary multi-category chance-corrected agreement |
| Cohen’s κ (two coders) on three-level codes | Familiar two-coder summary |
| Binary sensitivity: **explicit vs not-explicit** (κ / α + confusion matrix) | Aligns with primary estimand dichotomisation |
| Optional ordinal / weighted agreement | Only if freeze treats levels as ordered; justify explicitly |

**Candidate** floors from external review (α ≥ ~0.67 floor; ~0.80 target) are
**not locked** in Phase 4A. Do not choose a threshold because it yields a
preferred political result. Thresholds are set **before** main XIV outcomes
exist.

Preserve both annotators’ original labels through adjudication.

---

## Packet + provenance schemas

- Annotator-facing row: `zenodo/schemas/annotator_packet_row.schema.json`
- Label row provenance: `zenodo/schemas/annotation_row.schema.json`
- Header template: `zenodo/protocol/packet_templates/annotator_packet_header.csv`

Required provenance on every future label:
`unit_id`, `annotator_id`, `codebook_version`, `codebook_hash`,
`packet_version`, `coded_on`.
