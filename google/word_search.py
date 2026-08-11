"""
Word Search
===========

PROBLEM PROMPT
--------------
Given an m x n grid of characters `board` and a string `word`, return True if
`word` exists in the grid.

The word can be constructed from letters of sequentially ADJACENT cells, where
adjacent cells are horizontally or vertically neighboring. The SAME letter cell
may NOT be used more than once (in a single path).

Example 1:
    board = [["A","B","C","E"],
             ["S","F","C","S"],
             ["A","D","E","E"]]
    word = "ABCCED"   -> Output: True
    word = "SEE"      -> Output: True
    word = "ABCB"     -> Output: False  (would reuse the 'B' cell)

Constraints:
    m == len(board), n == len(board[0])
    1 <= m, n <= 6
    1 <= len(word) <= 15
    board and word consist of only lowercase and uppercase English letters.
"""


def exist(board, word):
    """
    Return True if `word` can be traced through adjacent cells of `board`.

    APPROACH (DFS backtracking on a grid with in-place marking)
    -----------------------------------------------------------
    Same choose -> recurse -> un-choose skeleton as the other backtracking
    problems, but the search space is a 2D grid and the "choices" at each step
    are the four neighbours (up / down / left / right).

    A match is a PATH through the grid whose letters spell `word` in order, using
    each cell at most once. We don't know where that path starts, so we try to
    launch a DFS from EVERY cell, asking: "starting here, can I spell word from
    index 0 onward?" If any launch succeeds, the answer is True.

    The DFS carries an index `k` = how many characters of `word` we've matched so
    far. At cell (r, c):

      1. If k == len(word), we've already matched every character -> success.
         (We check this before touching the grid, so it also handles the whole
         word being found.)
      2. If (r, c) is off the board OR board[r][c] != word[k], this cell can't
         extend the match -> return False (prune this branch immediately).
      3. Otherwise board[r][c] matches word[k]. We CHOOSE this cell, then recurse
         into its four neighbours to match word[k + 1]. If any neighbour
         succeeds, propagate True.

    IN-PLACE VISITED MARKING (the key trick): to forbid reusing a cell within the
    current path, we temporarily overwrite board[r][c] with a sentinel ('#') that
    can never equal any letter of `word`. That way, if the DFS wanders back to
    this cell, the board[r][c] != word[k] check rejects it -- no separate
    `visited` set needed. After exploring all four neighbours we RESTORE the
    original letter (un-choose), so the cell is free for other paths. Restoring
    is essential: skip it and you'd permanently blank out cells for future DFS
    launches.

    Why not a `visited` set? It also works and is arguably clearer, but the
    sentinel trick keeps the constraint (no reuse) and the letter-match check in
    a single comparison and uses O(1) extra space beyond the recursion stack.

    COMPLEXITY
    ----------
    Let m x n be the board size and L = len(word).
    Time  : O(m * n * 4^L) -- we may launch a DFS from each of the m*n cells, and
            each DFS branches into up to 4 directions per character, to depth L.
            (In practice the letter-match prune trims this enormously.)
    Space : O(L) for the recursion stack (path depth is at most the word length);
            the visited marking is done in place, using no extra grid.

    Args:
        board (list[list[str]]): The grid of characters.
        word (str): The word to search for.

    Returns:
        bool: True if `word` exists as an adjacent-cell path, else False.
    """
    if not word:
        return True
    if not board or not board[0]:
        return False

    rows, cols = len(board), len(board[0])

    def dfs(r, c, k):
        # Matched every character -> the word is fully found.
        if k == len(word):
            return True
        # Off-board or the current cell doesn't match word[k] -> dead branch.
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[k]:
            return False

        # Choose (r, c): mark it used so the path can't revisit it.
        original = board[r][c]
        board[r][c] = "#"

        # Recurse into the four neighbours to match the next character.
        found = (
            dfs(r + 1, c, k + 1)
            or dfs(r - 1, c, k + 1)
            or dfs(r, c + 1, k + 1)
            or dfs(r, c - 1, k + 1)
        )

        # Un-choose: restore the letter so other paths may use this cell.
        board[r][c] = original
        return found

    # Try to start the word at every cell.
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False


if __name__ == "__main__":
    board = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    print(exist(board, "ABCCED"))   # -> True
    print(exist(board, "SEE"))      # -> True
    print(exist(board, "ABCB"))     # -> False  (can't reuse the 'B' cell)
    print(exist(board, "ABCCEDASF"))   # -> True  (long winding path)

    # Single cell edge cases.
    print(exist([["A"]], "A"))      # -> True
    print(exist([["A"]], "B"))      # -> False

    # The board is left UNCHANGED after searching (marks are restored).
    snapshot = [row[:] for row in board]
    exist(board, "ABCCED")
    print(board == snapshot)        # -> True
