"""
Valid Palindrome
================

PROBLEM PROMPT
--------------
A phrase is a palindrome if, after converting all uppercase letters into
lowercase letters and removing all non-alphanumeric characters, it reads the
same forward and backward. Alphanumeric characters include letters and numbers.

Given a string `s`, return True if it is a palindrome, or False otherwise.

Example 1:
    Input:  s = "A man, a plan, a canal: Panama"
    Output: True
    Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
    Input:  s = "race a car"
    Output: False
    Explanation: "raceacar" is not a palindrome.

Example 3:
    Input:  s = " "
    Output: True
    Explanation: After removing non-alphanumeric characters, s is an empty
                 string "". An empty string reads the same forward and backward,
                 so it is a palindrome.

Constraints:
    1 <= len(s) <= 2 * 10^5
    s consists only of printable ASCII characters.
"""


def is_palindrome(s):
    """
    Return True if `s` is a palindrome, ignoring case and non-alphanumeric chars.

    APPROACH (Two Pointers)
    -----------------------
    A palindrome reads the same from both ends, so we compare characters from
    the outside in. We place one pointer at the start (`left`) and one at the
    end (`right`) of the string and walk them toward each other.

    Because we must ignore anything that isn't a letter or digit, each pointer
    skips over non-alphanumeric characters before a comparison is made. Once
    both pointers land on alphanumeric characters, we compare them in a
    case-insensitive way (by lowercasing). If they ever differ, the string
    cannot be a palindrome and we return False immediately. If the pointers
    cross without finding a mismatch, every meaningful pair matched and the
    string is a palindrome.

    This two-pointer method avoids building a separate cleaned-up copy of the
    string, so it uses no extra space proportional to the input.

    COMPLEXITY
    ----------
    Time  : O(n) — each pointer moves inward and together they visit each of the
            n characters at most once.
    Space : O(1) — only two index variables are used; no additional data
            structures scale with the input size.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if `s` is a valid palindrome, False otherwise.
    """
    # Pointers starting at the two ends of the string.
    left, right = 0, len(s) - 1

    while left < right:
        # Advance `left` past any character that isn't a letter or digit.
        while left < right and not s[left].isalnum():
            left += 1

        # Retreat `right` past any character that isn't a letter or digit.
        while left < right and not s[right].isalnum():
            right -= 1

        # Compare the two alphanumeric characters case-insensitively.
        # A mismatch means the string is not a palindrome.
        if s[left].lower() != s[right].lower():
            return False

        # Matched — move both pointers inward and continue.
        left += 1
        right -= 1

    # Pointers met/crossed with no mismatches, so it's a palindrome.
    return True


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(is_palindrome("A man, a plan, a canal: Panama"))  # -> True
    print(is_palindrome("race a car"))                      # -> False
    print(is_palindrome(" "))                               # -> True
    print(is_palindrome("0P"))                              # -> False ('0' != 'p')
