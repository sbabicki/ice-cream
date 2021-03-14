import pandas as pd
import numpy as np
import re

def data_consolidation():
    # Read csv 
    df = pd.read_csv('../data/raw/business-licences-hackathon.csv', delimiter = ";")
    
    # Fill nan with empty string
    df.fillna('', inplace=True)
    
    # Concatenate columns to create 'address' column
    df['Unit'] = df['Unit'].astype(str)
    df["House"] = df["House"].astype(str).str.replace(r'.0', '')
    df['Address'] = df['UnitType'] + " " + df['Unit'] + " " + df['House'] + " " + df['Street'] + " " + df['City'] + " " + df['Province'] + " " + df['Country'] + " " + df['PostalCode']
    df['Address'] = df['Address'].str.strip()
    
    # Drop some columns and reorder columns
    df = df.drop(columns=['Unit', 'UnitType', 'House', 'Street', 'City', 'Province', 'Country', 'PostalCode'])
    df = df[['BusinessName', 'BusinessTradeName', 'Address', 'FOLDERYEAR', 
             'LicenceRSN', 'LicenceNumber', 'LicenceRevisionNumber', 'Status', 
             'IssuedDate', 'ExpiredDate', 'BusinessType', 'BusinessSubType', 
             'LocalArea', 'NumberofEmployees', 'FeePaid', 'ExtractDate', 'Geom']]
    
    # Sort FOLDERYAR column by descending order
    df = df.sort_values(by='FOLDERYEAR', ascending=False)
    
    # Output processed csv file to processed data folder
    df.to_csv('../data/processed/business-licences-hackathon.csv', index = False)

if __name__ == "__main__":
    data_consolidation()
