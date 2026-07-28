"""
Validate Binary Search Tree
===========================

PROBLEM PROMPT
--------------
Given the root of a binary tree, determine if it is a valid binary search tree
(BST).

A valid BST is defined as follows:
    - The left subtree of a node contains only nodes with keys strictly LESS
      than the node's key.
    - The right subtree of a node contains only nodes with keys strictly GREATER
      than the node's key.
    - Both the left and right subtrees must also be binary search trees.

Example 1:
    Input:  root = [2, 1, 3]

                2
               / \
              1   3

    Output: True

Example 2:
    Input:  root = [5, 1, 4, None, None, 3, 6]

                5
               / \
              1   4
                 / \
                3   6

    Output: False
    Explanation: The root node's value is 5 but its right child's value is 4,
                 which is not greater than 5. (Also, the node 3 is in 5's right
                 subtree but is smaller than 5 — a violation the naive
                 parent-only check would miss.)

Constraints:
    The number of nodes in the tree is in the range [1, 10^4].
    -2^31 <= Node.val <= 2^31 - 1
"""


class TreeNode:
    """A node in a binary tree."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val      # The value stored in this node.
        self.left = left    # Reference to the left child (or None).
        self.right = right  # Reference to the right child (or None).


def is_valid_bst(root):
    """
    Return True if the binary tree is a valid binary search tree, else False.

    APPROACH (Recursion with Valid-Range Bounds)
    --------------------------------------------
    The common mistake is to only check that each node is greater than its left
    child and less than its right child. That's not enough: the BST property is
    about ENTIRE subtrees, not just immediate children. For example, a node deep
    in the left subtree of the root must still be smaller than the root, even
    though the root is not its direct parent (see Example 2, node 3).

    The clean way to enforce this is to give every node a valid (low, high) range
    that its value must fall strictly within, and to tighten that range as we
    descend:

      - The root may be anything, so it starts with an open range
        (-infinity, +infinity).
      - When we go LEFT from a node, every value down there must be less than the
        node, so the upper bound becomes the node's value: (low, node.val).
      - When we go RIGHT, every value must be greater, so the lower bound becomes
        the node's value: (node.val, high).

    A node is valid if low < node.val < high (strict, since duplicates are not
    allowed), and if both of its subtrees are valid under their tightened ranges.
    An empty subtree (None) is trivially a valid BST.

    Because each node carries the accumulated constraints from ALL of its
    ancestors — not just its parent — this correctly rejects trees like
    Example 2 where a node satisfies its parent but violates a grandparent.

    COMPLEXITY
    ----------
    Time  : O(n) — every one of the n nodes is visited exactly once, with O(1)
            comparison work per node.
    Space : O(h) — the recursion call stack goes as deep as the tree's height h.
            For a balanced tree that's O(log n); for a degenerate (list-like)
            tree it's O(n).

    Args:
        root (TreeNode | None): Root of the binary tree to validate.

    Returns:
        bool: True if the tree is a valid BST, False otherwise.
    """

    def validate(node, low, high):
        # An empty subtree satisfies the BST property vacuously.
        if node is None:
            return True

        # The node's value must lie strictly inside its allowed (low, high) range.
        if not (low < node.val < high):
            return False

        # Recurse with tightened bounds:
        #   - Left subtree values must be below node.val -> new upper bound.
        #   - Right subtree values must be above node.val -> new lower bound.
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))

    # Start the root with an unbounded range.
    return validate(root, float("-inf"), float("inf"))


# ---------------------------------------------------------------------------
# Helper function (for the sanity checks below — not part of the solution).
# ---------------------------------------------------------------------------
def build_tree(values):
    """
    Build a binary tree from a level-order list (LeetCode style) where None
    marks a missing child. Returns the root.
    """
    if not values:
        return None

    from collections import deque

    root = TreeNode(values[0])
    queue = deque([root])
    index = 1

    while queue and index < len(values):
        node = queue.popleft()

        if index < len(values) and values[index] is not None:
            node.left = TreeNode(values[index])
            queue.append(node.left)
        index += 1

        if index < len(values) and values[index] is not None:
            node.right = TreeNode(values[index])
            queue.append(node.right)
        index += 1

    return root


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(is_valid_bst(build_tree([2, 1, 3])))                       # -> True
    print(is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6])))     # -> False
    print(is_valid_bst(build_tree([5, 4, 6, None, None, 3, 7])))     # -> False (3 < 5 in right subtree)
    print(is_valid_bst(build_tree([1])))                            # -> True (single node)
    print(is_valid_bst(build_tree([2, 2, 2])))                      # -> False (duplicates not allowed)
