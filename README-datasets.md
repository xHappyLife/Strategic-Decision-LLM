# Strategic Decision LLM datasets

The collection contains **398 JSON Lines datasets**. Files below **100 MiB**
are stored directly as `.jsonl`; the larger files remain `.jsonl.gz` archives.
There are **363 uncompressed files** and **35 gzip archives**. Original
filenames, including `_synthetic` suffixes, are retained.

This snapshot contains **4,054,073 lines** and **19,010,996,896 source bytes**.
The mixed storage format occupies **5,678,201,920 bytes**. All dataset contents
are unchanged from the earlier fully compressed publication: restored files
were checked against the original source SHA-256 checksums. Of the 398
filenames, 31 carry the `_synthetic` suffix.

## Files

- `datasets/`: 363 directly readable `.jsonl` files and 35 `.jsonl.gz` archives.
- `manifest.json`: schema version 2, with source filenames, repository paths,
  storage formats, byte sizes, SHA-256 checksums, and line counts.
- `extract_datasets.py`: copy the plain files and extract the archives into one
  directory of JSONL files, or verify the stored files without extraction.

Each manifest entry has `path`, `storage_format` (`jsonl` or `gzip`),
`stored_bytes`, and `stored_sha256` for the file in the repository.
`source_filename`, `source_bytes`, and `source_sha256` describe the original
uncompressed JSONL file. The manifest's `synthetic_filename_marker` records the filename suffix only.
Line counts describe the files; they are not independently verified counts of
unique human decisions or participants. Packaging checks establish file
integrity, not research validity or training suitability. No per-study source
documentation or new data license is added by this upload.

## Read data directly

Plain JSONL files need no decompression. Python's standard library can also
stream the gzip files:

```python
import gzip
import json
from pathlib import Path

path = Path("datasets/1000.jsonl")  # Or, for example, datasets/103.jsonl.gz.
opener = gzip.open if path.suffix == ".gz" else open
with opener(path, "rt", encoding="utf-8-sig") as stream:
    for line in stream:
        record = json.loads(line)
        # Process one record at a time.
```

## Prepare and verify all JSONL files

Python 3.9 or newer is sufficient; no third-party packages are required.

```sh
python extract_datasets.py --output jsonl
```

This copies the plain files and extracts the archives into `jsonl/`, using the
original filenames and verifying each output against its source SHA-256 in the
manifest. Existing matching files are kept; existing files with different
content cause an error. Preparing the complete collection in a separate
directory requires free space at least equal to `total_source_bytes`.

To verify all stored files without copying or extracting them:

```sh
python extract_datasets.py --verify-only
```

GitHub [blocks regular Git files larger than 100 MiB](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
This collection stores files below that threshold directly and uses gzip only
for files at or above it. Git LFS is not needed. Git attributes disable newline
conversion for `.jsonl` files so their original bytes and checksums are preserved.
