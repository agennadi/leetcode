# Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
# The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
# You must write an algorithm that runs in O(n) time and without using the division operation.

# Example 1:
# Input: nums = [1,2,3,4]
# Output: [24,12,8,6]

# Example 2:
# Input: nums = [-1,1,0,-3,3]
# Output: [0,0,9,0,0]

# Constraints:
# 2 <= nums.length <= 105
# -30 <= nums[i] <= 30

from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # Time Complexity: O(N)  
        # Space Complexity: O(N)  
        prefix, postfix = [0]*len(nums), [0]*len(nums)
        prefix[0], postfix[len(nums)-1] = 1, 1
        for i in range(1, len(nums)):
            prefix[i] = prefix[i-1] * nums[i-1]
        for j in range(len(nums)-2, -1, -1):
            postfix[j] = postfix[j+1] * nums[j+1]    
        res = [0]*len(nums)
        for k in range(len(nums)):
            res[k] = prefix[k] * postfix[k]
        return res

    def productExceptSelfOptimized(self, nums: List[int]) -> List[int]:   
        # Time Complexity: O(N)  
        # Space Complexity: O(1)      
        length = len(nums)
        res = [0] * length
        res[0] = 1
        postfix = 1
        for i in range(1, length):
            res[i] = res[i-1] * nums[i-1]
        for j in range(length-1, -1, -1):
            res[j] *= postfix
            postfix *= nums[j]
        return res




nums1, nums2 = [1,2,3,4], [-1,1,0,-3,3]
output1, output2 = [24,12,8,6], [0,0,9,0,0]
solution = Solution()
assert solution.productExceptSelf(nums1) == output1
assert solution.productExceptSelf(nums2) == output2

assert solution.productExceptSelfOptimized(nums1) == output1
assert solution.productExceptSelfOptimized(nums2) == output2