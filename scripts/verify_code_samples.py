#!/usr/bin/env python3
"""Check every authored Python fence and execute explicitly runnable samples."""
import ast
import contextlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
meta = json.loads((ROOT / 'book/book.json').read_text())
checked = executed = 0
for part in meta['parts']:
    for name in part['chapters']:
        text = (ROOT / 'book' / name).read_text()
        fences = re.findall(r'^```(python|py)([^\n]*)\n(.*?)^```\s*$', text, re.M | re.S)
        for index, (_, info, code) in enumerate(fences, 1):
            label = f'{name}: Python block {index}'
            tree = ast.parse(code, filename=label)
            checked += 1
            if 'runnable' in info.split():
                assert any(isinstance(n, ast.Assert) for n in ast.walk(tree)), label + ': needs a checked outcome'
                # These are our authored examples, not downloaded third-party code.
                # Runnable samples are pure calculations and in-memory demonstrations.
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(tree, label, 'exec'), {'__name__': '__sample__'})
                executed += 1
assert checked >= 8, f'Expected substantive authored Python samples, got {checked}'
assert executed >= 4, f'Expected at least 4 independently executed samples, got {executed}'
print(f'OK: {checked} Python samples syntax checked; {executed} runnable samples executed with assertions')
