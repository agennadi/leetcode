# Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.
# Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.
# Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.
# Return the minimum integer k such that she can eat all the bananas within h hours. 

# Example 1:
# Input: piles = [3,6,7,11], h = 8
# Output: 4

# Example 2:
# Input: piles = [30,11,23,4,20], h = 5
# Output: 30

# Example 3:
# Input: piles = [30,11,23,4,20], h = 6
# Output: 23

# Constraints:
# 1 <= piles.length <= 104
# piles.length <= h <= 109
# 1 <= piles[i] <= 109
from typing import List
from math import ceil

class Solution:
    # Space: O(1)
    # Time: O(num piles * logN) - binary search where N is max(piles)
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        min_k, max_k = 1, max(piles)
        k = 0
        while min_k <= max_k:
            curr_k = (min_k+max_k)//2
            curr_h = 0
            for pile in piles:
                curr_h += ceil(pile/curr_k)
                if curr_h > h:
                    break
            if curr_h > h:
                min_k = curr_k + 1
            else:
                k = curr_k
                max_k = curr_k - 1
        return k 

solution = Solution()
tests = [([3,6,7,11], 8, 4), ([30,11,23,4,20], 5, 30), ([30,11,23,4,20], 6, 23)]
for p, h, o in tests:
    assert solution.minEatingSpeed(p,h) == o
    
    