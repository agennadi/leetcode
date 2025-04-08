# Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

# Example 1:
# Input: nums = [1,1,1,2,2,3], k = 2
# Output: [1,2]

from collections import Counter
import heapq
from typing import List

class Solution:
    def topKFrequentSort(self, nums: List[int], k: int) -> List[int]:
        # Time Complexity: O(N log N) - sorting the hashtable
        # Space Complexity: O(N) - N elems in the hashtable and res list
           
        hashtable = {}
        for num in nums: # O(N)
            hashtable[num] = hashtable.get(num, 0) + 1        
        res = sorted(hashtable.items(), key=lambda x:x[1]) # O(N log N)
        return [x[0] for x in res[-k:]] # O(K)   

    def topKFrequentCounter(self, nums: List[int], k: int) -> List[int]:
        # Time Complexity: O(N logK) - counter
        # Space Complexity: O(N log N) - count.most_common() uses sort in the worst case

        count = Counter(nums) # O(N)
        return [e[0] for e in count.most_common(k)] # O(N log N)


    def topKFrequentHeap(self, nums: List[int], k: int) -> List[int]:
        # Time Complexity: O(N logK) - heap
        # Space Complexity: O(N)

        hashtable = {}
        for num in nums: #O(N)
            hashtable[num] = hashtable.get(num, 0) + 1
        items = [(v,k) for k,v in hashtable.items()] #O(N)
        heapq.heapify(items)  # O(N)
        while len(items) > k: # O(NlogK)
            heapq.heappop(items)
        return [item[1] for item in items] # O(K)            


    def topKFrequentHeapCounter(self, nums: List[int], k: int) -> List[int]:
        # Time Complexity: O(N logK) - heap
        # Space Complexity: O(N)

        count = Counter(nums) # O(N)
        return heapq.nlargest(k, count.keys(), key=count.get) # O(N log K)

solution = Solution()
nums = [1,1,1,2,2,3]
k = 2
output = ([1,2], [2,1])
funcs = [solution.topKFrequentSort, solution.topKFrequentCounter, solution.topKFrequentHeap, solution.topKFrequentHeapCounter]
for func in funcs:
    assert func(nums, k) in output
