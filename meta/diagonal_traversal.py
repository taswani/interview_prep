"""
LeetCode 1424: Diagonal Traverse II

Problem Description:
---------------------
Given a 2D integer array nums (jagged array), return all elements of nums in diagonal order.

Diagonal order means traversing the array along diagonals from top-left to bottom-right. Within each diagonal, elements are ordered from bottom-left to top-right (i.e., larger row index first).

Solution:
---------
- Group elements by their diagonal index i + j.
- Track the maximum diagonal index.
- Loop through diagonal indices from 0 to max_diag in order and reverse each group.
- This avoids sorting the keys, achieving true O(N) time.

Time Complexity:
----------------
O(N) - N is the total number of elements.

Space Complexity:
-----------------
O(N) - for the dictionary and result list.
"""

from collections import defaultdict

class Solution:
    def findDiagonalOrder(self, nums):
        diagonals = defaultdict(list)
        max_diag = 0
        
        # Populate the dictionary with diagonal index -> list of elements
        for i, row in enumerate(nums):
            for j, val in enumerate(row):
                diag_idx = i + j
                diagonals[diag_idx].append(val)
                max_diag = max(max_diag, diag_idx)
        
        # Flatten diagonals in order of index
        result = []
        for diag in range(max_diag + 1):
            if diag in diagonals:
                result.extend(reversed(diagonals[diag]))
        
        return result


# ---------------- Test Cases ----------------
if __name__ == "__main__":
    solution = Solution()
    
    nums1 = [
        [1,2,3],
        [4,5],
        [6,7,8,9]
    ]
    print(solution.findDiagonalOrder(nums1))  # Expected: [1,4,6,5,3,7,8,9]

    nums2 = [
        [1,2,3,4,5],
        [6,7],
        [8],
        [9,10,11],
        [12,13,14,15,16]
    ]
    print(solution.findDiagonalOrder(nums2))  # Expected: [1,6,2,8,7,3,9,4,12,10,5,13,11,14,15,16]
