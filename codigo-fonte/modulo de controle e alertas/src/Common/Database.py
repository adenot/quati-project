
from pysqlite2 import dbapi2 as sqlite

from Common.Functions import *

'''
@package Common
@namespace Database

Database layer class. Abtracts the database access.
'''
class Database:
    
    def __init__(self):
        self.connection = sqlite.connect('quati.db')
        self.cursor = self.connection.cursor()
    
    def select(self,table="",condition="",sql="",params=()):
        '''Automates a select to the Quati database        
        '''
        if sql == "":
            sql = "SELECT * FROM "+table
            if condition is not "":
                sql += " WHERE "+condition
        
        #print sql
        
        try:
            self.cursor.execute(sql,params)
        except sqlite.Error, e:
            print "An error occurred: ", e.args[0]
            return None

        return self.cursor
    
    def delete(self,table,id):
        '''Automates the removal of a database tuple
        '''
        id = int(id)
        
        sql = "DELETE FROM "+table+" WHERE id="+str(id)
        
        try: 
            self.cursor.execute(sql)
        except sqlite.Error, e:
            print "An error ocurred: ", e.args[0]
            return False
    
        self.connection.commit()
        
        return True
        
            
    def update(self,table,id,data):
        '''Automates a tuple update
        '''
        if type(id) == type(""): 
            id = str(int(id))
        else:
            id = str(id)
            
        values = []
        for key, value in data.iteritems():    
            if type(value) == type(""):
                values.append(key+"="+value)
            else:
                values.append(key+"="+str(value))
            
        values_str = ",".join(values) 
        
        sql = "UPDATE "+table+" SET "+values_str+" WHERE id="+id
    
        try: 
            self.cursor.execute(sql)
        except sqlite.Error, e:
            print "An error ocurred: ", e.args[0]
            return False
    
        self.connection.commit()
        
        return True
    
    def insert(self,table,data):
        '''Automates database inserction
        @return: id of the new row
        '''
        data_str = []
        for item in data:
            data_str.append(str(item))
        
        sql = "INSERT INTO "+table+" VALUES ("+', '.join(data_str)+")"
        
        #print sql
        
        try:
            self.cursor.execute(sql)
        except sqlite.Error, e:
            print "An error occurred: ", e.args[0]
            return 0

        self.connection.commit()

        return self.cursor.lastrowid