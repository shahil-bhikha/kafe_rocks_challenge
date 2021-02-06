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
from datetime import datetime
from configparser import ConfigParser

fileFormat = ["csv", "csvx", "json"]

def main():
    # Read in config file.
    config = ConfigParser()
    config.read("config.ini")
    
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    
    boardName = config.get("metroretro", "board_name")
    
    # Connect to mysql DB.
    localDB = db(config.get("db", "db_host"), 
                 config.get("db", "db_user"), 
                 config.get("db", "db_password"))
    localDB.connect()
    
    # Connect to metroretro client.
    client = metroretro(config.get("metroretro", "metroboard_username"), 
                        config.get("metroretro", "metroboard_password"))
    client.connect()
        
    # Find the metro retro board id.
    board = client.getBoards(boardName)
    if board == "":
        return "Board not found"
    
    # Fetch board data.
    urlData = client.getBoardData(board, fileFormat[1])  
    
    # Be explicit about column names.
    columns = ["category", "author", "content", "votes", "date", "comments"]
    
    # Convert raw data into a dataframe.
    rawData = pd.read_csv(io.StringIO(urlData), names=columns, header=0)
    
    # Convert NaN fields to None.
    rawData = rawData.where(pd.notnull(rawData), None)
    
    # Update date column from string to timestamp.
    rawData['date'] = pd.to_datetime(rawData['date'])
        
    
    sql = ("INSERT INTO `metroboard` (`board_name`, `category`, "
    "`author`, `content`, `votes`, `date`, `comments`, `created_at`, "
    "`updated_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    for i, row in rawData.iterrows():
        val = (boardName, row['category'], row['author'], row['content'], 
               row['votes'], row['date'].strftime("%Y-%m-%d %H:%M:%S"), row['comments'], formatted_date, 
               formatted_date)    
        localDB.executestatement(sql, val)
        
    # Close db cursor and connection.
    localDB.close()

if __name__ == '__main__':
    main()


