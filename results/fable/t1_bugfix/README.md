# Task: fix merge_intervals

Users report wrong results from `merge_intervals` in `intervals.py`.

## Required behavior (the spec)

`merge_intervals(intervals)` takes a list of `[start, end]` integer pairs and returns
the merged list:

1. Intervals that overlap OR touch must be merged: `[[1,2],[2,3]]` -> `[[1,3]]`.
2. Input may be in ANY order; output must be sorted by start.
3. The input list and its inner lists must NOT be mutated.
4. Empty input returns `[]`.

## Deliverable

Fix `intervals.py` so it meets the spec. `test_basic.py` shows one known-good case.
Your fix will be graded against the spec above.
