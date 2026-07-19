"""
Problem: Word Ladder

A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words such that:
  - The first word is beginWord.
  - The last word is endWord.
  - Only one letter can be changed at a time.
  - Each transformed word must exist in wordList.

Return the length of the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Example 1:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: One shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog", length = 5.

Example 2:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: 0
Explanation: The endWord "cog" is not in wordList, so no transformation is possible.
"""

from typing import List
from collections import deque, defaultdict


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        
        length = len(beginWord)

        combo_list = defaultdict(list)

        for word in wordList:
            for idx in range(length):
                pattern = word[:idx] + "*" + word[idx + 1:]
                combo_list[pattern].append(word)
            
        queue = [beginWord]
        visited = {beginWord}
        res = 1

        while queue:
            for _ in range(len(queue)):
                
                curr_word = queue.pop(0)

                for idx in range(length):
                    pattern = curr_word[:idx] + "*" + curr_word[idx + 1:]

                    for neighbor in combo_list[pattern]:
                        if neighbor == endWord:
                            return res + 1
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                
            res += 1
        
        return 0


"""
Time Complexity:
- Preprocessing: For each word (N words, word length L), we create L patterns → O(N * L).
- BFS: Each word is processed once, and for each we generate L patterns → O(N * L).
- Total: O(N * L), where N = number of words in wordList, L = length of each word.

Space Complexity:
- Dictionary stores all patterns: O(N * L).
- Queue and visited set: O(N).
- Total: O(N * L).
"""


# ------------------------
# Test cases
# ------------------------
if __name__ == "__main__":
    solution = Solution()

    begin1, end1, words1 = "hit", "cog", ["hot","dot","dog","lot","log","cog"]
    print("Test 1:", solution.ladderLength(begin1, end1, words1), "Expected: 5")

    begin2, end2, words2 = "hit", "cog", ["hot","dot","dog","lot","log"]
    print("Test 2:", solution.ladderLength(begin2, end2, words2), "Expected: 0")

    begin3, end3, words3 = "a", "c", ["a","b","c"]
    print("Test 3:", solution.ladderLength(begin3, end3, words3), "Expected: 2")

    begin4, end4, words4 = "lost", "miss", ["most","mist","miss","lost","fist","fish"]
    print("Test 4:", solution.ladderLength(begin4, end4, words4), "Expected: 4")
