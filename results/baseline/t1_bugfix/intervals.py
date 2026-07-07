def merge_intervals(intervals):
    """Merge overlapping or touching intervals.

    Takes a list of [start, end] integer pairs and returns the merged list,
    sorted by start. Intervals that overlap or merely touch are combined:
    [[1, 2], [2, 3]] -> [[1, 3]]. The input and its inner lists are not mutated.

    Example: [[1, 3], [2, 6]] -> [[1, 6]]
    """
    # Sort a copy by start so any input order works and the input is untouched.
    ordered = sorted(intervals, key=lambda pair: pair[0])
    merged = []
    for start, end in ordered:
        if merged and start <= merged[-1][1]:
            # Overlaps or touches the last merged interval; extend it.
            merged[-1][1] = max(merged[-1][1], end)
        else:
            # Fresh copy so we never mutate the caller's inner lists.
            merged.append([start, end])
    return merged
