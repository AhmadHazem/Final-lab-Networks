from TCP import TCP_Segment
from TCP import TCPEnd
import sys

localIP     = "127.0.0.1"
localPort   = 54321
serverAddressPort   = ("127.0.0.1", 20001)

packet = TCP_Segment()

data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
print(sys.getsizeof(data))
client = TCPEnd()
client.set_IP_port(localIP, localPort)
status = client.intiate_handshake(serverAddressPort)
client.send_data(data, serverAddressPort)
client.close_connection(serverAddressPort)

