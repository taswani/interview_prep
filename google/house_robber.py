"""
House Robber
============

PROBLEM PROMPT
--------------
You are a professional robber planning to rob houses along a street. Each house
has a certain amount of money stashed. The only constraint stopping you from
robbing each of them is that ADJACENT houses have security systems connected,
and it will automatically contact the police if two adjacent houses were broken
into on the same night.

Given an integer array `nums` representing the amount of money of each house,
return the MAXIMUM amount of money you can rob tonight WITHOUT alerting the
police (i.e., without robbing two adjacent houses).

Example 1:
    Input:  nums = [1, 2, 3, 1]      -> Output: 4
    Explanation: Rob house 0 (money = 1) and house 2 (money = 3). 1 + 3 = 4.
Example 2:
    Input:  nums = [2, 7, 9, 3, 1]   -> Output: 12
    Explanation: Rob house 0 (2), house 2 (9), and house 4 (1). 2 + 9 + 1 = 12.

Constraints:
    1 <= len(nums) <= 100
    0 <= nums[i] <= 400
"""


def rob(nums):
    """
    Return the maximum money robbable from `nums` with no two adjacent houses.

    APPROACH (Dynamic programming, space-optimized)
    -----------------------------------------------
    Same "reason about the last decision" method as Climbing Stairs, but now the
    recurrence encodes a CHOICE WITH A TRADEOFF rather than a plain sum -- so it
    becomes a max() of two options instead of an addition.

    Define dp[i] = the most money robbable considering only houses 0..i. Standing
    at house i, you have exactly two mutually exclusive plans:

      - SKIP house i: you take whatever was optimal through house i-1. That's
        dp[i-1]. (Robbing i-1 is now allowed, since you're not touching i.)
      - ROB house i: you collect nums[i], but the adjacency rule forbids house
        i-1, so the best you can add is the optimum through house i-2. That's
        nums[i] + dp[i-2].

    You want the better of the two, so:

        dp[i] = max(dp[i-1], nums[i] + dp[i-2])

    The max() is the whole difference from Climbing Stairs: there we ADDED the
    two predecessors (counting paths); here we CHOOSE the more profitable of two
    plans (optimizing a value). Note it is NOT simply "every other house" -- e.g.
    [2,1,1,2] should rob houses 0 and 3 for 4, skipping two in a row, which the
    max() handles automatically.

    BASE CASES:
        dp[0] = nums[0]                 (one house: rob it)
        dp[1] = max(nums[0], nums[1])   (two houses: take the richer one)

    SPACE OPTIMIZATION: dp[i] depends only on the previous two values, so we keep
    two rolling variables instead of the whole array (exactly like Climbing
    Stairs):
        prev2 = dp[i-2],  prev1 = dp[i-1].
    Each step computes cur = max(prev1, nums[i] + prev2), then slides forward.

    COMPLEXITY
    ----------
    Let n = len(nums).
    Time  : O(n) -- one pass, O(1) work per house.
    Space : O(1) -- two rolling variables.

    Args:
        nums (list[int]): Money stashed at each house.

    Returns:
        int: The maximum robbable amount.
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    # prev2 = best through house i-2, prev1 = best through house i-1.
    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        # Choose: skip house i (prev1) OR rob it (nums[i] + prev2).
        cur = max(prev1, nums[i] + prev2)
        prev2, prev1 = prev1, cur

    return prev1


def rob_clean(nums):
    """
    Same result with a tighter loop that needs no special-casing of length.

    APPROACH
    --------
    Identical recurrence dp[i] = max(dp[i-1], nums[i] + dp[i-2]), but we start
    both rolling variables at 0 and let the loop handle every house uniformly.
    Reading rob = dp[i-1] and prev = dp[i-2]:

        take = prev + num        # rob this house (+ best up to two houses back)
        prev, rob = rob, max(rob, take)

    Here `prev` starts as "best two houses back" = 0 and `rob` as "best one house
    back" = 0, so houses 0 and 1 fall out of the same recurrence with no separate
    base cases. This is the compact form worth writing in an interview.

    COMPLEXITY
    ----------
    Time  : O(n).   Space : O(1).

    Args:
        nums (list[int]): Money stashed at each house.

    Returns:
        int: The maximum robbable amount.
    """
    prev, best = 0, 0     # best-through-(i-2), best-through-(i-1)
    for num in nums:
        take = prev + num                 # rob current house
        prev, best = best, max(best, take)  # skip vs rob, then slide
    return best


if __name__ == "__main__":
    # Quick sanity checks.
    print(rob([1, 2, 3, 1]))         # -> 4   (houses 0 + 2)
    print(rob([2, 7, 9, 3, 1]))      # -> 12  (houses 0 + 2 + 4)
    print(rob([5]))                   # -> 5   (single house)
    print(rob([2, 1, 1, 2]))         # -> 4   (houses 0 + 3: skips TWO in a row)
    print(rob([2, 100, 9, 3, 100])) # -> 200 (houses 1 + 4)
    print(rob([0, 0, 0]))            # -> 0

    # The clean variant returns the same answers.
    tests = [[1, 2, 3, 1], [2, 7, 9, 3, 1], [5], [2, 1, 1, 2], [2, 100, 9, 3, 100], [0, 0, 0]]
    print(all(rob(t) == rob_clean(t) for t in tests))   # -> True

    # Cross-check against a brute force that tries every non-adjacent subset.
    from itertools import combinations
    def brute(nums):
        n = len(nums)
        best = 0
        for r in range(n + 1):
            for combo in combinations(range(n), r):
                if all(combo[j + 1] - combo[j] >= 2 for j in range(len(combo) - 1)):
                    best = max(best, sum(nums[i] for i in combo))
        return best

    import random
    rng = random.Random(0)
    ok = all(
        rob(sample := [rng.randint(0, 20) for _ in range(rng.randint(1, 10))]) == brute(sample)
        for _ in range(1000)
    )
    print(ok)                                            # -> True
