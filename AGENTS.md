# Repository guidance

## Purpose

Maintain a source-backed Chinese book about Forward Deployed Engineering, titled FDE橙皮书. The book/ chapters are the current manuscript, organized as foundations, technical knowledge, delivery practice and final cases. Keep the PDF, reader HTML, detailed research, templates, and evidence ledger consistent. Preserve the legacy research and old editions.

## Content rules

- Separate sourced facts from analysis and unknowns.
- Prefer first-party sources, standards, filings, and official technical documentation.
- Treat X posts, forums, and job descriptions as signals with explicit limitations.
- Never invent customer architecture, staffing, contract value, causal attribution, or private implementation details.
- Every detailed case must include source links, an evidence grade, known limitations, and a reusable FDE work package.
- Do not copy third-party articles or repository code. Summarize and link.
- Update `research/01-source-ledger.md` and `CHANGELOG.md` when material facts change.

## Validation

Run `python3 scripts/validate_kb.py` before release. Broken relative links, empty files, missing case evidence labels, or placeholder text are release blockers.

Run `uv run --with pypdf python scripts/validate_book.py` for the current book. Inspect rendered PDF pages and the mobile/desktop reader after layout changes.

## Build

Run `uv run --with reportlab --with fonttools --with markdown-it-py --with pypdf python scripts/build_edition.py` to regenerate the current PDF, HTML, chapter directory and edition metadata. The builder does not update the cover PNG; render the PDF first page to dist/cover.png with pdftoppm after changing the cover.

Run `uv run --with python-docx python build_book.py` only for the legacy editable Word edition.
