"""Copy, extract, or verify the mixed JSONL/gzip dataset collection."""

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
        stored = (root / entry["path"]).resolve()
        if root not in stored.parents:
            raise ValueError("Dataset path is outside the repository")
        storage_format = entry["storage_format"]
        if storage_format not in ("jsonl", "gzip"):
            raise ValueError(f"Unsupported storage format: {storage_format}")
        if stored.stat().st_size != entry["stored_bytes"] or digest_file(stored) != entry["stored_sha256"]:
            raise ValueError(f"Stored file checksum or size mismatch: {stored.name}")
        if args.verify_only:
            print(f"Verified {stored.name}")
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
        source = gzip.open(stored, "rb") if storage_format == "gzip" else stored.open("rb")
        with source as src, temporary.open("xb") as dst:
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
