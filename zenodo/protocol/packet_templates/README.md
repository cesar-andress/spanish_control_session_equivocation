# Annotator packet template (blinded)

**Status:** DRAFT template — not a live annotation packet.

## Columns shown to annotators

| Column | Role |
|--------|------|
| `unit_id` | Stable exchange id |
| `registered_question` | Official written question (anchor) |
| `Q1` | Questioner opening turn (judgement target) |
| `R1` | PM first response |
| `question_target_type` | Empty for coding |
| `question_form` | Empty for coding |
| `question_confrontational` | Empty for coding |
| `reply_status` | Empty for coding |
| `borderline` | Optional |
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
