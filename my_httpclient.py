import socket

def client_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    request = "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    print(f"Response from server: {response}")
    client_socket.close()

if __name__ == "__main__":
    client_request()

