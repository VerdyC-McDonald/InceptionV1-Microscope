"""Restore the verified Site snapshot once; subsequent hosting uses local files."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import time
import urllib.request
from snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[1]


def restore(record):
    relative, expected_size, expected_hash, url = record
    destination = ROOT / relative
    if destination.is_file():
        data = destination.read_bytes()
        if len(data) == expected_size and hashlib.sha256(data).hexdigest() == expected_hash:
            return
    for attempt in range(6):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=90) as response:
                data = response.read()
            if len(data) != expected_size or hashlib.sha256(data).hexdigest() != expected_hash:
                raise ValueError('Snapshot checksum mismatch: ' + relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_name(destination.name + '.part')
            temporary.write_bytes(data)
            temporary.replace(destination)
            return
        except Exception:
            if attempt == 5:
                raise
            time.sleep(min(30, 2 ** attempt))


def commit_files(records, message):
    batch, size = [], 0
    for record in records:
        batch.append(record[0])
        size += record[1]
        if size >= 300 * 1024 * 1024:
            commit_batch(batch, message)
            batch, size = [], 0
    if batch:
        commit_batch(batch, message)


def commit_batch(paths, message):
    # NUL-delimited pathspec avoids argument limits for the full corpus.
    result = subprocess.run(['git', 'add', '--pathspec-from-file=-', '--pathspec-file-nul'],
                            input=b''.join(p.encode() + b'\0' for p in paths), cwd=ROOT, check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=ROOT).returncode == 0:
        return
    subprocess.run(['git', 'commit', '-m', message], cwd=ROOT, check=True)
    subprocess.run(['git', 'push', 'origin', 'HEAD:main'], cwd=ROOT, check=True)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--group', choices=['dist', 'original-source'], required=True)
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    records = [r for r in load_snapshot(restore) if r[0].startswith(args.group + '/')]
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:
        futures = {pool.submit(restore, r): r[0] for r in records}
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                future.result()
            except Exception as error:
                failures.append({'path': futures[future], 'error': str(error)})
            if count % 1000 == 0 or count == len(records):
                print(f'{args.group}: {count}/{len(records)} checked; {len(failures)} failed', flush=True)
    if failures:
        print(json.dumps(failures[:30], ensure_ascii=False), flush=True)
        raise SystemExit('Migration incomplete; no incomplete group will be committed.')
    if args.commit:
        commit_files(records, f'Import verified {args.group} snapshot')
    print(f'PASS: {len(records)} files match the original snapshot.', flush=True)


if __name__ == '__main__':
    main()
