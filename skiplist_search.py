"""
Problem: Skip List Search

A Skip List is a data structure that allows fast search, insertion, and deletion 
operations within an ordered sequence of elements, similar to a balanced tree 
but using probabilistic balancing.

Each node may have multiple forward pointers at different "levels."
When searching for a value, we start from the highest level and move forward 
until we would overshoot. Then we drop down one level and repeat until 
we reach level 0.

Your task: Implement a SkipList with the following methods:
- search(target): return True if target exists in the skiplist.
- add(num): insert num into the skiplist.
- erase(num): remove one occurrence of num from the skiplist, return True if removed.

The Skip List should maintain average O(log n) time complexity for these operations.
"""

import random


class Node:
    """Node for the skip list."""
    def __init__(self, val: int, level: int):
        self.val = val
        # forward pointers for each level
        self.next = [None] * (level + 1)


class SkipList:
    """Skip List implementation."""
    MAX_LEVEL = 16  # maximum number of levels

    def __init__(self):
        self.head = Node(-1, self.MAX_LEVEL)  # dummy head
        self.level = 0  # current highest level

    def random_level(self):
        """Randomly generate level for a new node."""
        lvl = 0
        while random.random() < 0.5 and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def search(self, target: int) -> bool:
        curr = self.head
        # Start from top level down to 0
        for i in range(self.level, -1, -1):
            while curr.next[i] and curr.next[i].val < target:
                curr = curr.next[i]
        curr = curr.next[0]
        return curr is not None and curr.val == target

    def add(self, num: int) -> None:
        update = [None] * (self.MAX_LEVEL + 1)
        curr = self.head
        # Track nodes that need to be updated at each level
        for i in range(self.level, -1, -1):
            while curr.next[i] and curr.next[i].val < num:
                curr = curr.next[i]
            update[i] = curr

        # Choose a random level for the new node
        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.head
            self.level = lvl

        new_node = Node(num, lvl)
        for i in range(lvl + 1):  # important: lvl + 1 because levels are 0-indexed
            new_node.next[i] = update[i].next[i]
            update[i].next[i] = new_node

    def erase(self, num: int) -> bool:
        update = [None] * (self.MAX_LEVEL + 1)
        curr = self.head
        for i in range(self.level, -1, -1):
            while curr.next[i] and curr.next[i].val < num:
                curr = curr.next[i]
            update[i] = curr

        curr = curr.next[0]
        if not curr or curr.val != num:
            return False

        for i in range(self.level + 1):
            if update[i].next[i] != curr:
                continue
            update[i].next[i] = curr.next[i]

        # Adjust list level if necessary
        while self.level > 0 and self.head.next[self.level] is None:
            self.level -= 1
        return True


# ------------------------
# Test cases
# ------------------------
if __name__ == "__main__":
    skiplist = SkipList()

    # Insert numbers
    skiplist.add(1)
    skiplist.add(2)
    skiplist.add(3)

    print("Search 0 (expect False):", skiplist.search(0))  # False
    skiplist.add(4)
    print("Search 1 (expect True):", skiplist.search(1))   # True

    # More inserts
    for num in [5, 6, 7, 8, 9, 10]:
        skiplist.add(num)

    print("Search 10 (expect True):", skiplist.search(10))
