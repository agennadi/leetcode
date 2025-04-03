# You are climbing a staircase. It takes n steps to reach the top.
# Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

# Example 1:

# Input: n = 2
# Output: 2
# Explanation: There are two ways to climb to the top.
# 1. 1 step + 1 step
# 2. 2 steps
# Example 2:

# Input: n = 3
# Output: 3
# Explanation: There are three ways to climb to the top.
# 1. 1 step + 1 step + 1 step
# 2. 1 step + 2 steps
# 3. 2 steps + 1 step 

class Solution:
    def climbStairsSlow(self, n: int) -> int: 
      # Time Complexity: O(2^N) - each call leads to 2 recursive calls, which resukts in a binary recursion tree 
      # Space Complexity: O(N) - recursive call stack of length n

      if n == 0:
            return 0
      if n == 1:
            return 1
      if n == 2:
           return 2 
      return self.climbStairsSlow(n-2) + self.climbStairsSlow(n-1)    

    # Previous approach was too slow because of redundant calculations.  
    # Memoization is used to store previously calculated values.
    def climbStairsMemoization(self, n: int, memo={}) -> int: 
      # Time Complexity: O(N) - each value is calculated once due to the hashtable
      # Space Complexity: O(N) - memoization hash table      
      
      if n in memo:
            return memo[n]
      if n == 0:
            return 0
      if n == 1:
            return 1
      if n == 2:
           return 2 
      memo[n] = self.climbStairsMemoization(n-2) + self.climbStairsMemoization(n-1)            
      return memo[n]            

solution = Solution()
assert solution.climbStairsSlow(2) == 2
assert solution.climbStairsSlow(3) == 3
#assert solution.climbStairsSlow(44) == 1134903170

assert solution.climbStairsMemoization(2) == 2
assert solution.climbStairsMemoization(3) == 3
assert solution.climbStairsMemoization(44) == 1134903170