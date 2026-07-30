"""
Insert Interval
===============

PROBLEM PROMPT
--------------
You are given an array of non-overlapping intervals `intervals` where
intervals[i] = [start_i, end_i] represent the start and the end of the i-th
interval, and `intervals` is sorted in ascending order by start_i. You are also
given an interval `newInterval` = [start, end] that represents the start and end
of another interval.

Insert `newInterval` into `intervals` such that `intervals` is still sorted in
ascending order by start_i and still does not have any overlapping intervals
(merge overlapping intervals if necessary).

Return `intervals` after the insertion.

Note that you don't need to modify `intervals` in-place. You can make a new array
and return it.

Example 1:
    Input:  intervals = [[1, 3], [6, 9]], newInterval = [2, 5]
    Output: [[1, 5], [6, 9]]

Example 2:
    Input:  intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]],
            newInterval = [4, 8]
    Output: [[1, 2], [3, 10], [12, 16]]
    Explanation: Because the new interval [4, 8] overlaps with [3, 5], [6, 7],
                 [8, 10], they merge into [3, 10].

Constraints:
    0 <= len(intervals) <= 10^4
    intervals[i].length == 2
    0 <= start_i <= end_i <= 10^5
    intervals is sorted by start_i in ascending order.
    newInterval.length == 2
    0 <= start <= end <= 10^5
"""


def insert(intervals, new_interval):
    """
    Insert new_interval into a sorted, non-overlapping interval list and merge.

    APPROACH (Single Linear Sweep in Three Phases)
    ----------------------------------------------
    Because the existing intervals are already SORTED by start and don't overlap
    each other, we don't need to sort anything. We can walk through them once and
    place them into three natural groups relative to `new_interval`:

      1. BEFORE — intervals that end strictly before new_interval starts
         (interval_end < new_start). These lie entirely to the left with no
         overlap, so we copy them into the result unchanged.

      2. OVERLAPPING — intervals that overlap new_interval. Two intervals overlap
         when each starts on or before the other ends, i.e.
         interval_start <= new_end AND interval_end >= new_start. Rather than add
         these individually, we absorb them into new_interval by expanding it:
             new_start = min(new_start, interval_start)
             new_end   = max(new_end,   interval_end)
         After consuming all overlappers, we append the single merged interval.

      3. AFTER — intervals that start strictly after new_interval ends
         (interval_start > new_end). These lie entirely to the right, so we copy
         them in unchanged.

    Since the list is sorted, these three groups appear in exactly this order as
    we scan left to right, so a single pass with three sequential loops handles
    them cleanly — no back-tracking needed.

    COMPLEXITY
    ----------
    Time  : O(n) — each of the n existing intervals is examined exactly once
            across the three phases.
    Space : O(n) — for the output list holding up to n + 1 intervals. Only O(1)
            extra working space is used beyond the result.

    Args:
        intervals (list[list[int]]): Sorted, non-overlapping intervals.
        new_interval (list[int]): The [start, end] interval to insert.

    Returns:
        list[list[int]]: The resulting sorted, non-overlapping interval list.
    """
    result = []
    i = 0
    n = len(intervals)
    new_start, new_end = new_interval[0], new_interval[1]

    # Phase 1: add all intervals that end before new_interval starts (no overlap).
    while i < n and intervals[i][1] < new_start:
        result.append(intervals[i])
        i += 1

    # Phase 2: merge every interval that overlaps new_interval by expanding the
    # new interval's bounds to cover them all.
    while i < n and intervals[i][0] <= new_end:
        new_start = min(new_start, intervals[i][0])
        new_end = max(new_end, intervals[i][1])
        i += 1
    result.append([new_start, new_end])  # append the single merged interval

    # Phase 3: add all remaining intervals that start after new_interval ends.
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(insert([[1, 3], [6, 9]], [2, 5]))                                  # -> [[1, 5], [6, 9]]
    print(insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]))       # -> [[1, 2], [3, 10], [12, 16]]
    print(insert([], [5, 7]))                                                # -> [[5, 7]] (empty input)
    print(insert([[1, 5]], [2, 3]))                                          # -> [[1, 5]] (new inside existing)
    print(insert([[1, 5]], [6, 8]))                                          # -> [[1, 5], [6, 8]] (no overlap, after)
    print(insert([[3, 5]], [1, 2]))                                          # -> [[1, 2], [3, 5]] (no overlap, before)
