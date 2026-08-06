"""
Word Break
==========

PROBLEM PROMPT
--------------
Given a string `s` and a dictionary of strings `wordDict`, return True if `s`
can be segmented into a space-separated sequence of one or more dictionary
words.

Note that the same word in the dictionary may be reused multiple times in the
segmentation.

Example 1:
    Input:  s = "leetcode", wordDict = ["leet", "code"]
    Output: True
    Explanation: Return True because "leetcode" can be segmented as "leet code".

Example 2:
    Input:  s = "applepenapple", wordDict = ["apple", "pen"]
    Output: True
    Explanation: Return True because "applepenapple" can be segmented as
                 "apple pen apple". Note that you are allowed to reuse a
                 dictionary word.

Example 3:
    Input:  s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
    Output: False
    Explanation: There is no way to segment the whole string into dictionary
                 words.

Constraints:
    1 <= len(s) <= 300
    1 <= len(wordDict) <= 1000
    1 <= len(wordDict[i]) <= 20
    s and wordDict[i] consist of only lowercase English letters.
    All the strings of wordDict are unique.
"""


class TrieNode:
    """A node in a prefix tree (trie)."""

    def __init__(self):
        # Maps a single character -> the child TrieNode reached by that character.
        self.children = {}
        # True if the path from the root to this node spells a complete word.
        self.is_word = False


def word_break(s, word_dict):
    """
    Return True if `s` can be segmented into words from `word_dict`.

    APPROACH (Dynamic Programming over Prefixes)
    --------------------------------------------
    The naive recursion — "try every dictionary word as a prefix, then recurse on
    the rest" — re-solves the same suffixes over and over, blowing up
    exponentially. The fix is dynamic programming: solve each subproblem once and
    remember the answer.

    Define a boolean array `dp` of length n + 1, where:

        dp[i] == True  means  the first i characters s[0:i] can be fully
                              segmented into dictionary words.

    dp[0] is True as the base case: the empty prefix is trivially segmentable
    (it needs zero words).

    To fill dp[i], we ask: is there some split point j (0 <= j < i) such that
      - the prefix s[0:j] is already segmentable (dp[j] is True), AND
      - the remaining chunk s[j:i] is itself a dictionary word?
    If such a j exists, then s[0:i] is segmentable, so dp[i] = True. In words: a
    prefix is breakable if it splits into a shorter breakable prefix plus one
    dictionary word at the end.

    We convert `word_dict` to a SET first so each "is this chunk a word?" check is
    O(1) on average instead of scanning the list.

    The final answer is dp[n]: can the ENTIRE string be segmented?

    COMPLEXITY
    ----------
    Let n = len(s) and L = the maximum word length.
    Time  : O(n^2 * L) — there are n values of i, each tries up to n split points
            j, and each s[j:i] slice/hash costs up to O(L). (Often written as
            O(n^2) when treating the substring hashing as O(1).)
    Space : O(n) for the dp array, plus O(total dictionary characters) for the set.

    Args:
        s (str): The string to segment.
        word_dict (list[str]): The dictionary of allowed words.

    Returns:
        bool: True if `s` can be fully segmented, False otherwise.
    """
    # Set membership is O(1) average vs. O(len) for scanning the list.
    words = set(word_dict)
    n = len(s)

    # dp[i] == True means s[0:i] is segmentable. dp[0] (empty prefix) is True.
    dp = [False] * (n + 1)
    dp[0] = True

    # Build up answers for longer and longer prefixes.
    for i in range(1, n + 1):
        # Try every split point j: s[0:j] breakable AND s[j:i] is a word.
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break  # One valid split is enough; stop checking other j's.

    # Can the whole string be segmented?
    return dp[n]


def word_break_trie(s, word_dict):
    """
    Return True if `s` can be segmented into words from `word_dict`, using a trie.

    APPROACH (Dynamic Programming + Prefix Tree)
    --------------------------------------------
    This uses the same dp[] idea as `word_break` above — dp[i] means s[0:i] is
    segmentable, dp[0] is True — but replaces the "slice s[j:i] and hash it
    against a set" step with a walk down a PREFIX TREE (trie).

    Why a trie helps:
      - No substring slicing. The set version builds a new string s[j:i] for
        every (j, i) pair, which allocates memory and re-reads characters. The
        trie walks the ORIGINAL string one character at a time, following child
        links, so it inspects each character in place.
      - Shared prefixes are traversed once. Dictionary words that begin the same
        way (e.g. "cat", "cats", "catalog") collapse into a single path in the
        trie, so overlapping candidates aren't re-scanned independently.
      - Early termination. As we extend a candidate word character by character,
        the moment the current character isn't a child of the current trie node,
        NO dictionary word continues this way — so we stop immediately instead of
        checking longer and longer dead-end substrings.

    The algorithm: build a trie from the dictionary. Then for every start index i
    where dp[i] is True (meaning s[0:i] is already segmentable), we walk the trie
    forward from position i. Each time we land on a node marked `is_word`, the
    chunk s[i:end+1] is a dictionary word, so the prefix ending there is
    segmentable — we set dp[end + 1] = True. We stop walking as soon as the path
    leaves the trie.

    COMPLEXITY
    ----------
    Let n = len(s), and let W = total characters across all dictionary words.
    Time  : O(n^2) — for each of the n start positions we walk forward up to n
            characters through the trie, each step O(1). (Building the trie is
            O(W).) This matches the set-based DP's O(n^2) but avoids the
            per-step substring allocation, so it's often faster in practice.
    Space : O(W) for the trie, plus O(n) for the dp array.

    Args:
        s (str): The string to segment.
        word_dict (list[str]): The dictionary of allowed words.

    Returns:
        bool: True if `s` can be fully segmented, False otherwise.
    """
    # --- Build the trie from every dictionary word. ---
    root = TrieNode()
    for word in word_dict:
        node = root
        for char in word:
            # Create the child branch for this character if it doesn't exist yet.
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True  # Mark the end of a complete word.

    n = len(s)

    # dp[i] == True means s[0:i] is segmentable. dp[0] (empty prefix) is True.
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(n):
        # Only bother extending from positions we can actually reach.
        if not dp[i]:
            continue

        # Walk the trie forward from position i, matching s[i], s[i+1], ...
        node = root
        for end in range(i, n):
            char = s[end]
            # If the path leaves the trie, no dictionary word continues here.
            if char not in node.children:
                break
            node = node.children[char]
            # Reached the end of a dictionary word -> s[0:end+1] is segmentable.
            if node.is_word:
                dp[end + 1] = True

    return dp[n]


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(word_break("leetcode", ["leet", "code"]))                          # -> True
    print(word_break("applepenapple", ["apple", "pen"]))                     # -> True (reuse "apple")
    print(word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))    # -> False
    print(word_break("a", ["a"]))                                            # -> True (single word)
    print(word_break("aaaaaaa", ["aaaa", "aaa"]))                            # -> True (4 + 3)
    print(word_break("cars", ["car", "ca", "rs"]))                           # -> True (ca + rs)

    # The trie variant returns the same answers.
    print(word_break_trie("leetcode", ["leet", "code"]))                     # -> True
    print(word_break_trie("catsandog", ["cats", "dog", "sand", "and", "cat"]))  # -> False
    print(word_break_trie("applepenapple", ["apple", "pen"]))                # -> True
    print(word_break_trie("cars", ["car", "ca", "rs"]))                      # -> True
