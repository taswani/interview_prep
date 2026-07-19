"""
Problem: Binary Search Tree Iterator

Implement an iterator over a binary search tree (BST). Your iterator should be initialized with the root node of a BST and should support the following operations:

    1. next() - returns the next smallest number in the BST.
    2. hasNext() - returns True if there exists a next number in the iterator.

Intuition:
    - A BST's in-order traversal gives nodes in ascending order.
    - We can simulate in-order traversal using a stack:
        - Always push the leftmost path of the current node onto the stack.
        - When calling next(), pop the top node (next smallest), and push its right child's leftmost path onto the stack.
    - This way, the stack always contains the "next nodes" to return in order.

Time Complexity:
    - next(): Average O(1) amortized, O(h) worst case (h = tree height)
    - hasNext(): O(1)
    - Initialization (__init__): O(h)
Space Complexity:
    - O(h) for the stack
"""

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    def __init__(self, root: Optional[TreeNode]):
        # Stack to simulate in-order traversal
        self.stack = []
        self.__push_left(root)

    def __push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        if not self.hasNext:
            return None
        
        node = self.stack.pop()
        val = node.val

        if node.right:
            self.__push_left(node.right)

        return val

    def hasNext(self) -> bool:
        return len(self.stack) > 0


# -----------------------------
# Test Cases
# -----------------------------
if __name__ == "__main__":
    # Build BST:
    #        7
    #       / \
    #      3   15
    #          / \
    #         9   20
    root = TreeNode(7)
    root.left = TreeNode(3)
    root.right = TreeNode(15, TreeNode(9), TreeNode(20))

    iterator = BSTIterator(root)
    results = []
    while iterator.hasNext():
        results.append(iterator.next())
    
    print("BST Iterator output (in-order traversal):", results)
    # Expected: [3, 7, 9, 15, 20]

    # Test hasNext on empty iterator
    empty_iterator = BSTIterator(None)
    print("Has next on empty BST:", empty_iterator.hasNext())  # Expected: False
