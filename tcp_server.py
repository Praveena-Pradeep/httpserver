import socket

# Define the host and port to bind the server to
host = '127.0.0.1'  # Localhost
port = 65432         # Non-privileged port

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {host}:{port}...")

# Accept a client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Handle communication with the client
with conn:
    while True:
        # Receive data from the client
        data = conn.recv(1024)
        if not data:
            break  # Exit if no data is received
        print(f"Received: {data.decode()}")

        # Send a response to the client
        response = f"Hello, {data.decode()}"
        conn.sendall(response.encode())

# Close the server socket
server_socket.close()


