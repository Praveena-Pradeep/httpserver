import socket
import os
import threading
import sqlite3
# Define the HTTP response template
HTTP_OK = "HTTP/1.1 200 OK\r\n"
HTTP_NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
HTTP_METHOD_NOT_ALLOWED = "HTTP/1.1 405 Method Not Allowed\r\n"
HTTP_BAD_REQUEST = "HTTP/1.1 400 Bad Request\r\n"
CONTENT_TYPE_HTML = "Content-Type: text/html\r\n"
CONTENT_TYPE_PLAIN = "Content-Type: text/plain\r\n"
CONTENT_TYPE_JSON = "Content-Type: application/json\r\n"
CONTENT_LENGTH = "Content-Length: {}\r\n"

# Directory to serve files from
DOCUMENT_ROOT = "./www"

# Parse the request headers
def parse_request(request):
    lines = request.split("\r\n")
    try:
        method, path, _ = lines[0].split(" ")
    except ValueError:
        print(f"Error: Bad Request - Could not parse the first line: {lines[0]}")
        return None, None, None, None

    headers = {}
    body = ""

    # Extract headers
    for line in lines[1:]:
        if not line:
            continue

        if ": " in line:
            header_key, header_value = line.split(": ", 1)
            headers[header_key] = header_value
    
    # For POST requests, we need to capture the body
    if method == "POST":
        body = lines[-1]
    
    return method, path, headers, body

# Handle GET request
def handle_get(path, client_socket):
    if path == "/":
        path = "/index.html"  # Default to index.html
    file_path = DOCUMENT_ROOT + path  # Fix indentation issue
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
        response = HTTP_OK + CONTENT_TYPE_HTML + CONTENT_LENGTH.format(len(content)) + "\r\n\r\n"
        client_socket.send(response.encode() + content)
    else:
        response = HTTP_NOT_FOUND + CONTENT_TYPE_HTML + "\r\n\r\n"
        client_socket.send(response.encode() + b"<h1>404 Not Found</h1>")

def connect_db():
    return sqlite3.connect('mydatabase.db')

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients
                      (name TEXT, age INTEGER)''')
    conn.commit()
    conn.close()
   
# Handle POST request
def handle_post(path, body, client_socket):
    if not body:
        print(f"Error: No POST body received for {path}")
        response = HTTP_BAD_REQUEST + CONTENT_TYPE_HTML + "\r\n\r\n"
        client_socket.send(response.encode() + b"<h1>400 Bad Request</h1>")
        return
    
    print(f"Received POST data for {path}: {body}")  # Log the POST body

    body_params = dict(param.split('=') for param in body.split('&'))
    name = body_params.get('name')
    age = body_params.get('age')

#store the data in the SQLIte database
    if name and age:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (name, age) VALUES (?, ?)", (name, age))    
        conn.commit()
        conn.close()

   # Handle /submit path
    if path == "/submit":
        response_body = f"""
        <html>
        <body>
            <h1>Received POST data:</h1>
            <p>{body}</p>
        </body>
        </html>
        """
        response = HTTP_OK + CONTENT_TYPE_HTML + CONTENT_LENGTH.format(len(response_body)) + "\r\n\r\n"
        client_socket.send(response.encode() + response_body.encode())
    
    # Handle unknown paths
    else:
        response = HTTP_NOT_FOUND + CONTENT_TYPE_HTML + "\r\n\r\n"
        client_socket.send(response.encode() + b"<h1>404 Not Found</h1>")

# Handle the client connection
def handle_client(client_socket):
    try:
        # Receive the request from the client
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            return

        # Parse the request
        method, path, headers, body = parse_request(request)
        
        # Handle GET requests
        if method == "GET":
            handle_get(path, client_socket)

        # Handle POST requests
        elif method == "POST":
            handle_post(path, body, client_socket)

        # Handle unsupported HTTP methods
        else:
            response = HTTP_METHOD_NOT_ALLOWED + CONTENT_TYPE_HTML + "\r\n\r\n"
            client_socket.send(response.encode() + b"<h1>405 Method Not Allowed</h1>")
    except Exception as e:
        print(f"Error handling request: {e}")
        response = HTTP_BAD_REQUEST + CONTENT_TYPE_HTML + "\r\n\r\n"
        client_socket.send(response.encode() + b"<h1>400 Bad Request</h1>")
    finally:
        client_socket.close()

# Start the server
def start_server(host='0.0.0.0', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server running on http://127.0.0.1:8080/")


    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Create a new thread for each client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()

