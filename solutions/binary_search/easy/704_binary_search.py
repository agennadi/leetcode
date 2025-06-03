# Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.
# You must write an algorithm with O(log n) runtime complexity.

# Example 1:
# Input: nums = [-1,0,3,5,9,12], target = 9
# Output: 4
# Explanation: 9 exists in nums and its index is 4

# Example 2:
# Input: nums = [-1,0,3,5,9,12], target = 2
# Output: -1
# Explanation: 2 does not exist in nums so return -1
 
# Constraints:
# 1 <= nums.length <= 104
# -104 < nums[i], target < 104
# All the integers in nums are unique.
# nums is sorted in ascending order.

from typing import List

class Solution:
    def search(self, nums: List[int], target: int):
        # Space: O(1) 
        # Time: O(logN) - log time because nums is divided in halves each time 
        l,r = 0, len(nums)-1
        while l < r:
            curr_ind = (l+r)//2
            curr_val = nums[curr_val]
            if curr_val == target:
                return curr_val
            if curr_val < target: 
                l = curr_val +1
            else:
                r = curr-val - 1


solution = Solution()
tests = [([-1,0,3,5,9,12], 9), ([-1,0,3,5,9,12], 2)]