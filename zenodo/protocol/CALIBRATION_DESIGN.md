# Calibration design (reply_status) — DRAFT

**Status:** design only. Seeds unset. Units **not** drawn yet.  
**Updated:** 2026-10-05 (Phase 4.4 — codebook v0.3 draft; calibration still undrawn)  
**Related:** `reply_status_codebook_v0.3.md` (DRAFT — NOT FROZEN);
`reply_status_codebook_v0.2.md` (preserved);
`development_set_manifest.yaml`

This document prepares the two-round calibration workflow. It does **not**
execute calibration coding or freeze the codebook.

---

## Hard rule

**Do not** use the XIV PM eligible pool (n=100) for development or calibration.

---

## Development corpus (Phase 4.1 — built)

| Field | Value |
|-------|-------|
| Manifest | `development_set_manifest.yaml` |
| Source | ParlaMint-ES PM FORMULA exchanges |
| Preferred legislature | **XIII** |
| Supplement | XII post-censure (Sánchez) to reach n |
| N | 15 |
| Selection | deterministic hash within legislature preference |
| Reliability use | **Forbidden** |
| Main sampling | `exclusion_from_main_sampling: true` |

Private blinded packet:
`_internal/data_private/development/out_of_pool/`.

**Superseded:** XIV in-pool development_codebook n=15 (provenance retained under
`_internal/data_private/development/superseded_xiv_inpool_2026-10-01/`; XIV
units restored to sampling frame).

---

## Calibration corpus (plan only — not drawn)

Same out-of-pool population family (XIII first, XII supplement as needed).
**Fresh** units with no overlap with the development 15.

| Set | N | Purpose | Reliability? | Seed |
|-----|---|--------|--------------|------|
| Development | 15 | Codebook examples / hard-case refinement | **No** | null (hash rule only) |
| Calibration Round 1 | 20 | Independent coding → discussion → revision | Exploratory only | null until freeze |
| Calibration Round 2 | 20 fresh | Independent coding → discussion → revision | Pre-freeze check | null until freeze |
| Main XIV frame | census/sample TBD | Study labels | Yes (after freeze) | null until freeze |

---

## Coding order within a unit

1. Question-side pass: `question_form`, `question_confrontational`,
   `question_target_type` (must not dictate reply label).
2. Reply pass: three-level `reply_status` against **Q1** (registered as anchor).

---

## Round 1 (n=20, out-of-pool, not drawn)

1. Draw 20 units from out-of-pool corpus excluding development IDs, using a
   frozen calibration seed (still unset).
2. Blinded packets must **display** `registered_question`, `Q1`, `R1` in that
   order (codebook v0.3 packet rule; validate with `scse.packet_validation`).
3. Two annotators code **independently** with codebook v0.3 (DRAFT).
4. Provisional agreement for discussion only.
5. Discuss; revise guidelines if needed. Case 7 of the development set remains
   outside calibration.

## Round 2 (n=20 fresh, out-of-pool, not drawn)

1. Draw 20 new out-of-pool units (no overlap with development or Round 1).
2. Independent coding; discussion; further edits allowed.
3. Then: decide freeze thresholds, hash codebook, deposit, annotator acknowledge.

Do **not** draw rounds until the seed is set in `seeds.yaml`.

---

## Proposed reliability metrics (thresholds TBD at freeze)

| Metric | Role |
|--------|------|
| Krippendorff’s α on three-level `reply_status` | Primary multi-category agreement |
| Cohen’s κ on three-level codes | Two-coder summary |
| Binary **explicit vs not-explicit** (κ / α + confusion matrix) | Sensitivity aligned with primary estimand |
| Optional ordinal / weighted agreement | Only if freeze treats levels as ordered |

Preserve both annotators’ original labels through adjudication.

---

## Packet + provenance schemas

- `zenodo/schemas/annotator_packet_row.schema.json`
- `zenodo/schemas/annotation_row.schema.json`
- `zenodo/protocol/packet_templates/annotator_packet_header.csv`

Required provenance: `unit_id`, `annotator_id`, `codebook_version`,
`codebook_hash`, `packet_version`, `coded_on`.
