"""
Word Search II
==============

PROBLEM PROMPT
--------------
Given an m x n board of characters and a list of strings `words`, return all
words on the board.

Each word must be constructed from letters of sequentially ADJACENT cells, where
adjacent cells are horizontally or vertically neighboring. The same letter cell
may NOT be used more than once in a word.

Example 1:
    board = [["o","a","a","n"],
             ["e","t","a","e"],
             ["i","h","k","r"],
             ["i","f","l","v"]]
    words = ["oath","pea","eat","rain"]
    Output: ["oath","eat"]        (order does not matter)

Example 2:
    board = [["a","b"],["c","d"]]
    words = ["abcb"]
    Output: []

Constraints:
    m == len(board), n == len(board[0])
    1 <= m, n <= 12
    board[i][j] is a lowercase English letter.
    1 <= len(words) <= 3 * 10^4
    1 <= len(words[i]) <= 10
    All strings of words are unique.
"""


class TrieNode:
    """
    One node of the prefix tree built from `words`.

    children : dict mapping a character -> child TrieNode.
    word     : the COMPLETE word that ends at this node, or None. Storing the
               whole word here (instead of a plain is_end bool) means that when
               the board DFS reaches this node we can record the match directly,
               with no need to reconstruct the path.
    """

    def __init__(self):
        self.children = {}
        self.word = None


def find_words(board, words):
    """
    Return every word in `words` that can be traced through adjacent board cells.

    APPROACH (One trie + a single board DFS, instead of one search per word)
    ------------------------------------------------------------------------
    The naive plan is to run "Word Search" (problem 79) once for every word:
    O(len(words) * m * n * 4^L). With up to 3*10^4 words that re-walks the board
    enormously and re-traverses shared prefixes over and over.

    The fix combines the two tools from this week:

      1. Build a TRIE from all the words. Words that share a prefix (e.g. "eat",
         "eater", "east") now share a single path, so a DFS from a board cell can
         test ALL of them at once by walking the trie in lockstep with the board.

      2. Do ONE backtracking DFS over the board (the grid backtracking from
         problem 79, with in-place '#' marking). But instead of matching a fixed
         target string, the DFS walks the TRIE: at board cell (r, c) holding
         letter `ch`, we only continue if `ch` is a child of the current trie
         node. That child becomes the new trie node for the next cell.

    So the board DFS and the trie descent move together. Two things happen at a
    node during the walk:

      - If node.word is not None, the path spelled so far is a complete word ->
        add it to the results. We then set node.word = None so the SAME word is
        not reported twice (a word could be reachable by more than one path).

      - We branch into the four neighbours, each time descending to the matching
        trie child. In-place marking (overwrite board[r][c] with '#', restore it
        after) forbids reusing a cell within the current path, exactly as in
        problem 79.

    Starting cells: we launch the DFS from every board cell whose letter is a
    child of the trie root -- i.e. only cells that could begin some word.

    OPTIONAL PRUNING (leaf trimming): after a child's subtree is fully explored,
    if that child now has no children AND no word (a dead end -- everything under
    it has been found or was never reachable), we delete it from its parent. This
    shrinks the trie as words are discovered, so later DFS steps fail faster. It
    is a meaningful optimization on large inputs; the core algorithm is correct
    without it.

    COMPLEXITY
    ----------
    Let m x n be the board size, W = number of words, L = max word length.
    Building the trie: O(W * L).
    Board DFS: O(m * n * 4^L) in the worst case -- from each start cell the walk
        branches up to 4 ways to depth L. Crucially this bound is now INDEPENDENT
        of W: the trie lets one traversal cover all words at once, versus the
        naive O(W * m * n * 4^L).
    Space: O(W * L) for the trie, plus O(L) recursion depth.

    Args:
        board (list[list[str]]): The grid of lowercase letters.
        words (list[str]): The words to find.

    Returns:
        list[str]: The subset of `words` present on the board (any order).
    """
    if not board or not board[0] or not words:
        return []

    # --- Build the trie from all words; store the full word at each end node. ---
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = word

    rows, cols = len(board), len(board[0])
    result = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.children[ch]     # caller guaranteed ch is a child

        # A complete word ends here -> record it once.
        if node.word is not None:
            result.append(node.word)
            node.word = None           # avoid reporting the same word twice

        # Mark this cell used so the current path can't revisit it.
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node.children:
                dfs(nr, nc, node)
        board[r][c] = ch               # restore (un-choose)

        # Prune this node if it became a dead end (nothing left to find below).
        if not node.children and node.word is None:
            del parent.children[ch]

    # Launch a DFS from every cell that could start some word.
    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root.children:
                dfs(r, c, root)

    return result


if __name__ == "__main__":
    board1 = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    print(sorted(find_words(board1, ["oath", "pea", "eat", "rain"])))
    # -> ['eat', 'oath']

    print(find_words([["a", "b"], ["c", "d"]], ["abcb"]))   # -> []  (would reuse 'b')

    # Duplicate-path word is reported only once.
    print(find_words([["a", "a"]], ["a"]))                   # -> ['a']

    # Overlapping-prefix words: the trie tests them together in one walk.
    board2 = [
        ["a", "b", "c"],
        ["a", "e", "d"],
        ["a", "f", "g"],
    ]
    print(sorted(find_words(board2, ["abc", "abcd", "abe", "aaa", "xyz"])))
    # -> ['aaa', 'abc', 'abcd', 'abe']  (all present via shared prefixes; xyz absent)

    # Board is left UNCHANGED after searching (marks are restored).
    snapshot = [row[:] for row in board1]
    find_words(board1, ["oath", "eat"])
    print(board1 == snapshot)                                # -> True
