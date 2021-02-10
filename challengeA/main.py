#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:42:53 2021

@author: shahil
"""

from datetime import datetime
from configparser import ConfigParser
from db.connect import db
from metroretro.metroretro import metroretro
import util

fileFormat = ["csv", "csvx", "json"]

def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"{now}: Executing metro retro pipeline now")
    # Read in config file.
    config = ConfigParser()
    config.read("config.ini")
    
    boardName = config.get("metroretro", "board_name")
    
    print("Connecting to DB")
    # Connect to mysql DB.
    localDB = db(config.get("db", "db_host"), 
                 config.get("db", "db_user"), 
                 config.get("db", "db_password"))
    localDB.connect()
    
    print("Connecting to metroretro client")
    # Connect to metroretro client.
    client = metroretro(config.get("metroretro", "metroboard_username"), 
                        config.get("metroretro", "metroboard_password"))
    client.connect()
        
    # Find the metro retro board id.
    board = client.getBoards(boardName)
    if board == "":
        return "Board not found"
    
    print("Fetching board data")
    # Fetch board data.
    urlData = client.getBoardData(board, fileFormat[1])  
    
    # Convert data to dataframe and clean.
    rawData = util.writeToDf(urlData)
    
    print("Writing data to the database")
    # Write dataframe to database.
    util.toDB(localDB, boardName, rawData)
        
    # Close db cursor and connection.
    localDB.close()
    
    print(f"{now}: Completed running metro retro pipeline")

if __name__ == '__main__':
    main()


