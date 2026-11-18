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

            raw_message = data.decode()
            print("Request message:", raw_message)

            # Determine operation based on prefix protocol
            if raw_message.startswith("ENC:"):
                text_to_process = raw_message[4:]
                print(f"Action: BWT Encode")
                result = bwt.bwt_encode(text_to_process)
            elif raw_message.startswith("DEC:"):
                text_to_process = raw_message[4:]
                print(f"Action: BWT Decode")
                result = bwt.bwt_decode(text_to_process)
            else:
                result = "Error: Unknown operation command."

            # Send response message (ensure it's bytes)
            if isinstance(result, str):
                result = result.encode()

            conn.sendall(result)
            print("Response sent.")