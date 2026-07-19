"""
LeetCode 862: Shortest Subarray with Sum at Least K

---------------------------------------------------
Problem:
Given an integer array nums and an integer k, return the length 
of the shortest non-empty subarray of nums with a sum at least k.
If no such subarray exists, return -1.

---------------------------------------------------
Intuition:
We use prefix sums to represent subarray sums as differences:
    subarray(i..j) = P[j] - P[i]
We want the shortest j - i such that P[j] - P[i] >= k.

We maintain a deque of candidate start indices:
- Pop from the front if it forms a valid subarray with the current j.
  (This checks shortest subarrays ending at j.)
- Pop from the back if the new prefix sum is smaller/equal,
  because earlier larger sums are "worse" and can never help.

---------------------------------------------------
Time Complexity:
- Each index is added once and removed once → O(n).

Space Complexity:
- We store prefix sums and the deque → O(n).

---------------------------------------------------
"""

from collections import deque
from typing import List

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # prefix sums
        P = [0]
        for num in nums:
            P.append(P[-1] + num)

        ans = n + 1
        dq = deque()  # will store indices of P

        for j in range(len(P)):
            # Pop from front while valid
            while dq and P[j] - P[dq[0]] >= k:
                ans = min(ans, j - dq[0])
                dq.popleft()

            # Pop from back while current prefix is smaller/equal
            while dq and P[j] <= P[dq[-1]]:
                dq.pop()

            dq.append(j)

        return ans if ans <= n else -1


# ---------------------------------------------------
# Test Cases
# ---------------------------------------------------
if __name__ == "__main__":
    sol = Solution()

    # Example 1
    nums1 = [1]
    k1 = 1
    print("Test 1:", sol.shortestSubarray(nums1, k1))  # Expected: 1

    # Example 2
    nums2 = [1, 2]
    k2 = 4
    print("Test 2:", sol.shortestSubarray(nums2, k2))  # Expected: -1

    # Example 3
    nums3 = [2, -1, 2]
    k3 = 3
    print("Test 3:", sol.shortestSubarray(nums3, k3))  # Expected: 3

    # Bigger Example
    nums4 = [84, -37, 32, 40, 95]
    k4 = 167
    print("Test 4:", sol.shortestSubarray(nums4, k4))  # Expected: 3
