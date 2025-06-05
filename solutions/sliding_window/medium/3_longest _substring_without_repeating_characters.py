# Given a string s, find the length of the longest substring without duplicate characters.

# Example 1:
# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3.

# Example 2:
# Input: s = "bbbbb"
# Output: 1
# Explanation: The answer is "b", with the length of 1.

# Example 3:
# Input: s = "pwwkew"
# Output: 3
# Explanation: The answer is "wke", with the length of 3.
# Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
 
# Constraints:
# 0 <= s.length <= 5 * 104
# s consists of English letters, digits, symbols and spaces.

def find_substring_inefficiently(s: str):
    # Time: O(N^2)
    # Space: O(1)
    max_len = 0
    l, r = 0, 1
    while r < len(s):
        if s[r] in s[l:r]:
            max_len = max(max_len, len(s[l:r]))
            l = s[l:r].index(s[r]) + l + 1 # create new substring s[l:r] takes O(r-l) time complexity; for each substring searching with index() has linear complexity as well => O((r-l)^2)
        r += 1
    return max(max_len, len(s[l:r]))


def find_substring_hash(s: str):    
    # Time: O(N) - each elem is seen at most teice (by l and r pointer)
    # Space: O(k) - unique chars in hashmap  
    hashmap = {}
    max_len = 0
    l = 0
    for r in range(len(s)):
        if s[r] in hashmap:
            if hashmap[s[r]] >= l: 
                l = hashmap[s[r]] + 1
        max_len = max(max_len, r - l + 1)
        hashmap[s[r]] = r
    return max_len 
        



tests = [("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0), ("dvdf", 3)]
for i, o in tests:
    assert find_substring_inefficiently(i) == o, f"Fail, expected {o}, recieved {find_substring(i)}"
    assert find_substring_hash(i) == o, f"Fail, expected {o}, recieved {find_substring_hash(i)}"