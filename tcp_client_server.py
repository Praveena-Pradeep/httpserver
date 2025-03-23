import socket
import threading
import time

# Server Code
def start_server(host='127.0.0.1', port=65432):
    # Create a socket object (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    
    # Start listening for incoming connections (max 5 clients in the queue)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")
    
    while True:
        # Accept a connection from the client
        client_socket, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        # Receive data from the client (max 1024 bytes)
        data = client_socket.recv(1024)
        print(f"Received: {data.decode()}")

        # Send a response to the client
        response = "Hello, Client! This is the server."
        client_socket.sendall(response.encode())

        # Close the connection after communication
        client_socket.close()

# Client Code
def start_client(host='127.0.0.1', port=65432):
    # Create a socket object (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((host, port))
    
    # Send a message to the server
    message = "Hello, Server!"
    client_socket.sendall(message.encode())
    
    # Receive the response from the server
    data = client_socket.recv(1024)
    print(f"Received from server: {data.decode()}")
    
    # Close the connection after communication
    client_socket.close()
# Function to start server and client in separate threads
def start_server_and_client():
    # Start the server in a new thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # This ensures the server stops when the main program stops
    server_thread.start()
    
    # Give the server a moment to start listening before starting the client
    time.sleep(1)
    
    # Start the client
    start_client()

if __name__ == '__main__':
    start_server_and_client()
