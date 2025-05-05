# Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

# Constraints:
# 1 <= n <= 8

class Solution:
    def generate(self, n):
        res = []
        def backtrack(stack, l_count, r_count):
            if len(stack) == 2*n:
                res.append(''.join(stack))
            if l_count < n: 
                stack.append('(')
                backtrack(stack, l_count+1, r_count)
                stack.pop()
            if r_count < l_count:
                stack.append(')')
                backtrack(stack, l_count, r_count+1)
                stack.pop()
        backtrack([], 0, 0)
        return res


solution = Solution()
tests = [(3, ["((()))","(()())","(())()","()(())","()()()"]), (1, ["()"])]
for i,o in tests:
    assert solution.generate(i) == o, f"Fail, not {o} but {print(solution.generate(i))}"