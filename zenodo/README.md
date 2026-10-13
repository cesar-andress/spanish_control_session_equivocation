# Reply Explicitness in Spanish Prime-Ministerial Control Sessions

Project slug: `spanish_control_session_equivocation`

## What this project studies

A human-annotated corpus study of first-response explicitness in Spanish
parliamentary control sessions. Expert annotators code whether the Prime
Minister's first response is an explicit reply, a partial reply, or an absence
of reply to a registered oral question (anchored by the oral turn).

## Primary question

How explicit-reply rates vary across a pre-defined formation-vote alignment
contrast of the questioner (opposed vs non-opposed), in descriptive terms only.

This is an observational contrast, not a causal claim. Confrontational question
formulation is strongly imbalanced by alignment in the XIV pool.

## Current status (Phase 6A)

- Sources acquired; eligible pool built (100 linked eligible XIV exchanges).
- Linkage-QA (n=30) restored to the main frame after contamination audit.
- Phase-0 probes (n=3) remain excluded → **pre-outcome main frame N=97**.
- Out-of-pool development and Calibration Round 1 completed; Round 2 pending.
- **No XIV reply_status labels exist.**
- Main annotation packets are **not** issued until the codebook is frozen.
- Public projections are identifier / metadata only (no Congreso full text).

## Research workflow

1. development (out of pool)
2. calibration (out of pool)
3. protocol freeze
4. main annotation
5. reliability
6. adjudication
7. analysis
8. release

## Repository layout

| Path | Role |
|------|------|
| `protocol/` | Draft study protocol and decision log (not yet preregistered) |
| `data/derived/` | Public-safe metadata projections |
| `src/scse/` | Analysis and pipeline package |
| `tests/` | Unit and hygiene tests |
| `outputs/` | Generated tables and figures (shells + pre-outcome assets) |
| `docs/` | Licensing notes and reproduction docs |
| `manifests/` | Release and provenance manifests |

Private working material lives outside this public tree (project `_internal/`).
It must never be copied into a Zenodo or GitHub public release.

## Reproducibility commands

From this directory (`zenodo/`):

```text
make help
make test
make hygiene
uv run python scripts/build_phase6a_preoutcome.py   # rebuild pre-outcome assets
```

Later-phase Make targets fail safely until their phase starts.

## Licensing

See `docs/licensing.md`. ParlaMint-ES: CC BY 4.0. Congreso full-text public
bundling: unresolved / identifier-based until cleared.

## Computational requirements

CPU-only. No GPU, torch, or transformers.
