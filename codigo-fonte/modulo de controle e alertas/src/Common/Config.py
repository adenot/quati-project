
try: 
    from elementtree.ElementTree import ElementTree as ET
    from elementtree.ElementTree import Element as E
except ImportError:
    try:
        from xml.etree.ElementTree import ElementTree as ET
        from xml.etree.ElementTree import Element as E
    except ImportError:
        print "ElementTree not installed!"
  
"""
@package Common
@namespace Config

Class Config, load configuration from config.xml file into a dictionary (self.conf)
"""      
class Config:
    """
    
    """
    def __init__(self):
        #root = ElementTree(file="sfa.xml").getroot()
        root = ET(file="config.xml").getroot()
        self.conf = {}
        self.conf = self.parse(root,self.conf)
    
    def printconf(self):
        print self.conf
        
    def parse (self,root,conf):
        conf = {}
        for element in list(root):
            #if element.
            if element.text.strip() == "":
                #print "entrando em %s" % element.tag
                conf[element.tag] = self.parse(element,conf)
            else:
                #print "tag: %s / valor: %s" % (element.tag,element.text.strip())
                conf[element.tag]=element.text.strip()
        
        return conf
        
        #node_passport_user = node_passport.
            
if __name__ == '__main__':
    Config()