# Data dictionary — pre-outcome public projections (Phase 6B)

## `eligible_pool_metadata_preannotation.csv`

Identifier-only projection of the Phase-2 pool. **No** full text. **No**
`reply_status`.

After Phase 6B: no active `linkage_QA` or `phase0_feasibility_probe` sampling
exclusions on eligible rows. Eligible ∧ ¬exclude_from_sampling = **100**.

## `main_frame_metadata_preannotation.csv`

Public-safe main-frame roster (**n=100**), including:

- identifiers and linkage fields
- `formation_vote_alignment`, `primary_alignment` (descriptive grouping)
- `question_topic`, `question_form`
- `question_confrontational` — **exploratory/diagnostic rule-based indicator**
  only (not a validated mandatory human variable)

**Omits** full Congreso/ParlaMint spoken and registered text strings.

## Private

`_internal/data_private/main/` holds full texts for annotation preparation.
