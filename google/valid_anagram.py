"""
Valid Anagram
=============

PROBLEM PROMPT
--------------
Given two strings `s` and `t`, return True if `t` is an anagram of `s`, and
False otherwise.

An anagram is a word or phrase formed by rearranging the letters of a different
word or phrase, using all the original letters exactly once.

Example 1:
    Input:  s = "anagram", t = "nagaram"
    Output: True

Example 2:
    Input:  s = "rat", t = "car"
    Output: False

Constraints:
    1 <= len(s), len(t) <= 5 * 10^4
    s and t consist of lowercase English letters.

Follow-up:
    What if the inputs contain Unicode characters? The counting approach below
    handles that naturally, since it counts whatever characters appear rather
    than assuming a fixed 26-letter alphabet.
"""


def is_anagram(s, t):
    """
    Return True if `t` is an anagram of `s`, False otherwise.

    APPROACH (Character Frequency Count)
    ------------------------------------
    Two strings are anagrams if and only if they contain exactly the same
    characters with exactly the same frequencies. A quick first check is length:
    if the two strings differ in length, they cannot be anagrams, so we can bail
    out immediately.

    Otherwise we tally how many times each character appears. We increment a
    counter for every character in `s` and decrement it for every character in
    `t`. If the two strings are anagrams, every increment from `s` is cancelled
    by a matching decrement from `t`, leaving every count at exactly zero. If any
    count is non-zero at the end, some character appeared a different number of
    times in each string, so they are not anagrams.

    Using a hash map (dictionary) of counts lets us look up and update each
    character's tally in O(1) average time.

    COMPLEXITY
    ----------
    Time  : O(n) — we scan both strings once (they share the same length n) and
            do O(1) work per character; the final check over the counts is at
            most O(k) where k is the number of distinct characters (k <= n).
    Space : O(k) — the count map holds one entry per distinct character. For a
            fixed alphabet (e.g. lowercase English letters) this is O(1); in the
            general case it is bounded by the number of distinct characters.

    Args:
        s (str): The first string.
        t (str): The second string.

    Returns:
        bool: True if `t` is an anagram of `s`, False otherwise.
    """
    # Different lengths can never be anagrams — no need to count anything.
    if len(s) != len(t):
        return False

    # Maps each character to its running frequency balance.
    counts = {}

    # Count up the characters in `s`...
    for char in s:
        counts[char] = counts.get(char, 0) + 1

    # ...and count down the characters in `t`.
    for char in t:
        # If `char` never appeared in `s`, get() returns 0 and this goes
        # negative, which will be caught by the check below.
        counts[char] = counts.get(char, 0) - 1

    # Anagrams leave every balance at exactly zero. Any non-zero value means
    # a character's frequency differed between the two strings.
    for value in counts.values():
        if value != 0:
            return False

    return True


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(is_anagram("anagram", "nagaram"))  # -> True
    print(is_anagram("rat", "car"))          # -> False
    print(is_anagram("a", "ab"))             # -> False (different lengths)
    print(is_anagram("", ""))                # -> True  (both empty)
