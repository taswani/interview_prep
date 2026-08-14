"""
Search a 2D Matrix
==================

PROBLEM PROMPT
--------------
You are given an m x n integer matrix `matrix` with the following two
properties:

  1. Each row is sorted in non-decreasing order (left to right).
  2. The first integer of each row is greater than the last integer of the
     previous row.

Given an integer `target`, return True if `target` is in `matrix`, or False
otherwise.

You must write a solution in O(log(m * n)) time complexity.

Example 1:
    Input:  matrix = [[1, 3, 5, 7],
                      [10, 11, 16, 20],
                      [23, 30, 34, 60]], target = 3
    Output: True

Example 2:
    Input:  matrix = [[1, 3, 5, 7],
                      [10, 11, 16, 20],
                      [23, 30, 34, 60]], target = 13
    Output: False

Constraints:
    m == len(matrix), n == len(matrix[0])
    1 <= m, n <= 100
    -10^4 <= matrix[i][j], target <= 10^4
"""


def search_matrix(matrix, target):
    """
    Return True if `target` appears in the row/column-sorted matrix.

    APPROACH (Treat the matrix as one flat sorted array)
    ----------------------------------------------------
    The two properties together are the whole trick. Property 1 says each row is
    sorted; property 2 says every row starts higher than the previous row ended.
    Chain those and the matrix, read left-to-right then top-to-bottom, is a
    SINGLE sorted sequence of m*n values:

        [[1, 3, 5, 7],
         [10, 11, 16, 20],   ->  1 3 5 7 10 11 16 20 23 30 34 60
         [23, 30, 34, 60]]

    So this is just plain binary search (see `binary_search.py`) over the virtual
    index range [0, m*n - 1] -- we never physically flatten the matrix, we just
    PRETEND it's a 1D array and translate each virtual index back to a (row, col)
    on demand.

    THE INDEX <-> (row, col) MAPPING: with n columns per row, virtual index `idx`
    corresponds to

        row = idx // n        (how many full rows of n fit before idx)
        col = idx %  n        (position within that row)

    Python's divmod(idx, n) returns exactly this (row, col) pair. So mid becomes
    matrix[mid // n][mid % n], and everything else is the identical closed-
    interval binary search: compare, then move lo = mid + 1 or hi = mid - 1.

    Because we search m*n virtual positions and halve the interval each step, the
    runtime is O(log(m*n)) -- which meets the required bound and is strictly
    better than an O(log m + log n) two-pass (search the row, then the column),
    though both are acceptable.

    COMPLEXITY
    ----------
    Let m = rows and n = columns.
    Time  : O(log(m * n)) -- one binary search over all m*n cells.
    Space : O(1) -- two pointers; the flattening is virtual, not materialized.

    Args:
        matrix (list[list[int]]): Row-sorted matrix with rows in increasing
            order (each row's first element > previous row's last element).
        target (int): The value to find.

    Returns:
        bool: True if `target` is present, else False.
    """
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1     # virtual indices into the flattened matrix

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        # Unfold the flat index back into a (row, col) coordinate.
        row, col = divmod(mid, cols)
        value = matrix[row][col]

        if value == target:
            return True
        elif value < target:
            lo = mid + 1            # target is later in the flattened order
        else:
            hi = mid - 1            # target is earlier

    return False


if __name__ == "__main__":
    matrix = [
        [1, 3, 5, 7],
        [10, 11, 16, 20],
        [23, 30, 34, 60],
    ]
    print(search_matrix(matrix, 3))    # -> True
    print(search_matrix(matrix, 13))   # -> False  (absent, falls between rows)
    print(search_matrix(matrix, 1))    # -> True   (top-left corner)
    print(search_matrix(matrix, 60))   # -> True   (bottom-right corner)
    print(search_matrix(matrix, 0))    # -> False  (below the minimum)
    print(search_matrix(matrix, 61))   # -> False  (above the maximum)

    # Single row and single cell edge cases.
    print(search_matrix([[1, 2, 3]], 2))   # -> True
    print(search_matrix([[5]], 5))         # -> True
    print(search_matrix([[5]], 4))         # -> False

    # Exhaustive cross-check: every value in the matrix must be found, and a
    # sweep of nearby non-members must all be rejected.
    present = all(search_matrix(matrix, v) for row in matrix for v in row)
    flat = {v for row in matrix for v in row}
    absent = all(not search_matrix(matrix, t) for t in range(-2, 65) if t not in flat)
    print(present and absent)               # -> True