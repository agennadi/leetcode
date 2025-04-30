# Given an integer array nums of length n and an integer target, find three integers in nums such that the sum is closest to target.
# Return the sum of the three integers.
# You may assume that each input would have exactly one solution.

# Example 1:
# Input: nums = [-1,2,1,-4], target = 1
# Output: 2
# Explanation: The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).

# Example 2:
# Input: nums = [0,0,0], target = 1
# Output: 0
# Explanation: The sum that is closest to the target is 0. (0 + 0 + 0 = 0).

# Constraints:
# 3 <= nums.length <= 500
# -1000 <= nums[i] <= 1000
# -104 <= target <= 104

from typing import List

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        # Time Complexity: O(N²) = n*log(n) and nested loop n²    
        # Space Complexity: not O(1) but O(logN) because of Timsort (python sorting is condisered in-place but it still needs some extra space)    
        nums.sort()
        dif = float("inf")
        for i, n in enumerate(nums):
            l = i + 1
            r = len(nums) - 1
            complement = target - n
            while l < r:
                triplet = n + nums[l] + nums[r]
                if abs(target - triplet) < abs(dif):
                    dif = target - triplet 
                if dif == 0:
                    break
                if nums[l] + nums[r] < complement:
                    l += 1
                elif nums[l] + nums[r] > complement: 
                    r -= 1
        return target - dif


solution = Solution()
