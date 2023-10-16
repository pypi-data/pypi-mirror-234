# -*- coding: utf-8 -*-
from __future__ import print_function
"""
Reading in Data Geophysical data from IMO


functions to read in data:
    def read_sil_data(start=None, end=None, area=None, frfile=None,
                      base_path="/mnt/sildata", fread="events.fps",
                      rcolumns=[], logging_level=logging.WARNING,
                      cum_moment=True, **kwargs):

functions for returning subsets:
    def seism_subset(data, start=None, end=None, min_lat=None, max_lat=None,
                     min_lon=None, max_lon=None, min_depth=None,
                     max_depth=None, min_mlw=None, max_mlw=None)

"""


#
# Functions returning data subsets.
#

# For seismic

def seism_subset(data, start=None, end=None,
                 min_lat=None, max_lat=None, min_lon=None, max_lon=None,
                 min_depth=None, max_depth=None, min_mlw=None, max_mlw=None,
                 dna=False, min_Q=None, max_Q=None, tstrf="%Y%m%d %H:%M:%S",
                 logger=__name__):
    '''Cuts out a subset of a dataframe assumes data.index is datetime index.'''
    import logging
    import pandas as pd

    # Handling logging
    module_logger = logging.getLogger(logger)

    if dna:
        data = data.dropna()

    start_ser = end_ser = data.index.notna()  # time, index
    min_lat_ser = max_lat_ser = data.index.notna()  # latitude
    min_lon_ser = max_lon_ser = data.index.notna()  # longitude
    min_depth_ser = max_depth_ser = data.index.notna()  # depth
    min_mlw_ser = max_mlw_ser = data.index.notna()  # Mlw
    min_Q_ser = max_Q_ser = data.index.notna()  # Q

    # making boolean filter arrays for all parameters
    if start is not None:
        start_ser = data.index > start
    if end is not None:
        end_ser = data.index < end
    if min_lat is not None:
        min_lat_ser = data["latitude"] > min_lat
    if max_lat is not None:
        max_lat_ser = data["latitude"] < max_lat
    if min_lon is not None:
        min_lon_ser = data["longitude"] > min_lon
    if min_lon is not None:
        max_lon_ser = data["longitude"] < max_lon
    if min_depth is not None:
        min_depth_ser = data["depth"] > min_depth
    if max_depth is not None:
        max_depth_ser = data["depth"] < max_depth
    if min_mlw is not None:
        if "MLW" in data:
            min_mlw_ser = data["MLW"] > min_mlw
        elif "ML" in data:
            min_mlw_ser = data["ML"] > min_mlw

    if max_mlw is not None:
        if "MLW" in data:
            max_mlw_ser = data["MLW"] < max_mlw
        elif "ML" in data:
            max_mlw_ser = data["ML"] < max_mlw

    if min_Q is not None:
        if "Q" in data:
            min_Q_ser = data["Q"] > min_Q

    if max_Q is not None:
        if "Q" in data:
            max_Q_ser = data["Q"] < max_Q

    # Applying all the filters in one call

    data = data[start_ser & end_ser &
                 min_lat_ser & max_lat_ser & 
                 min_lon_ser & max_lon_ser & 
                 min_depth_ser & max_depth_ser & 
                 min_mlw_ser & max_mlw_ser &
                 min_Q_ser & max_Q_ser]

    module_logger.info("Input time period: ({0}, {1}). Range in DataFrame: ({2}, {3})"
                        .format(start, end,  data.index.min(), data.index.max()) )
    module_logger.info("Selected latitude range: ({0}, {1}). Range in DataFrame: ({2:.3f}, {3:.3f})"
                        .format( min_lat, max_lat, data.latitude.min(), data.latitude.max()) )
    module_logger.info("Selected longitude range: ({0}, {1}). Range in DataFrame: ({2:.3f}, {3:.3f})"
                        .format( min_lon, max_lon, data.longitude.min(), data.longitude.max()) )
    module_logger.info("Selected depth range: ({0}, {1}). Range in DataFrame: ({2:.3f}, {3:.3f})"
                        .format( min_depth, max_depth, data.depth.min(), data.depth.max()) )

    if "MLW" in data:
        module_logger.info("Selected magnitude range: ({0}, {1}). Range in DataFrame: ({2:.2f}, {3:.2f})"
                            .format( min_mlw, max_mlw, data.MLW.min(), data.MLW.max()) )
    elif "ML" in data:
        module_logger.info("Selected magnitude range: ({0}, {1}). Range in DataFrame: ({2:.2f}, {3:.2f})"
                            .format( min_mlw, max_mlw, data.ML.min(), data.ML.max()) )
     
    if "Q" in data:
        module_logger.info("Selected quality range: ({0}, {1}). Range in DataFrame: ({2:.2f}, {3:.2f})"
                            .format( min_Q, max_Q, data.Q.min(), data.Q.max()) )

    module_logger.info("Number of earquakes: {0}".format( data.size) )
    module_logger.info("dataframe First and Last lines:\n"  + str(data.iloc[[0,-1]]))
    #module_logger.info("Latidues: {}".format( (min_lat_list and max_lat_list) ) )
    #data = data[start.strftime(tstrf):end.strftime(tstrf)]

    return data


def distalongline():
    """
    """


#
# Functions reading in data from data sources
#

def read_sil_file(dfile, duplicate=True, logger=__name__ ):
    """
    Open files from in a sil directory returning its content in a dataframe
    """

    import pandas as pd
    import logging
    import os


    # Handling logging
    module_logger = logging.getLogger(logger)

    module_logger.debug("Reading file {}:  ".format(dfile))

    fread = os.path.basename(dfile)
    
    # defining file structures of sil files
    if fread == "lib.mag":
        module_logger.info("reading data from  file {}:  ".format(dfile))

        # athuga nota num_of_st_pha
        # min_dist_sta distance to closest station
        columns = ["num", "date", "time", "latitude", "longitude", "depth", "MLW", "ML", "num_of_st_ML", 
                   "minMl", "maxMl", "num_of_st_pha", "num_of_P-pha", "num_of_S-pha", "num_of_polarities", 
                   "Ddata_time", "Dlatitude", "Dlongitude", "Ddepth", "w_rms_res", "min_dist_sta", 
                   "max_azim_gap", "vel_modelk", "event_type"]
        col_dtypel = ['int64', 'float64', 'float64', 'float64', 'float64', 'float64', 'int64',
                     'float64', 'float64', 'int64', 'int64', 'int64',
                     'int64', 'float64', 'float64', 'float64', 'float64', 'float64',
                     'float64', 'float64', 'int64', 'object']
        col_with=[ (0, 4), (4, 13), (13, 24), (24, 33), (33, 43), (43, 50), (50, 56), (56, 62), (62, 67), 
                   (67, 73), (73, 79), (79, 82), (82, 85), (85, 88), (88, 92), 
                   (92, 98), (98, 104), (104, 110), (110, 116), (116, 123), (123, 130), 
                   (130, 136), (136, 138), (138, 141)]

        

    elif fread=="events.fps":
        module_logger.info("reading data from  file {}:  ".format(dfile))

        columns =    [ "num", "date", "time", "latitude", "Dlatitude", "longitude", "Dlongitude", "depth", "Ddepth",
                       "MLW", "id", "seismic_moment", "ev_mag_ATH", "event_type", "sh_min", "sh_max", "azim_comp", 
                       "relative_size", "shearwave_corner_freq", "fault_radius", "stress_drop", "peak_slip", "source_file",
                       "strike_a_agr", "dip_a_agr", "slip_a_agr", "strike_b_agr", "dip_b_agr", "slip_b_agr", 
                       "num_of_polarities", "num_of_amplitudes", "unknown_pacc","is_significant"]
        col_dtypel = ['int64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64', 
                      'float64', 'object', 'float64', 'float64', 'object', 'float64', 'float64', 'float64', 
                      'float64', 'float64','int64', 'float64', 'float64', 'object', 
                      'int64', 'int64','int64', 'int64', 'int64', 'int64', 
                      'int64', 'int64', 'float64', 'int64']


    elif fread=="events.lib":
        module_logger.info("reading data from  file {}:  ".format(dfile))

        columns=[ "num", "date", "time", "latitude", "longitude", "depth", "MLW", "event_type", "id", "sh_min", "sh_max", "azim_comp", "num_of_polarities"]
        col_dtypel = ['int64', 'float64', 'float64', 'float64', 'float64', 'object', 'object', 'float64', 'float64', 'float64', 'int64']
        col_with=[ (0, 4), (4, 13), (13, 24), (24, 33), (33, 43), (43, 50), (50, 55), (55, 59), (59, 92), (92, 101), (101, 108), (108, 115), (115, 118)]


    elif fread=="cleanaut.mag" or fread=="aut.mag":
        module_logger.info("reading data from  file {}:  ".format(dfile))

        columns = ["num", "date", "time", "latitude", "longitude", "depth", "ML", "Q", "id"]
        col_dtypel = ['int64', 'float64', 'float64', 'float64', 'float64', 'float64',  'object']
        col_with=[ (0, 4), (4, 13), (13, 22), (22, 30), (30, 39), (39, 45), (45, 51), (51, 57), (57, 89)]

    else: # if file not regoginced raise an error
        module_logger.error("Unrecognised file name {}:  ".format(dfile))

        raise IOError 

    try:
        module_logger.info("Trying read columns {} from file {}:  ".format(columns, dfile))

        rcolumns = [columns[0]] + columns[3:]
        col_dtype = dict(zip(rcolumns, col_dtypel))

        if fread=="events.fps":
            tmp = pd.read_csv(dfile,  sep='\s+',  header=None, names=columns, dtype=col_dtype, infer_datetime_format=True,
                    parse_dates={"date_time": ['date', 'time']}, index_col="date_time")
            tmp=tmp.dropna()
        else:
            tmp = pd.read_fwf(dfile, header=None, colspecs=col_with, dtype=col_dtype, infer_datetime_format=True,
                    names=columns, parse_dates=[['date', 'time']], index_col="date_time")
            tmp=tmp.dropna()

        if duplicate == False:
            tmp = tmp[~tmp.duplicated()]
        
        if tmp.empty:
            # If empty file, will have columns 'date' and 'time' in empty
            # DataFrame as pandas will not apply parse_dates/index_col,
            # must drop them to avoid adding empty columns to final DataFrame.
            # Example: /mnt/sk2/1993/jan/29/events.fps (no event that day)
            tmp = pd.DataFrame(columns=rcolumns)

    
    except ValueError as e:        
        module_logger.info("While reading File {0}: exception of type {1} occured, returning an empty DataFrame: ".format( dfile, type(e).__name__ ) + str(e))

    except  IOError as e:
        module_logger.info("While reading File {0}: exception of type {1}:  ".format( dfile, type(e).__name__ ) + str(e))
        raise IOError

    except BaseException as e:
        module_logger.info("While reading File {0}: exception of type {1}: ".format( dfile, type(e).__name__ ) + str(e), exc_info=True)
        raise


    return tmp


def read_automatic( ddir, aut=True, repl_mlw=False, logger=__name__ ):
    """
    """
    import pandas as pd
    import logging
    import os


    # Handling logging
    module_logger = logging.getLogger(logger)


    rcolumns= ['latitude', 'longitude', 'depth', 'MLW', 'Q', 'id', 'seismic_moment', "MW"]

    eventfps = pd.DataFrame(columns = rcolumns)
    cleanaut = pd.DataFrame(columns = rcolumns)
                
    dfile = os.path.join( ddir,"events.fps")
    module_logger.debug("Reading file {}:  ".format(dfile))
    
    if aut == "only":
        pass
    else:
        try: 
            eventfps=read_sil_file(dfile, logger=logger)
       
            eventfps["MW"] = eventfps.seismic_moment.apply(MW)
            eventfps["Q"] = 99.99
            eventfps = eventfps[rcolumns]

        except AttributeError as e:
            module_logger.info("missing columns from dataFrame:\n"  + str(eventfps) )
            eventfps = pd.DataFrame(columns = rcolumns)

        except  pd.io.common.EmptyDataError as e:
            module_logger.info("While reading File {}:  ".format(dfile) + str(e))
            eventfps = pd.DataFrame(columns = rcolumns)

        except  IOError as e:
            module_logger.info("While reading File {}:  ".format(dfile) + str(e))
            eventfps = pd.DataFrame(columns = rcolumns)


    

    if aut:
        dfile = os.path.join( ddir,"cleanaut.mag")
        module_logger.debug("Reading file {}:  ".format(dfile))
    
    
        try:
            cleanaut = read_sil_file( dfile, logger=logger )
        
        except  IOError as e:
            module_logger.info("While reading File {}:  ".format(dfile) )
            dfile = os.path.join( ddir,"aut.mag")
            module_logger.info("Will try  {}:  ".format(dfile))

            try:
                cleanaut=read_sil_file(dfile, logger=logger )

            except  IOError as e:
                module_logger.info("While reading File {}:  ".format(dfile) + str(e))
                cleanaut = pd.DataFrame(columns = rcolumns)

            except NotImplementedError as e:
                module_logger.info("While reading File {}:  ".format(dfile) + str(e))
                cleanaut = pd.DataFrame(columns = rcolumns)


        
        #cleanaut = read_sil_file( dfile, logging_level=logging.INFO )

        if cleanaut.empty:
            module_logger.info("dataframe is empty:\n"  + str(cleanaut) )
            cleanaut = pd.DataFrame(columns = rcolumns)

        else:
            cleanaut = cleanaut.rename(columns={"ML":"MLW"})
            cleanaut['seismic_moment'] = float('nan')
            cleanaut['MW'] = float('nan')
            cleanaut = cleanaut[rcolumns]
                    
        data  = pd.concat([eventfps, cleanaut[~cleanaut['id'].isin(eventfps['id'])]])
    
    else:
        data = eventfps

    return data

def MW(S_moment):
    """
    Calculate moment magnitude from seismic moment
    """
    from numpy import log10

    return log10(S_moment)*2/3 - 6.03 

def pgverror(r,M): 
    """
    calculate relative difference if skipping nonlinear term in PGV model for calulating MW
    See:

    Attenuation relations for near- and far-field peak ground motion (PGV, PGA) 
    and new magnitude estimatesforlargeearthquakesin SW-IcelandforlargeearthquakesinSW-Iceland
    VÍ 2009-012, ISSN 1670-8261: page: 25 eq C: 
    derive
    """
    
    from numpy import log10
    
    return ( log10( r+0.00299*10**(0.621*M)) - log10(r) ) / log10(r) 

def M_PGV(x, mu=0.000001):
    """
    Return Moment magnitude estimation based on PGV model derived in 
    
    Attenuation relations for near- and far-field peak ground motion (PGV, PGA) 
    and new magnitude estimatesforlargeearthquakesin SW-IcelandforlargeearthquakesinSW-Iceland
    VÍ 2009-012, ISSN 1670-8261: page: 25 eq C: 
    
    expect pgv in m/s
    and    r in km

    """
    from numpy import log10

    

    return 1/1.05 * ( 1.69*log10(x[0]) +  log10( mu*x[1] ) + 4.96 )


##
# modules to extract PGV from Alert and distance in order to estimate Mw from PGV equation
##
def read_evb(filename, logger="__name__"):
    """
    """

    from datetime import datetime as dt
    import pandas as pd
    import logging


    # Handling logging
    module_logger = logging.getLogger(logger)

    columns = [ "sta", "arr.", "time", "res.",  "weight", "dist" , "azi", "az.obs",  "err", "number"]
    col_dtypel = ['str', 'str', 'int64', 'int64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64']

    col_with=[ (0, 4), (4, 6), (6, 18), (18, 24), (24, 30), (30, 36), (36, 42), (42, 49), (49, 55), (55, 62) ]
    
    parser = lambda time: dt.strptime(time, '%H %M %S.%f')
    #parse_dates={"time": ['hour', 'minute', 'sec']},
    data = pd.read_fwf( filename, skiprows=5, skipfooter=1, colspecs=col_with, names=columns, parse_dates=["time"], date_parser=parser, index_col="sta")
    data['time'] = pd.to_datetime(data.time).dt.time

    return data


def read_alert(filename, logger="__name__"):
    """
    """

    import pandas as pd
    import logging

    # Handling logging
    module_logger = logging.getLogger(logger)

    rcolumns = ["lon", "lat", "time", "pgv", "sta", "fb"]
    col_dtypel = ['float64', 'float64', 'float64', 'float64', 'str', 'float64']

    col_dtype = dict(zip(rcolumns, col_dtypel))

    data = pd.read_csv(filename, skiprows=1, sep="\s+", usecols=[0,1,2,3,4,5],
                       names=rcolumns, dtype=col_dtype,  index_col="sta")
    data['time'] = data['time'].div(100)  # change from samples to seconds
    return data


def downl_PGV_hraun(inpdate=None, tmp_path=None, dstr='/%Y/%b/%d',
                    logger=__name__, rm_files=False):
    """
    """

    import os
    import locale
    import logging
    import glob

    from datetime import date
    import urllib.request as ur

    import gtimes.timefunc as gt

    # Handling logging
    module_logger = logging.getLogger(logger)

    # changing locals so the system will recoginse month folders correctly (i.e des -> dec)
    loc = locale.getlocale()
    locale.setlocale(locale.LC_TIME, ('en_US', 'UTF-8'))

    # defing default period to extract
    # dstr='%Y-%m-%d %H:%M:%S'
    if inpdate == None:
        inpdate = date.today()

    elif type(inpdate) is str:
        inpdate = gt.toDatetime(inpdate, dstr)

    alert_url = "http://hraun.vedur.is/ja/alert/"
    dpath = inpdate.strftime("%Y/%b/%d/").lower()

    if tmp_path is None:
        tmp_path = "/tmp/alert/"

        # making sure download directoty exists and is empty
        try:
            os.makedirs(tmp_path)

        except FileExistsError as e:
            module_logger.info("directory {} exists:  ".format(tmp_path) + str(e), exc_info=True)

            if rm_files:
                files = glob.glob(tmp_path+'*')
                for f in files:
                    os.remove(f)
            else:
                raise

        except FileNotFoundError as e:
            module_logger.info("Can not create directory   {}:  ".format(tmp_path) + str(e), exc_info=True)

    i = 0
    while True:
        i += 1
        filename = "{0:03d}.event".format(i)
        try:
            ur.urlretrieve(alert_url + dpath + filename, os.path.join(tmp_path, filename))
        except:
            break

    # restoring locale settings
    locale.setlocale(locale.LC_TIME, loc)

    return tmp_path + "/"


def find_alert(event_id, sil_path="/mnt_data/sildata", pre_path="/tmp", eps=30, logger=__name__):
    """
    Get one SIL event evb, download alertMap events, return matching data.

    Parameters
    ----------
    event_id : str
        SIL event id = path to evb|eve|ana files.
        Example: "/2020/jun/25/00:05:00/09:33:883"
    sil_path : str, optional
        Path to SIL top dir which contains the year dirs. The default is
        "/mnt_data/sildata".
    pre_path : str, optional
        Path to local alertMap output dirs. The default is "/tmp".
        Will download XXX.event files to here and then parse them from there.
        Original location: "hellir:/var/www/sil.vedur.is/alert"
    eps : int, optional
        Time tolerance in seconds for associating events from SIL and
        alertMap. The default is 30.
    logger : str, optional
        Name of logger object. The default is __name__ (current method name).

    Returns
    -------
    dist_pgv : pandas.DataFrame
        Has index = station code, columns = dist, pgv, MW_pgv; for stations
        common in SIL *.evb and alertMap *.event files.
    """
    import logging
    import os
    import locale
    import csv
    import glob

    from datetime import datetime as dt
    from datetime import timedelta
    from pathlib import Path
    from shutil import rmtree

    loc = locale.getlocale()
    locale.setlocale(locale.LC_TIME, ('en_US', 'UTF-8'))

    # Handling logging
    module_logger = logging.getLogger(logger)

    # inpdate=dt.strptime(event_id[:12],"/%Y/%m/%d")
    # dpath=inpdate.strftime("%Y/%b/%d/").lower()

    tmp_path = os.path.join(pre_path, event_id[:12])

    # making sure download directoty exists and is empty
    try:
        os.makedirs(tmp_path)

    except FileExistsError as e:
        module_logger.info("directory {} exists:  ".format(tmp_path) + str(e), exc_info=True)

    except FileNotFoundError as e:
        module_logger.info("Can not create directory   {}:  ".format(tmp_path) + str(e), exc_info=True)
        raise

    locale.setlocale(locale.LC_TIME, loc)

    tmp_dir = sil_path + event_id
    filename = os.path.join(tmp_dir + ".evb")

    EVB = read_evb(filename, logger="__name__")
    # Download all alert files from the day of event_id and return the download path
    tmp_path = downl_PGV_hraun(inpdate=event_id[:12], tmp_path=tmp_path, logger=__name__, rm_files=True)

    files = glob.glob(tmp_path + '*')
    fields = {}
    for f in files:
        with open(f, 'r') as infile:
            reader = csv.DictReader(infile)
            fields[ reader.fieldnames[0].split()[0]] = reader.fieldnames[0].split()[4:8] 

    eps = timedelta(seconds=eps)
    window_min = (dt.combine(dt.today(), EVB.time.min()) - eps).time()
    window_max = (dt.combine(dt.today(), EVB.time.max()) + eps).time()
    for key, value in fields.items():
        event_found = window_min < dt.strptime(value[-1], "%H:%M:%S").time() < window_max

        module_logger.debug("Searching for event in {0}.event -> {1}, Found: {2}".format(key, value, event_found) )

        if event_found:
            use_file = tmp_path + key + ".event"
            module_logger.info("Found event in  -> {0}".format(use_file))

            break

    try:
        module_logger.warning("Attempting to fecth PGV values from -> {0}".format(use_file))
        PGV = read_alert(use_file)
        common_sta = list(set(PGV.index) & set(EVB.index))

        module_logger.warning("List of stations: {0}".format(common_sta))

        PGV = PGV.loc[common_sta]
        EVB = EVB.loc[common_sta]

        dist_pgv = EVB['dist'].to_frame().join(PGV['pgv'].to_frame())
        dist_pgv['MW_pgv'] = dist_pgv.apply(M_PGV, axis=1)
        dist_pgv.sort_values('dist', inplace=True)

    except:
        module_logger.warning("No alert file found for event -> {0}".format(event_id), exc_info=True)
        dist_pgv = None

    # remove the downloaded files and all the directories
    try:
        # rmtree( Path(tmp_path).parents[1] )
        pass
    except:
        module_logger.warning("Directory {0} not found".format(tmp_path))

    return dist_pgv


##
# ----------------------------------------------------------------------------
##

def removedubl(data, idcol=True, timetag=True):
    """
    """

    import numpy as np
    
    if idcol == True:
        tmp = data[data.id.duplicated(keep=False)].sort_values(['id','Q'], ascending=False)
        data.drop((tmp[tmp.id.duplicated()].index), inplace=True)

    if timetag == True:
        # adding the number 0 ... len(data) to the dataFrame for identification
        print(data.index.duplicated().any())
        print(data[data.index.duplicated(keep=False)])
        if data.index.duplicated().any():
            ilocation = data.reset_index().index
            data['ilocation'] = ilocation # tmp column to id correct rows
    
   
            # find all duplicate datetime tags and selct the row with lower "Q" to be removed
            print(data[data.index.duplicated(keep=False)].reset_index().sort_values(by=['Q']).set_index('index'))
            #tmp = data[data.index.duplicated(keep=False)].reset_index().sort_values(by=['index', 'Q']).set_index('index') 
            tmp = data[data.index.duplicated(keep=False)].reset_index().sort_values(by=['Q']).set_index('index') 
            iddrop = tmp[tmp.index.duplicated(keep='last')]['ilocation']
            print(iddrop)
    
            idx = ~np.ones(len(ilocation), dtype=bool) # True array
            idx[iddrop] = True # identifing colums to drop
            data.drop( data[idx].index, inplace=True) # droping dublicated time tags
            data.drop( ['ilocation'], inplace=True, axis=1 )# removing the tmp column)

    return data

def read_sil_data(
        start="1990-01-01", end=None,
        frfile=False, base_path="/mnt_data/sildata",
        fread="default", fname=None, rcolumns=[],
        aut=True, aut_per=30, repl_mlw=False, dna=False, duplicate=False,
        logger=__name__, logging_level=None, cum_moment=True, **kwargs):
    """
    Read earthquake parameters from IMO's SIL data structure.

    Parameters
    ----------
    start : string or datetime or int, optional
        Start of selected time range. Either string in ISO dateformat, or int
        days before end. The default is 1990-01-01.
    end : string or datetime, optional
        End of selected time range. The default is now.
    frfile : bool, optional
        Read dataframe from pickle/parquet file? If true, will use fname as
        filepath. The default is False.
    base_path : str, optional
        Path to SIL top dir which contains the year dirs,
        not used if frfile=True. The default is "/mnt_data/sildata".
    fread : str, optional
        Which type of SIL file: "lib.mag" or "events.fps",
        not used if frfile=True. The default is "events.fps".
    fname : str, optional
        Path to pickle/parquet file if frfile=True. The default is None.
    rcolumns : str, optional
        Columns to return: default selection if None or "default",
        else get all available. The default is None.
    aut : bool or str, optional
        Only used if fread="default". If aut=True, include automatic solutions
        from cleanout.mag. The default is True.
    aut_per : int, optional
        Set for how many days back from end automatic solutions to be included.
        Either an int or "all" can be set. The default is 30.
    repl_mlw : bool, optional
        Not used. The default is False.
    dna : bool, optional
        If True, drop Nan rows of output dataframe.
        TODO: Applied regardless for all files in read_sil_file(), fix it.
        The default is False.
    duplicate : bool, optional
        If true, remove duplicate entries using pandas.duplicates().
        The default is False.
    logger : str, optional
        Name of logger object. The default is __name__ (current method name).
    logging_level : str, optional
        Force set logging level by string:
            "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
        The default is None.
    cum_moment : bool, optional
        Whether to calculate and output cumulative moment as well.
        The default is True.
    **kwargs : all float
        More keys can be added to limit selection:
            min_lat, max_lat, min_lon, max_lon,
            min_depth, max_depth, min_mlw, max_mlw,
            min_Q, max_Q

    Returns
    -------
    pandas.DataFrame. Its index is event origin datetime, its columns
    are by default "latitude", "Dlatitude", "longitude", "Dlongitude",
    "depth", "Ddepth", "MLW", "seismic_moment", but can be different
    based on INPUT fread and rcolumns.
    """
    
    # Imports
    import os
    import logging
    import time
    
    from datetime import datetime as dt
    from datetime import timedelta

    import pandas as pd

    import gtimes.timefunc as gt

    # defining default period to extract
    if end is None:
        end = dt.now()
    elif isinstance(end, str):
        end = pd.to_datetime(end)
    if isinstance(start, int):
        start = abs(start)
        start = gt.currDatetime(-start,refday=end)
    elif isinstance(start, str):
        start = pd.to_datetime(start)


    # Handling logging
    logging.basicConfig()
    module_logger = logging.getLogger(logger)
    module_logger.setLevel(logging.WARNING)
    if logging_level:
        module_logger.debug('Set logger level: {}'.format(logging_level))
        module_logger.setLevel(
            {"NOTSET": logging.NOTSET,
             "DEBUG": logging.DEBUG,
             "INFO": logging.INFO,
             "WARNING": logging.WARNING,
             "ERROR": logging.ERROR,
             "CRITICAL": logging.CRITICAL}.get(
                logging_level.upper(), "WARNING"))

    # special formating of months used in some file structures #b lowercase i.e jan, feb, ...
    dstring="{0}/%Y/#b/%d".format(os.path.join(base_path))
    # standard formating of month %b uppercase i.e Jan, Feb
    standard_dstring="{0}/%Y/%b/%d".format(os.path.join(base_path))
    # time formating
    tstrf="%Y%m%d %H:%M:%S"

     
    auto_logg='default'
    df_tmp_list=[]
    start_run = intermediate_time = time.time()
    if frfile:
        if not fname:
            fname="sil-data.pik"
        data = read_pd_file(fname)

    else:
        # check basepath access and contents:
        if not os.path.isdir(base_path):
            raise Exception('SIL basepath not a directory: {}'.format(base_path))
        if not os.access(base_path, os.R_OK):
            raise Exception('SIL basepath not readable: {}'.format(base_path))
        if not os.listdir(base_path):
            raise Exception('SIL basepath is empty dir: {}'.format(base_path))

        # Creating a list of files to open
        dlist=gt.datepathlist(dstring,'0.8D',start,end, closed=None )
        
        ryear=int(start.strftime("%Y"))
        for ddir in dlist:
            module_logger.debug("Reading from directory {}:  ".format(ddir))
            
            # date from the string
            rdate = dt.strptime(ddir, standard_dstring)
            # file to read
            dfile = os.path.join(ddir,fread) 
            lyear=int(rdate.strftime("%Y"))
            # Printing out info on progress
            if lyear == ryear:
                module_logger.warning("------------ working on year {} ----------:".format(ryear))
                module_logger.warning("Reading files from:  {}:".format(os.path.join( "/", *ddir.split(os.sep)[:-2] )))

            # To return standard  output. bulleting data partly or all from automatic processing
            # Returning ['latitude', 'longitude', 'depth', 'MLW', 'Q', 'id', 'seismic_moment', "MW"]
            # MLW is ML if the event is from automatic processing.
            # MW = 2/3*log10(seismic_moment) - 6.03
            # MLW is replaced by MW if MLW > repl_mlw, (default not replace) 

            HAVE_FILE = True
            if fread == 'default':
                if aut:
                    if aut_per == "all":
                        tmp = read_automatic( ddir, aut=True, repl_mlw=repl_mlw, logger=auto_logg )

                    elif rdate > (end - timedelta(days = aut_per)):
                        tmp = read_automatic( ddir, aut=True, repl_mlw=repl_mlw, logger=auto_logg )

                    else:
                        tmp = read_automatic( ddir, aut=False, repl_mlw=repl_mlw, logger=auto_logg )

                else:
                    tmp = read_automatic( ddir, aut=False, repl_mlw=repl_mlw, logger=auto_logg )

            else:
                try:
                    if os.path.isfile(dfile):
                        tmp=read_sil_file(dfile)
                    else:
                        module_logger.info("File does not exist: {}".format(dfile))
                        HAVE_FILE = False

                except  IOError as e:
                    module_logger.info("While reading File {}:  ".format(dfile) + str(e), exc_info=True)
                    HAVE_FILE = False

            if HAVE_FILE:
                df_tmp_list.append(tmp)

            # Printing out info on progress

            if lyear == ryear:
                delta_time=time.time()- intermediate_time
                intermediate_time = delta_time + intermediate_time
                module_logger.warning("Total time working data from {0} is {1:.3f} s: ".format( ryear, delta_time ))
                ryear += 1
                #print(module_logger)


        data = pd.concat(df_tmp_list)
        module_logger.warning("Total time in for looping through all data: {0:.3f} s: ".format( time.time() - start_run ))
       
        #if data.empty:
        #    module_logger.exception("Empty DataFrame: {}:".format( data))
        #    raise ValueError
       
        
        if aut_per == "all" and fread == "default":
            module_logger.info( "using automatic events for all events not in events.fps" )
        elif fread == "default":
            module_logger.info( "Using automatic events for all events not in events.fps after {}:  ".format(end - timedelta(days = aut_per))) 
        else:   
            module_logger.info( "Reading from file {}:  ".format(dfile)) 

    # only returning subset of columns
    if data is not None and isinstance(data, pd.DataFrame) and not data.empty:
        if rcolumns == "default" or rcolumns == []: # Different options of column return
            if fread=="lib.mag":
                rcolumns=["latitude", "Dlatitude", "longitude", "Dlongitude", "depth", "Ddepth", "MLW", "ML"]

            elif fread=="events.fps":
                rcolumns=[ "latitude", "Dlatitude", "longitude", "Dlongitude", "depth", "Ddepth", "MLW", "seismic_moment"]
            
            elif fread=="cleanaut.mag":
                rcolumns=[ "latitude", "longitude", "depth",  "ML", "Q"]
            
            else:
                rcolumns=data.columns.to_list()

            module_logger.info( "Colums {} selected from file {}".format(rcolumns, fread) )

        else:
            if rcolumns == "all":
                rcolumns=data.columns.to_list()
                
            else:
                rcolumns=list(set(rcolumns) & set(data))
                module_logger.info( "Colums {} selected from file {}".format(rcolumns, fread) )



        if duplicate == False:
            data = data[~data.duplicated()]

        # in case of duplicate id
        if "Q" in data.columns and "id" in data.columns:
            data = removedubl(data,timetag=False)

           

        data = data[rcolumns]
        #data = data[start.strftime(tstrf):end.strftime(tstrf)]
        data = seism_subset(data, start=start, end=end,
                            **kwargs, dna=dna, logger=auto_logg)

        
        # Return cumulative moment 
        if cum_moment and  ('seismic_moment' in data) :
            data['cum_moment'] = data['seismic_moment'].cumsum()

        # For debugging: logging
        module_logger.info("Dataframe columns:\n" + str(data.columns) + "\n")
        module_logger.info("Input time period: ({}, {})".format(start, end))
        module_logger.info("dataframe First and Last lines:\n"  + str(data.iloc[[0,-1]]))
        module_logger.debug("Dataframe shape: {}".format( str(data.shape) )) 
        module_logger.debug("dataframe types:\n" + str(data.dtypes) + "\n" )

    else:
        module_logger.warning("dataframe is empty:\n"  + str(data) )
    
    module_logger.debug("dataframe File list:  " + str(dlist) )
    module_logger.debug("String to produse directory list:  " + dstring )

    module_logger.info("Time since for loop finished {0:.3f} s: ".format( time.time() - intermediate_time ))
    module_logger.info("Total time {0:.3f} s: ".format( time.time() - start_run ))

    return data


def read_pd_file(fn, filetype=None):
    """
    Read pandas dataframe saved as pickle or parquet file.

    This method is for convenience to read any of the two formats and any
    compression without having to specify the pandas read method.
    Method copy-pasted from shiver.u_io 2020-06-24 10:46 by tim.

    Parameters
    ----------
    fn : string
        Path to file, expected to be only pandas dataframe.
    filetype : string, optional
        Can specify if 'pickle' or 'parquet'. The default is None.

    Returns
    -------
    pandas.DataFrame
        Object which had been stored as file.
    """
    import pandas as pd
    pickle_opt = ['pickle', 'pkl', 'pik']
    parquet_opt = ['parquet', 'prq', 'pqt']
    ext_pkl_comp = ['.gz', '.bz2', '.xz']
    ext_prq_comp = ['.zst', '.gz', '.lz4', '.snp', '.lzo']
    ext_pkl = ['pickle', 'pkl', 'pik']
    ext_prq = ['parquet', 'prq', 'pqt']
    # if filetype specified by user:
    if filetype:
        if filetype.lower() in pickle_opt:
            return pd.read_pickle(fn)
        elif filetype.lower() in parquet_opt:
            return pd.read_parquet(fn)
        else:
            raise RuntimeError(
                "Given filetype '{}' unavailable.".format(filetype))
    fl = fn.lower()
    # if file extension matches common ones for (compressed) pickle/parquet:
    if any([fl.endswith(x) for x in ext_pkl_comp]):
        e2 = fl.split('.')[-2]
        if any([e2 == x for x in ext_pkl]):
            try:
                return pd.read_pickle(fn)
            except Exception as e:
                print('Warning: read as pickle (based on file-ext.) failed.')
                raise e
    if any([fl.endswith(x) for x in ext_prq_comp]):
        e2 = fl.split('.')[-2]
        if any([e2 == x for x in ext_prq]):
            try:
                return pd.read_parquet(fn)
            except Exception as e:
                print('Warning: read as parquet (based on file-ext.) failed.')
                raise e
    if any([fl.endswith(x) for x in ext_pkl]):
        try:
            return pd.read_pickle(fn)
        except Exception as e:
            print('Warning: read as pickle (based on file-ext.) failed.')
            raise e
    if any([fl.endswith(x) for x in ext_prq]):
        try:
            return pd.read_parquet(fn)
        except Exception as e:
            print('Warning: read as parquet (based on file-ext.) failed.')
            raise e
    # if no info given and file ext not typical, try both:
    try:
        return pd.read_pickle(fn)
    except:
        pass
    try:
        return pd.read_parquet(fn)
    except Exception as e:
        print('Warning: read as pickle and parquet failed.')
        raise e


##
# functions used for real time fixes of magnitude on bigger quakes
##

def read_station_loc(fileloc):
    """
    Read a net.dat and put into dataframe.

    Parameters
    ----------
    fileloc : str
        system location of file ex: /home/liljajo/Documents/net.dat

    Returns
    -------
    pandas dataframe
    """
    import pandas as pd

    columns = ["sta", "latitude", "longitude", "height"]
    col_dtypel = ['object', 'float64', 'float64', 'float64']
    col_with = [(0, 4), (4, 13), (13, 23), (23, 29)]
    col_dtype = dict(zip(columns, col_dtypel))
    tmp = pd.DataFrame(columns=columns)
    tmp = pd.read_fwf(fileloc, header=None, colspecs=col_with, dtype=col_dtype,
                      infer_datetime_format=True, names=columns)
    tmp = tmp.dropna()
    return tmp


def check_event_fit(location, SIL_time, PGV_time, PGV):
    """
    Find and compare arrival times of PGV to given criteria.

    Also filters for stations further than 230 km away, LE1 and ada.

    Parameters
    ----------
    location : list
        list of latitude and longitude of origin from SIL
    SIL_time: datetime
        datetime object of SIL origin time
    PGV_time: datetime
        datetime object from header of event file
    PGV: dataframe
        with index: "sta", columns: "fb", "lon", "lat", "time", "pgv"

    Returns
    -------
    True: boolean and PGV_fit: dataframe if enough sta fit within

    False: boolean and PGV_fit: dataframe if not enough sta fit
    """
    import pandas as pd
    from geopy import distance
    from datetime import datetime as dt
    from datetime import timedelta

    # add distances from SIL origin to PGV dataframe
    latitudes = PGV['lat'].tolist()
    longitudes = PGV['lon'].tolist()
    coordinates = list(map(lambda x, y: (x, y), latitudes, longitudes))
    PGV['distance'] = [distance.distance(location, x).km for x in coordinates]
    PGV_fit = PGV.copy()
    # compare PGV['time'] to SIL origin time
    PGV_fit['time'] = [PGV_time + timedelta(0, x) for x in PGV_fit['time']]
    i = 0
    j = 12
    fit = 0.68
    for index, row in PGV_fit.iterrows():
        if 64.55 <= location[0] <= 64.7 and -17.65 <= location[1] <= -17.1:
            j = 25
        t1 = SIL_time + timedelta(0, row.distance/7.3 - 2)
        t2 = SIL_time + timedelta(0, row.distance/1.9 + j)
        check = t1 < row.time < t2
        if check:
            i += 1

    if len(PGV_fit.index) != 0 and i >= 10 and i/len(PGV_fit.index) >= fit:
        PGV_fit['fit'] = '{}/{} ({:.0f}%) '.format(i, len(PGV_fit.index),
                                                   (i/len(PGV_fit.index))*100)
        print(str(i) + '/' + str(len(PGV_fit.index)), end=' -> ')
        return True, PGV_fit
    else:
        print(str(i) + '/' + str(len(PGV_fit.index)), end=' -> ')
        print('not enough PGV within limits', end=' -> ')
        return False, PGV_fit


def find_alertevent(event_id, sil_path="/net/granit/mnt/sdc1/sk2/",
                    pre_path="/net/hellir/mnt/sdc1/alert'",
                    eps=150, time=None, location=[], logger=__name__):
    """
    Find alerts that fit evb, check their fit.

    Additionally checks the event file pgv times against distance to origin if
    location, origin time and station list with coodinates are provided.

    Parameters
    ----------
    event_id : str
        SIL event id = path to evb|eve|ana files.
        Example: "/2020/jun/25/00:05:00/09:33:883"
    sil_path : str, optional
        Path to SIL top dir which contains the year dirs. The default is
        "/net/granit/mnt/sdc1/sk2/"
    pre_path : str, optional
        Path to local alertMap output dirs. The default is
        "/net/hellir/mnt/sdc1/alert"
    eps : int, optional
        Time tolerance in seconds for associating events from SIL and
        alertMap. The default is 30.
    time: datetime
        time of origin gotten from cleanaut.mag
        if not provided will result in no check of PGV times.
    location: list, optional
        should be a list of latitude and longitude of origin from evb file.
        if not provided will result in no check of PGV times.
    logger : str, optional
        Name of logger object. The default is __name__ (current method name).

    Returns
    -------
    PGV : pandas.DataFrame
        Has index = station code, columns = lon, lat, time, pgv, fb, distance,
        fit, event; for stations in AlertMap *.event file. if returned from
        check_event_fit otherwise is an empty dataframe.
    """
    import os
    import csv
    import glob

    from datetime import datetime as dt
    from datetime import timedelta
    import pandas as pd

    # read EVB file
    filename = os.path.join(sil_path, event_id + ".evb")
    EVB = read_evb(filename, logger="__name__")

    # read time in header of all event files from the day
    tmp_path = os.path.join(pre_path, event_id[:12])
    # (event_id[:4] + '.old') til að komast í .old möppur

    files = glob.glob(tmp_path+'*.event')
    fields = {}
    for f in files:
        with open(f, 'r') as infile:
            reader = csv.DictReader(infile)
            fields[reader.fieldnames[0].split()[0]] = reader.fieldnames[0].split()[5:9]

    # set time window to look fo events within
    eps = timedelta(seconds=eps)
    window_min = (dt.combine(dt.today(), EVB.time.min()) - eps).time()
    window_max = (dt.combine(dt.today(), EVB.time.max()) + eps).time()

    # search if the event fits into the time
    # if location and time are given check the PGV time fits  time from origin.
    for key, value in fields.items():
        t = '{}/{}/{} {}'.format(value[0], value[1], value[3], value[2])
        PGV_time = dt.strptime(t, "%b/%d/%Y %H:%M:%S")
        event_found = window_min < PGV_time.time() < window_max
        if event_found:
            file = os.path.join(tmp_path, key + ".event")
            PGV = read_alert(file)
            if location and time is not None:
                check, PGV_checked = check_event_fit(location, time, PGV_time,
                                                     PGV)
                if check:
                    print('event found for {} - event file {}'.format(event_id,
                                                                      key))
                    PGV_checked['event'] = key
                    return PGV_checked
            else:
                return PGV  # without location and time takes first event found

    print('no event found for {}'.format(event_id))
    return pd.DataFrame()  # return empty dataframe if no event found


def main():
    import logging
    import logging.config

    log_dict = { 
         'version': 1, 
         'disable_existing_loggers': False, 
         'formatters': { 
             'standard': { 
                 'format': '%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s' 
             }, 
         }, 
         'handlers': { 
             'default': { 
                 'level': 'WARNING', 
                 'formatter': 'standard', 
                 'class': 'logging.StreamHandler', 
             }, 
             'file_handler': { 
                 'level': 'INFO', 
                 'filename': '/tmp/mylogfile.log', 
                 'class': 'logging.FileHandler', 
                 'formatter': 'standard' 
             } 
         }, 
         'loggers': { 
             'default': { 
                 'handlers': ['default'], 
                 'level': 'WARNING', 
                 'propagate': True 
             }, 
             'debug': { 
                 'handlers': ['default'], 
                 'level': "DEBUG", 
                 'propagate': True  
      
             }, 
             'info': { 
                 'handlers': ['default'], 
                 'level': "INFO", 
                 'propagate': True  
      
             }, 
             'geo_dataread.sil_read': {  
             'handlers': ['default'],  
             'level': "WARNING",  
             'propagate': True  
             }, 
              
         } 
     }                  
    
    logging.config.dictConfig(log_dict)

if __name__ == '__main__':
    main()
