# Licensing status (Phase 0 update)

**Access date for checks:** 2026-09-29  
**Status:** partially verified — suitable for planning; not a final redistribution legal opinion.

## Code

The software under `src/`, `scripts/`, `tests/`, and the Makefile is released under the MIT License (see `../LICENSE`).

## ParlaMint-ES / ParlaMint 5.0

| Field | Verified value |
|-------|----------------|
| Deposit | CLARIN.SI: Multilingual comparable corpora of parliamentary debates ParlaMint 5.0 |
| Handle | http://hdl.handle.net/11356/2004 |
| Spanish package | `ParlaMint-ES.tgz` (listed on deposit page; MD5 published there) |
| Licence | **Creative Commons Attribution 4.0 International (CC BY 4.0)** |
| Evidence | Deposit page states the item is publicly available and licensed under CC BY 4.0 |
| Attribution | Required (cite ParlaMint / CLARIN.SI deposit and project) |
| Redistribution of derived excerpts | **Allowed under CC BY 4.0** with attribution and licence notice |

Optional annotated release: http://hdl.handle.net/11356/2005 (same family; confirm licence on that handle before use).

## Congreso de los Diputados records

| Field | Status |
|-------|--------|
| Sources in scope | Iniciativas (pregunta oral en Pleno, type `180/`), Diario de Sesiones / actas, open-data portal (`/es/opendata/...`) |
| Official open-data portal | https://www.congreso.es/es/datos-abiertos and section pages for iniciativas, intervenciones, votaciones, diputados |
| Formats advertised | XML, JSON, CSV (portal text) |
| Copyright / reuse licence text | **NOT FULLY PINNED in this phase** (portal access from automated clients intermittent; conditions-of-use page not captured as a stable licence identifier comparable to CC BY) |
| Working scientific stance | Texts are public acts of public officials in parliamentary proceedings. Reuse for research is expected, but **Zenodo full-text deposit of Congreso-derived strings must wait until the Congreso reuse notice is recorded with URL + access date**. |
| Safe release meanwhile | Stable identifiers (`expediente`, DS references, dates, hashes of local copies), derived labels, and scripts that reacquire official pages |

## Provisional public-release strategy

1. **ParlaMint-derived unit text:** may be released under CC BY 4.0 with attribution once Phase 2 pins checksums.  
2. **Congreso registered-question / DS excerpts:** default to **identifier-based release + reacquisition scripts** until reuse terms are pinned; then upgrade if permitted.  
3. **Annotations / alignment labels / reliability tables:** releasable as project-generated data (MIT for code; data notice TBD).

Do **not** assume all project data are CC BY 4.0.
