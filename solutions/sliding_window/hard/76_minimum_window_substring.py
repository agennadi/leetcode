# Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".
# The testcases will be generated such that the answer is unique.

# Example 1:
# Input: s = "ADOBECODEBANC", t = "ABC"
# Output: "BANC"
# Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

# Example 2:
# Input: s = "a", t = "a"
# Output: "a"
# Explanation: The entire string s is the minimum window.

# Example 3:
# Input: s = "a", t = "aa"
# Output: ""
# Explanation: Both 'a's from t must be included in the window.
# Since the largest window of s only has one 'a', return empty string.
 
# Constraints:
# m == s.length
# n == t.length
# 1 <= m, n <= 105
# s and t consist of uppercase and lowercase English letters.
 
from collections import Counter, defaultdict

def find_min_win(s: str, t: str) -> str:
    # Space: O(N+M) - t_counter and s_counter
    # Time: O(M) - we iterate over s 
    res = ""
    t_counter = Counter(t)
    s_counter = defaultdict(int)
    l = 0
    have, need = 0, len(t_counter) # t_counter, not t, as we only count unique chars
    for r in range(len(s)):
        char = s[r]
        s_counter[char] += 1
        if char in t_counter and t_counter[char] == s_counter[char]:
            have += 1
        while have == need:
            if len(res) == 0 or len(res)> r-l+1:
                res = s[l:r+1]
            s_counter[s[l]] -= 1 # move the left wall
            if s[l] in t_counter and s_counter[s[l]] < t_counter[s[l]]:
                have -= 1
            l += 1
    return res

    # 0: A:1
    # 1: A:1 D:1
    # 2: A:1 D:1 O:1
    # 3: A:1 D:1 O:1 B:1
    # 4: A:1 D:1 O:1 B:1 E:1
    # 5: A:1 D:1 O:1 B:1 E:1 C:1 -> ADOBEC res="ADOBEC" 
    # Res found, so we shift the left wall by one -> D:1 O:1 B:1 E:1 C:1
    # 6: D:1 O:2 B:1 E:1 C:1
    # 7: D:2 O:2 B:1 E:1 C:1
    # 8: D:2 O:2 B:1 E:2 C:1
    # 9: D:2 O:2 B:2 E:2 C:1
    # 10: D:2 O:2 B:2 E:2 C:1 A:1 -> DOBECODEBA res="ADOBEC" because new res is bigger 
    # New potential res found, so we shift the left wall by one -> D:1 O:2 B:2 E:2 C:1 A:1 -> OBECODEBA res="ADOBEC" because new res is bigger
    # New potential res found (OBECODEBA), so we shift the left wall by one -> D:1 O:1 B:2 E:2 C:1 A:1 -> BECODEBA res="ADOBEC" because new res is bigger
    # New potential res found (BECODEBA), so we shift the left wall by one -> D:1 O:1 B:1 E:2 C:1 A:1 -> ECODEBA res="ADOBEC" because new res is bigger
    # New potential res found (ECODEBA), so we shift the left wall by one -> D:1 O:1 B:1 E:1 C:1 A:1 -> CODEBA res="ADOBEC" because new res has equal length
    # New potential res found (ODEBA), so we shift the left wall by one -> D:1 O:1 B:1 E:1 A:1 -> this is not a valid window, shift the right wall instead
    # 11: D:1 O:1 B:1 E:1 A:1 N:1
    # 12: D:1 O:1 B:1 E:1 A:1 N:1 C:1 -> ODEBANC res="ADOBEC" because new res is bigger
    # New potential res found (ODEBANC), so we shift the left wall by one -> D:1 B:1 E:1 A:1 N:1 C:1 -> DEBANC res="ADOBEC" because new res has equal length
    # New potential res found (DEBANC), so we shift the left wall by one -> B:1 E:1 A:1 N:1 C:1 -> EBANC res="EBANC" because new res is smaller than the old one
    # New res found (EBANC), so we shift the left wall by one -> B:1 A:1 N:1 C:1 -> BANC res="BANC" because new res is smaller than the old one
    # New res found (BANC),  so we shift the left wall by one -> A:1 N:1 C:1 -> this is not a valid window and we can't shift the right wall => res="BANC"

tests = [("ADOBECODEBANC", "ABC", "BANC"), ("a", "a", "a"), ("a", "aa", ""), ("aa", "aa", "aa")]
for s, t, o in tests:
    assert find_min_win(s,t) == o, f"Failed, expected {o}, returned {find_min_win(s,t)}"