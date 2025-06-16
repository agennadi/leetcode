# You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
# Return the max sliding window.

# Example 1:
# Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
# Output: [3,3,5,5,6,7]
# Explanation: 
# Window position                Max
# ---------------               -----
# [1  3  -1] -3  5  3  6  7       3
#  1 [3  -1  -3] 5  3  6  7       3
#  1  3 [-1  -3  5] 3  6  7       5
#  1  3  -1 [-3  5  3] 6  7       5
#  1  3  -1  -3 [5  3  6] 7       6
#  1  3  -1  -3  5 [3  6  7]      7

# Example 2:
# Input: nums = [1], k = 1
# Output: [1] 

# Constraints:
# 1 <= nums.length <= 105
# -104 <= nums[i] <= 104
# 1 <= k <= nums.length


from collections import deque


def find_max_elems(nums: list, k: int) -> list:
    # Space: O(k) - max window size in queue 
    # Time: O(N) - each elem is added to and popped from the queue at most once
    max_list = []
    l = 0
    q = deque() # queue to store indices of monotonically decreasing elements in the window
    for r in range(len(nums)):
        while q and nums[r] > nums[q[-1]]: # if curr element is bigger than the previous ones, pop them
            q.pop()
        q.append(r)
        
        if r-l+1 >= k: #if the window >= k
            while q and q[0] < l: # make sure to remove stale elements
                q.popleft()               
            max_list.append(nums[q[0]])
            l +=1     
    return max_list


# We can solve it by brute force - i.e. find max for each k elems in n with time complexity of O(N*K)
# This will likely result in TLE
# If nums[i] > nums[i-1], we can disregard nums[i-1], as it will never be the max element
# 1 => q=[1]
# 3>1 => q=[3]
# -1 < 3 => q=[3, -1]
# we went over k elems, so we put q[0] in the max_list = [3] and l+=1. We don't popleft() because both elements will still be considered for the next window. their indices > l
# -3<-1 => q=[3, -1, -3] 
# we went over the next k elems, so we put q[0] in the max_list = [3, 3] and l+=1. Now we popleft() once because index of 3 < l. In this case we only remove one elem but i code I'll use "while"
# 5>-1>-3 => q=[5]
# we went over k elems, so we put q[0] in the max_list = [3, 3, 5] and l+=1. index of 5 >= l => we keep 5 in the queue
# 3<5 => q[5, 3]
# we went over k elems, so we put q[0] in the max_list = [3, 3, 5, 5] and l+=1. index of 5 >= l => we keep 5 in the queue
# 6>5>3 = q=[6]
# we went over k elems, so we put q[0] in the max_list = [3, 3, 5, 5, 6] and l+=1. index of 6 >= l => we keep 6 in the queue
# 7>6 => q=[7]
# we went over k elems, so we put q[0] in the max_list = [3, 3, 5, 5, 6, 7] and l+=1. index of 6 >= l => we keep 6 in the queue
# r is out of bounds, return max_list = [3, 3, 5, 5, 6, 7]

tests = [([1,3,-1,-3,5,3,6,7], 3, [3,3,5,5,6,7]), ([1], 1, [1])]
for nums, k, o in tests:
    assert find_max_elems(nums, k) == o, f"Failes, expected {o}, returned {find_max_elems(nums, k)}"