"""
Container With Most Water
=========================

PROBLEM PROMPT
--------------
You are given an integer array `height` of length n. There are n vertical lines
drawn such that the two endpoints of the i-th line are (i, 0) and (i, height[i]).

Find two lines that, together with the x-axis, form a container that holds the
most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container — the water level is limited by the
shorter of the two lines.

Example 1:
    Input:  height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    Output: 49
    Explanation: The lines at index 1 (height 8) and index 8 (height 7) form a
                 container. Its width is 8 - 1 = 7 and its height is min(8, 7) = 7,
                 so it holds 7 * 7 = 49 units of water.

Example 2:
    Input:  height = [1, 1]
    Output: 1

Constraints:
    n == len(height)
    2 <= n <= 10^5
    0 <= height[i] <= 10^4
"""


def max_area(height):
    """
    Return the maximum amount of water two lines can contain.

    APPROACH (Two Pointers)
    -----------------------
    The water held between two lines at indices `left` and `right` is:

        area = width * height = (right - left) * min(height[left], height[right])

    A brute-force check of every pair is O(n^2). Instead we use two pointers,
    one at each end of the array, giving the widest possible container to start.
    We then move inward, and the key insight is which pointer to move:

        The container's height is capped by the SHORTER of the two lines. Moving
        the taller line inward can only reduce the width while the height stays
        capped by the same short line — so it can never help. Moving the SHORTER
        line, however, discards that limiting line for a chance at a taller one,
        which is the only way the area might grow.

    So at each step we compute the current area, update our best, and then move
    the pointer at the shorter line inward. We repeat until the pointers meet.
    Because every move discards the shorter line, we never skip a container that
    could have been better than what we keep.

    (If the two lines are equal in height, moving either one is fine — both
    candidates capped by that height are already accounted for.)

    COMPLEXITY
    ----------
    Time  : O(n) — the two pointers start at opposite ends and move toward each
            other, so together they traverse the array exactly once.
    Space : O(1) — only a few scalar variables are used, regardless of input size.

    Args:
        height (list[int]): Heights of the vertical lines.

    Returns:
        int: The maximum water area that can be contained.
    """
    # Start with the widest possible container: the two outermost lines.
    left, right = 0, len(height) - 1
    best = 0

    while left < right:
        # Width is the distance between the lines; height is the shorter line.
        width = right - left
        current_height = min(height[left], height[right])
        best = max(best, width * current_height)

        # Move the pointer at the shorter line inward — it's the limiting factor,
        # and only replacing it gives a chance at a larger area.
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # -> 49
    print(max_area([1, 1]))                        # -> 1
    print(max_area([4, 3, 2, 1, 4]))               # -> 16
    print(max_area([1, 2, 1]))                     # -> 2
