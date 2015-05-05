
import xmpp

import sys,time
import select
import socket
import traceback


from Common.Config import Config
from Common.Daemon import Daemon
from Common.Socket import Socket

from Parser import Parser

class MessengerDaemon(Daemon):
    def run(self):
        Messenger()

class Messenger:
    def __init__(self):
        
        self.alertQueue = []
        
        self.chatObj = None
        
        self.parser = Parser(self)
        
        self.config = Config()
        
        self.m_server = self.config.conf['messenger']['login']['server']
        self.m_port = self.config.conf['messenger']['login']['port']
        self.m_user = self.config.conf['messenger']['login']['user']
        self.m_pass = self.config.conf['messenger']['login']['pass']
        self.admin = self.config.conf['messenger']['administrator']
        self.admin_ack = False

        self.agent = False
        while not self.agent:
            try:
                self.agent = Socket("localhost",26)
            except socket.error:
                self.agent = False
                print "Cannot connect to Agent, trying again in five..."
                time.sleep(5)

        self.agent.send("NAME messenger")

        print 'Starting Messenger...'
        
        while 1:
            try:
                self.connectIM()
                self.listenIM()
            except:
                print "Connection dropped, trying again in five"
                traceback.print_exc()
                time.sleep(5)
        

    def cbMessage(self, con, event):
        text = event.getBody()
        fromuser = event.getFrom().getStripped()

        error = event.getTagData('error')
        
        #print '#####Error is %s' % error

        if fromuser != self.admin:
            self.cl.send(xmpp.protocol.Message(self.admin,"Someone is trying to contact me! "+fromuser))
            self.cl.send(xmpp.protocol.Message(fromuser,"I'm not supposed to talk with strangers!"))
            return
        
        '''
        Cant deliver (user offline):
        <message to="quati.project@gmail.com/4BFD0FA2" id="58" from="adenot@gmail.com" type="error">
          <body>Hello Master</body>
          <nos:x value="disabled" xmlns:nos="google:nosave"/>
          <arc:record otr="false" xmlns:arc="http://jabber.org/protocol/archive"/>
          <error code="503" type="cancel">
          <service-unavailable xmlns="urn:ietf:params:xml:ns:xmpp-stanzas"/>
          </error>
        </message>
        '''
        
        
        id=self.cl.send(xmpp.protocol.Message(self.admin,text))
            
    def cbPresence(self, conn, event):
        """ Handles incoming presence from other users. """
        user = event.getFrom()
        type = event.getType()
        show = event.getShow()
        status = event.getStatus()
        
        if user.getStripped() == self.admin and self.admin_ack == False and type != "unavailable":
            '''Greets the administrator'''
            self.cl.send(xmpp.protocol.Message(self.admin,"Hello Master"))
            self.admin_ack = True
        elif user.getStripped() != self.admin and not user.getStripped().startswith(self.m_user):
            '''If he is not the admin and isnt me, unsubscribe him'''
            self.cl.getRoster().Unauthorize(user)
            self.cl.getRoster().Unsubscribe(user)
            print "Unsubscribing unknown user %s" % user.getStripped()

        return

        print "Presence from User: " + user.getStripped() + "/" + user.getResource()
        print "Type %s" % (type)
        print "Show %s" % (show)
        print "Status %s" % (status)

        '''
        # status = online
        if type is None and show is None:
            # status = online
#            print "Online"
            self.api.addStatus(user, 'online', status)

        # status = * (away, xa, unavailable)
        elif type is None and show is not None:
            # status = * (away, xa, unavailable)
#            print "Online & %s" % (show)
            self.api.addStatus(user, show, status)

        # status = offline
        elif type == "unavailable":
            # status = offline
#            print "Offline"
            self.api.addStatus(user, 'offline', status)

        # subscription request
        elif type == "subscribe":
            self.roster.Authorize(user)
            self.roster.Subscribe(user)
#            print "Subscribing to %s" % (user.getStripped())
            """ stuff """

        # subscribed to user
        elif type == "subscribed":
            # add to roster
#            print "Subscribed to %s" % (user.getStripped())
            """ stuff """

        # unsubscribe request
        elif type == "unsubscribe":
            self.roster.Unauthorize(user)
            self.roster.Unsubscribe(user)
#            print "Unsubscribing from %s" % (user.getStripped())

        # unsubscribed to user
        elif type == "unsubscribed":
            # remove from roster
#            print "Unsubscribed from %s" % (user.getStripped())
        '''
    
    def listenIM(self):
        times=0
        
        while 1:
            self.cl.Process(1)
            
            print "."
            msg = self.agent.send("ACK")
            
            ''' @todo: we need to parse too!
            '''
            if msg != "":
                #self.cl.send(xmpp.protocol.Message(self.admin,msg))
                self.parser.parse(msg)

            time.sleep(1)


    def connectIM(self):
        self.cl = xmpp.Client('gmail.com',debug=[])
        self.cl.connect( server=(self.m_server,int(self.m_port)) )

        self.cl.auth(self.m_user, self.m_pass)
        self.cl.sendInitPresence()
        
        self.cl.RegisterHandler('message',self.cbMessage)
        self.cl.RegisterHandler('presence',self.cbPresence)
        
        #id=self.cl.send(xmpp.protocol.Message("adenot@gmail.com","Hello Master"))

        self.cl.getRoster().Authorize(self.admin)
        self.cl.getRoster().Subscribe(self.admin)
        

        
        print "Messenger: Login successful"



    def alertAdministrator(self,connection):
        src_ip = connection[0]
        src_port = connection[1]
        dst_ip = connection[2]
        dst_port = connection[3]
        service = connection[4]
        if len(connection) < 6:
            connection[5]="null"
        parameters = connection[5:]
        
        msg = "Shall I drop this connection?"
        msg += "%s:%s <-> %s:%s" % (src_ip,src_port,dst_ip,dst_port)
        if len(parameters) > 1:
            msg += "%s" % parameters
        
    
    def sendMessage(self,message):
        pass
        
    def addAlertQueue(self,question,action):
        pass
    
    def removeAlertQueue(self,question):
        pass
    
    def executeAction(self,action):
        pass
    
    def getResponse(self,response):
        pass


if __name__ == "__main__":
    
    daemon = MessengerDaemon('/tmp/q_messenger.pid',stdout="/dev/pts/0",stderr="/dev/pts/0")
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
    