import pandas as pd
import numpy as np
import sqlite3
    
def query_climate_database(db_file, country, year_begin, year_end, month):
    
    """
    makes a query to db_file for climate data for given arguments and
    returns a dataframe with relevant data    
    """
    
    cols = 'stations.NAME, LATITUDE, LONGITUDE, countries.Name AS Country, Year, Month, Temp'
    ISOcmd = \
    f"""
        SELECT {cols} 
        FROM ((temperatures 
        INNER JOIN stations ON temperatures.ID = stations.ID)
        LEFT JOIN countries ON SUBSTR(stations.ID, 1, 2) = "ISO 3166")
        WHERE countries.Name = \'{country}\' AND Year >= {year_begin} \
        AND Year <= {year_end} AND Month = {month}
    ;"""
    FIPScmd = \
    f"""
        SELECT {cols} 
        FROM ((temperatures 
        INNER JOIN stations ON temperatures.ID = stations.ID)
        LEFT JOIN countries ON SUBSTR(stations.ID, 1, 2) = "FIPS 10-4")
        WHERE countries.Name = \'{country}\' AND Year >= {year_begin} \
        AND Year <= {year_end} AND Month = {month}
    ;"""

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        df = pd.read_sql_query(ISOcmd, conn)
        df2 = pd.read_sql_query(FIPScmd, conn)
        df = df.merge(df2, how = 'outer')
        df = df[~np.isnan(df['Temp'])]
        
    return df
