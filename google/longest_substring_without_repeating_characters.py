"""
Longest Substring Without Repeating Characters
==============================================

PROBLEM PROMPT
--------------
Given a string `s`, find the length of the longest substring without repeating
characters.

A substring is a contiguous (non-empty) sequence of characters within the
string. Note this is different from a subsequence, which need not be contiguous.

Example 1:
    Input:  s = "abcabcbb"
    Output: 3
    Explanation: The answer is "abc", with a length of 3.

Example 2:
    Input:  s = "bbbbb"
    Output: 1
    Explanation: The answer is "b", with a length of 1.

Example 3:
    Input:  s = "pwwkew"
    Output: 3
    Explanation: The answer is "wke", with a length of 3. Note that "pwke" is a
                 subsequence, not a substring.

Constraints:
    0 <= len(s) <= 5 * 10^4
    s consists of English letters, digits, symbols and spaces.
"""


def length_of_longest_substring(s):
    """
    Return the length of the longest substring of `s` with all distinct chars.

    APPROACH (Sliding Window + Hash Map)
    ------------------------------------
    We maintain a "window" — a contiguous range [left, right] — that always
    contains only distinct characters. We expand the window by moving `right`
    forward one character at a time, and whenever a duplicate appears we shrink
    it from the left until the window is valid (duplicate-free) again.

    To do the shrinking in O(1) instead of re-scanning, we store the most recent
    index at which each character was seen in a hash map:

        last_seen: character -> its most recent index

    When we encounter a character that is already inside the current window
    (i.e. its last seen index is >= left), we jump `left` to just past that
    previous occurrence. This removes the duplicate from the window in a single
    step rather than sliding one character at a time.

    At every position we update the best length with the current window size,
    which is (right - left + 1). The largest value seen is the answer.

    The `last_seen[char] >= left` check is important: a character seen earlier
    but *before* the current window's start is not actually a duplicate inside
    the window, so we must not move `left` backward.

    COMPLEXITY
    ----------
    Time  : O(n) — `right` advances through each of the n characters once, and
            `left` only ever moves forward, so total pointer movement is O(n).
    Space : O(k) — the map holds at most one entry per distinct character, where
            k is the size of the character set (bounded by min(n, alphabet size)).

    Args:
        s (str): The input string.

    Returns:
        int: Length of the longest substring without repeating characters.
    """
    # Maps each character to the most recent index where we saw it.
    last_seen = {}

    # Left edge of the current window and the best window length found so far.
    left = 0
    best = 0

    # `right` scans the string; it is the right edge of the window.
    for right, char in enumerate(s):
        # If we've seen `char` before AND that occurrence is inside the current
        # window, move `left` to just past it to drop the duplicate.
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        # Record (or update) the latest index of this character.
        last_seen[char] = right

        # Current window [left, right] is duplicate-free; update the best length.
        best = max(best, right - left + 1)

    return best


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(length_of_longest_substring("abcabcbb"))  # -> 3 ("abc")
    print(length_of_longest_substring("bbbbb"))     # -> 1 ("b")
    print(length_of_longest_substring("pwwkew"))    # -> 3 ("wke")
    print(length_of_longest_substring(""))          # -> 0 (empty string)
    print(length_of_longest_substring("abba"))      # -> 2 (tests the left-pointer guard)
