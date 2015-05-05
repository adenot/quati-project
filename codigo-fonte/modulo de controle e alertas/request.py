
import cgi
import sys,time
sys.path.append('./src/')

from Common.Database import Database
from Common.Socket import Socket

from Agent.Rules import Rules

import Common.simplejson as json

get = cgi.FieldStorage()

#time.sleep(1)

''' 
Task List:
* setRule will receive a list os parameters that must be saved in the database
  agent must receive this parameters in order to update the database.
  
* setObject must do the same as setRule

* setRule and setObject also must be able to create new tuples and delete ones
  if a setRule/Object with id=1 and do=delete is received the tuple must be deleted 


'''


if not get.has_key("action"):
     sys.exit(0)


if get["action"].value == "setRule":

    res = {}
    
    ## RULE(3,teste2,1,0,192.168.1.1,80,HTTP,uol.com,1,1)
    ## _dc=1224953825385&description=teste2&source_object=1&destination_port=80&destination_ip=192.168.1.1&service=HTTP&alert=on
    
    try:
        agent = Socket("localhost",26)
        agent.send("NAME request")
    except:
        agent = False
        

    id = get["id"].value
    
    if not agent:
        error_msg = "Agent is not running"
        ret = "FAIL"
        
    else:
        
        if get.has_key("delete") and get["delete"].value == "1":
            rule = [id,"delete"]
            rule_str = ",".join(rule)
            ret = agent.send("RULE("+rule_str+")")
            
            success_msg = "Rule deleted successfully"
            error_msg = "Error storing the database"
        
        else:
            
            desc = get["description"].value
            
            source_object = "0"
            if get.has_key("source_object"):
                source_object = get["source_object"].value
            
            source_port = "0"
            if get.has_key("source_port"):
                source_port = get["source_port"].value
            
            destination_ip=""
            if get.has_key("destination_ip"):
                destination_ip = get["destination_ip"].value
            
            destination_port = "0"
            if get.has_key("destination_port"):
                destination_port = get["destination_port"].value
            
            service=""
            if get.has_key("service"):
                if get["service"]=="ALL":
                    service = ""
                else:
                    service = get["service"].value
            
            parameters=" " 
            if get.has_key("parameters"):
                parameters = get["parameters"].value
            
            enabled = "0"
            if get.has_key("enabled"):
                enabled = get["enabled"].value
            
            alert = "0"
            if get.has_key("alert"):
                alert = get["alert"].value
        
            rule = [id,desc,source_object,source_port,destination_ip,destination_port,service,parameters,enabled,alert]
            rule_str = ",".join(rule)
        
            ret = agent.send("RULE("+rule_str+")")
            
            success_msg = "Rule saved successfully"
            error_msg = "Error storing the database"


    if str(ret).strip() == "":
        res["success"]=True
        res["message"]=success_msg
    else:
        res["success"]=False
        res["message"]=error_msg
    

    json_res = json.dumps(res)
    
    if get.has_key("callback"):
        json_res = get["callback"].value+"("+json_res+");"
        
    print json_res


if get["action"].value == "setObject":

    res = {}
    
    ## RULE(3,teste2,1,0,192.168.1.1,80,HTTP,uol.com,1,1)
    ## _dc=1224953825385&description=teste2&source_object=1&destination_port=80&destination_ip=192.168.1.1&service=HTTP&alert=on
    
    try:
        agent = Socket("localhost",26)
    except:
        agent = False

    id = get["id"].value
    
    if not agent:
        error_msg = "Agent is not running"
        ret = "FAIL"
        
    else:
        
        if get.has_key("delete") and get["delete"].value == "1":
            rule = [id,"delete"]
            rule_str = ",".join(rule)
            ret = agent.send("OBJECT("+rule_str+")")
            
            success_msg = "Object deleted successfully"
            error_msg = "Error storing the database"
        
        else:
            
            name = get["name"].value
            value = get["value"].value
            
            object = [id,name,value]
            object_str = ",".join(object)
        
            ret = agent.send("OBJECT("+object_str+")")
            
            success_msg = "Object saved successfully"
            error_msg = "Error storing the database"


    if str(ret).strip() == "":
        res["success"]=True
        res["message"]=success_msg
    else:
        res["success"]=False
        res["message"]=error_msg
    

    json_res = json.dumps(res)
    
    if get.has_key("callback"):
        json_res = get["callback"].value+"("+json_res+");"
        
    print json_res

if get["action"].value == "getObjectList":

    db = Database()
    res = db.select(sql="SELECT count(*) as total FROM objects")
    res2 = res.fetchone()
    total = res2[0]
    
    res = db.select(sql="SELECT id,name,value FROM objects" )

    res2 = {"totalCount":total, "objects": []}
    i = 0

    tmp = {}
    tmp["id"]=0
    tmp["name"]="All sources"
    tmp["value"]="0.0.0.0"
    res2["objects"].append(tmp)
    
    for row in res:
        tmp = {}
        tmp["id"]=row[0]
        tmp["name"]=row[1]
        tmp["value"]=row[2]
        
        res2["objects"].append(tmp)
        i=i+1
    
    json_res = json.dumps(res2)
    
    if get.has_key("callback"):
        json_res = get["callback"].value+"("+json_res+");"
        
    print json_res

if get["action"].value == "getRuleList":

    db = Database()
    res = db.select(sql="SELECT count(*) as total FROM rules")
    res2 = res.fetchone()
    total = res2[0]
    
    res = db.select(sql="SELECT id,description,source_object,source_port,destination_ip,destination_port,service,parameters,enabled,alert FROM rules" )

    res2 = {"totalCount":total, "rules": []}
    i = 0
    
    for row in res:
        tmp = {}
        tmp["id"]=row[0]
        tmp["description"]=row[1]
        tmp["source_object"]=row[2]
        tmp["source_port"]=row[3]
        tmp["destination_ip"]=row[4]
        tmp["destination_port"]=row[5]
        tmp["service"]=row[6]
        tmp["parameters"]=row[7]
        tmp["enabled"]=row[8]
        tmp["alert"]=row[9]
        
        res2["rules"].append(tmp)
        i=i+1
    
    json_res = json.dumps(res2)
    
    if get.has_key("callback"):
        json_res = get["callback"].value+"("+json_res+");"
        
    print json_res

if get["action"].value == "getLogList":
    
    if get.has_key("start"):
        start = get["start"].value
    else:
        start = str(0)
    if get.has_key("limit"):
        limit = get["limit"].value
    else:
        limit = str(50)
    if get.has_key("order"):
        order = get["order"].value
    else:
        order = "timestamp ASC"

    ## double check the variables
    start = str(int(start))
    limit = str(int(limit))
    
    ## we need to filter the order variable against injection

    db = Database()
    res = db.select(sql="SELECT count(*) as total FROM logs")
    res2 = res.fetchone()
    total = res2[0]
    
    res = db.select(sql="SELECT id,timestamp,source_ip,source_port,destination_ip,destination_port,service,parameters FROM logs ORDER BY ? LIMIT ?,?", params=(order,start,limit) )
    
    res2 = {"totalCount":total, "logs": []}
    i = 0
    
    for row in res:
        tmp = {}
        
        tmp["id"]=row[0]
        tmp["timestamp"]=row[1]
        tmp["source"]=row[2]+":"+str(row[3])
        tmp["parameters"]=row[7]
        if tmp["parameters"] != "":
            destination_ip = tmp["parameters"].split(",")[0]
            tmp["parameters"] = tmp["parameters"].split(",")[1]
        else:
            destination_ip = row[4]
        tmp["destination"]=destination_ip+":"+str(row[5])
        tmp["service"]=row[6]
        
        
        res2["logs"].append(tmp)
        
        i=i+1
    
    json_res = json.dumps(res2)
    
    if get.has_key("callback"):
        json_res = get["callback"].value+"("+json_res+");"
        
        
    print json_res
        