# --- Burrows-Wheeler Transform Algorithm ---

# Constants
ASCII_SIZE = 256


# Calculate all the possible combination of shifts to the right
def generate_rotations(string: str) -> list[str]:
    rotations = [string]

    while string[0] != '$':
        string = string[1::] + string[0]
        rotations.append(string)

    return rotations


# Get characters cumulative counts in a string
def calculate_cumulative_counts(string: str) -> list[int]:
    counts = [0] * ASCII_SIZE

    # Count frequencies
    for c in string:
        counts[ord(c)] += 1

    # Get cumulative indexes
    for i in range(1, ASCII_SIZE):
        counts[i] += counts[i - 1]

    # Return cumulative indexes
    return counts


# Sort rotations lexicographically (through LSD radix sort)
def radix_sort_lsd(strings: list[str]) -> list[str]:
    rotation_length = len(strings[0])
    n_strings = len(strings)

    # Reorder the strings starting from the least significant digit
    for i in range(rotation_length - 1, -1, -1):
        # Save the i-th column as a temporary string
        column = [string[i] for string in strings]

        # Counting sort
        counts = calculate_cumulative_counts(column)

        result = [""] * n_strings

        # Reverse iteration preserves counting sort stability
        for s in reversed(strings):
            char = ord(s[i])
            counts[char] -= 1
            result[counts[char]] = s

        # Update the strings list
        strings = result

    return strings


# Encode a string through BWT
def bwt_encode(string: str) -> str:
    # Add '$' at the end of the string
    string += '$'

    rotations = generate_rotations(string)
    rotations = radix_sort_lsd(rotations)

    # Join the last character of each rotation in one string
    string = "".join(rotation[-1] for rotation in rotations)

    return string


# Decode a string encoded in BWT
def bwt_decode(last_column: str) -> str:
    length = len(last_column)

    # Find first occurences positions of the given string
    cumulative_counts = calculate_cumulative_counts(last_column)

    # Create index jumps map
    next_indices = [0] * length
    character_ranks = [0] * ASCII_SIZE

    # Get characters ranks
    for i, c in enumerate(last_column):
        code = ord(c)
        rank = character_ranks[code]
        character_ranks[code] += 1

        # Find start index in first column
        start = cumulative_counts[code - 1] if code > 0 else 0
        next_indices[i] = start + rank

    # Build the reversed string from '$'
    current_index = last_column.index('$')
    result = []

    for _ in range(length):
        result.append(last_column[current_index])
        current_index = next_indices[current_index]

    return "".join(reversed(result))