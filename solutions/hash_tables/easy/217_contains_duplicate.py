# Given an integer array nums, return true if any value appears at least twice in the array, 
# and return false if every element is distinct.
# Constraints:

# 1 <= nums.length <= 105
# -109 <= nums[i] <= 109

from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # Time Complexity: O(N) - iterate over nums, hashmap lookup and insertion are O(1)  
        # Space Complexity: O(N) - hashtable

        hashtable = {}
        for n in nums:
            if n in hashtable:
                return True
            hashtable[n] = 1
        return False 

solution = Solution()
nums = [1,1,1,3,3,4,3,2,4,2]
assert solution.containsDuplicate(nums) == True