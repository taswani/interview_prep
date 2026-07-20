"""
Invert Binary Tree
==================

PROBLEM PROMPT
--------------
Given the root of a binary tree, invert the tree, and return its root.

Inverting a binary tree means swapping the left and right children of every
node, producing a mirror image of the original tree.

Example 1:
    Input:  root = [4, 2, 7, 1, 3, 6, 9]

                4                     4
              /   \                 /   \
             2     7      -->      7     2
            / \   / \             / \   / \
           1   3 6   9           9   6 3   1

    Output: [4, 7, 2, 9, 6, 3, 1]

Example 2:
    Input:  root = [2, 1, 3]
    Output: [2, 3, 1]

Example 3:
    Input:  root = []
    Output: []

Constraints:
    The number of nodes in the tree is in the range [0, 100].
    -100 <= Node.val <= 100
"""


class TreeNode:
    """A node in a binary tree."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val      # The value stored in this node.
        self.left = left    # Reference to the left child (or None).
        self.right = right  # Reference to the right child (or None).


def invert_tree(root):
    """
    Invert (mirror) a binary tree and return its root.

    APPROACH (Recursion / Depth-First)
    ----------------------------------
    Inverting a tree means that at every node, its left subtree and right
    subtree trade places. Crucially, this must happen at *every* level, not just
    the top — so it's a naturally recursive problem: to invert a tree, invert
    each of its subtrees and then swap them.

    The recursion works as follows:
      - Base case: an empty tree (None) has nothing to invert, so we return None.
      - Recursive case: swap the current node's left and right children, then
        recursively invert each of those children.

    The order of "swap then recurse" versus "recurse then swap" doesn't matter
    here — every node gets swapped exactly once regardless — so we simply swap
    the two child references and recurse into both.

    (This uses the call stack to visit nodes; an explicit stack or queue with a
    loop would work equally well and avoid Python's recursion-depth limit for
    very deep trees.)

    COMPLEXITY
    ----------
    Time  : O(n) — every one of the n nodes is visited exactly once, doing O(1)
            work (a pointer swap) per node.
    Space : O(h) — the recursion call stack goes as deep as the tree's height h.
            In the worst case (a completely unbalanced tree) h == n, giving O(n);
            for a balanced tree h == log n, giving O(log n).

    Args:
        root (TreeNode | None): Root of the binary tree to invert.

    Returns:
        TreeNode | None: Root of the inverted tree (same node object as input).
    """
    # Base case: an empty subtree stays empty.
    if root is None:
        return None

    # Swap this node's two children. Python's tuple assignment swaps both
    # references simultaneously, so no temporary variable is needed.
    root.left, root.right = root.right, root.left

    # Recursively invert each subtree so the mirroring reaches every level.
    invert_tree(root.left)
    invert_tree(root.right)

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

        # Attach left child if present.
        if index < len(values) and values[index] is not None:
            node.left = TreeNode(values[index])
            queue.append(node.left)
        index += 1

        # Attach right child if present.
        if index < len(values) and values[index] is not None:
            node.right = TreeNode(values[index])
            queue.append(node.right)
        index += 1

    return root


def level_order(root):
    """Return the tree's values in level order (None for missing children)."""
    if root is None:
        return []

    from collections import deque

    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
            continue
        result.append(node.val)
        queue.append(node.left)
        queue.append(node.right)

    # Trim trailing None values for a cleaner comparison with the expected output.
    while result and result[-1] is None:
        result.pop()
    return result


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(level_order(invert_tree(build_tree([4, 2, 7, 1, 3, 6, 9]))))  # -> [4, 7, 2, 9, 6, 3, 1]
    print(level_order(invert_tree(build_tree([2, 1, 3]))))              # -> [2, 3, 1]
    print(level_order(invert_tree(build_tree([]))))                    # -> []
