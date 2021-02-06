#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:42:53 2021

@author: shahil
"""

from db.connect import db
from metroretro.metroretro import metroretro
import pandas as pd
import io

metroboard_username = "bhikha234@gmail.com"
metroboard_password = "JDetDlv&3&Lawg!x85"
boardName = "Kafe Rock Challenge"
fileFormat = ["csv", "csvx", "json"]
db_host = "localhost"
db_user = "root"
db_password = ""    

def main():
    # Connect to mysql DB
    localDB = db(db_host, db_user, db_password)
    localDB.connect()
    
    # Connect to metroretro client
    client = metroretro(metroboard_username, metroboard_username)
    client.connect()
        
    boards = client.getBoards(boardName)    
    if boards == "":
        return "Board not found"
        
    # Fetch columns
    urlData = client.getBoardData(boards, fileFormat[1])  
    
    # Be explicit about column names
    columns = ["category", "author", "content", "votes", "date", "comments"]
    
    rawData = pd.read_csv(io.StringIO(urlData), names=columns, header=0)
        
    cols = "`,`".join(i for i in columns)
    sql = "INSERT INTO `` (`" +cols + "`) VALUES (%s, %s, %s, %s, %s, %s)"
    
    for i, row in rawData.iterrows():
        update = sql.format(tuple(row))
        localDB.executestatement(update)

if __name__ == '__main__':
    main()


