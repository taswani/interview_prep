"""
Number of Islands
=================

PROBLEM PROMPT
--------------
Given an m x n 2D binary grid `grid` which represents a map of '1's (land) and
'0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands
horizontally or vertically. You may assume all four edges of the grid are all
surrounded by water. (Diagonal connections do NOT count.)

Example 1:
    Input:  grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    Output: 1

Example 2:
    Input:  grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    Output: 3

Constraints:
    m == len(grid)
    n == len(grid[0])
    1 <= m, n <= 300
    grid[i][j] is '0' or '1'.
"""


def num_islands(grid):
    """
    Count the number of islands (connected groups of land) in the grid.

    APPROACH (DFS Flood Fill)
    -------------------------
    Think of the grid as a graph where each land cell ('1') is a node connected
    to its up/down/left/right land neighbors. An "island" is simply a connected
    component of that graph. Counting islands means counting connected
    components.

    We scan the grid cell by cell. Every time we encounter a piece of land we
    have NOT visited yet, we've found a new island, so we increment the counter.
    We then "flood fill" that entire island with a depth-first search, marking
    every connected land cell as visited so we never count any part of it again.

    To mark cells as visited without allocating a separate visited-set, we SINK
    each land cell we reach — overwrite its '1' with '0' (water). Once an island
    is fully sunk, the outer scan will never re-enter it. (This mutates the input
    grid; if the caller needs the grid preserved, use a separate visited set or a
    copy instead.)

    The DFS from a starting land cell recursively spreads in all four directions,
    stopping whenever it steps off the grid or onto water. By the time it
    returns, the whole island has been sunk.

    COMPLEXITY
    ----------
    Time  : O(m * n) — every cell is examined by the outer scan once, and the DFS
            visits each land cell a constant number of times before sinking it.
            With m rows and n columns that's O(m * n) total.
    Space : O(m * n) — worst-case recursion depth. If the entire grid is land,
            the DFS call stack can hold every cell at once (e.g. a snake-like
            filling order), giving O(m * n) stack frames.

    Args:
        grid (list[list[str]]): 2D grid of '1' (land) and '0' (water). Mutated
            in place (land is sunk to water as it is counted).

    Returns:
        int: The number of islands.
    """
    # An empty grid has no islands.
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def sink(r, c):
        """Flood-fill (sink) the whole island reachable from cell (r, c)."""
        # Stop if we've walked off the grid or hit water (already-visited or sea).
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == "0":
            return

        # Mark this land cell as visited by sinking it to water.
        grid[r][c] = "0"

        # Spread to the four orthogonal neighbors.
        sink(r + 1, c)  # down
        sink(r - 1, c)  # up
        sink(r, c + 1)  # right
        sink(r, c - 1)  # left

    # Scan every cell; each unvisited land cell starts a new island.
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1     # Found a new island...
                sink(r, c)     # ...then sink it so it's only counted once.

    return count


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    print(num_islands(grid1))  # -> 1

    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    print(num_islands(grid2))  # -> 3

    print(num_islands([["0"]]))                    # -> 0 (all water)
    print(num_islands([["1"]]))                    # -> 1 (single land cell)
    print(num_islands([["1", "0", "1", "0", "1"]]))  # -> 3 (diagonal/separated)
