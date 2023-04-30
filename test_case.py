from TCP import TCP_Segment
from TCP import TCPEnd
import sys

localIP     = "127.0.0.1"
localPort   = 54321
serverAddressPort   = ("127.0.0.1", 20028)
target_host = "localhost"

def main():
    packet = TCP_Segment()
    client = TCPEnd()
    data = "hello world"
    packet.set_data(data)
    client.set_IP_port(localIP, localPort)
    client.bind()
    status = client.intiate_handshake(serverAddressPort)
    client.send_corrupted_segment(packet, serverAddressPort)
    while True:
        segment, address = client.receive_segment()
        if segment is not None:
            if segment['packet_type'] == 'ACK':
               print(segment)
               
            else:
                 segment['packet_type'] = 'NACK'
                 print(segment)
                 client.send_data(data, serverAddressPort)
                 break
if __name__ == "__main__":
    finish = main()