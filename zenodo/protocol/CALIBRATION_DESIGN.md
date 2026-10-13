# Calibration design (reply_status) — Round 1 RETURNS INGESTED

**Status:** Calibration Round 1 returns complete after Jose Jaime mark
clarification (cases 5 and 10); agreement on n=20 recorded.  
**Updated:** 2026-10-13 (Phase 5A)  
**Related:** `reply_status_codebook_v0.3.md` (CALIBRATION VERSION — not frozen for
main study); `calibration_round1_manifest.yaml`; `seeds.yaml`;
`_internal/reports/CALIBRATION_ROUND1_AGREEMENT.md`

Do **not** freeze the main-study codebook yet. Proceed to disagreement
discussion for cases 5, 6, 7 and 10.

---

## Hard rule

**Do not** use the XIV PM eligible pool for development or calibration.

---

## Development corpus (Phase 4.1 — built)

| Field | Value |
|-------|-------|
| Manifest | `development_set_manifest.yaml` |
| N | 15 |
| Reliability use | **Forbidden** |

---

## Calibration Round 1 (Phase 5A — drawn)

| Field | Value |
|-------|-------|
| N | 20 |
| Manifest | `calibration_round1_manifest.yaml` |
| Seed | `2071684612` (derived; see seeds.yaml notes) |
| Source | ParlaMint-ES PM FORMULA outside XIV (X 2015, XI, XII, XIII); PM Sánchez or Rajoy |
| Development overlap | **0** (utterance-id check) |
| XIV overlap | **0** |
| Registered+Q1+R1 | required and displayed |
| Diversity rule | ≥2 `question_topic` and ≥2 `question_form` in the 20 (coded from registered+Q1 only; fixed before reply labels) |
| Human packets | `_internal/calibration_round1/` |
| Returned packets | `_internal/calibration_round1/returns/` |
| Codes / returns JSON | `_internal/data_private/calibration/round1/CALIBRATION_ROUND1_CODES.csv` |
| Agreement report | `_internal/reports/CALIBRATION_ROUND1_AGREEMENT.md` |
| Codebook | v0.3.0 |

### Round 1 agreement (before disagreement discussion)

| Field | Value |
|-------|-------|
| Complete pairs | 20 / 20 (after Jose Jaime mark clarification on 5 and 10) |
| First-pass usable pairs (2026-10-09) | 18 / 20 |
| Agree (n=20, adjusted) | 16 / 20 |
| Raw agreement | 0.800 |
| Cohen’s κ (3-way) | 0.672 |
| Krippendorff’s α | 0.669 |
| Disagreements | cases 5, 6, 7, 10 |

Question-side audit of the XIV eligible pool (no R1 outcomes):
`_internal/reports/QUESTION_SIDE_TOPIC_AND_DIVERSITY_AUDIT.md`.
Topic×alignment confound risk: **MEDIUM**. Main XIV pool not altered.

Remaining eligible OOP IDs reserved for Round 2+:
`_internal/data_private/calibration/round1/CALIBRATION_REMAINING_POOL_IDS.json`

## Round 2

**Not drawn.** Must not reuse Round 1 IDs.

---

## Coding order within a unit

1. Identify the communicative demand of the oral question (registered as anchor).
2. Assign three-level reply status under v0.3.

Question-side fields remain defined in the codebook for later study coding; the
Round 1 human booklet focuses on reply status only to keep burden light.

---

## Independence rule

No discussion between annotators until both completed packets are returned.
Agreement is calculated **before** any discussion. Original independent
responses are preserved.

---

## Proposed reliability metrics (after returns; thresholds TBD at freeze)

| Metric | Role |
|--------|------|
| Raw agreement | Descriptive |
| 3-category confusion matrix | Boundary inspection |
| Krippendorff’s α (nominal, three-level) | Multi-category agreement |
| Cohen’s κ (three-level) | Two-coder summary |
| Binary explicit vs not-explicit (agreement + κ) | Sensitivity aligned with primary estimand |

Implementation in `scse.calibration_metrics`; Round 1 diagnostics computed on
complete pairs only. Round 1 remains exploratory, not final validation.
