"""Download a versioned dataset, verify archive parts and extract safely."""
import hashlib
import io
import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

REPOSITORY = "anglee0323/fomo-top100-traders"
TAG = "v2026.10.14"


class Concatenated(io.RawIOBase):
    def __init__(self, paths):
        self.paths = iter(paths); self.current = None

    def read(self, size=-1):
        if size < 0:
            raise ValueError("Streaming reads must be bounded")
        values = []; remaining = size
        while remaining:
            if self.current is None:
                try: self.current = next(self.paths).open("rb")
                except StopIteration: break
            block = self.current.read(remaining)
            if not block:
                self.current.close(); self.current = None; continue
            values.append(block); remaining -= len(block)
        return b"".join(values)

    def close(self):
        if self.current is not None:
            self.current.close()
        super().close()


def main():
    root = Path(__file__).resolve().parent; target = root / "dataset"
    if target.is_symlink() or any(target.rglob("*.parquet")):
        raise ValueError("Dataset already exists; refusing to overwrite local data")
    cli = shutil.which("gh") or next((str(p) for p in (Path("/opt/homebrew/bin/gh"), Path("/usr/local/bin/gh")) if p.is_file()), None)
    if not cli:
        raise RuntimeError("Install GitHub CLI before downloading")
    with tempfile.TemporaryDirectory(prefix=".download-", dir=root) as temporary:
        temporary = Path(temporary)
        subprocess.run([cli, "release", "download", TAG, "-R", REPOSITORY,
            "--pattern", "*-dataset.tar.part*", "--pattern", "archive.json", "--pattern", "SHA256SUMS",
            "--dir", str(temporary)], check=True)
        manifest = json.loads((temporary / "archive.json").read_bytes()); parts = []
        for item in manifest["parts"]:
            name = item["name"]
            if Path(name).name != name:
                raise ValueError("Invalid archive part name")
            path = temporary / name; digest = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(2**20), b""): digest.update(block)
            if path.stat().st_size != item["bytes"] or digest.hexdigest() != item["sha256"]:
                raise ValueError("Archive integrity check failed: " + name)
            parts.append(path)
        staging = temporary / "unpacked"; staging.mkdir()
        expected_root = staging / "dataset"
        with Concatenated(parts) as combined, tarfile.open(fileobj=combined, mode="r|") as archive:
            for member in archive:
                path = staging / member.name
                if not path.resolve().is_relative_to(expected_root.resolve()) or member.issym() or member.islnk():
                    raise ValueError("Unsafe archive member")
                if member.isdir(): path.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(member) as source, path.open("xb") as destination:
                        shutil.copyfileobj(source, destination, 2**20)
                else: raise ValueError("Unsupported archive member")
        if target.exists():
            for path in target.rglob("*"):
                if path.is_symlink(): raise ValueError("Local dataset contains a symbolic link")
                if path.is_file():
                    incoming = expected_root / path.relative_to(target)
                    if not incoming.is_file() or path.read_bytes() != incoming.read_bytes():
                        raise ValueError("Local metadata differs: " + str(path.relative_to(target)))
            for path in expected_root.rglob("*"):
                destination = target / path.relative_to(expected_root)
                if path.is_dir(): destination.mkdir(exist_ok=True)
                elif not destination.exists(): path.rename(destination)
        else:
            expected_root.rename(target)
    print("Dataset ready: " + str(target))


if __name__ == "__main__": main()
