#!/usr/bin/env python3
"""Validate local structure and editorial release gates for the FDE knowledge base."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIRS = [ROOT / "knowledge-base", ROOT / "templates", ROOT / "research"]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.I),
    re.compile(r"\bTBD\b", re.I),
    re.compile(r"\blorem ipsum\b", re.I),
    re.compile(r"待补充|待完善"),
]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "LICENSE.md"]
    for directory in CONTENT_DIRS:
        files.extend(sorted(directory.rglob("*.md")))
    return files


def validate() -> list[str]:
    errors: list[str] = []
    files = markdown_files()

    for path in files:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"empty file: {path.relative_to(ROOT)}")
        if not text.startswith("# "):
            errors.append(f"missing H1: {path.relative_to(ROOT)}")
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"release placeholder {pattern.pattern!r}: {path.relative_to(ROOT)}"
                )
        for target in LINK_RE.findall(text):
            target = target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local = unquote(target.split("#", 1)[0])
            if not local:
                continue
            resolved = (path.parent / local).resolve()
            if not resolved.exists():
                errors.append(
                    f"broken local link: {path.relative_to(ROOT)} -> {target}"
                )

    case_dir = ROOT / "knowledge-base" / "03-海外案例"
    cases = sorted(p for p in case_dir.glob("[0-9][0-9]-*.md") if not p.name.startswith("00-"))
    if len(cases) != 8:
        errors.append(f"expected 8 detailed cases, found {len(cases)}")
    for case in cases:
        text = case.read_text(encoding="utf-8")
        for marker in ["证据等级", "FDE 视角重构", "资料没有说明什么"]:
            if marker not in text:
                errors.append(f"case missing {marker}: {case.relative_to(ROOT)}")
        if "https://" not in text:
            errors.append(f"case missing external source: {case.relative_to(ROOT)}")

    ledger = ROOT / "research" / "01-source-ledger.md"
    if ledger.exists():
        ledger_text = ledger.read_text(encoding="utf-8")
        for prefix in ["R01", "C01", "G01", "X01"]:
            if prefix not in ledger_text:
                errors.append(f"source ledger missing section identifier: {prefix}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("FDE knowledge base validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    files = markdown_files()
    chars = sum(len(path.read_text(encoding="utf-8")) for path in files if path.exists())
    print(f"OK: {len(files)} Markdown files, {chars:,} characters, 8 detailed cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
