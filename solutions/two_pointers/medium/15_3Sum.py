# Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

# Notice that the solution set must not contain duplicate triplets.

# Example 1:
# Input: nums = [-1,0,1,2,-1,-4]
# Output: [[-1,-1,2],[-1,0,1]]
# Explanation: 
# nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
# nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
# nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
# The distinct triplets are [-1,0,1] and [-1,-1,2].
# Notice that the order of the output and the order of the triplets does not matter.

# Example 2:
# Input: nums = [0,1,1]
# Output: []
# Explanation: The only possible triplet does not sum up to 0.

# Constraints:
# 3 <= nums.length <= 3000
# -105 <= nums[i] <= 105

from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # 3sum -> 2sum
        # Time Complexity: O(N²) = n*log(n) and nested loop n²    
        # Space Complexity: O(N²) = if there are combinations for each pair             
        res = []
        nums.sort() #n log(n)
        for i in range(len(nums)): #n
            if i > 0 and nums[i] == nums[i-1]:
                continue
            if nums[i] > 0:
                break
            target = 0 - nums[i]
            l = i + 1
            r = len(nums) - 1
            while l < r: 
                if nums[l] + nums[r] == target:
                    triplet = [nums[i], nums[l], nums[r]]
                    if triplet not in res:
                        res.append(triplet)
                    l += 1
                    r -= 1
                    while l<r and nums[l] == nums[l-1]:
                        l +=1
                    while l<r and nums[r] == nums[r+1]:
                        r -= 1    
                elif nums[l] + nums[r] < target:
                    l +=1
                else:
                    r-=1
        return res


solution = Solution()
nums1, output1 = [-1,0,1,2,-1,-4], [[-1,-1,2],[-1,0,1]]
nums2, output2 = [0,1,1], []
nums3, output3 = [0,0,0], [[0,0,0]]

assert solution.threeSum(nums1) == output1
assert solution.threeSum(nums2) == output2
assert solution.threeSum(nums3) == output3