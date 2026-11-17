# --- Burrows-Wheeler Transform Algorithm ---

# Calculate all the possible combination of shifts to the right
def calculate_rotations(string: str) -> list:
    rotations = [string]

    while string[0] != '$':
        string = string[1::] + string[0]
        rotations.append(string)

    return rotations


# Get characters cumulative counts in a string
def get_cumulative_counts(string: str):
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


# Encode a string through BWT
def bwt_encode(string: str):
    # Add '$' at the end of the string
    string += '$'

    rotations = calculate_rotations(string)
    rotations = lsd_radix_sort(rotations)

    string = "".join(s[-1] for s in rotations)

    return string


# Decode a string encoded in BWT
def bwt_decode(last_column: str):
    # String length
    length = len(last_column)

    # Find first occurences positions of the given string
    cumulative = get_cumulative_counts(last_column)

    # Create index jumps map
    next_indexes = [0] * length
    current_counts = [0] * 256

    # Get characters ranks
    for i, c in enumerate(last_column):
        code = ord(c)
        rank = current_counts[code]
        current_counts[code] += 1

        # Find start index in first column
        start = cumulative[code - 1] if code > 0 else 0
        next_indexes[i] = start + rank

    # Build the reversed string from '$'
    current_index = last_column.index('$')
    result = []

    for _ in range(length):
        result.append(last_column[current_index])
        current_index = next_indexes[current_index]

    return "".join(reversed(result))