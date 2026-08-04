"""
K Closest Points to Origin
==========================

PROBLEM PROMPT
--------------
Given an array of `points` where points[i] = [x_i, y_i] represents a point on
the X-Y plane and an integer `k`, return the `k` closest points to the origin
(0, 0).

The distance between two points on the X-Y plane is the Euclidean distance
(sqrt((x1 - x2)^2 + (y1 - y2)^2)).

You may return the answer in any order. The answer is guaranteed to be unique
(except for the order that it is in).

Example 1:
    Input:  points = [[1, 3], [-2, 2]], k = 1
    Output: [[-2, 2]]
    Explanation:
        The distance between (1, 3) and the origin is sqrt(10).
        The distance between (-2, 2) and the origin is sqrt(8).
        Since sqrt(8) < sqrt(10), (-2, 2) is closer, and it is the closest point.

Example 2:
    Input:  points = [[3, 3], [5, -1], [-2, 4]], k = 2
    Output: [[3, 3], [-2, 4]]
    Explanation: The answer [[-2, 4], [3, 3]] would also be accepted.

Constraints:
    1 <= k <= len(points) <= 10^4
    -10^4 <= x_i, y_i <= 10^4
"""

import heapq


def k_closest(points, k):
    """
    Return the k points closest to the origin (0, 0).

    APPROACH (Max-Heap of Size k on Squared Distance)
    -------------------------------------------------
    We want the k smallest distances. Two simplifications make this efficient:

      1. SKIP THE SQUARE ROOT. Euclidean distance is sqrt(x^2 + y^2), but sqrt is
         monotonic — it preserves ordering. So comparing x^2 + y^2 gives the same
         "which is closer" answers as comparing the true distances, while
         avoiding a costly (and floating-point-imprecise) sqrt. We rank by
         SQUARED distance.

      2. USE A BOUNDED MAX-HEAP OF SIZE k. To keep the k closest points, we keep
         a heap that holds at most k of them, where the point currently FARTHEST
         from the origin sits at the top (ready to be evicted). Python's heapq is
         a MIN-heap, so we store NEGATED squared distances to simulate a max-heap
         — the most-negative value (the largest true distance) rises to the top.

    We push each point's (-squared_distance, point) onto the heap; whenever the
    heap exceeds k entries, we pop the top, which discards the farthest of the
    current candidates. After processing all points, the heap holds exactly the
    k closest, and we extract their coordinates.

    (Alternative: Quickselect partitions the array around the k-th closest in
    O(n) average time — faster asymptotically — but the heap is simpler, stable
    in the worst case, and ideal when points stream in or k is small.)

    COMPLEXITY
    ----------
    Let n = number of points.
    Time  : O(n log k) — each of the n points triggers a heap push/pop costing
            O(log k), since the heap never holds more than k elements. This beats
            the O(n log n) of sorting all points by distance.
    Space : O(k) — the heap stores at most k points at any time.

    Args:
        points (list[list[int]]): The points as [x, y] pairs.
        k (int): How many closest points to return.

    Returns:
        list[list[int]]: The k closest points to the origin (in arbitrary order).
    """
    # Max-heap (via negated distances) capped at size k.
    heap = []

    for x, y in points:
        # Squared distance to origin — no sqrt needed since it preserves order.
        dist = x * x + y * y

        # Negate so heapq's min-heap behaves as a max-heap: the farthest point
        # (largest dist -> most negative key) sits at the top for easy eviction.
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)  # Drop the current farthest candidate.

    # The heap now holds the k closest points; return just their coordinates.
    return [[x, y] for _, x, y in heap]


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(k_closest([[1, 3], [-2, 2]], 1))                # -> [[-2, 2]]
    print(sorted(k_closest([[3, 3], [5, -1], [-2, 4]], 2)))  # -> [[-2, 4], [3, 3]] (order may vary)
    print(k_closest([[0, 0]], 1))                         # -> [[0, 0]] (the origin itself)
    print(sorted(k_closest([[1, 1], [1, 1], [2, 2]], 2)))  # -> [[1, 1], [1, 1]] (ties)
    print(sorted(k_closest([[1, 0], [0, 1], [2, 0]], 3)))  # -> [[0, 1], [1, 0], [2, 0]] (k == n)
