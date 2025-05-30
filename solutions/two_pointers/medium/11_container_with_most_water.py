# You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
# Find two lines that together with the x-axis form a container, such that the container contains the most water.
# Return the maximum amount of water a container can store. 

# Example 1:
# Input: height = [1,8,6,2,5,4,8,3,7]
# Output: 49
# Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

# Example 2:
# Input: height = [1,1]
# Output: 1

# Constraints:
# n == height.length
# 2 <= n <= 105
# 0 <= height[i] <= 104


class Solution:
    def maxArea(self, height: List[int]) -> int:
        # Time Complexity: O(N) for iterating, O(N) for min and max, total: O(N)    
        # Space Complexity: O(1)        
        l, r = 0, len(height) - 1
        max_square = 0
        while l < r:
            y = min(height[l], height[r])
            x = r - l 
            max_square = max(x*y, max_square)
            if height[l] < height[r]:
                l += 1
            else:
                r-=1
        return max_square