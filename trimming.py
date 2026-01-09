import argparse
import json
import sys
import random
import tempfile
import shutil
from collections import Counter
from pathlib import Path
from typing import Optional

#!/usr/bin/env python3

def count_temas(path: Path):
    counts = Counter()
    total = 0
    missing = 0
    with path.open("r", encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON on line {ln}: {e}", file=sys.stderr)
                continue
            tema = obj.get("tema")
            if tema is None:
                counts["<MISSING>"] += 1
                missing += 1
            else:
                counts[tema] += 1
            total += 1
    return counts, total, missing

def main():
    parser = argparse.ArgumentParser(description="Count or trim entries per 'tema' in a .jsonl file")
    parser.add_argument("file", nargs="?", default="subjects/matematicas.jsonl", help="path to JSONL file")
    parser.add_argument("--drop", "-d", type=int, default=0, help="total number of entries to drop across temas")
    parser.add_argument("--threshold", "-t", type=int, default=9, help="minimum entries to keep per tema")
    parser.add_argument("--seed", type=int, default=None, help="random seed for deterministic trimming")
    parser.add_argument("--output", "-o", help="output file path (default: <input>.trimmed.jsonl)")
    parser.add_argument("--inplace", action="store_true", help="overwrite input file")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(2)

    counts, total, missing = count_temas(path)
    for tema, cnt in counts.most_common():
        print(f"{tema}\t{cnt}")
    print(f"\nTotal lines processed: {total}", file=sys.stderr)
    if missing:
        print(f"Lines missing 'tema': {missing}", file=sys.stderr)
    if args.drop > 0:
        removed, out_path = trim_jsonl(path, drop=args.drop, threshold=args.threshold, seed=args.seed, output=args.output, inplace=args.inplace)
        print(f"Wrote trimmed output to: {out_path}", file=sys.stderr)
        return

def trim_jsonl(path: Path, drop: int = 41, threshold: int = 9, seed: Optional[int] = None, output: Optional[str] = None, inplace: bool = False):
    """
    Trim up to `drop` entries from `path` by removing one random entry per eligible 'tema'
    in repeated passes until `drop` entries are removed or no eligible temas remain.
    A 'tema' is eligible when it currently has more than `threshold` entries.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    tema_indices = {}
    for i, line in enumerate(lines):
        line_strip = line.strip()
        if not line_strip:
            continue
        try:
            obj = json.loads(line_strip)
        except json.JSONDecodeError:
            continue
        tema = obj.get("tema")
        if tema is None:
            continue
        tema_indices.setdefault(tema, []).append(i)

    rng = random.Random(seed)
    indices = {t: list(idxs) for t, idxs in tema_indices.items()}
    eligible = [t for t, idxs in indices.items() if len(idxs) > threshold]
    remove_flags = [False] * len(lines)
    removed = 0

    while removed < drop and eligible:
        rng.shuffle(eligible)
        for tema in list(eligible):
            if removed >= drop:
                break
            idxs = indices.get(tema, [])
            if len(idxs) <= threshold:
                try:
                    eligible.remove(tema)
                except ValueError:
                    pass
                continue
            pick = rng.choice(idxs)
            remove_flags[pick] = True
            idxs.remove(pick)
            removed += 1
            if len(idxs) <= threshold:
                try:
                    eligible.remove(tema)
                except ValueError:
                    pass

    if output:
        out_path = Path(output)
    else:
        out_path = path.with_name(path.stem + ".trimmed" + path.suffix)

    if inplace:
        tmp = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
        tmp_path = Path(tmp.name)
        with tmp as fh:
            for i, line in enumerate(lines):
                if not remove_flags[i]:
                    fh.write(line.rstrip("\n") + "\n")
        shutil.move(str(tmp_path), str(path))
        out_path_real = path
    else:
        with out_path.open("w", encoding="utf-8") as fh:
            for i, line in enumerate(lines):
                if not remove_flags[i]:
                    fh.write(line.rstrip("\n") + "\n")
        out_path_real = out_path

    print(f"Removed {removed} entries (requested {drop}).", file=sys.stderr)
    return removed, out_path_real



if __name__ == "__main__":
    main()



