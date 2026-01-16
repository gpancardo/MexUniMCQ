from pathlib import Path
import json
import argparse
import logging
import sys

#!/usr/bin/env python3
"""
Aggregate all .jsonl files in the script directory into MexUniMCQ.jsonl.

Usage:
    python aggregate.py              # aggregate files in the same folder as this script
    python aggregate.py -d PATH      # aggregate files in PATH
    python aggregate.py -o OUT.jsonl # specify output filename
    python aggregate.py --dedupe     # remove duplicate JSON objects (canonicalized)
    python aggregate.py --overwrite  # overwrite existing output
"""

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def aggregate(folder: Path, out_file: Path, dedupe: bool = False, overwrite: bool = False):
    if not folder.is_dir():
        logging.error("Provided folder does not exist: %s", folder)
        sys.exit(2)

    if out_file.exists() and not overwrite:
        logging.error("Output file exists (%s). Use --overwrite to replace.", out_file)
        sys.exit(2)

    jsonl_files = sorted([p for p in folder.glob("*.jsonl") if p.name != out_file.name and not p.name.startswith(".")])
    if not jsonl_files:
        logging.info("No .jsonl files found in %s", folder)
        return

    seen = set() if dedupe else None
    written = 0
    read_lines = 0

    with out_file.open("w", encoding="utf-8") as out:
        for p in jsonl_files:
            logging.info("Reading %s", p.name)
            with p.open("r", encoding="utf-8") as fh:
                for lineno, raw in enumerate(fh, start=1):
                    line = raw.rstrip("\n")
                    if not line.strip():
                        continue
                    read_lines += 1
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError as e:
                        logging.warning("Skipping invalid JSON in %s:%d (%s)", p.name, lineno, e)
                        continue

                    if dedupe:
                        canon = json.dumps(obj, separators=(",", ":"), sort_keys=True)
                        if canon in seen:
                            continue
                        seen.add(canon)
                        out.write(canon + "\n")
                    else:
                        out.write(line + "\n")
                    written += 1

    logging.info("Wrote %d lines (read %d) into %s", written, read_lines, out_file)


def main():
    default_folder = Path(__file__).parent
    parser = argparse.ArgumentParser(description="Aggregate JSONL files into a single MexUniMCQ.jsonl")
    parser.add_argument("-d", "--dir", type=Path, default=default_folder, help="Folder containing .jsonl files (default: script folder)")
    parser.add_argument("-o", "--output", type=Path, default=default_folder / "MexUniMCQ.jsonl", help="Output JSONL file name (default: MexUniMCQ.jsonl)")
    parser.add_argument("--dedupe", action="store_true", help="Deduplicate JSON objects (canonicalized)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output if it exists")
    args = parser.parse_args()

    aggregate(args.dir, args.output, dedupe=args.dedupe, overwrite=args.overwrite)


if __name__ == "__main__":
    main()