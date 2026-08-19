"""
Coin Change
===========

PROBLEM PROMPT
--------------
You are given an integer array `coins` representing coins of different
denominations and an integer `amount` representing a total amount of money.

Return the FEWEST number of coins that you need to make up that amount. If that
amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an INFINITE number of each kind of coin.

Example 1:
    Input:  coins = [1, 2, 5], amount = 11   -> Output: 3
    Explanation: 11 = 5 + 5 + 1.
Example 2:
    Input:  coins = [2], amount = 3           -> Output: -1
Example 3:
    Input:  coins = [1], amount = 0           -> Output: 0

Constraints:
    1 <= len(coins) <= 12
    1 <= coins[i] <= 2^31 - 1
    0 <= amount <= 10^4
"""


def coin_change(coins, amount):
    """
    Return the fewest coins summing to `amount`, or -1 if impossible.

    APPROACH (Bottom-up DP over amounts -- "unbounded knapsack")
    -----------------------------------------------------------
    Same "reason about the last decision" method as Climbing Stairs / House
    Robber, but the recurrence now has an INNER LOOP over choices, and we're
    OPTIMIZING (fewest coins -> min) rather than counting.

    Define dp[a] = the minimum number of coins needed to make amount `a`. The
    last decision to reach `a` is "which coin did I place last?" If that final
    coin is `c` (with c <= a), then before placing it we had made amount a - c
    optimally, so this plan uses dp[a - c] + 1 coins. We don't know which last
    coin is best, so we try EVERY coin and take the minimum:

        dp[a] = min(dp[a - c] + 1  for each coin c with c <= a)

    That inner "for each coin" loop is the new ingredient versus the fixed
    look-back of Climbing Stairs (which only ever needed dp[i-1], dp[i-2]).
    Because each coin may be reused unlimited times, dp[a - c] is a value we've
    ALREADY computed for a smaller amount -- this is the "unbounded knapsack"
    shape, and building dp[] from 0 upward means every subproblem is ready when
    we need it.

    BASE CASE: dp[0] = 0 -- making amount 0 needs zero coins. This anchors the
    recurrence (a coin c that exactly equals a lands on dp[0] + 1 = 1).

    THE "IMPOSSIBLE" SENTINEL: initialize every dp[a] for a >= 1 to a value that
    means "unreachable" -- we use amount + 1, which is larger than any real
    answer (you can never need more than `amount` coins, since the smallest coin
    is >= 1). If after filling the table dp[amount] is still that sentinel, no
    combination works -> return -1. Using a sentinel (rather than float('inf'))
    keeps the arithmetic in ints and the `+ 1` harmless.

    We compute dp[a] for a = 1..amount; for each we scan the coins and relax.

    COMPLEXITY
    ----------
    Let A = amount and n = len(coins).
    Time  : O(A * n) -- A subproblems, each trying all n coins.
    Space : O(A) -- the dp array.

    Args:
        coins (list[int]): Available denominations (each usable unlimited times).
        amount (int): Target amount to make.

    Returns:
        int: Fewest coins to make `amount`, or -1 if it cannot be made.
    """
    # dp[a] = fewest coins to make amount a. Sentinel amount+1 means "unreachable".
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0   # base case: zero coins make amount 0

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                # Try making `a` by placing coin c last, atop the best for a - c.
                dp[a] = min(dp[a], dp[a - c] + 1)

    # Still the sentinel -> no combination reaches `amount`.
    return dp[amount] if dp[amount] != amount + 1 else -1


def coin_change_memo(coins, amount):
    """
    Same answer via top-down memoized recursion -- the recurrence stated directly.

    APPROACH (Top-down with a cache)
    --------------------------------
    fewest(a) = 0 if a == 0; if a < 0 the path is invalid (return infinity so it
    loses the min); otherwise min over coins of fewest(a - c) + 1. Memoize
    fewest(a) so each amount is solved once, turning the exponential recursion
    tree into O(A * n). Mirrors the bottom-up table from the top-down angle.

    COMPLEXITY
    ----------
    Time  : O(A * n).   Space : O(A) cache + O(A) recursion depth.

    Args:
        coins (list[int]): Available denominations.
        amount (int): Target amount.

    Returns:
        int: Fewest coins, or -1 if impossible.
    """
    INF = float("inf")
    memo = {}

    def fewest(a):
        if a == 0:
            return 0
        if a < 0:
            return INF          # overshoot: this branch can't be used
        if a in memo:
            return memo[a]
        best = min((fewest(a - c) + 1 for c in coins), default=INF)
        memo[a] = best
        return best

    result = fewest(amount)
    return result if result != INF else -1


if __name__ == "__main__":
    # Quick sanity checks.
    print(coin_change([1, 2, 5], 11))    # -> 3   (5 + 5 + 1)
    print(coin_change([2], 3))            # -> -1  (odd amount, only 2s)
    print(coin_change([1], 0))            # -> 0   (amount 0)
    print(coin_change([1, 2, 5], 100))   # -> 20  (twenty 5s)
    print(coin_change([2, 5, 10, 1], 27))  # -> 4  (10 + 10 + 5 + 2)
    print(coin_change([186, 419, 83, 408], 6249))  # -> 20  (greedy would fail here)
    print(coin_change([3, 7], 5))         # -> -1  (no combination)

    # The memoized variant returns the same answers.
    cases = [([1, 2, 5], 11), ([2], 3), ([1], 0), ([1, 2, 5], 100),
             ([2, 5, 10, 1], 27), ([186, 419, 83, 408], 6249), ([3, 7], 5)]
    print(all(coin_change(c, a) == coin_change_memo(c, a) for c, a in cases))   # -> True

    # Cross-check against a BFS "fewest steps" shortest-path view on small inputs.
    from collections import deque
    def bfs(coins, amount):
        if amount == 0:
            return 0
        seen = {0}
        q = deque([(0, 0)])
        while q:
            total, steps = q.popleft()
            for c in coins:
                nxt = total + c
                if nxt == amount:
                    return steps + 1
                if nxt < amount and nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, steps + 1))
        return -1

    import random
    rng = random.Random(0)
    ok = all(
        coin_change(cs := rng.sample(range(1, 12), rng.randint(1, 4)),
                    amt := rng.randint(0, 60)) == bfs(cs, amt)
        for _ in range(500)
    )
    print(ok)                                                                    # -> True
