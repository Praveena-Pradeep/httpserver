import socket

# Function to send HTTP POST request with user-entered data
def send_post_request(host, port, path):
    # Ask the user for their name and age
    name = input("Enter your name: ")  # Get name from the user
    age = input("Enter your age: ")    # Get age from the user
    
    # Ensure age is a number, else prompt again
    while not age.isdigit():
        print("Please enter a valid number for age.")
        age = input("Enter your age: ")
    
    # Prepare the body for the POST request
    body = f"name={name}&age={age}"
    
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((host, port))
    
    # Create the HTTP POST request
    request = f"POST {path} HTTP/1.1\r\n"
    request += "Host: " + host + "\r\n"
    request += "Content-Type: application/x-www-form-urlencoded\r\n"
    request += f"Content-Length: {len(body)}\r\n"
    request += "\r\n"
    request += body
    
    # Send the request
    client_socket.send(request.encode())
    
    # Receive the response
    response = client_socket.recv(1024).decode('utf-8')
    print("Response from server:")
    print(response)
    
    # Close the connection
    client_socket.close()

# Call the function to send the POST request with user-entered name and age
send_post_request('127.0.0.1', 8080, "/submit")
