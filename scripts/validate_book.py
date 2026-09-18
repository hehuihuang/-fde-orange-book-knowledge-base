#!/usr/bin/env python3
"""Validate chapter order, local sources, PDF coverage and destinations."""
import json
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
meta = json.loads((ROOT / 'book/book.json').read_text())
files = [f for part in meta['parts'] for f in part['chapters']]
assert len(meta['parts']) == 4
assert len(files) == len(set(files)) == 27
assert [int(f[:2]) for f in files] == list(range(1, 28))
toc = (ROOT / 'book/目录.md').read_text()
readme = (ROOT / 'README.md').read_text()
reader = (ROOT / 'dist/FDE橙皮书.html').read_text()
for number, filename in enumerate(files, 1):
    text = (ROOT / 'book' / filename).read_text()
    heading = text.splitlines()[0][2:]
    assert text.startswith(f'# 第 {number} 章'), filename
    assert filename in toc and filename in readme, filename
    assert heading in reader, filename
    assert len(text) > 500, filename
    han = len(re.findall(r'[\u4e00-\u9fff]', text))
    minimum = 1800 if number <= 4 or 19 <= number <= 26 else 1500
    if 5 <= number <= 10: minimum = 3500
    if number == 27: minimum = 10000
    assert han >= minimum, f'{filename}: only {han} Chinese characters; depth floor {minimum}'
    headings = re.findall(r'^## (.+)$', text, re.M)
    assert len(headings) >= 6, (filename, 'Needs navigable substantive sections')
    assert len(headings) == len(set(headings)), (filename, 'Duplicate section heading')
    assert 'https://' in text or number == 12, filename
    assert not re.search(r'\bTODO\b|\bTBD\b|lorem ipsum|待补充|待完善', text, re.I), filename
    if number >= 19:
        for marker in ['证据等级', '可复用的 FDE 工作包', '资料没有说明什么', '来源与回读']:
            assert marker in text, (filename, marker)
assert '知识库' not in readme.splitlines()[0]
assert (ROOT / 'dist/FDE橙皮书.pdf').stat().st_size > 100000
edition = json.loads((ROOT / 'dist/edition.json').read_text())
assert edition['title'] == meta['title'] and edition['chapter_count'] == len(files)
expected_sources = ['book/' + f for f in files] + ['book/' + meta['frontmatter'], 'book/book.json', 'design/reader-template.html', 'scripts/build_edition.py']
companion = ROOT / 'examples/material_assistant'
expected_sources += [str(p.relative_to(ROOT)) for p in sorted(companion.glob('*.py')) + sorted(companion.glob('README.md'))]
assert set(expected_sources) == set(edition['source_sha256'])
for source, digest in edition['source_sha256'].items():
    assert hashlib.sha256((ROOT / source).read_bytes()).hexdigest() == digest, f'Rebuild edition after changing {source}'
try:
    from pypdf import PdfReader
except ImportError:
    print('OK: 27 chapters, 4 parts, Markdown/README/HTML aligned; install pypdf for PDF checks')
else:
    pdf = PdfReader(ROOT / 'dist/FDE橙皮书.pdf')
    assert len(pdf.pages) == edition['pages']
    assert 185 <= len(pdf.pages) <= 220, f'Book target around 200 pages; got {len(pdf.pages)}'
    for filename in files:
        key = 'ch-' + filename[:2]
        index = edition['chapter_pages'][key] - 1
        heading = (ROOT / 'book' / filename).read_text().splitlines()[0][2:]
        normalize = lambda value: re.sub(r'\s+', '', value)
        assert normalize(heading) in normalize(pdf.pages[index].extract_text()), filename
    def flatten(items):
        for item in items:
            if isinstance(item, list): yield from flatten(item)
            else: yield item
    bookmarks = list(flatten(pdf.outline))
    section_count = sum(len(re.findall(r'^## ', (ROOT / 'book' / f).read_text(), re.M)) for f in files + [meta['frontmatter']])
    assert len(bookmarks) == 32 + section_count, len(bookmarks)
    for item in bookmarks:
        assert 0 <= pdf.get_destination_page_number(item) < len(pdf.pages)
    links = [a.get_object() for p in pdf.pages for a in p.get('/Annots', [])]
    assert sum(a.get('/Subtype') == '/Link' for a in links) >= 60
    assert '\ufffd' not in ''.join(p.extract_text() for p in pdf.pages)
    print(f'OK: 27 chapters, 4 parts, {len(pdf.pages)} PDF pages, {len(bookmarks)} bookmarks, {len(links)} links')
