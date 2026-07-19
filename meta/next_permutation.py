"""
Problem: Next Permutation

Implement the next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers.

If such arrangement is not possible, it must rearrange it as the lowest possible order (i.e., sorted in ascending order).

The replacement must be in-place and use only constant extra memory.

Example 1:
Input: [1,2,3]
Output: [1,3,2]

Example 2:
Input: [3,2,1]
Output: [1,2,3]

Example 3:
Input: [1,1,5]
Output: [1,5,1]
"""

from typing import List

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        if n <= 1:
            return nums
        
        i = n - 2

        while i >= 0 and nums[i] > nums[i + 1]:
            i -= 1
        
        j = n - 1

        if i >= 0:
            while nums[j] < nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        
        left, right = i + 1, n - 1

        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
        


"""
Time Complexity:
- Step 1: O(n) to find the pivot
- Step 2: O(n) to find the element to swap
- Step 4: O(n) to reverse the suffix
- Total: O(n), where n = len(nums)

Space Complexity:
- In-place swaps only, constant extra space: O(1)
"""

# ------------------------
# Test cases
# ------------------------
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1 = [1, 2, 3]
    solution.nextPermutation(nums1)
    print("Test 1:", nums1, "Expected: [1,3,2]")

    # Test Case 1.5
    nums1_5 = [1, 2, 3, 4, 5]
    solution.nextPermutation(nums1_5)
    print("Test 1.5:", nums1_5, "Expected: [1, 2, 3, 5, 4]")

    # Test Case 2
    nums2 = [3, 2, 1]
    solution.nextPermutation(nums2)
    print("Test 2:", nums2, "Expected: [1,2,3]")

    # Test Case 3
    nums3 = [1, 1, 5]
    solution.nextPermutation(nums3)
    print("Test 3:", nums3, "Expected: [1,5,1]")

    # Test Case 4: longer array
    nums4 = [1, 3, 2, 4]
    solution.nextPermutation(nums4)
    print("Test 4:", nums4, "Expected: [1,3,4,2]")

    # Test Case 5: already largest permutation
    nums5 = [5, 4, 3, 2, 1]
    solution.nextPermutation(nums5)
    print("Test 5:", nums5, "Expected: [1,2,3,4,5]")

    # Test Case 6: single element
    nums6 = [1]
    solution.nextPermutation(nums6)
    print("Test 6:", nums6, "Expected: [1]")
