"""
Problem: Longest Increasing Sequence in a Binary Tree

Given a binary tree, find the length of the longest path where each node in the path 
has a value greater than its parent node. The path must go downwards (from parent 
to child), but does not need to go through the root.

Example:

Input:
        2
       / \
      3   2
     /     \
    4       3

Output: 3
Explanation: The longest increasing path is 2 -> 3 -> 4 (length = 3)
"""

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def longestIncreasingPath(self, root: Optional[TreeNode]) -> int:
        max_length = 0

        def dfs(node, parent, length):
            nonlocal max_length
            if not node:
                return
            
            if node.val > parent.val:
                length += 1
            else:
                length = 1
            
            max_length = max(max_length, length)
            dfs(node.left, node, length)
            dfs(node.right, node, length)
        
        dfs(root, TreeNode(float("-inf")), 0)
        
        return max_length


"""
Time Complexity:
- We visit each node exactly once in DFS.
- For n nodes, Time Complexity = O(n)

Space Complexity:
- Recursive DFS stack can go up to the height of the tree.
- In the worst case (skewed tree), Space Complexity = O(n)
- Otherwise, O(log n) for balanced tree.
"""


# ------------------------
# Test cases
# ------------------------
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    root1 = TreeNode(2)
    root1.left = TreeNode(3)
    root1.right = TreeNode(2)
    root1.left.left = TreeNode(4)
    root1.right.right = TreeNode(3)
    print("Test 1:", solution.longestIncreasingPath(root1), "Expected: 3")

    # Test Case 2: single node
    root2 = TreeNode(10)
    print("Test 2:", solution.longestIncreasingPath(root2), "Expected: 1")

    # Test Case 3: all decreasing
    root3 = TreeNode(5)
    root3.left = TreeNode(4)
    root3.right = TreeNode(3)
    print("Test 3:", solution.longestIncreasingPath(root3), "Expected: 1")

    # Test Case 4: mixed
    root4 = TreeNode(1)
    root4.left = TreeNode(2)
    root4.right = TreeNode(3)
    root4.left.left = TreeNode(3)
    root4.left.right = TreeNode(4)
    root4.right.right = TreeNode(5)
    print("Test 4:", solution.longestIncreasingPath(root4), "Expected: 3")
