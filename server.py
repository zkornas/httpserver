import socket

host = ""
port = 80

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind((host, port))
tcp_socket.listen()

print(f"Listening for connection on {port}")

while True:
    # Wait for client connections
    client_connection, client_address = tcp_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    headers = request.split('\n')
    filename = headers[0].split()[1]

    # Open resource
    if filename == '/':
        filename = '/index.html'
    
    try:
        page = open('docs' + filename)
        content = page.read()
        page.close

        response = 'HTTP/1.1 200 OK \n\n' + content
    except FileNotFoundError:
        response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()


#tcp_socket.close()
