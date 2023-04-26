import socket
import os

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

    filename = headers[0].split()[1]

    # Open resource
    if request_type == 'GET':
        print(filename)
        if filename == '/':
            filename = '/index.html'
        
        try:
            page = open(filename[1:])
            content = page.read()
            page.close

            response = "HTTP/1.1 200 OK\r\n"

            if filename == 'text.txt':
                response += "Content-Type: text/plain\r\n"
            else:
                response += "Content-Type: text/html\r\n"
                response += "Content-Length: " + str(len(content)) + "\r\n"
                response += "\r\n" + content

        except FileNotFoundError:
            response = 'HTTP/1.1 404 NOT FOUND File Not Found\r\n\r\n'
            print("I'm returning a 404 error")

        # Send HTTP response
        client_connection.sendall(response.encode())
        client_connection.close()
    elif request_type == 'POST':
        if os.path.isfile(filename[1:]):
            content = headers[7]
            with open(filename[1:], "a") as myfile:
                myfile.write(content)
            response = "HTTP/1.1 200 OK\r\n"
        else:
            response = 'HTTP/1.1 404 NOT FOUND\r\nFile Not Found'

    elif request_type == 'PUT':
        if os.path.isfile(filename[1:]):
            os.remove(filename[1:])
        fp = open(filename[1:], 'x')
        s = '\n'.join(str(x) for x in headers[10:])
        fp.write(s)
        fp.close()
        response = "HTTP/1.1 200 OK\r\n"
        client_connection.sendall(response.encode())
        client_connection.close()
    elif request_type == 'DELETE':
        if os.path.isfile(filename[1:]):
            os.remove(filename[1:])
            response = "HTTP/1.1 200 OK\r\n"
        else:
            response = 'HTTP/1.1 404 NOT FOUND\r\nFile Not Found'
        client_connection.sendall(response.encode())
        client_connection.close()
    
    else:
        print('403 FORBIDDEN')

        




#tcp_socket.close()

#TODO
#   Ask Eric about not getting 404 error for GET, but printing when getting to that line.
#   Remove hard code for GET content type/length
