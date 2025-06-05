# You are given an array prices where prices[i] is the price of a given stock on the ith day.
# You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
# Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

# Example 1:
# Input: prices = [7,1,5,3,6,4]
# Output: 5
# Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
# Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

# Example 2:
# Input: prices = [7,6,4,3,1]
# Output: 0
# Explanation: In this case, no transactions are done and the max profit = 0.
 
# Constraints:
# 1 <= prices.length <= 105
# 0 <= prices[i] <= 104

def find_best_time(prices : list) -> int:
    # Space: O(1)
    # Time: O(N) - iterate over prices
    buy, sell = 0, 1
    max_profit = 0
    while sell < len(prices):
        if prices[sell] >= prices[buy]:
            curr_profit = prices[sell] - prices[buy]
            max_profit = max(max_profit, curr_profit)
        else:
            buy = sell
        sell += 1 
    return max_profit


tests = [([7,1,5,3,6,4], 5), ([7,6,4,3,1], 0), ([2], 0), ([1, 2, 3, 4, 5], 4)]
for i,o in tests:
    assert find_best_time(i) == o, f"Failed, expected {o}, returned {find_best_time(i)}"
