# Strategic Decision LLM datasets

JSON Lines datasets packaged as individual `.jsonl.gz` files. Each archive
preserves the exact bytes of its corresponding local JSONL source. Original
filenames, including `_synthetic` suffixes, are retained.

This snapshot contains **398 files**, **4,054,073 lines**, and **19,010,996,896
uncompressed bytes**, packaged into **249,576,203 compressed bytes**. Of the
398 filenames, 31 carry the `_synthetic` suffix.

## Files

- `datasets/`: one gzip archive per source JSONL file.
- `manifest.json`: source and archive filenames, byte sizes, SHA-256 checksums,
  and line counts for every file, plus collection totals.
- `extract_datasets.py`: extract the collection and verify source checksums.

The manifest's `synthetic_filename_marker` records the filename suffix only.
Line counts describe the files; they are not independently verified counts of
unique human decisions or participants. Packaging checks establish file
integrity, not research validity or training suitability. No per-study source
documentation or new data license is added by this upload.

## Read compressed data directly

Python's standard library can stream an archive without extracting it:

```python
import gzip
import json

with gzip.open("datasets/1000.jsonl.gz", "rt", encoding="utf-8-sig") as stream:
    for line in stream:
        record = json.loads(line)
        # Process one record at a time.
```

## Extract and verify

Python 3.9 or newer is sufficient; no third-party packages are required.

```sh
python extract_datasets.py --output jsonl
```

This creates the original JSONL filenames in `jsonl/` and checks each file
against its source SHA-256 in the manifest. Existing matching files are kept;
existing files with different content cause an error. Extraction requires free
disk space at least equal to `total_source_bytes` in the manifest.

To check compressed archives without extracting them:

```sh
python extract_datasets.py --verify-only
```

Gzip is used because several uncompressed source files exceed GitHub's regular
Git file-size limit. All archives are ordinary Git files; Git LFS is not needed.
