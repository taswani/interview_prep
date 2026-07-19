"""
Problem: Local Minimum in an Array

Description:
You are given an array `nums` of distinct integers. A local minimum is defined as
an element that is strictly smaller than its neighbors. For the edge elements,
a local minimum is one that is smaller than its single neighbor.

Write a function `findLocalMin(nums)` that returns the index of any local minimum.
You may assume that at least one local minimum always exists.

Example:
    Input: [9, 7, 2, 8, 5]
    Output: 2
    Explanation: nums[2] = 2 is smaller than both neighbors (7 and 8).

Constraints:
- The input array contains distinct integers.
- Array length n >= 1.
- At least one local minimum exists.

-------------------------------------------------------------------------------
Solution Approach:
We can use a modified binary search:
1. Pick the middle element mid.
2. If nums[mid] is a local minimum → return mid.
3. If nums[mid] > nums[mid-1], then a local minimum exists on the left side.
4. Otherwise, search on the right side.
This works because the slope changes ensure a dip (local minimum) exists.

-------------------------------------------------------------------------------
Time Complexity:
- O(log n) since we use binary search.
Space Complexity:
- O(1), only a few variables are used.
-------------------------------------------------------------------------------
"""

def findLocalMin(nums):
    l = 0
    r = len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] < nums[mid + 1]:
            r = mid
        else:
            l = mid + 1
    return l

# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        ([9, 7, 2, 8, 5], 2),
        ([1, 2, 3, 4, 5], 0),   # edge case, first element is local min
        ([5, 4, 3, 2, 1], 4),   # edge case, last element is local min
        ([10, 5, 11], 1),       # middle is local min
        ([3], 0),               # single element
    ]
    
    for nums, expected in test_cases:
        result = findLocalMin(nums)
        print(f"Array: {nums}, Local Min Index: {result}, Expected: {expected}")
