"""Extract or verify the dataset collection with Python's standard library."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path


def digest_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("jsonl"))
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if not args.verify_only:
        args.output.mkdir(parents=True, exist_ok=True)
    for entry in manifest["files"]:
        archive = (root / entry["archive"]).resolve()
        if root not in archive.parents:
            raise ValueError("Archive path is outside the repository")
        if digest_file(archive) != entry["compressed_sha256"]:
            raise ValueError(f"Archive checksum mismatch: {archive.name}")
        if args.verify_only:
            print(f"Verified {archive.name}")
            continue
        name = entry["source_filename"]
        if Path(name).name != name or name in ("", ".", ".."):
            raise ValueError("Invalid source filename in manifest")
        target = args.output / name
        if target.exists():
            if digest_file(target) != entry["source_sha256"]:
                raise FileExistsError(f"Existing file differs: {target}")
            print(f"Already verified {name}")
            continue
        temporary = target.with_name(target.name + ".partial")
        digest = hashlib.sha256()
        size = 0
        with gzip.open(archive, "rb") as src, temporary.open("xb") as dst:
            while block := src.read(4 * 1024 * 1024):
                digest.update(block)
                size += len(block)
                dst.write(block)
        if digest.hexdigest() != entry["source_sha256"] or size != entry["source_bytes"]:
            raise ValueError(f"Extracted checksum or size mismatch: {name}")
        temporary.rename(target)
        print(f"Extracted and verified {name}")


if __name__ == "__main__":
    main()
