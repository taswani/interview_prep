"""
LeetCode 138: Copy List with Random Pointer

Problem Description:
--------------------
You are given a linked list where each node contains:
    - `val`: an integer value
    - `next`: a pointer to the next node in the list
    - `random`: a pointer to any node in the list (or None)

Your task is to return a deep copy of the list. A deep copy means that 
new nodes should be created such that none of the new nodes reference 
the original list nodes.

Example:
--------
Input: head = [[7, null], [13, 0], [11, 4], [10, 2], [1, 0]]
Explanation:
    Node 0 (val=7) → random = null
    Node 1 (val=13) → random = Node 0
    Node 2 (val=11) → random = Node 4
    Node 3 (val=10) → random = Node 2
    Node 4 (val=1) → random = Node 0

Output: Deep copy of the above list.

Constraints:
------------
- The number of nodes in the list is in the range [0, 1000].
- -10^4 <= Node.val <= 10^4
- random pointer is null or points to a valid node in the list.
"""

from typing import Optional


class Node:
    def __init__(self, val: int, next: 'Optional[Node]' = None, random: 'Optional[Node]' = None):
        self.val = val
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        """
        Creates a deep copy of the linked list with random pointers.
        """
        if not head:
            return None

        # Step 1: Create a mapping from original nodes to copied nodes
        old_to_new = {}

        curr = head
        while curr:
            old_to_new[curr] = Node(curr.val)
            curr = curr.next

        # Step 2: Assign next and random pointers for copied nodes
        curr = head
        while curr:
            if curr.next:
                old_to_new[curr].next = old_to_new[curr.next]
            if curr.random:
                old_to_new[curr].random = old_to_new[curr.random]
            curr = curr.next

        # Return the copied head
        return old_to_new[head]


# -------------------------------------------------------
# Time and Space Complexity
# -------------------------------------------------------
# Time Complexity: O(n)
#   - We traverse the list twice (once for creating nodes, once for linking).
#
# Space Complexity: O(n)
#   - Extra hashmap to store mapping between original and copied nodes.


# -------------------------------------------------------
# Test Cases
# -------------------------------------------------------
def print_list(head: Optional[Node]):
    """Helper function to print list nodes in (val, random_val) format."""
    result = []
    curr = head
    while curr:
        rand_val = curr.random.val if curr.random else None
        result.append((curr.val, rand_val))
        curr = curr.next
    return result


if __name__ == "__main__":
    # Build test list:
    # 7 -> 13 -> 11 -> 10 -> 1
    n1 = Node(7)
    n2 = Node(13)
    n3 = Node(11)
    n4 = Node(10)
    n5 = Node(1)

    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5

    # Random pointers
    n1.random = None
    n2.random = n1
    n3.random = n5
    n4.random = n3
    n5.random = n1

    print("Original list:", print_list(n1))

    sol = Solution()
    copied_head = sol.copyRandomList(n1)

    print("Copied list:", print_list(copied_head))
