# Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. 
# If there is no future day for which this is possible, keep answer[i] == 0 instead.

# Constraints:
# 1 <= temperatures.length <= 105
# 30 <= temperatures[i] <= 100

from typing import List

class Solution:

    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        #Space: O(N)
        #Time: O(N) despite the nested loops, each elem is pushed and popped at most once
        stack = []
        res = [0]*len(temperatures)
        for i in range(len(temperatures)):
            while stack and temperatures[stack[-1]] < temperatures[i]:
                elem = stack.pop()
                days = i - elem
                res[elem] = days
            stack.append(i)
        return res


solution = Solution()
tests = [([73,74,75,71,69,72,76,73], [1,1,4,2,1,1,0,0]), ([30,40,50,60], [1,1,1,0]), ([30,60,90], [1,1,0])]
for i,o in tests:
    assert solution.dailyTemperatures(i) == o, f"Fail, not {o} but {print(solution.dailyTemperatures(i))}"