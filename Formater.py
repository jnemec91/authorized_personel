import re

def change_string_format(s):
    # Define the regex pattern to match the format "A-PR-500", "S-P3-240", "C-P12-100"
    pattern = re.compile(r"([A-Z]+-[A-Z0-9]+)-(\d+)")

    # List to store the transformed strings
    transformed_strings = []

    if isinstance(s, str):
        s = s.strip()
        if pattern.match(s):
            transformed_strings.append(pattern.sub(r"\1.\2", s))
            s = transformed_strings[0]

    return s