import socket

def handle_request(client_socket):
    try:
        # Receive the request from the client
        request = client_socket.recv(1024).decode()
        print("Request received:")
        print(request)

        # Split the request into lines and process
        lines = request.split("\r\n")
        if len(lines) > 0:
            # Split the first line to get method, path, and HTTP version
            method, path, _ = lines[0].split(" ")
            print(f"Method: {method}, Path: {path}")

            # Handle GET / (home page)
            if method == "GET":
                if path == "/":
                    response_body = """<html>
                    <head>
                        <style>
                            body {
                                background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPvgRAut3jqvRVH71WNibGa-w1GN-D4u8BKQ&s');
                                background-size: cover;
                                background-position: center;
                                background-attachment: fixed;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Welcome to My HTTP Server</h1>
                    </body>
                    </html>"""

                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
                else:
                    response_body = "<html><body><h1>404 Not Found</h1></body></html>"
                    response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
                client_socket.send(response.encode())
            else:
                response_body = "<html><body><h1>405 Method Not Allowed</h1></body></html>"
                response = f"HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
                client_socket.send(response.encode())

        client_socket.close()

    except Exception as e:
        response_body = f"<html><body><h1>400 Bad Request</h1><p>{str(e)}</p></body></html>"
        response = f"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
        client_socket.send(response.encode())
        client_socket.close()

def run_http_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    print(f"Server running on http://127.0.0.1:8080/")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_request(client_socket)

if __name__ == "__main__":
    run_http_server()

