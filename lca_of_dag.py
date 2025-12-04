"""
Problem: 
    Given a Directed Acyclic Graph (DAG) and two vertices u and v, 
    find their Lowest Common Ancestors (LCAs).

    A node x is a common ancestor of u and v if there is a directed path 
    from x to u and from x to v. A Lowest Common Ancestor is a common 
    ancestor that is not an ancestor of any other common ancestor.

Intuition:
    1. To find common ancestors, we need to traverse "upwards". 
       So we build a reverse graph where edges point from a node to its parents.
    2. Find all ancestors of u and all ancestors of v by walking this reverse graph.
    3. Their intersection gives us candidate common ancestors.
    4. To filter only the *lowest* ones, we check which candidates are ancestors of others.
       - Precompute descendants for each node (memoized DFS).
       - A candidate is not lowest if it contains another candidate in its descendants.

Time Complexity:
    - Building reverse graph: O(V + E)
    - Finding ancestors: O(V + E)
    - Computing descendants with memoization: O(V + E) total
    - Filtering candidates: O(C^2) in worst case (C = number of common ancestors)
    Overall: O(V + E + C^2), usually dominated by graph traversal.

Space Complexity:
    - Reverse graph + memoization + visited sets: O(V + E)
    - Ancestors / descendants storage: O(V^2) worst-case in a dense DAG

Solution below is optimized for sparse DAGs (most practical cases).
"""

from collections import defaultdict
from typing import Dict, List, Set


def find_ancestors(rev_graph: Dict[int, List[int]], node: int) -> Set[int]:
    """Return all ancestors of a node using DFS on the reverse graph."""
    visited = set()
    stack = [node]
    while stack:
        curr = stack.pop()
        for parent in rev_graph[curr]:
            if parent not in visited:
                visited.add(parent)
                stack.append(parent)
    visited.add(node)  # include the node itself
    return visited


def find_descendants(graph: Dict[int, List[int]], node: int, memo: Dict[int, Set[int]]) -> Set[int]:
    """Return all descendants of a node using DFS with memoization."""
    if node in memo:
        return memo[node]

    desc = set()
    for nei in graph[node]:
        desc.add(nei)
        desc |= find_descendants(graph, nei, memo)
    memo[node] = desc
    return desc


def find_LCAs(graph: Dict[int, List[int]], u: int, v: int) -> Set[int]:
    """Main function to compute LCAs in a DAG."""
    # 1. Build reverse graph
    rev_graph = defaultdict(list)
    for src in graph:
        for dst in graph[src]:
            rev_graph[dst].append(src)

    # 2. Find ancestors of u and v
    ancestors_u = find_ancestors(rev_graph, u)
    ancestors_v = find_ancestors(rev_graph, v)

    # 3. Common ancestors
    candidates = ancestors_u & ancestors_v

    # 4. Precompute descendants
    memo = {}
    for node in graph:
        if node not in memo:
            find_descendants(graph, node, memo)

    # 5. Filter for lowest common ancestors
    LCAs = set()
    for c in candidates:
        if not any((other in memo[c]) for other in candidates if other != c):
            LCAs.add(c)

    return LCAs


# -----------------------------
# Test Cases
# -----------------------------
if __name__ == "__main__":
    # Example DAG:
    # 0 → 2, 0 → 3
    # 1 → 2, 1 → 3
    # 2 → 6, 3 → 6
    # 4 → 0, 5 → 1
    graph = {
        0: [2, 3],
        1: [2, 3],
        2: [6],
        3: [6],
        4: [0],
        5: [1],
        6: []
    }

    print("LCA of (2, 3):", find_LCAs(graph, 2, 3))  # Expected {0, 1}
    print("LCA of (6, 6):", find_LCAs(graph, 6, 6))  # Expected {6}
    print("LCA of (4, 5):", find_LCAs(graph, 4, 5))  # Expected ∅ (no common ancestor)
    print("LCA of (2, 6):", find_LCAs(graph, 2, 6))  # Expected {2}
