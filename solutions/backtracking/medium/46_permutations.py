# Given an array nums of distinct integers, return all the possible permutations. 
# You can return the answer in any order.
# Example 1:
# Input: nums = [1,2,3]
# Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def backtrack(curr):
            if len(curr) == len(nums):
                res.append(curr[:])
                return #a permutation is found, exit
            for num in nums:
                if num not in curr: #check all elems that are not in the permutation yet
                    curr.append(num)
                    backtrack(curr)
                    curr.pop() #backtracking

        res = []
        backtrack([]) #start with an empty list
        return res


solution = Solution()
nums = [1,2,3]
permutations = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
assert solution.permute(nums) == permutations