"""
Combination Sum
===============

PROBLEM PROMPT
--------------
Given an array of DISTINCT integers `candidates` and a target integer `target`,
return a list of all UNIQUE combinations of `candidates` where the chosen
numbers sum to `target`. You may return the combinations in any order.

The SAME number may be chosen from `candidates` an UNLIMITED number of times.
Two combinations are unique if the frequency of at least one of the chosen
numbers is different.

The test cases are generated such that the number of unique combinations that
sum up to `target` is fewer than 150 for the given input.

Example 1:
    Input:  candidates = [2, 3, 6, 7], target = 7
    Output: [[2, 2, 3], [7]]
    Explanation:
        2 + 2 + 3 = 7, and 7 = 7. These are the only two combinations.

Example 2:
    Input:  candidates = [2, 3, 5], target = 8
    Output: [[2, 2, 2, 2], [2, 3, 3], [3, 5]]

Example 3:
    Input:  candidates = [2], target = 1
    Output: []

Constraints:
    1 <= len(candidates) <= 30
    2 <= candidates[i] <= 40
    All elements of candidates are distinct.
    1 <= target <= 40
"""


def combination_sum(candidates, target):
    """
    Return all combinations of `candidates` that sum to `target` (reuse allowed).

    APPROACH (Backtracking with element reuse)
    ------------------------------------------
    Same choose -> recurse -> un-choose skeleton as `subsets` and
    `permutations`, distinguished by ONE detail in the recursive call -- and
    that detail is the whole lesson of this problem.

        subsets:        recurse with start = i + 1   (each element used <= once)
        combination_sum: recurse with start = i       (each element reusable)

    Passing `i` again (instead of `i + 1`) means the element we just chose stays
    on the table, so it can be picked over and over -- that's how [2, 2, 3] is
    formed from a single 2 in the input. We still never pass an index BELOW the
    current `start`, which keeps combinations in non-decreasing index order and
    prevents duplicates like [2, 3, 2] and [3, 2, 2] from all appearing: only
    the sorted-order [2, 2, 3] is generated.

    Instead of tracking the running sum, we carry `remaining` = how much target
    is still unmet. Each choice of candidates[i] subtracts from it. Two base
    cases end a branch:
      - remaining == 0 -> the current `path` sums exactly to target -> record a
        copy.
      - remaining < 0  -> we overshot; this branch is dead, stop.

    (Because every candidate is >= 2 > 0, `remaining` strictly decreases as the
    path grows, so the recursion is guaranteed to terminate.)

    OPTIONAL PRUNING (see `combination_sum_pruned`): if we sort `candidates`
    first, then the moment candidates[i] > remaining we can STOP the loop
    entirely -- every later candidate is even larger and would also overshoot.

    COMPLEXITY
    ----------
    Let n = len(candidates) and t = target, with `m` the smallest candidate.
    Time  : O(n^(t/m)) in the worst case -- the recursion tree has depth up to
            t/m (using the smallest element repeatedly) and up to n branches per
            node. Copying each valid combination adds an O(t/m) factor.
    Space : O(t/m) auxiliary for the recursion stack and `path` (excluding the
            output list itself).

    Args:
        candidates (list[int]): Distinct positive integers.
        target (int): The sum to reach.

    Returns:
        list[list[int]]: Every unique combination summing to `target`.
    """
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            # `path` sums exactly to target -> snapshot it.
            result.append(path[:])
            return
        if remaining < 0:
            # Overshot the target; abandon this branch.
            return

        # Consider each candidate from `start` onward (never look backward).
        for i in range(start, len(candidates)):
            path.append(candidates[i])            # choose candidates[i]
            # start = i (NOT i + 1) -> candidates[i] may be reused.
            backtrack(i, remaining - candidates[i])
            path.pop()                            # un-choose

    backtrack(0, target)
    return result


def combination_sum_pruned(candidates, target):
    """
    Same result as `combination_sum`, with sort-based early termination.

    APPROACH (Sort, then break instead of continue)
    -----------------------------------------------
    Sorting `candidates` ascending lets us cut the search short. When we reach a
    candidate that already exceeds `remaining`, every candidate AFTER it is even
    larger (the list is sorted), so none of them can fit either -- we `break`
    out of the loop rather than merely skipping this one. This trims whole
    branches the unsorted version would still descend into and immediately
    reject via the `remaining < 0` base case.

    The output is identical to `combination_sum`; only the amount of work
    differs.

    COMPLEXITY
    ----------
    Sorting adds O(n log n) up front. Worst-case asymptotics match
    `combination_sum`, but pruning makes it substantially faster in practice.

    Args:
        candidates (list[int]): Distinct positive integers.
        target (int): The sum to reach.

    Returns:
        list[list[int]]: Every unique combination summing to `target`.
    """
    result = []
    path = []
    candidates = sorted(candidates)

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            # Sorted: if this candidate overshoots, so do all the later ones.
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])   # reuse allowed (start = i)
            path.pop()

    backtrack(0, target)
    return result


if __name__ == "__main__":
    # Quick sanity checks. Order does not matter, so sort for stable comparison.
    def normalize(combos):
        return sorted(sorted(combo) for combo in combos)

    print(normalize(combination_sum([2, 3, 6, 7], 7)))      # -> [[2, 2, 3], [7]]
    print(normalize(combination_sum([2, 3, 5], 8)))         # -> [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    print(combination_sum([2], 1))                          # -> []  (cannot reach 1)
    print(normalize(combination_sum([7, 3, 2], 18)))        # unsorted input still works

    # The pruned variant returns the same combinations.
    print(normalize(combination_sum_pruned([2, 3, 6, 7], 7)) == normalize(combination_sum([2, 3, 6, 7], 7)))  # -> True
    print(normalize(combination_sum_pruned([2, 3, 5], 8)))  # -> [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
