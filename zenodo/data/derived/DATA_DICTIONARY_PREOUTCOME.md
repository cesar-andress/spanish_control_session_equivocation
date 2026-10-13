# Data dictionary — pre-outcome public projections

## `eligible_pool_metadata_preannotation.csv`

Identifier-only projection of the Phase-2 pool (eligible and non-eligible rows).
**No** registered/Q1/R1 full text. **No** `reply_status`.

Key fields: `exchange_id`, `expediente`, `date`, `session_id`, `questioner_id`,
`link_status`, `eligible`, `exclude_from_sampling`, `sampling_exclusion_reason`.

After Phase 6A: active `linkage_QA` sampling exclusions are cleared; Phase-0
probes remain excluded. Sampling/main frame among eligible = 97.

## `main_frame_metadata_preannotation.csv`

Public-safe main-frame roster (n=97). Includes pre-outcome metadata:

- identifiers and linkage fields
- `formation_vote_alignment`, `primary_alignment`
- `question_topic`, `question_form`, `question_confrontational`

**Omits** full Congreso/ParlaMint spoken and registered text strings.

## Private (not for public release)

`_internal/data_private/main/MAIN_FRAME_CORPUS_FULL.*` holds full texts for
annotation preparation. Do not bundle into Zenodo until Congreso packaging is
cleared.
