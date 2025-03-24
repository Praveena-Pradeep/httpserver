import socket

# Define the server's address and port
host = '127.0.0.1'  # Localhost
port = 65432         # The same port the server is listening on

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))

# Send data to the server
message = "World"  # Example message
client_socket.sendall(message.encode())

# Receive a response from the server
data = client_socket.recv(1024)
print(f"Received from server: {data.decode()}")

# Close the client socket
client_socket.close()



