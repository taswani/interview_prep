"""
Best Time to Buy and Sell Stock
===============================

PROBLEM PROMPT
--------------
You are given an array `prices` where `prices[i]` is the price of a given stock
on the i-th day.

You want to maximize your profit by choosing a single day to buy one stock and
choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot
achieve any profit, return 0.

Example 1:
    Input:  prices = [7, 1, 5, 3, 6, 4]
    Output: 5
    Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6),
                 profit = 6 - 1 = 5. Note that buying on day 2 and selling on
                 day 1 is not allowed because you must buy before you sell.

Example 2:
    Input:  prices = [7, 6, 4, 3, 1]
    Output: 0
    Explanation: Prices only fall, so no transaction is made and profit is 0.

Constraints:
    1 <= len(prices) <= 10^5
    0 <= prices[i] <= 10^4
"""


def max_profit(prices):
    """
    Return the maximum profit achievable from a single buy-then-sell transaction.

    APPROACH (Single Pass / Track Minimum So Far)
    ---------------------------------------------
    The profit for selling on a given day is:

        price_today - (lowest price seen on any earlier day)

    So the best possible profit *ending* on any day depends only on the cheapest
    price we've encountered up to that point. We therefore walk through the
    prices once, maintaining two running values:

        min_price  -> the lowest buy price seen so far
        best_profit -> the largest (price - min_price) seen so far

    On each day we:
      1. Check what profit we'd make selling today (current price - min_price),
         and update best_profit if it beats our previous best.
      2. Update min_price if today's price is a new low (a cheaper day to buy).

    Because a buy must come before a sell, updating best_profit *before*
    lowering min_price naturally enforces that ordering — min_price always
    reflects a strictly earlier (or equal) day than the current sell day.

    COMPLEXITY
    ----------
    Time  : O(n) — a single pass over the n prices, doing O(1) work per day.
    Space : O(1) — only two scalar variables are stored, regardless of input size.

    Args:
        prices (list[int]): Daily stock prices.

    Returns:
        int: The maximum achievable profit, or 0 if no profit is possible.
    """
    # The cheapest price we've seen so far. Start it at infinity so the first
    # day's price always becomes the initial minimum.
    min_price = float("inf")

    # The best profit found so far. Starts at 0 to cover the "no profit" case.
    best_profit = 0

    for price in prices:
        # Profit if we sold today, having bought at the cheapest earlier price.
        # If this beats our running best, record it.
        best_profit = max(best_profit, price - min_price)

        # Update the cheapest buy price seen for use on future days.
        min_price = min(min_price, price)

    return best_profit


if __name__ == "__main__":
    # Quick sanity checks demonstrating the function.
    print(max_profit([7, 1, 5, 3, 6, 4]))  # -> 5
    print(max_profit([7, 6, 4, 3, 1]))     # -> 0
    print(max_profit([1, 2]))              # -> 1
    print(max_profit([5]))                 # -> 0 (only one day, no sell possible)
