"""
Generate Parentheses
====================

PROBLEM PROMPT
--------------
Given `n` pairs of parentheses, write a function to generate all combinations of
well-formed (balanced) parentheses.

Example 1:
    Input:  n = 3
    Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

Example 2:
    Input:  n = 1
    Output: ["()"]

Constraints:
    1 <= n <= 8

Note: the number of valid combinations is the n-th Catalan number
(1, 2, 5, 14, 42, ... for n = 1, 2, 3, 4, 5), which grows roughly like
4^n / (n * sqrt(n)) -- far fewer than the 2^(2n) raw strings of that length.
"""


def generate_parenthesis(n):
    """
    Return all combinations of `n` pairs of well-formed parentheses.

    APPROACH (Backtracking gated by validity, not by an index)
    ----------------------------------------------------------
    Same choose -> recurse -> un-choose skeleton as `subsets` / `permutations` /
    `combination_sum`, but the "choices" change shape. There is no input array
    and no `start` index to walk. At every step there are only ever TWO possible
    moves:

        1. add an opening bracket '('
        2. add a closing bracket ')'

    The whole problem is deciding WHEN each move is legal. Instead of an index,
    we carry two counters:

        open_count  = number of '(' placed so far
        close_count = number of ')' placed so far

    The two rules that keep the string valid at all times:

      - We may add '(' as long as we haven't used all n opens
        (open_count < n). Opening brackets are always safe to add up to the
        budget.
      - We may add ')' only if it would match an already-open '('
        (close_count < open_count). This is the key rule: a ')' that has no
        unmatched '(' to its left makes the string invalid (e.g. "())"), so we
        forbid it up front rather than build a bad string and reject it later.

    Because we only ever make LEGAL moves, every complete string is guaranteed
    valid -- there is no separate "is this balanced?" check. A string is complete
    when its length reaches 2n (equivalently, when close_count == n), at which
    point every open has been matched and we record it.

    This "prune at the choice, not at the leaf" style is why the recursion tree
    only ever visits Catalan-many valid strings plus their prefixes, instead of
    all 2^(2n) bracket strings.

    We build the string on a `path` list of characters (cheap append/pop) and
    "".join it when complete, rather than concatenating new strings at every
    step.

    COMPLEXITY
    ----------
    Let C(n) be the n-th Catalan number = the count of valid results.
    Time  : O(n * C(n)) -- the tree produces C(n) leaves, and materializing each
            length-2n string costs O(n). C(n) ~ 4^n / (n * sqrt(n)).
    Space : O(n) auxiliary for the recursion stack and `path` (excluding the
            output list itself).

    Args:
        n (int): The number of parenthesis pairs.

    Returns:
        list[str]: Every well-formed combination.
    """
    result = []
    path = []

    def backtrack(open_count, close_count):
        # A complete string uses all n opens and all n closes.
        if len(path) == 2 * n:
            result.append("".join(path))
            return

        # Choice 1: add '(' while we still have opens left in the budget.
        if open_count < n:
            path.append("(")
            backtrack(open_count + 1, close_count)
            path.pop()

        # Choice 2: add ')' only if there is an unmatched '(' to close.
        if close_count < open_count:
            path.append(")")
            backtrack(open_count, close_count + 1)
            path.pop()

    backtrack(0, 0)
    return result


if __name__ == "__main__":
    # Quick sanity checks. Order does not matter, so sort for stable comparison.
    print(sorted(generate_parenthesis(1)))   # -> ['()']
    print(sorted(generate_parenthesis(2)))   # -> ['(())', '()()']
    print(sorted(generate_parenthesis(3)))
    # -> ['((()))', '(()())', '(())()', '()(())', '()()()']

    # The count of results is the n-th Catalan number: 1, 2, 5, 14, 42.
    print([len(generate_parenthesis(n)) for n in range(1, 6)])   # -> [1, 2, 5, 14, 42]

    # Every produced string is balanced (spot-check via a running counter).
    def is_balanced(s):
        depth = 0
        for ch in s:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                return False
        return depth == 0

    print(all(is_balanced(s) for s in generate_parenthesis(4)))  # -> True
