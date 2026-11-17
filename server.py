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
    print(f"Server listening on {IP}:{PORT}...")

    # Main server loop
    while True:
        # Accept client request and get client socket data
        conn, addr = server.accept()
        print(f"Request accepted from client {addr[0]}:{addr[1]}")

        with conn:
            # Receive client message
            data = conn.recv(1024)
            if not data:
                continue

            # Decode data
            decoded_data = data.decode()

            # Print request message
            print("Request message:", decoded_data)

            # Encode message in BWT
            encoded_data = bwt.bwt_encode(decoded_data)

            # Send response message
            conn.sendall(encoded_data.encode())