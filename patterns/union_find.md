# Union-Find (Disjoint Set Union)

**What it does:** tracks which elements are grouped together, and answers two
questions in nearly O(1) each:
- *"Are these two in the same group?"*
- *"Merge these two groups."*

**Reach for it when:** counting connected components, detecting a cycle in an
**undirected** graph, checking if a graph is a tree, or merging things
incrementally as edges/relations arrive. It shines over DFS/BFS when edges come
one at a time or you need repeated connectivity queries (it answers "connected?"
without re-traversing).

---

## The idea in one sentence

Each group is identified by **one representative (its "leader" / root)**.
Everything Union-Find does is find leaders and merge groups under a shared leader.

**Analogy — friend circles:** each circle has one designated leader (any fixed
member). Two people are in the same circle iff they name the *same* leader.

---

## The one array that runs everything: `parent`

We don't store whole groups — just, for each element, who points toward its leader:

```
parent[x] = the element just "above" x on the way to the leader
```

- A **leader points to itself** (`parent[x] == x`). That's how you know you've hit the top.
- **Start:** everyone is their own leader — n groups of one.

```
nodes:   0   1   2   3   4
parent:  0   1   2   3   4      (everyone points to themselves)
```

---

## The two operations

**`find(x)` — "who is x's leader?"** Walk up until someone points to themselves.

**`union(a, b)` — "put a and b in the same group":**
1. Find a's leader `ra` and b's leader `rb`.
2. Same leader → already together, do nothing.
3. Different → point one leader at the other. The groups are now merged.

> Key subtlety: `union` merges the **leaders**, not the two nodes directly.
> That's why joining any member of group A to any member of group B merges the
> *whole* groups.

---

## Template (with both speed-ups)

```python
parent = list(range(n))   # each node starts as its own leader
rank   = [0] * n          # approximate tree height per root

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression: point at grandparent
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False                    # already connected -> no merge
    if rank[ra] < rank[rb]:             # union by rank: short tree under tall
        ra, rb = rb, ra
    parent[rb] = ra
    if rank[ra] == rank[rb]:
        rank[ra] += 1
    return True                         # merged two distinct groups
```

`union` returns a **bool** on purpose — `True` = a real merge happened,
`False` = the two were already connected. That return value is the whole answer
to several problems (see below).

---

## Worked example — count components

`n = 5`, edges `[[0,1], [1,2], [3,4]]`.

```
start        parent: 0 1 2 3 4      groups: {0}{1}{2}{3}{4}
union(0,1)   parent: 0 0 2 3 4      groups: {0,1}{2}{3}{4}
union(1,2)   parent: 0 0 0 3 4      groups: {0,1,2}{3}{4}   # find(1)=0, find(2)=2, merge
union(3,4)   parent: 0 0 0 3 3      groups: {0,1,2}{3,4}
```

Result: **2 groups.** Notice `union(1,2)` merged leaders 0 and 2 — so all of
{0,1,2} joins, not just node 2.

**Counting trick:** start a counter at `n`, subtract 1 on every *real* merge
(when `union` returns `True`). Redundant edges don't change it.

```
components = n - (number of real merges)      # 5 - 3 = 2
```

---

## The two speed-ups (why it's ~O(1))

Without them, trees can grow tall and `find` gets slow. Two fixes:

1. **Path compression** (inside `find`): while climbing, point nodes closer to the
   root. The one-line "path halving" form is `parent[x] = parent[parent[x]]`. Over
   time the tree flattens — most nodes point almost directly at the leader.
2. **Union by rank**: hang the **shorter** tree under the **taller** one, never the
   reverse, so trees stay shallow. `rank` is a rough height estimate.

Together: amortized **α(n)** (inverse Ackermann), which is < 5 for any realistic n
— effectively constant.

---

## Complexity

| | Time | Space |
|---|---|---|
| `find` / `union` | ~O(α(n)) ≈ O(1) amortized | — |
| Whole problem (n nodes, E edges) | O((n + E) · α(n)) ≈ O(n + E) | O(n) |

---

## The `union`-returns-bool payoffs

The `True`/`False` from `union` directly solves a family of problems:

- **Number of Connected Components (323):** `components = n - (# True unions)`.
- **Redundant Connection (684):** the **first** edge whose `union` returns `False`
  (endpoints already connected) is the cycle-closing edge → return it.
- **Graph Valid Tree (261):** it's a tree iff `len(edges) == n - 1` **and** every
  `union` returns `True` (no edge ever connects an already-connected pair, i.e. no
  cycle). One `False` → not a tree.

---

## 30-second mental summary

- **Each group = a tree with one root (leader).**
- **`find`** = walk up to the root. **`union`** = point one root at the other; skip if same.
- **Same root ⇒ same group.**
- **Count** = `n − real merges`.
- **Path compression + union by rank** = keep trees flat → basically constant time.

The reason it feels magical: a single `parent` array encodes arbitrarily many
groups, and merging two groups of any size is **one pointer change** — because you
only ever touch the roots, never the members.

---

*See [number_of_connected_components.py](../google/number_of_connected_components.py)
for a full worked implementation.*
