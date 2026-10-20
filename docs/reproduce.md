# Reproduce

## Environment

From the package root:

```bash
uv sync --all-extras
make test
make hygiene
```

Requires Python ≥ 3.11 (installed via `uv` if needed).

## What public reproduction covers

- package imports and seed utilities;
- public-tree hygiene scan;
- identifier-only derived metadata presence;
- aggregate agreement summary JSON.

## What public reproduction does not cover

Unit-level recomputation from original independent human labels requires private
materials that are intentionally excluded from this package. In the standalone
public clone, those tests are skipped. Aggregate locked metrics are published in
`data/derived/measurement_agreement_summary.json`.

Pipeline targets that acquire ParlaMint/Congreso caches or build annotator
packets expect a private monorepo layout and are not the public reproduction
path for v1.0.0.
