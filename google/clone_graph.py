"""
Clone Graph
===========

PROBLEM PROMPT
--------------
Given a reference of a node in a connected undirected graph, return a deep copy
(clone) of the graph.

Each node in the graph contains a value (int) and a list of its neighbors.

    class Node:
        def __init__(self, val, neighbors):
            self.val = val
            self.neighbors = neighbors

Test case format:
    For simplicity, each node's value is the same as the node's index (1-indexed).
    For example, the first node with val == 1, the second node with val == 2, and
    so on. The graph is represented in the test case using an adjacency list.

    An adjacency list is a collection of unordered lists used to represent a
    finite graph. Each list describes the set of neighbors of a node in the graph.

    The given node will always be the first node with val == 1. You must return
    the COPY of the given node as a reference to the cloned graph.

Example 1:
    Input:  adjList = [[2, 4], [1, 3], [2, 4], [1, 3]]
    Output: [[2, 4], [1, 3], [2, 4], [1, 3]]
    Explanation: There are 4 nodes in the graph.
        1st node (val = 1): neighbors are 2 and 4.
        2nd node (val = 2): neighbors are 1 and 3.
        3rd node (val = 3): neighbors are 2 and 4.
        4th node (val = 4): neighbors are 1 and 3.

Example 2:
    Input:  adjList = [[]]
    Output: [[]]
    Explanation: The graph has one node with no neighbors.

Example 3:
    Input:  adjList = []
    Output: []
    Explanation: The graph is empty (there are no nodes).

Constraints:
    The number of nodes in the graph is in the range [0, 100].
    1 <= Node.val <= 100
    Node.val is unique for each node.
    There are no repeated edges and no self-loops in the graph.
    The graph is connected and all nodes can be reached starting from the given node.
"""


class Node:
    """A node in an undirected graph."""

    def __init__(self, val=0, neighbors=None):
        self.val = val
        # List of adjacent Node objects; default to empty to avoid the mutable
        # default-argument pitfall.
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node):
    """
    Return a deep copy of a connected undirected graph given one of its nodes.

    APPROACH (DFS + Hash Map of Originals -> Clones)
    ------------------------------------------------
    A deep copy means we must create a brand-new Node for every original node
    and rebuild the neighbor links so the copy points only at other copies, never
    at the originals.

    The central challenge is that graphs contain CYCLES (e.g. node 1 <-> node 2).
    A naive recursion would clone node 1, then clone its neighbor node 2, which
    in turn lists node 1 as a neighbor — sending us into infinite recursion. We
    also must ensure each original node is cloned EXACTLY once, so that shared
    neighbors end up pointing at the same clone rather than duplicate copies.

    A hash map solves both problems at once:

        cloned: original Node -> its clone Node

    We do a depth-first traversal. For each original node we visit:
      1. If it's already in `cloned`, we've made its copy before — return that
         existing clone immediately. This both prevents infinite loops on cycles
         and guarantees one clone per node.
      2. Otherwise, create its clone and record it in the map BEFORE recursing
         into neighbors. Registering it first is what breaks cycles: when the
         recursion comes back around to this node, step 1 finds it.
      3. Recursively clone each neighbor and append the returned clones to this
         clone's neighbor list.

    COMPLEXITY
    ----------
    Time  : O(V + E) — we visit each of the V nodes once and process each of the
            E edges once (each undirected edge is looked at from both endpoints,
            which is still O(E)).
    Space : O(V) — the hash map holds one entry per node, and the DFS recursion
            stack can go up to O(V) deep in the worst case.

    Args:
        node (Node | None): A reference to any node in the graph, or None if the
            graph is empty.

    Returns:
        Node | None: The corresponding node in the deep-copied graph, or None.
    """
    # An empty graph clones to nothing.
    if node is None:
        return None

    # Maps each original node to its freshly created clone.
    cloned = {}

    def dfs(original):
        # Already cloned this node -> return the existing clone (handles cycles
        # and shared neighbors, ensuring exactly one clone per original).
        if original in cloned:
            return cloned[original]

        # Create the clone (without neighbors yet) and register it IMMEDIATELY,
        # before recursing, so cycles back to this node terminate.
        copy = Node(original.val)
        cloned[original] = copy

        # Clone each neighbor and wire up the copy's neighbor list.
        for neighbor in original.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)


# ---------------------------------------------------------------------------
# Helper functions (for the sanity checks below — not part of the solution).
# ---------------------------------------------------------------------------
def build_graph(adj_list):
    """
    Build a graph from a 1-indexed adjacency list and return node 1 (or None).
    adj_list[i] holds the neighbor values of the node with val == i + 1.
    """
    if not adj_list:
        return None

    # Create all nodes first so edges can reference them.
    nodes = {i + 1: Node(i + 1) for i in range(len(adj_list))}
    for i, neighbors in enumerate(adj_list):
        nodes[i + 1].neighbors = [nodes[v] for v in neighbors]
    return nodes[1]


def to_adj_list(node):
    """Convert a graph back into a sorted 1-indexed adjacency list for printing."""
    if node is None:
        return []

    # BFS/DFS to collect every node.
    seen = {}
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.val in seen:
            continue
        seen[cur.val] = cur
        for nb in cur.neighbors:
            if nb.val not in seen:
                stack.append(nb)

    # Emit neighbor-value lists in order of node value.
    return [sorted(nb.val for nb in seen[v].neighbors) for v in sorted(seen)]


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    g1 = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
    print(to_adj_list(clone_graph(g1)))  # -> [[2, 4], [1, 3], [2, 4], [1, 3]]

    g2 = build_graph([[]])
    print(to_adj_list(clone_graph(g2)))  # -> [[]]

    g3 = build_graph([])
    print(to_adj_list(clone_graph(g3)))  # -> []

    # Verify it is truly a DEEP copy: the clone's node objects differ from the
    # originals even though the structure matches.
    original = build_graph([[2], [1]])
    copy = clone_graph(original)
    print(original is copy)  # -> False (different objects, same shape)
