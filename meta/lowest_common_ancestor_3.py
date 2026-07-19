"""
Leetcode 1650: Lowest Common Ancestor of a Binary Tree III

Problem Description:
--------------------
Given two nodes p and q of a binary tree, return their lowest common ancestor (LCA).
Each node has a reference to its parent node in addition to its left and right children.

Definition of LCA:
The lowest node in the tree that has both p and q as descendants (a node can be a descendant of itself).

Constraints:
- The number of nodes in the tree is in the range [2, 10^5].
- -10^9 <= Node.val <= 10^9
- All Node.val are unique.
- p != q
- p and q exist in the tree.

--------------------------------------------------------------------------------
Solution:
---------
We can solve this problem using the two-pointer technique, similar to finding the
intersection of two linked lists.

Intuition:
- Imagine the path from p to root and from q to root as two linked lists.
- Start two pointers, one at p and one at q, and move upward.
- When a pointer reaches the root (None), redirect it to the other starting node.
- Eventually, both pointers will align and meet at the LCA.

Why it works:
- Both pointers traverse exactly the same distance (depth(p) + depth(q)).
- The meeting point is guaranteed to be their lowest common ancestor.

--------------------------------------------------------------------------------
Time Complexity:
- O(h), where h is the height of the tree.
- In worst case, O(depth(p) + depth(q)) steps.

Space Complexity:
- O(1), since we only use two pointers.

"""

# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

class Solution:
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        a, b = p, q
        while a != b:
            a = a.parent if a else q
            b = b.parent if b else p
        return a


# -------------------------------------------------------------
# Test Cases
# -------------------------------------------------------------
if __name__ == "__main__":
    # Construct example tree:
    #       3
    #      / \
    #     5   1
    #    / \
    #   6   2
    #      / \
    #     7   4

    root = Node(3)
    node5 = Node(5)
    node1 = Node(1)
    node6 = Node(6)
    node2 = Node(2)
    node7 = Node(7)
    node4 = Node(4)

    root.left, root.right = node5, node1
    node5.parent, node1.parent = root, root
    node5.left, node5.right = node6, node2
    node6.parent, node2.parent = node5, node5
    node2.left, node2.right = node7, node4
    node7.parent, node4.parent = node2, node2

    solution = Solution()

    # Test 1: LCA of 6 and 4 is 5
    print("LCA of 6 and 4:", solution.lowestCommonAncestor(node6, node4).val)  # Expected 5

    # Test 2: LCA of 7 and 1 is 3
    print("LCA of 7 and 1:", solution.lowestCommonAncestor(node7, node1).val)  # Expected 3

    # Test 3: LCA of 6 and 5 is 5
    print("LCA of 6 and 5:", solution.lowestCommonAncestor(node6, node5).val)  # Expected 5
