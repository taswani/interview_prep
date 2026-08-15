"""
Climbing Stairs
===============

PROBLEM PROMPT
--------------
You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many DISTINCT ways can you
climb to the top?

Example 1:
    Input:  n = 2   -> Output: 2
    Explanation: 1+1, or 2.
Example 2:
    Input:  n = 3   -> Output: 3
    Explanation: 1+1+1, 1+2, or 2+1.

Constraints:
    1 <= n <= 45
"""


def climb_stairs(n):
    """
    Return the number of distinct ways to climb `n` stairs (1 or 2 at a time).

    APPROACH (Dynamic programming, space-optimized)
    -----------------------------------------------
    This is the canonical "first DP problem." The trick is to spot the
    RECURRENCE -- how the answer for n is built from smaller answers.

    Think about the VERY LAST move you make to arrive at step n. It was either:
      - a 1-step hop from step n-1, or
      - a 2-step hop from step n-2.
    Those two cases are disjoint (a given way ends with exactly one final move)
    and together they cover every possibility. So the number of ways to reach
    step n is the number of ways to reach n-1 PLUS the number of ways to reach
    n-2:

        ways(n) = ways(n-1) + ways(n-2)

    That is exactly the Fibonacci recurrence. The base cases:
        ways(0) = 1   (one way to "climb" zero stairs: do nothing / the empty
                       climb -- this makes the recurrence work cleanly)
        ways(1) = 1   (a single 1-step)

    WHY DP AND NOT PLAIN RECURSION: computing ways(n) by naive recursion re-solves
    ways(n-2) from both ways(n) and ways(n-1), and so on, branching into an
    O(2^n) tree of repeated subproblems. DP fixes this by solving each subproblem
    ONCE. The three standard ways to arrange that computation:
      1. Top-down memoized recursion: cache ways(k) the first time it's computed
         (see `climb_stairs_memo`).
      2. Bottom-up table: fill an array dp[0..n] left to right.
      3. Bottom-up with O(1) space: notice dp[i] only ever needs the previous TWO
         values, so we don't keep the whole array -- just two rolling variables.
    This function uses option 3.

    ROLLING VARIABLES: let `prev2 = ways(i-2)` and `prev1 = ways(i-1)`. Each step
    computes the current count `prev1 + prev2`, then slides the window forward.
    After the loop, `prev1` holds ways(n).

    COMPLEXITY
    ----------
    Time  : O(n) -- one pass computing each count once.
    Space : O(1) -- two rolling variables instead of a full dp array.

    Args:
        n (int): The number of stairs.

    Returns:
        int: The count of distinct ways to reach the top.
    """
    # Base cases: 1 way to reach step 0 (empty climb) and step 1.
    if n <= 1:
        return 1

    prev2, prev1 = 1, 1     # ways(0), ways(1)
    for _ in range(2, n + 1):
        # ways(i) = ways(i-1) + ways(i-2); then slide the window forward.
        prev2, prev1 = prev1, prev1 + prev2
    return prev1


def climb_stairs_memo(n):
    """
    Same result via top-down memoized recursion -- the DP recurrence written the
    way most people first discover it.

    APPROACH (Top-down with a cache)
    --------------------------------
    Write the recurrence directly as a recursive function, but remember each
    result the first time it's computed so repeated subproblems cost O(1) on
    later hits. This turns the O(2^n) naive recursion tree into O(n) distinct
    computations. It mirrors option 1 above; kept here to show the same
    recurrence from the top-down angle.

    COMPLEXITY
    ----------
    Time  : O(n) -- each of ways(0..n) is computed exactly once.
    Space : O(n) -- the cache plus the recursion stack (deeper than the O(1)
            iterative form, a reason to prefer the bottom-up version at scale).

    Args:
        n (int): The number of stairs.

    Returns:
        int: The count of distinct ways to reach the top.
    """
    memo = {0: 1, 1: 1}

    def ways(k):
        if k in memo:
            return memo[k]
        memo[k] = ways(k - 1) + ways(k - 2)   # solve once, then cache
        return memo[k]

    return ways(n)


if __name__ == "__main__":
    # Quick sanity checks.
    print(climb_stairs(2))    # -> 2
    print(climb_stairs(3))    # -> 3
    print(climb_stairs(1))    # -> 1
    print(climb_stairs(5))    # -> 8   (Fibonacci: 1,1,2,3,5,8)
    print(climb_stairs(10))   # -> 89
    print(climb_stairs(45))   # -> 1836311903  (the constraint's upper bound)

    # The memoized variant returns the same counts.
    print(all(climb_stairs(n) == climb_stairs_memo(n) for n in range(1, 46)))  # -> True

    # Cross-check against the closed-form Fibonacci relation: ways(n) = F(n+1).
    def fib(m):
        a, b = 0, 1
        for _ in range(m):
            a, b = b, a + b
        return a
    print(all(climb_stairs(n) == fib(n + 1) for n in range(1, 46)))            # -> True
