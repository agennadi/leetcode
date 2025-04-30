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
        # Time Complexity: O(N²) = nested loop n²    
        # Space Complexity: O(N²) = if there are combinations for each pair             
        res, dups = set(), set()
        seen = {}
        for i, val1 in enumerate(nums):
            if val1 not in dups:
                dups.add(val1)
                for j, val2 in enumerate(nums[i + 1 :]):
                    complement = -val1 - val2
                    if complement in seen and seen[complement] == i:
                        res.add(tuple(sorted((val1, val2, complement))))
                    seen[val2] = i   
        return [list(x) for x in res]


solution = Solution()
nums1, output1 = [-1,0,1,2,-1,-4], [[-1,0,1], [-1,-1,2]]
nums2, output2 = [0,1,1], []
nums3, output3 = [0,0,0], [[0,0,0]]

assert solution.threeSum(nums1) == output1
assert solution.threeSum(nums2) == output2
assert solution.threeSum(nums3) == output3