# Public package manifest (v1.0.0)

## Original third-party sources (not bulk-redistributed)

| Item | Role in package |
|------|-----------------|
| ParlaMint 5.0 / ParlaMint-ES | Pin provenance in `data/raw_pinned/` (handle, hashes, CC BY 4.0). Bulk `.tgz` excluded. |
| Congreso de los Diputados | Initiative identifiers only in derived metadata; full text excluded. |

## Derived data (public)

| Path | Contents |
|------|----------|
| `data/derived/eligible_pool_metadata_preannotation.*` | Identifier-only pool projection |
| `data/derived/main_frame_metadata_preannotation.*` | XIV frame N=100 non-outcome metadata |
| `data/derived/measurement_agreement_summary.json` | Aggregate locked agreement metrics |
| `data/derived/DATA_DICTIONARY_PREOUTCOME.md` | Field dictionary |

## Analysis code

| Path | Contents |
|------|----------|
| `src/scse/` | Pipeline and metrics package |
| `scripts/` | Build/ingest helpers (many need private monorepo inputs) |
| `tests/` | Public + private-skippable tests |
| `Makefile` | `test`, `hygiene`, phase stubs |

## Protocols / instruments

| Path | Contents |
|------|----------|
| `protocol/reply_status_codebook_v0.*.md` | Three-category instruments |
| `protocol/direct_resolution_codebook_v1.0-*.md` | Binary redesign drafts (not a frozen validated v1.0) |
| `protocol/CALIBRATION_DESIGN.md`, `DECISIONS.md`, manifests | Measurement-programme record |

## Figures / tables

| Path | Contents |
|------|----------|
| `outputs/tables/` | Pre-outcome composition + outcome shells |
| `outputs/figures/` | Study-flow / reliability figures + shells |

## Documentation / metadata

| Path | Contents |
|------|----------|
| `README.md` | Entry point |
| `CITATION.cff` | Citation metadata |
| `.zenodo.json` | Zenodo GitHub integration metadata |
| `LICENSE` | MIT for code |
| `docs/licensing.md` | Multi-component reuse policy |
| `docs/reproduce.md` | Reproduction notes |
| `docs/private_area.md` | What is excluded |
| `RELEASE_NOTES.md` | v1.0.0 notes |
| `SHA256SUMS.txt` | File hashes |

## Explicit exclusions

- `_internal/` (private labels, returns, reports, source caches)
- Annotator DOCX/XLSX returns
- Full Congreso text / ParlaMint bulk archive
- Manuscript `paper/` tree
- Credentials, `.env`, agent configs
