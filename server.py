import socket

host = ""
port = 80

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(host, port)

tcp_socket.listen()

print(f"Listening for connection on {port}")

while True:
    client_connection, client_address = tcp_socket.accept()

    request = client_connection.recv(1024).decode()
    print(request)

    response = 'HTTP/1.1 200 ok \n\n Hello!'
    client_connection.sendall(response.encode())
    client_connection.close()


#tcp_socket.close()
