# --- Client ---

import socket

# Server socket data
IP = "127.0.0.1"
PORT = 5000

# Open client socket (closes automatically)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    # Connect to server
    print("Connecting to server...")
    client.connect((IP, PORT))
    print("Connected!")

    # Get string to encode in input
    message = input("Insert the string to encode with BWT: ")

    # Send message
    client.sendall(message.encode())

    # Receive response
    data = client.recv(1024)

    # Print response
    print("Response message:", data.decode())