"""
Two Sum
=======

PROBLEM PROMPT
--------------
Given an array of integers `nums` and an integer `target`, return the indices
of the two numbers such that they add up to `target`.

You may assume that each input has exactly one solution, and you may not use
the same element twice. You can return the answer in any order.

Example:
    Input:  nums = [2, 7, 11, 15], target = 9
    Output: [0, 1]          # because nums[0] + nums[1] == 2 + 7 == 9

Constraints:
    2 <= len(nums) <= 10^4
    -10^9 <= nums[i] <= 10^9
    -10^9 <= target <= 10^9
    Exactly one valid answer exists.
"""


def two_sum(nums, target):
    """
    Return the indices of the two numbers in `nums` that add up to `target`.

    APPROACH (Hash Map / One-Pass)
    ------------------------------
    For each number `n` we need to find its "complement" — the value that,
    when added to `n`, equals `target` (i.e. complement = target - n).

    Instead of scanning the rest of the array to look for that complement
    (which would be an O(n^2) brute-force pair check), we remember every
    number we've already seen in a hash map that maps:

        value -> index

    As we walk the array once, we ask: "Have I already seen the complement
    I need?" A hash map answers that question in O(1) average time. If yes,
    we've found our pair and return both indices. If no, we store the current
    number and continue. Because a solution is guaranteed to exist, the loop
    is certain to return before it ends.

    COMPLEXITY
    ----------
    Time  : O(n) — we traverse the list of n elements exactly once, and each
            hash-map lookup/insert is O(1) on average.
    Space : O(n) — in the worst case we store almost every element in the
            hash map before finding the matching pair.

    Args:
        nums (list[int]): List of integers to search.
        target (int): The target sum.

    Returns:
        list[int]: The two indices whose values sum to `target`.
    """
    # Maps each number we've already seen to the index where it appeared.
    seen = {}

    # enumerate gives us both the index and the value on each iteration.
    for index, num in enumerate(nums):
        # The value we still need in order to reach `target`.
        complement = target - num

        # If we've seen the complement before, we have our answer.
        # Its stored index comes first because we encountered it earlier.
        if complement in seen:
            return [seen[complement], index]

        # Otherwise, record the current number and its index for later lookups.
        seen[num] = index

    # Per the problem's constraints this line is never reached, but we return
    # an empty list to make the "no solution" case explicit.
    return []


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(two_sum([2, 7, 11, 15], 9))  # -> [0, 1]
    print(two_sum([3, 2, 4], 6))       # -> [1, 2]
    print(two_sum([3, 3], 6))          # -> [0, 1]
