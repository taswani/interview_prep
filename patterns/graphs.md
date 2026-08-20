# Graphs

**What it is:** a set of **nodes** connected by **edges**. Tons of problems are
secretly graphs — a grid (each cell is a node, neighbors are edges), course
prerequisites, friend networks, word-ladder transformations. The skill is
*recognizing* the graph, then picking the right traversal.

**Reach for it when:** the problem is about **connectivity** ("are these linked",
"how many groups"), **reachability / paths** ("can you get from A to B",
"shortest path"), **ordering under dependencies** ("do X before Y"), or you have a
grid/map and move between neighbors.

---

## Step 0 — recognize and represent

First ask: **what are the nodes, what are the edges?** For a grid it's implicit
(cell → its 4 neighbors). For an explicit graph, build one of these:

```python
# Adjacency list (the default — sparse, fast to iterate neighbors)
adj = [[] for _ in range(n)]
for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)          # BOTH directions if UNDIRECTED; one way if directed
```

> **The #1 setup bug:** forgetting to add both directions for an undirected graph
> (or adding both for a *directed* one). Decide directed-vs-undirected first.

Directed vs undirected, weighted vs unweighted, cyclic vs acyclic — these four
facts decide which tool below you use.

---

## The idea in one sentence

**Explore outward from a starting node, keeping a `visited` set so you never
process the same node twice.** Every graph algorithm here is a variation on that.

**Analogy — exploring a cave system:** you walk through tunnels (edges) between
caverns (nodes), and you drop a chalk mark in each cavern you enter (`visited`) so
you don't wander in circles. **DFS** = follow one tunnel as deep as it goes, then
back up. **BFS** = explore all caverns one step away, then all two steps away, ….

---

## The two traversals

### DFS — go deep first

```python
visited = set()
def dfs(node):
    visited.add(node)
    for nxt in adj[node]:
        if nxt not in visited:
            dfs(nxt)
```

Use for: connectivity, "flood fill" a region, cycle detection, anything where
depth doesn't matter. Simple to write recursively. Watch recursion depth on huge
graphs.

### BFS — go wide, layer by layer

```python
from collections import deque
def bfs(start):
    seen = {start}
    q = deque([start])
    steps = 0
    while q:
        for _ in range(len(q)):     # process exactly one layer
            node = q.popleft()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        steps += 1
```

Use for: **shortest path in an UNWEIGHTED graph** (fewest edges/steps). The
layer-by-layer `for _ in range(len(q))` is what lets you count distance.

> **Mark visited when you ENQUEUE, not when you dequeue.** Marking at dequeue lets
> the same node get added to the queue many times before it's processed —
> blowing up time and sometimes correctness.

**Multi-source BFS:** seed the queue with *all* starting nodes at once. Great for
"spread from every source simultaneously" — Rotting Oranges, Pacific Atlantic,
shortest distance from all buildings.

---

## Decision guide — which tool?

| The question is about… | Use |
|---|---|
| Connected? How many components? | DFS/BFS flood fill, or **Union-Find** |
| Shortest path, **unweighted** | **BFS** (layers = distance) |
| Shortest path, **weighted, non-negative** | **Dijkstra** (min-heap) |
| Shortest path, weights can be negative / "≤ K stops" | **Bellman-Ford** (relax edges K times) |
| Ordering with prerequisites (DAG) | **Topological sort** (Kahn's BFS or DFS) |
| Cycle in a **directed** graph | DFS **three-color**, or Kahn's (leftover nodes) |
| Cycle in an **undirected** graph / incremental merges | **Union-Find** |

---

## Topological sort (ordering under dependencies)

For a **DAG**: produce an order where every node comes before the ones that depend
on it. Kahn's BFS is the robust choice — cycles fall out naturally.

```python
indeg = [0] * n
adj = [[] for _ in range(n)]
for a, b in edges:                  # edge b -> a means "b before a"
    adj[b].append(a)
    indeg[a] += 1

q = deque(i for i in range(n) if indeg[i] == 0)   # no prerequisites
order = []
while q:
    u = q.popleft()
    order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

# len(order) < n  ->  a cycle blocked some nodes
return order if len(order) == n else []
```

- **Course Schedule (207):** return `len(order) == n`.
- **Course Schedule II (210):** return `order`.
- **Alien Dictionary (269):** *build the graph yourself* — compare adjacent words,
  first differing char gives an edge, then topo-sort.

---

## Directed cycle detection — DFS three-color

A directed graph has a cycle iff DFS finds a **back edge** to a node still on the
current path. You need three states, not a plain visited set:

```python
state = [0] * n     # 0 = unvisited, 1 = on current path, 2 = fully done
def has_cycle(u):
    if state[u] == 1: return True    # back edge -> cycle
    if state[u] == 2: return False   # already cleared
    state[u] = 1
    if any(has_cycle(v) for v in adj[u]): return True
    state[u] = 2
    return False
```

> A single `visited` set can't tell **"on my current path"** (a real cycle) from
> **"seen earlier down another branch"** (perfectly fine). The 1-vs-2 distinction
> is the whole point.

---

## Weighted shortest path — Dijkstra

Non-negative weights. Greedily settle the closest unsettled node using a min-heap.

```python
import heapq
def dijkstra(n, adj, src):          # adj[u] = list of (weight, v)
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]                 # (distance, node)
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:            # stale entry -> skip
            continue
        for w, v in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

- **Network Delay Time (743):** Dijkstra from the source, answer = max finite dist.
- **Cheapest Flights within K Stops (787):** Bellman-Ford / BFS with a stop counter
  (Dijkstra needs a tweak when a hop limit is involved).

> Dijkstra requires **non-negative** weights. Negative edges → use Bellman-Ford.

---

## Grids are graphs

A common disguise. Cell `(r, c)` is a node; its edges are the in-bounds neighbors.

```python
for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == ...:
        # visit (nr, nc)
```

- **Number of Islands / connected regions:** DFS/BFS flood fill.
- **Shortest path through a grid:** BFS (unweighted) — Rotting Oranges, Shortest Bridge.
- Mark visited in place (flip the cell) or with a `visited` set — same idea as the
  grid backtracking pattern, but here you usually **don't** un-mark (you want to
  visit each cell once, not explore all paths).

---

## Complexity

Let V = nodes, E = edges.

| Algorithm | Time | Space |
|---|---|---|
| DFS / BFS | O(V + E) | O(V) |
| Topological sort | O(V + E) | O(V + E) |
| Dijkstra (binary heap) | O((V + E) log V) | O(V + E) |
| Bellman-Ford | O(V · E) | O(V) |
| Union-Find op | ~O(α(n)) ≈ O(1) | O(V) |

---

## The usual bugs

- **Undirected edge added one way** (or directed added both). Set this first.
- **BFS marking visited at dequeue** instead of enqueue → duplicates in the queue.
- **DFS cycle detection with a plain visited set** → can't distinguish a real cycle
  from a re-visit; you need three colors.
- **Not counting layers** in BFS when you need a distance (`for _ in range(len(q))`).
- **Dijkstra with negative weights** → wrong answers; use Bellman-Ford.
- **Recursion depth** on DFS over a huge/linear graph → convert to an iterative
  stack.

---

## 30-second mental summary

1. **Spot the graph:** what are nodes, what are edges? Directed? Weighted? Cyclic?
2. **Connectivity / components** → DFS/BFS flood fill or **Union-Find**.
3. **Shortest path:** unweighted → **BFS**; weighted ≥0 → **Dijkstra**; negative/K-stops → **Bellman-Ford**.
4. **Dependencies / ordering** → **topological sort**.
5. **Cycle:** directed → three-color DFS; undirected → Union-Find.
6. Always keep a **`visited`** set, and **mark on enqueue** in BFS.

Every one of these is "explore outward, don't repeat yourself." Pick the traversal
that matches what the question measures.

---

*Related: [union_find.md](union_find.md) for connectivity/merge problems.
Worked implementations:
[number_of_islands.py](../google/number_of_islands.py),
[clone_graph.py](../google/clone_graph.py),
[course_schedule.py](../google/course_schedule.py),
[course_schedule_ii.py](../google/course_schedule_ii.py),
[alien_dictionary.py](../google/alien_dictionary.py),
[number_of_connected_components.py](../google/number_of_connected_components.py).*
