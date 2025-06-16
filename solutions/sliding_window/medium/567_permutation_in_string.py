# Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.
# In other words, return true if one of s1's permutations is the substring of s2.

# Example 1:
# Input: s1 = "ab", s2 = "eidbaooo"
# Output: true
# Explanation: s2 contains one permutation of s1 ("ba").
# Example 2:

# Input: s1 = "ab", s2 = "eidboaoo"
# Output: false
 

# Constraints:
# 1 <= s1.length, s2.length <= 104
# s1 and s2 consist of lowercase English letters.

# a:0 b:0
# l=0 r=0 e 
# l=1 r=1 i
# l=2 r=2 d
# l=3 r=3 b a:0 b:1 
# l=3 r=4 a:1 b: 1
# window size = len(s1)
from collections import Counter, defaultdict

def find_permutation_failed(s1 : str, s2: str) -> bool:
    # this code won't work for the following test case: s1="adc" s2="dcda" - we need to track the window size
    # Space: O(N)
    # Time: O(M*N)
    s1_counter = Counter(s1)
    win_counter = defaultdict(int)
    l, r = 0, 0
    while r < len(s2): #O(M)    
        if s2[r] in s1_counter:
            win_counter[s2[r]] += 1
            if win_counter == s1_counter: #O(N) comparison
                return True                
        else:
            win_counter.clear() #O(1)
        l +=1
        r +=1
    print(win_counter)
    return False


def find_permutation(s1 : str, s2: str) -> bool:
    # Space: O(N)
    # Time: O(M*N)
    s1_counter = Counter(s1)
    s2_counter = defaultdict(int)
    l, r = 0, 0
    while r < len(s2): #O(M)    
        s2_counter[s2[r]] += 1
        if r - l + 1 > len(s1):
            s2_counter[s2[l]] -= 1
            if s2_counter[s2[l]] == 0:
                del s2_counter[s2[l]]
            l += 1
        if s2_counter == s1_counter: #O(N) comparison
            return True                
        r +=1
    return False


tests = [("ab", "eidbaooo", True), ("ab", "eidboaoo", False), ("b", "b", True), ("ab", "babababa", True), ("adc", "dcda", True)]
for s1, s2, o in tests:
    assert find_permutation(s1, s2) == o, f"Failed, expected {o}, returned {find_permutation_failed(s1, s2)}"
            


