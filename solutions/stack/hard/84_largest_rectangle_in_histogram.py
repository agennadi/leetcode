# Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.

# Input: heights = [2,1,5,6,2,3]
# Output: 10
# Explanation: The above is a histogram where width of each bar is 1.
# The largest rectangle is shown in the red area, which has an area = 10 units.

# Input: heights = [2,4]
# Output: 4
 

# Constraints:
# 1 <= heights.length <= 105
# 0 <= heights[i] <= 104

from typing import List

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        # Time complexity: O(N)
        # Space complexity: O(N)        
        max_area = 0
        stack = [-1] # always have a left boundary 
        for i in range(len(heights)): #curr index is the right bpundary 
            while stack[-1] != -1 and heights[stack[-1]] > heights[i]: 
                prev_ind = stack.pop()
                width = i - stack[-1] - 1
                area = width * heights[prev_ind]
                max_area = max(max_area, area) 
            stack.append(i)  
        
        while stack[-1] != -1: # handle the rest in ascending order
            top_ind = stack.pop()
            width = len(heights) - stack[-1] - 1
            height = heights[top_ind]
            max_area = max(max_area, width*height)

        return max_area    

solution = Solution()
tests = [([2,1,5,6,2,3], 10), ([2,4], 4), ([4,2,0,3,2,5], 6), ([10, 9, 8, 7], 28), ([0, 0, 0], 0)]
for i, o in tests:
    assert solution.largestRectangleArea(i) == o, f"Fail, not {o} but {print(solution.largestRectangleArea(i))}"    