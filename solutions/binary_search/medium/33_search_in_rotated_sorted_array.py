# There is an integer array nums sorted in ascending order (with distinct values).
# Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] 
# might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].
# Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.
# You must write an algorithm with O(log n) runtime complexity.

# Example 1:
# Input: nums = [4,5,6,7,0,1,2], target = 0
# Output: 4

# Example 2:
# Input: nums = [4,5,6,7,0,1,2], target = 3
# Output: -1

# Example 3:
# Input: nums = [1], target = 0
# Output: -1

# Constraints:
# 1 <= nums.length <= 5000
# -104 <= nums[i] <= 104
# All values of nums are unique.
# nums is an ascending array that is possibly rotated.
# -104 <= target <= 104

class Solution:
    def search_in_array(self, nums: list, target: int) -> int:
        # First identify which half is sorted!
        # Then, decide if the target lies in that half 
        # Space: O(1)
        # Time: O(logN)
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l+r)//2
            if target == nums[mid]:
                return mid
            if nums[l] <= nums[mid]: # the left half is sorted
                if nums[l] <= target < nums[mid]:
                    r = mid - 1 # target is in the sorted left half
                else:
                    l = mid + 1 # target is in the right half (may or may not be sorted)
            else: # the right side is sorted
                if nums[mid] < target <= nums[r]: # target is in the sorted right half
                    l = mid + 1
                else:
                    r = mid - 1 # target is in the left half (may or may not be sorted)

        return -1

solution = Solution()
tests = [([4,5,6,7,0,1,2], 0, 4), ([4,5,6,7,0,1,2], 3, -1), ([1], 0, -1)]    
for i, t, o in tests:
    assert solution.search_in_array(i, t) == o, f'Fail, should be {o} but is {solution.search_in_array(i, t)}'