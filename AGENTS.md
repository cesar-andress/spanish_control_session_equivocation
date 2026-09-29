# AGENTS.md — spanish_control_session_equivocation

## Paper identity (scaffold freeze)

**Working title.** Answering Allies and Adversaries: Equivocation in Prime-Ministerial Replies during Spanish Parliamentary Control Sessions

**Primary question (observational).** In Spanish Congress control sessions, does the Prime Minister give explicit replies to pre-registered oral questions at different rates depending on the political alignment of the questioner's parliamentary group?

Do not sharpen this into a causal claim. Operational codebook definitions are not frozen.

**Phase.** Phase 1 scaffold complete. No data, no sample, no annotation, no results.

## Design brief

`_internal/planning/design/project_design_brief.md`

Literature claims there are not frozen until Phase 0 (`_internal/literature/`).

## Layout

| Path | Role |
|------|------|
| `paper/` | Manuscript (LaTeX); not the public software tree |
| `zenodo/` | Public replication package |
| `_internal/` | Never published |

## Authors (from workspace identity standard)

- Jose Jaime Baena Rojas (ORCID 0000-0002-0915-4087)
- Daniel Pinto Pajares (ORCID 0000-0001-9397-811X)
- César Andrés (ORCID 0009-0001-8968-3404)

## Hard constraints

- No LLM labelling or coding assistance.
- No GPU / torch / transformers stack.
- Do not reanalyse the previous paper's N=100 pilot.
- Do not claim primacy until Phase 0 novelty freeze.
- Public tree must not contain `_internal/`, Cursor/agent config, or (for software release) manuscript LaTeX.
- Do not fabricate references or empirical claims.

## Integrity sequence

development → calibration → protocol freeze → main annotation → reliability → adjudication → analysis

## Next gate

Literature/novelty freeze + source-data feasibility. Then Phase 2 (`make data` / `make pool`) under a separate prompt.
