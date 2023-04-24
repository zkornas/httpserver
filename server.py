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
    #print(request)

    headers = request.split('\n')
    request_type = headers[0].split()[0]

    print(headers[0])
    print(request_type)

    # Open resource
    if request_type == 'GET':
        filename = headers[0].split()[1]
        print(filename)
        if filename == '/':
            filename = '/index.html'
        
        try:
            page = open(filename[1:], 'rb')
            content = page.read()
            page.close

            response = "HTTP/1.1 200 OK\r\n"
            if filename == 'sal.JPG':
                response += "Content-Type: image/jpeg\r\n"
            else:
                response += "Content-Type: text/html\r\n"
                response += "Content-Length: " + str(len(content)) + "\r\n"
                response += "\r\n" + content

        except FileNotFoundError:
            response = 'HTTP/1.1 404 NOT FOUND\r\nFile Not Found'

        # Send HTTP response
        try:
            client_connection.sendall(response.encode())
        except UnicodeDecodeError:
            client_connection.sendall(response.encode('utf-16'))
        client_connection.close()
    elif request_type == 'POST':
        print(request_type)
    elif request_type == 'PUT':
        print(request_type)
    elif request_type == 'DELETE':
        print(request_type)
    else:
        print('403 FORBIDDEN')

        




#tcp_socket.close()
