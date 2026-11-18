# Constants
CHARACTER_SET_SIZE = 256



# --- Helper Functions ---

def validate_character_range(string: str) -> None:
    """
    Validates that all characters in a string belong to the supported
    ASCII character range (0-255).

    Args:
        string (str): The input string to validate.

    Raises:
        ValueError: If the string contains a character outside the
                    supported ASCII range.
    """
    if any(ord(char) >= CHARACTER_SET_SIZE for char in string):
        raise ValueError("Input must contain only ASCII characters.")


def generate_rotations(string: str) -> list[str]:
    """
    Generates all cyclic rotations of a string by repeatedly shifting
    its first character to the end, until '$' becomes the first character.

    Args:
        string (str): The input string, which must end with '$'.

    Returns:
        list: A list containing all cyclic rotations of the input string.
    """
    rotations = [string]

    for _ in range(len(string)):
        string = string[1:] + string[0]
        rotations.append(string)

    return rotations


def calculate_cumulative_counts(string: str | list[str]) -> list[int]:
    """
    Calculates the cumulative frequency of each ASCII character (0-255).

    First counts the occurrences of each character, then converts the
    frequencies into cumulative counts, representing the ending indexes
    of each character in a sorted sequence.

    Args:
        string (str): The input string to analyze.

    Returns:
        list: A list of 256 cumulative character counts.
    """
    counts = [0] * CHARACTER_SET_SIZE

    # Count frequencies
    for char in string:
        counts[ord(char)] += 1

    # Calculate cumulative indexes
    for index in range(1, CHARACTER_SET_SIZE):
        counts[index] += counts[index - 1]

    return counts


def generate_next_indices(last_column: str) -> list[int]:
    """
    Generates the mapping between character positions in the last
    and first columns of the BWT matrix.

    Args:
        last_column: The BWT-encoded string.

    Returns:
        list: A list mapping each position to its corresponding position
        in the first column.
    """
    length = len(last_column)

    cumulative_counts = calculate_cumulative_counts(last_column)

    next_indices = [0] * length
    occurrence_counts = [0] * CHARACTER_SET_SIZE

    # Calculate occurrence counts
    for index, char in enumerate(last_column):
        code = ord(char)
        rank = occurrence_counts[code]
        occurrence_counts[code] += 1

        start = cumulative_counts[code - 1] if code > 0 else 0
        next_indices[index] = start + rank

    return next_indices



# --- Sorting Algorithms ---

def radix_sort_lsd(strings: list[str]) -> list[str]:
    """
    Sorts a list of strings lexicographically using LSD (Least
    Significant Digit) Radix Sort with Counting Sort.

    Processes characters from right to left, maintaining sorting
    stability at each iteration.

    Args:
        strings (list): A list of strings of equal length to sort.

    Returns:
        list: The lexicographically sorted list of strings.
    """
    rotation_length = len(strings[0])
    n_strings = len(strings)

    # Reorder the strings starting from the least significant digit
    for index in range(rotation_length - 1, -1, -1):
        # Save the i-th column as a temporary string
        column = [string[index] for string in strings]

        # Counting sort
        counts = calculate_cumulative_counts(column)

        result = [""] * n_strings

        # Reverse iteration preserves counting sort stability
        for string in reversed(strings):
            char = ord(string[index])
            counts[char] -= 1
            result[counts[char]] = string

        # Update the strings list
        strings = result

    return strings



# --- Burrows-Wheeler Transform ---

def bwt_encode(string: str) -> str:
    """
    Encodes a string using the Burrows-Wheeler Transform (BWT).

    Appends the '$' end-of-string marker, generates all cyclic rotations,
    sorts them lexicographically, and extracts the last character
    of each sorted rotation.

    Args:
        string (str): The input string to encode.

    Returns:
        str: The Burrows-Wheeler transformed string.
    """

    # Input validation
    if '$' in string:
        raise ValueError("Input string cannot contain '$'.")
    validate_character_range();

    # Add '$' at the end of the string
    string += '$'

    rotations = generate_rotations(string)
    rotations = radix_sort_lsd(rotations)

    # Join the last character of each rotation in one string
    last_column = "".join(rotation[-1] for rotation in rotations)

    return last_column


def bwt_decode(last_column: str) -> str:
    """
    Decodes a Burrows-Wheeler transformed string to reconstruct
    the original input string.

    Reconstructs the original string by traversing the mapping
    between character positions in the last and first columns
    of the sorted rotation matrix.

    Args:
        last_column (str): The BWT-encoded string, including '$'.

    Returns:
        str: The original string, without the '$' end-of-string marker.
    """
    # Input validation
    validate_character_range();

    # Generate mapping positions between first and last column
    next_indices = generate_next_indices(last_column)

    # Build the reversed string starting from '$'
    current_index = last_column.index('$')
    result = []

    for _ in range(len(last_column)):
        result.append(last_column[current_index])
        current_index = next_indices[current_index]

    result = "".join(reversed(result))

    return result
