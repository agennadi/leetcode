# There are n cars at given miles away from the starting mile 0, traveling to reach the mile target.
# You are given two integer array position and speed, both of length n, where position[i] is the starting mile of the ith car and speed[i] is the speed of the ith car in miles per hour.
# A car cannot pass another car, but it can catch up and then travel next to it at the speed of the slower car.
# A car fleet is a car or cars driving next to each other. The speed of the car fleet is the minimum speed of any car in the fleet.
# If a car catches up to a car fleet at the mile target, it will still be considered as part of the car fleet.
# Return the number of car fleets that will arrive at the destination.

# Constraints:
# n == position.length == speed.length
# 1 <= n <= 105
# 0 < target <= 106
# 0 <= position[i] < target
# All the values of position are unique.
# 0 < speed[i] <= 106

from typing import List

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        # zip the position and speed: [(10,2), (8,4), (0,1), (5,1), (3,3)]
        # sort by position: [(0,1), (3,3), (5,1), (8,4), (10,2)]
        # to find steps till target: (target - position) / speed
        # steps = [12, 3, 7, 1, 1]
        # stack = []
        # steps.pop(); stack empty => stack.append(1)
        # steps.pop(); stack[-1] == curr => don't do anything, as they are one fleet
        # steps.pop(); stack[-1] < curr; the curr car will never catch up with the previous fleet => stack.append(7): [1,7]
        # steps.pop(); stack[-1] > curr; the curr car is faster than the prev, so it will catch up => do nothing
        # steps.pop(); stack[-1] < curr; the curr car will never catch up with the prev, so append => stack.append(12) [1,7,12]
        # len(steps) == num of fleets

        # Time complexity: O(NlogN)
        # Space complexity: O(N)
        cars = zip(position, speed) #O(N)
        cars = sorted(cars, key=lambda x:x[0]) #O(NlogN)
        steps = [(target-car[0])/car[1] for car in cars] #O(N)
        stack = []
        while steps: #O(N)
            curr = steps.pop()
            if not stack or stack[-1] < curr:
                stack.append(curr) 
            else:
                continue
        return len(stack)  


solution = Solution()
tests = [(12, [10,8,0,5,3], [2,4,1,1,3], 3), (10, [3], [3], 1), (100, [0,2,4], [4,2,1], 1), (10, [8,3,7,4,6,5], [4,4,4,4,4,4], 6)]
for target, pos, speed, output in tests:
    assert solution.carFleet(target, pos, speed) == output, f"Failed" 