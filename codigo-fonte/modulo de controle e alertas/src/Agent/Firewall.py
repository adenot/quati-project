
import os
#from Common.scapy import *

class Firewall:
    
    def __init__(self):
        pass
    
        os.system("iptables -F QUATIBLOCK")
        os.system("iptables -N QUATIBLOCK")
        os.system("iptables -D FORWARD -p tcp --dport 80 -j QUATIBLOCK")
        os.system("iptables -I FORWARD -p tcp --dport 80 -j QUATIBLOCK")
        
        os.system("iptables -t nat -F QUATIBLOCK")
        os.system("iptables -t nat -N QUATIBLOCK")
        os.system("iptables -t nat -D PREROUTING -j QUATIBLOCK");
        os.system("iptables -t nat -I PREROUTING -j QUATIBLOCK");
        #os.system("iptables -A HTTPBLOCK -m recent --set --name HTTPBLOCK")
        
    def createRule(self,src_ip,src_port,dst_ip,dst_port,service,params=""):
        '''
        The response time in tests concluded that aprox. 2kb of the first connection is downloaded before the rule is created.
        @todo: redirect to a localhost webserver and see if user get redirected and a error message. 
        '''
        
        
        #os.system("iptables -A HTTPBLOCK -d %s -m recent --update  --seconds 60 --hitcount 1 --name HTTPBLOCK -j REJECT" % dst_ip)
    
        
        #load = 'HTTP/1.1 302 Found\r\nLocation: http://www.uol.com.br\r\nCache-Control: private\r\nContent-Type: text/html; charset=UTF-8\r\nSet-Cookie: SS=Q0=L3dlYmhwP3Jscz1pZw; path=/search\r\nDate: Sat, 06 Sep 2008 20:58:51 GMT\r\nServer: gws\r\nContent-Length: 231\r\n\r\n<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">\n<TITLE>302 Moved</TITLE></HEAD><BODY>\n<H1>302 Moved</H1>\nThe document has moved\n<A HREF="http://www.google.com/webhp?rls=ig">here</A>.\r\n</BODY></HTML>\r\n'
        #p=IP(src=dst_ip,dst=src_ip)/TCP(sport=int(dst_port),dport=int(src_port))/load
        #send(p,0,0,1)
        
        # just in debug mode. the above rule cant block self made connections
        #os.system("iptables -I OUTPUT -s %s -d %s -p tcp --sport %s --dport %s -j DROP" % (src_ip,dst_ip,src_port,dst_port))
        
        #os.system("iptables -t raw -I PREROUTING -s %s -d %s -p tcp --sport %s --dport %s -j NOTRACK" %  (src_ip,dst_ip,src_port,dst_port))
        
        #os.system("iptables -t nat -I PREROUTING -s %s -d %s -p tcp --sport %s --dport %s -j DNAT --to-destination 192.168.1.54:80" %  (src_ip,dst_ip,src_port,dst_port))
        
        if service == "HTTP":
            # redirects to a local server in order to show the Access Denied page
            os.system("iptables -t nat -I QUATIBLOCK -s %s -d %s -p tcp --dport %s -j REDIRECT --to-ports 80" %  (src_ip,dst_ip,dst_port))
        
        # Sends a RST to both ends, so the connection is dropped and when the browser starts a new one, he is redirected to the access denied. 
        os.system("cutter %s %s %s" % (dst_ip,dst_port,src_ip))
        
        #os.system("iptables -I QUATIBLOCK -s %s -d %s -p tcp --dport %s -j REJECT" % (src_ip,dst_ip,dst_port))
        