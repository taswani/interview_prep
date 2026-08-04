"""
Top K Frequent Elements
=======================

PROBLEM PROMPT
--------------
Given an integer array `nums` and an integer `k`, return the `k` most frequent
elements. You may return the answer in any order.

Example 1:
    Input:  nums = [1, 1, 1, 2, 2, 3], k = 2
    Output: [1, 2]
    Explanation: 1 appears three times, 2 appears twice, 3 appears once. The two
                 most frequent elements are 1 and 2.

Example 2:
    Input:  nums = [1], k = 1
    Output: [1]

Constraints:
    1 <= len(nums) <= 10^5
    -10^4 <= nums[i] <= 10^4
    k is in the range [1, the number of unique elements in the array].
    It is guaranteed that the answer is unique.

Follow-up:
    Your algorithm's time complexity must be better than O(n log n), where n is
    the array's size. The bucket-sort solution below runs in O(n).
"""

import heapq
from collections import Counter


def top_k_frequent(nums, k):
    """
    Return the k most frequently occurring elements in `nums`.

    APPROACH (Frequency Count + Bucket Sort)
    ----------------------------------------
    First we tally how many times each number appears (a hash-map count). The
    challenge is then to pick the k numbers with the highest counts efficiently.

    Sorting the numbers by frequency would work but costs O(n log n), which the
    follow-up asks us to beat. The key observation that unlocks O(n): a
    frequency can never exceed n (a number can appear at most n times in an
    array of length n). So we can BUCKET numbers by their exact frequency using
    an array indexed by count:

        buckets[f] = list of numbers that appear exactly f times

    This is a bucket sort keyed on frequency. Because the index IS the frequency,
    the buckets are implicitly ordered by frequency for free — no comparison
    sorting needed.

    Finally we walk the buckets from the HIGHEST frequency down to the lowest,
    collecting numbers until we have k of them. Since the problem guarantees a
    unique answer, we never have to break ties arbitrarily.

    COMPLEXITY
    ----------
    Time  : O(n) — counting is O(n), building the buckets is O(unique elements)
            <= O(n), and scanning buckets to collect k answers is O(n). No
            O(n log n) sort is involved.
    Space : O(n) — the count map and the bucket array together hold O(n) entries.

    Args:
        nums (list[int]): The input array.
        k (int): How many of the most frequent elements to return.

    Returns:
        list[int]: The k most frequent elements (in arbitrary order).
    """
    # Step 1: count occurrences of each number. Counter is a hash map of counts.
    counts = Counter(nums)

    # Step 2: bucket numbers by frequency. Index f holds numbers seen f times.
    # We need indices 0..len(nums), so the array has len(nums) + 1 slots.
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in counts.items():
        buckets[freq].append(num)

    # Step 3: walk from the highest frequency downward, gathering k elements.
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:   # Collected enough — stop early.
                return result

    return result  # Reached only if k covers every unique element.


def top_k_frequent_heap(nums, k):
    """
    Return the k most frequent elements using a bounded min-heap.

    APPROACH (Frequency Count + Min-Heap of Size k)
    -----------------------------------------------
    As before, we first tally each number's frequency with a hash map. To select
    the top k, we maintain a MIN-heap keyed on frequency that never holds more
    than k entries:

      - We push each (frequency, number) pair onto the heap.
      - Whenever the heap grows past k entries, we pop the SMALLEST — i.e. the
        least frequent number currently held. This evicts weak candidates early.

    Because it's a min-heap, the element at the top is always the least frequent
    of the k we're keeping, so it's exactly the right one to discard when a more
    frequent number arrives. After processing every unique number, the heap holds
    precisely the k most frequent ones.

    WHY CHOOSE THIS OVER THE BUCKET SORT?
    -------------------------------------
    It is NOT asymptotically faster — O(n log k) is strictly worse than the
    bucket sort's O(n). Prefer it when:
      - k is small relative to n, so the heap only ever holds O(k) entries
        (smaller working space than an n-sized bucket array), and log k is tiny.
      - The data is streamed / n is not known up front, so a fixed-size bucket
        array cannot be pre-allocated.
    Python's heapq is a min-heap, which is exactly what a "keep the largest k"
    bounded heap needs.

    COMPLEXITY
    ----------
    Let u = number of unique elements (u <= n).
    Time  : O(n + u log k) — O(n) to count, then u pushes/pops each costing
            O(log k) because the heap is capped at size k. This is better than a
            full O(n log n) sort but not as good as the O(n) bucket sort.
    Space : O(u + k) — the count map is O(u) and the heap is O(k).

    Args:
        nums (list[int]): The input array.
        k (int): How many of the most frequent elements to return.

    Returns:
        list[int]: The k most frequent elements (in arbitrary order).
    """
    # Step 1: count occurrences of each number.
    counts = Counter(nums)

    # Step 2: keep a min-heap of at most k (frequency, number) pairs. When it
    # overflows, popping the smallest frequency evicts the weakest candidate.
    heap = []
    for num, freq in counts.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)

    # Step 3: the heap now holds the k most frequent numbers; extract them.
    # (The frequency in each pair is no longer needed, so it's discarded as `_`.)
    return [num for _, num in heap]


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))     # -> [1, 2]
    print(top_k_frequent([1], 1))                     # -> [1]
    print(top_k_frequent([4, 4, 4, 6, 6, 7], 1))      # -> [4]
    print(sorted(top_k_frequent([5, 5, 6, 6, 7], 2))) # -> [5, 6] (order may vary)
    print(top_k_frequent([1, 2, 3, 4], 4))            # -> [1, 2, 3, 4] (all unique)

    # The heap variant returns the same set (order may differ).
    print(sorted(top_k_frequent_heap([1, 1, 1, 2, 2, 3], 2)))  # -> [1, 2]
    print(top_k_frequent_heap([1], 1))                         # -> [1]
    print(sorted(top_k_frequent_heap([4, 4, 4, 6, 6, 7], 1)))  # -> [4]
