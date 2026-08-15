"""
House Robber II
===============

PROBLEM PROMPT
--------------
You are a professional robber planning to rob houses along a street. Each house
has a certain amount of money stashed. All houses at this place are arranged in
a CIRCLE. That means the first house is the neighbor of the last one.

Meanwhile, adjacent houses have a security system connected, and it will
automatically contact the police if two adjacent houses were broken into on the
same night (the circular adjacency included).

Given an integer array `nums` representing the amount of money of each house,
return the MAXIMUM amount of money you can rob tonight WITHOUT alerting the
police.

Example 1:
    Input:  nums = [2, 3, 2]      -> Output: 3
    Explanation: You cannot rob house 0 (money = 2) and house 2 (money = 2),
                 because they are adjacent (the circle). So rob house 1 for 3.
Example 2:
    Input:  nums = [1, 2, 3, 1]   -> Output: 4
    Explanation: Rob house 0 (money = 1) and house 2 (money = 3). 1 + 3 = 4.
Example 3:
    Input:  nums = [1, 2, 3]      -> Output: 3

Constraints:
    1 <= len(nums) <= 100
    0 <= nums[i] <= 1000
"""


def rob(nums):
    """
    Return the max robbable from houses arranged in a CIRCLE (no two adjacent).

    APPROACH (Reduce to the linear House Robber, run it twice)
    ----------------------------------------------------------
    House Robber I solved a STRAIGHT street with the recurrence
    dp[i] = max(dp[i-1], nums[i] + dp[i-2]). The only new wrinkle here is the
    circle: house 0 and house n-1 are now neighbors, so they can't BOTH be
    robbed. The clean way to handle that is not to invent a new recurrence, but
    to REDUCE this problem to the one we already solved.

    THE KEY INSIGHT: in any valid robbery on the circle, at least ONE of the two
    "wrap-around" houses (the first or the last) must be left un-robbed -- you
    can never take both. So every optimal plan falls into one of two cases:

        Case A: house 0 is NOT robbed -> the eligible houses are nums[1 .. n-1],
                which is now a plain STRAIGHT street (no wrap, since house 0 is
                out). Solve it with linear House Robber.
        Case B: house n-1 is NOT robbed -> the eligible houses are nums[0 .. n-2],
                again a straight street. Solve it with linear House Robber.

    The true answer is the better of the two:

        answer = max( rob_linear(nums[1:]), rob_linear(nums[:-1]) )

    Neither slice contains both endpoints, so the circular adjacency is
    automatically respected -- we never even mention house 0 and house n-1 in the
    same subproblem. (An optimal plan that robs neither endpoint is covered by
    BOTH cases, which is harmless; we're taking a max.)

    EDGE CASE: a single house has no "other" neighbor to wrap to. Slicing would
    give one empty range and one single-element range; simplest is to special-
    case len(nums) == 1 and just return nums[0]. (For n == 2 the slices are
    [nums[1]] and [nums[0]], and max picks the richer house -- correct, since the
    two are adjacent on the circle.)

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(n) -- two linear passes, each O(n).
    Space : O(1) -- the linear helper uses two rolling variables; the slices add
            O(n) only if you materialize them (you can pass index ranges instead
            to keep it strictly O(1), shown as a comment in the helper).

    Args:
        nums (list[int]): Money stashed at each house, arranged in a circle.

    Returns:
        int: The maximum robbable amount.
    """
    # One house: no wrap-around neighbor exists, just rob it.
    if len(nums) == 1:
        return nums[0]

    # Case A excludes house 0; Case B excludes house n-1. Take the better.
    return max(_rob_linear(nums, 1, len(nums) - 1),
               _rob_linear(nums, 0, len(nums) - 2))


def _rob_linear(nums, lo, hi):
    """
    Linear House Robber over the INCLUSIVE index range nums[lo..hi].

    This is exactly the straight-street solution (dp[i] = max(dp[i-1],
    nums[i] + dp[i-2])) with O(1) rolling variables, but restricted to a
    sub-range via indices instead of slicing -- so it allocates nothing and
    keeps the whole solution O(1) space.

    `prev` = best-through-(i-2), `best` = best-through-(i-1); both start at 0 so
    the first one or two houses fall out of the same recurrence with no special
    cases. Returns 0 for an empty range (lo > hi).

    Args:
        nums (list[int]): The full house array.
        lo (int): First eligible index (inclusive).
        hi (int): Last eligible index (inclusive).

    Returns:
        int: Max robbable within nums[lo..hi], treated as a straight street.
    """
    prev, best = 0, 0
    for i in range(lo, hi + 1):
        take = prev + nums[i]                 # rob house i
        prev, best = best, max(best, take)    # skip vs rob, then slide forward
    return best


if __name__ == "__main__":
    # Quick sanity checks.
    print(rob([2, 3, 2]))         # -> 3   (can't take both 2s; they wrap)
    print(rob([1, 2, 3, 1]))      # -> 4   (houses 0 + 2)
    print(rob([1, 2, 3]))         # -> 3
    print(rob([5]))                # -> 5   (single house)
    print(rob([1, 2]))            # -> 2   (two adjacent; take the richer)
    print(rob([200, 3, 140, 20, 10]))  # -> 340 (houses 0 + 2)
    print(rob([0, 0, 0]))         # -> 0

    # Cross-check against a brute force over every valid CIRCULAR subset.
    from itertools import combinations
    def brute(nums):
        n = len(nums)
        if n == 1:
            return nums[0]
        best = 0
        for r in range(n + 1):
            for combo in combinations(range(n), r):
                ok = all(combo[j + 1] - combo[j] >= 2 for j in range(len(combo) - 1))
                # Circular adjacency: first and last index can't both be chosen.
                if combo and combo[0] == 0 and combo[-1] == n - 1:
                    ok = False
                if ok:
                    best = max(best, sum(nums[i] for i in combo))
        return best

    import random
    rng = random.Random(0)
    passed = all(
        rob(sample := [rng.randint(0, 20) for _ in range(rng.randint(1, 10))]) == brute(sample)
        for _ in range(1000)
    )
    print(passed)                                        # -> True
