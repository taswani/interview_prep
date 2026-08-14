"""
Koko Eating Bananas
===================

PROBLEM PROMPT
--------------
Koko loves to eat bananas. There are `n` piles of bananas, the i-th pile has
piles[i] bananas. The guards have gone and will come back in `h` hours.

Koko can decide her banana-eating speed of `k` bananas per hour. Each hour, she
chooses some pile and eats k bananas from it. If the pile has fewer than k
bananas, she eats all of them instead and will NOT eat any more bananas during
that hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before
the guards return. Return the MINIMUM integer `k` such that she can eat all the
bananas within `h` hours.

Example 1:
    Input:  piles = [3, 6, 7, 11], h = 8    -> Output: 4
Example 2:
    Input:  piles = [30, 11, 23, 4, 20], h = 5   -> Output: 30
Example 3:
    Input:  piles = [30, 11, 23, 4, 20], h = 6   -> Output: 23

Constraints:
    1 <= len(piles) <= 10^4
    piles.length <= h <= 10^9
    1 <= piles[i] <= 10^9
"""

import math


def min_eating_speed(piles, h):
    """
    Return the minimum eating speed `k` that lets Koko finish within `h` hours.

    APPROACH (Binary search on the ANSWER, not on an array)
    -------------------------------------------------------
    The previous binary-search problems searched positions inside a sorted array.
    This one has no array to index into -- instead we binary search over the
    RANGE OF POSSIBLE ANSWERS: the eating speed k. That's the key mental shift.
    The pattern is often called "binary search on the answer" or "parametric
    search," and it applies whenever:

        (a) the answer is an integer in a known range [lo, hi], AND
        (b) there's a MONOTONIC yes/no test: if speed k works, every speed > k
            also works; if k fails, every speed < k also fails.

    Here the yes/no test is "can Koko finish all piles in <= h hours at speed k?"
    It's monotonic because eating faster never takes more hours. So the feasible
    speeds form a sorted boolean pattern:

        k:        1    2    3   ...  ANS-1  ANS  ANS+1 ...
        feasible: no   no   no  ...  no     YES  YES   ...

    and we want the FIRST YES -- the leftmost feasible speed. That is exactly a
    "find the boundary" binary search over k.

    THE SEARCH BOUNDS:
      - lo = 1: the slowest meaningful speed (k must be at least 1).
      - hi = max(piles): eating faster than the biggest pile is pointless,
        because each hour Koko eats from only ONE pile and can't carry leftover
        capacity to another pile. At k = max(piles) every pile takes exactly one
        hour, giving len(piles) hours total, which is <= h by the constraint
        piles.length <= h. So hi is always feasible -- a valid upper bound.

    HOURS NEEDED AT SPEED k: for a single pile of size p, Koko needs
    ceil(p / k) hours (the last hour may be partial). Summing over piles gives
    the total. We compute ceil(p / k) as -(-p // k) or math.ceil(p / k); using
    integer math avoids float rounding issues on the large values here.

    THE BOUNDARY SEARCH (find the leftmost feasible k):
      - mid = lo + (hi - lo) // 2
      - if feasible(mid): mid MIGHT be the answer, but a smaller k could also
        work, so keep mid as a candidate and search left -> hi = mid.
      - else: mid is too slow, the answer is strictly faster -> lo = mid + 1.
      - Loop while lo < hi; they converge on the single leftmost feasible speed,
        which is the answer.

    NOTE this uses `while lo < hi` with `hi = mid` (a half-open convergence),
    NOT the `lo <= hi` / `hi = mid - 1` form from plain binary search. When
    searching for a BOUNDARY (leftmost value satisfying a predicate) rather than
    an exact match, we must keep mid as a live candidate, so we never do
    hi = mid - 1. lo and hi close in on the boundary and meet there.

    COMPLEXITY
    ----------
    Let n = len(piles) and M = max(piles).
    Time  : O(n * log M) -- the search runs O(log M) iterations over the speed
            range, and each feasibility check sums ceil over all n piles.
    Space : O(1).

    Args:
        piles (list[int]): Banana counts per pile.
        h (int): Hours available before the guards return.

    Returns:
        int: The minimum integer eating speed.
    """
    def hours_needed(k):
        # Total hours to clear every pile at speed k (each pile: ceil(p / k)).
        return sum(math.ceil(p / k) for p in piles)

    lo, hi = 1, max(piles)

    # Find the leftmost speed k for which hours_needed(k) <= h.
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if hours_needed(mid) <= h:
            hi = mid            # mid works; a slower speed might too -> keep mid
        else:
            lo = mid + 1        # mid too slow; the answer is strictly faster

    # lo == hi is the smallest feasible speed.
    return lo


if __name__ == "__main__":
    # Quick sanity checks.
    print(min_eating_speed([3, 6, 7, 11], 8))            # -> 4
    print(min_eating_speed([30, 11, 23, 4, 20], 5))      # -> 30  (h == #piles: max speed)
    print(min_eating_speed([30, 11, 23, 4, 20], 6))      # -> 23
    print(min_eating_speed([1], 1))                       # -> 1
    print(min_eating_speed([1000000000], 2))             # -> 500000000  (huge pile)
    print(min_eating_speed([312884470], 312884469))      # -> 2  (needs 2 hours max)

    # Cross-check against a brute-force linear scan of every speed on small input.
    def brute(piles, h):
        for k in range(1, max(piles) + 1):
            if sum(math.ceil(p / k) for p in piles) <= h:
                return k
        return max(piles)

    import random
    rng = random.Random(0)
    ok = True
    for _ in range(2000):
        piles = [rng.randint(1, 30) for _ in range(rng.randint(1, 6))]
        h = rng.randint(len(piles), 40)
        if min_eating_speed(piles, h) != brute(piles, h):
            ok = False
    print(ok)                                             # -> True
