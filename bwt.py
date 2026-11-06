# --- Burrows-Wheeler Transform Algorithm ---

def bwt(string: str):
    # String input request
    string = str(input("Inserisci una stringa: "))

    # Add '$' at the end of the string
    string += '$'

    # Calculate all the possible rotations to the right
    shift = [string]

    while string[0] != '$':
        string += string[0]
        string = string[1::]
        shift.append(string)

    # Lexicographically sort rotations 
    for i in range(len(shift)):
        index = i
        for j in range(i + 1, len(shift)):
            if shift[j] < shift[index]:
                index = j
        shift[i], shift[j] = shift[j], shift[i]

    # Resolute transform
    transform = ""
    for temp in shift:
        transform += temp[len(temp) - 1]
    
    return transform