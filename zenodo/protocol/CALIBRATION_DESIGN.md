# Calibration design (reply_status) — DRAFT

**Status:** design only. Seeds unset. Units **not** drawn yet.  
**Date:** 2026-10-01  
**Related:** `reply_status_codebook_v0.1.md` (DRAFT — NOT FROZEN)

This document prepares the two-round calibration workflow. It does **not**
execute calibration coding or freeze the codebook.

---

## Separation of sets

| Set | N | Purpose | Reliability? | Sampling seed |
|-----|---|--------|--------------|---------------|
| Development | 15 | Codebook examples / hard-case refinement | **No** | null (deterministic hash rule only) |
| Calibration Round 1 | 20 | Independent coding → discussion → revision | Exploratory only | null until freeze |
| Calibration Round 2 | 20 fresh | Independent coding → discussion → revision | Pre-freeze check | null until freeze |
| Main sample | TBD | Confirmatory labels | Yes (after freeze) | null until freeze |

**Hard exclusions from all future scientific samples:** Phase-0 probes; linkage
QA (n=30); development_codebook (n=15). Calibration units, once drawn, must also
be excluded from the main sample.

Development IDs: `_internal/data_private/development/DEVELOPMENT_SET_MANIFEST.json`.

---

## Round 1 (n=20)

1. Draw 20 units from the current sampling frame (eligible and not
   `exclude_from_sampling`) using a **frozen calibration seed** (still unset).
2. Build **blinded** packets (`unit_id`, `registered_question`, `Q1`, `R1` only).
3. Two annotators code **independently** with codebook v0.1 (or successor draft).
4. Compute provisional agreement (α, κ) for discussion only — **not** a freeze gate
   yet.
5. Discuss disagreements; revise guideline text if needed → draft v0.2.

## Round 2 (n=20 fresh)

1. Draw 20 **new** units (no overlap with development, QA, phase0, R1).
2. Blinded packets; independent coding with the revised draft.
3. Discussion; further guideline edits allowed.
4. Then: decide freeze thresholds, hash codebook, deposit, annotator acknowledge.

Do **not** draw Round 1/2 until the calibration seed is explicitly frozen in
`seeds.yaml`.

---

## Proposed reliability metrics (thresholds TBD)

| Metric | Role |
|--------|------|
| Krippendorff’s α (nominal, 3-level `reply_status`) | Primary multi-category chance-corrected agreement |
| Cohen’s κ (two coders) | Familiar two-coder summary |
| Optional ordinal / quadratic-weighted κ | Only if freeze treats levels as ordered (explicit > intermediate > non-reply); justify because confirmatory endpoint later dichotomises explicit vs other |

**Do not** choose a numeric threshold because it yields a preferred political
result. Thresholds are set **before** main-sample outcomes exist.

---

## Packet + provenance schemas

- Annotator-facing row: `zenodo/schemas/annotator_packet_row.schema.json`
- Label row provenance: `zenodo/schemas/annotation_row.schema.json`
- Header template: `zenodo/protocol/packet_templates/annotator_packet_header.csv`

Required provenance on every future label:
`unit_id`, `annotator_id`, `codebook_version`, `codebook_hash`,
`packet_version`, `coded_on`.
