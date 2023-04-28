import socket
from TCP import TCP_Segment
HOST = "127.0.0.1" 
PORT = 65432  

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    packet = TCP_Segment()
    packet.set_data("Hello World")
    string = packet.formulate_segment()
    s.sendall(bytes(string, 'utf-8'))
    data = s.recv(1024)
    print(f"Received {data!r}")
