"""
Course Schedule II
==================

PROBLEM PROMPT
--------------
There are a total of `numCourses` courses you have to take, labeled from 0 to
numCourses - 1. You are given an array `prerequisites` where
prerequisites[i] = [a_i, b_i] indicates that you MUST take course b_i first if
you want to take course a_i.

    For example, the pair [0, 1] means: to take course 0 you have to first take
    course 1.

Return the ORDERING of courses you should take to finish all courses. If there
are many valid answers, return any of them. If it is impossible to finish all
courses, return an EMPTY array.

Example 1:
    Input:  numCourses = 2, prerequisites = [[1, 0]]
    Output: [0, 1]
Example 2:
    Input:  numCourses = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
    Output: [0, 1, 2, 3]   (or [0, 2, 1, 3] -- either is valid)
Example 3:
    Input:  numCourses = 1, prerequisites = []
    Output: [0]

Constraints:
    1 <= numCourses <= 2000
    0 <= len(prerequisites) <= numCourses * (numCourses - 1)
    prerequisites[i].length == 2
    0 <= a_i, b_i < numCourses
    a_i != b_i
    All the pairs [a_i, b_i] are distinct.
"""

from collections import deque


def find_order(num_courses, prerequisites):
    """
    Return a valid course ordering, or [] if the prerequisites contain a cycle.

    APPROACH (Kahn's algorithm -- topological sort, now RECORDING the order)
    -----------------------------------------------------------------------
    This is Course Schedule (problem 207) taken one step further. There we only
    needed a yes/no: "can all courses be finished?" -- and answered it by
    COUNTING how many courses Kahn's BFS managed to schedule. Here we need the
    actual schedule, so we do the identical BFS but APPEND each course to an
    output list as we take it. That list, in the order courses come off the
    queue, IS a valid topological ordering -- a course is only enqueued once
    every prerequisite pointing into it has already been taken and recorded, so
    prerequisites always appear before the courses that need them.

    The steps (same machinery as 207):

      1. Build adjacency (edge b -> a for pair [a, b], "b unlocks a") and the
         indegree array (indegree[a] = number of unmet prerequisites of a).

      2. Seed a queue with every indegree-0 course (nothing to take first).

      3. Pop a course, APPEND it to `order`, and for each course it unlocks,
         decrement that course's indegree; if it drops to 0, enqueue it.

      4. When the queue drains, `order` holds all courses we scheduled.

    THE CYCLE CHECK, expressed on the output: if len(order) == num_courses we
    scheduled everyone -> return order. Otherwise a cycle trapped the remaining
    courses (their indegree never reached 0), so a full ordering is impossible ->
    return [] as the problem requires. This replaces 207's `taken == num_courses`
    boolean with the same test on the recorded list's length.

    "Return any valid answer": the specific order depends on how ties among
    indegree-0 courses are broken (queue insertion order). Every ordering Kahn's
    produces is valid; the grader accepts any of them.

    COMPLEXITY
    ----------
    Let V = num_courses and E = len(prerequisites).
    Time  : O(V + E) -- build the graph, then enqueue each node once and relax
            each edge once.
    Space : O(V + E) -- adjacency list, indegree array, queue, and output list.

    Args:
        num_courses (int): Total number of courses.
        prerequisites (list[list[int]]): Pairs [a, b] meaning b must precede a.

    Returns:
        list[int]: A valid ordering, or [] if none exists (cycle present).
    """
    # adjacency[b] = courses unlocked by b; indegree[a] = a's unmet prerequisites.
    adjacency = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:
        adjacency[b].append(a)   # edge b -> a
        indegree[a] += 1

    # Courses with no prerequisites can go first.
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)

    order = []
    while queue:
        course = queue.popleft()
        order.append(course)     # record the course as taken
        for nxt in adjacency[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    # Full ordering found only if every course was scheduled; else a cycle exists.
    return order if len(order) == num_courses else []


def _is_valid_order(num_courses, prerequisites, order):
    """
    Verify that `order` is a genuine topological ordering (test helper).

    Checks it is a permutation of all courses AND that for every pair [a, b]
    the prerequisite b appears BEFORE a. Used only by the self-tests, since the
    problem accepts ANY valid ordering (so we can't compare against one fixed
    expected list).
    """
    if sorted(order) != list(range(num_courses)):
        return False
    position = {course: i for i, course in enumerate(order)}
    return all(position[b] < position[a] for a, b in prerequisites)


if __name__ == "__main__":
    # For solvable inputs we validate the ordering (any valid order is accepted).
    print(find_order(2, [[1, 0]]))                                   # e.g. [0, 1]
    print(_is_valid_order(2, [[1, 0]], find_order(2, [[1, 0]])))     # -> True

    p = [[1, 0], [2, 0], [3, 1], [3, 2]]
    print(find_order(4, p))                                          # e.g. [0, 1, 2, 3]
    print(_is_valid_order(4, p, find_order(4, p)))                   # -> True

    print(find_order(1, []))                                         # -> [0]
    print(find_order(3, [[0, 1], [1, 2], [2, 0]]))                   # -> []  (3-cycle)

    # A batch check: solvable cases yield valid orders; cyclic ones yield [].
    solvable = [
        (2, [[1, 0]]),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]]),
        (1, []),
        (6, [[1, 0], [2, 1], [3, 1], [4, 2], [4, 3], [5, 4]]),
    ]
    cyclic = [
        (2, [[1, 0], [0, 1]]),
        (3, [[0, 1], [1, 2], [2, 0]]),
    ]
    print(all(_is_valid_order(n, p, find_order(n, p)) for n, p in solvable))   # -> True
    print(all(find_order(n, p) == [] for n, p in cyclic))                      # -> True
