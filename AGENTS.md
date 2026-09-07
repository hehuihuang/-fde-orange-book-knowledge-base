# Repository guidance

## Purpose

Maintain a source-backed Chinese knowledge base about Forward Deployed Engineering. Keep the orange book, detailed cases, reusable templates, and evidence ledger consistent.

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

## Build

Run `uv run --with python-docx python build_book.py` to regenerate the editable book.
