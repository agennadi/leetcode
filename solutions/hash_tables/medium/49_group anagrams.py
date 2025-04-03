# Given an array of strings strs, group the anagrams together. You can return the answer in any order.
# Example 1:

# Input: strs = ["eat","tea","tan","ate","nat","bat"]
# Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

# 1 <= strs.length <= 104
# 0 <= strs[i].length <= 100 
from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Time Complexity: O(N * K * logK) - sorting string takes O(k log k) for N strings 
        # Space Complexity: O(N * K) - hashtable stores N keys, each key takes up K space

        hashtable = {}
        for s in strs:
            k = tuple(sorted(s)) #remember that lists and sets are not hashable
            hashtable.setdefault(k, []).append(s) #hashmap.get(group, []).append(s) won't work because it's not storing the list - can also use collections.defaultdict
        return list(hashtable.values())            

    def groupAnagramsOptimized(self, strs: List[str]) -> List[List[str]]:
        # Time Complexity: O(N * K) - no sorting
        # Space Complexity: O(N * K) - hashtable stores N keys, each key takes up K space

        hashtable = defaultdict(list)
        for s in strs:
            count = [0] * 26 #alphabet counter
            for c in s: #one-hot encoding for each word 
                count[ord(c) - ord('a')] += 1 
            hashtable[tuple(count)].append(s) 
        return list(hashtable.values())          

solution = Solution()
strs = ["eat","tea","tan","ate","nat","bat"]
output = [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
assert solution.groupAnagrams(strs) == output
assert solution.groupAnagramsOptimized(strs) == output