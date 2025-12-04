"""
Problem: Maximum in Sliding Window

You are given an array of integers `nums` and an integer `k`. 
A sliding window of size `k` moves from left to right across the array. 
At each step, you should return the maximum value inside the current window.

Return a list of maximums for each sliding window position.

Example:
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]

Explanation:
Window positions:
[1,3,-1],-3,5,3,6,7 → max = 3
1,[3,-1,-3],5,3,6,7 → max = 3
1,3,[-1,-3,5],3,6,7 → max = 5
1,3,-1,[-3,5,3],6,7 → max = 5
1,3,-1,-3,[5,3,6],7 → max = 6
1,3,-1,-3,5,[3,6,7] → max = 7


-----------------------------------
Solution:
We use a deque (double-ended queue) to store indices of useful elements 
in the current window:
- Maintain indices in decreasing order of values.
- The front of deque always holds the index of the maximum element.
- Pop elements from the back if they are smaller than the current element.
- Remove indices from the front if they fall outside the window.

-----------------------------------
Time Complexity:
- O(N), where N = len(nums), since each element is added and removed from the deque at most once.

Space Complexity:
- O(K), for storing indices in the deque.
"""

from collections import deque
from typing import List

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if not nums or k == 0:
            return []
        
        dq = deque()  # stores indices of useful elements
        res = []
        
        for i in range(len(nums)):
            # Remove elements out of this window
            while dq and dq[0] <= i - k:
                dq.popleft()
            
            # Remove smaller values as they are useless
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()
            
            dq.append(i)
            
            # The first index where window is fully formed
            if i >= k - 1:
                res.append(nums[dq[0]])
        
        return res


# -------------------------
# Test Cases
# -------------------------
if __name__ == "__main__":
    sol = Solution()

    print("Test Case 1:")
    print(sol.maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3))  
    print("Expected: [3,3,5,5,6,7]")

    print("\nTest Case 2:")
    print(sol.maxSlidingWindow([1], 1)) 
    print("Expected: [1]")

    print("\nTest Case 3:")
    print(sol.maxSlidingWindow([9,11], 2)) 
    print("Expected: [11]")

    print("\nTest Case 4:")
    print(sol.maxSlidingWindow([4,-2], 2))
    print("Expected: [4]")

    print("\nTest Case 5:")
    print(sol.maxSlidingWindow([1,3,1,2,0,5], 3))
    print("Expected: [3,3,2,5]")
