"""
Subsets
=======

PROBLEM PROMPT
--------------
Given an integer array `nums` of UNIQUE elements, return all possible subsets
(the power set).

The solution set must not contain duplicate subsets. Return the solution in any
order.

Example 1:
    Input:  nums = [1, 2, 3]
    Output: [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]

Example 2:
    Input:  nums = [0]
    Output: [[], [0]]

Constraints:
    1 <= len(nums) <= 10
    -10 <= nums[i] <= 10
    All the numbers of nums are unique.

Note: an array of n unique elements has exactly 2^n subsets, because each
element is independently either IN or OUT of a given subset.
"""


def subsets(nums):
    """
    Return the power set of `nums` using backtracking.

    APPROACH (Backtracking: choose -> recurse -> un-choose)
    -------------------------------------------------------
    Every subset is a series of independent yes/no decisions: for each element,
    do we include it or not? We explore that decision tree with the canonical
    backtracking skeleton.

    We walk the array left to right carrying a `path` (the subset built so far)
    and a `start` index (the first element still available to consider). At each
    call, `path` is ALREADY a valid subset, so we record a COPY of it. Then we
    try extending it: for every index i from `start` onward we

        1. choose   -> append nums[i] to path,
        2. recurse  -> explore all subsets that include nums[i], drawing only
                       from elements AFTER i (start = i + 1) so we never reuse
                       an element or produce the same subset in a different
                       order, and
        3. un-choose -> pop nums[i] back off so the next iteration starts clean.

    Advancing `start` to i + 1 is what enforces "combinations, not
    permutations": {1,2} is generated once (via 1 then 2), never again as
    {2,1}.

    Why we append a COPY (path[:]): `path` is a single list mutated in place
    throughout the recursion. Storing the reference would mean every entry in
    the result points at the same list, which ends up empty once all the pops
    unwind. The slice snapshots the subset at this moment.

    The recursion tree visits every subset exactly once; the empty subset is
    recorded by the very first call before any element is chosen.

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(n * 2^n) -- there are 2^n subsets, and copying each into the
            result costs up to O(n).
    Space : O(n) auxiliary for the recursion stack and `path` (not counting the
            O(n * 2^n) needed to hold the output itself).

    Args:
        nums (list[int]): Array of unique integers.

    Returns:
        list[list[int]]: Every subset of `nums`.
    """
    result = []
    path = []

    def backtrack(start):
        # `path` is a complete subset at every entry -> record a snapshot of it.
        result.append(path[:])

        # Try adding each remaining element as the next member of the subset.
        for i in range(start, len(nums)):
            path.append(nums[i])      # choose nums[i]
            backtrack(i + 1)          # recurse on elements strictly after i
            path.pop()                # un-choose, restoring path for the next i

    backtrack(0)
    return result


def subsets_iterative(nums):
    """
    Return the power set of `nums` by iteratively doubling the result set.

    APPROACH (Cascading / iterative construction)
    ---------------------------------------------
    Start with the power set of the empty prefix: [[]]. Then fold in one element
    at a time. The key insight is that adding a new element `x` to a set whose
    power set we already have simply DOUBLES that power set:

      - every existing subset stays (the subsets that exclude x), AND
      - a copy of every existing subset with x appended (the subsets that
        include x).

    Walking through nums = [1, 2, 3]:
        start:      [[]]
        add 1 ->    [[]] + [[1]]              = [[], [1]]
        add 2 ->    [[], [1]] + [[2], [1,2]]  = [[], [1], [2], [1,2]]
        add 3 ->    ... + [[3],[1,3],[2,3],[1,2,3]]

    This produces the same 2^n subsets as the backtracking version, just built
    breadth-first instead of depth-first. No recursion required.

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(n * 2^n) -- the result doubles n times, and each doubling copies
            every current subset (each up to length n).
    Space : O(n * 2^n) for the output (no extra recursion stack).

    Args:
        nums (list[int]): Array of unique integers.

    Returns:
        list[list[int]]: Every subset of `nums`.
    """
    result = [[]]
    for num in nums:
        # For each subset we already have, spawn a copy that also includes `num`.
        result += [subset + [num] for subset in result]
    return result


if __name__ == "__main__":
    # Quick sanity checks. Order does not matter, so sort for stable comparison.
    def normalize(subsets_list):
        return sorted(sorted(subset) for subset in subsets_list)

    print(normalize(subsets([1, 2, 3])))
    # -> [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    print(normalize(subsets([0])))                 # -> [[], [0]]
    print(len(subsets([1, 2, 3, 4, 5])))           # -> 32  (2^5)

    # The iterative variant returns the same power set.
    print(normalize(subsets_iterative([1, 2, 3])) == normalize(subsets([1, 2, 3])))  # -> True
    print(len(subsets_iterative([1, 2, 3, 4])))    # -> 16  (2^4)
