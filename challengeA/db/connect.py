#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 22:06:31 2021

@author: shahil
"""

import mysql.connector
from mysql.connector import errorcode

class db:
    
    def __init__(self, host, user, passw):
        self.host = host
        self.user = user
        self.password = passw

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                db = "kafe_rocks"
                )
            
            self.cur = self.db.cursor()    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                # raise Exception
                print("Incorrect username or password")
            else:
                print(err)
        
    def close(self):
        self.cur.close()
        self.db.close()
    

    def executestatement(self, query, values):
        try: 
            self.cur.execute(query, values)
            self.db.commit()
            return
        except mysql.connector.Error as e:
            return e

    def getall(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def getone(self, query):
        self.cur.execute(query)
        row = self.cur.fetchone()
        while row:
            yield row
            self.cur.fetchone()
            