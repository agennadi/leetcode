# You are given an integer array nums consisting of n elements, and an integer k.
# Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10-5 will be accepted. 

# Example 1:
# Input: nums = [1,12,-5,-6,50,3], k = 4
# Output: 12.75000
# Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75

# Example 2:
# Input: nums = [5], k = 1
# Output: 5.00000
 
# Constraints:
# n == nums.length
# 1 <= k <= n <= 105
# -104 <= nums[i] <= 104


def find_max_avg_inefficient(nums, k):
    # No need to calculate avg -> find the max sum
    # Space: O(1)
    # Time: O(n*k) - slice and recalculate sum for each k elems in n
    l,r = 0, k-1
    max_sum = float('-inf')
    while r < len(nums):
        max_sum = max(max_sum, sum(nums[l:r+1])) 
        l += 1
        r += 1
    return max_sum/k

def find_max_avg(nums, k):
    # No need to calculate avg -> find the max sum
    # Space: O(1)
    # Time: O(n) 
    cur_sum = sum(nums[:k])
    max_sum = cur_sum
    for r in range(k, len(nums)):
        cur_sum += nums[r] - nums[r-k] #O(1) for addition and O(1) for subtraction 
        max_sum = max(max_sum, cur_sum)
    return max_sum/k

tests = [([1,12,-5,-6,50,3], 4, 12.75000), ([5], 1, 5.00000)]
for nums, k, o in tests:
    assert find_max_avg_inefficient(nums, k) == o, f"Failes, expected {o}, returned {find_max_avg_inefficient(nums, k)}"
    assert find_max_avg(nums, k) == o, f"Failes, expected {o}, returned {find_max_avg(nums, k)}"