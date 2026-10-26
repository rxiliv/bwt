if __name__ == "__main__":
    # Richiesta della stringa in input
    stringa = str(input("Inserisci una stringa: "))

    # Aggiunta di '$' alla fine della stringa
    stringa += '$'

    # Calcolo di tutte le possibili rotazioni verso destra della stringa
    shift = list()

    while stringa[0] != '$':
        stringa += stringa[0]
        stringa = stringa[1::]
        shift.append(stringa)

    # Riordine delle rotazioni lessicograficamente
    for i, parola in enumerate(shift):
        index = i
        for j in range(len(shift) - i):
            if shift[j] < parola:
                index = j
        temp = parola
        shift[i] = shift[j]
        shift[j] = temp