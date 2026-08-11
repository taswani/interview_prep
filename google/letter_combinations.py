"""
Letter Combinations of a Phone Number
=====================================

PROBLEM PROMPT
--------------
Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given
below. Note that 1 does not map to any letters.

    2 -> "abc"    3 -> "def"    4 -> "ghi"    5 -> "jkl"
    6 -> "mno"    7 -> "pqrs"   8 -> "tuv"    9 -> "wxyz"

Example 1:
    Input:  digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:
    Input:  digits = ""
    Output: []

Example 3:
    Input:  digits = "2"
    Output: ["a","b","c"]

Constraints:
    0 <= len(digits) <= 4
    digits[i] is a digit in the range ['2', '9'].
"""


# Telephone keypad: each digit maps to the letters printed on its button.
DIGIT_TO_LETTERS = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations(digits):
    """
    Return every letter combination the phone number `digits` could spell.

    APPROACH (Backtracking with per-position choice sets)
    -----------------------------------------------------
    Same choose -> recurse -> un-choose skeleton as the other backtracking
    problems, walked by an index -- but with a twist compared to `subsets`:

      - subsets: at each index we made a binary decision (include nums[i] or
        not), and advanced with `start = i + 1`.
      - here: position `i` in the answer must be filled by EXACTLY ONE letter,
        chosen from the set of letters that digit i maps to. Different digits
        offer different-sized choice sets ("2" -> 3 letters, "7" -> 4 letters),
        so the branching factor varies from level to level.

    We build the answer left to right. The index `i` says which digit of the
    input we are currently spelling. At each call:

      - if i == len(digits), every digit has contributed a letter, so `path`
        is a complete combination -> record it, or
      - otherwise, look up the letters for digits[i] and try each one in turn:
            1. choose    -> append the letter to path,
            2. recurse   -> move to the next digit (i + 1),
            3. un-choose -> pop the letter so the next candidate can take its
                            place in this position.

    Unlike subsets/combination_sum, there is no "skip forward past several
    indices" -- every digit MUST be spelled, so we always advance by exactly one
    (i + 1) and never reuse a position. The combinatorial explosion comes purely
    from the fan-out: the answer count is the product of the choice-set sizes
    (e.g. "23" -> 3 * 3 = 9, "234" -> 3 * 3 * 3 = 27).

    EDGE CASE: an empty `digits` string has no combinations at all -- the
    expected output is [] (an empty list), NOT [""]. We guard for that up front,
    because the bare recursion would otherwise record the empty string as a
    "complete" combination of zero digits.

    COMPLEXITY
    ----------
    Let n = len(digits) and let the largest choice set have size m (m <= 4, for
    the digits 7 and 9).
    Time  : O(n * m^n) -- there are up to m^n combinations, each of length n to
            build and copy.
    Space : O(n) auxiliary for the recursion stack and `path` (excluding the
            output list itself).

    Args:
        digits (str): A string of digits in '2'..'9'.

    Returns:
        list[str]: Every letter combination the number could represent.
    """
    # No digits -> no combinations. Return [] rather than [""].
    if not digits:
        return []

    result = []
    path = []

    def backtrack(i):
        # Every digit has contributed a letter -> `path` is a full combination.
        if i == len(digits):
            result.append("".join(path))
            return

        # Try each letter this digit can map to.
        for letter in DIGIT_TO_LETTERS[digits[i]]:
            path.append(letter)     # choose `letter` for position i
            backtrack(i + 1)        # spell the next digit
            path.pop()              # un-choose

    backtrack(0)
    return result


if __name__ == "__main__":
    # Quick sanity checks. Order does not matter, so sort for stable comparison.
    print(sorted(letter_combinations("23")))
    # -> ['ad','ae','af','bd','be','bf','cd','ce','cf']
    print(letter_combinations(""))          # -> []  (NOT ['']))
    print(sorted(letter_combinations("2")))  # -> ['a', 'b', 'c']

    # The result count is the product of the per-digit choice-set sizes.
    print(len(letter_combinations("23")))    # -> 9   (3 * 3)
    print(len(letter_combinations("234")))   # -> 27  (3 * 3 * 3)
    print(len(letter_combinations("79")))    # -> 16  (4 * 4, digits 7 and 9)
