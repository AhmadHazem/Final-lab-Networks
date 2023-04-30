import socket

HOST = 'localhost'
PORT = 8090

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{PORT}')
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        request = conn.recv(1024)
        request = request.decode('utf-8').split('\r\n')
        response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello World'
        conn.sendall(response)
        for r in request:
            print(r)