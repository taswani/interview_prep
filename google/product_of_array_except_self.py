"""
Product of Array Except Self
============================

PROBLEM PROMPT
--------------
Given an integer array `nums`, return an array `answer` such that answer[i] is
equal to the product of all the elements of `nums` except nums[i].

The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit
integer.

You must write an algorithm that runs in O(n) time and WITHOUT using the
division operation.

Example 1:
    Input:  nums = [1, 2, 3, 4]
    Output: [24, 12, 8, 6]
    Explanation:
        answer[0] = 2*3*4 = 24
        answer[1] = 1*3*4 = 12
        answer[2] = 1*2*4 = 8
        answer[3] = 1*2*3 = 6

Example 2:
    Input:  nums = [-1, 1, 0, -3, 3]
    Output: [0, 0, 9, 0, 0]

Constraints:
    2 <= len(nums) <= 10^5
    -30 <= nums[i] <= 30
    The product of any prefix or suffix of nums is guaranteed to fit in a
    32-bit integer.

Follow-up:
    Can you solve the problem in O(1) extra space complexity? (The output array
    does not count as extra space for this purpose.) The solution below does.
"""


def product_except_self(nums):
    """
    Return an array where each element is the product of all others in `nums`.

    APPROACH (Prefix Products * Suffix Products, No Division)
    ---------------------------------------------------------
    The obvious idea — multiply everything, then divide by nums[i] — is banned
    (and breaks on zeros anyway). Instead, observe that the answer for index i is:

        (product of everything to the LEFT of i) * (product of everything to the
         RIGHT of i)

    So if we know, for each position, the running product of all elements before
    it and the running product of all elements after it, multiplying those two
    gives the answer without ever including nums[i] itself.

    We compute this in two passes using the output array to avoid extra space:

      Pass 1 (left -> right): fill answer[i] with the product of all elements
      strictly to the LEFT of i. answer[0] has nothing to its left, so it's 1.

      Pass 2 (right -> left): keep a running product `right` of all elements
      strictly to the RIGHT of i, and multiply it into answer[i] (which already
      holds the left product). answer[last] has nothing to its right, so `right`
      starts at 1.

    After both passes, answer[i] = (left product) * (right product) = product of
    every element except nums[i]. Zeros are handled naturally: an index whose
    only zero lies to one side gets a 0 from that side's product, and the single
    index that IS the zero gets the product of all the (nonzero) others.

    COMPLEXITY
    ----------
    Time  : O(n) — two linear passes over the array, each doing O(1) work per
            element.
    Space : O(1) extra — aside from the output array (which the problem excludes
            from the space count), we use only a single scalar running product.
            No division is used.

    Args:
        nums (list[int]): The input array.

    Returns:
        list[int]: answer[i] = product of all nums except nums[i].
    """
    n = len(nums)
    answer = [1] * n

    # Pass 1: answer[i] becomes the product of everything to the LEFT of i.
    # `left` is the running product of elements seen before index i.
    left = 1
    for i in range(n):
        answer[i] = left      # product of nums[0..i-1]
        left *= nums[i]       # extend the running left product to include nums[i]

    # Pass 2: multiply in the product of everything to the RIGHT of i.
    # `right` is the running product of elements seen after index i.
    right = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= right    # combine left product (already stored) with right
        right *= nums[i]      # extend the running right product to include nums[i]

    return answer


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(product_except_self([1, 2, 3, 4]))         # -> [24, 12, 8, 6]
    print(product_except_self([-1, 1, 0, -3, 3]))    # -> [0, 0, 9, 0, 0]
    print(product_except_self([2, 3]))               # -> [3, 2]
    print(product_except_self([0, 0]))               # -> [0, 0] (two zeros)
    print(product_except_self([5, 0]))               # -> [0, 5] (single zero)
