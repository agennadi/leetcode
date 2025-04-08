# You are given an m x n integer matrix matrix with the following two properties:

# Each row is sorted in non-decreasing order.
# The first integer of each row is greater than the last integer of the previous row.
# Given an integer target, return true if target is in matrix or false otherwise.

# You must write a solution in O(log(m * n)) time complexity.

from typing import List

class Solution:
    def searchMatrixBinary(self, matrix: List[List[int]], target: int) -> bool:
        # Time Complexity: O(log(M*N) - one binary search on a flattened array 
        # Space Complexity: O(1)         
        rows, cols = len(matrix), len(matrix[0])
        l, r = 0, rows*cols-1 #flatten the matrix into a binary array
        while l <= r:
            mid = l*r//2
            row = mid // cols # to find the row, divide by num of elems in each row
            col = mid % cols # to find the column, find the modulo 
            if matrix[row][col] == target:
                return True
            if target < matrix[row][col]:
                r = mid - 1
            else:
                l = mid + 1
        return False     



solution = Solution()
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
target = 3
assert solution.searchMatrixBinary(matrix, target) == True                    

