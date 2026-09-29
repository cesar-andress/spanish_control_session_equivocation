# Licensing status (Phase 2)

**Access date for checks:** 2026-09-29  
**Status:** ParlaMint pinned; Congreso reuse notice recorded; public release remains identifier-based for Congreso strings pending final legal review of redistribution packaging.

## Code

The software under `src/`, `scripts/`, `tests/`, and the Makefile is released under the MIT License (see `../LICENSE`).

## ParlaMint-ES / ParlaMint 5.0

| Field | Verified value |
|-------|----------------|
| Deposit | CLARIN.SI ParlaMint 5.0 |
| Handle | http://hdl.handle.net/11356/2004 |
| Spanish package | `ParlaMint-ES.tgz` |
| MD5 (publisher) | `2ba1216f3fcf1300ee74f50efe42ec6a` |
| SHA-256 (observed) | `b101c066a7770c80fcd835cc39282f29acd32883887306017cbd454c4d6eef68` |
| Licence | **Creative Commons Attribution 4.0 International (CC BY 4.0)** |
| Redistribution | **SAFE TO REDISTRIBUTE** derived excerpts with attribution |
| Cache location | `_internal/source_cache/parlamint/` (**PRIVATE SOURCE CACHE**; not committed) |

## Congreso de los Diputados records

| Field | Verified value |
|-------|----------------|
| Official source | Búsqueda de iniciativas — Pregunta oral en Pleno (`180/######`) |
| Base URL | https://www.congreso.es/es/busqueda-de-iniciativas |
| Access method | Authenticated-browser-equivalent HTTP GET with documented research User-Agent; HTML initiative detail pages; polite caching under `_internal/source_cache/congreso/` |
| Terms / reuse URL | https://www.congreso.es/es/cem/aviso-legal (section *Reutilización de información*) |
| Licence / reuse wording | Information on www.congreso.es is reusable if the user: (a) does not alter content; (b) does not distort meaning; (c) cites the source; (d) mentions the date of last update; (e) uses content diligently / not unlawfully. **Not** expressed as a Creative Commons identifier. |
| Attribution | Cite Congreso de los Diputados; preserve content meaning; record update date when redistributing |
| Exact registered-question strings | Reuse conditions appear to **permit** redistribution with citation; packaging choice for this deposit remains conservative |
| Identifiers / metadata | **SAFE TO REDISTRIBUTE** (`expediente`, dates, DS references, ParlaMint IDs, linkage status) |
| Uncertainty | Aviso legal is a reuse notice with conditions, not a standard open-licence URI. Treat full-text Zenodo bundling of Congreso initiative HTML/strings as **UNRESOLVED** for deposit packaging until counsel/journal check. |

### Artifact classification (Phase 2)

| Artifact | Class |
|----------|-------|
| Pipeline code / schemas / manifests (checksums, IDs) | SAFE TO REDISTRIBUTE (MIT / project) |
| ParlaMint-derived utterance IDs + CC BY excerpts (if later released) | SAFE TO REDISTRIBUTE (CC BY 4.0 + attribution) |
| `zenodo/data/derived/eligible_pool_metadata_preannotation.*` | IDENTIFIER-ONLY (no Congreso/ParlaMint full text) |
| `_internal/source_cache/parlamint/` | PRIVATE SOURCE CACHE |
| `_internal/source_cache/congreso/` | PRIVATE SOURCE CACHE |
| `_internal/data_private/eligible_pool_full.parquet` | PRIVATE SOURCE CACHE (full text) |
| Congreso initiative full text in a Zenodo bag | UNRESOLVED (reuse conditions recorded; packaging deferred) |

## Provisional public-release strategy

**IDENTIFIER-BASED** for Congreso registered-question and DS text; ParlaMint identifiers in the public metadata projection; full working texts only in the private pool until packaging is approved.

Do **not** assume all project data are CC BY 4.0.
