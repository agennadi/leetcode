# Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

# Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
# Output: 6
# Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
# Example 2:

# Input: height = [4,2,0,3,2,5]
# Output: 9

# Constraints:
# n == height.length
# 1 <= n <= 2 * 104
# 0 <= height[i] <= 105
from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        '''
        0: (0,0) total=0 first elem
        1: (1,1) total=0 bigger than last elem in stack => we pop it => stack empty => add last to stack, total doesn't change 
        0: (1,1)(0,2) total=0 curr smaller than last elem => push curr to the stack
        2: (2,3) total=1 curr is bigger than top (0,2), so we pop it; total += (min(2,1)-0) * (3-1-1) = 1
            curr (1,1) is bigger than top, so we pop it; the stack is empty, we put curr on top and move on
        1: (2,3)(1,4) total=1 curr smaller than last elem => push curr to the stack
        0: (2,3)(1,4)(0,5) total=1 curr smaller than last elem => push curr to the stack
        1: (2,3)(1,4)(1,6) total=2 curr is bigger than top (0,5), so we pop it; total += (min(1,1)-0) * (6-4-1) = 1 
        3: (3,7) total=5 curr is bigger than top (1,6), so we pop it; total += (min(1,3)-1)*(7-6-1) = 0  
           curr is bigger than top (1,4), so we pop it; total += (min(2,3) - 1) * (7-3-1) = 3
           curr is bigger than top(2,3), so we pop it and the stack is empty => push curr to the stack
        2: (3,7)(2,8)
        1: (3,7)(2,8)(1,9)
        2: (3,7)(2,8)(1,9)(2,10)
        1: (3,7)(2,8)(1,9)(2,10)(1,11)
        end: total = 6   

        1. Push the 1st elem on the stack.
        2.0 Iterate over the rest of the list:
            2.1 While the stack is not empty and its top is smaller than the curr value:
            2.2 Remove the top
            2.3 If the stack is empty, no left wall exists - break and go to 2.5
            2.4 Else, add height*width to the total.  
            2.5 Push curr to stack and return to 2.0
        3. Return total

        Space: O(N) because of the stack list
        Time: O(N) despite the nested loops, each elem is pushed and popped at most once
        '''
        stack = [0]
        total = 0
        for i in range(1, len(height)):
            while stack and height[stack[-1]] < height[i]:
                bottom = stack.pop()
                if not stack:      
                    break
                total += (min(height[stack[-1]], height[i])-height[bottom]) * (i - stack[-1] - 1)     
            stack.append(i)        
        return total         

solution = Solution()
height1, output1 = [0,1,0,2,1,0,1,3,2,1,2,1], 6
height2, output2 = [4,2,0,3,2,5], 9
assert solution.trap(height1) == output1
assert solution.trap(height2) == output2