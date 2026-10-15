# Calibration design (reply_status)

**Status:** Round 2 in progress (independent returns not yet inspected for
protocol lock). Round-2 **decision rule locked prospectively** (Phase 6B).  
**Updated:** 2026-10-13 (Phase 6B)  
**Codebook:** `reply_status_codebook_v0.3.md` (Round-2 Gate C STOP; no v0.4)

Do **not** use the XIV PM eligible pool for development or calibration.

---

## Development corpus

| Field | Value |
|-------|-------|
| Manifest | `development_set_manifest.yaml` |
| N | 15 OOP |
| Reliability use | **Forbidden** |

## Calibration Round 1

| Field | Value |
|-------|-------|
| N | 20 OOP |
| Seed | `2071684612` |
| Agree (n=20) | 16 / 20 |
| Cohen κ (3-way) | ≈0.672 |
| Krippendorff α | ≈0.669 |
| Disagreements | 5, 6, 7, 10 (joint review issued) |

## Calibration Round 2

| Field | Value |
|-------|-------|
| N | 20 new OOP |
| Seed | `322720977` |
| Manifest | `calibration_round2_manifest.yaml` |
| Round 3 | **Not** planned by default |

Human packets returned 2026-10-15 and ingested. Agreement computed before
discussion. Locked rule applied → **Gate C (STOP)**. See
`_internal/reports/CALIBRATION_ROUND2_AGREEMENT.md`.

---

## Prospective Round-2 decision rule (LOCKED before returns)

**Primary three-category metric:** Krippendorff’s α, nominal (three reply-status
categories).

Also report (always): raw three-category agreement; Cohen’s κ (three-category);
nominal Krippendorff α; binary explicit vs non-explicit agreement; binary Cohen
κ; confusion matrix.

### A — Retain three-category primary scheme

If nominal α ≥ **0.67**:

- retain the three-category response scheme;
- no Round 3;
- transcribe agreed joint clarifications faithfully into codebook v0.4;
- freeze the guide;
- proceed to main annotation.

### B — Binary primary endpoint; three-category secondary

If nominal α < **0.67** BUT binary explicit vs non-explicit Cohen κ ≥ **0.67**:

- no Round 3;
- retain collected three-category judgements;
- make **explicit vs non-explicit** the primary analytic endpoint;
- treat the three-category distribution as secondary/descriptive and report
  its weaker reliability transparently.

### C — Stop

If nominal α < **0.67** AND binary explicit vs non-explicit κ < **0.67**:

- **STOP** before main annotation;
- do not create Round 3 automatically;
- reconsider the measurement scheme.

Do **not** optimise this rule after seeing Round-2 results.

### Applied outcome (2026-10-15)

**Gate C.** Observed α ≈ 0.126; binary κ ≈ 0.121 (n=20 complete pairs after
case-5 completion). STOP before main; no automatic Round 3; codebook remains
v0.3.

---

## Independence / agreement timing

Agreement is calculated **before** discussion. Original independent labels are
preserved. Round 1 remains exploratory relative to the main freeze.
