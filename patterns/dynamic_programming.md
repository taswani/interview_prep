# Dynamic Programming

**What it is:** solve a big problem by combining answers to smaller versions of
the *same* problem — and **remember each small answer so you never recompute it.**
That's the whole thing. "Dynamic programming" = recursion + not being wasteful.

**Reach for it when:** you're asked for a **count** ("how many ways…"), an
**optimum** ("fewest / most / longest / min cost…"), or a **yes/no reachability**
("can you make…"), AND a choice now leads to the same kind of subproblem later.
Signals: "how many ways", "minimum/maximum", "longest", overlapping choices.

> If subproblems *don't* overlap (each is solved once), you don't need DP — that's
> just plain recursion / divide-and-conquer. DP earns its keep only when the same
> subproblem shows up again and again.

---

## The idea in one sentence

**Look at the LAST decision.** Whatever the final move was, everything *before* it
is a smaller instance of the same problem — which you've already solved. Combine
those sub-answers, and you're done.

**Analogy — climbing a staircase:** to count the ways to reach step `n`, ask "what
was my last hop?" It was a 1-step (from `n-1`) or a 2-step (from `n-2`). So
`ways(n) = ways(n-1) + ways(n-2)`. You didn't trace whole climbs — you reduced
step `n` to two smaller *already-answered* questions.

---

## The 5-step method (run this every time)

1. **Define the subproblem in words.** `dp[i]` = "the answer considering only …
   up to i". Getting this sentence right is 80% of the problem.
2. **Find the recurrence by reasoning about the last decision.** Express `dp[i]`
   using smaller `dp[...]` values.
3. **Pin the base case(s).** The smallest inputs, answered directly (`dp[0] = …`).
4. **Choose a direction:** top-down (recurse + memo) or bottom-up (fill a table).
5. **Optimize space** if `dp[i]` only needs the last few entries → rolling variables.

That progression — **recurrence → memo → table → rolling variables** — is exactly
what to narrate out loud in an interview.

---

## The single most useful distinction: counting vs optimizing

**This picks your combine operator.**

| Goal | Operator | Example recurrence |
|---|---|---|
| **Count** ways | `+` (sum) | `dp[i] = dp[i-1] + dp[i-2]` (Climbing Stairs) |
| **Optimize** a value | `min` / `max` | `dp[i] = max(dp[i-1], nums[i] + dp[i-2])` (House Robber) |
| **Reachability** | `or` / any | `dp[i] = any(dp[j] and ok(j, i))` (Word Break) |

If you're counting, you *add* the sub-answers. If you're optimizing, you take the
*best* of them. Mixing these up is the most common conceptual error.

---

## Template A — 1-D, look back a fixed amount (rolling variables)

When `dp[i]` depends only on the previous one or two values, you don't need the
whole array — just slide a window.

```python
prev2, prev1 = base0, base1
for i in range(2, n + 1):
    cur = combine(prev1, prev2)     # + for counting, max/min for optimizing
    prev2, prev1 = prev1, cur
return prev1
```

- **Climbing Stairs:** `cur = prev1 + prev2`.
- **House Robber:** `cur = max(prev1, nums[i] + prev2)` (skip vs rob this house).

O(n) time, **O(1) space.**

---

## Template B — 1-D with an inner loop over choices

When the last decision picks from a *set* of options (which coin, which previous
element), add an inner loop.

```python
dp = [base] * (target + 1)
dp[0] = identity                    # 0 for min-count, 1 for counting ways
for a in range(1, target + 1):
    for choice in choices:
        if choice <= a:
            dp[a] = combine(dp[a], dp[a - choice])   # min(...+1) or += ...
return dp[target]
```

- **Coin Change (322, optimize):** `dp[a] = min(dp[a], dp[a - coin] + 1)`, sentinel
  `amount+1` for "impossible".
- **Coin Change II (518, count):** `dp[a] += dp[a - coin]`.

---

## The loop-order trap (combinations vs permutations)

Only matters for the *counting* version, but it's the classic Coin Change II bug:

```python
for coin in coins:            for a in range(...):
    for a in range(...):  vs.     for coin in coins:
        dp[a] += dp[a-coin]           dp[a] += dp[a-coin]
   → COMBINATIONS  {1,2}=={2,1}   → PERMUTATIONS  1+2 ≠ 2+1
```

**Coins on the outer loop** builds each combination in one fixed coin order, so
`{1,2}` is counted once. Swap the loops and you count ordered sequences instead.
Rule of thumb: *coins-outer = combinations, amount-outer = permutations.*

---

## Two other recurrence shapes worth recognizing

- **Two-state** (carry more than one number per step). *Max Product Subarray:*
  track running **max and min**, because a negative flips them —
  `hi, lo = max(x, x*hi, x*lo), min(x, x*lo, x*hi)`.
- **Reduce to a solved problem.** *House Robber II* (houses in a circle) = run the
  linear robber twice (once excluding the first house, once the last) and take the
  max. Recognizing "this is the previous problem in disguise" beats inventing new
  DP.

---

## Top-down vs bottom-up (they're the same recurrence)

- **Top-down (memoized recursion):** write the recurrence directly; cache each
  result the first time. Most intuitive; costs recursion-stack space.
- **Bottom-up (table):** fill `dp[]` from base cases upward. Avoids recursion depth,
  and enables the O(1) rolling-variable trick.

Both do the same work in the same time. Pick top-down to *discover* the recurrence,
bottom-up to *ship* it.

```python
# top-down skeleton
memo = {}
def solve(state):
    if state in base_cases: return base_value
    if state in memo: return memo[state]
    memo[state] = combine(solve(smaller_1), solve(smaller_2), ...)
    return memo[state]
```

---

## Complexity (how to state it)

Roughly: **(number of distinct subproblems) × (work per subproblem).**

| Shape | Time | Space |
|---|---|---|
| 1-D fixed look-back (rolling) | O(n) | O(1) |
| 1-D with inner choice loop | O(n · k) | O(n) |
| 2-D table (LCS, Edit Distance) | O(m · n) | O(m · n) → often O(n) |

---

## The usual bugs

- **Wrong or missing base case** — the whole table is built on it.
- **Counting with `max` (or optimizing with `+`)** — wrong combine operator.
- **Pattern-matching instead of trusting the recurrence** — e.g. "rob every other
  house" is wrong; `[2,1,1,2] → 4` skips two in a row. Let the `max` decide.
- **Loop order** in counting problems (combinations vs permutations).
- **Off-by-one in the table size** — usually want `dp[0..n]`, length `n+1`.

---

## 30-second mental summary

1. **Subproblem in words** → `dp[i] = "answer up to i"`.
2. **Recurrence from the last decision.**
3. **Base case.**
4. **Counting → `+`, optimizing → `min`/`max`.**
5. **Only need the last few? → rolling variables (O(1) space).**

DP feels hard because the recurrence looks like magic. It isn't — it's always just
*"what was my last move, and what smaller problem did it leave behind?"*

---

*Worked implementations:
[climbing_stairs.py](../google/climbing_stairs.py),
[house_robber.py](../google/house_robber.py),
[house_robber_ii.py](../google/house_robber_ii.py),
[coin_change.py](../google/coin_change.py),
[coin_change_ii.py](../google/coin_change_ii.py).*
