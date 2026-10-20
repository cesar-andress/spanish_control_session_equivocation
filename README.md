# When Does a Reply Count as an Answer?

**Threshold Instability in Expert Coding of Spanish Parliamentary Replies**

Public research / reproducibility package **v1.0.1**.

Current archive: [DOI 10.5281/zenodo.23496446](https://doi.org/10.5281/zenodo.23496446).  
Previous archive: [v1.0.0 DOI 10.5281/zenodo.23495525](https://doi.org/10.5281/zenodo.23495525).

## What changed in v1.0.1

v1.0.1 improves **computational reproducibility** by adding:

- `data/HUMAN_EVIDENCE_67_PUBLIC.csv` — redistributable 67-unit independent label table;
- `data/HUMAN_EVIDENCE_67_PUBLIC_DATA_DICTIONARY.md`;
- public recomputation of the locked agreement statistics from that table alone
  (`scripts/reproduce_public_agreement.py`).

**No scientific result changed. No labels changed. No new annotation occurred.**

## Archived releases

| Field | v1.0.0 | v1.0.1 |
|-------|--------|--------|
| Status | Published (superseded for citation) | **Published (current)** |
| Zenodo DOI | [10.5281/zenodo.23495525](https://doi.org/10.5281/zenodo.23495525) | [10.5281/zenodo.23496446](https://doi.org/10.5281/zenodo.23496446) |

## What this package contains

This package supports a short **methodological / measurement** study of expert
agreement when coding whether a prime minister’s first reply resolves a
parliamentary oral question. It includes:

- the public 67-unit evidence table and data dictionary;
- analysis code (`src/scse/`) including public recomputation helpers;
- protocols and codebooks used in the sequential measurement programme;
- identifier-only public metadata for the XIV target frame (N=100 context);
- locked agreement summaries (recomputable from the unit table);
- pre-outcome tables/figures and measurement-paper figures;
- schemas, manifests, and reproducibility documentation.

**Version:** `v1.0.1`

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
| `data/HUMAN_EVIDENCE_67_PUBLIC.csv` | 67-unit independent labels (coder_A / coder_B) |
| `data/HUMAN_EVIDENCE_67_PUBLIC_DATA_DICTIONARY.md` | Column and instrument documentation |
| `src/scse/` | Python package (metrics, public recomputation, hygiene) |
| `protocol/` | Codebooks, calibration design, decisions log, manifests |
| `data/derived/` | Identifier-only metadata + agreement summary JSON |
| `data/raw_pinned/` | ParlaMint pin provenance (no bulk corpus) |
| `outputs/` | Tables and figures |
| `schemas/` | JSON schemas |
| `manifests/` | Acquisition / release manifests |
| `docs/` | Licensing, reproduction, private-area boundary notes |
| `tests/` | Unit and hygiene tests |
| `scripts/` | Build/ingest helpers + public agreement reproduction |

## Reproduce (public package)

Requires Python ≥ 3.11 and [`uv`](https://github.com/astral-sh/uv).

```bash
uv sync --all-extras
uv run python scripts/reproduce_public_agreement.py
make test
make hygiene
```

The public package alone recomputes raw agreement, Cohen’s κ, Krippendorff’s α,
pooled Round 1+Round 2 estimates, binary κ_max, and disagreement-direction
counts from `data/HUMAN_EVIDENCE_67_PUBLIC.csv` (bootstrap: 5,000 resamples;
seed `20261020`).

## Software requirements

- Python ≥ 3.11
- `uv` for environment sync
- See `pyproject.toml` for dependencies

## Data provenance

- **ParlaMint-ES / ParlaMint 5.0** (handle [11356/2004](http://hdl.handle.net/11356/2004)): CC BY 4.0. Bulk archive is **not** redistributed here; utterance identifiers in the public evidence table point to the ParlaMint release. See `data/raw_pinned/` and `docs/licensing.md`.
- **Congreso de los Diputados** initiative records: identifier-based public packaging only; full registered-question text redistribution remains deferred (see `docs/licensing.md`). The OOP evidence table leaves `congreso_expediente` empty when not stored in the source audits.
- **XIV main-frame metadata** (`data/derived/main_frame_metadata_preannotation.*`): identifiers and non-outcome fields only; **no** reply labels; **no** full spoken/registered text.

## Intentionally NOT included

- private `_internal/` working materials;
- annotator return DOCX / XLSX packets;
- annotator free-text comments;
- full Congreso initiative HTML/text and full parliamentary reply text;
- ParlaMint bulk `.tgz`;
- manuscript LaTeX (`paper/`);
- personal annotator names in the unit-level table (coder_A / coder_B only);
- AI reply-side labels (none were used as outcomes);
- XIV responsiveness outcomes (none exist under the failed instruments).

## Licensing / reuse

- **Code** (`src/`, `scripts/`, `tests/`, Makefile): MIT (`LICENSE`).
- **ParlaMint-derived identifiers / attribution:** CC BY 4.0 (see pin metadata).
- **Congreso:** follow Congreso reuse notice; this package redistributes **identifiers/metadata only**.
- Do **not** assume every file is CC BY 4.0. Details: `docs/licensing.md`.

## Citation

See `CITATION.cff`. Cite the current v1.0.1 archive:

Andrés, C., Baena Rojas, J. J., & Pinto Pajares, D. (2026). *When Does a Reply
Count as an Answer? … (research package)* (v1.0.1). Zenodo.
https://doi.org/10.5281/zenodo.23496446

## Authors / contact

1. César Andrés — ORCID [0009-0001-8968-3404](https://orcid.org/0009-0001-8968-3404) — cesar.andres@unir.net  
2. Jose Jaime Baena Rojas — ORCID [0000-0002-0915-4087](https://orcid.org/0000-0002-0915-4087) — josejaime.baena@unir.net  
3. Daniel Pinto Pajares — ORCID [0000-0001-9397-811X](https://orcid.org/0000-0001-9397-811X) — daniel.pinto@unir.net  

Affiliation: Universidad Internacional de la Rioja, Spain.
