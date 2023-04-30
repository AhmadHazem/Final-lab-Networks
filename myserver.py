from TCP import TCP_Segment
from TCP import TCPEnd
import sys

localIP     = "127.0.0.1"
localPort   = 20019

file1 = open("log.txt","a")
Server = TCPEnd()
Server.set_IP_port(localIP, localPort)
Server.bind()
whole_data_recieved = []
data = ""
c = 0
while True:
    segment , address = Server.receive_segment()
    if segment is not None:
        server_checksum = Server.checksum_calculate(segment['data'])
        if segment['packet_type'] == 'SYN':
            if server_checksum == segment['checksum']:
                print(segment)
                file1.write(str(segment) + "\n")
                packet = TCP_Segment()
                packet.set_flags(syn=True, ack=True)
                packet.set_ack_number(segment['sequence_number'] + 1)
                print(packet)
                file1.write(str(packet) + "\n")
                Server.send_segment(packet, address)
            else:
                print(segment)
                file1.write(str(segment) + "\n")
                packet = TCP_Segment()
                packet.set_ack_number(segment['sequence_number'])
                packet.set_flags(syn=True, ack=False)
                Server.send_segment(packet, address)
        elif segment['packet_type'] == 'DATA':
            if server_checksum == segment['checksum']:
                print(segment)
                file1.write(str(segment) + "\n")
                packet = TCP_Segment()
                packet.set_flags(ack=True)
                packet.set_sequence_number(segment['ack_number'])
                packet.set_ack_number(segment['sequence_number'] + 1)
                data += segment['data']
                c += 1
                if segment['end'] == True:
                    Server.send_segment(packet, address)
                    response = Server.process_request(data)
                    data = ""
                    #print(response)
                    #file1.write(str(response) + "\n")
                    Server.current_seq_number += c
                    Server.current_ack_number += c
                    Server.send_data(response, address)
                    c = 0
            else:
                print(segment)
                file1.write(str(segment))
                packet = TCP_Segment()
                packet.set_flags(ack=False)
                packet.set_sequence_number(segment['ack_number'])
                packet.set_ack_number(segment['sequence_number'] )
                Server.send_segment(packet, address)
        elif segment['packet_type'] == 'FIN':
            if server_checksum == segment['checksum']:
                print(segment)
                file1.write(str(segment) + "\n")
                packet = TCP_Segment()
                packet.set_flags(fin=True, ack=True)
                packet.set_sequence_number(segment['ack_number'])
                packet.set_ack_number(segment['sequence_number'] + 1)
                Server.send_segment(packet, address)
                break
            else:
                print(segment)
                file1.write(str(segment) + "\n")
                packet = TCP_Segment()
                packet.set_flags(fin=True, ack=False)
                packet.set_sequence_number(segment['ack_number'])
                packet.set_ack_number(segment['sequence_number'] )
                Server.send_segment(packet, address)
        
        elif segment['packet_type'] == 'ACK':
            print(segment)
            file1.write(str(segment) + "\n")
        Server.current_seq_number = segment['sequence_number']
        Server.current_ack_number = segment['ack_number']




