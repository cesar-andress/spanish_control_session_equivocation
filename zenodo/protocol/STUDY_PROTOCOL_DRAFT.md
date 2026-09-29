# Study protocol — DRAFT

**Status: DRAFT — NOT YET FROZEN OR PREREGISTERED**

This document records design intentions for scaffolding and planning. It is
**not** a preregistration. Hypotheses, N, seeds, codebook hashes, and analysis
code will be deposited only at protocol freeze (planned Phase 5).

Working title: *Answering Allies and Adversaries: Equivocation in
Prime-Ministerial Replies during Spanish Parliamentary Control Sessions*

Project slug: `spanish_control_session_equivocation`

---

## Research question

In Spanish Congress control sessions, does the Prime Minister give explicit
replies to pre-registered oral questions at different rates depending on the
political alignment of the questioner's parliamentary group?

This is an observational contrast. It is not a causal claim.

---

## Population (concept)

Oral questions addressed to the Presidente del Gobierno in Congress plenary
control sessions during the Sánchez premiership, within the coverage of the
pinned ParlaMint-ES release (exact release pending), answered in person by the
Prime Minister, with recoverable registered question text and complete
transcription of the questioner's opening turn and the Prime Minister's first
response.

Exact date bounds, exclusions, and source pins are unresolved (see below).

---

## Intended unit

One exchange comprising:

1. the registered (written) oral question;
2. the questioner's opening turn;
3. the Prime Minister's first response.

The réplica and dúplica are out of scope for the primary coding unit.

---

## Intended annotation construct

`reply_status` with a three-level structure conceptually based on the Bull
reply / non-reply tradition:

- explicit reply
- intermediate reply
- non-reply

Exact operational definitions are **not frozen** and must not be invented in
the scaffold phase. A Spanish-adapted codebook is planned for Phase 3.

Additional planned fields (not yet operationalised): question form;
equivocation type for non-explicit responses; borderline flag; free-text note.

---

## Annotators and workflow separation

Two independent expert annotators (authors A and B). A third author runs the
pipeline and does not annotate.

Intended sequence:

development → calibration → protocol freeze → main annotation → reliability →
adjudication → analysis

Integrity constraints:

- calibration items must not silently enter main evaluation;
- adjudicated labels must not overwrite original independent labels;
- sampling must not occur after outcome inspection;
- codebook changes after main annotation begins require a logged protocol
  deviation;
- post-hoc analyses must not be presented as pre-specified;
- exploratory outputs must not overwrite confirmatory outputs.

Adjudication occurs only after reliability metrics are computed and committed.

---

## Intended primary endpoint

Risk difference in explicit-reply rate between pre-defined alignment strata
(non-opposition minus opposition), on adjudicated labels for the frozen main
sample, with a questioner-cluster bootstrap confidence interval.

Exact decision rule, equivalence margin, and N are not frozen (see unresolved
items).

---

## Protocol freeze (planned)

Before main sampling and main annotation: deposit hypotheses, primary endpoint,
analysis code, alignment rule, exclusions, N, sampling seeds, and codebook hash
in a timestamped registry (OSF or Zenodo protocol record). Annotators acknowledge
the codebook hash.

---

## Currently unresolved decisions

- Exact ParlaMint-ES release (URL, version, checksum, licence)
- Exact Congreso oral-question source / API and reuse terms
- Eligible Sánchez date range and hard exclusions (including prior-paper sitting
  dates once verified)
- Operational definition of opposition / non-opposition and `alignment_table.yaml`
- Realised eligible pool size and stratum sizes
- Final sample size N
- Exact Bull-derived codebook definitions and Spanish examples
- Calibration performance gates (numeric thresholds to confirm at freeze)
- Final statistical decision rule (including any equivalence margin)
- Licence / redistribution terms for derived data
- Named scientific seed values (`calibration`, `main_sample`, etc.)

---

## Related documents

- `DECISIONS.md` — append-only decision log
- `seeds.yaml` — named seeds (all pending until freeze)
- `../docs/licensing.md` — licensing audit status
- `../manifests/release_manifest.schema.json` — release provenance schema
