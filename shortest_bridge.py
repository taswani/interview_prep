"""
Problem: Shortest Bridge (LeetCode 934)

Description:
-------------
Given a 2D grid of 0s (water) and 1s (land), there are exactly two islands 
(each island is a group of connected 1s, horizontally or vertically). 

You may flip 0s to 1s to connect the two islands. 

Return the minimum number of 0s you must flip to connect the two islands, 
i.e., the length of the shortest bridge.

Example:
--------
Input: grid = [
  [0,1],
  [1,0]
]
Output: 1

Input: grid = [
  [0,1,0],
  [0,0,0],
  [0,0,1]
]
Output: 2
"""

from collections import deque

def shortestBridge(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(1,0),(0,1),(-1,0),(0,-1)]
    visited = set()
    
    # Helper DFS to mark the first island
    def dfs(r, c, q):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != 1 or (r,c) in visited):
            return
        visited.add((r,c))
        q.append((r,c))
        for dr, dc in directions:
            dfs(r+dr, c+dc, q)
    
    # Step 1: find first island and mark it
    queue = deque()
    found = False
    for r in range(rows):
        if found: break
        for c in range(cols):
            if grid[r][c] == 1:
                dfs(r, c, queue)
                found = True
                break

    # Step 2: BFS to expand towards the second island
    steps = 0
    while queue:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in visited:
                    if grid[nr][nc] == 1:
                        # Reached the second island
                        return steps
                    queue.append((nr,nc))
                    visited.add((nr,nc))
        steps += 1


# ---------------- Time & Space Complexity ----------------
# Time: O(n*m) - each cell visited at most once
# Space: O(n*m) - visited set and BFS queue
# ---------------------------------------------------------

# ---------------- Test Cases ----------------
if __name__ == "__main__":
    grid1 = [[0,1],[1,0]]
    print(shortestBridge(grid1))  # Expected: 1

    grid2 = [
        [0,1,0],
        [0,0,0],
        [0,0,1]
    ]
    print(shortestBridge(grid2))  # Expected: 2

    grid3 = [
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1]
    ]
    print(shortestBridge(grid3))  # Expected: 1

    grid4 = [
        [0,1,0,0,0],
        [0,1,0,0,1],
        [0,0,0,0,1],
        [0,0,0,1,1]
    ]
    print(shortestBridge(grid4))  # Expected: 2
