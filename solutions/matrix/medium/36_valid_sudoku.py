# Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

# Each row must contain the digits 1-9 without repetition.
# Each column must contain the digits 1-9 without repetition.
# Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
# Note:

# A Sudoku board (partially filled) could be valid but is not necessarily solvable.
# Only the filled cells need to be validated according to the mentioned rules.

# Constraints:
# board.length == 9
# board[i].length == 9
# board[i][j] is a digit 1-9 or '.'.
from typing import List
from collections import defaultdict


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Time Complexity: O(N²) + O(N²) + O(N²) = O(N²)
        # Space Complexity: O(N²)          
        l = len(board)
        for row in board:
            hashmap = {}
            for r in row:
                if not r.isdigit():
                    continue
                if r in hashmap:
                    return False
                hashmap[r] = 1
        for col in range(l):
            hashmap = {}
            for row in range(l):
                val = board[row][col]
                if not val.isdigit():
                    continue
                if val in hashmap:
                    return False
                hashmap[val] = 1
        for row in range(0, l, 3):
            triple = board[row: row+3]
            bound = 0
            while bound <= 9:
                hashmap = {}
                for t in triple:
                    r = t[bound:bound+3]
                    for elem in r:
                        if not elem.isdigit():
                            continue
                        if elem in hashmap:
                            return False
                        hashmap[elem] = 1 
                bound +=3
        return True

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Time Complexity: O(N²) because we need to traverse every position in the board
        # Space Complexity: O(N²) if the board is full, we need a hash set each with size N to store all seen numbers
        rows = defaultdict(set)
        cols = defaultdict(set)
        blocks = defaultdict(set)
        N = len(board)
        for i in range(N):
            for j in range(N):
                if board[i][j] == '.':
                    continue
                val = board[i][j]
                if val in rows[i] or val in cols[j] or val in blocks[(i//3,j//3)]:
                    return False
                rows[i].add(val)
                cols[j].add(val)
                blocks[(i//3,j//3)].add(val) 
        return True        


board1 = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]        
board2 =[["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
board3 = [[".",".",".",".","5",".",".","1","."],[".","4",".","3",".",".",".",".","."],[".",".",".",".",".","3",".",".","1"],["8",".",".",".",".",".",".","2","."],[".",".","2",".","7",".",".",".","."],[".","1","5",".",".",".",".",".","."],[".",".",".",".",".","2",".",".","."],[".","2",".","9",".",".",".",".","."],[".",".","4",".",".",".",".",".","."]]
solution = Solution()
assert solution.isValidSudoku(board1) == True
assert solution.isValidSudoku(board2) == False
assert solution.isValidSudoku(board3) == False