"""
Problem: Complete Binary Tree

A complete binary tree is a binary tree in which every level, except possibly the last, 
is completely filled, and all nodes are as far left as possible.

Write a function to determine if a given binary tree is complete.

Example 1:

Input:
        1
       / \
      2   3
     / \  /
    4  5 6

Output: True

Example 2:

Input:
        1
       / \
      2   3
     / \   \
    4  5    7

Output: False
"""

from typing import Optional
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isCompleteTree(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        queue = deque([root])
        end = False  # flag indicating we should see no more children

        while queue:
            node = queue.popleft()

            if node:
                if end:
                    # If we already saw a null node, then any non-null node violates completeness
                    return False
                queue.append(node.left)
                queue.append(node.right)
            else:
                # Encountered a null node, set flag
                end = True

        return True


"""
Time Complexity:
- We traverse each node once in BFS.
- For n nodes, Time Complexity = O(n)

Space Complexity:
- Queue can hold up to O(n) nodes in the last level.
- Space Complexity = O(n)
"""


# ------------------------
# Test cases
# ------------------------
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1: Complete tree
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.left.left = TreeNode(4)
    root1.left.right = TreeNode(5)
    root1.right.left = TreeNode(6)
    print("Test 1:", solution.isCompleteTree(root1), "Expected: True")

    # Test Case 2: Not complete
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(3)
    root2.left.left = TreeNode(4)
    root2.left.right = TreeNode(5)
    root2.right.right = TreeNode(7)
    print("Test 2:", solution.isCompleteTree(root2), "Expected: False")

    # Test Case 3: Single node
    root3 = TreeNode(1)
    print("Test 3:", solution.isCompleteTree(root3), "Expected: True")

    # Test Case 4: Empty tree
    root4 = None
    print("Test 4:", solution.isCompleteTree(root4), "Expected: True")

    # Test Case 5: Last level not filled from left
    root5 = TreeNode(1)
    root5.left = TreeNode(2)
    root5.right = TreeNode(3)
    root5.left.left = TreeNode(4)
    root5.right.left = TreeNode(5)
    print("Test 5:", solution.isCompleteTree(root5), "Expected: False")
