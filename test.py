import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("localhost", 8085))
sock.send(b"POST http://localhost/greet.php/ HTTP/1.1\r\nHost:localhost\r\n\r\nUser=dummy")
while True:
    try:
        response = sock.recv(4096)
        if response is not None:
            break
    except socket.timeout:
        sock.send(b"POST http://localhost/greet.php/ HTTP/1.1\r\nHost:localhost\r\n\r\nUser=dummy")

sock.close()
print(response.decode())