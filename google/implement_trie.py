"""
Implement Trie (Prefix Tree)
============================

PROBLEM PROMPT
--------------
A trie (pronounced as "try") or prefix tree is a tree data structure used to
efficiently store and retrieve keys in a set of strings. There are various
applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

    Trie()                       Initializes the trie object.
    void insert(String word)     Inserts the string `word` into the trie.
    boolean search(String word)  Returns True if `word` is in the trie (i.e.,
                                 was inserted before), and False otherwise.
    boolean startsWith(String prefix)
                                 Returns True if there is a previously inserted
                                 string `word` that has the prefix `prefix`, and
                                 False otherwise.

Example:
    Input:
        ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
        [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
    Output:
        [null, null, true, false, true, null, true]

    Explanation:
        trie = Trie()
        trie.insert("apple")
        trie.search("apple")      -> True
        trie.search("app")        -> False   (inserted "apple", not "app")
        trie.startsWith("app")    -> True     ("apple" has prefix "app")
        trie.insert("app")
        trie.search("app")        -> True

Constraints:
    1 <= len(word), len(prefix) <= 2000
    word and prefix consist only of lowercase English letters.
    At most 3 * 10^4 calls in total will be made to insert, search, startsWith.
"""


class TrieNode:
    """
    A single node in the prefix tree.

    Each node represents one character position along some set of words. It holds:
      - children: a dict mapping a next character -> the child TrieNode for it.
        A dict (rather than a fixed size-26 array) keeps the code simple and only
        stores the branches that actually exist.
      - is_end: True if the path from the ROOT to this node spells a COMPLETE
        inserted word (not merely a prefix of one). This flag is what lets us
        distinguish `search` (needs a full word) from `startsWith` (needs only a
        path to exist).
    """

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """
    A prefix tree supporting insert / search (exact word) / startsWith (prefix).

    APPROACH (Character-by-character tree walk)
    -------------------------------------------
    A trie stores words by SHARING their common prefixes along tree paths. The
    root represents the empty prefix; each edge is labeled by a character; and
    following the edges c1, c2, ..., ck from the root spells the prefix
    c1 c2 ... ck. Words that begin the same way (e.g. "app", "apple", "apply")
    share the same initial nodes and only branch where they start to differ, so
    common prefixes are stored ONCE.

    All three operations are the same walk: start at the root and step to
    children[ch] for each character ch of the input.

      - insert(word): walk the characters, CREATING any child node that doesn't
        exist yet, then mark the final node's is_end = True to record that a
        complete word ends here.

      - search(word): walk the characters; if any child is missing, the word was
        never inserted -> False. If the walk completes, return the final node's
        is_end flag -- the path existing is not enough, it must be flagged as a
        real word's end (this is why search("app") is False after inserting only
        "apple").

      - startsWith(prefix): the SAME walk, but we don't care about is_end. If the
        walk completes without a missing child, some inserted word passes through
        here, so the prefix exists -> True.

    search and startsWith share their entire traversal; the ONLY difference is
    the final check (is_end vs. "did we get here at all"). We factor that shared
    walk into a private `_find` helper that returns the node reached, or None if
    the path breaks.

    WHY A TRIE OVER A HASH SET: a set answers exact `search` in O(L) too, but it
    CANNOT answer `startsWith` efficiently -- you'd have to scan every stored key.
    The trie makes prefix queries O(L) (L = length of the query) regardless of
    how many words are stored, which is exactly what autocomplete needs.

    COMPLEXITY (L = length of the word/prefix argument)
    ---------------------------------------------------
    insert     : O(L) time, O(L) new nodes in the worst case.
    search     : O(L) time, O(1) extra space.
    startsWith : O(L) time, O(1) extra space.
    Overall space: O(total characters inserted) across all words.
    """

    def __init__(self):
        # The root represents the empty prefix; it holds no character itself.
        self.root = TrieNode()

    def insert(self, word):
        """Insert `word`, creating nodes as needed and flagging the end."""
        node = self.root
        for ch in word:
            # Create the branch for this character if we haven't seen it here.
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        # The path from root to here now spells a complete inserted word.
        node.is_end = True

    def search(self, word):
        """Return True only if `word` was inserted as a COMPLETE word."""
        node = self._find(word)
        # Path must exist AND end on a node flagged as a word's end.
        return node is not None and node.is_end

    def startsWith(self, prefix):
        """Return True if any inserted word begins with `prefix`."""
        # Path existing is sufficient; is_end is irrelevant for a prefix query.
        return self._find(prefix) is not None

    def _find(self, s):
        """
        Walk the trie following the characters of `s`.

        Returns the TrieNode reached after consuming all of `s`, or None if any
        character has no matching child (the path breaks). Shared by both
        `search` and `startsWith`.
        """
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None      # path breaks -> neither word nor prefix exists
            node = node.children[ch]
        return node


if __name__ == "__main__":
    # Walk through the worked example from the prompt.
    trie = Trie()
    trie.insert("apple")
    print(trie.search("apple"))       # -> True
    print(trie.search("app"))         # -> False  ("apple" inserted, not "app")
    print(trie.startsWith("app"))     # -> True   ("apple" has prefix "app")
    trie.insert("app")
    print(trie.search("app"))         # -> True   (now inserted)

    # A few more cases.
    t = Trie()
    for w in ["apply", "apple", "apt", "bat"]:
        t.insert(w)
    print(t.search("apple"))          # -> True
    print(t.search("ap"))             # -> False  (a shared prefix, not a word)
    print(t.startsWith("ap"))         # -> True
    print(t.startsWith("ba"))         # -> True
    print(t.startsWith("ca"))         # -> False  (no word starts with "ca")
    print(t.search("bat"))            # -> True
    print(t.search("batman"))         # -> False  (longer than any inserted word)
    print(t.startsWith(""))           # -> True   (empty prefix: every trie has it)
