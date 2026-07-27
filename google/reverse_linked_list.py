"""
Reverse Linked List
===================

PROBLEM PROMPT
--------------
Given the head of a singly linked list, reverse the list, and return the
reversed list's head.

Example 1:
    Input:  head = [1, 2, 3, 4, 5]
    Output: [5, 4, 3, 2, 1]

Example 2:
    Input:  head = [1, 2]
    Output: [2, 1]

Example 3:
    Input:  head = []
    Output: []

Constraints:
    The number of nodes in the list is in the range [0, 5000].
    -5000 <= Node.val <= 5000

Follow-up:
    A linked list can be reversed either iteratively or recursively. Could you
    implement both? (Both are shown below.)
"""


class ListNode:
    """A node in a singly linked list."""

    def __init__(self, val=0, next=None):
        self.val = val    # The value stored in this node.
        self.next = next  # Reference to the next node (or None at the end).


def reverse_list(head):
    """
    Reverse a singly linked list iteratively and return the new head.

    APPROACH (Iterative Pointer Reversal)
    -------------------------------------
    Reversing a singly linked list means flipping the direction of every `next`
    pointer: the node that used to point forward should instead point backward.

    We walk the list one node at a time, keeping track of three references:

        prev  -> the node just behind us (the reversed portion's head so far).
                 Starts as None because the original head becomes the new tail,
                 whose `next` must be None.
        curr  -> the node we're currently processing.
        nxt   -> the next node, saved BEFORE we overwrite curr.next, so we don't
                 lose the rest of the list.

    For each node we redirect curr.next to point at prev (reversing that link),
    then slide all three pointers forward by one. When curr falls off the end
    (becomes None), prev is sitting on the last node we processed — which is the
    original tail and therefore the new head.

    COMPLEXITY
    ----------
    Time  : O(n) — we visit each of the n nodes exactly once.
    Space : O(1) — only three pointer variables are used, regardless of list
            length. (The recursive version below is O(n) space due to the call
            stack.)

    Args:
        head (ListNode | None): Head of the list to reverse.

    Returns:
        ListNode | None: Head of the reversed list.
    """
    prev = None      # Reversed portion built up behind us; new list's growing head.
    curr = head      # Node we're currently reversing.

    while curr:
        nxt = curr.next   # Save the next node before we overwrite the link.
        curr.next = prev  # Reverse this node's pointer to face backward.
        prev = curr       # Advance `prev` to the node we just reversed.
        curr = nxt        # Advance `curr` to the saved next node.

    # `curr` is now None; `prev` is the original tail, i.e. the new head.
    return prev


def reverse_list_recursive(head):
    """
    Reverse a singly linked list recursively and return the new head.

    APPROACH (Recursion)
    --------------------
    Recursively reverse everything after the head, then fix up the single link
    between the head and its original successor.

      - Base case: an empty list or a single node is already its own reverse, so
        we return it unchanged.
      - Recursive case: reverse the sublist starting at head.next. That call
        returns the new head of the fully reversed remainder. The original
        head.next node is now the tail of that reversed remainder, so we make it
        point back at head (head.next.next = head), and sever head's old forward
        link (head.next = None) so head becomes the new tail.

    COMPLEXITY
    ----------
    Time  : O(n) — each node is touched once.
    Space : O(n) — the recursion call stack goes n frames deep in the worst case.

    Args:
        head (ListNode | None): Head of the list to reverse.

    Returns:
        ListNode | None: Head of the reversed list.
    """
    # Base case: empty list or a single node needs no reversing.
    if head is None or head.next is None:
        return head

    # Reverse the rest of the list; new_head is the reversed remainder's head.
    new_head = reverse_list_recursive(head.next)

    # head.next is the tail of the reversed remainder; point it back at head.
    head.next.next = head
    head.next = None  # head is now the last node, so it points to nothing.

    return new_head


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
    # Quick sanity checks demonstrating both implementations.
    print(to_python_list(reverse_list(build_list([1, 2, 3, 4, 5]))))            # -> [5, 4, 3, 2, 1]
    print(to_python_list(reverse_list(build_list([1, 2]))))                     # -> [2, 1]
    print(to_python_list(reverse_list(build_list([]))))                        # -> []
    print(to_python_list(reverse_list_recursive(build_list([1, 2, 3, 4, 5]))))  # -> [5, 4, 3, 2, 1]
    print(to_python_list(reverse_list_recursive(build_list([]))))              # -> []
