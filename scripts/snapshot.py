"""Expand a pinned, compact manifest into the exact original file inventory."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_snapshot(restore=None):
    snapshot = json.loads((ROOT / 'migration/snapshot.json').read_text())
    records = {r[0]: r for r in snapshot['files']}
    for index in snapshot['indexes']:
        seed = records[index['path']]
        if restore is not None:
            restore(seed)
        data = (ROOT / seed[0]).read_bytes()
        assert len(data) == seed[1] and hashlib.sha256(data).hexdigest() == seed[2], seed[0]
        values = json.loads(data)
        if index['field']:
            values = values[index['field']]
        for path, value in values.items():
            if index['keep_prefixes'] and not path.startswith(tuple(index['keep_prefixes'])):
                continue
            relative = index['prefix'] + path
            base = ('https://inception-microscope-explorer.honeysugar12.chatgpt.site/source/'
                    if relative.startswith('dist/') else
                    'https://already-clean.goodfire.com/microscope/inceptionv1/')
            record = [relative, value['bytes'], value['sha256'], base + path]
            assert relative not in records, relative
            records[relative] = record
    for group, expected in snapshot['expected_counts'].items():
        assert sum(p.startswith(group + '/') for p in records) == expected, group
    return sorted(records.values())
