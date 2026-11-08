# --- Burrows-Wheeler Transform Algorithm ---


# Calculate all the possible combination of shifts to the right
def calculate_rotations(string: str) -> list:
    rotations = [string]

    while string[0] != '$':
        string = string[1::] + string[0]
        rotations.append(string)

    print(rotations)

    return rotations


# Sort rotations lexicographically (through LSD radix sort)
def lsd_radix_sort(strings):
    string_length = len(strings[0])
    n_strings = len(strings)

    # Counting sort
    for i in range(string_length - 1, -1, -1):
        counters = [0] * 256
        result = [""] * n_strings

        # Count frequencies
        for s in strings:
            counters[ord(s[i])] += 1

        # Get cumulative indexes
        for j in range(1, 256):
            counters[j] += counters[j - 1]

        # Order in reverse (mantaining stability)
        for s in reversed(strings):
            char_code = ord(s[i])
            counters[char_code] -= 1
            result[counters[char_code]] = s

        print(result)

        strings = result

    return strings


# Take the last character of each sorted rotation
def get_transform(rotations: list) -> str:
    transform = ""
    
    for temp in rotations:
        transform += temp[-1]

    return transform


# Encode a string through BWT
def bwt_encode(string: str):
    # Add '$' at the end of the string
    string += '$'

    rotations = calculate_rotations(string)

    rotations = lsd_radix_sort(rotations)
    
    return get_transform(rotations)


if __name__ == "__main__":
    print(bwt_encode("banana"))
    # lsd_radix_sort(["zuwu", "auwu", "euss"])