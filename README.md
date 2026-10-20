# When Does a Reply Count as an Answer?

**Threshold Instability in Expert Coding of Spanish Parliamentary Replies**

Public research / reproducibility package **v1.0.0**.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23495525.svg)](https://doi.org/10.5281/zenodo.23495525)

## Archived release

| Field | Value |
|-------|-------|
| Archived release | **v1.0.0** (stable research package) |
| Zenodo DOI | [https://doi.org/10.5281/zenodo.23495525](https://doi.org/10.5281/zenodo.23495525) |
| Published | 2026-10-20 |

Cite the Zenodo DOI for the archived package. Post-release DOI metadata on the
default branch documents that archive; it was not necessarily present inside
the frozen v1.0.0 Git snapshot.

## What this release contains

This package supports a short **methodological / measurement** study of expert
agreement when coding whether a prime minister’s first reply resolves a
parliamentary oral question. It includes:

- analysis code (`src/scse/`);
- protocols and codebooks used in the sequential measurement programme;
- identifier-only public metadata for the XIV target frame (N=100 context);
- aggregate locked agreement summaries;
- pre-outcome tables/figures and measurement-paper figures;
- schemas, manifests, and reproducibility documentation.

**Version:** `v1.0.0`

## Research purpose

The study documents how inter-annotator agreement behaved across repeated
out-of-pool exercises (development, two three-category calibrations, and a
redesigned binary validation). It does **not** estimate substantive XIV
responsiveness rates.

**No substantive XIV reply / responsiveness outcomes are included.**

The instruments examined here are **not** claimed to be validated for main
annotation. The methodological paper was **not** preregistered as a separate
publication plan (calibration/validation gates were fixed during the original
measurement programme; the publication pivot came later).

## Package structure

| Path | Contents |
|------|----------|
| `src/scse/` | Python package (pool, calibration helpers, metrics, hygiene) |
| `protocol/` | Codebooks, calibration design, decisions log, manifests |
| `data/derived/` | Identifier-only metadata + aggregate agreement summary |
| `data/raw_pinned/` | ParlaMint pin provenance (no bulk corpus) |
| `outputs/` | Tables and figures |
| `schemas/` | JSON schemas |
| `manifests/` | Acquisition / release manifests |
| `docs/` | Licensing, reproduction, private-area boundary notes |
| `tests/` | Unit and hygiene tests |
| `scripts/` | Build/ingest helpers (many require private monorepo materials) |

## Reproduce (public package)

Requires Python ≥ 3.11 and [`uv`](https://github.com/astral-sh/uv).

```bash
uv sync --all-extras
make test
make hygiene
```

In this **standalone** public package, tests that need private human returns or
the manuscript tree are skipped automatically. Full local recomputation of
unit-level agreement from original labels is **not** possible from the public
bag alone (labels remain private). Aggregate locked metrics are provided in
`data/derived/measurement_agreement_summary.json`.

## Software requirements

- Python ≥ 3.11
- `uv` for environment sync
- See `pyproject.toml` for dependencies

## Data provenance

- **ParlaMint-ES / ParlaMint 5.0** (handle [11356/2004](http://hdl.handle.net/11356/2004)): CC BY 4.0. Bulk archive is **not** redistributed here; see `data/raw_pinned/` and `docs/licensing.md`.
- **Congreso de los Diputados** initiative records: identifier-based public packaging only; full registered-question text redistribution remains deferred (see `docs/licensing.md`).
- **XIV main-frame metadata** (`data/derived/main_frame_metadata_preannotation.*`): identifiers and non-outcome fields only; **no** reply labels; **no** full spoken/registered text.

## Intentionally NOT included

- private `_internal/` working materials;
- annotator return DOCX / XLSX packets;
- unit-level independent human labels and free-text comments;
- full Congreso initiative HTML/text;
- ParlaMint bulk `.tgz`;
- manuscript LaTeX (`paper/`);
- AI reply-side labels (none were used as outcomes).

## Licensing / reuse

- **Code** (`src/`, `scripts/`, `tests/`, Makefile): MIT (`LICENSE`).
- **ParlaMint-derived identifiers / attribution:** CC BY 4.0 (see pin metadata).
- **Congreso:** follow Congreso reuse notice; this package redistributes **identifiers/metadata only**.
- Do **not** assume every file is CC BY 4.0. Details: `docs/licensing.md`.

## Citation

See `CITATION.cff`. Preferred citation for the archived package:

Andrés, C., Baena Rojas, J. J., & Pinto Pajares, D. (2026). *When Does a Reply
Count as an Answer? … (research package)* (v1.0.0). Zenodo.
https://doi.org/10.5281/zenodo.23495525


## Authors / contact

1. César Andrés — ORCID [0009-0001-8968-3404](https://orcid.org/0009-0001-8968-3404) — cesar.andres@unir.net  
2. Jose Jaime Baena Rojas — ORCID [0000-0002-0915-4087](https://orcid.org/0000-0002-0915-4087)  
3. Daniel Pinto Pajares — ORCID [0000-0001-9397-811X](https://orcid.org/0000-0001-9397-811X)  

Affiliation: Universidad Internacional de la Rioja, Spain.
