# Converts string into a list
def convert_to_list(string: str) -> list[str]:
    return [item for item in string]

# Checks if string is in any of alphabets
def check(string: str, *alphabets) -> bool:

    for alphabet in alphabets:
        if string in alphabet:
            return True

    return False
