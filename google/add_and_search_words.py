"""
Design Add and Search Words Data Structure
==========================================

PROBLEM PROMPT
--------------
Design a data structure that supports adding new words and finding if a string
matches any previously added string.

Implement the WordDictionary class:

    WordDictionary()             Initializes the object.
    void addWord(word)           Adds `word` to the data structure, it can be
                                 matched later.
    bool search(word)            Returns True if there is any string in the data
                                 structure that matches `word` or False
                                 otherwise. `word` may contain dots '.' where a
                                 dot can be matched with ANY letter.

Example:
    Input:
        ["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
        [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
    Output:
        [null,null,null,null,false,true,true,true]

    Explanation:
        wd = WordDictionary()
        wd.addWord("bad")
        wd.addWord("dad")
        wd.addWord("mad")
        wd.search("pad")   -> False
        wd.search("bad")   -> True
        wd.search(".ad")   -> True   (dot matches b/d/m)
        wd.search("b..")   -> True   ("bad")

Constraints:
    1 <= len(word) <= 25
    word in addWord consists of lowercase English letters.
    word in search consists of '.' or lowercase English letters.
    There are at most 2 dots in `word` for `search` queries.
    At most 10^4 calls will be made to addWord and search.
"""


class TrieNode:
    """
    One node of the prefix tree.

    children : dict mapping a character -> child TrieNode.
    is_end   : True if the path from the root to this node spells a complete
               added word (not merely a prefix).
    """

    def __init__(self):
        self.children = {}
        self.is_end = False


class WordDictionary:
    """
    A trie that supports exact adds and wildcard ('.') search.

    APPROACH (Trie + DFS that branches on the wildcard)
    ---------------------------------------------------
    `addWord` is the ordinary trie insert from `implement_trie.py`: walk the
    characters, creating nodes as needed, and flag the final node is_end = True.

    `search` is where this problem differs. For a normal letter the walk is
    deterministic -- from the current node, step to children[ch] if it exists,
    else fail. But a DOT '.' matches ANY single letter, so at a dot we don't know
    which branch to take; we must try them ALL. That turns the linear walk into a
    DEPTH-FIRST SEARCH over the trie.

    We DFS with a helper dfs(index, node), where `index` is the position in the
    query `word` we're currently matching and `node` is the trie node we've
    reached so far:

      - BASE CASE: index == len(word). We've consumed the whole query. It's a
        MATCH only if `node` marks the end of a real word -> return node.is_end.
        (Reaching the node isn't enough; a query like "ba" must not match the
        added word "bad" -- the path exists but node.is_end is False.)

      - LETTER (word[index] != '.'): deterministic step. If that child is
        missing, this branch can't match -> return False. Otherwise recurse into
        the single child at index + 1.

      - DOT (word[index] == '.'): branch. Try EVERY child of `node`; if the DFS
        succeeds down ANY of them (recursing at index + 1), the whole search
        succeeds -> return True. If none work, return False.

    The short-circuiting `any(...)` stops at the first child that leads to a
    match, so we don't explore the rest once we've found one.

    COMPLEXITY
    ----------
    Let L = len(word) and let the alphabet size be 26 (children per node).
    addWord : O(L) time.
    search  : O(L) time when `word` has no dots (a single deterministic path).
              With d dots the DFS can branch up to 26 ways at each dot, so the
              worst case is O(26^d * L). The constraint of at most 2 dots keeps
              this small in practice; a leading run of dots is the costly case
              because it fans out near the root.
    Space   : O(total characters added) for the trie; O(L) recursion depth per
              search.
    """

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word):
        """Insert `word` into the trie (plain deterministic walk)."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        """Return True if `word` (with '.' wildcards) matches any added word."""

        def dfs(index, node):
            # Consumed the whole query -> match iff this node ends a real word.
            if index == len(word):
                return node.is_end

            ch = word[index]
            if ch == ".":
                # Wildcard: succeed if ANY child leads to a match.
                return any(dfs(index + 1, child) for child in node.children.values())
            else:
                # Concrete letter: the one specific branch must exist.
                if ch not in node.children:
                    return False
                return dfs(index + 1, node.children[ch])

        return dfs(0, self.root)


if __name__ == "__main__":
    # Worked example from the prompt.
    wd = WordDictionary()
    for w in ["bad", "dad", "mad"]:
        wd.addWord(w)
    print(wd.search("pad"))    # -> False (never added)
    print(wd.search("bad"))    # -> True  (exact)
    print(wd.search(".ad"))    # -> True  (dot matches b/d/m)
    print(wd.search("b.."))    # -> True  ("bad")

    # More cases.
    wd2 = WordDictionary()
    for w in ["a", "ab", "abc"]:
        wd2.addWord(w)
    print(wd2.search("a"))      # -> True
    print(wd2.search("a."))     # -> True  ("ab")
    print(wd2.search(".."))     # -> True  ("ab")
    print(wd2.search("..."))    # -> True  ("abc")
    print(wd2.search("...."))   # -> False (no length-4 word)
    print(wd2.search("ab"))     # -> True
    print(wd2.search("."))      # -> True  ("a")
    print(wd2.search("b."))     # -> False (nothing starts with 'b')

    # A prefix that is not itself a word must NOT match (is_end check).
    wd3 = WordDictionary()
    wd3.addWord("bad")
    print(wd3.search("ba"))     # -> False (path exists, but not a full word)
    print(wd3.search("b.d"))    # -> True  ("bad")
    print(wd3.search("..."))    # -> True  ("bad")
