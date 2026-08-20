# Patterns Cheat Sheet

Day-before review. Each section: the template, the knob that changes between variants,
and the one thing that's usually the bug. Code is Python, matching the repo.

---

## 1. Backtracking

**Skeleton:** choose → recurse → un-choose. Snapshot with `path[:]` when recording
(a bare `path` aliases one list that empties as the recursion unwinds).

```python
def backtrack(start, path):
    record(path[:])                 # or check a completeness condition
    for i in range(start, len(nums)):
        path.append(nums[i])        # choose
        backtrack(i + 1, path)      # recurse
        path.pop()                  # un-choose
```

**The one knob that changes everything — how you recurse:**

| Problem | Recursive call | Effect |
|---|---|---|
| Subsets (78) | `backtrack(i + 1)` | each element ≤ once, no reordering |
| Combination Sum (39) | `backtrack(i)` | element **reusable**, no reordering |
| Permutations (46) | loop all + `used[]` | each once, **all** orderings |

- **Permutations** drop `start`; use a `used[]` array (or swap in place) because order matters.
- **Constraint-driven** (Generate Parentheses): no array/index — carry counters and
  only make *legal* moves (`open<n`, `close<open`). Prune at the choice, not the leaf.
- **Variable choices per position** (Letter Combinations): always advance `i+1`, branch
  over that position's choice set. Guard empty input → `[]` not `[""]`.

**Grid backtracking (Word Search):** 4-directional DFS from every cell; mark visited
**in place** (`board[r][c]="#"`), recurse, then **restore**. The restore *is* the
un-choose — forget it and cells leak.

> **Usual bug:** marking on the way in but not un-marking on the way out — especially an
> early `return` between the mark and the restore. Do all rejecting (bounds/visited/
> mismatch) *before* you mark, so the only code after the mark is recurse + unmark.

---

## 2. Binary Search

**Two templates. Pick by whether you want an exact value or a boundary.**

**(a) Exact match — closed interval `[lo, hi]`:**
```python
lo, hi = 0, len(nums) - 1
while lo <= hi:                     # <= : lo==hi is a real 1-element interval
    mid = lo + (hi - lo) // 2       # overflow-safe habit
    if nums[mid] == target: return mid
    elif nums[mid] < target: lo = mid + 1   # exclude mid → interval strictly shrinks
    else: hi = mid - 1
return -1
```

**(b) Boundary / leftmost-true — half-open convergence:**
```python
lo, hi = 0, len(nums)              # or [1, max] for search-on-answer
while lo < hi:                     # < : converge two pointers onto the boundary
    mid = lo + (hi - lo) // 2
    if feasible(mid): hi = mid     # keep mid as a live candidate (NOT mid-1)
    else: lo = mid + 1
return lo
```

**Which template each problem uses:**
- 704 exact, 33 exact (+ "which half is sorted?") → template (a)
- 153 find-min, 34 first/last, 875 Koko, 1011 ship → template (b)

**Variant cheats:**
- **Rotated search (33):** one half is always sorted. `nums[lo] <= nums[mid]` → left
  sorted. Check if target is in the sorted half's range; else go the other way.
- **Find min (153):** compare `nums[mid]` to **`nums[hi]`** (right end — left end is
  ambiguous). `>` → min is right (`lo=mid+1`); else `hi=mid`.
- **Search on the answer (Koko/ship):** search the *value range*, not an array. Needs
  (1) answer in a known integer range, (2) monotonic `feasible()`. Bounds = smallest
  *valid* answer (e.g. `lo=1`, not 0) and a provably feasible `hi`.
- **2D matrix (74):** treat as one flat sorted array; `row, col = divmod(mid, cols)`.

> **Usual bugs:** `<` vs `<=` (rotated: `nums[lo] <= nums[mid]` — equality when `lo==mid`);
> using `hi=mid-1` in a boundary search (discards the answer); `lo=0` in search-on-answer
> causing div-by-zero at `feasible(0)`; the compare must involve `mid` (endpoints-only
> can't decide which half of mid to keep).

---

## 3. Dynamic Programming

**The method (say it out loud):** reason about the **last decision** → recurrence →
base cases → memo → table → rolling variables.

**Counting vs optimizing — this picks your operator:**
- Counting paths → **sum**: `dp[i] = dp[i-1] + dp[i-2]` (Climbing Stairs)
- Optimizing a value → **max/min**: `dp[i] = max(dp[i-1], nums[i] + dp[i-2])` (House Robber)

**Rolling variables** (when `dp[i]` needs only the last 1–2 values → O(1) space):
```python
prev2, prev1 = base0, base1
for i in range(2, n + 1):
    prev2, prev1 = prev1, combine(prev1, prev2)
return prev1
```

**Shapes seen:**
- **1-D look-back-k:** Climbing Stairs, House Robber.
- **Reduce to a solved problem:** House Robber II (circle) = linear robber run twice
  (drop first house, drop last house), take the max.
- **Inner loop / choice set:** Coin Change (`dp[amt] = min over coins`), LIS.
- **Two-state:** Max Product Subarray (track running max *and* min — a negative flips them).
- **2-D grid/table:** Unique Paths, LCS, Edit Distance.

> **Usual bug:** wrong/missing base case; and don't pattern-match ("rob every other
> house" is wrong — trust the `max` recurrence, e.g. `[2,1,1,2]` → 4).

---

## 4. Trie (Prefix Tree)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None            # store the full word (or is_end=True)

def insert(root, word):
    node = root
    for ch in word:
        node = node.children.setdefault(ch, TrieNode())
    node.word = word
```

- **search** = walk; success only if you land on a node with `word`/`is_end`
  (path existing ≠ word — `search("app")` is False after inserting only `"apple"`).
- **startsWith** = same walk, skip the end check.
- **Wildcard `.` (211):** at a dot, DFS over **all** children; concrete letter = one step.
- **Word Search II (212):** build a trie of all words, do **one** grid DFS walking the
  trie in lockstep (drops the `×len(words)` factor). Record `node.word`, set it to
  `None` after (dedupe). Optional: prune dead leaf nodes.

> **Usual bug:** storing the end-marker as a key inside `children` — then a wildcard's
> `.values()` iterates over the sentinel. Keep `is_end`/`word` as a separate field.

---

## 5. Graphs

**BFS (shortest path in unweighted / level order):**
```python
q = deque([start]); seen = {start}
while q:
    for _ in range(len(q)):        # one layer at a time
        node = q.popleft()
        for nxt in neighbors(node):
            if nxt not in seen:
                seen.add(nxt); q.append(nxt)
    steps += 1
```
Multi-source: seed the queue with *all* sources at once (Rotting Oranges, Pacific Atlantic).

**Topological sort — Kahn's BFS (preferred; cycles fall out naturally):**
```python
indeg = [0]*n; adj = [[] for _ in range(n)]
for a, b in edges: adj[b].append(a); indeg[a] += 1   # edge b -> a
q = deque(i for i in range(n) if indeg[i] == 0)
order = []
while q:
    u = q.popleft(); order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
return order if len(order) == n else []   # short == cycle
```
- **Course Schedule (207):** return `len(order)==n`. **II (210):** return `order`.
- **Alien Dictionary (269):** *build the graph yourself* — compare adjacent words, first
  differing char gives edge `w1[i]->w2[i]`, `break`. Init indegree for **all** letters.
  Invalid-prefix trap: `w1` longer than `w2` but `w2` is its prefix → `""`.

**DFS cycle detection — three-color:**
```python
state = [0]*n                       # 0 unvisited, 1 on-path, 2 done
def has_cycle(u):
    if state[u] == 1: return True   # back edge onto current path
    if state[u] == 2: return False
    state[u] = 1
    if any(has_cycle(v) for v in adj[u]): return True
    state[u] = 2; return False
```
> A plain `visited` set can't tell "on my current path" (real cycle) from "seen earlier
> down another branch" (fine). Need the 1-vs-2 distinction.

**Union-Find (connectivity, cycle in undirected, components):**
```python
parent = list(range(n)); rank = [0]*n
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False           # already connected → cycle
    if rank[ra] < rank[rb]: ra, rb = rb, ra
    parent[rb] = ra
    if rank[ra] == rank[rb]: rank[ra] += 1
    return True
```

**Dijkstra (weighted shortest path, non-negative):** min-heap of `(dist, node)`, pop
smallest, skip stale entries, relax neighbors. Bellman-Ford / "K stops" (787): relax
edges a bounded number of times.

---

## 6. Interview reflexes (the process, not the pattern)

1. **Clarify first** — restate, ask input size / duplicates / empty / negatives, confirm output.
2. **Brute force out loud** → then optimize. State complexity of each.
3. **Think out loud the whole time** — Google grades communication and ambiguity handling.
4. **Test your own code** — walk a small example line by line before saying "done".
5. **Name your convention** ("closed interval `[lo,hi]`", "edge b→a") so choices follow from it.
6. **Verify your own expected outputs** — a wrong test annotation reads as a code bug (and vice-versa).

---

## 7. Complexity quick reference

| Pattern | Time | Space |
|---|---|---|
| Binary search | O(log n) | O(1) |
| Subsets | O(n·2ⁿ) | O(n) |
| Permutations | O(n·n!) | O(n) |
| Grid DFS / BFS | O(m·n) | O(m·n) |
| Trie op | O(L) | O(total chars) |
| Topo sort / graph traversal | O(V+E) | O(V+E) |
| Union-Find op | ~O(α(n)) ≈ O(1) | O(n) |
| 1-D DP (rolling) | O(n) | O(1) |
| 2-D DP | O(m·n) | O(m·n) → often O(n) |
