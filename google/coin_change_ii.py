"""
Coin Change II
==============

PROBLEM PROMPT
--------------
You are given an integer array `coins` representing coins of different
denominations and an integer `amount` representing a total amount of money.

Return the NUMBER OF COMBINATIONS that make up that amount. If that amount of
money cannot be made up by any combination of the coins, return 0.

You may assume that you have an INFINITE number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.

Example 1:
    Input:  amount = 5, coins = [1, 2, 5]   -> Output: 4
    Explanation: there are four ways to make up the amount:
        5 = 5
        5 = 2 + 2 + 1
        5 = 2 + 1 + 1 + 1
        5 = 1 + 1 + 1 + 1 + 1
Example 2:
    Input:  amount = 3, coins = [2]          -> Output: 0
    Explanation: the amount of 3 cannot be made up just with coins of 2.
Example 3:
    Input:  amount = 10, coins = [10]        -> Output: 1

Constraints:
    1 <= len(coins) <= 300
    1 <= coins[i] <= 5000
    All the values of coins are unique.
    0 <= amount <= 5000
"""


def change(amount, coins):
    """
    Return the number of distinct coin COMBINATIONS that sum to `amount`.

    APPROACH (Counting DP -- and why the LOOP ORDER matters)
    --------------------------------------------------------
    This is the counting cousin of Coin Change (problem 322). There we OPTIMIZED
    (fewest coins -> min); here we COUNT combinations, so the recurrence combines
    subproblems with ADDITION instead of min -- the same "counting uses +,
    optimizing uses min/max" rule.

    Define dp[a] = number of ways to make amount `a`. Base case dp[0] = 1: there
    is exactly ONE way to make amount 0 -- use no coins (the empty combination).
    Every other dp[a] starts at 0.

    THE KEY DECISION -- combinations, not permutations. We must count {1,2} and
    {2,1} as the SAME way (order of coins doesn't matter). The clean way to
    enforce that is to introduce the coin denominations ONE AT A TIME as an OUTER
    loop, and for each coin sweep amounts as the INNER loop:

        for coin in coins:                 # OUTER: decide coins in a fixed order
            for a in range(coin, amount+1): # INNER: amounts, ascending
                dp[a] += dp[a - coin]

    Reading it: after the outer iteration for `coin` finishes, dp[a] counts every
    combination of the coins CONSIDERED SO FAR that sums to a. Adding dp[a - coin]
    says "extend a combination for (a - coin) by one more `coin`." Because `coin`
    is fixed by the outer loop while we sweep amounts, each combination is built
    in a single, non-decreasing coin order -- so {1 then 2} is generated but
    {2 then 1} is never counted separately. That's what makes it COMBINATIONS.

    WHY NOT THE OTHER LOOP ORDER: if you swap them --

        for a in range(1, amount+1):
            for coin in coins:
                dp[a] += dp[a - coin]

    -- you'd count PERMUTATIONS instead (this is the recurrence for Combination
    Sum IV / "number of ordered sequences"), giving a larger, WRONG answer here.
    For amount 3, coins [1,2] that version counts 1+2 and 2+1 as two ways. The
    coin-outer order is the whole trick of this problem; getting it backwards is
    the classic bug.

    The inner loop runs `a` from `coin` upward (ascending). Ascending -- reusing
    the SAME dp array as we go -- is exactly what allows a coin to be used
    UNLIMITED times (dp[a - coin] on the current row already includes uses of
    `coin`). This is the standard unbounded-knapsack sweep direction.

    COMPLEXITY
    ----------
    Let A = amount and n = len(coins).
    Time  : O(A * n) -- n coins, each sweeping up to A amounts.
    Space : O(A) -- a single dp array reused across coins.

    Args:
        amount (int): Target amount to make.
        coins (list[int]): Available denominations (each usable unlimited times).

    Returns:
        int: The number of distinct combinations summing to `amount`.
    """
    # dp[a] = number of ways to make amount a. One way to make 0: use nothing.
    dp = [0] * (amount + 1)
    dp[0] = 1

    # OUTER over coins -> counts combinations (each built in a fixed coin order).
    for coin in coins:
        # INNER ascending over amounts -> allows unlimited reuse of `coin`.
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]

    return dp[amount]


if __name__ == "__main__":
    # Quick sanity checks.
    print(change(5, [1, 2, 5]))     # -> 4
    print(change(3, [2]))            # -> 0   (impossible)
    print(change(10, [10]))          # -> 1
    print(change(0, [1, 2, 5]))     # -> 1   (empty combination makes 0)
    print(change(3, [1, 2]))        # -> 2   ({1,1,1}, {1,2}) -- NOT 3 (no perms)
    print(change(500, [1, 2, 5]))   # -> 12701

    # Cross-check against a brute-force combination count (non-decreasing coins).
    def brute(amount, coins):
        coins = sorted(coins)
        def count(remaining, i):
            if remaining == 0:
                return 1
            if remaining < 0 or i == len(coins):
                return 0
            # Either use coin i again (stay at i) or skip to the next coin.
            return count(remaining - coins[i], i) + count(remaining, i + 1)
        return count(amount, 0)

    import random
    rng = random.Random(0)
    ok = all(
        change(amt := rng.randint(0, 40),
                cs := rng.sample(range(1, 10), rng.randint(1, 4))) == brute(amt, cs)
        for _ in range(500)
    )
    print(ok)                                                                    # -> True
