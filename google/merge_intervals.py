"""
Merge Intervals
===============

PROBLEM PROMPT
--------------
Given an array of `intervals` where intervals[i] = [start_i, end_i], merge all
overlapping intervals, and return an array of the non-overlapping intervals that
cover all the intervals in the input.

Example 1:
    Input:  intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    Output: [[1, 6], [8, 10], [15, 18]]
    Explanation: Intervals [1, 3] and [2, 6] overlap, so they merge into [1, 6].

Example 2:
    Input:  intervals = [[1, 4], [4, 5]]
    Output: [[1, 5]]
    Explanation: Intervals [1, 4] and [4, 5] are considered overlapping (they
                 touch at 4), so they merge into [1, 5].

Constraints:
    1 <= len(intervals) <= 10^4
    intervals[i].length == 2
    0 <= start_i <= end_i <= 10^4
"""


def merge(intervals):
    """
    Merge all overlapping intervals and return the non-overlapping result.

    APPROACH (Sort by Start, Then Sweep)
    ------------------------------------
    If the intervals are in arbitrary order, an overlapping pair could sit
    anywhere relative to each other, which is awkward to reason about. The key
    move is to SORT the intervals by their start value. Once sorted, any
    interval that overlaps a given one must come immediately after it — so we
    only ever need to compare each interval with the last one we kept.

    We walk through the sorted intervals, maintaining a `merged` list whose last
    entry is the interval we're currently extending:

      - If the current interval's start is <= the end of the last merged
        interval, they overlap (or touch), so we merge them by extending the
        last interval's end to the maximum of the two ends. We use `max` because
        the current interval might sit entirely inside the previous one (e.g.
        [1, 9] then [2, 5]), in which case the end should not shrink.

      - Otherwise there's a gap, so the current interval starts a brand-new
        non-overlapping block, and we append it as-is.

    Touching intervals like [1, 4] and [4, 5] are treated as overlapping because
    the condition uses `<=`.

    COMPLEXITY
    ----------
    Time  : O(n log n) — dominated by the sort. The subsequent single sweep is
            O(n).
    Space : O(n) — for the output list (and O(n) or O(log n) for the sort's
            internal usage, depending on implementation). No extra space beyond
            the result grows with the input.

    Args:
        intervals (list[list[int]]): The list of [start, end] intervals.

    Returns:
        list[list[int]]: The merged, non-overlapping intervals sorted by start.
    """
    # Sort by start so that any overlaps are always adjacent in the sequence.
    intervals.sort(key=lambda interval: interval[0])

    merged = []
    for interval in intervals:
        # No intervals yet, or a clean gap between this interval and the last
        # merged one -> start a new block. Copy the interval so we can safely
        # mutate its end later without touching the original input.
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval[:])
        else:
            # Overlap (or touch): extend the last block's end to cover this one.
            # max() guards against a fully-contained interval shrinking the end.
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))  # -> [[1, 6], [8, 10], [15, 18]]
    print(merge([[1, 4], [4, 5]]))                      # -> [[1, 5]] (touching)
    print(merge([[1, 4], [2, 3]]))                      # -> [[1, 4]] (fully contained)
    print(merge([[1, 4], [0, 4]]))                      # -> [[0, 4]] (unsorted input)
    print(merge([[1, 4]]))                              # -> [[1, 4]] (single interval)
