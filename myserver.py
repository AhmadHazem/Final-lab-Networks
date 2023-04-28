from TCP import TCP_Segment
from TCP import TCPEnd
import sys

localIP     = "127.0.0.1"
localPort   = 20001

Server = TCPEnd()
Server.set_IP_port(localIP, localPort)
Server.bind()
while True:
    segment , address = Server.receive_segment()
    if segment is not None:
        server_checksum = Server.checksum_calculate(segment['data'])
        if segment['packet_type'] == 'SYN':
            if server_checksum != segment['checksum']:
                print(segment)
                packet = TCP_Segment()
                packet.set_flags(syn=True, ack=False)
                packet.set_ack_number(segment['sequence_number'] + 1)
                print(packet)
                Server.send_segment(packet, address)
            else:
                print(segment)
                packet = TCP_Segment()
                packet.set_ack_number(segment['sequence_number'])
                packet.set_flags(syn=True, ack=True)
                Server.send_segment(packet, address)
        elif segment['packet_type'] == 'DATA':
            if server_checksum != segment['checksum']:
                print(segment)
                packet = TCP_Segment()
                packet.set_flags(ack=True)
                packet.set_sequence_number(segment['ack_number'])
                packet.set_ack_number(segment['sequence_number'] + 1)
                Server.send_segment(packet, address)
            else:
                print(segment)
                packet = TCP_Segment()
                packet.set_flags(ack=True)
                packet.set_sequence_number(segment['ack_number'])
                packet.set_ack_number(segment['sequence_number'] + 1)
                Server.send_segment(packet, address)
        elif segment['packet_type'] == 'FIN':
            if server_checksum != segment['checksum']:
                print(segment)
                packet = TCP_Segment()
                packet.set_flags(fin=True, ack=True)
                packet.set_sequence_number(segment['ack_number'])
                packet.set_ack_number(segment['sequence_number'] + 1)
                Server.send_segment(packet, address)
            else:
                print(segment)
                packet = TCP_Segment()
                packet.set_flags(fin=True, ack=True)
                packet.set_sequence_number(segment['ack_number'])
                packet.set_ack_number(segment['sequence_number'] + 1)
                Server.send_segment(packet, address)
        elif segment['packet_type'] == 'ACK':
            print(segment)
        Server.current_seq_number = segment['sequence_number']
        Server.current_ack_number = segment['ack_number']




