"""Download and verify the cleaned dataset from this repository's GitHub Release."""
import hashlib
import io
import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

REPOSITORY = 'anglee0323/fomo-top100-traders'
TAG = 'clean-20261014'


class Concatenated(io.RawIOBase):
    def __init__(self, paths):
        self.paths = iter(paths); self.current = None

    def read(self, size=-1):
        if size < 0: raise ValueError('Streaming reads must be bounded')
        values = []; remaining = size
        while remaining:
            if self.current is None:
                try: self.current = next(self.paths).open('rb')
                except StopIteration: break
            block = self.current.read(remaining)
            if not block:
                self.current.close(); self.current = None; continue
            values.append(block); remaining -= len(block)
        return b''.join(values)


def main():
    root = Path(__file__).resolve().parent; data = root / 'data'; target = data / 'clean'
    if target.exists(): raise ValueError('data/clean already exists; refusing to overwrite it')
    data.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.download-', dir=root) as directory:
        directory = Path(directory)
        github_cli = shutil.which('gh') or next((str(p) for p in [Path('/opt/homebrew/bin/gh'), Path('/usr/local/bin/gh')] if p.is_file()), None)
        if github_cli is None: raise RuntimeError('Install GitHub CLI before downloading')
        subprocess.run([github_cli, 'release', 'download', TAG, '-R', REPOSITORY,
                        '--pattern', 'clean-data.tar.part*', '--pattern', 'ARCHIVE.json',
                        '--pattern', 'SHA256SUMS', '--dir', str(directory)], check=True)
        manifest = json.loads((directory / 'ARCHIVE.json').read_bytes())
        parts = []
        for item in manifest['parts']:
            path = directory / item['name']; h = hashlib.sha256()
            with path.open('rb') as f:
                for b in iter(lambda: f.read(2**20), b''): h.update(b)
            if path.stat().st_size != item['bytes'] or h.hexdigest() != item['sha256']:
                raise ValueError('Downloaded part failed integrity check')
            parts.append(path)
        with tarfile.open(fileobj=Concatenated(parts), mode='r|') as archive:
            for member in archive:
                path = data / member.name
                if not path.resolve().is_relative_to(target.resolve()) or member.issym() or member.islnk():
                    raise ValueError('Unsafe archive member')
                if member.isdir(): path.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(member) as src, path.open('xb') as dst:
                        shutil.copyfileobj(src, dst, 2**20)
                else: raise ValueError('Unsupported archive member')
    print('Ready: ' + str(target))


if __name__ == '__main__': main()
