"""
Add Two Numbers
===============

PROBLEM PROMPT
--------------
You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in REVERSE order, and each of their nodes contains a single
digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the
number 0 itself.

Example 1:
    Input:  l1 = [2, 4, 3], l2 = [5, 6, 4]
    Output: [7, 0, 8]
    Explanation: 342 + 465 = 807. (The lists are stored reversed, so [2,4,3]
                 represents 342, and the result 807 is stored as [7, 0, 8].)

Example 2:
    Input:  l1 = [0], l2 = [0]
    Output: [0]

Example 3:
    Input:  l1 = [9, 9, 9, 9, 9, 9, 9], l2 = [9, 9, 9, 9]
    Output: [8, 9, 9, 9, 0, 0, 0, 1]
    Explanation: 9999999 + 9999 = 10009998.

Constraints:
    The number of nodes in each list is in the range [1, 100].
    0 <= Node.val <= 9
    It is guaranteed that the list represents a number that does not have
    leading zeros.
"""


class ListNode:
    """A node in a singly linked list."""

    def __init__(self, val=0, next=None):
        self.val = val    # A single digit (0-9).
        self.next = next  # Reference to the next node (or None at the end).


def add_two_numbers(l1, l2):
    """
    Add two numbers represented as reversed-digit linked lists.

    APPROACH (Elementary Addition with a Carry)
    -------------------------------------------
    Because the digits are stored in REVERSE order, the heads of both lists are
    the least-significant digits (ones place). That's exactly the order you add
    numbers by hand: start from the rightmost digits, add them, write down the
    result digit, and carry the overflow into the next column. So we can walk
    both lists front-to-back in lockstep and add column by column.

    For each position we sum three things:
        digit from l1 (or 0 if that list has ended)
      + digit from l2 (or 0 if that list has ended)
      + the carry from the previous column

    From that total, the new digit is `total % 10` and the carry passed forward
    is `total // 10` (either 0 or 1). We append the new digit to the result list.

    Two details make the loop clean:
      - A DUMMY head node lets us append without special-casing the first digit;
        the real result is `dummy.next`.
      - The loop continues while EITHER list has nodes left OR there is still a
        carry. That final carry condition handles cases like 999 + 1 = 1000,
        where the sum has more digits than either input (Example 3).

    COMPLEXITY
    ----------
    Time  : O(max(n, m)) — where n and m are the two list lengths. We process
            each column once, and there are max(n, m) columns (plus possibly one
            more for a final carry).
    Space : O(max(n, m)) — the result list has max(n, m) or max(n, m) + 1 digits.
            Only O(1) extra working space (the carry and a few pointers) is used
            beyond the output itself.

    Args:
        l1 (ListNode): Head of the first number (digits reversed).
        l2 (ListNode): Head of the second number (digits reversed).

    Returns:
        ListNode: Head of the summed number (digits reversed).
    """
    # Dummy head simplifies appending; `tail` tracks the end of the result list.
    dummy = ListNode()
    tail = dummy
    carry = 0

    # Continue while either list has digits left, or a carry still needs placing.
    while l1 or l2 or carry:
        # Pull the current digit from each list, treating a finished list as 0.
        digit1 = l1.val if l1 else 0
        digit2 = l2.val if l2 else 0

        # Column sum, including the carry from the previous column.
        total = digit1 + digit2 + carry
        carry = total // 10          # 1 if the column overflowed past 9, else 0.

        # Append the ones-place of this column as the next result digit.
        tail.next = ListNode(total % 10)
        tail = tail.next

        # Advance each list pointer if it still has nodes.
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    # dummy.next skips the throwaway node and points at the real result head.
    return dummy.next


# ---------------------------------------------------------------------------
# Helper functions (for the sanity checks below — not part of the solution).
# ---------------------------------------------------------------------------
def build_list(values):
    """Build a linked list from a Python list and return its head."""
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_python_list(head):
    """Convert a linked list back into a Python list for easy printing."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(to_python_list(add_two_numbers(build_list([2, 4, 3]),
                                         build_list([5, 6, 4]))))  # -> [7, 0, 8]
    print(to_python_list(add_two_numbers(build_list([0]),
                                         build_list([0]))))        # -> [0]
    print(to_python_list(add_two_numbers(build_list([9, 9, 9, 9, 9, 9, 9]),
                                         build_list([9, 9, 9, 9]))))  # -> [8, 9, 9, 9, 0, 0, 0, 1]
