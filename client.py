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

    # Ask user to choose the operation
    choice = ""
    while True:
        choice = input("Do you want to (E)ncode or (D)ecode? ").strip().upper()
        if choice in ['E', 'D']:
            break
        print("Invalid choice. Please type 'E' for encode or 'D' for decode.")

    # Get string to encode in input
    message = input("Insert the string: ")

    # Format the payload with a command prefix
    prefix = "ENC:" if choice == 'E' else "DEC:"
    payload = prefix + message

    # Send message
    client.sendall(payload.encode())

    # Receive response
    data = client.recv(1024)

    # Print response
    print("Response message:", data.decode())