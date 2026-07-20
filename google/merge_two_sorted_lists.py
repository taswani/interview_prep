"""
Merge Two Sorted Lists
======================

PROBLEM PROMPT
--------------
You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one sorted list. The list should be made by splicing
together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
    Input:  list1 = [1, 2, 4], list2 = [1, 3, 4]
    Output: [1, 1, 2, 3, 4, 4]

Example 2:
    Input:  list1 = [], list2 = []
    Output: []

Example 3:
    Input:  list1 = [], list2 = [0]
    Output: [0]

Constraints:
    The number of nodes in both lists is in the range [0, 50].
    -100 <= Node.val <= 100
    Both list1 and list2 are sorted in non-decreasing order.
"""


class ListNode:
    """A node in a singly linked list."""

    def __init__(self, val=0, next=None):
        self.val = val    # The value stored in this node.
        self.next = next  # Reference to the next node (or None at the end).


def merge_two_lists(list1, list2):
    """
    Merge two sorted linked lists into one sorted list and return its head.

    APPROACH (Two Pointers + Dummy Head)
    ------------------------------------
    Because both input lists are already sorted, we can merge them the same way
    you would merge two sorted piles of cards: repeatedly take the smaller of the
    two current front cards and place it onto the output.

    Two tricks keep the code clean:

      1. Dummy head node — we create a throwaway `dummy` node and build the
         merged list after it. This means we never have to special-case setting
         the very first node; `dummy.next` ends up pointing at the real head.

      2. Tail pointer — `tail` always points at the last node of the merged list
         so we can append the next chosen node in O(1) time.

    We walk both lists at once. At each step we compare the current nodes and
    splice the smaller one onto `tail`, then advance that list's pointer. When
    one list runs out, the other list is already sorted and can simply be
    attached to the end in a single link — no further comparisons needed.

    We splice existing nodes rather than allocating new ones, so no extra list
    is built.

    COMPLEXITY
    ----------
    Time  : O(n + m) — where n and m are the lengths of the two lists. Each node
            is visited and linked exactly once.
    Space : O(1) — only a fixed number of pointers are used. The merged list
            reuses the existing nodes, so no space grows with the input size.
            (The output list itself is not counted as extra space.)

    Args:
        list1 (ListNode | None): Head of the first sorted list.
        list2 (ListNode | None): Head of the second sorted list.

    Returns:
        ListNode | None: Head of the merged sorted list.
    """
    # Dummy head simplifies edge cases; `tail` tracks the end of the merged list.
    dummy = ListNode()
    tail = dummy

    # While both lists still have nodes, pick the smaller front node each time.
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1      # Attach list1's node to the merged list.
            list1 = list1.next     # Advance past the node we just used.
        else:
            tail.next = list2      # Attach list2's node instead.
            list2 = list2.next     # Advance past it.
        tail = tail.next           # Move the tail to the newly attached node.

    # At most one list still has nodes left. Since it's already sorted, we can
    # attach the whole remainder in one link.
    tail.next = list1 if list1 else list2

    # dummy.next skips the throwaway node and points at the real merged head.
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
    print(to_python_list(merge_two_lists(build_list([1, 2, 4]),
                                         build_list([1, 3, 4]))))  # -> [1, 1, 2, 3, 4, 4]
    print(to_python_list(merge_two_lists(build_list([]),
                                         build_list([]))))         # -> []
    print(to_python_list(merge_two_lists(build_list([]),
                                         build_list([0]))))        # -> [0]
