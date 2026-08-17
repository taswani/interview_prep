"""
Course Schedule
===============

PROBLEM PROMPT
--------------
There are a total of `numCourses` courses you have to take, labeled from 0 to
numCourses - 1. You are given an array `prerequisites` where
prerequisites[i] = [a_i, b_i] indicates that you MUST take course b_i first if
you want to take course a_i.

    For example, the pair [0, 1] means: to take course 0 you have to first take
    course 1.

Return True if you can finish all courses. Otherwise, return False.

Example 1:
    Input:  numCourses = 2, prerequisites = [[1, 0]]
    Output: True
    Explanation: Take course 0, then course 1.
Example 2:
    Input:  numCourses = 2, prerequisites = [[1, 0], [0, 1]]
    Output: False
    Explanation: 0 needs 1 and 1 needs 0 -- a cycle, impossible.

Constraints:
    1 <= numCourses <= 2000
    0 <= len(prerequisites) <= 5000
    prerequisites[i].length == 2
    0 <= a_i, b_i < numCourses
    All the pairs prerequisites[i] are unique.
"""

from collections import deque


def can_finish(num_courses, prerequisites):
    """
    Return True if all courses can be completed (no prerequisite cycle).

    APPROACH (Topological sort via Kahn's algorithm / BFS on indegrees)
    -------------------------------------------------------------------
    Model courses as a DIRECTED GRAPH. For a pair [a, b] ("b before a") we add an
    edge b -> a, read as "b unlocks a" / "a depends on b." You can finish every
    course exactly when this graph has NO CYCLE: a cycle means a set of courses
    that all (transitively) require each other, so none can ever be the first one
    taken. So the whole question reduces to CYCLE DETECTION in a directed graph.

    Kahn's algorithm detects this while building a topological order:

      1. INDEGREE = number of prerequisites still unmet for each course (how many
         edges point INTO it). Build the adjacency list (b -> [a, ...]) and the
         indegree array in one pass over prerequisites.

      2. A course with indegree 0 has all prerequisites satisfied, so it can be
         taken now. Seed a queue with every indegree-0 course.

      3. Repeatedly "take" a course from the queue: increment a counter, then for
         each course it unlocks, decrement that course's indegree (one
         prerequisite just got satisfied). If an unlocked course's indegree hits
         0, it's now takeable -> enqueue it.

      4. When the queue empties, `taken` = how many courses we managed to
         schedule. If taken == num_courses we ordered them all (no cycle) ->
         True. If taken < num_courses, the leftover courses are exactly those
         trapped in a cycle (their indegree never reached 0 because they keep
         requiring each other) -> False.

    Intuition for why leftovers mean a cycle: every acyclic dependency graph has
    at least one course with no unmet prerequisite at each stage, so BFS keeps
    finding indegree-0 courses until all are taken. Only a cycle can leave a
    nonempty set where every course still points into the set.

    COMPLEXITY
    ----------
    Let V = num_courses and E = len(prerequisites).
    Time  : O(V + E) -- build the graph in O(E), then each node is enqueued once
            and each edge relaxed once.
    Space : O(V + E) -- adjacency list + indegree array + queue.

    Args:
        num_courses (int): Total number of courses.
        prerequisites (list[list[int]]): Pairs [a, b] meaning b must precede a.

    Returns:
        bool: True if all courses can be finished, else False.
    """
    # adjacency[b] lists the courses that b unlocks; indegree[a] counts a's
    # unmet prerequisites.
    adjacency = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:
        adjacency[b].append(a)   # edge b -> a ("take b before a")
        indegree[a] += 1

    # Start with every course that has no prerequisites.
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)

    taken = 0
    while queue:
        course = queue.popleft()
        taken += 1
        # Taking `course` satisfies one prerequisite of each course it unlocks.
        for nxt in adjacency[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:   # all of nxt's prerequisites now met
                queue.append(nxt)

    # Every course scheduled == no cycle. Leftovers == a cycle blocked them.
    return taken == num_courses


def can_finish_dfs(num_courses, prerequisites):
    """
    Same answer via DFS cycle detection with three-color marking.

    APPROACH (DFS, detect a back edge)
    ----------------------------------
    Build the same directed graph (edge b -> a). A directed graph has a cycle iff
    a DFS encounters a "back edge" -- an edge leading to a node that is still on
    the current recursion stack. We track each node's state with three colors:

        0 = UNVISITED : not explored yet.
        1 = VISITING  : currently on the DFS recursion stack (in progress).
        2 = DONE      : fully explored, and no cycle was found through it.

    dfs(course) returns True if a cycle is reachable from `course`:
      - If course is VISITING, we've looped back onto the current path -> cycle.
      - If course is DONE, it was already cleared -> no cycle here, prune.
      - Otherwise mark it VISITING, recurse into all courses it unlocks; if any
        recursion reports a cycle, propagate True. If none do, mark it DONE and
        return False.

    Marking nodes DONE (color 2) is the memoization that keeps this O(V + E): a
    node cleared once is never re-explored. Using only a "visited" set without the
    VISITING/DONE distinction would either miss cycles or redo work.

    COMPLEXITY
    ----------
    Time  : O(V + E).   Space : O(V + E) for the graph, plus O(V) recursion depth.

    Args:
        num_courses (int): Total number of courses.
        prerequisites (list[list[int]]): Pairs [a, b] meaning b must precede a.

    Returns:
        bool: True if all courses can be finished, else False.
    """
    adjacency = [[] for _ in range(num_courses)]
    for a, b in prerequisites:
        adjacency[b].append(a)

    state = [0] * num_courses   # 0 unvisited, 1 visiting, 2 done

    def has_cycle(course):
        if state[course] == 1:      # back edge onto the current path -> cycle
            return True
        if state[course] == 2:      # already cleared -> no cycle through here
            return False

        state[course] = 1           # mark on the recursion stack
        for nxt in adjacency[course]:
            if has_cycle(nxt):
                return True
        state[course] = 2           # fully explored, cleared
        return False

    # A cycle anywhere in the graph makes the schedule impossible.
    return not any(has_cycle(c) for c in range(num_courses))


if __name__ == "__main__":
    # Quick sanity checks.
    print(can_finish(2, [[1, 0]]))                       # -> True
    print(can_finish(2, [[1, 0], [0, 1]]))               # -> False (2-cycle)
    print(can_finish(1, []))                              # -> True  (no prereqs)
    print(can_finish(4, [[1, 0], [2, 1], [3, 2]]))       # -> True  (linear chain)
    print(can_finish(3, [[0, 1], [1, 2], [2, 0]]))       # -> False (3-cycle)
    print(can_finish(5, [[1, 0], [2, 0], [3, 1], [3, 2]]))  # -> True (diamond DAG)

    # The DFS variant returns the same answers.
    cases = [
        (2, [[1, 0]]),
        (2, [[1, 0], [0, 1]]),
        (1, []),
        (4, [[1, 0], [2, 1], [3, 2]]),
        (3, [[0, 1], [1, 2], [2, 0]]),
        (5, [[1, 0], [2, 0], [3, 1], [3, 2]]),
    ]
    print(all(can_finish(n, p) == can_finish_dfs(n, p) for n, p in cases))   # -> True
