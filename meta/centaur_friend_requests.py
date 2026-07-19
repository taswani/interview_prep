"""
Problem: Centaur Friend Requests
--------------------------------
A group of centaurs (mythical half-human, half-horse creatures) all sign up for Facebook accounts. 
They send friend requests under the following rules:

1. A centaur of age x will only send a request to another centaur of age y if:
   - y >= (x / 2 + 7)

2. A centaur will not send a request to someone older:
   - y <= x

3. A centaur older than 100 will not send a request to someone under 100.
   - But centaurs under 100 can still befriend each other.

Return the total number of friend requests sent.

------------------------------------------------
Intuition
---------
This is a variation of LeetCode 825 (Friends of Appropriate Ages).
Naive O(n^2) checking of every pair (x, y) is too slow for large n.

Optimized approach:
1. Sort ages.
2. For each age x:
   - Use two pointers (left, right) to find the valid interval of ages y that satisfy the rules.
   - Count how many y fall inside that interval.
   - Apply rule (3): if x > 100, exclude all y < 100.
3. Add up all valid counts.

This works because sorting lets us efficiently "window" valid ages using monotonic two-pointer moves.

------------------------------------------------
Time Complexity
---------------
- Sorting: O(n log n)
- Two-pointer scan: O(n)
Overall: O(n log n)

Space Complexity: O(1) (in-place pointers)

------------------------------------------------
"""

from typing import List


def numCentaurRequests(ages: List[int]) -> int:
    ages.sort()
    n = len(ages)
    total = 0
    left = 0
    right = 0

    for i, age in enumerate(ages):
        if age < 15:  # under 15 → can't send requests (fails rule 1)
            continue

        # Rule 1: must be >= age/2 + 7
        while left < n and ages[left] < (0.5 * age + 7):
            left += 1

        # Rule 2: must be <= age
        while right < n and ages[right] <= age:
            right += 1

        # Count valid candidates in [left, right-1], excluding self
        count = right - left - 1

        # Rule 3: if x > 100, exclude anyone under 100
        if age > 100:
            # move a cutoff pointer to first index >= 100
            cutoff = 0
            while cutoff < n and ages[cutoff] < 100:
                cutoff += 1
            count = max(0, right - max(left, cutoff) - 1)

        total += count

    return total


# ------------------------------------------------
# Test Cases
# ------------------------------------------------
if __name__ == "__main__":
    tests = [
        ([16, 16], 2),              # each 16 can befriend the other
        ([20, 30, 100, 110, 120], 3), # 110->100, 120->100, 120->110
        ([200, 120, 150, 99, 101, 80], 6), # test rule 3 cutoff
        ([14, 14, 14], 0),          # all too young
        ([99, 101], 0),             # 101 cannot friend 99 due to rule 3
        ([105, 110, 120], 3),       # each can friend younger 100+ centaurs
    ]

    for ages, expected in tests:
        result = numCentaurRequests(ages)
        print(f"ages={ages} => {result} (expected {expected})")
