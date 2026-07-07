#!/usr/bin/env python3
"""Count word frequencies in a text file.

Usage: python wordfreq.py <file> [--top N] [--min-len L]
"""
import argparse
import re
import sys
from collections import Counter

# A word is a maximal run of ASCII letters; everything else separates.
WORD_RE = re.compile(r"[a-zA-Z]+")


def main() -> int:
    parser = argparse.ArgumentParser(description="Count word frequencies in a text file.")
    parser.add_argument("file", help="input text file")
    parser.add_argument("--top", type=int, default=None, help="print only the first N lines")
    parser.add_argument("--min-len", type=int, default=1, help="ignore words shorter than L characters")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        print(f"error: cannot read '{args.file}': {e}", file=sys.stderr)
        return 1

    counts = Counter(
        w for w in (m.group().lower() for m in WORD_RE.finditer(text))
        if len(w) >= args.min_len
    )

    # Sort by count descending, then word ascending for ties.
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    if args.top is not None:
        ordered = ordered[: args.top]

    out = "".join(f"{word} {count}\n" for word, count in ordered)
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
