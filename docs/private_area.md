# Private area (never publish)

The project root contains a sibling directory `_internal/` next to `zenodo/`
and `paper/`.

That directory holds:

- literature notes and novelty worksheets
- planning and design memos
- private link-audit sheets
- raw returned annotator packets
- calibration notes
- correspondence
- AI prompts and orchestration material
- internal status reports

## Rules

1. `_internal/` must never be copied into a Zenodo deposit, GitHub public tree,
   or other public release archive.
2. No file under `zenodo/` may embed absolute personal home paths.
3. Prompt files and agent configuration must not appear under `zenodo/`.
4. Release packaging (`make release`) must refuse if private-area material is
   detected inside the public tree.

Manuscript sources live under `paper/` and are also outside the public software
release package unless a journal-specific submission workflow says otherwise.
