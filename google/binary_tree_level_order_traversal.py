"""
Binary Tree Level Order Traversal
=================================

PROBLEM PROMPT
--------------
Given the root of a binary tree, return the level order traversal of its nodes'
values. (i.e., from left to right, level by level).

Example 1:
    Input:  root = [3, 9, 20, None, None, 15, 7]

                3
              /   \
             9     20
                  /  \
                 15   7

    Output: [[3], [9, 20], [15, 7]]

Example 2:
    Input:  root = [1]
    Output: [[1]]

Example 3:
    Input:  root = []
    Output: []

Constraints:
    The number of nodes in the tree is in the range [0, 2000].
    -1000 <= Node.val <= 1000
"""

from collections import deque


class TreeNode:
    """A node in a binary tree."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val      # The value stored in this node.
        self.left = left    # Reference to the left child (or None).
        self.right = right  # Reference to the right child (or None).


def level_order(root):
    """
    Return the values of a binary tree grouped level by level, left to right.

    APPROACH (Breadth-First Search with a Queue)
    --------------------------------------------
    "Level by level, left to right" is exactly the order a breadth-first search
    (BFS) visits nodes, so we use a FIFO queue. The one extra requirement is that
    the output must be GROUPED per level, so we need to know where one level ends
    and the next begins.

    The trick is to process the queue one full level at a time. At the top of
    each iteration, the queue contains exactly the nodes of the current level.
    We snapshot how many there are (`len(queue)`) and pop precisely that many
    nodes, collecting their values into one list. As we pop each node, we enqueue
    its children — these form the *next* level and stay queued behind the current
    level's nodes, so they aren't touched until the next iteration.

    Because we captured the level's size before adding any children, the count
    cleanly separates one level from the next.

    A deque is used for the queue so that popping from the front is O(1); a plain
    list's pop(0) would be O(n) and make the whole traversal O(n^2).

    COMPLEXITY
    ----------
    Time  : O(n) — each of the n nodes is enqueued and dequeued exactly once,
            with O(1) work per node.
    Space : O(n) — the queue holds at most one full level of nodes at a time. In
            the worst case (the widest level of a full tree) that's up to ~n/2
            nodes, i.e. O(n). The output list also holds all n values.

    Args:
        root (TreeNode | None): Root of the binary tree.

    Returns:
        list[list[int]]: Node values grouped by level, top to bottom.
    """
    # An empty tree has no levels to report.
    if root is None:
        return []

    result = []
    queue = deque([root])  # Start BFS with just the root on the queue.

    while queue:
        # Number of nodes in the current level, captured BEFORE adding children.
        level_size = len(queue)
        current_level = []

        # Pop exactly the current level's nodes; enqueue their children for next.
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result


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
    print(level_order(build_tree([3, 9, 20, None, None, 15, 7])))  # -> [[3], [9, 20], [15, 7]]
    print(level_order(build_tree([1])))                            # -> [[1]]
    print(level_order(build_tree([])))                             # -> []
    print(level_order(build_tree([1, 2, 3, 4, None, None, 5])))    # -> [[1], [2, 3], [4, 5]]
