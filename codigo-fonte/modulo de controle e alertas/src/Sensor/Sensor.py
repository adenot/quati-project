
import sys,time,socket

from Common.Config import Config
from Common.Daemon import Daemon
from Common.Socket import Socket

from Sniffer import Sniffer

import pcapy 
from pcapy import open_live

"""
@package Sensor
@namespace Sensor


@title Initialize Sensor
@goal Starts and daemonize the process to start sniffing the network
@context The system initialization scripts invokes the sensor
@actor System
@episode Open Quati config
@episode Connect to Agent


@title Open Quati config
@goal Read the configuration in an array
@context 
@actor Sensor
@resource quati.xml
@exception File not found, Error reading

@title Connect to Agent
@goal Open a connection with agent
@context
@actor Sensor
@resource Network socket
@exception Socket Error

}


"""

class Sensor(Daemon):
    """This is the main core class, their objective is probe for new connections and alert the interface 

    Details...
    """

    def run(self):
        """Starts the probing
        @param self: The object pointer.
        """

        self.config = Config()
        dev = self.config.conf['sensor']['interface']
        
        self.connectAgent()
        
        p = open_live(dev, 1500, 0, 100)
        p.setfilter("tcp port not 22 and tcp port not 139 and tcp port not 445 and udp port not 138 and udp port not 137")


        Sniffer(p,self.agent,self)
    
    def connectAgent(self):
        self.agent = False
        while not self.agent:
            try:
                self.agent = Socket("localhost",26)
            except socket.error:
                self.agent = False
                print "Cannot connect to Agent, trying again in five..."
                time.sleep(5)
        
        self.agent.send("NAME sensor")

        return self.agent
        
    

if __name__ == "__main__":
    
    daemon = Sensor('/tmp/q_sensor.pid',stdout="/dev/pts/0",stderr="/dev/pts/0")
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