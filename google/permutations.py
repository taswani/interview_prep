"""
Permutations
============

PROBLEM PROMPT
--------------
Given an array `nums` of DISTINCT integers, return all the possible
permutations. You can return the answer in any order.

Example 1:
    Input:  nums = [1, 2, 3]
    Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]

Example 2:
    Input:  nums = [0, 1]
    Output: [[0,1], [1,0]]

Example 3:
    Input:  nums = [1]
    Output: [[1]]

Constraints:
    1 <= len(nums) <= 6
    -10 <= nums[i] <= 10
    All the integers of nums are unique.

Note: an array of n distinct elements has exactly n! permutations, because there
are n choices for the first slot, n-1 for the second, and so on.
"""


def permute(nums):
    """
    Return all permutations of `nums` using backtracking.

    APPROACH (Backtracking: choose -> recurse -> un-choose)
    -------------------------------------------------------
    Same skeleton as `subsets`, with one crucial difference: order MATTERS here,
    so [1,2,3] and [2,1,3] are BOTH valid answers. That changes how we loop.

    In subsets we carried a `start` index and only ever looked forward, which
    deliberately forbade reorderings ({1,2} but never {2,1}). For permutations
    we WANT every ordering, so we drop `start` entirely and instead let each
    slot consider EVERY element of nums -- we just need to skip the ones already
    placed in the current arrangement. A `used` boolean array tracks that:
    used[i] is True while nums[i] sits somewhere in the current `path`.

    We build `path` one position at a time. At each call:
      - if path has length n, it's a full arrangement -> record a copy, or
      - otherwise, scan all indices i; for each UNUSED nums[i]:
            1. choose    -> mark used[i], append nums[i] to path,
            2. recurse   -> fill the remaining slots,
            3. un-choose -> pop nums[i], clear used[i] so the next sibling
                            branch can use that element in this slot instead.

    Because every slot re-scans the whole array (minus what's already placed),
    element 3 can appear first in one branch and last in another -- which is
    exactly how we obtain all n! orderings. The `used` guard is the ONLY thing
    stopping an element from being reused within a single permutation.

    Why we append a COPY (path[:]): `path` is a single list mutated in place; we
    snapshot it at full length, otherwise every stored result would alias the
    same list and end up empty as the pops unwind.

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(n * n!) -- there are n! permutations, and copying each full-length
            arrangement into the result costs O(n).
    Space : O(n) auxiliary for the recursion stack, `path`, and `used` (not
            counting the O(n * n!) output itself).

    Args:
        nums (list[int]): Array of distinct integers.

    Returns:
        list[list[int]]: Every permutation of `nums`.
    """
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        # A permutation is complete once every slot is filled.
        if len(path) == len(nums):
            result.append(path[:])
            return

        # Try every element that isn't already placed in the current path.
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True            # choose nums[i] for this slot
            path.append(nums[i])
            backtrack()               # fill the remaining slots
            path.pop()                # un-choose...
            used[i] = False           # ...and free nums[i] for the next branch

    backtrack()
    return result


def permute_swap(nums):
    """
    Return all permutations of `nums` by swapping elements into place.

    APPROACH (In-place swapping)
    ----------------------------
    Instead of a separate `used` array and `path`, we permute `nums` itself. The
    index `first` marks the boundary: everything before `first` is already fixed
    for this arrangement, and everything from `first` onward is still up for
    grabs.

    At each level we try each candidate for position `first` by swapping it into
    place, recursing on `first + 1`, then swapping back to restore the array for
    the next candidate:

        for i in range(first, n):
            swap(first, i)      # put nums[i] into the `first` slot
            recurse(first + 1)  # permute the rest
            swap(first, i)      # undo, so the next i sees the original order

    When `first == n` every position is fixed, so the current state of `nums` is
    one complete permutation -- record a copy. This avoids the auxiliary `used`
    array, trading it for mutating (and restoring) the input.

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(n * n!) -- same n! arrangements, O(n) to copy each out.
    Space : O(n) auxiliary for the recursion stack (permutes in place; no `used`
            array), excluding the output.

    Args:
        nums (list[int]): Array of distinct integers.

    Returns:
        list[list[int]]: Every permutation of `nums`.
    """
    result = []
    n = len(nums)

    def backtrack(first):
        # All positions fixed -> `nums` currently holds a full permutation.
        if first == n:
            result.append(nums[:])
            return

        for i in range(first, n):
            nums[first], nums[i] = nums[i], nums[first]   # swap candidate in
            backtrack(first + 1)                          # permute the suffix
            nums[first], nums[i] = nums[i], nums[first]   # swap back (restore)

    backtrack(0)
    return result


if __name__ == "__main__":
    # Quick sanity checks. Order does not matter, so sort for stable comparison.
    def normalize(perms):
        return sorted(perms)

    print(normalize(permute([1, 2, 3])))
    # -> [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
    print(normalize(permute([0, 1])))              # -> [[0, 1], [1, 0]]
    print(permute([1]))                            # -> [[1]]
    print(len(permute([1, 2, 3, 4])))              # -> 24  (4!)

    # The swap-based variant returns the same set of permutations.
    print(normalize(permute_swap([1, 2, 3])) == normalize(permute([1, 2, 3])))  # -> True
    print(len(permute_swap([1, 2, 3, 4, 5])))      # -> 120  (5!)
