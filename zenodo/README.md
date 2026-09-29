# Answering Allies and Adversaries

**Equivocation in Prime-Ministerial Replies during Spanish Parliamentary Control Sessions**

Project slug: `spanish_control_session_equivocation`

## What this project studies

A planned human-annotated corpus study of reply and equivocation behaviour in Spanish parliamentary control sessions. Expert annotators will code whether the Prime Minister's first response constitutes an explicit reply, an intermediate reply, or a non-reply to a pre-registered oral question.

## Primary question

Whether explicit-reply rates differ across a pre-defined political-alignment contrast of the questioner's parliamentary group.

This is an observational contrast, not a causal claim.

## Current status

**Project scaffold only.**

- No corpus data have been acquired in this repository yet.
- No sample has been drawn.
- No human annotation has been performed.
- No empirical results exist.

## Research workflow

The intended sequence is:

1. development
2. calibration
3. protocol freeze
4. main annotation
5. reliability
6. adjudication
7. analysis
8. release

Calibration units must not enter main evaluation. Independent labels are preserved; adjudication does not overwrite them. Codebook changes after main annotation begins require a logged protocol deviation.

## Repository layout

| Path | Role |
|------|------|
| `protocol/` | Draft study protocol and decision log (not yet preregistered) |
| `data/` | Pinned source manifests and derived tables (empty until Phase 2) |
| `src/scse/` | Analysis and pipeline package |
| `tests/` | Unit and hygiene tests |
| `outputs/` | Generated tables and figures |
| `docs/` | Licensing notes and reproduction docs |
| `manifests/` | Release and provenance manifests |

Private working material lives outside this public tree (project `_internal/`). It must never be copied into a Zenodo or GitHub public release.

## Reproducibility commands

From this directory (`zenodo/`):

```text
make help         # list targets
make test         # run unit and hygiene tests (available now)
make data         # Phase 2: acquire pinned sources (not yet)
make pool         # Phase 2: build eligible exchange pool (not yet)
make power        # Phase 2: precision simulation (not yet)
make calibrate    # Phase 4: calibration sample (not yet)
make freeze       # Phase 5: protocol freeze + main sample (not yet)
make packets      # Phase 6: annotator packets (not yet)
make validate     # Phase 6: validate returned packets (not yet)
make agreement    # Phase 7: reliability metrics (not yet)
make adjudicate   # Phase 7: adjudication sheets (not yet)
make analysis     # Phase 8: pre-registered analyses (not yet)
make figures      # Phase 8: figures (not yet)
make paper-assets # copy outputs into ../paper/ (not yet)
make release      # build release manifest (not yet)
```

Targets that depend on future phases exit with a clear message and do not fabricate outputs.

## Computational requirements

CPU only. No GPU, no LLM labelling, and no deep-learning stack are part of the current design.

## Licensing

- **Code:** MIT (see `LICENSE`).
- **Data / derived corpus material:** redistribution terms are **to be verified** against ParlaMint-ES and Congreso open-data licences before any public data release. See `docs/licensing.md`.

## Citation

See draft `CITATION.cff` (pre-release; no DOI yet).
