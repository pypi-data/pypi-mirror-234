import re

def tokenize(regex):
    stack = ""
    last = ""
    def match(text):
        nonlocal stack
        nonlocal last
        matcher = re.match(regex, text)
        if (matcher and matcher.lastgroup == "noise"):
            return None
        stack = stack + text
        matcher = re.search(regex, stack)
        if matcher and matcher.lastgroup == last:
          stack = ""
          return None
        if matcher:
            stack = ""
            last = matcher.lastgroup
            return (matcher.lastgroup, matcher.group())
        return None
    return match
