"""
3Sum
====

PROBLEM PROMPT
--------------
Given an integer array `nums`, return all the triplets
[nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and
nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
    Input:  nums = [-1, 0, 1, 2, -1, -4]
    Output: [[-1, -1, 2], [-1, 0, 1]]
    Explanation:
        nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
        nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
        nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
        The distinct triplets are [-1, 0, 1] and [-1, -1, 2].
        Notice that the order of the output and the order of the triplets
        does not matter.

Example 2:
    Input:  nums = [0, 1, 1]
    Output: []
    Explanation: The only possible triplet does not sum up to 0.

Example 3:
    Input:  nums = [0, 0, 0]
    Output: [[0, 0, 0]]
    Explanation: The only possible triplet sums up to 0.

Constraints:
    3 <= len(nums) <= 3000
    -10^5 <= nums[i] <= 10^5
"""


def three_sum(nums):
    """
    Return all unique triplets in `nums` that sum to zero.

    APPROACH (Sort + Two Pointers)
    ------------------------------
    A brute-force check of every triple would be O(n^3). We can do much better
    by first SORTING the array, which unlocks two things: a fast two-pointer
    scan, and an easy way to skip duplicates.

    We fix one number at a time (call it the "anchor" at index i) and then look
    for two other numbers to its right that sum to -nums[i] (so all three add to
    zero). Because the array is sorted, we can find those two numbers with the
    classic two-pointer technique:

        left  starts just after the anchor
        right starts at the end of the array

      - If nums[left] + nums[right] is too small, we need a bigger sum, so move
        `left` rightward (to a larger value).
      - If it's too big, move `right` leftward (to a smaller value).
      - If it equals the target, we've found a valid triplet.

    Avoiding duplicates (the tricky part):
      - Skip an anchor value identical to the previous anchor — it would only
        reproduce triplets we already generated.
      - After recording a triplet, advance `left`/`right` past any values equal
        to the ones just used, so we don't emit the same triplet twice.

    Early exit: once the anchor value is greater than 0, no triplet can sum to
    zero (all remaining numbers are >= the anchor and thus positive), so we stop.

    COMPLEXITY
    ----------
    Time  : O(n^2) — sorting is O(n log n), then for each of the n anchors the
            two-pointer scan is O(n), giving O(n^2) overall (which dominates).
    Space : O(1) extra (or O(n) depending on the sort implementation), not
            counting the output list. Only a constant number of pointers is used
            beyond the space needed to hold the answer.

    Args:
        nums (list[int]): The input array of integers.

    Returns:
        list[list[int]]: All unique triplets that sum to zero.
    """
    # Sorting enables the two-pointer scan and makes duplicate-skipping easy.
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n):
        # Once the anchor is positive, the two larger numbers to its right are
        # also positive, so the sum can never reach zero. Stop entirely.
        if nums[i] > 0:
            break

        # Skip a repeated anchor value to avoid producing duplicate triplets.
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Two-pointer search over the subarray to the right of the anchor.
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total < 0:
                # Sum too small — need a larger value, so move `left` up.
                left += 1
            elif total > 0:
                # Sum too big — need a smaller value, so move `right` down.
                right -= 1
            else:
                # Found a triplet that sums to zero.
                result.append([nums[i], nums[left], nums[right]])

                # Move both pointers inward past the values we just used, then
                # skip any duplicates so the same triplet isn't recorded again.
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

    return result


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(three_sum([-1, 0, 1, 2, -1, -4]))  # -> [[-1, -1, 2], [-1, 0, 1]]
    print(three_sum([0, 1, 1]))              # -> []
    print(three_sum([0, 0, 0]))              # -> [[0, 0, 0]]
    print(three_sum([-2, 0, 0, 2, 2]))       # -> [[-2, 0, 2]] (duplicate handling)
