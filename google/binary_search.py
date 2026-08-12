"""
Binary Search
=============

PROBLEM PROMPT
--------------
Given an array of integers `nums` which is sorted in ASCENDING order, and an
integer `target`, write a function to search `target` in `nums`. If `target`
exists, return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input:  nums = [-1, 0, 3, 5, 9, 12], target = 9
    Output: 4
    Explanation: 9 exists in nums and its index is 4.

Example 2:
    Input:  nums = [-1, 0, 3, 5, 9, 12], target = 2
    Output: -1
    Explanation: 2 does not exist in nums so return -1.

Constraints:
    1 <= len(nums) <= 10^4
    -10^4 < nums[i], target < 10^4
    All the integers in nums are UNIQUE.
    nums is sorted in ascending order.
"""


def search(nums, target):
    """
    Return the index of `target` in the sorted array `nums`, or -1 if absent.

    APPROACH (Iterative binary search on a closed interval)
    -------------------------------------------------------
    Binary search repeatedly halves the portion of the array that could still
    contain `target`. We track that portion with two pointers, `lo` and `hi`,
    and this implementation treats [lo, hi] as a CLOSED interval -- both ends are
    still candidates.

    THE INVARIANT (the thing that must stay true every loop iteration):
        If `target` is in `nums` at all, its index is within [lo, hi].
    We start with lo = 0 and hi = n - 1, so the interval is the whole array and
    the invariant holds trivially. Every step shrinks [lo, hi] while preserving
    it, so we never discard the answer.

    Each iteration:
      1. mid = lo + (hi - lo) // 2
         We compute the midpoint this way rather than (lo + hi) // 2 to avoid
         integer overflow when lo + hi exceeds the max int. (In Python ints are
         arbitrary-precision so it can't actually overflow, but this is the habit
         to carry into languages where it can -- and interviewers look for it.)
      2. Compare nums[mid] to target:
         - nums[mid] == target -> found it, return mid.
         - nums[mid] <  target -> target, if present, is strictly to the RIGHT,
           so discard mid and everything left of it: lo = mid + 1.
         - nums[mid] >  target -> target is strictly to the LEFT, so discard mid
           and everything right of it: hi = mid - 1.

    THE TWO DETAILS THAT MAKE IT CORRECT (and are the usual bug sources):

      - Loop condition `while lo <= hi` (NOT `lo < hi`). Because the interval is
        CLOSED, lo == hi is still a valid one-element interval that we must
        inspect. Using `<` would exit early and miss a target sitting at that
        last index.

      - Updates `mid + 1` / `mid - 1` (NOT `mid`). Since we've just tested mid
        and it wasn't the target, we EXCLUDE it from the next interval. Writing
        lo = mid (or hi = mid) can leave the interval the same size when it has
        two elements, producing an INFINITE LOOP. Moving past mid guarantees the
        interval strictly shrinks every iteration, so the loop always terminates.

    When lo > hi the interval is empty: every index has been ruled out, so
    `target` isn't present -> return -1.

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(log n) -- each iteration halves the search interval.
    Space : O(1) -- only two pointers, no recursion.

    Args:
        nums (list[int]): A list sorted in ascending order.
        target (int): The value to locate.

    Returns:
        int: The index of `target`, or -1 if it is not in `nums`.
    """
    lo, hi = 0, len(nums) - 1

    # [lo, hi] is a CLOSED interval; lo == hi is still worth checking.
    while lo <= hi:
        # Midpoint written to avoid overflow in fixed-width-int languages.
        mid = lo + (hi - lo) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1        # target is to the right; drop mid and its left
        else:
            hi = mid - 1        # target is to the left; drop mid and its right

    # Interval emptied out -> target not present.
    return -1


def search_recursive(nums, target):
    """
    Recursive variant of binary search, same logic and complexity.

    APPROACH
    --------
    Identical closed-interval reasoning as `search`, expressed with recursion
    instead of a loop. Each call inspects the midpoint of [lo, hi] and recurses
    into whichever half can still contain `target`. The base case lo > hi means
    the interval is empty -> return -1.

    COMPLEXITY
    ----------
    Time  : O(log n).
    Space : O(log n) for the recursion stack (vs O(1) for the iterative form) --
            a reason to prefer the iterative version in practice.

    Args:
        nums (list[int]): A list sorted in ascending order.
        target (int): The value to locate.

    Returns:
        int: The index of `target`, or -1 if it is not in `nums`.
    """
    def helper(lo, hi):
        if lo > hi:                       # empty interval -> not found
            return -1
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            return helper(mid + 1, hi)    # search the right half
        return helper(lo, mid - 1)        # search the left half

    return helper(0, len(nums) - 1)


if __name__ == "__main__":
    # Quick sanity checks.
    print(search([-1, 0, 3, 5, 9, 12], 9))    # -> 4
    print(search([-1, 0, 3, 5, 9, 12], 2))    # -> -1  (absent)
    print(search([5], 5))                      # -> 0   (single element, hit)
    print(search([5], -5))                     # -> -1  (single element, miss)
    print(search([], 1))                       # -> -1  (empty array)
    print(search([1, 2, 3, 4, 5], 1))          # -> 0   (first element)
    print(search([1, 2, 3, 4, 5], 5))          # -> 4   (last element)

    # The recursive variant returns the same indices.
    print(search_recursive([-1, 0, 3, 5, 9, 12], 9))   # -> 4
    print(search_recursive([-1, 0, 3, 5, 9, 12], 2))   # -> -1

    # Exhaustive cross-check against Python's built-in membership on a range.
    arr = list(range(0, 100, 2))   # even numbers 0..98
    ok = all(
        (search(arr, t) == (arr.index(t) if t in arr else -1))
        for t in range(-2, 101)
    )
    print(ok)                                   # -> True
