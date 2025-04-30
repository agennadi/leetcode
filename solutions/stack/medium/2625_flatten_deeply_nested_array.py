# Given a multi-dimensional array arr and a depth n, return a flattened version of that array.

# A multi-dimensional array is a recursive data structure that contains integers or other multi-dimensional arrays.

# A flattened array is a version of that array with some or all of the sub-arrays removed and replaced with the actual elements in that sub-array. This flattening operation should only be done if the current depth of nesting is less than n. The depth of the elements in the first array are considered to be 0.

# Example 1:

# Input
# arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
# n = 0
# Output
# [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]

# Example 2:

# Input
# arr = [[1, 2, 3], [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
# n = 2
# Output
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

class Solution:
    def flatStack(self, arr, n):
        # Time Complexity: O(N) - each elem is processed once 
        # Space Complexity: O(N) - res list 
        stack, res = [], []
        for a in reversed(arr): # LIFO
            stack.append((a,n))
        while stack:
            elem, depth = stack.pop() # pop the elem on top
            if isinstance(elem, list) and depth > 0:
                for e in reversed(elem):  #push back into the LIFO stack, hence reverse 
                    stack.append((e, depth - 1))
            else:
                res.append(elem)
        return res


solution = Solution()
arr1, n1, output1 = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]], 0, [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
arr2, n2, output2 = [[1, 2, 3], [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]], 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
arr3, n3, output3 = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]], 1, [1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11], 12, 13, 14, 15]

assert solution.flatStack(arr1, n1) == output1
assert solution.flatStack(arr2, n2) == output2
assert solution.flatStack(arr3, n3) == output3