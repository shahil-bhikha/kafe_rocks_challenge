#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 10:45:37 2021

@author: shahil
"""

import io
import pandas as pd
from datetime import datetime

# Be explicit about column names.
columns = ["category", "author", "content", "votes", "date", "comments"]

def writeToDf(data):
    # Convert raw data into a dataframe.
    rawData = pd.read_csv(io.StringIO(data), names=columns, header=0)
    
    # Convert NaN fields to None.
    rawData = rawData.where(pd.notnull(rawData), None)
    
    # Update date column from string to timestamp.
    rawData['date'] = pd.to_datetime(rawData['date'])
    
    return rawData

def toDB(dbconn, board, data):
    formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    sql = ("INSERT INTO `metroboard` (`board_name`, `category`, "
           "`author`, `content`, `votes`, `date`, `comments`, `created_at`, "
           "`updated_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    for i, row in data.iterrows():
        val = (board, row['category'], row['author'], row['content'], 
           row['votes'], row['date'].strftime("%Y-%m-%d %H:%M:%S"), row['comments'], 
           formatted_date, formatted_date)    
        dbconn.executestatement(sql, val)
