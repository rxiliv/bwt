   ### Gioia Chen 5BT-i
Istituto di Istruzione Superiore "Archimede" - Treviglio

# Burrows-Wheeler Transform (BWT)

Python implementation of the Burrows-Wheeler Transform (BWT) algorithm, paired with the **LSD Radix Sort** sorting algorithm using Counting Sort and integrated into a **Client-Server** network architecture based on TCP sockets.

## Contents
- [Project Description](#project-description)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [How the Algorithm Works](#how-the-algorithm-works)
- [Client-Server Architecture and Protocol](#client-server-architecture-and-protocol)
- [Usage](#usage)
- [Execution Example](#execution-example)
- [Known Limitations](#known-limitations)

---

## Project Description

The Burrows-Wheeler Transform (invented in 1994 by Michael Burrows and David Wheeler) reversibly rearranges a character string by grouping identical symbols together. This property makes it particularly useful as a preprocessing step for lossless data compression algorithms (such as `bzip2`) and for indexing and sequencing genomic data (in combination with the FM-index).

The project separates the algorithmic logic from the user interface through a Client-Server model running locally (loopback).

---

## Repository Structure

| File | Description |
| :--- | :--- |
| `bwt.py` | Main module containing the encoding (`bwt_encode`), decoding (`bwt_decode`), and sorting (`radix_sort_lsd`) functions, along with helper functions. |
| `server.py` | TCP server that imports the `bwt` module, listens on port `5000`, and processes encoding and decoding requests. |
| `client.py` | CLI client that connects to the server, gets the operation and string from the user, and displays the result. |
| `README.md` | Project documentation. |

---

## Requirements

- **Python 3.10+** (developed and tested with Python 3.14.3)
- No external libraries required: the project uses only the Python standard library (`socket`).

---

## How the Algorithm Works

The `bwt.py` module is divided into three main sections:

1. **Burrows-Wheeler Transform**
   - `bwt_encode(string)`: validates the input (extended ASCII characters 0-255 only, no `$` sentinel character), appends `$` to the end of the string, generates all cyclic rotations, sorts them lexicographically, and extracts the last column.
   - `bwt_decode(last_column)`: reconstructs the original string from the last column using the mapping between the last and first columns of the BWT matrix, starting from the `$` terminator.
2. **Sorting Algorithm**
   - `radix_sort_lsd(strings)`: lexicographically sorts the cyclic rotations from the last column to the first (Least Significant Digit) using a stable Counting Sort over an extended ASCII alphabet ($k = 256$).
3. **Helper Functions**
   - `validate_character_range(string)`: checks that all characters fall within the extended ASCII range (0-255).
   - `generate_rotations(string)`: generates all cyclic rotations of the string.
   - `calculate_cumulative_counts(string)`: calculates the cumulative frequencies of characters.
   - `generate_next_indices(last_column)`: builds the mapping between character positions in the last column and those in the first column.

---

## Client-Server Architecture and Protocol

Communication takes place via IPv4 sockets (`socket.AF_INET`) and the TCP protocol (`socket.SOCK_STREAM`) on address `127.0.0.1` at port `5000`.

To coordinate message exchange, a text-based protocol using 4-character prefixes is defined:

| Prefix | Operation | Function Executed by Server | Response |
| :--- | :--- | :--- | :--- |
| `ENC:` | BWT Encoding | `bwt.bwt_encode()` | Encoded string (with `$` terminator) |
| `DEC:` | BWT Decoding | `bwt.bwt_decode()` | Reconstructed original string |
| *Other* | Invalid command | None | `Error: Unknown operation command.` |

---

## Usage

1. Open a first terminal and start the server:
   ```bash
   python server.py
   ```
   The server will start listening on `127.0.0.1:5000`.

2. Open a second terminal and start the client:
   ```bash
   python client.py
   ```

3. Follow the on-screen instructions to choose whether to encode (`E`) or decode (`D`) and enter the desired string.

---

## Execution Example

**Encoding:**
```text
Connecting to server...
Connected!
Do you want to (E)ncode or (D)ecode? E
Insert the string: banana
Response message: annb$aa
```

**Decoding:**
```text
Connecting to server...
Connected!
Do you want to (E)ncode or (D)ecode? D
Insert the string: annb$aa
Response message: banana
```

---

## Known Limitations

- **Character set**: only extended ASCII characters (codes 0-255) are supported; the string to encode cannot contain the `$` character, which is reserved as an end-of-string marker.
- **Maximum message size**: reading via `recv(1024)` limits the size of a single payload to 1024 bytes (including the command prefix).
- **Concurrency**: the server handles requests sequentially (one connection at a time, with a maximum queue of 3 pending requests).