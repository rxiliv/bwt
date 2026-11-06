# --- Burrows-Wheeler Transform Algorithm ---

# Calculate all the possible combination of shifts to the right
def calculate_rotations(string: str) -> list:
    rotations = [string]

    while string[0] != '$':
        string = string[1::] + string[0]
        rotations.append(string)

    return rotations
    
# Sort rotations lexicographically
def sort_rotations(rotations: list):
    for i in range(len(rotations)):
        index = i
        for j in range(i + 1, len(rotations)):
            if rotations[j] < rotations[index]:
                index = j
        rotations[i], rotations[j] = rotations[j], rotations[i]

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

    sort_rotations(rotations)
    
    return get_transform(rotations)