

import re
import xmpp

class Parser:
    
    def __init__(self,messengerObj):
        self.messengerObj = messengerObj
        pass
    
    def createMessage(self,alert):
        rule_id = alert[0]
        src_ip = str(alert[1]).strip()
        src_name = str(alert[2]).strip()
        rule_name = str(alert[3]).strip()
        
        if src_name != "":
            msg = "[%s] was detected with [%s (%s)]" % (rule_name,src_name,src_ip)
        else:
            msg = "[%s] was detected with [%s]" % (rule_name,src_ip)
        
        self.messengerObj.cl.send(xmpp.protocol.Message(self.messengerObj.admin,msg))
    
    
    def parse(self,msg):
        expr = re.compile("^ALERT\((.+)\)$",re.I|re.S)
        match = expr.match(msg)
        if match:
            data = match.group(1).strip()
            alert = data.split(",")
            if len(alert) < 4:
                return "Invalid Arguments"
            
            msg = self.createMessage(alert)
            
            return "OK"
            