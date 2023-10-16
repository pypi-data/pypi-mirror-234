test = """
Updated Function:

```python
def disable(self) -> None:
    # Setting the instance attribute __has_gpu to False
    # We denote private variables by prefixing them with double underscore (__)
    # Here, __has_gpu indicates whether our instance keeps track of GPU utilization or not
    # By setting it to False, we're disabling GPU accounting
    self.__has_gpu = False
```
"""

import re

def find_code_start(code: str) -> int:
    """
    Finds the starting location of a code block in a string.

    Args:
        code: A string containing code.

    Returns:
        An integer representing the starting position of the code block.

    """
    lines = code.split('\n')
    i = 0
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    while not lines[i].strip().startswith('```'):
        i += 1
    first_line = lines[i]
    offset = 3
    if first_line == '```':
        return offset
    matched = re.match(r'^```(?P<language>[a-z]*)', first_line)
    if matched:
        offset += len(matched.group('language')) + 1
        word = first_line[offset:].strip()
        if len(word) >= 0 and ' ' not in word:
            return len(word) + offset
    return -1

print(find_code_start(test))
