"""
Alien Dictionary
================

PROBLEM PROMPT
--------------
There is a new alien language that uses the English alphabet. However, the order
among the letters is unknown to you.

You are given a list of strings `words` from the alien language's dictionary. The
strings in `words` are SORTED lexicographically by the rules of this new
language.

Return a string of the unique letters in the new alien language sorted in
LEXICOGRAPHICALLY INCREASING order by the new language's rules. If there is no
solution, return "". If there are multiple solutions, return ANY of them.

A string s is lexicographically smaller than a string t if at the first letter
where they differ, the letter in s comes before the letter in t in the alien
order. If the first min(len(s), len(t)) letters are the same, then s is smaller
if and only if len(s) < len(t).

Example 1:
    Input:  words = ["wrt","wrf","er","ett","rftt"]
    Output: "wertf"
Example 2:
    Input:  words = ["z","x"]
    Output: "zx"
Example 3:
    Input:  words = ["z","x","z"]
    Output: ""
    Explanation: The order is invalid, so return "".

Constraints:
    1 <= len(words) <= 100
    1 <= len(words[i]) <= 100
    words[i] consists of only lowercase English letters.
"""

from collections import deque, defaultdict


def alien_order(words):
    """
    Return a letter ordering consistent with the alien-sorted `words`, or "".

    APPROACH (Derive the graph from adjacent words, then topological sort)
    ---------------------------------------------------------------------
    The topological sort is the routine part (Kahn's algorithm, exactly as in
    Course Schedule). The crux of THIS problem is CONSTRUCTING the graph: the
    letter order isn't given, we must EXTRACT the ordering constraints from the
    fact that `words` is already sorted.

    WHERE CONSTRAINTS COME FROM: comparing two ADJACENT words w1, w2 (w1 sorted
    before w2), the FIRST position where they differ reveals one ordering fact.
    If w1[i] != w2[i] is the first mismatch, then in the alien order
    w1[i] comes before w2[i] -- that's a directed edge w1[i] -> w2[i]. Everything
    before position i is equal and tells us nothing; everything AFTER i is
    irrelevant, because the first difference alone decides the sort order. So each
    adjacent pair contributes AT MOST ONE edge, and we stop at the first mismatch.

    THE INVALID-PREFIX EDGE CASE (the classic trap): if w1 is a strict PREFIX of
    w2 reversed -- i.e. w1 is LONGER than w2 yet they share w2 as a prefix, like
    ["abc", "ab"] -- then a longer word sorts before its own prefix, which is
    impossible in any valid ordering. We must detect this and return "". Concretely:
    if we scan to the end of the shorter word without finding a mismatch AND
    len(w1) > len(w2), the input is invalid.

    COLLECTING THE VERTICES: every distinct letter that appears anywhere must be
    in the output, even letters that never participate in an edge (no constraint
    relates them). We initialize indegree for each seen letter to 0 up front so
    those "free" letters still get emitted.

    Then it's standard Kahn's topological sort over the letter graph:
      - indegree[c] = number of letters that must come before c.
      - Seed a queue with all indegree-0 letters, pop them one at a time, appending
        to the result and relaxing edges (decrement successors' indegree, enqueue
        any that reach 0).
      - If we emit every distinct letter, return the built string. If some letters
        never reach indegree 0, a CYCLE exists (contradictory constraints, e.g.
        a<b and b<a), so no valid order exists -> return "".

    (Note: use a SET of successors per letter so a repeated identical edge from
    multiple word pairs doesn't inflate indegree and wrongly break the count.)

    COMPLEXITY
    ----------
    Let C = total number of characters across all words, and U = number of unique
    letters (<= 26).
    Time  : O(C) -- one pass to gather letters, one pass over adjacent pairs
            (each comparison bounded by word length), then O(U + edges) for the
            sort.
    Space : O(U + edges) = O(1) bounded by the 26-letter alphabet.

    Args:
        words (list[str]): Words sorted per the alien language's rules.

    Returns:
        str: A valid letter ordering, or "" if none exists.
    """
    # adjacency[c] = set of letters that must come AFTER c; indegree per letter.
    adjacency = defaultdict(set)
    indegree = {ch: 0 for word in words for ch in word}   # every letter starts at 0

    # Derive one edge from each adjacent pair of words.
    for w1, w2 in zip(words, words[1:]):
        min_len = min(len(w1), len(w2))
        # Invalid: a longer word appears before its own prefix (e.g. "abc","ab").
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for i in range(min_len):
            if w1[i] != w2[i]:
                # First difference: w1[i] must come before w2[i].
                if w2[i] not in adjacency[w1[i]]:
                    adjacency[w1[i]].add(w2[i])
                    indegree[w2[i]] += 1
                break   # only the first mismatch matters; stop comparing.

    # Kahn's algorithm: start from letters with no predecessor.
    queue = deque(ch for ch in indegree if indegree[ch] == 0)
    order = []
    while queue:
        ch = queue.popleft()
        order.append(ch)
        for nxt in adjacency[ch]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    # All letters placed -> valid order; otherwise a cycle blocked some -> "".
    return "".join(order) if len(order) == len(indegree) else ""


def _is_valid_order(words, order):
    """
    Verify `order` is consistent with `words` (test helper).

    Checks that (a) `order` contains exactly the distinct letters of `words`, and
    (b) mapping each letter to its rank in `order` makes every adjacent word pair
    correctly sorted. Used because the problem accepts ANY valid ordering, so we
    can't compare against one fixed expected string.
    """
    letters = {ch for w in words for ch in w}
    if set(order) != letters or len(order) != len(letters):
        return False
    rank = {ch: i for i, ch in enumerate(order)}
    for w1, w2 in zip(words, words[1:]):
        # Compare w1, w2 under the derived ranking; w1 must be <= w2.
        for a, b in zip(w1, w2):
            if a != b:
                if rank[a] > rank[b]:
                    return False
                break
        else:
            if len(w1) > len(w2):   # prefix violation
                return False
    return True


if __name__ == "__main__":
    print(alien_order(["wrt", "wrf", "er", "ett", "rftt"]))   # e.g. "wertf"
    print(_is_valid_order(["wrt", "wrf", "er", "ett", "rftt"],
                          alien_order(["wrt", "wrf", "er", "ett", "rftt"])))   # -> True

    print(alien_order(["z", "x"]))                             # e.g. "zx"
    print(alien_order(["z", "x", "z"]))                        # -> ""  (cycle z<x, x<z)
    print(alien_order(["abc", "ab"]))                          # -> ""  (invalid prefix)

    # Single word: any order of its letters is fine.
    print(_is_valid_order(["abc"], alien_order(["abc"])))      # -> True

    # Repeated identical words give no constraints; all letters still returned.
    print(sorted(alien_order(["aa", "aa"])))                   # -> ['a']

    # Batch validity check on solvable inputs.
    solvable = [
        ["wrt", "wrf", "er", "ett", "rftt"],
        ["z", "x"],
        ["ba", "bc", "ac", "cab"],
        ["abc"],
    ]
    print(all(_is_valid_order(ws, alien_order(ws)) for ws in solvable))   # -> True
    # Invalid inputs must return "".
    print(alien_order(["z", "x", "z"]) == "" and alien_order(["abc", "ab"]) == "")  # -> True
