import socket

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a local address and port
server_socket.bind(('192.168.1.5', 8090))

# listen for incoming connections
server_socket.listen(1)

# accept incoming connections
while True:
    # wait for a client to connect
    client_socket, address = server_socket.accept()

    # receive the HTTP request
    request = ''
    while True:
        data = client_socket.recv(1024).decode()
        request += data
        if '\r\n\r\n' in request:
            break

    # print the HTTP request
    print(request)

    # close the client socket
    client_socket.close()