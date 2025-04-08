# Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and is decoded back to the original list of strings.

# Machine 1 (sender) has the function:

# string encode(vector<string> strs) {
#   // ... your code
#   return encoded_string;
# }
# Machine 2 (receiver) has the function:
# vector<string> decode(string s) {
#   //... your code
#   return strs;
# }
# So Machine 1 does:

# string encoded_string = encode(strs);
# and Machine 2 does:

# vector<string> strs2 = decode(encoded_string);
# strs2 in Machine 2 should be the same as strs in Machine 1.

# Implement the encode and decode methods.
from typing import List

class Codec:
    def encode_non_ascii(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string.
        """
        return '🌍'.join(s for s in strs) #O(n)
        

    def decode_non_ascii(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings.
        """
        return s.split('🌍') #O(n)


codec = Codec()
strs = ["Hello","World"]
assert codec.decode_non_ascii(codec.encode_non_ascii(strs)) == strs