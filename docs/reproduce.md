# Reproduce

## Environment

From the package root:

```bash
uv sync --all-extras
uv run python scripts/reproduce_public_agreement.py
make test
make hygiene
```

Requires Python ≥ 3.11 (installed via `uv` if needed).

## What public reproduction covers (v1.0.1)

From `data/HUMAN_EVIDENCE_67_PUBLIC.csv` alone:

- per-exercise raw agreement;
- three-category Cohen’s κ and nominal Krippendorff’s α;
- explicit-versus-rest binary κ (three-category exercises);
- Round 1 initial N=18 and final N=20;
- pooled Round 1 + Round 2 metrics;
- redesigned binary-validation κ, marginals, κ_max;
- disagreement-direction counts;
- bootstrap percentile 95% intervals (5,000 resamples; seed `20261020`) with
  invalid-draw and zero-κ diagnostics.

Outputs:

- `data/derived/measurement_agreement_summary.json`
- `data/derived/measurement_agreement_public_repro.json`

## What remains excluded

- Congreso / oral-turn full text;
- annotator free-text comments and original DOCX/XLSX returns;
- XIV reply / responsiveness outcomes;
- AI reply labels.

Pipeline targets that acquire ParlaMint/Congreso caches or build annotator
packets expect a private monorepo layout and are not required for the public
agreement recomputation path.
