"""
formater.py
This module defines the change_string_format function, which formats a room number
to a specific format.
"""
import re

def change_string_format(s: str) -> str:
    """
    finds all occurrences of the regex pattern in the string and replaces them with the new format.
    """
    pattern = re.compile(r"\b([A-Z0-9]+-[A-Z0-9]+\d*)-(\d+[a-zA-Z]?)\b")

    if isinstance(s, str):
        s = s.strip().upper()
        # Replace all matching patterns in the string
        matches = pattern.findall(s)
        for match in matches:
            # Construct the new format using the matched groups
            s = f"{match[0]}.{match[1]}"

        return s

    return s


if __name__ == '__main__':
    print(change_string_format('A-PR-500'))
    print(change_string_format('S-P3-240'))
    print(change_string_format('C-P12-100'))
    print(change_string_format('D1-P1-100'))
    print(change_string_format('D-P6-402b'))
    print(change_string_format('D1-S1-402'))
