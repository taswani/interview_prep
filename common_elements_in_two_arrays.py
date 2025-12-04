"""
LeetCode 2956: Find Common Elements Between Two Arrays

Problem:
You are given two 0-indexed integer arrays `nums1` and `nums2` of sizes `n` and `m`, respectively.

Compute two values:
1. The number of indices i (0 ≤ i < n) such that nums1[i] occurs at least once in nums2.
2. The number of indices i (0 ≤ i < m) such that nums2[i] occurs at least once in nums1.

Return a list answer of size 2: [count1, count2].

This script provides a simple O(n + m) solution using hash sets,
and includes test cases you can run directly.
"""

from typing import List

class Solution:
    def findIntersectionValues(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        Count how many elements in nums1 appear in nums2 (counting per-index, not distinct)
        and how many elements in nums2 appear in nums1.
        Returns [count1, count2].
        """
        set1 = set(nums1)
        set2 = set(nums2)

        count1 = 0
        for x in nums1:
            if x in set2:
                count1 += 1

        count2 = 0
        for x in nums2:
            if x in set1:
                count2 += 1

        return [count1, count2]


# Time Complexity:
# - Building sets: O(n + m)
# - Counting memberships: O(n + m)
# => Total: O(n + m)
#
# Space Complexity:
# - O(n + m) for the two sets.

# ----------------------------
# Test Cases
# ----------------------------
def run_tests():
    sol = Solution()

    # Example 1
    nums1 = [4, 3, 2, 3, 1]
    nums2 = [2, 2, 5, 2, 3, 6]
    print("Test 1:", sol.findIntersectionValues(nums1, nums2), "Expected: [3, 4]")

    # Example 2
    nums1 = [3, 4, 2, 3]
    nums2 = [1, 5]
    print("Test 2:", sol.findIntersectionValues(nums1, nums2), "Expected: [0, 0]")

    # Test with duplicates
    nums1 = [2, 2, 2]
    nums2 = [2]
    print("Test 3:", sol.findIntersectionValues(nums1, nums2), "Expected: [3, 1]")

    # No overlap
    nums1 = [1, 2, 3]
    nums2 = [4, 5, 6]
    print("Test 4:", sol.findIntersectionValues(nums1, nums2), "Expected: [0, 0]")

    # Full overlap
    nums1 = [1, 2, 3]
    nums2 = [1, 2, 3, 1]
    print("Test 5:", sol.findIntersectionValues(nums1, nums2), "Expected: [3, 3]")

    # Mixed values
    nums1 = [7, 7, 8, 9]
    nums2 = [7, 10, 9, 7]
    print("Test 6:", sol.findIntersectionValues(nums1, nums2), "Expected: [4, 3]")

if __name__ == "__main__":
    run_tests()
