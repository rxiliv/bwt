### Gioia Chen 5BT-i
Istituto di Istruzione Superiore "Archimede" - Treviglio

# Burrows-Wheeler Transform (BWT)

Implementazione in Python dell'algoritmo della Trasformata di Burrows-Wheeler (BWT), abbinato all'algoritmo di ordinamento **LSD Radix Sort** con Counting Sort e integrato in un'architettura di rete **Client-Server** basata su socket TCP.

## Contenuti
- [Descrizione del progetto](#descrizione-del-progetto)
- [Struttura della repository](#struttura-della-repository)
- [Requisiti](#requisiti)
- [Funzionamento dell'algoritmo](#funzionamento-dellalgoritmo)
- [Architettura Client-Server e protocollo](#architettura-client-server-e-protocollo)
- [Utilizzo](#utilizzo)
- [Esempio di esecuzione](#esempio-di-esecuzione)
- [Limiti noti](#limiti-noti)

---

## Descrizione del progetto

La Trasformata di Burrows-Wheeler (ideata nel 1994 da Michael Burrows e David Wheeler) riorganizza una stringa di caratteri in modo reversibile raggruppando insieme simboli uguali. Questa proprietà la rende particolarmente utile come fase preliminare per algoritmi di compressione senza perdita di dati (come `bzip2`) e per l'indicizzazione e il sequenziamento di dati genomici (in combinazione con l'FM-index).

Il progetto separa la logica algoritmica dall'interfaccia utente tramite un modello Client-Server in esecuzione locale (loopback).

---

## Struttura della repository

| File | Descrizione |
| :--- | :--- |
| `bwt.py` | Modulo principale contenente le funzioni di codifica (`bwt_encode`), decodifica (`bwt_decode`), ordinamento (`radix_sort_lsd`) e le funzioni di supporto. |
| `server.py` | Server TCP che importa il modulo `bwt`, rimane in ascolto sulla porta `5000` ed elabora le richieste di codifica e decodifica. |
| `client.py` | Client CLI che si connette al server, acquisisce l'operazione e la stringa dall'utente e visualizza il risultato. |
| `README.md` | Documentazione del progetto. |

---

## Requisiti

- **Python 3.10+** (sviluppato e testato con Python 3.14.3)
- Nessuna libreria esterna richiesta: il progetto utilizza esclusivamente la libreria standard di Python (`socket`).

---

## Funzionamento dell'algoritmo

Il modulo `bwt.py` è suddiviso in tre sezioni principali:

1. **Burrows-Wheeler Transform**
   - `bwt_encode(string)`: valida l'input (solo caratteri ASCII estesi 0-255, assenza del carattere sentinella `$`), aggiunge `$` alla fine della stringa, genera tutte le rotazioni cicliche, le ordina lessicograficamente ed estrae l'ultima colonna.
   - `bwt_decode(last_column)`: ricostruisce la stringa originale a partire dall'ultima colonna utilizzando la mappatura tra ultima e prima colonna della matrice BWT, partendo dal terminatore `$`.
2. **Sorting Algorithm**
   - `radix_sort_lsd(strings)`: ordina lessicograficamente le rotazioni cicliche procedendo dall'ultima colonna alla prima (Least Significant Digit) tramite Counting Sort stabile su alfabeto ASCII esteso ($k = 256$).
3. **Helper Functions**
   - `validate_character_range(string)`: verifica che tutti i caratteri rientrino nell'intervallo ASCII esteso (0-255).
   - `generate_rotations(string)`: genera tutte le rotazioni cicliche della stringa.
   - `calculate_cumulative_counts(string)`: calcola le frequenze cumulative dei caratteri.
   - `generate_next_indices(last_column)`: costruisce la mappatura tra le posizioni dei caratteri dell'ultima colonna e quelle della prima.

---

## Architettura Client-Server e protocollo

La comunicazione avviene tramite socket IPv4 (`socket.AF_INET`) e protocollo TCP (`socket.SOCK_STREAM`) sull'indirizzo `127.0.0.1` alla porta `5000`.

Per coordinare lo scambio di messaggi è definito un protocollo testuale basato su prefissi di 4 caratteri:

| Prefisso | Operazione | Funzione eseguita dal Server | Risposta |
| :--- | :--- | :--- | :--- |
| `ENC:` | Codifica BWT | `bwt.bwt_encode()` | Stringa codificata (con terminatore `$`) |
| `DEC:` | Decodifica BWT | `bwt.bwt_decode()` | Stringa originale ricostruita |
| *Altro* | Comando non valido | Nessuna | `Error: Unknown operation command.` |

---

## Utilizzo

1. Aprire un primo terminale e avviare il server:
   ```bash
   python server.py
   ```
   Il server si metterà in ascolto su `127.0.0.1:5000`.

2. Aprire un secondo terminale e avviare il client:
   ```bash
   python client.py
   ```

3. Seguire le istruzioni a schermo per scegliere se codificare (`E`) o decodificare (`D`) e inserire la stringa desiderata.

---

## Esempio di esecuzione

**Codifica:**
```text
Connecting to server...
Connected!
Do you want to (E)ncode or (D)ecode? E
Insert the string: banana
Response message: annb$aa
```

**Decodifica:**
```text
Connecting to server...
Connected!
Do you want to (E)ncode or (D)ecode? D
Insert the string: annb$aa
Response message: banana
```

---

## Limiti noti

- **Set di caratteri**: sono supportati solo caratteri ASCII estesi (codici 0-255); la stringa da codificare non può contenere il carattere `$`, riservato come marcatore di fine stringa.
- **Dimensione massima del messaggio**: la lettura tramite `recv(1024)` limita la dimensione del singolo payload a 1024 byte (incluso il prefisso di comando).
- **Concorrenza**: il server gestisce le richieste in modo sequenziale (una connessione alla volta, con coda massima di 3 richieste pendenti).
