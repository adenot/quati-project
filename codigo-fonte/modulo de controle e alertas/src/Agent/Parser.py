
import re

from Common.Functions import *
from Common.Database import Database

from Rules import Rules

class Parser:
    
    def __init__(self):
        self.database = Database()
        self.rules = Rules(self.database)
        #self.messenger = Messenger()
        
    
    def parse(self,msgqueue,command):
        #print "Command received: "+command
        
        '''
        rules:
            if a connection is matched, should be blocked.
            if a connection is not matched, just log is.
            if a connection is matched as an alert, the messenger thread must be alerted
        
        problem: we have to alert the messenger somehow.
        solution: alert all the threads and the messenger thread will hold the message to themself
        
        '''
        
        ## EDIT RULE
        
        # RULE(id,description,source_object,source_port,destination_ip,destination_port,service,parameters,enabled,alert)
        expr = re.compile("^RULE\((.+)\)$",re.I|re.S)
        match = expr.match(command)
        if match:
            data = match.group(1).strip()
            rule = data.split(",")
            if len(rule) < 10 and rule[1] != "delete":
                return "Invalid Arguments"
            if self.rules.editRule(rule) == True:
                self.rules.loadRules()
                return "OK"
            else:
                return "FAIL"

        # OBJECT(id,name,value)
        expr = re.compile("^OBJECT\((.+)\)$",re.I|re.S)
        match = expr.match(command)
        if match:
            data = match.group(1).strip()
            rule = data.split(",")
            if len(rule) < 3 and rule[1] != "delete":
                return "Invalid Arguments"
            if self.rules.editObject(rule) == True:
                self.rules.loadRules()
                return "OK"
            else:
                return "FAIL"     
        
        ## NEW CONNECTION
        expr = re.compile("^NEW\((.+)\)$",re.I|re.S)
        match = expr.match(command)
        if match:
            data = match.group(1).strip()
            connection = data.split(",")
            if len(connection) < 5:
                return "Invalid Arguments"
            self.rules.logConnection(connection)
            
            
            alert_desc = []
            ret = self.rules.createRuleIfMatch(connection,alert_desc)
            
            if ret == 0:
                ## did not match any rule or alert
                pass
            elif ret == 1:
                ## rule was created!
                pass
            elif ret == 2:
                ## alert match, tell messenger
                msgqueue.put("messenger: ALERT("+','.join(alert_desc)+")")
        
            return "OK"
    

        return "OK"
        

    

        