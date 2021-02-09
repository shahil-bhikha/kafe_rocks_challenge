# -*- coding: utf-8 -*-

import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def getFiles(directory):
    """
    getFiles reads in files from the directory specified and stores them in seperate lists
    depending on the contents of the file.
    
    Parameters
    ----------
    directory : Dataframe
        Contains marketing metadata.

    Returns
    -------
    metaFile : List
        Contains csv files which have marketing metadata.
    depositFiles : List
        Contains csv files which have customer deposit data.
    reportFiles : List
        Contains csv files which have customer revenue data.
    """
    f = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        f.extend(filenames)
        break
    
    metaFile = []
    depositFiles = []
    reportFiles = []
    for file in f:
        if "CustomerReport" in file:            
            df = pd.read_csv(os.path.join(dirpath, file), header=0, index_col=None)
            df["Date"] = file[2:9]
            reportFiles.append(df)
        elif "CustomerDeposits" in file:
            df = pd.read_csv(os.path.join(dirpath, file), header=0, index_col=None)
            df["Date"] = file[2:9]
            depositFiles.append(df)
        elif "MarketingSourceMapping" in file:
            df = pd.read_csv(os.path.join(dirpath, file), header=0, index_col=None)
            df["Date"] = file[2:9]
            metaFile.append(df)
            
    return metaFile, depositFiles, reportFiles

def cleanDf(metaD, customerD, customerR):
    """
    cleanDf takes in the three dataframes, cleans the data and provides a final
    denormalised dataset.
    Parameters
    ----------
    metaD : Dataframe
        Contains marketing metadata.
    customerD : Dataframe
        How much funds were deposited per customer per month.
    customerR : Dataframe
        How much revenue was generated per customer per month.

    Returns
    -------
    df2 : Dataframe
        Dataframe with the cleaned data ready for additional business logic.
    """
    # Raname columns to better format.
    metaD.rename(columns=lambda x: str.lower(x).replace(" ", "_"), inplace=True)
    customerD.rename(columns=lambda x: str.lower(x).replace(" ", "_"), inplace=True)
    customerR.rename(columns=lambda x: str.lower(x).replace(" ", "_"), inplace=True)
    
    
    # Drop null rows and 'Total' rows.
    customerD.drop(customerD[(customerD["customer_reference_id"] == "Totals:")
                              | (customerD["customer_reference_id"].isnull())].index,
                    inplace=True)
    
    customerR.drop(customerR[(customerR["customer_reference_id"] == "Totals:")
                              | (customerR["customer_reference_id"].isnull())].index, 
                    inplace=True)
    # Left join customer revenue onto customer deposits and select only a subset of columns.
    df = pd.merge(customerD[["customer_reference_id", "date","total_first_deposit_count"]],
                    customerR[["customer_reference_id","marketing_source_name",
                    "total_net_revenue","date", "reward_plan"]],
                    how="left", 
                    on=["customer_reference_id","date"])
    # Left join metadata onto df (above). 
    df1 = pd.merge(df, metaD[["domainid", "name", "reward_plan"]], 
                      how="left", 
                      left_on=["marketing_source_name", "reward_plan"], 
                      right_on=["name", "reward_plan"],
                      validate="many_to_one")
    
    # Drop any customers who have not made a first time deposit.
    df2 = df1.drop(df1[df1["total_first_deposit_count"].isnull()].index)
    
    # Add a new customer retention column to track how many customer came back 
    # in the following months.
    df2['customers_retained_count'] = df2.sort_values(by=["date"], ascending=True)\
        .groupby(["customer_reference_id"])["total_first_deposit_count"]\
        .shift(1)
    
    df2['customers_retained_revenue_sum'] = df2.sort_values(by=["date"], ascending=True)\
    .groupby(["customer_reference_id"])["total_net_revenue"]\
    .shift(1)
    
    return df2

def reportFilter(df, ID: int):
    """
    reportFilter checks if any filter needs to be applied to the dataset and returns
    the resultant set accordingly.
    Parameters
    ----------
    df : Dataframe
        Input dataframe to apply filter on.
    ID : int
        DomainID to filter the dataframe on.

    Returns
    -------
    Dataframe
        New dataframe with the filtered data.

    """
    if ID in df["domainid"].unique():
        return df[df["domainid"] == int(ID)]
    else:
        print("Not a valid domain id, no filter was applied")
        return df
        

def getReports(df, domainID:int):
    """
    getReports takes in the dataframe, generates and saves the plots in the current
    directory.
    Parameters
    ----------
    df : Dataframe
        Provide the final dataframe to create plots over.

    Returns
    -------
    None.

    """
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    
    df1 = df.groupby("date")\
        .count()[["total_first_deposit_count", "customers_retained_count"]]
    
    fig, ax = plt.subplots()
    df1.plot.bar(rot=0, ax=ax)
    ax.legend(["first_deposit_count", "customers_retained_count"]);
    fig.savefig(f'first_deposit_per_customer_domain_{domainID}_{now}.png');

    df2 = df.groupby("date")\
        .sum()[["total_net_revenue", "customers_retained_revenue_sum"]]
    
    fig, ax = plt.subplots()
    df2.plot.bar(rot=0, ax=ax)
    ax.legend(["customer_first_deposit_net_revenue", "customers_retained_revenue_sum"]);
    fig.savefig(f'revenue_per_customer_domain_{domainID}_{now}.png');
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    