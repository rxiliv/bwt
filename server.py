# --- Server ---

import socket
import bwt

# Socket data
IP = "127.0.0.1"
PORT = 5000

# Open server socket (closes automatically)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Bind data to server socket
    server.bind((IP, PORT))

    # Get server to listen
    server.listen(3)

    # Accept client request and get client socket data
    conn, addr = server.accept()

    # Receive client message
    data = server.recv(1024)

    # Print request message
    print("Request message:", data.decode())

    # Encode message in BWT
    data = bwt.bwt_encode(data)

    # Send response message
    conn.sendall(data)