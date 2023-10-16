# -*- coding: utf-8 -*-
from __future__ import print_function
"""
This module contains functions for reading and returning GPS data

The module containes the following functions 
---------------
def read_hytrological(station, start=None, end=None, 
                      frfile=False, fname=None, wrfile=True, flist=[], 
                      base_path="/mnt/hytrodata/", fext=".dat" )
---------------

"""

# used in a a function arguments
import logging

#
# Functions returning data subsets.
#


#
# Functions reading in data from data sources
#


def read_hytrological_data(station, start=None, end=None, frfile=False, fname=None, wrfile=True, 
                           flist=[], base_path="/mnt_data/hytrodata/", fext=".dat", logging_level=logging.WARNING):
        
    """
    ----------------------- ALPHA VERSION --------------------------------
    Reading in hytrological data and returning it
    
    input: 
        station: 


    output:
        return data:
            data is a pandas.DataFrame() containing time series of hytrological data specified in input.
    

    This is the first attempt at general reading in of  hytrological data 
    
    for test and achive purpuses the data can be read in through a file by frfile=True and spesifying a file name
    assuming the data structure was saved using data.to_pickle.

    """
    
    # Imports
    import os
    import logging

    import datetime as dt
    import pandas as pd

    import gtimes.timefunc as gt

    
    tstrf="%Y%m%d %H:%M:%S"
    # defing period to extract
    if end == None:
        end = dt.datetime.now()
    if start == None:
        start = gt.toDatetime("1990-01-01 00:00:00",dstr)
        #start = gt.currDatetime(-90,refday=end) 

    # Handling logging
    logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging_level )
    logging.getLogger().setLevel(logging_level)
    module_logger = logging.getLogger()

    if frfile:
        # For later
        if not fname:
            fname="hytro-data.pik"
        data = pd.read_pickle(fname)

    else:
        
        if flist == []:
            # formatting the file and constructing a list
            var_path="{0}".format(station.capitalize())
            fbasename="{0}_alestur-".format(station.capitalize())
            fstring="{0}%Y{1}".format(os.path.join(base_path, var_path, fbasename),fext)

            # Creating a list of files to open
            flist=gt.datepathlist(fstring,'1Y',start,end, datelist=[ dt.date(year,1,1) for year in range(start.year,end.year+1) ])

            #u_columnlist=["W1_med_cm", "Tw1_med_C", "EC_med_us", "pH_med", "TL1_med_C"]
            # data columns to use
            u_columnlist=["W1_med_cm", "Tw1_med_C", "EC_med_us", "TL1_med_C"]

        data = pd.DataFrame()
        for dfile in flist:
            try:
                module_logger.info("Reading from file: {}".format(dfile))
                tmp = pd.read_csv(dfile,sep=',', header=[0],skiprows=[0,2,3], parse_dates=["TIMESTAMP"] ,index_col=[0], dayfirst=True,
                                  error_bad_lines=False, warn_bad_lines=False, low_memory=False)
                                  # low_memory=False suppresses mixed type warning ???
                module_logger.debug("Dataframe columns: {}:\n".format(dfile) + str(tmp.columns) + "\n")

            except:
                module_logger.warning("File, {0} not found".format(dfile))
                continue
            
            for column in u_columnlist:
                tmp[column] = pd.to_numeric(tmp[column], errors="coerce")
                
            tmp = tmp[u_columnlist].dropna()
            data = data.append(tmp)

        data.drop_duplicates()
        module_logger.info("Dataframe columns:\n" + str(data.columns) + "\n")
        module_logger.info("Input time period: ({}, {})".format(start, end))
        module_logger.info("dataframe First and Last lines:\n"  + str(data.iloc[[0,-1]]))
        module_logger.debug("Dataframe shape: {}".format( str(data.shape) )) 
        module_logger.debug("dataframe types:\n" + str(data.dtypes) + "\n" )


        if wrfile:
            if not fname:
                fname="hytro-data.pik"

            data.to_pickle("{}".format(fname))



    if data.index[0] > start:
        start =  data.index[0]

    if data.index[-1] < end:
        end = data.index[-1]

    return data[start.strftime(tstrf):end.strftime(tstrf)]
