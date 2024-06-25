# src/main.py
from regex_engine import match, findall, search, split, sub

alphabet = set('abcdefghijklmnopqrstuvwxyz')

# Example Usage
patterns = ["a*b|c", "ab", "a|b", "a*", "a+", "[^a]", "^a", "a$", "(ab)", "a?"]
strings = ["aaab", "ab", "a", "aaaa", "b", "", "aa", "ba", "ab", ""]

for pattern in patterns:
    for string in strings:
        print(f"Pattern: {pattern}, String: {string} -> Match: {match(pattern, string, alphabet)}")

print(findall("a", "aaab", alphabet))  # ['a', 'a', 'a']
print(search("a", "aaab", alphabet))  # 0
print(split("a", "aaab", alphabet))  # ['', '', '', 'b']
print(sub("a", "x", "aaab", alphabet))  # 'xxxb'
