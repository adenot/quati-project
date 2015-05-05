
from Firewall import Firewall


from Common.Functions import *

import re
from time import time

class Rules:
    
    def __init__(self,databaseObj):
        self.database = databaseObj
        
        self.firewall = Firewall()
        
        self.loadRules()

    def loadRules(self):
        '''
        load all rules in memory to fasten rule comparing!
        '''
        
        self.rules = []
        
        res = self.database.select(sql='''
            SELECT rules.id,description,src.value,src.name,source_port,destination_ip,destination_port,service,parameters,alert
            FROM rules 
            LEFT JOIN objects as src ON src.id = rules.source_object 
            WHERE enabled = 1
            ORDER BY rules.id DESC
            ''')
        
        self.rules = res.fetchall()
        
        
        self.objects = {}
        res = self.database.select(sql='''
            SELECT name,value
            FROM objects
            ''')
        objs = res.fetchall()
        
        for obj in objs:
            self.objects[obj[1]]=obj[0]
        
        print self.objects
        
        print self.rules
        ## [(1, u'youtubey!', u'10.211.55.3', u'spike', 0, None, None, 80, u'HTTP', u'www.youtube.com', 1)]


    def editObject(self,rule):
        id = rule[0]
        name = rule[1]
        
        if name.strip() == "delete":
            return self.database.delete("objects",id)
        
        value = rule[2]
        
        if id == "0":
            #insert
            insert_data = ("null",quotes(name),quotes(value))
            id = self.database.insert("objects",insert_data)
            if id == 0:
                return False
            else:
                return True
        else:
            data = {
                    "name":quotes(name),
                    "value":quotes(value)
                    }
            ret = self.database.update("objects",id,data)
            return ret
        
        
    def editRule(self,rule):
        id = rule[0]
        desc = rule[1]
        
        if desc.strip() == "delete":
            return self.database.delete("rules",id)
        
        src_obj = rule[2]
        src_port = rule[3]
        dst_ip = rule[4]
        dst_port = rule[5]
        service = rule[6]
        parameters = rule[7]
        enabled = rule[8]
        alert = rule[9]
        
        if id == "0":
            #insert
            insert_data = ("null",quotes(desc),src_obj,src_port,quotes(dst_ip),dst_port,quotes(service),quotes(parameters),enabled,alert)
            id = self.database.insert("rules",insert_data)
            if id == 0:
                ret = False
            else:
                ret = True
        else:
            data = {
                    "description":quotes(desc),
                    "source_object":src_obj,
                    "source_port":src_port,
                    "destination_ip":quotes(dst_ip),
                    "destination_port":dst_port,
                    "service":quotes(service),
                    "parameters":quotes(parameters),
                    "enabled":enabled,
                    "alert":alert
                    }
            ret = self.database.update("rules",id,data)

        self.loadRules()
        
        return ret


        
    def removeRule(self):
        pass
    
    def enableRule(self,id):
        pass
    
    def disableRule(self,index):
        pass
    
    def createRuleIfMatch(self,connection,alert_desc=[]):
        '''
        This method searches in the rules list for ones that match the new connection probed.
        If found, tells the firewall to create a rule.
        As requisite, this operation must be very fast.
        '''
        
        #print connection
        ## ['10.211.55.3', '1216', '208.65.153.238', '80', 'HTTP', 'www.youtube.com', 'http://www.youtube.com/']

        src_id = 0
        src_ip = str(connection[0]).strip()
        src_port = connection[1]
        dst_id = 0
        dst_ip = str(connection[2]).strip()
        dst_port = connection[3]
        service = connection[4].strip()
        if len(connection) <= 5:
            parameters = ["",""]
        else:
            parameters = connection[5:]

        for rule in self.rules:
            rule_id = rule[0]
            rule_name = str(rule[1]).strip()
            rule_src_ip = str(rule[2]).strip()
            rule_src_name = str(rule[3]).strip()
            rule_src_port = rule[4]
            rule_dst_ip = str(rule[5]).strip()
            ##rule_dst_name = rule[6]
            rule_dst_port = rule[6]
            rule_service = str(rule[7]).strip()
            rule_params = str(rule[8]).strip()
            rule_alert = int(rule[9])
            
            #   0  1             2               3         4  5     6   7        8                   9
            # [(1, u'youtubey!', u'10.211.55.3', u'spike', 0, None, 80, u'HTTP', u'www.youtube.com', 1)]


            if rule_src_ip != "" and rule_src_ip != "None" and rule_src_ip != src_ip:
                print "saiu1 %s %s" % (str(rule_src_ip),str(src_ip))
                continue
                
            if rule_dst_ip != "" and rule_dst_ip != "None" and rule_dst_ip != dst_ip:
                print "saiu2 %s %s" % (str(rule_dst_ip),str(dst_ip))
                continue
            
            if rule_src_port is not 0 and int(rule_src_port) is not int(src_port):
                print "saiu3 %d %d" % (int(rule_src_port),int(src_port))
                continue
            
            if rule_dst_port is not 0 and int(rule_dst_port) is not int(dst_port):
                print "saiu4 %d %d" % (int(rule_dst_port),int(dst_port))
                continue
            
            # if we get here, means the connection if match, lets check the param if there is any.

            if rule_service != service:
                print "saiu5 %s %s" % (rule_service,service)
                continue
            
            #print parameters
            print "### Comparando %s in %s" % (rule_params,parameters[1])
            
            
            if service == "HTTP":
                if parameters != "" and not rule_params in parameters[1]:
                    continue
            
            if rule_alert == 0 or rule_alert == 2:
                #match!
                print "#######################################"
                print "Rule Match ! (%s)" % rule_name
                print "#######################################"
                self.firewall.createRule(src_ip,src_port,dst_ip,dst_port,service)
                
                return 1
                
            if rule_alert == 1 or rule_alert == 2:
                print "#######################################"
                print "Alert Match ! (%s)" % rule_name
                print "#######################################"
                
                if self.objects.has_key(src_ip):
                    src_name = self.objects[src_ip]
                else:
                    src_name = ""
                
                alert_desc.append(str(rule_id))
                alert_desc.append(src_ip)
                alert_desc.append(src_name)
                alert_desc.append(rule_name)
                return 2
                
            
            
        
        return 0
        
    
    def createRuleIfMatchSQL(self,connection):
        '''
        NOT USED!
        
        This method searches in database for rules that match the new connection probed.
        If found, tells the firewall to create a rule.
        As requisite, this operation must be very fast.
        '''
        src_id = 0
        src_ip = connection[0]
        src_port = connection[1]
        dst_id = 0
        dst_ip = connection[2]
        dst_port = connection[3]
        service = connection[4]
        if len(connection) < 6:
            connection[5]="null"
        parameters = connection[5:]
        
        sql_param = []
        
        if service == "HTTP":
            sql_param.append("parameters LIKE '%"+parameters[1]+"%'")
        
        sql='''
            SELECT description,src.value,source_port,dst.value,destination_port 
            FROM rules 
            LEFT JOIN objects as src ON src.id = rules.source_object 
            LEFT JOIN objects as dst ON dst.id = rules.destination_object 
            WHERE enabled = 1 
            AND (src.value = "'''+src_ip+'''" OR source_object = 0) 
            AND (source_port = '''+src_port+''' OR source_port = 0)
            AND (dst.value = "'''+dst_ip+'''" OR destination_object = 0)
            AND (destination_port = '''+dst_port+''' OR destination_port = 0)
            AND ('''+' OR '.join(sql_param)+''')
            ORDER BY rules.id DESC
            '''
        
        '''
        @todo: temos uma url completa e precisamos buscar por partes dela no banco.. como fazer? 
        podemos carregar para array, mas ai a comparacao de mascara vai ficar lenta (mais q o sqlite?)
        '''
        
        res = self.database.select(sql=sql)
        
        print sql
        
        
        rule = []
        for item in res:
            rule = item
            break
        
        if len(rule) == 0:
            return
        
        self.firewall.createRule(src_ip,src_port,dst_ip,dst_port)
        

    def logConnection(self,connection):
        
        src_id = 0
        src_ip = connection[0]
        src_port = connection[1]
        dst_id = 0
        dst_ip = connection[2]
        dst_port = connection[3]
        service = connection[4]
        #parameters = quotes(','.join(connection[5:]))
        
        if len(connection) <= 5:
            parameters=""
        else:
            parameters = connection[5:]
        
        
        '''
        res = self.database.select(sql="SELECT * FROM objects WHERE value = "+quotes(src_ip)+" or value = "+quotes(dst_ip))
        
        for item in res:
            tmp_id = item[0]
            tmp_name = item[1]
            tmp_value = item[2]
            if tmp_value == src_ip:
                src_id = tmp_id
            elif tmp_value == dst_ip:
                dst_id = tmp_id
            
        if src_id is 0:
            src_id = self.database.insert("objects",["null",quotes(src_ip),quotes(src_ip)])
        if dst_id is 0:
            dst_id = self.database.insert("objects",["null",quotes(parameters[0]),quotes(dst_ip)])
        '''
        
    
        
        # src_ip,src_port,dst_ip,dst_port,service,parameters
        insert_data = ["null",str(time()),quotes(src_ip),src_port,quotes(dst_ip),dst_port,quotes(service),quotes(','.join(parameters))]
        
        self.database.insert("logs",insert_data)
        
        