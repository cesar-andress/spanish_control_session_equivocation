# Decision log

Append-only. Do not rewrite past entries. Use ISO dates.

Format per entry:

- **date**
- **decision**
- **status**
- **evidence**
- **reason**
- **effect on protocol**

---

## 2026-09-29 — Project creation

- **decision:** Create project `spanish_control_session_equivocation` with
  `paper/`, `zenodo/`, and private `_internal/` areas.
- **status:** accepted
- **evidence:** Phase 1 scaffold task; design brief archived under
  `_internal/planning/design/`
- **reason:** Separate manuscript, public reproducibility package, and private
  working material.
- **effect on protocol:** Establishes repository layout; no empirical protocol
  freeze.

## 2026-09-29 — Working research question

- **decision:** Adopt the observational primary question comparing explicit-reply
  rates across a pre-defined political-alignment contrast of the questioner's
  group; do not frame a causal claim.
- **status:** accepted (draft; not preregistered)
- **evidence:** Design brief §4; Phase 1 scientific-identity freeze
- **reason:** One inspectable confirmatory question for a reply-rate study.
- **effect on protocol:** Recorded in `STUDY_PROTOCOL_DRAFT.md`; operational
  alignment rule still unresolved.

## 2026-09-29 — Public / private separation

- **decision:** Public reproducibility content lives under `zenodo/`; private
  material under `_internal/` must never enter public releases; manuscript under
  `paper/`.
- **status:** accepted
- **evidence:** Workspace public-release hygiene rules; design brief §21
- **reason:** Prevent leakage of prompts, raw packets, and private notes.
- **effect on protocol:** Hygiene tests and docs enforce the split.

## 2026-09-29 — No LLM component

- **decision:** No LLM labelling, baselines, or assistance in coding for the
  empirical study.
- **status:** accepted
- **evidence:** Design brief §18
- **reason:** Keep the study human-centred and reviewable without model-as-coder
  complications.
- **effect on protocol:** Computational stack excludes LLM / GPU frameworks.

## 2026-09-29 — No GPU requirement

- **decision:** Pipeline is CPU-only (XML parsing, linkage, bootstrap, plots).
- **status:** accepted
- **evidence:** Design brief §17
- **reason:** Design does not require neural training or inference.
- **effect on protocol:** Environment omits torch / transformers.

## 2026-09-29 — No data sampled yet

- **decision:** Phase 1 scaffold only; no corpus acquisition, no sample draw, no
  annotation, no empirical results.
- **status:** accepted
- **evidence:** Phase 1 task gate
- **reason:** Reproducibility infrastructure before data work.
- **effect on protocol:** Make targets for later phases fail safely; seeds unset.
