# Reproduce (scaffold)

## Environment

From the `zenodo/` directory:

```bash
uv sync --all-extras
make test
make hygiene
```

Requires Python >= 3.11 (installed via `uv` if needed).

## Phase status

Only environment setup, tests, and hygiene scans are available.

Targets such as `make data`, `make pool`, and later analysis commands exit with
an explicit phase-not-ready message and do not write fabricated outputs.
