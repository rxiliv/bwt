# --- Algoritmo della Trasformata di Burrows-Wheeler ---

def bwt(string: str):
    # Richiesta della stringa in input
    stringa = str(input("Inserisci una stringa: "))

    # Aggiunta di '$' alla fine della stringa
    stringa += '$'

    # Calcolo di tutte le possibili rotazioni verso destra della stringa
    shift = [stringa]

    while stringa[0] != '$':
        stringa += stringa[0]
        stringa = stringa[1::]
        shift.append(stringa)

    # Riordine delle rotazioni lessicograficamente
    for i in range(len(shift)):
        index = i
        for j in range(i + 1, len(shift)):
            if shift[j] < shift[index]:
                index = j
        shift[i], shift[j] = shift[j], shift[i]

    # Estrapolazione della trasformata
    trasformata = ""
    for parola in shift:
        trasformata += parola[len(parola) - 1]
    
    return trasformata