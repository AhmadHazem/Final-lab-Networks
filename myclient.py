from TCP import TCP_Segment
from TCP import TCPEnd
import sys

localIP     = "127.0.0.1"
localPort   = 54321
serverAddressPort   = ("127.0.0.1", 20019)
target_host = "localhost"
file1 = open("log.txt","a")

def main():
    packet = TCP_Segment()
    #data = "GET http://localhost/greet.php/ HTTP/1.1\r\nHost:{}\r\n\r\n".format(target_host)
    data = "POST http://localhost/greet.php/ HTTP/1.1\r\nHost:{}\r\n\r\nUser={}".format(target_host,"dalia")
    # print(sys.getsizeof(data))
    client = TCPEnd()
    client.set_IP_port(localIP, localPort)
    client.bind()
    status = client.intiate_handshake(serverAddressPort)
    status = client.send_data(data, serverAddressPort)
    data = ""
    if status is True:
        while True:
            segment, address = client.receive_segment()
            if segment is not None:
                print(segment)
                file1.write(str(segment) + "\n")
                client_checksum = client.checksum_calculate(segment['data'])
                if segment['packet_type'] == 'DATA':
                    if client_checksum == segment['checksum']:
                        #print(segment)
                        #file1.write(str(segment) + "\n")
                        packet = TCP_Segment()
                        packet.set_flags(ack=True)
                        packet.set_sequence_number(segment['ack_number'])
                        packet.set_ack_number(segment['sequence_number'] + 1)
                        client.current_seq_number = segment['ack_number']
                        client.current_ack_number = segment['sequence_number'] + 1
                        data += segment['data']
                        if segment['end'] == True:
                            client.send_segment(packet, address)
                            break
                    else:
                        #print(segment)
                        #file1.write(str(segment)+ "\n")
                        packet = TCP_Segment()
                        packet.set_flags(ack=False)
                        packet.set_sequence_number(segment['ack_number'])
                        packet.set_ack_number(segment['sequence_number'] )
                        client.send_segment(packet, address)
 
    client.close_connection(serverAddressPort)
    report_status = data.split("\r\n\r")[0].split("\r\n")[0].split(" ")[1] + " " + data.split("\r\n\r")[0].split("\r\n")[0].split(" ")[2]
    #print(data)
    #print(report_status)
    client.UDP_Socket.close()
    return "status for posting " + "dalia" + " is " + report_status + " ."

if __name__ == "__main__":
    finish = main()
    sys.stdout.write(finish  + "\n")
    sys.stdout.flush()
    sys.exit(0)