"""
Longest Palindromic Substring
=============================

PROBLEM PROMPT
--------------
Given a string `s`, return the longest palindromic substring in `s`.

A palindrome reads the same forward and backward. A substring is a contiguous
(non-empty) sequence of characters within the string.

Example 1:
    Input:  s = "babad"
    Output: "bab"
    Explanation: "aba" is also a valid answer.

Example 2:
    Input:  s = "cbbd"
    Output: "bb"

Constraints:
    1 <= len(s) <= 1000
    s consists of only digits and English letters.
"""


def longest_palindrome(s):
    """
    Return the longest palindromic substring of `s`.

    APPROACH (Expand Around Center)
    -------------------------------
    A brute-force check of every substring for palindrome-ness is O(n^3). The key
    insight that beats it: every palindrome has a CENTER and reads symmetrically
    outward from it. So instead of checking substrings, we consider every
    possible center and grow outward as long as the characters on both sides
    match. The longest expansion we ever achieve is the answer.

    There are two kinds of centers, and we must try both at each position:

      - ODD-length palindromes (e.g. "aba") have a single character at their
        center. There are n such centers — one per character.
      - EVEN-length palindromes (e.g. "abba") have their center BETWEEN two
        characters. There are n - 1 such centers — one per adjacent pair.

    For each center we push a left pointer and a right pointer outward in tandem,
    stopping as soon as they go out of bounds or the characters stop matching.
    The span they cover is a palindrome; we keep track of the longest one seen.

    In total there are ~2n centers and each expansion is at most O(n), giving
    O(n^2) time with only O(1) extra space — a great balance of simplicity and
    efficiency for the given constraints. (The O(n) Manacher's algorithm exists
    but is far more intricate and rarely expected in interviews.)

    COMPLEXITY
    ----------
    Time  : O(n^2) — 2n - 1 centers, each expanded outward up to O(n) times.
    Space : O(1) — only index/length bookkeeping is stored; no auxiliary arrays.
            (The returned substring slice is the output, not extra working space.)

    Args:
        s (str): The input string.

    Returns:
        str: The longest palindromic substring (any one, if there are ties).
    """
    if len(s) < 2:
        # A string of length 0 or 1 is already its own longest palindrome.
        return s

    # Track the [start, end] indices of the best palindrome found so far.
    best_start, best_end = 0, 0

    def expand(left, right):
        """
        Expand outward from a center while the palindrome holds, and return the
        (start, end) index bounds of the widest palindrome centered there.
        """
        # Grow while in bounds and the mirrored characters match.
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # The loop overshoots by one step on each side, so pull back in.
        return left + 1, right - 1

    for center in range(len(s)):
        # Odd-length palindrome: single-character center at `center`.
        l1, r1 = expand(center, center)
        if r1 - l1 > best_end - best_start:
            best_start, best_end = l1, r1

        # Even-length palindrome: center sits between `center` and `center + 1`.
        l2, r2 = expand(center, center + 1)
        if r2 - l2 > best_end - best_start:
            best_start, best_end = l2, r2

    # Slice is inclusive of best_end, hence the + 1.
    return s[best_start:best_end + 1]


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(longest_palindrome("babad"))  # -> "bab" (or "aba")
    print(longest_palindrome("cbbd"))   # -> "bb"
    print(longest_palindrome("a"))      # -> "a"
    print(longest_palindrome("ac"))     # -> "a" (or "c"; no multi-char palindrome)
    print(longest_palindrome("forgeeksskeegfor"))  # -> "geeksskeeg" (even-length center)
