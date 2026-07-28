"""
Lowest Common Ancestor of a Binary Tree
=======================================

PROBLEM PROMPT
--------------
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in
the tree.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is
defined between two nodes p and q as the lowest node in T that has both p and q
as descendants (where we allow a node to be a descendant of itself)."

NOTE: This is a GENERAL binary tree, not a binary search tree. There is no
ordering property to exploit, so we cannot decide direction by comparing values
(that shortcut only works for a BST).

Example 1:
    Input:  root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], p = 5, q = 1

                    3
                  /   \
                 5     1
                / \   / \
               6   2 0   8
                  / \
                 7   4

    Output: 3
    Explanation: The LCA of nodes 5 and 1 is 3.

Example 2:
    Input:  root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], p = 5, q = 4
    Output: 5
    Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant
                 of itself according to the LCA definition.

Constraints:
    The number of nodes in the tree is in the range [2, 10^5].
    -10^9 <= Node.val <= 10^9
    All Node.val are unique.
    p != q, and both p and q exist in the binary tree.
"""


class TreeNode:
    """A node in a binary tree."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val      # The value stored in this node.
        self.left = left    # Reference to the left child (or None).
        self.right = right  # Reference to the right child (or None).


def lowest_common_ancestor(root, p, q):
    """
    Return the lowest common ancestor of nodes p and q in a general binary tree.

    APPROACH (Recursive Post-Order Search)
    --------------------------------------
    Without a BST's ordering we can't tell which side p or q is on just by
    comparing values, so we actually have to SEARCH both subtrees. The elegant
    way is a post-order (bottom-up) recursion that answers, for each node, the
    question: "Did I find p and/or q at or below me?"

    The recursion returns:
      - The node itself if it IS p or q (a node can be its own ancestor), or if
        p and q were found in different subtrees below it.
      - Whatever non-None result bubbles up from its children otherwise.
      - None if neither p nor q is found in this subtree.

    Concretely, at each node we recurse into the left and right subtrees:

      - If BOTH sides return a non-None node, it means p was found in one subtree
        and q in the other. This node is where their paths first meet, so it is
        the LCA — we return it.
      - If only ONE side is non-None, both targets (or the single relevant one)
        live down that side, so we pass that result upward.
      - The base case returns the current node when it equals p or q (found one),
        or None when we fall off the tree (found nothing).

    The "split" node — the first one whose two subtrees each contain one target —
    is by definition the lowest node that has both as descendants.

    IMPORTANT SUBTLETY: This works even when one target is an ancestor of the
    other (Example 2). Say p is an ancestor of q. The recursion hits p first on
    the way down and returns p immediately without descending further to find q.
    Since the other subtree returns None, p bubbles all the way up as the answer
    — which is correct, because p is q's ancestor and its own descendant.

    COMPLEXITY
    ----------
    Time  : O(n) — in the worst case we visit every one of the n nodes once.
    Space : O(h) — the recursion call stack goes as deep as the tree's height h.
            For a balanced tree that's O(log n); for a degenerate (list-like)
            tree it's O(n).

    Args:
        root (TreeNode): Root of the binary tree.
        p (TreeNode): First target node.
        q (TreeNode): Second target node.

    Returns:
        TreeNode: The lowest common ancestor of p and q.
    """
    # Base case: fell off the tree (None), or found one of the targets. In both
    # situations we return the current value up to the caller.
    if root is None or root is p or root is q:
        return root

    # Search both subtrees for p and q.
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    # Found one target in each subtree -> this node is where they split -> LCA.
    if left and right:
        return root

    # Otherwise, whichever side is non-None carries the answer upward
    # (or None if neither side found anything).
    return left if left else right


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
    """Locate and return the node whose value equals target_val (BFS search)."""
    from collections import deque

    if root is None:
        return None
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node.val == target_val:
            return node
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return None


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    tree = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])

    p, q = find(tree, 5), find(tree, 1)
    print(lowest_common_ancestor(tree, p, q).val)  # -> 3

    p, q = find(tree, 5), find(tree, 4)
    print(lowest_common_ancestor(tree, p, q).val)  # -> 5 (one node is the other's ancestor)

    p, q = find(tree, 7), find(tree, 4)
    print(lowest_common_ancestor(tree, p, q).val)  # -> 2

    p, q = find(tree, 6), find(tree, 8)
    print(lowest_common_ancestor(tree, p, q).val)  # -> 3
