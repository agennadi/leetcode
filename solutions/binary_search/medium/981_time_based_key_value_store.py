# Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

# Implement the TimeMap class:

# TimeMap() Initializes the object of the data structure.
# void set(String key, String value, int timestamp) Stores the key with the value at the given time timestamp.
# String get(String key, int timestamp) Returns a value such that set was called previously, with timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".
 

# Example 1:
# Input
# ["TimeMap", "set", "get", "get", "set", "get", "get"]
# [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
# Output
# [null, null, "bar", "bar", null, "bar2", "bar2"]

# Constraints:
# 1 <= key.length, value.length <= 100
# key and value consist of lowercase English letters and digits.
# 1 <= timestamp <= 107
# All the timestamps timestamp of set are strictly increasing.
# At most 2 * 105 calls will be made to set and get.
from collections import defaultdict

class TimeMap:
    def __init__(self):
        # Space: O(N)
        self.time_map = defaultdict(list) 

    
    def set(self, k : str, v: str, timestamp : int):
        # Time: O(1)
        self.time_map[k].append((v, timestamp))


    def get(self, k : str, timestamp : int):
        # timestamps are strictly increasing - binary search
        # return the value with the given timestamp or with the next largest timestamp
        # Space: O(1) - local variables 
        # Time: O(logM) - O(1) for dict lookup and O(logM) for binary search 
        if k not in self.time_map:
            return ''
        values = self.time_map[k] 
        l, r = 0, len(values) - 1
        res = ''
        while l <= r:
            mid = (l+r)//2
            if values[mid][1] > timestamp:
                r = mid - 1
            else: #this can be the right element or there can be a bigger one that is still smaller than timestamp
                res = values[mid][0] # save it in case this is the biggest allowed timestamp
                l = mid + 1
        return res


time_map = TimeMap()
time_map.set("foo", "bar", 1) # store the key "foo" and value "bar" along with timestamp = 1.
assert time_map.get("foo", 1) == "bar" 
assert time_map.get("foo", 3) == "bar", f"Fail, returned {time_map.get("foo", 3)}"
time_map.set("foo", "bar2", 4) 
assert time_map.get("foo", 4) == "bar2" 
assert time_map.get("foo", 5) == "bar2" 

