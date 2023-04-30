import socket

HOST = 'localhost'
PORT = 8090
webpage = open('greet.php', 'r').read()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{PORT}')
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        request = conn.recv(1024)
        request = request.decode('utf-8').split('\r\n')
        print(request)
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{}'.format(webpage)
        conn.sendall(response.encode('utf-8'))
        while True:
            request = conn.recv(1024)
            if request is not None:
                request = request.decode('utf-8').split('\r\n')
                break
        print(request)