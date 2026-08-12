"""
Search in Rotated Sorted Array
==============================

PROBLEM PROMPT
--------------
There is an integer array `nums` sorted in ascending order (with DISTINCT
values). Prior to being passed to your function, `nums` is possibly ROTATED at
an unknown pivot index k (0 <= k < len(nums)), so that the array becomes

    [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]

(0-indexed). For example, [0,1,2,4,5,6,7] rotated at pivot 3 becomes
[4,5,6,7,0,1,2].

Given the array `nums` AFTER the rotation and an integer `target`, return the
index of `target` if it is in `nums`, or -1 if it is not.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input:  nums = [4,5,6,7,0,1,2], target = 0   -> Output: 4
Example 2:
    Input:  nums = [4,5,6,7,0,1,2], target = 3   -> Output: -1
Example 3:
    Input:  nums = [1], target = 0               -> Output: -1

Constraints:
    1 <= len(nums) <= 5000
    -10^4 <= nums[i] <= 10^4
    All values of nums are unique.
    nums is an ascending array possibly rotated in the range [0, n-1].
    -10^4 <= target <= 10^4
"""


def search(nums, target):
    """
    Return the index of `target` in a rotated sorted array, or -1 if absent.

    APPROACH (Binary search + "which half is sorted?")
    --------------------------------------------------
    This is the standard closed-interval binary search from `binary_search.py`,
    with ONE extra idea layered on top. In a plain sorted array, comparing
    nums[mid] to target tells us which half to keep. Rotation breaks that: the
    array has a "cliff" where it wraps from a high value back down to a low one,
    so nums[mid] < target no longer implies "go right".

    THE KEY OBSERVATION: no matter where mid lands, AT LEAST ONE of the two
    halves [lo, mid] and [mid, hi] is fully sorted (has no cliff in it). The
    rotation point can sit in only one of them. So each iteration we:

      1. Detect which half is sorted by comparing the half's endpoints:
           - if nums[lo] <= nums[mid], the LEFT half [lo, mid] is sorted.
           - otherwise the RIGHT half [mid, hi] is sorted.
         (The `<=` matters for the two-element case where lo == mid.)

      2. Inside the SORTED half we can use ordinary range checks, because it has
         no cliff. Ask "does target fall within this sorted half's value range?"
           - Left sorted:  if nums[lo] <= target < nums[mid], target is in the
             left half -> hi = mid - 1; else it's in the other half -> lo = mid+1.
           - Right sorted: if nums[mid] < target <= nums[hi], target is in the
             right half -> lo = mid + 1; else -> hi = mid - 1.

    We always reason about the SORTED half (where range comparisons are valid)
    and decide whether target is in it. If it is, we go there; if it isn't, the
    answer must be in the other (unsorted) half, which we then recurse into and
    re-split -- one of ITS halves will be sorted, and so on.

    The bounds still shrink by mid +/- 1 every step (we've already checked mid
    for equality up front), so the O(log n) guarantee and termination argument
    carry over unchanged from plain binary search.

    WHY THE ENDPOINTS ARE INCLUSIVE where they are:
      - `nums[lo] <= target` and `target <= nums[hi]` include the endpoints
        because target could equal the first/last element of the sorted half.
      - `target < nums[mid]` and `nums[mid] < target` are STRICT because we
        already ruled out target == nums[mid] with the equality check, so mid
        itself never needs to be re-included.

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(log n) -- one comparison chain per iteration, interval halves.
    Space : O(1) -- two pointers, iterative.

    Args:
        nums (list[int]): A rotated ascending array of distinct integers.
        target (int): The value to locate.

    Returns:
        int: The index of `target`, or -1 if it is not in `nums`.
    """
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if nums[mid] == target:
            return mid

        # Decide which half is sorted, then whether target lies inside it.
        if nums[lo] <= nums[mid]:
            # LEFT half [lo, mid] is sorted (no cliff in it).
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1        # target is within the sorted left half
            else:
                lo = mid + 1        # target must be in the right half
        else:
            # RIGHT half [mid, hi] is sorted.
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1        # target is within the sorted right half
            else:
                hi = mid - 1        # target must be in the left half

    return -1


if __name__ == "__main__":
    # Quick sanity checks.
    print(search([4, 5, 6, 7, 0, 1, 2], 0))    # -> 4
    print(search([4, 5, 6, 7, 0, 1, 2], 3))    # -> -1  (absent)
    print(search([4, 5, 6, 7, 0, 1, 2], 4))    # -> 0   (pivot element)
    print(search([4, 5, 6, 7, 0, 1, 2], 2))    # -> 6   (last element)
    print(search([1], 0))                       # -> -1
    print(search([1], 1))                       # -> 0
    print(search([5, 1, 3], 5))                 # -> 0   (small rotation)
    print(search([3, 1], 1))                    # -> 1

    # Exhaustive cross-check: rotate a sorted array every possible way and
    # confirm every query matches Python's own index lookup.
    base = list(range(0, 20, 2))    # even numbers 0..18, distinct & sorted
    ok = True
    for k in range(len(base)):
        rotated = base[k:] + base[:k]
        for t in range(-2, 22):
            expected = rotated.index(t) if t in rotated else -1
            if search(rotated, t) != expected:
                ok = False
    print(ok)                                    # -> True
