"""
Group Anagrams
==============

PROBLEM PROMPT
--------------
Given an array of strings `strs`, group the anagrams together. You can return the
answer in any order.

An anagram is a word or phrase formed by rearranging the letters of a different
word or phrase, using all the original letters exactly once.

Example 1:
    Input:  strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    Output: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    Explanation:
        - "bat" has no other anagrams in the list.
        - "nat" and "tan" are anagrams of each other.
        - "ate", "eat", and "tea" are anagrams of each other.
        (The order of the groups and the order within a group do not matter.)

Example 2:
    Input:  strs = [""]
    Output: [[""]]

Example 3:
    Input:  strs = ["a"]
    Output: [["a"]]

Constraints:
    1 <= len(strs) <= 10^4
    0 <= len(strs[i]) <= 100
    strs[i] consists of lowercase English letters.
"""

from collections import defaultdict


def group_anagrams(strs):
    """
    Group strings that are anagrams of one another into shared buckets.

    APPROACH (Canonical Key via Sorted Characters)
    ----------------------------------------------
    Two words are anagrams exactly when they contain the same letters with the
    same frequencies. We need a "signature" that is IDENTICAL for anagrams but
    DIFFERENT for non-anagrams, so we can use it to bucket words together.

    The simplest such signature is the word's characters sorted alphabetically:
        "eat" -> "aet"
        "tea" -> "aet"
        "tan" -> "ant"
    All anagrams collapse to the same sorted string, while non-anagrams produce
    different ones. We use that sorted string as a dictionary KEY and append each
    original word to the list stored under its key. At the end, the dictionary's
    values are exactly the anagram groups.

    A defaultdict(list) lets us append to a key's list without first checking
    whether the key exists.

    (Alternative signature: a 26-length tuple of letter counts. That builds the
    key in O(k) instead of O(k log k) sorting time — see the complexity note — but
    sorting is simpler to write and fast enough for these constraints.)

    COMPLEXITY
    ----------
    Let n = number of words and k = the maximum word length.
    Time  : O(n * k log k) — for each of the n words we sort its k characters,
            which costs O(k log k). (The count-tuple variant would be O(n * k).)
    Space : O(n * k) — the dictionary stores every word once across all its
            buckets, plus the keys.

    Args:
        strs (list[str]): The list of strings to group.

    Returns:
        list[list[str]]: The anagram groups (in arbitrary order).
    """
    # Maps a canonical signature -> list of words sharing that signature.
    groups = defaultdict(list)

    for word in strs:
        # Sorting the characters yields the same key for all anagrams.
        # sorted() returns a list of chars, so join it back into a string key.
        key = "".join(sorted(word))
        groups[key].append(word)

    # The buckets themselves are the answer; keys are no longer needed.
    return list(groups.values())


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # -> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]] (order may vary)

    print(group_anagrams([""]))       # -> [[""]]
    print(group_anagrams(["a"]))      # -> [["a"]]
    print(group_anagrams(["abc", "bca", "cab", "xyz"]))
    # -> [["abc", "bca", "cab"], ["xyz"]] (order may vary)
