from TCP import TCP_Segment
from TCP import TCPEnd
import sys

localIP     = "127.0.0.1"
localPort   = 54321
serverAddressPort   = ("127.0.0.1", 20001)


target_host = "www.google.com"
packet = TCP_Segment()
data = "GET / HTTP/1.1\r\nHost:{}\r\n\r\n".format(target_host)
print(sys.getsizeof(data))
client = TCPEnd()
client.set_IP_port(localIP, localPort)
status = client.intiate_handshake(serverAddressPort)
client.send_data(data, serverAddressPort)
client.close_connection(serverAddressPort)

