def merge_intervals(intervals):
    """Merge overlapping or touching intervals.

    Takes a list of [start, end] integer pairs in any order and returns the
    merged list sorted by start. Overlapping or touching intervals are merged
    (e.g. [[1, 2], [2, 3]] -> [[1, 3]]). Input is not mutated.

    Example: [[1, 3], [2, 6]] -> [[1, 6]]
    """
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            # Copy so we never mutate the caller's inner lists.
            merged.append([start, end])
    return merged
