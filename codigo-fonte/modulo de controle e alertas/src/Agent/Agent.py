import sys
from socket import *
from Queue import Queue,Empty

from Common.Config import Config
from Common.Daemon import Daemon
from Common.Database import Database


from Parser import Parser

"""
Messenger and Sensor module will stay connected to me, in order to exchange commands

if both modules are connected to me, constantly, agent can monitor the other daemons,
invoking them if they aren't connected to me.

@todo: the database connection, logging the network activity and the user-ip table.
@todo: create a protocol to communicate with the other daemons
@todo: block a site on request (by IP). if the site is open again, block the other site IP.
        (forward to a Error page? a webserver must be open)
@todo: if the ip has multiple sites? i can block individually, example:
        user Montenegro wants to access www.google.com that is blocked
        a rule with source ip, source port, destination ip, destination port is created, blocking that connection
        if another user try to access other site in the same ip, the rule wont apply to him
        problem: is the rule fast enough to redirect user to the error page? or only on reload user will see the error page? (is this a problem?)

@episodes
@title Initialize Agent
@title Open Quati configuration
@title Handle messages

"""

class SimpleServer:
    #
    # This means the main server will not do the equivalent of a
    # pthread_join() on the new threads.  With this set, Ctrl-C will
    # kill the server reliably.
    daemon_threads = False

    # By setting this we allow the server to re-bind to the address by
    # setting SO_REUSEADDR, meaning you don't have to wait for
    # timeouts when you kill the server and the sockets don't get
    # closed down correctly.
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        handler = RequestHandlerClass()
        handler.handle()

class Agent(Daemon):

    def run(self):
        
        self.config = Config()
        
        bind_host = self.config.conf['agent']['host']
        bind_port = int(self.config.conf['agent']['port'])

        print 'Starting the server...'
        s = socket(AF_INET,SOCK_DGRAM)
        s.bind((bind_host,bind_port))
        
        handler = AgentHandler(s)
        handler.handle()
        
class msgQueue:
    
    def __init__(self):
        self.msgqueue = ''
    
    def put(self,msgqueue):
        self.msgqueue = msgqueue
    def get(self):
        return self.msgqueue
    def clean(self):
        self.msgqueue = '' 
    
        
class AgentHandler:
    '''Class to handle sending a greeting to a client
    '''
    
    def __init__(self,socket):
        self.parser = Parser()
        self.socket = socket

    def handle(self):

        clients = {}
        text = ''
        line = ''
        done = False
        msg = ''
        msgqueue = msgQueue()
        while not done:
            #print client_name+"..."

                               
            data,addr = self.socket.recvfrom(1024)
            if len(data) > 0:
                text += str(data)
                while text.find("\n") != -1:
                    
                    line, text = text.split("\n", 1)
                    line = line.strip()
                    
                    print "Agent: < "+line

                    ## Get client name
                    client_name = ''
                    for name in clients:
                        addr_tmp = clients[name]
                        if addr_tmp[1] != addr[1]:
                            continue
                        client_name = name

                    ## if there's a message to my client, send now
                    msgqueue_tmp = msgqueue.get()
                    if msgqueue_tmp != '':
                        if msgqueue_tmp.startswith(client_name+": "):
                            print "Sending to client "+client_name+" this: "+msgqueue_tmp[len(client_name)+2:]
                            self.socket.sendto(msgqueue_tmp[len(client_name)+2:]+"\n",addr)
                            msgqueue.clean()
                            continue

                    
                    ## Set client name
                    if line.startswith("NAME"):
                        client_name = line[5:]
                        #possible names: sensor|messenger
                        
                        self.socket.sendto("Hello %s\n" % client_name,addr)
                        clients[client_name] = addr
                        #print clients
                    
                    ## Parse other messages
                    else:
                        ret = str(self.parser.parse(msgqueue,line))+"\n"
                        print "Agent > ("+addr[0]+":"+str(addr[1])+") "+ret
                        self.socket.sendto(ret,addr)
            

                            
                            
            
        self.socket.close()
    

if __name__ == "__main__":
    
    daemon = Agent('/tmp/q_agent.pid',stdout="/dev/pts/0",stderr="/dev/pts/0")
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        
        sys.exit(0)
    
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
    