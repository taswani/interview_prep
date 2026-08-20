"""
Number of Connected Components in an Undirected Graph
=====================================================

PROBLEM PROMPT
--------------
You have a graph of `n` nodes labeled from 0 to n - 1. You are given an integer
`n` and a list of `edges` where edges[i] = [a_i, b_i] indicates that there is an
UNDIRECTED edge between a_i and b_i in the graph.

Return the number of CONNECTED COMPONENTS in the graph.

(A connected component is a maximal set of nodes such that each pair is connected
by some path, and which is connected to no additional nodes outside the set.)

Example 1:
    Input:  n = 5, edges = [[0, 1], [1, 2], [3, 4]]
    Output: 2
    Explanation: {0, 1, 2} form one component, {3, 4} form another.
Example 2:
    Input:  n = 5, edges = [[0, 1], [1, 2], [2, 3], [3, 4]]
    Output: 1

Constraints:
    1 <= n <= 2000
    0 <= len(edges) <= 10000
    edges[i].length == 2
    0 <= a_i <= b_i < n
    a_i != b_i
    There are no repeated edges.
"""


def count_components(n, edges):
    """
    Return the number of connected components using Union-Find (DSU).

    APPROACH (Union-Find / Disjoint Set Union)
    ------------------------------------------
    Union-Find maintains a collection of disjoint sets and answers "are these two
    elements in the same set?" plus "merge these two sets" in nearly O(1) each.
    That is exactly what counting components needs: every node starts in its own
    set, we merge the sets joined by each edge, and the number of sets left at the
    end is the number of components.

    THE DATA STRUCTURE:
      - parent[x]: each set is a tree; parent[x] points toward the set's
        representative ("root"). Initially parent[x] = x -- every node is its own
        root, so we start with n singleton sets.
      - find(x): follow parent pointers up to the root; two nodes are in the same
        set iff they share a root.
      - union(a, b): link the root of one set under the root of the other,
        merging them into a single set.

    THE COMPONENT COUNT -- the neat part. Start a counter at n (n separate sets).
    Each edge calls union; if that union actually MERGES two DIFFERENT sets, the
    number of sets drops by one, so we decrement the counter. If an edge connects
    two nodes ALREADY in the same set (a redundant edge / cycle), union changes
    nothing and the counter stays put. So:

        components = n - (number of unions that merged two distinct sets)

    THE TWO OPTIMIZATIONS that make each operation ~O(1):
      - PATH COMPRESSION (in find): after locating the root, flatten the path so
        the nodes point closer to the root, making future finds fast. Here we do
        the "path halving" form: parent[x] = parent[parent[x]] as we climb.
      - UNION BY RANK: attach the shorter tree under the taller one so trees stay
        shallow (never let a tall tree hang off a short one). `rank` approximates
        tree height.
    Together these give an amortized inverse-Ackermann factor alpha(n), which is
    effectively constant for any n you will ever see.

    (Alternative: build an adjacency list and count components with DFS/BFS in
    O(n + E). Union-Find is the natural fit when edges arrive incrementally or you
    also need connectivity queries; both are accepted here.)

    COMPLEXITY
    ----------
    Let n = nodes and E = len(edges).
    Time  : O((n + E) * alpha(n)) ~ O(n + E) -- near-linear.
    Space : O(n) for the parent and rank arrays.

    Args:
        n (int): Number of nodes (labeled 0..n-1).
        edges (list[list[int]]): Undirected edges.

    Returns:
        int: The number of connected components.
    """
    parent = list(range(n))   # each node is initially its own root
    rank = [0] * n            # approximate tree height per root

    def find(x):
        # Climb to the root, halving the path along the way (compression).
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # point x at its grandparent
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False      # already connected -> no merge happened
        # Attach the shorter tree under the taller one (union by rank).
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True           # merged two distinct sets

    components = n
    for a, b in edges:
        if union(a, b):       # only real merges reduce the component count
            components -= 1
    return components


def count_components_dfs(n, edges):
    """
    Same answer via DFS over an adjacency list -- the alternative worth knowing.

    APPROACH (Traversal)
    --------------------
    Build an undirected adjacency list, then walk the graph: iterate nodes 0..n-1,
    and each time we find an UNVISITED node, that node begins a NEW component --
    increment the count and DFS to mark every node reachable from it as visited.
    The number of times we launch a fresh DFS equals the number of components.

    COMPLEXITY
    ----------
    Time  : O(n + E).   Space : O(n + E) for the adjacency list + visited set
            (+ recursion depth).

    Args:
        n (int): Number of nodes.
        edges (list[list[int]]): Undirected edges.

    Returns:
        int: The number of connected components.
    """
    adjacency = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)   # undirected: add both directions

    visited = [False] * n

    def dfs(node):
        visited[node] = True
        for nxt in adjacency[node]:
            if not visited[nxt]:
                dfs(nxt)

    components = 0
    for node in range(n):
        if not visited[node]:
            components += 1       # a new, previously-unreached component
            dfs(node)
    return components


if __name__ == "__main__":
    # Quick sanity checks.
    print(count_components(5, [[0, 1], [1, 2], [3, 4]]))              # -> 2
    print(count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]))      # -> 1
    print(count_components(4, []))                                     # -> 4 (all isolated)
    print(count_components(1, []))                                     # -> 1
    print(count_components(6, [[0, 1], [2, 3], [4, 5]]))             # -> 3 (three pairs)
    print(count_components(3, [[0, 1], [1, 2], [0, 2]]))            # -> 1 (redundant edge)

    # The DFS variant returns the same answers.
    cases = [
        (5, [[0, 1], [1, 2], [3, 4]]),
        (5, [[0, 1], [1, 2], [2, 3], [3, 4]]),
        (4, []),
        (1, []),
        (6, [[0, 1], [2, 3], [4, 5]]),
        (3, [[0, 1], [1, 2], [0, 2]]),
    ]
    print(all(count_components(n, e) == count_components_dfs(n, e) for n, e in cases))  # -> True

    # Randomized cross-check between the two approaches.
    import random
    rng = random.Random(0)
    ok = True
    for _ in range(500):
        n = rng.randint(1, 12)
        possible = [(i, j) for i in range(n) for j in range(i + 1, n)]
        edges = rng.sample(possible, rng.randint(0, len(possible)))
        if count_components(n, edges) != count_components_dfs(n, edges):
            ok = False
    print(ok)                                                          # -> True
