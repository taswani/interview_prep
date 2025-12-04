"""
LeetCode 317 — Shortest Distance from All Buildings

🧩 Problem:
You are given a 2D grid of size m x n, where:
  0 = empty land you can build on
  1 = building (cannot pass through)
  2 = obstacle (cannot pass through)

Find the empty land that has the shortest total distance to all buildings.
You can move up, down, left, or right.

Return the minimum total distance. If it is impossible for all buildings to reach
an empty land, return -1.

Example:
----------
Input:
[
  [1,0,2,0,1],
  [0,0,0,0,0],
  [0,0,1,0,0]
]

Output: 7
Explanation: The best place to build a house is (1,2),
with total distance = 7.
"""

from collections import deque

def shortestDistance(grid):
    """
    🧠 Intuition:
    Instead of BFS from every empty land (which would be O((mn)^2)),
    we BFS from every building and accumulate distances to all reachable empty lands.

    For each building:
      - Perform BFS outward.
      - Update two matrices:
        total_dist[r][c]: sum of all distances from buildings to (r, c)
        reach[r][c]: how many buildings can reach (r, c)

    At the end, pick the minimum total_dist[r][c] where
    reach[r][c] == total_buildings and grid[r][c] == 0.

    ⚙️ Approach:
      1. Gather all building coordinates.
      2. For each building, BFS and update distances.
      3. Compute the smallest total distance among valid empty cells.

    ⏱️ Time Complexity:  O(B * M * N)
    🧮 Space Complexity: O(M * N)
    where B = number of buildings, M = rows, N = cols
    """

    if not grid or not grid[0]:
        return -1

    rows, cols = len(grid), len(grid[0])
    total_dist = [[0] * cols for _ in range(rows)]
    reach = [[0] * cols for _ in range(rows)]

    buildings = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]
    total_buildings = len(buildings)

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def bfs(sr, sc):
        visited = [[False] * cols for _ in range(rows)]
        queue = deque([(sr, sc, 0)])
        visited[sr][sc] = True

        while queue:
            r, c, dist = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < rows and
                    0 <= nc < cols and
                    not visited[nr][nc] and
                    grid[nr][nc] == 0
                ):
                    visited[nr][nc] = True
                    total_dist[nr][nc] += dist + 1
                    reach[nr][nc] += 1
                    queue.append((nr, nc, dist + 1))

    # Run BFS from each building
    for br, bc in buildings:
        bfs(br, bc)

    # Find the minimum distance
    result = float('inf')
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0 and reach[r][c] == total_buildings:
                result = min(result, total_dist[r][c])

    return result if result != float('inf') else -1


# 🧪 Test Cases
if __name__ == "__main__":
    grids = [
        (
            [
                [1,0,2,0,1],
                [0,0,0,0,0],
                [0,0,1,0,0]
            ],
            7
        ),
        (
            [
                [1,0],
                [0,0]
            ],
            1
        ),
        (
            [
                [1,2,0]
            ],
            -1
        ),
        (
            [
                [1,0,1,0,1],
                [0,0,0,0,0],
                [1,0,1,0,1]
            ],
            14
        )
    ]

    for i, (grid, expected) in enumerate(grids, 1):
        print(f"Test Case {i}: Expected = {expected}, Got = {shortestDistance(grid)}")
