# You are given an m x n integer matrix matrix with the following two properties:

# Each row is sorted in non-decreasing order.
# The first integer of each row is greater than the last integer of the previous row.
# Given an integer target, return true if target is in matrix or false otherwise.

# You must write a solution in O(log(m * n)) time complexity.

from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # Time Complexity: O(M*N) 
        # Space Complexity: O(1) 
        m, n = len(matrix), len(matrix[0])
        for i in range(m-1, -1, -1): #start from the last row
            if target < matrix[i][0]: #skip the row if the 1st element is too big
                continue
            for j in range(n):
                if target == matrix[i][j]:
                    return True
        return False

    def searchMatrixStaircase(self, matrix: List[List[int]], target: int) -> bool:
        # Time Complexity: O(M+N) - we don't traverse each row and column; we go m steps down and n steps left at most
        # Space Complexity: O(1)         
        row, col = 0, len(matrix[0])-1 #start at the right top elem and go left if target is smaller, or down if bigger
        while row < len(matrix) and col >= 0:
            if matrix[row][col] == target:
                return True
            if matrix[row][col] > target:
                col -= 1
            else:
                row +=1
        return False                

solution = Solution()
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
target = 3
assert solution.searchMatrix(matrix, target) == True      
assert solution.searchMatrixStaircase(matrix, target) == True              

