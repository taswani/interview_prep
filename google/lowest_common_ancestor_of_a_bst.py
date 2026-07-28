"""
Lowest Common Ancestor of a Binary Search Tree
==============================================

PROBLEM PROMPT
--------------
Given a binary search tree (BST), find the lowest common ancestor (LCA) of two
given nodes in the BST.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is
defined between two nodes p and q as the lowest node in T that has both p and q
as descendants (where we allow a node to be a descendant of itself)."

Example 1:
    Input:  root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], p = 2, q = 8

                    6
                  /   \
                 2     8
                / \   / \
               0   4 7   9
                  / \
                 3   5

    Output: 6
    Explanation: The LCA of nodes 2 and 8 is 6.

Example 2:
    Input:  root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], p = 2, q = 4
    Output: 2
    Explanation: The LCA of nodes 2 and 4 is 2, since a node can be a descendant
                 of itself according to the LCA definition.

Constraints:
    The number of nodes in the tree is in the range [2, 10^5].
    -10^9 <= Node.val <= 10^9
    All Node.val are unique.
    p != q, and both p and q exist in the BST.
"""


class TreeNode:
    """A node in a binary search tree."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val      # The value stored in this node.
        self.left = left    # Left child: values less than this node.
        self.right = right  # Right child: values greater than this node.


def lowest_common_ancestor(root, p, q):
    """
    Return the lowest common ancestor of nodes p and q in a BST.

    APPROACH (Exploit the BST Ordering, Recursively)
    ------------------------------------------------
    In a general binary tree, finding the LCA requires searching both subtrees.
    But a BST gives us a powerful shortcut: for any node, everything in its left
    subtree is smaller and everything in its right subtree is larger. That
    ordering tells us which way p and q lie relative to the current node without
    any searching.

    Starting at the root, we compare both target values against the current
    node's value and recurse into just ONE subtree:

      - If BOTH p and q are greater than the current node, the LCA must be
        somewhere in the RIGHT subtree, so we recurse right.
      - If BOTH p and q are less than the current node, the LCA must be in the
        LEFT subtree, so we recurse left.
      - Otherwise the values "split" — one is <= the current node and the other
        is >= it (or one of them IS the current node). This is the exact point
        where the paths to p and q diverge, so the current node is their lowest
        common ancestor. We return it (this is the recursion's base case).

    Because at each step we recurse into only one child, this recursion never
    branches — it walks a single path down the tree.

    COMPLEXITY
    ----------
    Time  : O(h) — where h is the height of the tree. We follow a single path
            downward, so at most h nodes are visited. For a balanced BST that's
            O(log n); for a degenerate (list-like) BST it's O(n).
    Space : O(h) — the recursion call stack goes as deep as the path we follow,
            i.e. the tree height. (The iterative version would be O(1); recursion
            trades that constant space for the call stack. Note Python does not
            optimize tail calls, so the frames genuinely accumulate.)

    Args:
        root (TreeNode): Root of the BST.
        p (TreeNode): First target node.
        q (TreeNode): Second target node.

    Returns:
        TreeNode: The lowest common ancestor of p and q.
    """
    # Both targets larger -> LCA lies to the right, so recurse right.
    if p.val > root.val and q.val > root.val:
        return lowest_common_ancestor(root.right, p, q)

    # Both targets smaller -> LCA lies to the left, so recurse left.
    if p.val < root.val and q.val < root.val:
        return lowest_common_ancestor(root.left, p, q)

    # The paths split here (or this node is one of the targets): it's the LCA.
    # This is the base case that stops the recursion.
    return root


# ---------------------------------------------------------------------------
# Helper functions (for the sanity checks below — not part of the solution).
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


def find(root, target_val):
    """Locate and return the node whose value equals target_val (BST search)."""
    node = root
    while node:
        if target_val < node.val:
            node = node.left
        elif target_val > node.val:
            node = node.right
        else:
            return node
    return None


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    tree = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])

    p, q = find(tree, 2), find(tree, 8)
    print(lowest_common_ancestor(tree, p, q).val)  # -> 6

    p, q = find(tree, 2), find(tree, 4)
    print(lowest_common_ancestor(tree, p, q).val)  # -> 2 (a node can be its own ancestor)

    p, q = find(tree, 3), find(tree, 5)
    print(lowest_common_ancestor(tree, p, q).val)  # -> 4
