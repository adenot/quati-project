#!/usr/bin/env python

import sys, os, time, string, re

import socket

from Common.Functions import *

"""
@package Sensor
@namespace Sniffer



@title Sniff Network
@goal Receive network packets from a network interface
@context Network interface
@actor System, Pcap, Network Interface
@resource Network Packet
@episode Open network interface to sniff

"""

class Sniffer:
    """This class's objective is to sniff the network and calls apropriate class to process the data
    
    @todo: connections list may grow up a little too much. we can clean the oldies from time to time
    """
    
    ## trigger filters elements printable
    packet_printable = filter(lambda c: c not in string.whitespace, string.printable) + ' '
    ## history of connections
    connections = []
    ## history of connections types
    connections_types = []
    
    def __init__(self, pcapObj,agentObj,sensorObj):
        """Initiate the class"""
                
        self.pcap = pcapObj
        
        self.agent = agentObj
        
        self.sensor = sensorObj
        
        self.IPs = []
        self.IPs = getIPs()
        
        self.run()

    def run(self):
        """Sniff ad infinitum.
        #PacketHandler shall be invoked by pcap for every packet."""
        self.pcap.loop(0, self.packetHandler)

    def checkPacket(self,data):
        """Test hexadecimal parts of the packet, filtering and determining their type, and then calling the alert
        the data goes to self.connections and self.connections_types
        
        @see getPacketType
        
        Filter IP and TCP packets
        After the first packet is identified, discard the others.
        
        captured example packet (telnet)
         0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
        00 1c 42 95 a1 9b 00 1c 42 00 00 01 08 00 45 10 00 36 2b d9 40 00 40 06 8b 2c 0a d3 37 02 0a d3 37 05 c1 f2 00 17 6b 81 60 7d 4f fd cc bc 80 18 ff ff 8c 26 00 00 01 01 08 0a 2c c4 0e 0e 01 86 72 c5 0d 00 
        
        @param data data captured from pcap
        
        @type data: string
        
        @return false if packet isnt ip and tcp or hasnt the right size
        @return true if the packet is identified (even as unknown)
        
        
        
        @title Parse Network Packet
        @goal Extract information from a packet
        @context Packet is received from Pcap library
        @actor System
        @resource Network Packet
        @episode The packet is checked
        
        """

        '''
        @episode The lenght is tested
        '''
        if len(data) < 59:
            return False

        '''
        @episode The type of packet (must be IP) 
        '''
        if ord(data[12]) != 0x08 or ord(data[13]) != 0x00 :
            return False
        
        '''
        @episode The packet protocol must be TCP (0x06, UDP would be 0x17)
        '''
        if ord(data[23]) != 0x06 :
            return False

        '''
        @episode The source and destination IPs (bytes 12/16)
        '''
        src_ip = socket.inet_ntoa(data[26:30])
        dst_ip = socket.inet_ntoa(data[30:34])

        '''
        @exception Cant be one of system IPs
        '''
        if dst_ip in self.IPs or src_ip in self.IPs:
            return False

        '''
        @episode The source and destination ports
        '''
        src_port = int('%x%x' % (ord(data[34]),ord(data[35])),16)
        dst_port = int('%x%x' % (ord(data[36]),ord(data[37])),16)

        # 38,39,40,41: seq number
        # 42,43,44,45: ack number
        # 46: data offset & reserved
        # 47: tcp options
        # 48,49: window size
        # 50,51: checksum
        # 52,53: urgent pointer
        # 54,55,56,57: options (optional)
        # 58+: data

        # ord(data[47]):
        #    2 para pedido de abertura de conexao
        #    18 para resposta da abertura de conexao
        #    24 quando identifica o protocolo

        data_string = data[54:]

        '''
        @episode Tries to determine the layer 7 protocol
        '''
        packet_type = self.getPacketType(src_ip,src_port,dst_ip,dst_port,data_string)
        
        '''
        @episode Log the Connection
        '''
        #if packet_type[0] != "UNKNOWN":
        if not self.connections.__contains__("%s;%s;%s;%s;%s" % (src_ip,src_port,dst_ip,dst_port,",".join(packet_type))): 
        #and not self.connections.__contains__("%s;%s;%s;%s;%s" % (dst_ip,dst_port,src_ip,src_port,",".join(packet_type))):
        # the same connection can handle different urls.
        
            self.connections.append("%s;%s;%s;%s;%s" % (src_ip,src_port,dst_ip,dst_port,",".join(packet_type)))
            self.connections_types.append(packet_type[0])
            self.newAlert(src_ip, dst_ip, src_port, dst_port, packet_type)
        
        
        #print "%s:%d -> %s:%d" % (src_ip,src_port,dst_ip,dst_port)
        #print data_string
        
        
        #if ord(data[47]) == 2 or ord(data[47]) == 18:
        #    print data_string
            
            #print ('%.2x' % ord(data[47]))


        return True
        
        hexout = ""
        for byte in data:
            hexout += '%.2x ' % ord(byte)
            
        print hexout+"\n"
        
        
        

    def packetHandler(self, hdr, data):
        self.checkPacket(data)

    def getPacketType(self,src_ip,src_port,dst_ip,dst_port,data_string):
        """Gets returns the packet type and some parameters, based on type.
        @return: tuple with the type and adicional parameters (variable size)
        
        
        @title Tries to determine the layer 7 protocol
        @goal 
        @context
        @actor Sensor
        @resource Network Packet
        @episode Compare the packet with regular expressions
        
        """
        
        
        """
        HTTP 
            Packet begins with:
                GET / HTTP/1.1
                Host: www.google.com.br
        """
        if dst_port == 80: 
            expr = re.compile(".*(GET ([\x09-\x0d -~]*) HTTP/(0\.9|1\.0|1\.1)).*",re.I|re.S|re.M)
        
            #expr = re.compile(".*(http/(0\.9|1\.0|1\.1) [1-5][0-9][0-9] [\x09-\x0d -~]*(connection:|content-type:|content-length:|date:)|post [\x09-\x0d -~]* http/[01]\.[019]).*",re.I|re.S|re.M)
            #expr_http = re.compile(".*(html).*",re.I|re.S|re.M)
            match = expr.match(data_string)
            if match:
                url = match.group(2).strip()
                http_host = ""
                # jah tenho a URL, pegando agora o host
                expr = re.compile(".*Host: ([a-zA-Z0-9\-\._]+).*",re.I|re.S|re.M)
                match = expr.match(data_string)
                if match:
                    http_host = match.group(1).strip()
                else:
                    http_host = dst_ip
                    
                uri = "http://"+http_host+url    
                
                return ["HTTP",http_host,uri]
        
        """
        TELNET
        """
        expr = re.compile(".*(\xff[\xfb-\xfe].\xff[\xfb-\xfe].\xff[\xfb-\xfe]).*",re.I|re.S|re.M)
        match = expr.match(data_string)
        if match:
            return ["TELNET"]
        
        """
        MSN
            eh possivel pegar tambem o login do msn
            *ainda nao testado*
        """
        expr = re.compile(".*(ver [0-9]+ msnp[1-9][0-9]? [\x09-\x0d -~]*cvr0\x0d\x0a$|usr 1 [!-~]+ [0-9. ]+\x0d\x0a$|ans 1 [!-~]+ [0-9. ]+\x0d\x0a).*",re.I|re.S|re.M)
        match = expr.match(data_string)
        if match:
            return ["MSN"]        
        
        return ["UNKNOWN"]
        
    def newAlert(self,src_ip,dst_ip,src_port,dst_port,service):
        '''Sends to Agent a NEW command. 
        Agent will log this connection and block if a rule is matched.
        
        @title Log the Connection
        @goal Records the connection found in database and block if a rule is matched
        @context The layer 7 protocol is identified
        @resource Network Packet Header, Agent
        @actor Sensor
        @episode Send to Agent a UDP datagram, containing the Network Packet Header.
        @exception Agent is Off: Connect and try again.
        '''
        
        
        print "New Connection Found!"
        print "  Source: %s:%s" % (src_ip,src_port)
        print "  Destination: %s:%s" % (dst_ip,dst_port)
        print "  Service: %s" % service[0]
        if len(service) > 1:
            print "  Params: %s" % ",".join(service[1:])
        print
        
        seq = [src_ip,str(src_port),dst_ip,str(dst_port)]
        seq+=service
        
        seq_str = ','.join(seq)
        
        try:
            self.agent.send("NEW("+seq_str+")")
        except socket.error:
            ## reconnect...
            self.agent = self.sensor.connectAgent()
            ## call me again...
            self.newAlert(src_ip, dst_ip, src_port, dst_port, service)
            