#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 19:48:54 2021

@author: shahil
"""

import argparse

import pandas as pd

import util

directory = "Data_Engineer_Challenge_-_Data"


def main():    
    parser = argparse.ArgumentParser(description="Filter for customer reports")
    parser.add_argument("-id", help="domain ID you would like to filter reports on")
    args = parser.parse_args()
    
    domainID = args.id
    if domainID == None:
        domainID = 0
    
    # Read in all the required files from the directory specified.
    metaFile, depositFiles, reportFiles = util.getFiles(directory)
    
    # Convert files to dataframe objects. 
    metaD = pd.concat(metaFile, axis=0, ignore_index=True)    
    customerD = pd.concat(depositFiles, axis=0, ignore_index=True)    
    customerR = pd.concat(reportFiles, axis=0, ignore_index=True)
    
    # Clean and transform data.
    df = util.cleanDf(metaD, customerD, customerR)

    # Apply any filter provided to dataset.
    df1 = util.reportFilter(df, domainID)
    
    # Generate and save reports.
    util.getReports(df1, domainID)

if __name__ == '__main__':
    main()