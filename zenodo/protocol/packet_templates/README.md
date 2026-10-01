# Annotator packet template (blinded)

**Status:** DRAFT template — not a live annotation packet.

## Columns shown to annotators

| Column | Role |
|--------|------|
| `unit_id` | Stable exchange id |
| `registered_question` | Official written question |
| `Q1` | Questioner opening turn |
| `R1` | PM first response |
| `reply_status` | Empty for coding |
| `borderline` | Optional |
| `confidence` | Optional |
| `notes` | Optional |

## Forbidden in annotator-facing sheets

Do **not** include:

- parliamentary group / party;
- `formation_vote_alignment` / `primary_alignment`;
- questioner name or speaker id;
- investiture vote category;
- session politics labels.

Those fields may exist only in private audit sidecars held by the pipeline
author.
