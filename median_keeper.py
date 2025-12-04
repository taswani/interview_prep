"""
LeetCode 295: Find Median from Data Stream

Problem Description:
--------------------
The median is the middle value in an ordered list of integers. 
If the size of the list is even, the median is the average of the two middle values.

Implement a data structure that supports the following operations:
1. addNum(int num) - Inserts a number into the data structure.
2. findMedian() - Returns the median of all numbers inserted so far.

Constraints:
------------
- At most 5 * 10^4 calls will be made to addNum and findMedian.
- -10^5 <= num <= 10^5

Example:
--------
Input:
    ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
    [[], [1], [2], [], [3], []]
Output:
    [null, null, null, 1.5, null, 2.0]

Explanation:
    MedianFinder medianFinder = new MedianFinder();
    medianFinder.addNum(1);    // arr = [1]
    medianFinder.addNum(2);    // arr = [1, 2]
    medianFinder.findMedian(); // return 1.5
    medianFinder.addNum(3);    // arr = [1, 2, 3]
    medianFinder.findMedian(); // return 2.0
"""

import heapq


class MedianFinder:
    def __init__(self):
        # max-heap for the smaller half (stored as negatives)
        self.low = []
        # min-heap for the larger half
        self.high = []

    def addNum(self, num: int) -> None:
        # Step 1: add to max-heap (invert sign for max behavior)
        heapq.heappush(self.low, -num)

        # Step 2: ensure ordering between low and high
        heapq.heappush(self.high, -heapq.heappop(self.low))

        # Step 3: balance sizes (low can have 1 more element than high)
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self) -> float:
        # Odd number of elements → top of max-heap
        if len(self.low) > len(self.high):
            return -self.low[0]
        # Even number of elements → average of tops
        return (-self.low[0] + self.high[0]) / 2


# ---------------------------------------------------
# Time and Space Complexity:
# ---------------------------------------------------
# - addNum(): O(log n) due to heap push/pop
# - findMedian(): O(1)
# - Space Complexity: O(n) to store all elements in heaps
# ---------------------------------------------------

# ---------------- Test Cases ----------------
if __name__ == "__main__":
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    print(mf.findMedian())  # Expected 1.5
    mf.addNum(3)
    print(mf.findMedian())  # Expected 2.0

    # Additional tests
    mf2 = MedianFinder()
    nums = [5, 15, 1, 3]
    for num in nums:
        mf2.addNum(num)
        print(f"Added {num}, current median: {mf2.findMedian()}")

    # Edge case: single element
    mf3 = MedianFinder()
    mf3.addNum(42)
    print(mf3.findMedian())  # Expected 42
