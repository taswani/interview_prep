"""
Problem: Print Trees by Column (Vertical Order Traversal)

Given the root of a binary tree, print the nodes of the tree column by column. 
Nodes that are in the same vertical column (based on horizontal distance from the root) 
should be grouped together.

Definition of horizontal distance (HD):
- The root node has HD = 0.
- For any node:
  - Its left child has HD = parent HD - 1
  - Its right child has HD = parent HD + 1

Example:
Input:
        3
       / \
      9   8
     / \ / \
    4  0 1  7

Output (by columns, left to right):
[[4], [9], [3, 0, 1], [8], [7]]

Explanation:
- Column -2 → [4]
- Column -1 → [9]
- Column  0 → [3, 0, 1]
- Column  1 → [8]
- Column  2 → [7]


-----------------------------------
Solution Approach:
1. Perform BFS traversal while keeping track of each node's column index.
2. Use a dictionary (column_index → list of nodes).
3. Track the minimum and maximum column indices encountered.
4. At the end, collect the columns from min to max into the result list.

-----------------------------------
Time Complexity:
- O(N), where N is the number of nodes, since each node is visited exactly once.

Space Complexity:
- O(N), for storing the dictionary of columns and the BFS queue.
"""

from collections import defaultdict, deque

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def verticalOrder(self, root: TreeNode):
        if not root:
            return []
        
        # Dictionary to store column index → list of values
        col_table = defaultdict(list)
        # Queue for BFS: (node, column_index)
        queue = deque([(root, 0)])
        
        min_col = max_col = 0
        
        while queue:
            node, col = queue.popleft()
            if node:
                col_table[col].append(node.val)
                min_col = min(min_col, col)
                max_col = max(max_col, col)
                
                # Left child goes to col - 1
                if node.left:
                    queue.append((node.left, col - 1))
                # Right child goes to col + 1
                if node.right:
                    queue.append((node.right, col + 1))
        
        # Collect results from min_col to max_col
        return [col_table[x] for x in range(min_col, max_col + 1)]


# -------------------------
# Test Cases
# -------------------------
if __name__ == "__main__":
    sol = Solution()

    # Example tree
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(8)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(0)
    root.right.left = TreeNode(1)
    root.right.right = TreeNode(7)

    print("Test Case 1:")
    print(sol.verticalOrder(root))  
    print("Expected: [[4], [9], [3, 0, 1], [8], [7]]")

    # Single node
    print("\nTest Case 2:")
    root2 = TreeNode(1)
    print(sol.verticalOrder(root2))  
    print("Expected: [[1]]")

    # Left skewed tree
    print("\nTest Case 3:")
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    root3.left.left = TreeNode(3)
    print(sol.verticalOrder(root3))  
    print("Expected: [[3], [2], [1]]")

    # Right skewed tree
    print("\nTest Case 4:")
    root4 = TreeNode(1)
    root4.right = TreeNode(2)
    root4.right.right = TreeNode(3)
    print(sol.verticalOrder(root4))  
    print("Expected: [[1], [2], [3]]")
