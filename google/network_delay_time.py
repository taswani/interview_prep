"""
Network Delay Time
==================

PROBLEM PROMPT
--------------
You are given a network of `n` nodes, labeled from 1 to n. You are also given
`times`, a list of travel times as directed edges times[i] = (u_i, v_i, w_i),
where u_i is the source node, v_i is the target node, and w_i is the time it
takes for a signal to travel from source to target.

We will send a signal from a given node `k`. Return the MINIMUM time it takes for
all the n nodes to receive the signal. If it is impossible for all the n nodes to
receive the signal, return -1.

Example 1:
    Input:  times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
    Output: 2
    Explanation: signal from 2 reaches 1 (t=1), 3 (t=1), then 4 via 3 (t=2). The
                 last node receives it at time 2.
Example 2:
    Input:  times = [[1,2,1]], n = 2, k = 1   -> Output: 1
Example 3:
    Input:  times = [[1,2,1]], n = 2, k = 2   -> Output: -1
    Explanation: node 1 can never be reached from node 2.

Constraints:
    1 <= k <= n <= 100
    1 <= len(times) <= 6000
    times[i].length == 3
    1 <= u_i, v_i <= n
    u_i != v_i
    0 <= w_i <= 100
    All the pairs (u_i, v_i) are unique. (i.e., no multiple edges.)
"""

import heapq
from collections import defaultdict


def network_delay_time(times, n, k):
    """
    Return the time for a signal from node `k` to reach all nodes, or -1.

    APPROACH (Dijkstra -- single-source shortest paths, non-negative weights)
    ------------------------------------------------------------------------
    "Time for ALL nodes to receive the signal" = the time the LAST node gets it =
    the MAXIMUM over all nodes of the shortest travel time from k to that node. So
    we compute the shortest distance from k to every node, then take the max. If
    any node is unreachable (distance stays infinite), return -1.

    Because edge weights are NON-NEGATIVE, Dijkstra's algorithm gives those
    shortest distances. The core idea: always settle the CLOSEST not-yet-finalized
    node next. Once we pop a node with the smallest known distance, that distance
    is final -- no later path can beat it, since every remaining edge only ADDS
    non-negative weight. We use a MIN-HEAP to always pull the closest frontier
    node in O(log V).

    THE ALGORITHM:
      1. Build an adjacency list: adj[u] = list of (weight, v) out-edges.
      2. dist[node] = best known time from k; unknown = infinity, dist[k] = 0.
         Push (0, k) onto the heap.
      3. Pop the smallest (d, u). If d is stale (d > dist[u], meaning we already
         found a shorter way to u), skip it -- this "lazy deletion" is why we can
         leave outdated entries in the heap instead of updating them in place.
      4. Otherwise RELAX each out-edge: if going through u reaches v faster
         (d + w < dist[v]), update dist[v] and push (dist[v], v).
      5. When the heap empties, dist holds the shortest time to every reachable
         node.

    THE ANSWER: if every node has a finite dist, return max(dist over all nodes);
    otherwise some node was never reached -> return -1.

    WHY LAZY DELETION (skipping stale entries): a node can be pushed multiple times
    as we find progressively shorter routes to it. Rather than find-and-update the
    old heap entry (costly), we just leave it; when it eventually pops, its
    distance is larger than the finalized dist[u], so the `d > dist[u]` guard
    discards it. Each node is finalized exactly once.

    COMPLEXITY
    ----------
    Let V = n and E = len(times).
    Time  : O(E log V) -- each edge can trigger a heap push, each push/pop is
            O(log V). (Sometimes written O((V + E) log V).)
    Space : O(V + E) -- adjacency list, dist array, and heap.

    Args:
        times (list[list[int]]): Directed edges [u, v, w].
        n (int): Number of nodes (labeled 1..n).
        k (int): The source node.

    Returns:
        int: Time for all nodes to receive the signal, or -1 if impossible.
    """
    # adj[u] = list of (weight, neighbor) for edges leaving u.
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((w, v))

    # Shortest known time from k to each node; unknown = infinity.
    dist = {node: float("inf") for node in range(1, n + 1)}
    dist[k] = 0

    # Min-heap of (distance_so_far, node); always expand the closest frontier node.
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                 # stale entry -> a shorter path already settled u
        for w, v in adj[u]:
            nd = d + w
            if nd < dist[v]:         # relax: found a faster route to v
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    # The signal reaches everyone only if every node has a finite distance.
    slowest = max(dist.values())
    return slowest if slowest < float("inf") else -1


if __name__ == "__main__":
    # Quick sanity checks.
    print(network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))   # -> 2
    print(network_delay_time([[1, 2, 1]], 2, 1))                          # -> 1
    print(network_delay_time([[1, 2, 1]], 2, 2))                          # -> -1 (node 1 unreachable)
    print(network_delay_time([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1))   # -> 3 (1->2->3 = 3 < 4)
    print(network_delay_time([[1, 2, 1], [2, 3, 7], [1, 3, 4], [2, 4, 2], [3, 4, 1]], 4, 1))
    # -> 4  (dist: {1:0, 2:1, 4:3, 3:4}; the slowest node to hear is node 3 at t=4)
    print(network_delay_time([], 1, 1))                                   # -> 0 (source is the only node)

    # Cross-check Dijkstra against a Bellman-Ford baseline on random graphs.
    def bellman_ford(times, n, k):
        dist = {node: float("inf") for node in range(1, n + 1)}
        dist[k] = 0
        for _ in range(n - 1):
            for u, v, w in times:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        slowest = max(dist.values())
        return slowest if slowest < float("inf") else -1

    import random
    rng = random.Random(0)
    ok = True
    for _ in range(500):
        n = rng.randint(1, 8)
        pairs = [(u, v) for u in range(1, n + 1) for v in range(1, n + 1) if u != v]
        chosen = rng.sample(pairs, rng.randint(0, len(pairs)))
        times = [[u, v, rng.randint(0, 10)] for u, v in chosen]
        k = rng.randint(1, n)
        if network_delay_time([e[:] for e in times], n, k) != bellman_ford(times, n, k):
            ok = False
    print(ok)                                                             # -> True
