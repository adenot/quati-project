import socket

'''
@package Common
@namespace Socket

Class Socket, abstracts the socket connection and message exchange
'''
class Socket:    
    def __init__(self,host,port):
        self.addr = (host,port)

        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            #self.sock.connect(self.addr)
        except socket.error, msg:
            raise socket.error

        ## this will raise a error if the UDP por isnt open
        self.send("ACK")
        
    def send(self,command):
        '''Sends a command to the connected socket
        @return: empty string if a OK is reveived
        @raise socket.error: if the connection is lost
        '''

        try:
            self.sock.sendto(command+"\n",self.addr)
        except socket.error, msg:
            print "Socket error!"
            raise socket.error
        
        #return True
        #self.sock.setblocking(0)
        data = self.sock.recv(1024)
        
        if data.strip() == "OK":
            return ""
        
        return str(data).strip()

            
    def receive(self,nonblocking=True):
        '''Receive data from server
        @return: Data received
        '''
        
        ## now with non-blocking !
        '''
        if nonblocking == True:
            self.sock.settimeout(1)
            pass    
        '''
        if nonblocking == True:
            self.sock.setblocking(0);
                    
        
        data = self.sock.recv(1024)
        string = ""
        while len(data):
            string = string + data
            data = self.sock.recv(1024)
            string += str(data)
        
        return string.strip()
        