import re

def strings(filename, min=4):
    with open(filename, 'rb') as f:
        data = f.read()
        # Regular expression to find sequences of printable characters
        pattern = f"[\\x20-\\x7E]{{{min},}}"
        printable_chars = re.findall(pattern.encode(), data)

        # Decode the byte sequences to strings
        printable_strings = [sequence.decode() for sequence in printable_chars]
        return printable_strings

