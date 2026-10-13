# Derived public-safe metadata

## `eligible_pool_metadata_preannotation.*`

Identifier-only projection of the Phase-2 pool (eligible and non-eligible rows).

- **Not** a labelled research dataset
- **No** `reply_status` / outcomes
- Congreso and ParlaMint full texts omitted (see `docs/licensing.md`)
- Full working pool (private): `_internal/data_private/eligible_pool_full.parquet`

After Phase 6A, active linkage-QA sampling exclusions are cleared; Phase-0
probes remain excluded. Eligible ∧ ¬exclude_from_sampling = **97**.

## `main_frame_metadata_preannotation.*`

Public-safe roster of the pre-outcome main frame (n=97), including
`formation_vote_alignment`, `primary_alignment`, and question-side codes.
**No** full registered/Q1/R1 text strings.

See `DATA_DICTIONARY_PREOUTCOME.md`.
