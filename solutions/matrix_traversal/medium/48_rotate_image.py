#You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).
#You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. 
#DO NOT allocate another 2D matrix and do the rotation.
#Example:
#Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
#Output: [[7,4,1],[8,5,2],[9,6,3]]

from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix[0]) #find the side length of a matrix
        for i in range(n):
            for j in range(i):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j] #transpose
        for row in matrix:
            row.reverse()


solution = Solution()
matrix = [[1,2,3],[4,5,6],[7,8,9]]
rotated_matrix = [[7,4,1],[8,5,2],[9,6,3]]
solution.rotate(matrix)
print(matrix)
assert matrix == rotated_matrix
