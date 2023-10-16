# -*- coding: utf-8 -*-
from __future__ import print_function
"""
Reading in gas data from IMO

functions ror read in data: 
def read_gas_data(station, device,  start=None, end=None, dsource="FILE", wrfile=True, 
                  fname=None, with_excluded=True, id_observation_start=False, conn_dict=False, 
                  logging_level=logging.INFO):

functions for returning subsets:
"""

# used in  a function arguments
#import geofunc.geo as geo 
import logging

#
# Initital trivial filtering
#


def mask_first(x):

    """
    """
    import numpy as np

    x[0] = False
    
    return x

def init_multigas(data):
    """
    """
    import pandas as pd  
    pd.set_option('mode.chained_assignment',None) 
    

    data['filter']=True
    mask = data.groupby(['acquisition'])['filter'].transform(mask_first)
    data = data.loc[mask]
    #data.loc[:,'co2_concentration'] *= 0.0001 # data['co2'].multiply(0.0001)

    if "co2_concentration" in data.columns:
        data['co2_concentration'] = data['co2_concentration'].apply( lambda x: x*0.0001)

    return data


#
# reading the gas data
#

def read_gas_data(station, device,  start=None, end=None, dsource="FILE", wrfile=True, 
                  fname=None, with_excluded=True, id_observation_start=False, conn_dict=False, 
                  logging_level=logging.INFO):
    """
    Reading in gas data and returning it as pandas.DataFrame
    """

    import requests
    import logging
    import psycopg2
    from psycopg2 import sql
    import pandas as pd
    import datetime as dt
    from datetime import timedelta as td
    import gtimes.timefunc as gt

    # String format for the rest service
    strf="%Y-%m-%d %H:%M:%S"

    # Handling logging
    logging.basicConfig(
        format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
        level=logging_level )

    logging.getLogger().setLevel(logging_level)
    module_logger = logging.getLogger()

    #pd.options.mode.chained_assignment = None

    if fname == None:
        #fname="gas/lagu.p"
        fname = "{0:s}-{1:s}.p.gz".format(station,device)
    
        

    data = pd.DataFrame()
    if dsource == "FILE":
        try: 
            module_logger.info("Reading gas data from file: {}".format(fname))
            data = pd.read_pickle(fname)

        except  IOError as e:
            module_logger.info("While reading File {}:  ".format(fname) + str(e))
        except  pd.errors.EmptyDataError as e:
            module_logger.info("While reading File {}:  ".format(fname) + str(e))
        except BaseException as e:
            module_logger.error("While reading File {}:  ".format(fname) + str(e))
            raise

        if start:
            data = data[(data.index > start)]
        if end:
            data = data[(data.index < end)]

    elif dsource == "DBASE":
        period = ""
        if start:
            period = period + "and o.acquisition >= '{}'".format(start.strftime(strf)) 
        if end:
            period = period + " and o.acquisition <= '{}'".format(end.strftime(strf)) 
        
        #if conn_dict:
        module_logger.info("Connecting to database:")
        module_logger.info("Connection info:\n{}".format(conn_dict))
        
        try:
            conn = psycopg2.connect( dbname=conn_dict["dbname"],
                                       user=conn_dict["user"],
                                   password=conn_dict["password"], 
                                       host=conn_dict["host"], 
                                       port=conn_dict["port"] )
        except TypeError as e:
            module_logger.warning("Your dicionary is not formated correctly it's value is:\n  {} \n".format(conn_dict) + str(e))
            raise
        except BaseException as e:
            module_logger.error("Error while connecting to database using {}\n:  ".format(conn_dict) + str(e))
            raise

        cursor = conn.cursor()

        sql_command="SELECT * FROM device;"

        query = ("select o.id, code, observation_time, acquisition, numeric_value \
                \
                 from observation o \
                 join device d \
                    on o.id_device= d.id \
                 join tos_station s \
                    on d.id_tos_station=s.id \
                 join parameter p \
                    on o.id_parameter=p.id \
                    \
                 where s.station_identifier = '{}' \
                 and  d.device_identifier = '{}'  {} \
                \
                order by o.observation_time").format(station,device,period)
        
        module_logger.info("Query info:\n" + str(query))

        #data.to_pickle("{}_{}.p.gz".format(station,device))
        
        try:
            data = pd.read_sql(query, conn)
            data = pd.concat([data.set_index('observation_time')['acquisition'],
                          data.pivot(  index='observation_time', columns='code', 
                          values='numeric_value')], axis=1).drop_duplicates()    
        except:
            pass

    elif dsource == "SERVICE":

        server="localhost"
        port=11111
        prepath="/aot/gas/v2/stations"

        url_rest="http://{}:{}{}/{}/devices/{}/observations".format(server,port,prepath,station,device)

        if end == None:
             end = dt.datetime.now()
        if start == None:
            start = gt.currDatetime(-30,refday=end) 

    
        #print(end-start)
        #read_blocks=gt.datepathlist(strf,'20D',start,end)
        #dspan = "&date_from={0:s}&date_to={1:s}".format(start.strftime(strf),end.strftime(strf))

        #dspan = "?date_to={0:s}".format(end.strftime(strf))
        #with_excluded="?with_excluded={0}".format(with_excluded)
    
        id_observation_start="&id_observation_start={0}".format(id_observation_start)
        param_string=with_excluded+id_observation_start+dspan

        #request = requests.get(url_rest+station_marker+'?date_from=2012-12-01 00:00:00&date_to=2017-12-31 00:00:00')
        #print(url_rest+param_string)
        request = requests.get(url_rest+param_string)
        data = pd.DataFrame.from_records(request.json()['data'],index='observation_time')
        data.index = pd.to_datetime(data.index)
        
    
        if device == "multigas":
            data = init_multigas(data)
        elif device == "crowcon":
            pass

    else:
        module_logger.error("Unregignised read method {}, use: \"FILE\", \"SERVICE\" or \"DBASE\" ".format(dsource))
        raise NameError("Unregignised source name {}".format(dsource))




    if wrfile == True:
        data.to_pickle(fname)
    try:
        module_logger.info("Dataframe columns:\n" + str(data.columns) + "\n")
        module_logger.info("Input time period: ({}, {})".format(start, end))
        module_logger.info("dataframe First and Last lines:\n"  + str(data.iloc[[0,-1]]))
        module_logger.debug("Dataframe shape: {}".format( str(data.shape) )) 
    except IndexError:
        module_logger.warning("Dataframe is empty {}".format( str(data) )) 


    #tbegin = dt.strptime(request.json()['temporalExtent']['begin'], "%Y-%m-%dT%H:%M:%S")
    #tend = dt.strptime(request.json()['temporalExtent']['end'], "%Y-%m-%dT%H:%M:%S")
    #print(tbegin)
    #print(tend)
    #print(tend-tbegin)
    return data

