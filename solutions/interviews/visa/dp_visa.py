"""
Problem Statement

You are given an integer array nums containing both positive and negative integers.

You start at index 0 and need to reach the last index n - 1.

From any index i, you may jump forward by:

exactly 1, or
a prime number that ends with digit 3

For example, valid jump sizes include 1, 3, 13, 23, 43, ....

Return the maximum possible sum of values visited along a valid path from index 0 to index n - 1.

# Test case 1
nums1 = [5, -10, 4, 100, -2]
# Valid best path: 0 -> 3 -> 4
# Sum = 5 + 100 - 2 = 103
# Expected: 103

# Test case 2
nums2 = [1, 2, 3, 4]
# Expected: 10

# Test case 3
nums3 = [10, -5, -2, -1, 20]
# Best path: 0 -> 3 -> 4
# Sum = 10 + (-1) + 20 = 29
# Expected: 29

# Test case 4
nums4 = [-1, -2, -3, -4]
# Best path: 0 -> 3
# Sum = -1 + -4 = -5
# Expected: -5

# Test case 5
nums = [7]
# Already at the last index
# Expected: 7

Hints
Hint 1
Think of dp[i] as the maximum sum you can get when you land on index i.
Hint 2
For each index i, look backward at all indices that can jump into i.
Hint 3
Precompute all valid jump sizes up to len(nums) - 1.

"""

'''
dp logic on example nums1 = [5, -10, 4, 100, -2]:
1. We start at index 0, so dp[0] = 5
2. dp[1] = 5 + (-10) = -5. There is only one way to get to index 1 - using step size 1.
3. dp[2] = -1. Again, since 2 < 3, the only way to get to index 2 is from index 1 using step size 1.
4. dp[3] = max(105, 99) = 105. We can get to index 3 from index 0 using step size 3, or from index 2 using step size 1.
5. dp[4] = max(-7,103) = 103. We can get to index 4 from index 3 using step size 1, or from index 1 (dp[1] = -5) using step size 3

Algorithm:
1. Precompute all valid jump sizes till 10^4 (the array length limit)
2. For each index i calculate the possible jump sizes that can reach index i. 
3. For each valid jump size, calculate dp[i-jump_size] + nums[i] and take the max value
4. Return dp[n-1] as the result
'''


from typing import List

def _is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True

def find_jumps(limit):
    jump_list = [1]
    for i in range(2, limit):
        if _is_prime(i) and i % 10 == 3:
            jump_list.append(i)
    return jump_list

def max_path_sum(nums: List[int]) -> int:
    """
    Return the maximum sum of values visited when moving from index 0
    to the last index.

    Allowed jump sizes:
    - 1
    - any prime number ending in digit 3
    """
    step_list = find_jumps(len(nums))
    dp = [0] * len(nums)
    dp[0] = nums[0]
    for i in range(1, len(nums)):
        paths = []
        for j in step_list:
            if i - j >= 0:
                paths.append(dp[i-j] + nums[i])
        dp[i] = max(paths)
    return dp[-1] 


assert max_path_sum([5, -10, 4, 100, -2]) == 103
assert max_path_sum([1, 2, 3, 4]) == 10
assert max_path_sum([10, -5, -2, -1, 20]) == 29
assert max_path_sum([7]) == 7


