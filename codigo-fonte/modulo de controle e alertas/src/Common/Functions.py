import os,re

def quotes(text):
    '''@return: text between quotes
    '''
    return '"'+text+'"'



def getIPs():
    '''@return: List with all IP address of the running system
    '''
 
    ipconf = os.popen("ifconfig").read()

    # print [x.strip() for x in ipconf.split("\n")]
    tIPs = re.findall("\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}",ipconf)
    IPs = []
    for ip in tIPs:
        if ip.split(".")[0] == "127" : continue # lo
        if ip.split(".")[0] == "255" : continue # mask
        if ip.split(".")[3] == "255" : continue # bcast
        IPs.append(ip)
        
    return IPs