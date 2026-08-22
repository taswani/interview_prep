"""
Cheapest Flights Within K Stops
===============================

PROBLEM PROMPT
--------------
There are `n` cities connected by some number of flights. You are given an array
`flights` where flights[i] = [from_i, to_i, price_i] indicates that there is a
flight from city from_i to city to_i with cost price_i.

You are also given three integers `src`, `dst`, and `k`. Return the CHEAPEST
price from `src` to `dst` with AT MOST `k` STOPS. If there is no such route,
return -1.

Example 1:
    Input:  n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
            src = 0, dst = 3, k = 1
    Output: 700
    Explanation: the cheapest with at most 1 stop is 0 -> 1 -> 3 = 700. The route
                 0 -> 1 -> 2 -> 3 costs only 500 but uses 2 stops (not allowed).
Example 2:
    Input:  n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=1
    Output: 200   (0 -> 1 -> 2, one stop)
Example 3:
    Input:  n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=0
    Output: 500   (no stops allowed, must fly direct)

Constraints:
    1 <= n <= 100
    0 <= len(flights) <= (n * (n - 1) / 2)
    flights[i].length == 3
    0 <= from_i, to_i < n,  from_i != to_i
    1 <= price_i <= 10^4
    0 <= src, dst, k < n
    There will not be any multiple flights between two cities.
"""


def find_cheapest_price(n, flights, src, dst, k):
    """
    Return the cheapest src->dst price using at most `k` stops, or -1.

    APPROACH (Bellman-Ford: relax all edges k + 1 times)
    ----------------------------------------------------
    WHY NOT PLAIN DIJKSTRA. In Network Delay Time we used Dijkstra with a
    "finalize each node the first time it's popped" rule -- safe there because the
    first pop is always the globally cheapest way to reach a node. That rule
    BREAKS here: the cheapest route to a city might use MORE stops than the hop
    budget allows, while a pricier route uses fewer. If we finalized a city at its
    globally-cheapest (but too-many-stops) price, we could lock in a path we're
    not allowed to take and miss the valid, slightly-pricier one. The stop limit
    means "cheapest" is no longer a property of the node alone -- it depends on
    HOW MANY EDGES we've used.

    THE KEY REFRAME: "at most k STOPS" = "at most k + 1 EDGES" (k intermediate
    cities means k + 1 flights). Bellman-Ford fits perfectly, because after `t`
    rounds of relaxing every edge, dist[] holds the cheapest cost to each city
    using AT MOST t edges. So we run exactly k + 1 rounds and read off dist[dst].

    THE ALGORITHM:
      - dist[city] = cheapest known cost from src; dist[src] = 0, rest = infinity.
      - Repeat k + 1 times:
          Make a SNAPSHOT copy of dist. For every flight (u -> v, price), relax
          using the SNAPSHOT: if snapshot[u] + price < dist[v], update dist[v].
      - After the loop, dist[dst] is the answer (or -1 if still infinity).

    WHY THE SNAPSHOT MATTERS (the classic bug). Each round must add AT MOST ONE
    edge to every path. If we relaxed against the live dist[] that we're updating
    in the same round, a city improved earlier in this round could be used to
    improve another city LATER in the same round -- chaining two (or more) edges
    in a single round and undercounting the stops. Reading from a frozen snapshot
    of the previous round guarantees every relaxation in round t extends a path of
    length (t-1) by exactly one edge. So we copy dist at the start of each round
    and relax against that copy.

    COMPLEXITY
    ----------
    Let E = len(flights).
    Time  : O(k * E) -- k + 1 rounds, each scanning all E edges. (n <= 100 here,
            so this is tiny.)
    Space : O(n) -- the dist array and its per-round snapshot.

    Args:
        n (int): Number of cities.
        flights (list[list[int]]): Directed edges [from, to, price].
        src (int): Start city.
        dst (int): Destination city.
        k (int): Maximum number of stops (intermediate cities).

    Returns:
        int: Cheapest price within the stop budget, or -1 if unreachable.
    """
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0

    # k stops -> at most k + 1 flights -> k + 1 relaxation rounds.
    for _ in range(k + 1):
        # Snapshot: every relaxation this round extends a PREVIOUS-round path by
        # exactly one edge, so we never chain two edges within a single round.
        snapshot = dist[:]
        for u, v, price in flights:
            if snapshot[u] != INF and snapshot[u] + price < dist[v]:
                dist[v] = snapshot[u] + price

    return dist[dst] if dist[dst] != INF else -1


if __name__ == "__main__":
    # Quick sanity checks.
    f1 = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
    print(find_cheapest_price(4, f1, 0, 3, 1))   # -> 700  (0->1->3; the 500 route needs 2 stops)

    f2 = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    print(find_cheapest_price(3, f2, 0, 2, 1))   # -> 200  (0->1->2, one stop)
    print(find_cheapest_price(3, f2, 0, 2, 0))   # -> 500  (no stops -> must fly direct)

    print(find_cheapest_price(3, f2, 2, 0, 5))   # -> -1   (nothing leaves toward 0)
    print(find_cheapest_price(2, [[0, 1, 50]], 0, 1, 0))   # -> 50   (direct, 0 stops)
    print(find_cheapest_price(1, [], 0, 0, 0))   # -> 0    (already at dst)

    # Cross-check against a BFS/DFS that explicitly tracks stops used, on small
    # random graphs.
    from collections import deque
    def brute(n, flights, src, dst, k):
        adj = [[] for _ in range(n)]
        for u, v, p in flights:
            adj[u].append((v, p))
        best = float("inf")
        # (city, cost, stops_used); stops_used counts intermediate cities.
        q = deque([(src, 0, -1)])
        while q:
            city, cost, stops = q.popleft()
            if city == dst:
                best = min(best, cost)
                continue
            if stops == k:          # no more hops allowed
                continue
            for nxt, price in adj[city]:
                if cost + price < best:   # simple prune
                    q.append((nxt, cost + price, stops + 1))
        return best if best != float("inf") else -1

    import random
    rng = random.Random(0)
    ok = True
    for _ in range(1000):
        n = rng.randint(2, 6)
        pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
        chosen = rng.sample(pairs, rng.randint(0, len(pairs)))
        flights = [[u, v, rng.randint(1, 20)] for u, v in chosen]
        src, dst = rng.sample(range(n), 2)
        k = rng.randint(0, n)
        if find_cheapest_price(n, [f[:] for f in flights], src, dst, k) != brute(n, flights, src, dst, k):
            ok = False
    print(ok)                                     # -> True
