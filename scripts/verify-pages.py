"""Verify every published snapshot file and GitHub Pages relative entry points."""
import hashlib
import json
from pathlib import Path
from snapshot import load_snapshot

root = Path(__file__).resolve().parents[1]
files = [r for r in load_snapshot() if r[0].startswith('dist/')]
for path, size, digest, _ in files:
    contents = (root / path).read_bytes()
    assert len(contents) == size, path
    assert hashlib.sha256(contents).hexdigest() == digest, path
html = (root / 'dist/index.html').read_text()
assert 'src="/app.js"' not in html
assert 'href="/style.css"' not in html
print(f'PASS: {len(files)} complete website files verified; relative Pages entry points.')
