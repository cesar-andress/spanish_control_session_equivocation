# Data dictionary — `HUMAN_EVIDENCE_67_PUBLIC.csv`

Public unit-level evidence table for the 67 independently double-coded
out-of-pool (OOP) exchanges used in the measurement paper.

**Package version:** 1.0.1  
**Row count:** 67  
**Coder identifiers:** anonymous `coder_A` / `coder_B` only (stable across all rows)

## Purpose

This table allows independent recomputation of:

- raw agreement;
- three-category Cohen’s κ and nominal Krippendorff’s α;
- explicit-versus-rest binary κ (three-category exercises only);
- Round 1 initial N=18 and final N=20;
- pooled Round 1 + Round 2 metrics;
- redesigned binary-validation κ, marginals, maximum agreement, and κ_max;
- disagreement-direction counts.

It does **not** redistribute restricted source text or private annotator comments.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| `public_unit_id` | string | Opaque unit identifier used in the measurement programme |
| `exercise` | string | One of `development`, `calibration_round1`, `calibration_round2`, `binary_validation` |
| `case_number` | integer | Case number within the exercise packet |
| `instrument` | string | Instrument / codebook version applied for that exercise |
| `label_system` | string | `three_category` or `binary_direct_resolution` |
| `legislature` | string | Source legislature label where recorded (e.g. `XII`, `XII_pre`, `XIII`) |
| `parlamint_session_id` | string | ParlaMint-ES session / document id (CC BY 4.0 attribution) |
| `parlamint_q1_utterance_id` | string | ParlaMint utterance id for the first oral question turn |
| `parlamint_r1_utterance_id` | string | ParlaMint utterance id for the first reply turn |
| `congreso_expediente` | string | Congreso initiative / expediente identifier when available (identifier only). Empty for these OOP audits when not stored |
| `coder_A_label` | string | Independent label from annotator A |
| `coder_B_label` | string | Independent label from annotator B |
| `coder_A_doubtful` | 0/1 | Annotator A doubtful / borderline flag |
| `coder_B_doubtful` | 0/1 | Annotator B doubtful / borderline flag |
| `usable_in_initial_round1_18` | 0/1 or empty | For Round 1 only: `1` if pair counted in initial N=18; `0` if excluded. Empty for other exercises |
| `administrative_clarification_flag` | 0/1 | `1` for the two Round-1 cases whose Annotator B marks were later clarified administratively (missing / multiple marks). **Not adjudication.** Annotator A values were not revealed during clarification |

## Exercises

| `exercise` | N | Instrument | Label system |
|------------|--:|------------|--------------|
| `development` | 15 | `reply_status_pre_v0.3_development` | three_category |
| `calibration_round1` | 20 | `reply_status_v0.3` | three_category |
| `calibration_round2` | 20 | `reply_status_v0.3` | three_category |
| `binary_validation` | 12 | `direct_resolution_v1.0-validation` | binary_direct_resolution |

## Label vocabularies

### Three-category (`label_system = three_category`)

Spanish codebook labels (as coded):

- `respuesta explícita`
- `respuesta parcial o intermedia`
- `ausencia de respuesta`

English equivalents used internally by metrics code:

- `explicit_reply` / `intermediate_reply` / `non_reply`

**Explicit-versus-rest collapse** (secondary binary metric on three-category exercises only):
`respuesta explícita` → explicit; otherwise → non_explicit.

### Binary redesign (`label_system = binary_direct_resolution`)

- `direct_resolution_yes`
- `direct_resolution_no`

**Do not pool** the redesigned binary validation with the three-category
explicit-versus-rest collapse. They are different instruments.

## Coder A / Coder B convention

- `coder_A` and `coder_B` are stable anonymous labels for the two expert
  annotators who independently double-coded all 67 units.
- Personal names are intentionally omitted from this public table.
- Disagreement direction in public recomputation:
  - `coder_A_more` = A’s label is higher on the ordered responsiveness scale;
  - `coder_B_more` = B’s label is higher.
  Order (three-category): ausencia < parcial < explícita.  
  Order (binary): No < Yes.

## Round 1 initial-18 vs final-20

- Initial N=18: rows with `exercise=calibration_round1` and
  `usable_in_initial_round1_18=1`.
- Final N=20: all Round-1 rows (includes the two administratively clarified
  cases, `administrative_clarification_flag=1`, cases 5 and 10).
- Clarification corrected Annotator B’s return where marks were missing or
  multiply marked. It is **not** joint adjudication and does not use Annotator A’s labels.

## Why source text and comments are excluded

- Congreso registered-question and oral-turn **full text** is not redistributed
  while reuse packaging remains identifier-based.
- Annotator free-text comments and original DOCX/XLSX returns remain private.
- ParlaMint utterance identifiers are included so readers can locate the
  corresponding turns in the CC BY 4.0 ParlaMint-ES release (handle 11356/2004).

## How to recompute

From the package root:

```bash
uv sync --all-extras
uv run python scripts/reproduce_public_agreement.py
```

Outputs:

- `data/derived/measurement_agreement_summary.json`
- `data/derived/measurement_agreement_public_repro.json` (includes bootstrap invalid-draw counts)

Bootstrap: 5,000 resamples; seed `20261020`; percentile 95% intervals;
degenerate/invalid draws counted and excluded from percentiles.
