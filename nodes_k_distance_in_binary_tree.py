"""
Problem: All Nodes Distance K in Binary Tree (LeetCode 863)

Given the root of a binary tree, the value of a target node, and an integer k,
return a list of the values of all nodes that have a distance k from the target node.

The distance between two nodes is the number of edges in the shortest path between them.
"""

from collections import defaultdict, deque
from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


"""
Intuition:
-----------
1. A binary tree does not give direct access to parent nodes.
   To handle "upward" traversal, we first build an undirected graph
   representation of the tree (node <-> parent and node <-> children).

2. Once we have the graph, the problem reduces to:
   "Find all nodes at BFS distance k from the target node."

3. Perform a BFS starting at the target node.
   Track visited nodes to avoid cycles.
   Stop when we reach distance k.

Time Complexity:
----------------
- Building graph: O(N), where N is the number of nodes.
- BFS traversal: O(N), each node visited at most once.
Total: O(N)

Space Complexity:
-----------------
- Graph storage: O(N)
- BFS queue and visited set: O(N)
Total: O(N)
"""

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        if not root:
            return []

        # Step 1: Build undirected graph representation
        graph = defaultdict(list)

        def build_graph(node, parent=None):
            if not node:
                return
            if parent:
                graph[node].append(parent)
                graph[parent].append(node)
            build_graph(node.left, node)
            build_graph(node.right, node)

        build_graph(root)

        # Step 2: BFS from target
        res = []
        queue = deque([(target, 0)])
        visited = {target}

        while queue:
            node, dist = queue.popleft()
            if dist == k:
                res.append(node.val)
            elif dist < k:
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))

        return res


# ------------------ TEST CASES ------------------

def build_tree():
    """
    Build the example tree:
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4
    """
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)
    return root

if __name__ == "__main__":
    tree = build_tree()
    sol = Solution()
    target = tree.left  # Node with value 5
    print("Test 1:", sol.distanceK(tree, target, 2))  # Expected [7,4,1]

    target = tree.right  # Node with value 1
    print("Test 2:", sol.distanceK(tree, target, 1))  # Expected [3,0,8]

    target = tree  # Node with value 3
    print("Test 3:", sol.distanceK(tree, target, 3))  # Expected [7,4]
