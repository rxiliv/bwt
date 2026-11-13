# --- Burrows-Wheeler Transform Algorithm ---


# Calculate all the possible combination of shifts to the right
def calculate_rotations(string: str) -> list:
    rotations = [string]

    while string[0] != '$':
        string = string[1::] + string[0]
        rotations.append(string)

    return rotations

# Partial counting sort
def get_cumulative_counts(string: str):
    length = len(string)

    counts = [0] * 256

    # Count frequencies
    for c in string:
        counts[ord(c)] += 1

    # Get cumulative indexes
    for i in range(1, 256):
        counts[i] += counts[i - 1]

    # Return cumulative indexes
    return counts


# Sort rotations lexicographically (through LSD radix sort)
def lsd_radix_sort(strings):
    string_length = len(strings[0])
    n_strings = len(strings)

    # Reorder the strings starting from the least significant digit
    for i in range(string_length - 1, -1, -1):
        # Save the i-th column as a temporary string
        column = [s[i] for s in strings]

        # Counting sort
        counts = get_cumulative_counts(column)

        result = [""] * n_strings

        # Order in reverse (in order to mantain stability)
        for s in reversed(strings):
            char = ord(s[i])
            counts[char] -= 1
            result[counts[char]] = s

        # Update the strings list
        strings = result

    return strings


# Get the BWT
def get_transform(rotations: list) -> str:
    transform = ""

    # Take the last character of each sorted rotation
    for s in rotations:
        transform += s[-1]

    return transform


# Encode a string through BWT
def bwt_encode(string: str):
    # Add '$' at the end of the string
    string += '$'

    rotations = calculate_rotations(string)
    rotations = lsd_radix_sort(rotations)

    return get_transform(rotations)

# Decode a string encoded in BWT
def bwt_decode(last_column: str):
    # String length
    length = len(last_column)

    # Lexicographically ordered string
    first_column = [""] * length

    # Original string
    reversed = [""] * length

    # Lexicographically order given string
    # Counting sort
    counts = get_cumulative_counts(last_column)

    # Order in reverse (in order to mantain stability)
    for c in reversed(last_column):
        code = ord(c)
        counts[code] -= 1
        first_column[counts[code]] = c

    for i in range(length):
        ...


if __name__ == "__main__":
    print(bwt_encode("banana"))