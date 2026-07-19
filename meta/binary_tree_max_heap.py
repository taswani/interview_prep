"""
=====================================================
🏰 Problem: Is a Binary Tree a Heap?
=====================================================

🧩 Problem Statement:
Given the root of a binary tree, determine whether it satisfies
the properties of a *max-heap*.

A binary tree is a max-heap if:
1. It is a **complete binary tree (CBT)** — all levels are fully
   filled except possibly the last, which is filled from left to right.
2. It satisfies the **heap property** — every node's value is
   greater than or equal to its children’s values.

-----------------------------------------------------
💡 Intuition:
We need to check both:
1️⃣ Completeness → via level-order traversal (BFS).
   Once we find a None child, all following nodes must be None.
2️⃣ Heap property → every node >= its children.

If either property fails, the tree is not a heap.

-----------------------------------------------------
⚙️ Approach (BFS):
1. If tree is empty, return True.
2. Use a queue to traverse the tree level by level.
3. Track a flag `found_none = False`.
4. For each node:
   - If left or right child violates heap order, return False.
   - If a None child is found, mark `found_none = True`.
   - If a non-null node is found *after* `found_none = True`,
     completeness is broken → return False.
5. If traversal completes, return True.

-----------------------------------------------------
⏱️ Time Complexity:  O(n)   — each node is visited once
💾 Space Complexity: O(n)   — queue for BFS traversal
=====================================================
"""

from collections import deque


# -----------------------------------------------------
# 🧱 TreeNode Definition
# -----------------------------------------------------
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# -----------------------------------------------------
# ⚙️ Function: isHeap
# -----------------------------------------------------
def isHeap(root: TreeNode) -> bool:
    """
    Check whether a binary tree satisfies the properties of a max-heap.
    """
    if not root:
        return True

    queue = deque([root])
    found_none = False

    while queue:
        node = queue.popleft()

        # ---- LEFT CHILD ----
        if node.left:
            if found_none:
                # A non-null node appears after a missing one
                return False
            if node.left.val > node.val:
                # Heap property violated
                return False
            queue.append(node.left)
        else:
            found_none = True

        # ---- RIGHT CHILD ----
        if node.right:
            if found_none:
                return False
            if node.right.val > node.val:
                return False
            queue.append(node.right)
        else:
            found_none = True

    return True


# -----------------------------------------------------
# 🧪 Test Cases
# -----------------------------------------------------
if __name__ == "__main__":
    # ✅ Example 1: Valid max heap
    root = TreeNode(10,
                    TreeNode(9,
                             TreeNode(7),
                             TreeNode(6)),
                    TreeNode(8))
    print("Test 1:", isHeap(root))  # ✅ True

    # ❌ Example 2: Violates heap order
    root2 = TreeNode(10,
                     TreeNode(15),  # 15 > 10 → violates max-heap
                     TreeNode(8))
    print("Test 2:", isHeap(root2))  # ❌ False

    # ❌ Example 3: Incomplete tree
    root3 = TreeNode(10,
                     TreeNode(9),
                     None)
    root3.left.left = TreeNode(8)  # Missing right before filling next level
    print("Test 3:", isHeap(root3))  # ❌ False

    # ✅ Example 4: Single node
    print("Test 4:", isHeap(TreeNode(5)))  # ✅ True

    # ✅ Example 5: Perfect heap
    root4 = TreeNode(100,
                     TreeNode(50,
                              TreeNode(20),
                              TreeNode(10)),
                     TreeNode(30,
                              TreeNode(5),
                              TreeNode(1)))
    print("Test 5:", isHeap(root4))  # ✅ True
