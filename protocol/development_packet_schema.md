# Development / annotation packet schema (from Phase 4.4 / codebook v0.3)

**Status:** DRAFT template for development, calibration and main packets.  
**Not** gold / validation / benchmark / reliability by itself.

## Purpose

Support expert linguists coding `reply_status` under
`reply_status_codebook_v0.3.md` (**DRAFT — NOT FROZEN**).

## Required displayed fields (mandatory)

Every ordinary unit **must** present, in this order:

1. `registered_question` — pregunta registrada  
2. `Q1` — pregunta oral  
3. `R1` — primera respuesta del Presidente del Gobierno  

Validation (`scse.packet_validation`) **fails** if any of these is missing or
whitespace-only.

**Exception:** if the registered question is genuinely unavailable, set
`registered_unavailable=true` **before** annotation and keep the unit out of
the ordinary circuit. Do not silently omit the registered text (Phase 4.3
defect in cases 12–13 of the first human booklet).

## Annotator-facing columns (CODING sheet)

| Column | Required | Values |
|--------|----------|--------|
| `unit_id` | yes (prefilled) | opaque id |
| `registered_question` | yes (prefilled, displayed) | institutional anchor text |
| `Q1` | yes (prefilled, displayed) | oral question turn |
| `R1` | yes (prefilled, displayed) | PM first response |
| `question_target_type` | study coding | see codebook |
| `question_form` | study coding | see codebook |
| `question_confrontational` | study coding | see codebook |
| `reply_status` | yes (empty until coded) | `explicit_reply` \| `intermediate_reply` \| `non_reply` |
| `borderline` | optional | boolean / yes\|no |
| `notes` | optional | free text |

Development exercise packets (Phase 4.2) used a reduced coding sheet without
question-side fields; future calibration/main packets should include them.

## Forbidden columns

Do **not** include: party, parliamentary group, MP name as metadata, alignment,
vote, legislature, `formation_vote_alignment`, `primary_alignment`.

Natural mention of a name **inside** Q1/R1/registered text may remain.

## Workbook sheets (typical)

| Sheet | Content |
|-------|---------|
| `INSTRUCTIONS` | Exercise / round constraints |
| `CODING` | Blinded units + empty label columns |
| `FEEDBACK` | Guide-improvement questions (development/calibration) |
| `PACKET_META` | annotator id, codebook version/hash, date |

## Provenance

Record: codebook version (`0.3.0` while draft), codebook hash (at freeze),
packet version, creation date, unit ids, exclusion from main sampling when
applicable.

## Related files

| Path | Role |
|------|------|
| `schemas/annotator_packet_row.schema.json` | JSON Schema |
| `src/scse/packet_validation.py` | Runtime validation |
| `protocol/packet_templates/annotator_packet_header.csv` | Header template |
| `protocol/reply_status_codebook_v0.3.md` | Coding instrument |
