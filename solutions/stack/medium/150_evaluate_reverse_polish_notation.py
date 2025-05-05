# You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.

# Evaluate the expression. Return an integer that represents the value of the expression.

# Note that:

# The valid operators are '+', '-', '*', and '/'.
# Each operand may be an integer or another expression.
# The division between two integers always truncates toward zero.
# There will not be any division by zero.
# The input represents a valid arithmetic expression in a reverse polish notation.
# The answer and all the intermediate calculations can be represented in a 32-bit integer.

# Constraints:

# 1 <= tokens.length <= 104
# tokens[i] is either an operator: "+", "-", "*", or "/", or an integer in the range [-200, 200].

from typing import List

class Solution:
    def eval(self, tokens: List[str]) -> int:
        # Time complexity: O(N) - each token is pushed once
        # Space complexity: O(N) - the stack list
        stack = []
        for t in tokens:
            if t.lstrip('-').isdigit():
                stack.append(int(t))
            else:
                y = stack.pop() # mind the order!
                x = stack.pop()
                res = 0
                match t:
                    case "/":
                        res = int(x/y) # truncates toward zero
                    case "*":
                        res = x*y
                    case "-":
                        res = x-y
                    case "+":
                        res = x+y
                stack.append(res)
        return stack[-1]  


soltion = Solution()
tests = [(["2","1","+","3","*"], 9), (["4","13","5","/","+"], 6), (["10","6","9","3","+","-11","*","/","*","17","+","5","+"], 22)]
for i,o in tests:
    assert soltion.eval(i) == o, f"Fail, not {o} but {print(soltion.eval(i))}"