# -*- coding: utf-8 -*-
import random
import ast
import socket
import math

# Constants
BUFFERSIZE = 1024
LAST_CONNECTION = -1
FIRST = 0

class TCP_Segment:
    def __init__(self):
        self.source_port = None
        self.destination_port = None
        #Sequence number and acknoledgement number
        self.seuqence_number = self.generateSeqNumber()
        self.ack_number = 0
        #flags
        self.ack = False
        self.rst = False
        self.syn = False
        self.fin = False
        #Window size 
        self.window_size = 50
        self.checksum = 0
        self.data = " "
    
    def set_ack_number(self, ack_number):
        self.ack_number = ack_number

    def set_sequence_number(self, sequence_number):
        self.seuqence_number = sequence_number

    def generateSeqNumber(self):
        return random.randint(0, 4294967295)

    def set_flags(self, ack=False, syn=False, fin=False):
        self.ack = ack
        self.syn = syn
        self.fin = fin

    def set_data(self, data):
        self.data = data

    def packet_type(self):
        packet_type = ""
        if self.syn and self.ack:
            packet_type = "SYN-ACK"
        elif self.ack and self.fin:
            packet_type = "FIN-ACK"
        elif self.syn:
            packet_type = "SYN"
        elif self.ack:
            packet_type = "ACK"
        elif self.fin:
            packet_type = "FIN"
        elif self.data != "":
            packet_type = "DATA"
        return packet_type
    

class TCPEnd(object):
    def __init__(self):
        self.status = 0
        self.UDP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDP_Socket.settimeout(0.5)
        self.current_seq_number = 0
        self.current_ack_number = 0
        self.cwnd = 50
        self.localIP = None
        self.localPort = None
    
    def set_IP_port(self, IP, port):
        self.localIP = IP
        self.localPort = port

    def bind(self):
        self.UDP_Socket.bind((self.localIP, self.localPort))

    def checksum_calculate(self,s):
        total = 0
        for c in s:
            total += ord(c)
        return total % 256

    def prepare_segment(self, segment):
        self.the_segment = {
            "sequence_number": segment.seuqence_number,
            "ack_number": segment.ack_number,
            "source_port": segment.source_port,
            "destination_port": segment.destination_port,
            "ack": segment.ack,
            "rst": segment.rst,
            "syn": segment.syn,
            "fin": segment.fin,
            "packet_type": segment.packet_type(),
            "window_size": segment.window_size,
            "checksum": segment.checksum,
            "data": segment.data
        }
        return str(self.the_segment)
    
    def send_segment(self, segment, address):
        segment.source_port = self.localPort
        segment.destination_port = address[1]
        segment.checksum = self.checksum_calculate(segment.data)
        string_segment = self.prepare_segment(segment)
        self.UDP_Socket.sendto(string_segment.encode("utf-8"), address)


    def receive_segment(self):
        try:
            segment, address = self.UDP_Socket.recvfrom(BUFFERSIZE)
            segment = segment.decode('utf-8')
            segment = ast.literal_eval(segment)
            return segment, address
        except socket.timeout:
            return "Timeout", None
        
    def intiate_handshake(self, address):
        segment = TCP_Segment()
        segment.set_flags(syn=True)
        self.send_segment(segment, address)
        while True:
            response, address = self.receive_segment()
            if response is not None:
                if response["syn"] and response["ack"]:
                    response['destination_port'] = 54321
                    print(response)
                    third_reply = TCP_Segment()
                    third_reply.set_flags(ack=True)
                    third_reply.set_ack_number(response["sequence_number"] + 1)
                    third_reply.set_sequence_number(response["ack_number"])
                    self.send_segment(third_reply, address)
                    self.current_seq_number = third_reply.seuqence_number + 1
                    self.current_ack_number = third_reply.ack_number 
                    return True
                elif response["syn"] and not response["ack"]:
                    self.send_segment(segment, address)

    
    def close_connection(self, address):
        segment = TCP_Segment()
        segment.set_flags(fin=True)
        segment.set_sequence_number(self.current_seq_number)
        segment.set_ack_number(self.current_ack_number)
        self.send_segment(segment, address)
        while True:
            response, address = self.receive_segment()
            if response is not None:
                if response["fin"] and response["ack"]:
                    response['destination_port'] = 54321
                    print(response)
                    third_reply = TCP_Segment()
                    third_reply.set_flags(ack=True)
                    third_reply.set_ack_number(response["sequence_number"] + 1)
                    third_reply.set_sequence_number(response["ack_number"])
                    self.send_segment(third_reply, address)
                    self.current_seq_number = third_reply.seuqence_number + 1
                    self.current_ack_number = third_reply.ack_number
                    return True
                elif response["fin"] and not response["ack"]:
                    self.send_segment(segment, address)

    def send_data(self, data, address):
        number_of_segments = math.ceil(len(data) / self.cwnd)
        for i in range(number_of_segments):
            segment = TCP_Segment()
            packet_data = data[i * self.cwnd : (i + 1) * self.cwnd]
            segment.set_data(packet_data)
            segment.set_sequence_number(self.current_seq_number)
            segment.set_ack_number(self.current_ack_number)
            self.send_segment(segment, address)
            self.current_seq_number = segment.seuqence_number + 1
        while True:
            segment, address = self.receive_segment()
            if segment is not None:
                if segment["ack"] and self.current_seq_number <= segment["sequence_number"]:
                    segment['destination_port'] = 54321
                    print(segment)
                    self.current_seq_number = segment["ack_number"] + 1
                    self.current_ack_number = segment["sequence_number"] + 1
                    break
                elif not segment["ack"] or segment == "Timeout":
                    self.current_seq_number = self.current_seq_number - i
                    for i in range(number_of_segments):
                        segment = TCP_Segment()
                        packet_data = data[i * self.cwnd : (i + 1) * self.cwnd]
                        segment.set_data(packet_data)
                        segment.set_sequence_number(self.current_seq_number)
                        segment.set_ack_number(self.current_ack_number)
                        self.send_segment(segment, address)
                        self.current_seq_number = segment.seuqence_number + 1
        return True
                
    




