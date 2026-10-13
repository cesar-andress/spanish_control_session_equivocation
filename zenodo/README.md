# Reply Explicitness in Spanish Prime-Ministerial Control Sessions

Project slug: `spanish_control_session_equivocation`

## What this project studies

A human-annotated corpus study of first-response explicitness in Spanish
parliamentary control sessions.

## Primary framing

Reply explicitness / responsiveness in first prime-ministerial responses.
Formation-vote alignment is a **descriptive contextual grouping**, not a
confirmatory causal contrast.

## Current status (Phase 6B)

- Eligible linked XIV exchanges: 100.
- QA30 + Phase-0 probes restored after contamination audit → **main frame N=100**.
- Round-2 decision rule locked prospectively (α 0.67 / binary κ fallback / STOP).
- Round 2 human returns pending; codebook still v0.3.
- **No XIV reply_status labels.** Main packets **not** issued.
- `question_confrontational`: exploratory/diagnostic rule-based indicator only.
- AI simulation **deferred**.

## Repository layout

| Path | Role |
|------|------|
| `protocol/` | Draft protocol, decisions, codebook, calibration design |
| `data/derived/` | Public-safe metadata projections |
| `src/scse/` | Pipeline package |
| `tests/` | Unit and hygiene tests |
| `outputs/` | Tables/figures (pre-outcome + shells) |

Private material: project `_internal/` (not for public release bags).

## Commands

```text
make test
make hygiene
uv run python scripts/build_phase6b_pre_round2_lock.py
```

## Licensing

See `docs/licensing.md`. Congreso full text: identifier-based until cleared.
