# Public package manifest (v1.0.1)

## Original third-party sources (not bulk-redistributed)

| Item | Role in package |
|------|-----------------|
| ParlaMint 5.0 / ParlaMint-ES | Pin provenance in `data/raw_pinned/` (handle, hashes, CC BY 4.0). Bulk `.tgz` excluded. Utterance ids in the public evidence table. |
| Congreso de los Diputados | Initiative identifiers only in derived metadata; full text excluded. |

## Derived data (public)

| Path | Contents |
|------|----------|
| `data/HUMAN_EVIDENCE_67_PUBLIC.csv` | 67-unit independent labels (coder_A / coder_B); no source full text |
| `data/HUMAN_EVIDENCE_67_PUBLIC_DATA_DICTIONARY.md` | Column / instrument dictionary |
| `data/derived/eligible_pool_metadata_preannotation.*` | Identifier-only pool projection |
| `data/derived/main_frame_metadata_preannotation.*` | XIV frame N=100 non-outcome metadata |
| `data/derived/measurement_agreement_summary.json` | Agreement metrics (recomputable from unit table) |
| `data/derived/measurement_agreement_public_repro.json` | Full public recomputation payload + bootstrap invalid/zero counts |
| `data/derived/DATA_DICTIONARY_PREOUTCOME.md` | Pre-outcome field dictionary |

## Analysis code

| Path | Contents |
|------|----------|
| `src/scse/` | Pipeline and metrics package |
| `src/scse/public_evidence.py` | Public recomputation from the 67-unit table |
| `scripts/reproduce_public_agreement.py` | CLI entry for public recomputation |
| `scripts/` | Other build/ingest helpers (many need private monorepo inputs) |
| `tests/` | Public + private-skippable tests |
| `tests/test_public_evidence_67.py` | Public table + lock reproduction tests |
| `Makefile` | `test`, `hygiene`, `public-repro`, phase stubs |

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
| `CITATION.cff` | Citation metadata (version 1.0.1) |
| `.zenodo.json` | Zenodo GitHub integration metadata (version 1.0.1) |
| `LICENSE` | MIT for code |
| `docs/licensing.md` | Multi-component reuse policy |
| `docs/reproduce.md` | Reproduction notes |
| `docs/private_area.md` | What is excluded |
| `docs/ARCHIVE_DOI.md` | Published v1.0.0 DOI record |
| `RELEASE_NOTES.md` | v1.0.0 / v1.0.1 notes |
| `SHA256SUMS.txt` | File hashes |

## Explicit exclusions

- `_internal/` (private returns, reports, source caches)
- Annotator DOCX/XLSX returns and free-text comments
- Full Congreso text / ParlaMint bulk archive
- Manuscript `paper/` tree
- Credentials, `.env`, agent configs
- XIV reply / responsiveness outcomes
- AI reply labels
