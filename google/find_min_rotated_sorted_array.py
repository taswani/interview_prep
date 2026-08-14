"""
Find Minimum in Rotated Sorted Array
====================================

PROBLEM PROMPT
--------------
Suppose an array of length n sorted in ascending order is ROTATED between 1 and
n times. For example, the array [0,1,2,4,5,6,7] might become:

    [4,5,6,7,0,1,2]  if it was rotated 4 times.
    [0,1,2,4,5,6,7]  if it was rotated 7 times (back to the original).

Notice that rotating an array [a[0], a[1], ..., a[n-1]] once results in the
array [a[n-1], a[0], a[1], ..., a[n-2]].

Given the sorted rotated array `nums` of UNIQUE elements, return the MINIMUM
element of this array.

You must write an algorithm that runs in O(log n) time.

Example 1:
    Input:  nums = [3, 4, 5, 1, 2]       -> Output: 1
Example 2:
    Input:  nums = [4, 5, 6, 7, 0, 1, 2] -> Output: 0
Example 3:
    Input:  nums = [11, 13, 15, 17]      -> Output: 11  (not rotated / full rotation)

Constraints:
    n == len(nums)
    1 <= n <= 5000
    -5000 <= nums[i] <= 5000
    All the integers of nums are unique.
    nums is sorted and rotated between 1 and n times.
"""


def find_min(nums):
    """
    Return the minimum element of a rotated sorted array in O(log n).

    APPROACH (Binary search for the pivot, comparing mid to the RIGHT end)
    ---------------------------------------------------------------------
    Rotation puts exactly one "cliff" in the array -- the single spot where a
    larger value is immediately followed by a smaller one. The minimum element is
    right AT the bottom of that cliff (the first element of the second sorted
    run). So finding the minimum is really finding the pivot.

    We converge on it with binary search, but the comparison is the crux, and it
    is different from "Search in Rotated Sorted Array" (problem 33). Here we
    compare nums[mid] against nums[hi] -- the RIGHT endpoint -- not nums[lo].

    WHY COMPARE TO nums[hi] AND NOT nums[lo]:
      Comparing to the LEFT end is ambiguous. In a not-rotated array like
      [1,2,3,4,5], nums[mid] > nums[lo] holds, and in a rotated one like
      [3,4,5,1,2] nums[mid] (=5) > nums[lo] (=3) ALSO holds -- the same
      comparison points us in opposite directions, so it can't decide the half.
      The RIGHT end has no such ambiguity:

        - If nums[mid] > nums[hi]: the right portion is "out of order" relative
          to mid, which means the cliff (and thus the minimum) is STRICTLY to the
          RIGHT of mid. mid itself can't be the min, so lo = mid + 1.

        - If nums[mid] < nums[hi]: the segment from mid to hi is properly sorted,
          so the minimum is at mid or to its LEFT. mid could BE the minimum, so
          we keep it: hi = mid  (never hi = mid - 1, which could discard the
          answer).

      (No equal case to handle: the elements are unique, and mid < hi throughout
      the loop, so nums[mid] == nums[hi] never occurs.)

    LOOP FORM: `while lo < hi` with hi = mid -- the half-open "converge on a
    boundary" style (same as Koko / binary-search-on-the-answer), NOT the
    lo <= hi / return-on-equal style. We aren't looking for a specific value to
    match; we're squeezing [lo, hi] down until it pins the single pivot index.
    When lo == hi the interval is one element -- that's the minimum -> return
    nums[lo].

    The array might not be rotated at all (or rotated a full n times, which looks
    the same). Then it is already sorted, nums[mid] < nums[hi] always holds, hi
    marches left to 0, and we correctly return nums[0], the first element.

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(log n) -- interval halves each iteration.
    Space : O(1) -- two pointers, iterative.

    Args:
        nums (list[int]): A rotated ascending array of unique integers.

    Returns:
        int: The minimum element.
    """
    lo, hi = 0, len(nums) - 1

    # Converge [lo, hi] onto the pivot (the minimum's index).
    while lo < hi:
        mid = lo + (hi - lo) // 2

        if nums[mid] > nums[hi]:
            # Cliff is to the right; mid can't be the minimum.
            lo = mid + 1
        else:
            # nums[mid] < nums[hi]: mid..hi is sorted; min is at mid or left.
            hi = mid

    # lo == hi points at the minimum.
    return nums[lo]


if __name__ == "__main__":
    # Quick sanity checks.
    print(find_min([3, 4, 5, 1, 2]))            # -> 1
    print(find_min([4, 5, 6, 7, 0, 1, 2]))      # -> 0
    print(find_min([11, 13, 15, 17]))           # -> 11  (not rotated)
    print(find_min([2, 1]))                      # -> 1   (smallest rotation)
    print(find_min([1]))                         # -> 1   (single element)
    print(find_min([5, 1, 2, 3, 4]))            # -> 1   (min just past the front)
    print(find_min([2, 3, 4, 5, 1]))            # -> 1   (min at the very end)

    # Exhaustive cross-check: rotate a sorted array every possible way and
    # confirm we always recover the true minimum.
    base = list(range(-3, 12))   # distinct, sorted
    ok = all(
        find_min(base[k:] + base[:k]) == min(base)
        for k in range(len(base))
    )
    print(ok)                                    # -> True
