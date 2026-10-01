# Development packet schema (Phase 4.2)

**Status:** DRAFT template for the **development exercise** only.  
**Not** gold / validation / benchmark / calibration / reliability.

## Purpose

Support expert linguists testing whether codebook v0.2 is understandable.

## Source units

Defined in `development_set_manifest.yaml`:

- ParlaMint-ES PM FORMULA exchanges;
- XIII preferred + XII post-censure supplement;
- `n_units = 15`;
- `exclusion_from_main_sampling: true`;
- outside XIV eligible population.

## Annotator-facing columns (CODING sheet)

| Column | Required | Values |
|--------|----------|--------|
| `unit_id` | yes (prefilled) | opaque `dev_*` id |
| `registered_question` | yes (prefilled) | institutional anchor text |
| `Q1` | yes (prefilled) | oral question turn |
| `R1` | yes (prefilled) | PM first response |
| `reply_status` | yes (empty) | `explicit_reply` \| `intermediate_reply` \| `non_reply` |
| `borderline` | yes (empty) | `yes` \| `no` |
| `confidence` | optional | `low` \| `medium` \| `high` |
| `notes` | optional | free text |

## Forbidden columns

Do **not** include: party, parliamentary group, MP name as metadata, alignment,
vote, legislature, `formation_vote_alignment`, `primary_alignment`.

Natural mention of a name **inside** Q1/R1 text may remain.

## Workbook sheets

| Sheet | Content |
|-------|---------|
| `INSTRUCTIONS` | Exercise constraints |
| `CODING` | Blinded units + empty label columns |
| `FEEDBACK` | Codebook-improvement questions |
| `PACKET_META` | annotator id, codebook version, date |

## Feedback items

1. Was the category decision clear?
2. What rule was missing?
3. What wording in the codebook caused uncertainty?
4. Would another expert likely make the same decision?

## Provenance

Private package provenance:
`_internal/development/DEVELOPMENT_PACKAGE_PROVENANCE.json`

Fields include: `development_source`, `development_ids`, `codebook_version`,
`creation_date`, `packet_hashes`.

## Files

| Path | Role |
|------|------|
| `_internal/development/development_annotator_A.xlsx` | Annotator A packet |
| `_internal/development/development_annotator_B.xlsx` | Annotator B packet |
| `_internal/development/development_annotator_*_coding.csv` | Coding-sheet CSV twin |
| `_internal/development/development_feedback_form.md` | Feedback companion |
| `_internal/reports/DEVELOPMENT_EXERCISE_INSTRUCTIONS.md` | Human instructions |
