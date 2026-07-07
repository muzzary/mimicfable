#!/usr/bin/env python3
"""Count word frequencies in a text file.

A word is a maximal run of ASCII letters; counting is case-insensitive.
Output is `word count`, sorted by count descending then word ascending.
"""
import argparse
import re
import sys
from collections import Counter

WORD_RE = re.compile(r"[A-Za-z]+")


def main() -> int:
    parser = argparse.ArgumentParser(description="Count word frequencies in a text file.")
    parser.add_argument("file", help="path to the text file")
    parser.add_argument("--top", type=int, help="print only the first N lines")
    parser.add_argument("--min-len", type=int, default=1, help="ignore words shorter than L")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        print(f"wordfreq: cannot read {args.file}: {e.strerror}", file=sys.stderr)
        return 1

    counts = Counter(
        w for w in WORD_RE.findall(text.lower()) if len(w) >= args.min_len
    )

    # Count descending, then word ascending for ties.
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    if args.top is not None:
        ordered = ordered[: max(args.top, 0)]

    out = "".join(f"{word} {count}\n" for word, count in ordered)
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
