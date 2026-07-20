"""
Valid Parentheses
==================

PROBLEM PROMPT
--------------
Given a string `s` containing just the characters '(', ')', '{', '}', '[' and
']', determine if the input string is valid.

An input string is valid if:
    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
    Input:  s = "()"
    Output: True

Example 2:
    Input:  s = "()[]{}"
    Output: True

Example 3:
    Input:  s = "(]"
    Output: False

Example 4:
    Input:  s = "([)]"
    Output: False   # correct types but wrong order

Example 5:
    Input:  s = "{[]}"
    Output: True

Constraints:
    1 <= len(s) <= 10^4
    s consists only of the characters '()[]{}'.
"""


def is_valid(s):
    """
    Return True if the bracket string `s` is valid, False otherwise.

    APPROACH (Stack)
    ----------------
    Brackets must close in the reverse order they were opened — the most
    recently opened bracket must be the first one closed. That "last opened,
    first closed" behaviour is exactly what a stack (last-in, first-out)
    models.

    We scan the string left to right:
      - When we see an opening bracket, we push it onto the stack, recording
        that it is waiting to be closed.
      - When we see a closing bracket, it must match the bracket on top of the
        stack (the most recent still-open one). If the stack is empty (nothing
        to close) or the top doesn't match the expected opener, the string is
        invalid.

    A lookup table maps each closing bracket to the opening bracket it requires,
    keeping the matching logic simple.

    After the scan, a valid string leaves the stack empty — every opener was
    matched and closed. If anything remains on the stack, there are unclosed
    openers, so the string is invalid.

    COMPLEXITY
    ----------
    Time  : O(n) — each of the n characters is processed once with O(1) work
            (a push, or a pop-and-compare).
    Space : O(n) — in the worst case (e.g. "(((((") every character is an opener
            and all of them sit on the stack at once.

    Args:
        s (str): The bracket string to validate.

    Returns:
        bool: True if `s` is valid, False otherwise.
    """
    # Maps each closing bracket to its matching opening bracket.
    closing_to_opening = {")": "(", "]": "[", "}": "{"}

    # Stack holding the opening brackets we've seen but not yet closed.
    stack = []

    for char in s:
        if char in closing_to_opening:
            # It's a closing bracket. Pop the most recent opener (or a
            # placeholder if the stack is empty) and check that it matches.
            top = stack.pop() if stack else "#"
            if top != closing_to_opening[char]:
                return False
        else:
            # It's an opening bracket. Remember it until its match arrives.
            stack.append(char)

    # Valid only if every opener was matched — i.e. the stack is now empty.
    return not stack


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(is_valid("()"))       # -> True
    print(is_valid("()[]{}"))   # -> True
    print(is_valid("(]"))       # -> False
    print(is_valid("([)]"))     # -> False
    print(is_valid("{[]}"))     # -> True
    print(is_valid("("))        # -> False (unclosed opener)
