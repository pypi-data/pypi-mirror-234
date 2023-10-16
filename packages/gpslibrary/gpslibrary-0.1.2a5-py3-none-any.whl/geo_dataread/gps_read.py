"""
This module contains functions for reading and returning GPS data

The module containes the following functions 
---------------
openGlobkTimes(STA, Dir=None)
dPeriod(yearf, data, Ddata, startyear=None, endyear=None)
iprep(yearf, data, Ddata, uncert=20.0)
detrend(yearf, data, fitfunc, errfunc, STA)
vshift(yearf, data, Ddata, uncert=20.0, refdate=None, Period=5):
filt_outl(yearf,data,Ddata,pb,errfunc,outlier)
gamittoNEU(sta):
---------------

"""

import numpy as np
import logging

#
# time series filtering
#


def line(x, p0, p1):
    return p0 + p1 * x


def lineperiodic(x, p0, p1, p2, p3, p4, p5):
    """
    linear function with a periodic supperimposed
    """

    import numpy as np

    return (
        p0
        + p1 * x
        + p2 * np.cos(2 * np.pi * x)
        + p3 * np.sin(2 * np.pi * x)
        + p4 * np.cos(4 * np.pi * x)
        + p5 * np.sin(4 * np.pi * x)
    )


def periodic(x, p0, p1, p2, p3, p4, p5):
    """
    Periodic function
    """

    import numpy as np

    return (
        p2 * np.cos(2 * np.pi * x)
        + p3 * np.sin(2 * np.pi * x)
        + p4 * np.cos(4 * np.pi * x)
        + p5 * np.sin(4 * np.pi * x)
    )


def xf(x, p0, p1, p2, tau=4.8):
    import numpy as np

    return p0 + p1 * x + p2 * np.exp(-tau * x)


def expxf(x, p0, p1, p2, p3):
    import numpy as np

    return p0 + p1 * x + p2 * np.exp(-p3 * x)


def expf(x, p0, p1, p2):
    import numpy as np

    return p0 + p1 * np.exp(-p2 * x)


def gpsvelo_df():
    """
    dataframe for pygmt velo with three  extra columns
    for date, period and bolian for vertical data
    """
    import pandas as pd

    gpsvelo = pd.DataFrame(
        columns=[
            "longitude",
            "latitude",
            "east_velo",
            "north_velo",
            "east_sigma",
            "north_sigma",
            "coorelation_EN",
            "Station",
            "date",
            "period",
            "vertical",
        ],
    )

    return gpsvelo


def gpsvelo(sta, ll, vel, vertical=False, vfile=None, pheader=False):
    """
    Return gps velocities gmt velo
    """

    gpsvelo = "{0:5.6f} {1:5.6f}\t{2:7.2f} {5:7.2f}\t{3:7.2f} {6:7.2f}\t{4:7.2f} {7:7.2f}\t\t{8:s}".format(
        ll[1], ll[0], vel[0], vel[1], vel[2], vel[3], vel[4], vel[5], sta
    )


def getDetrFit(
    STA,
    useSTA=None,
    useFIT=None,
    onlyPeriodic=False,
    detrFile="detrend_itrf2008.csv",
    logging_level=logging.WARNING,
):
    """ """

    import logging
    import numpy as np
    import pandas as pd

    import cparser as cp

    # Handling logging
    logging.basicConfig(
        format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
        level=logging_level,
    )

    logging.getLogger().setLevel(logging_level)
    module_logger = logging.getLogger()

    North = ["Nrate", "Nacos", "Nasin", "Nscos", "Nssin"]
    East = ["Erate", "Eacos", "Easin", "Escos", "Essin"]
    Up = ["Urate", "Uacos", "Uasin", "Uscos", "Ussin"]
    Info = ["Sitename", "Starttime", "Endtime", "UseSTA", "Fit"]
    columns = North + East + Up + Info
    sta_name = cp.Parser().getStationInfo(STA)["station"]["name"]
    data = [[np.nan] * 15 + [sta_name, np.nan, np.nan, np.nan, np.nan]]
    table = pd.DataFrame(data, index=[STA], columns=columns)

    try:
        table = pd.read_csv(detrFile, index_col="STA")
    except pd.errors.EmptyDataError:
        module_logger.warn("{} does not contain any data".format(detrFile))
    except FileNotFoundError:
        module_logger.warn("Detrend file not found")

    module_logger.info("Existing detrend constant table:\n{}".format(table))
    try:
        const = pd.DataFrame(index=[STA], columns=columns)
        const.loc[STA] = tuple(table.loc[STA].values)
    except KeyError:
        module_logger.warn("{} not in table making an empty row".format(STA))
        const = pd.DataFrame(data, index=[STA], columns=table.columns)

    if useSTA:
        module_logger.warn(
            "Setting {0} {1} constants as {1} parameters for {2}".format(
                useSTA, useFIT, STA
            )
        )
        module_logger.info("current {} constants are:\n {} ".format(STA, const))

        const.loc[STA, ["UseSTA", "Fit"]] = useSTA, useFIT
        if useFIT == "periodic":
            const.loc[STA, North[1:] + East[1:] + Up[1:]] = table.loc[
                useSTA, North[1:] + East[1:] + Up[1:]
            ]
        elif useFIT == "lineperiodic":
            const.loc[STA, North + East + Up] = table.loc[
                useSTA, North + East + Up
            ]
        elif useFIT == "line":
            const.loc[STA, North[:1] + East[:1] + Up[:1]] = table.loc[
                useSTA, North[:1] + East[:1] + Up[:1]
            ]

        module_logger.info("New parameters for {} are:\n {}".format(STA, const))

    if onlyPeriodic is True:
        const["Nrate"] = const["Erate"] = const["Urate"] = 0

    return const


def convconst(const, pb=None):
    """
    convert detrend constants from pandas dataframe to list of the form
    [[], [], []] for optimize.curv_fit
    """

    import numpy as np

    North = ["Nrate", "Nacos", "Nasin", "Nscos", "Nssin"]
    East = ["Erate", "Eacos", "Easin", "Escos", "Essin"]
    Up = ["Urate", "Uacos", "Uasin", "Uscos", "Ussin"]
    if pb:
        # const = pd.DataFrame(data, index=[STA], columns=table.columns)
        if len(pb[0]) == 2:
            pb = [np.concatenate((pb[i], np.zeros(4))) for i in range(3)]

        stat = const.index.tolist()[0]
        for i, dimention in zip(range(3), [North, East, Up]):
            const.loc[stat, dimention] = list(pb[i][1:])

        return const

    else:
        if const[North].isna().sum(axis=1).values == 5:
            p0 = [None, None, None]
        else:
            p0 = [[], [], []]
            p0[0] = [0] + const[North].values.tolist()[0]
            p0[1] = [0] + const[East].values.tolist()[0]
            p0[2] = [0] + const[Up].values.tolist()[0]

            p0 = np.nan_to_num(p0)

        return p0


def save_detrend_const(const, detrFile="detrend_itrf2008.csv"):
    """
    save a constants for detrending GPS stations
    """
    import pandas as pd
    from pathlib import Path

    North = ["Nrate", "Nacos", "Nasin", "Nscos", "Nssin"]
    East = ["Erate", "Eacos", "Easin", "Escos", "Essin"]
    Up = ["Urate", "Uacos", "Uasin", "Uscos", "Ussin"]
    Info = ["Sitename", "Starttime", "Endtime", "UseSTA", "Fit"]
    columns = North + East + Up + Info

    stationlist = const.index.values
    path = Path(Path.cwd(), detrFile)
    if not path.is_file():
        open(path, "w").close()

    try:
        table = pd.read_csv(detrFile, index_col="STA")
    except pd.errors.EmptyDataError:
        table = pd.DataFrame(index=["STA"], columns=columns)

    if all(table.isnull().all(1)):
        print("No data in file")
        const.to_csv(detrFile, mode="w", header=True, index_label="STA")

        return
    else:
        for stat in stationlist:
            if stat in table.index:
                print("Station {} already in table updating".format(stat))
                table.loc[stat, :] = const.loc[stat]
                print("Saving the new table")
                table.to_csv(detrFile, mode="w", header=True, index_label="STA")
            else:
                print("stations {} are not in detrend file, adding it".format(stat))
                table.loc[stat, :] = const.loc[stat]
                table.to_csv(detrFile, mode="w", header=True, index_label="STA")

        return


def fitdataframe(func, df, p0=[None, None, None]):
    """ """
    from scipy import optimize

    x = df["yearf"].to_numpy()
    y = df[["north", "east", "up"]].to_numpy().T
    yD = df[["Dnorth", "Deast", "Dup"]].to_numpy().T

    return fittimes(func, x, y, yD, p0=p0)


def fittimes(func, x, y, yD=[None, None, None], p0=[None, None, None]):
    from scipy import optimize

    pb = [[], [], []]
    pcov = [[], [], []]

    for i in range(3):
        pb[i], pcov[i] = optimize.curve_fit(
            func, x, y[i], p0=p0[i], sigma=yD[i], maxfev=100000
        )

    return pb, pcov


# routines to extract and save coordiantes and time series from gamit


def gamittooneuf(sta, outFile, mm=True, ref="plate", dstring=None, outformat=True):
    """
    extract Gamit time series from standard format to one file formated time string
    input:
        sta: station four letter short name
        outFile: file object
        mm: boolean True return data in mm, else in m
        ref: subtract plate velocity from the time series.
        dstring: format of the time string (e.g dstring)="%Y%m%d-%H%M%S"), defaults to decimal year (yyyy.yyyy)
        outformat: not finished but determains the output order of the data into the file
    """
    # "%Y/%m/%d 12:00:00.000"

    NEUdata = gamittoNEU(sta, mm=mm, ref=ref, dstring=dstring)

    gamittoFile(NEUdata, outFile, mm=mm, ref=ref, dstring=dstring, outformat=outformat)


def gamittoFile(NEUdata, outFile, mm=True, ref="plate", dstring=None, outformat=True):
    """ """

    if dstring == "yearf":
        timef = "{0: 8.4f}\t"
        timeh = "#\"yyyy.dddd'     "
    else:
        timef = " {0:s}\t"
        timeh = "#yyyy/mm/dd HH:MM:SS.SSS          "

    if mm:
        if outformat:
            header = timeh + "dN[mm] DN[mm]\tdE[mm] DE[mm]\tdU[mm]  DU[mm]"
            formatstr = (
                timef + "{1: 7.2f} {4: 7.2f}\t{2: 7.2f} {5: 7.2f}\t{3: 7.2f} {6: 7.2f}"
            )
        else:
            header = timeh + "dN[mm]  dE[mm] dU[mm]\t\t  DN[mm]  DE[mm]  DU[mm]"
            formatstr = (
                timef
                + "{1: 7.2f} {2: 7.2f} {3: 7.2f}\t\t{4: 7.2f} {5: 7.2f}\t{6: 7.2f}"
            )
    else:
        if outformat:
            header = timeh + "dN[m] DN[m]\tdE[m] DE[m]\tdU[m]  DU[m]"
            formatstr = (
                timef + "{1: 7.5f} {4: 7.5f}\t{2: 7.5f} {5: 7.5f}\t{3: 7.5f} {6: 7.5f}"
            )
        else:
            header = timeh + "dN[m]    dE[m]    dU[m]          DN[m]   DE[m]    DU[m]"
            formatstr = (
                timef + "{1: 7.5f} {2: 7.5f} {3: 7.5f}\t{4: 7.5f} {5: 7.5f} {6: 7.5f}"
            )

    print(header, file=outFile)  # ,

    for x in NEUdata:
        print(
            formatstr.format(
                x["yearf"],
                x["data[0]"],
                x["data[1]"],
                x["data[2]"],
                x["Ddata[0]"],
                x["Ddata[1]"],
                x["Ddata[2]"],
            ),
            file=outFile,
        )


def savedisp(dataDict, fname=None, header=""):
    """ """
    from collections import OrderedDict

    valtype = type(list(dataDict.values())[0])

    dataDict = OrderedDict(sorted(dataDict.items()))

    datavalues = list(dataDict.values())
    if (valtype is list) or (valtype is np.ndarray):
        fmt = "% 3.8f\t% 2.8f\t% 2.8f\t%s"
        ab = np.zeros(
            len(dataDict.keys()),
            dtype=[
                ("var1", "float"),
                ("var2", "float"),
                ("var3", "float"),
                ("var4", "a4"),
            ],
        )
        ab["var1"] = np.squeeze(datavalues)[:, 0]
        ab["var2"] = np.squeeze(datavalues)[:, 1]
        ab["var3"] = np.squeeze(datavalues)[:, 2]
        ab["var4"] = [str(item) for item in dataDict.keys()]
    if valtype is tuple:
        fmt = "% 3.8f\t% 2.8f\t% 2.8f\t%2.8f\t%2.8f\t%s"
        ab = np.zeros(
            len(dataDict.keys()),
            dtype=[
                ("var1", "float"),
                ("var2", "float"),
                ("var3", "float"),
                ("var4", "float"),
                ("var5", "float"),
                ("var6", "a4"),
            ],
        )
        ab["var1"] = np.squeeze(list(zip(*datavalues[:]))[0])[:, 0]
        ab["var2"] = np.squeeze(list(zip(*datavalues[:]))[0])[:, 1]
        ab["var3"] = np.squeeze(list(zip(*datavalues[:]))[1])[:, 0]
        ab["var4"] = np.squeeze(list(zip(*datavalues[:]))[1])[:, 1]
        ab["var5"] = np.squeeze(list(zip(*datavalues[:]))[1])[:, 2]
        ab["var6"] = [str(item) for item in dataDict.keys()]

    if fname:
        np.savetxt(fname, ab, fmt=fmt, header=header)
    return ab


def extractfromGamitBakf(cfile, stations):
    """ """
    import re

    slines = []

    site = re.compile(stations)
    tim = re.compile("Solution refers to", re.IGNORECASE)
    f = open(cfile, "r")

    for line in f:
        if site.search(line):  # or tim.search(line):
            slines.append(line.rstrip())

    return slines


def openGlobkTimes(STA, Dir=None, tType="TOT"):
    """
    Import data from Globk time series files into a numpy arrays

    Dir is the directory containing the time series if left blank the default path will will be the path
    defined in config file postprossesing.cfg, totPath

    input:
        STA, Station four letter short name in captial letters
        Dir, optional alternative location of the GAMIT time series data.

    output:
         yearf, data, Ddata
            yearf: is array with time  (usually) in fractional year format (i.e. 2014.62328)
            data:  three arrays containing GPS data in north,east, up
            Ddata: respective uncertainty values

    """

    import os
    import numpy as np
    import datetime as dt

    # custom modules
    import cparser as cp
    from gtimes.timefunc import shifTime, TimetoYearf

    # loading the data-------------------

    if Dir is None:
        Dir = cp.Parser().getPostprocessConfig()["totPath"]
    else:
        # print( os.path.isdir(Dir) )
        # check if the path given as argument indeed exists
        pass

    # constructing the full path filenames and parsing parameters

    # filepre = "mb_%s_TOT.dat" % STA

    filepre = "mb_{0:s}_{1:s}.dat".format(STA, tType)
    if os.path.isfile(os.path.join(Dir, filepre + "1")):
        pass
    else:
        filepre = "mb_{0:s}_{1:s}.dat".format(STA, "TOT")

    Datafile1 = os.path.join(Dir, filepre + "1")
    Datafile2 = os.path.join(Dir, filepre + "2")
    Datafile3 = os.path.join(Dir, filepre + "3")

    # loading the data for files and storing it in arrays
    yearf, d1, D1 = np.loadtxt(
        Datafile1, unpack=True, skiprows=3, converters={1: __converter, 2: __converter}
    )
    d2, D2 = np.loadtxt(
        Datafile2,
        usecols=(1, 2),
        unpack=True,
        skiprows=3,
        converters={1: __converter, 2: __converter},
    )
    d3, D3 = np.loadtxt(
        Datafile3,
        usecols=(1, 2),
        unpack=True,
        skiprows=3,
        converters={1: __converter, 2: __converter},
    )
    data = np.vstack([d1, d2, d3])
    Ddata = np.vstack([D1, D2, D3])

    if tType == "08h":
        shift8h = dt.timedelta(**shifTime("H8"))
        yearf = np.array(
            [
                TimetoYearf(*(item + shift8h).timetuple()[:6])
                for item in toDateTime(yearf)
            ]
        )

    return yearf, data, Ddata


def open3DataFiles(STA, Dir=None, comp=["-N", "-E", "-U"]):
    """
    open data contained in 3 files one file for each component E, N and U
    """

    import os
    import pandas as pd

    if Dir is None:
        Dir = os.getcwd()

    compdict = {}
    compdict[comp[0]] = ["north", "Dnorth"]
    compdict[comp[1]] = ["east", "Deast"]
    compdict[comp[2]] = ["up", "Dup"]
    components = {"north": None, "east": None, "up": None}

    for item in compdict.keys():
        dfile = "{0}{1}".format(STA, item)
        components[compdict[item][0]] = pd.read_csv(
            dfile, sep=r'\s+', index_col=0, header=None, names=compdict[item]
        )

    # return reduce(lambda x, y: pd.merge(x, y, on=inpd.concat([df1, df2, df3, ...], axis=1)dex_col), components.values() )
    columnreorder = ["north", "east", "up", "Dnorth", "Deast", "Dup"]
    data = pd.concat(components.values(), axis=1)[columnreorder]
    data.set_index(pd.DatetimeIndex(toDateTime(data.index)), inplace=True)
    data.index = data.index.round("1h")

    return data


def convGlobktopandas(yearf, data, Ddata):
    """
    input: yearf, data, Data from openGlobkTimes
    output: pandas dataframe


    reads in time series data from openGlobkTimes and returns a dataframe with the structure
    Index [datetime], north, east, up, Dnorth, Deast, Dup, yearf
    """

    import pandas as pd
    from collections import OrderedDict

    # reduce(lambda x, y: pd.merge(x, y, on = 'Date'), dfList)
    names = ["north", "east", "up", "Dnorth", "Deast", "Dup", "yearf"]

    # !!!!! from_item depricated will remove
    # data = pd.DataFrame.from_items(zip(names[:3],data))
    # data = data.join( pd.DataFrame.from_items(zip(names[3:],Ddata) ) )
    # Using from_dict instead
    data = pd.DataFrame.from_dict(OrderedDict(zip(names[:3], data)))
    data = data.join(pd.DataFrame.from_dict(OrderedDict(zip(names[3:], Ddata))))
    data["yearf"] = yearf
    data.set_index(pd.DatetimeIndex(toDateTime(yearf)), inplace=True)
    data.index = data.index.round("1h")

    return data


def compGlobkTimes(stalist="any", dirConFilePath=None, freq=None):
    """
    joins old and new mb_ time series files
    """
    import glob
    import sys
    import shutil
    import os

    import cparser as cp

    if dirConFilePath:  # for custom file
        Dirs = parsedir(dirConFilePath)
    else:
        Dirs = cp.Parser().getPostprocessConfig()
        print(Dirs)

    PrePath = Dirs["prePath"]
    RapPath = Dirs["rapPath"]
    TotPath = Dirs["totPath"]

    if freq == "TOT" or freq is None:
        freq = "TOT"
    else:
        PrePath = PrePath + "_%s" % (freq)
        RapPath = RapPath + "_%s" % (freq)

    if stalist == "any":
        FilePreL = os.path.join(PrePath, "mb_*.dat?")
        FileRapL = os.path.join(RapPath, "mb_*.dat?")

        List = glob.glob(FilePreL) + glob.glob(FileRapL)

        # listing all stations in  the Rap and Pre dir
        stalist = sorted(set([item[-13:-9] for item in List]))

    for STA in stalist:
        FilePre = "mb_%s_?PS.dat" % STA
        OutFilePre = "mb_%s_GPS.dat" % STA
        GPS20PS = "mb_%s_0PS.dat" % STA

        for axes in range(1, 4):
            FilePreR = os.path.join(PrePath, FilePre + "%s" % (axes,))
            FileRapR = os.path.join(RapPath, FilePre + "%s" % (axes,))

            # graping the list for files for for that station
            PreFileL = glob.glob(FilePreR)  # listing files in the pre dir
            RapFileL = glob.glob(FileRapR)  # listing files in th Rap dir

            #  Sorting the file lists
            PreFileL.sort()
            if len(PreFileL) > 1:
                PreFileL.insert(0, PreFileL.pop(-1))
            RapFileL.sort()
            if len(RapFileL) > 1:
                RapFileL.insert(0, RapFileL.pop(-1))

            TotFile = os.path.join(TotPath, "mb_%s_%s.dat%s" % (STA, freq, axes))
            print("Concating all the %s data to %s" % (STA, TotFile))
            if os.path.exists(TotFile):
                os.remove(TotFile)
            outf = open(TotFile, "a")
            for fil in PreFileL:
                print("Processing file %s " % fil, file=sys.stderr)
                f = open(fil)
                f.seek(61)
                shutil.copyfileobj(f, outf)
                f.close()
            outf.close()

            preexist = os.stat(TotFile).st_size != 0
            if preexist:
                outf = open(TotFile, "r")
                lastline = outf.readlines()[-1]
                lastline = lastline.split()
                outf.close()

            outf = open(TotFile, "a")
            for file in RapFileL:
                formatstr = "Processing file {0:s} ".format(file)
                print(formatstr, file=sys.stderr)
                rapfile = open(file, "r")
                rapfile.seek(61)
                lines = rapfile.readlines()
                if preexist:
                    lines = "".join(
                        [line for line in lines if line.split()[0] > lastline[0]]
                    )
                else:
                    lines = "".join([line for line in lines])

            outf.close()


def TieTimes(sta1, sta2, dirConFilePath=None, freq=None, tie=[None, None, None]):
    """
    joins old and new mb_ time series files
    """
    import glob
    import sys
    import shutil

    import cparser as cp

    if dirConFilePath:  # for custom file
        Dirs = parsedir(dirConFilePath)
    else:
        Dirs = cp.Parser().getPostprocessConfig()

    PrePath = Dirs["prePath"]
    RapPath = Dirs["rapPath"]
    TotPath = Dirs["totPath"]

    if freq == "TOT" or freq is None:
        freq = "TOT"
    else:
        PrePath = PrePath + "_%s" % (freq)
        RapPath = RapPath + "_%s" % (freq)

    if stalist == "any":
        FilePreL = os.path.join(PrePath, "mb_*.dat?")
        FileRapL = os.path.join(RapPath, "mb_*.dat?")

        List = glob.glob(FilePreL) + glob.glob(FileRapL)

        # listing all stations in  the Rap and Pre dir
        stalist = sorted(set([item[-13:-9] for item in List]))

    for STA in stalist:
        FilePre = "mb_%s_?PS.dat" % STA
        OutFilePre = "mb_%s_GPS.dat" % STA
        GPS20PS = "mb_%s_0PS.dat" % STA

        for axes in range(1, 4):
            FilePreR = os.path.join(PrePath, FilePre + "%s" % (axes,))
            FileRapR = os.path.join(RapPath, FilePre + "%s" % (axes,))

            # graping the list for files for for that station
            PreFileL = glob.glob(FilePreR)  # listing files in the pre dir
            RapFileL = glob.glob(FileRapR)  # listing files in th Rap dir

            #  Sorting the file lists
            PreFileL.sort()
            if len(PreFileL) > 1:
                PreFileL.insert(0, PreFileL.pop(-1))
            RapFileL.sort()
            if len(RapFileL) > 1:
                RapFileL.insert(0, RapFileL.pop(-1))

            TotFile = os.path.join(TotPath, "mb_%s_%s.dat%s" % (STA, freq, axes))
            print("Concating all the %s data to %s" % (STA, TotFile))
            if os.path.exists(TotFile):
                os.remove(TotFile)
            outf = open(TotFile, "a")
            for fil in PreFileL:
                print("Processing file %s " % fil, file=sys.stderr)
                f = open(fil)
                f.seek(61)
                shutil.copyfileobj(f, outf)
                f.close()
            outf.close()

            preexist = os.stat(TotFile).st_size != 0
            if preexist:
                outf = open(TotFile, "r")
                lastline = outf.readlines()[-1]
                lastline = lastline.split()
                outf.close()

            outf = open(TotFile, "a")
            for file in RapFileL:
                formatstr = "Processing file {0:s} ".format(file)
                print(formatstr, file=sys.stderr)
                rapfile = open(file, "r")
                rapfile.seek(61)
                lines = rapfile.readlines()
                if preexist:
                    lines = "".join(
                        [line for line in lines if line.split()[0] > lastline[0]]
                    )
                else:
                    lines = "".join([line for line in lines])

                outf.write(lines)
                rapfile.close()

            outf.close()


def TieTimes(sta1, sta2, dirConFilePath=None, freq=None, tie=[None, None, None]):
    """
    joins old and new mb_ time series files
    """
    import glob
    import sys
    import shutil

    from pandas import read_table
    import pandas as pd

    import cparser as cp

    if dirConFilePath:  # for custom file
        Dirs = parsedir(dirConFilePath)
    else:
        Dirs = cp.Parser().getPostprocessConfig()

    # PrePath = Dirs['prePath']
    # RapPath = Dirs['rapPath']
    TieFile = Dirs["tiefile"]
    TotPath = Dirs["totPath"]

    if freq == "TOT" or freq is None:
        freq = "TOT"
    else:
        PrePath = PrePath + "_%s" % (freq)
        RapPath = RapPath + "_%s" % (freq)

    print(TieFile)

    dtype = [
        ("North", "<f8"),
        ("East", "<f8"),
        ("Up", "<f8"),
        ("sta1", "|S5"),
        ("sta2", "|S5"),
    ]

    const = np.genfromtxt(TieFile, dtype=dtype)
    const = [i for i in const if i[3] == sta1 and i[4] == sta2]

    for axes in range(1, 4):
        TotFile1 = os.path.join(TotPath, "mb_%s_%s.dat%s" % (sta1, freq, axes))
        TotFile2 = os.path.join(TotPath, "mb_%s_%s.dat%s" % (sta2, freq, axes))
        print("Concating all the %s data to %s" % (sta1, TotFile2))
        # outf = open(TotFile, 'r')
        data1 = read_table(
            TotFile1, sep=r'\s+', header=None, index_col=0, names=["disp", "uncert"]
        )
        data2 = pd.read_csv(
            TotFile2, sep=r'\s+', header=None, index_col=0, names=["disp", "uncert"]
        )
        print(const[0][axes - 1])
        data2["disp"] -= const[0][axes - 1] / 1000
        data = pd.concat([data1, data2])

        outfile = os.path.join(TotPath, "mb_%s_%s.dat%s" % (sta2, "JON", axes))
        data.to_csv(outfile, sep="\t", index=True, header=False)


fitfuncl = lambda p, x: p[0] * x + p[1]
errfuncl = lambda p, x, y: fitfuncl(p, x) - y  # Distance to the target function
fitfunc = (
    lambda p, x: p[0] * x
    + p[1] * np.cos(2 * np.pi * x)
    + p[2] * np.sin(2 * np.pi * x)
    + p[3] * np.cos(4 * np.pi * x)
    + p[4] * np.sin(4 * np.pi * x)
    + p[5]
)
errfunc = lambda p, x, y: fitfunc(p, x) - y  # Distance to the target function


def fitline(yearf, data, STA):
    """
    fit a line through data
    """

    from scipy import optimize
    import numpy as np

    dtype = [
        ("Nrate", "<f8"),
        ("Erate", "<f8"),
        ("Urate", "<f8"),
        ("Nacos", "<f8"),
        ("Nasin", "<f8"),
        ("Eacos", "<f8"),
        ("Easin", "<f8"),
        ("Uacos", "<f8"),
        ("Uasin", "<f8"),
        ("Nscos", "<f8"),
        ("Nssin", "<f8"),
        ("Escos", "<f8"),
        ("Essin", "<f8"),
        ("Uscos", "<f8"),
        ("Ussin", "<f8"),
        ("shortname", "|S5"),
        ("name", "|S20"),
    ]

    const = np.genfromtxt("itrf08det", dtype=dtype)
    const = [i for i in const if i[15] == STA]

    pN = [const[0][0]]
    pE = [const[0][1]]
    pU = [const[0][2]]
    pN = [-1 * i for i in pN]
    pE = [-1 * i for i in pE]
    pU = [-1 * i for i in pU]
    # pN.append(0)
    # pE.append(0)
    # pU.append(0)

    # print "pN: %s" % p
    # print "pE: %s" % pE
    # print "pU: %s" % pU

    pb = [[0, 0], [0, 0], [0, 0]]

    # pb[0], success = optimize.leastsq(errfunc, pN[:], args=(yearf-yearf[0], data[0]))
    # pb[1], success = optimize.leastsq(errfunc, pE[:], args=(yearf-yearf[0], data[1]))
    # pb[2], success = optimize.leastsq(errfunc, pU[:], args=(yearf-yearf[0], data[2]))
    pb[0], success = optimize.leastsq(errfuncl, pb[0], args=(yearf, data[0]))
    pb[1], success = optimize.leastsq(errfuncl, pb[1], args=(yearf, data[1]))
    pb[2], success = optimize.leastsq(errfuncl, pb[2], args=(yearf, data[2]))

    return pN, pE, pU, pb


def pvel(pl, pcov):
    """ """
    vunc = [None, None, None]
    vel = [None, None, None]

    for i in range(3):
        vel[i] = pl[i][1]
        vunc[i] = np.sqrt(np.diag(pcov[i]))[1]
        # print("{0:0.2f} {1:0.2f}".format( pl[i][1],vunc[i]) )

    return vel, vunc


def printvelocity(sta, ll, vel, vfile, pheader=False):
    """ """
    import os

    header = (
        "#lon       lat\t\t   N[mm]   DN[mm]  E[mm]  DE[mm]  U[mm]  DU[mm]\t\tStation"
    )

    if pheader is True:
        print(header, file=vfile)

    gpsvelo = "{0:5.6f} {1:5.6f}\t{2:7.2f} {5:7.2f}\t{3:7.2f} {6:7.2f}\t{4:7.2f} {7:7.2f}\t\t{8:s}".format(
        ll[1], ll[0], vel[0], vel[1], vel[2], vel[3], vel[4], vel[5], sta
    )

    print(gpsvelo, file=vfile)

    return gpsvelo


def detrend(
    x,
    y,
    Dy=None,
    fitfunc=lineperiodic,
    p=None,
    pcov=None,
    STA=None,
    onlyPeriodic=True,
    zref=False,
):
    """
    Returning detrend parameters very preliminary construction
    """

    import numpy as np

    # import dread.gread as gtf
    import geo_dataread.gps_read as gdrgps

    if Dy is None:
        Dy = np.ones(y.shape)

    # Handling parameters
    if p is not None:
        pass
    else:
        if STA:
            const = getDetrFit(STA, onlyPeriodic=onlyPeriodic)
            p0 = convconst(const)
        else:
            p0 = [None, None, None]

        p, pcov = fittimes(fitfunc, x, y, Dy, p0=p0)

    for i in range(3):
        y[i] = y[i] - fitfunc(x, *p[i])

    if zref:
        _, y, _ = gdrgps.vshift(x, y, Dy, uncert=20.0, refdate=None, Period=5)

    return y


def dPeriod(yearf, data, Ddata, startyear=None, endyear=None):
    """
    update( dict( [ [ line.split(',')[0], line.split(',')[1:] ] for line in args.eventf.read().splitlines() ] ) )

    returns a subperiod of input data (default behaviour: do nothing)

    Input:
        yearf: time array
        data: data array
        Ddata: same form as data
        startyear: default=None
        endyear: default=None

    Output:
        returns yearf, data, Data within the period defined by startyear and endyear

    """
    if startyear:
        index = np.where(yearf <= startyear - 0.001)
        yearf = np.delete(yearf, index)
        data = np.delete(data, index, 1)
        Ddata = np.delete(Ddata, index, 1)

    if endyear:
        index = np.where(yearf >= endyear + 0.001)
        yearf = np.delete(yearf, index)
        data = np.delete(data, index, 1)
        Ddata = np.delete(Ddata, index, 1)

    return yearf, data, Ddata


def vshift(yearf, data, Ddata, uncert=20.0, refdate=None, Period=5, offset=None):
    """
    Shifts time series data by the average value of the interval defined by
    reday and the number of days specified ()
    """

    from gtimes.timefunc import currYearfDate

    # Filtering a little, removing big outliers
    with np.errstate(invalid="ignore"):
        filt = Ddata < uncert
    filt = np.logical_and(np.logical_and(filt[0, :], filt[1, :]), filt[2, :])

    yearf = yearf[filt]
    data = np.reshape(data[np.array([filt, filt, filt])], (3, -1))
    Ddata = np.reshape(Ddata[np.array([filt, filt, filt])], (3, -1))

    if data.any():
        if not (offset is None):
            pass
        else:
            offset = estimate_offset(yearf, data, Ddata, refdate=refdate, Period=Period)

    data = np.array([data[i, :] - offset[i] for i in range(3)])

    return yearf, data, Ddata, offset


def estimate_offset(yearf, data, Ddata, refdate=None, Period=5):
    """
    Estimating offset of a time series at a reference (refdate) point for a given interval (Period)
    defaults at 5 days at the start of the time series
    """
    # averaging the first period days
    if refdate:
        startdate = currYearfDate(0, refdate)
        enddate = currYearfDate(Period, refdate)
        if Period < 0:
            tmpyearf, tmpdata, tmpDdata = dPeriod(
                yearf, data, Ddata, enddate, startdate
            )
        else:
            tmpyearf, tmpdata, tmpDdata = dPeriod(
                yearf, data, Ddata, startdate, enddate
            )

        if tmpdata.any():
            # if there are any data from this period
            offset = np.average(tmpdata[0:3, :], 1, weights=1 / tmpDdata[0:3, :])
        else:
            # We need to extrapolate
            # þarf að díla við þetta með því að módelera.
            offset = np.average(data[0:3, 0:j], 1, weights=1 / Ddata[0:3, 0:7])
    else:
        offset = np.average(data[0:3, 0:Period], 1, weights=1 / Ddata[0:3, 0:Period])

    return offset


def iprep(yearf, data, Ddata, uncert=20.0, offset=None):
    """
    Wrapper for vshift intendet for initializing the time series.
    converts to mm and initializes the start of the time series to zero
    """

    # converting to mm
    data *= 1000
    Ddata *= 1000
    return vshift(yearf, data, Ddata, uncert=uncert, offset=offset)


def filt_outl(yearf, data, Ddata, pb, errfunc, outlier):
    # Removing big outliers
    for i in range(3):
        index = np.where(abs(errfunc(pb[i], yearf - yearf[0], data[i])) > outlier[i])
        yearf = np.delete(yearf, index)
        data = np.delete(data, index, 1)
        Ddata = np.delete(Ddata, index, 1)

    return yearf, data, Ddata


def gamittoNEU(sta, mm=False, ref="plate", dstring=None):
    """
    convert a gamit time series to a single np.array with readable time tag
    """

    import geofunc.geofunc as gf

    yearf, data, Ddata = openGlobkTimes(sta)
    yearf, data, Ddata, _ = vshift(
        yearf, data, Ddata, uncert=1.1, refdate=None, Period=5, offset=None
    )

    # remove plata velocity
    if ref == "plate":
        plateVel = gf.plateVelo([sta])
        data[0, :] = data[0, :] - plateVel[0, 1] * (yearf - yearf[0])
        data[1, :] = data[1, :] - plateVel[0, 0] * (yearf - yearf[0])

    # convert to mm
    if mm:
        data = data * 1000
        Ddata = Ddata * 1000

    return gtoNEU(yearf, data, Ddata, dstring=dstring)


def gtoNEU(yearf, data, Ddata, dstring=None):
    """ """

    import numpy as np

    from gtimes.timefunc import convfromYearf

    if dstring == "yearf":  # use the decimal year format
        NEUdata = np.array(
            zip(yearf, data[0], data[1], data[2], Ddata[0], Ddata[1], Ddata[2]),
            dtype=[
                ("yearf", float),
                ("data[0]", float),
                ("data[1]", float),
                ("data[2]", float),
                ("Ddata[0]", float),
                ("Ddata[1]", float),
                ("Ddata[2]", float),
            ],
        )
    else:
        yearf = convfromYearf(yearf, dstring)

        NEUdata = np.array(
            zip(yearf, data[0], data[1], data[2], Ddata[0], Ddata[1], Ddata[2]),
            dtype=[
                ("yearf", "S23"),
                ("data[0]", float),
                ("data[1]", float),
                ("data[2]", float),
                ("Ddata[0]", float),
                ("Ddata[1]", float),
                ("Ddata[2]", float),
            ],
        )

    return NEUdata


def read_gps_data(
    sta,
    Dir=None,
    start=None,
    end=None,
    ref="plate",
    detrend_periodic=True,
    detrend_line=True,
    fit=False,
    detrend_period=[None, None],
    useSTA=None,
    useFIT=None,
    uncert=20.0,
    database=False,
    logging_level=logging.WARNING,
):
    """

    Expample usage:
        Return undetrended data in ITRF2008 reference frame:
            VMEY_raw, _ = gpsr.read_gps_data("VMEY", detrend_line=False, detrend_periodic=False, ref="itrf2008")
        Return undetrended, plate removed data:
            VMEY_plate, _ = gpsr.read_gps_data("VMEY", detrend_line=False, detrend_periodic=False, ref="plate")
        Return detrended data:
            VMEY_detrend, _ = gpsr.read_gps_data("VMEY", detrend_line=True, detrend_periodic=True, ref="plate")

    returns:
        data: dataframe with GPS data
        const: paramers for detrending the station
    """

    import logging
    import numpy as np
    from gtimes.timefunc import TimetoYearf

    # Handling logging
    logging.basicConfig(
        format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
        level=logging_level,
    )
    logging.getLogger().setLevel(logging_level)
    module_logger = logging.getLogger()
    if database:
        module_logger("calling gps data from a database")
        pass
    else:
        yearf, data, Ddata, _ = getData(sta, Dir=Dir, ref=ref)

    syearf, sdata, sDdata = yearf, data, Ddata

    # NOTE: detrending needs to be revised.
    const = getDetrFit(sta, useSTA=useSTA, useFIT=useFIT)
    p0 = convconst(const)
    pb = p0.copy()

    module_logger.info("Fitting constants:\n {}".format(p0))
    if fit:
        pass
    elif not np.all([p0[i][1:].dtype is np.dtype('float64') if p0[i] is not None else False for i in range(3)]):
        module_logger.info("Setting fit to lineperiodic")
        fit = "lineperiodic"

    if useFIT == "periodic":
        module_logger.info(
            '"{}" parameters from {} used in {}'.format(
                const["Fit"].values[0], const["UseSTA"].values[0], sta
            )
        )
        module_logger.info('Setting the fit to a "line" for estimating the rate')
        fit = "line"

    syearf, sdata, sDdata = dPeriod(
        yearf,
        data,
        Ddata,
        startyear=detrend_period[0],
        endyear=detrend_period[1],
    )

    if fit:
        module_logger.info("Fitting =====================")
        if len(syearf) == 0:
            module_logger.warning(
                "No data for interval {}-{} try using the whole time series".format(
                    *detrend_period
                )
            )
            syearf, sdata, sDdata = yearf, data, Ddata

        module_logger.info("Fitting the data to a {}".format(fit))
        if fit == "line":
            if p0[0] is not None:
                pt = [p0[i][0:2] for i in range(3)]
            else:
                pt = p0
            module_logger.warning("initial parameters p0 {}".format(pt))
            pb, _ = fittimes(line, syearf, sdata, sDdata, p0=pt)
            module_logger.info("Estimated parameters for {} {}".format(sta, pb))
            if p0[0] is not None:
                pb = [np.concatenate((pb[i], p0[i][2:])) for i in range(3)]
            else:
                pb = [np.concatenate((pb[i], np.zeros(4))) for i in range(3)]
            module_logger.warning("estimated parameters pb {}".format(pb))
                

        elif fit == "periodic":
            pb, _ = fittimes(periodic, syearf, sdata, sDdata, p0=p0)

        elif fit == "lineperiodic":
            pb, _ = fittimes(lineperiodic, syearf, sdata, sDdata, p0=p0)

        if fit == "undetrend":
            pb = [np.zeros(6) for i in range(3)]
            syearf = [None, None]


        const = convconst(const, pb)
        const.loc[sta, ["Starttime", "Endtime"]] = [syearf[0], syearf[-1]]

        if fit == "undetrend":
            pb = [np.zeros(6) for i in range(3)]
            const = convconst(const, pb)
            const.loc[sta, ["Starttime", "Endtime"]] = [None, None]

    else:
        module_logger.info("Not fitting")

    if np.all([pb[i][1:].dtype is np.dtype('float64') if pb[i] is not None else False for i in range(3)]):
        if detrend_periodic:
            module_logger.info("Periodic detrending")
            module_logger.debug("Fitt parameters: {}".format(pb))
            data = detrend(yearf, data.copy(), Ddata, fitfunc=periodic, p=pb)

        if detrend_line:
            module_logger.info("linear detrending")
            pc = [pb[i][0:2] for i in range(3)]
            module_logger.debug("Fitt parameters: {}".format(pc))
            data = detrend(yearf, data.copy(), Ddata, fitfunc=line, p=pc)
    else:
        module_logger.warn("Fitt parameters are unknown pb={}".format(pb))
        if (detrend_periodic or detrend_line):
            module_logger.warning(
                "Will try to estimate the parameters based the whole dataset and detrend"
            )
            data = detrend(yearf, data.copy(), Ddata, fitfunc=lineperiodic)
    # ----------------------------------------------------

    if start:
        startf = TimetoYearf(start.year, start.month, start.day)
    else:
        startf = yearf[0]
    if end:
        endf = TimetoYearf(end.year, end.month, end.day)
    else:
        endf = yearf[-1]

    yearf, data, Ddata = dPeriod(yearf, data, Ddata, startyear=startf, endyear=endf)
    yearf, data, Ddata, _ = vshift(yearf, data, Ddata, uncert=uncert)

    data = convGlobktopandas(yearf, data, Ddata)

    data["hlength"] = np.sqrt(np.square(data[["east", "north"]]).sum(axis=1))
    data["hangle"] = np.rad2deg(np.arctan2(data["north"], data["east"]))
    data["Dhlength"] = np.sqrt(np.square(data[["Deast", "Dnorth"]]).sum(axis=1))

    module_logger.info("Dataframe columns:\n" + str(data.columns) + "\n")
    module_logger.info("Input time period: ({}, {})".format(start, end))
    module_logger.info("dataframe First and Last lines:\n" + str(data.iloc[[0, -1]]))
    module_logger.info("detrend parameter row:\n" + str(const))
    module_logger.debug("Dataframe shape: {}".format(str(data.shape)))
    module_logger.debug("dataframe types:\n" + str(data.dtypes) + "\n")

    return data, const


#
# Other functions
#


def toDateTime(yearf):
    """
    from floating point year to datetime
    """
    from gtimes.timefunc import TimefromYearf

    tmp = []

    for i in range(len(yearf)):
        tmp.append(TimefromYearf(yearf[i]))

    return tmp


def toord(yearf):
    """
    from floating point year to floating point ordinal
    """
    from gtimes.timefunc import TimefromYearf

    for i in range(len(yearf)):
        yearf[i] = TimefromYearf(yearf[i], "ordinalf")

    return yearf


def fromord(yearf):
    # from floating point year to floating point ordinal

    from gtimes.timefunc import TimetoYearf

    for i in range(len(yearf)):
        yearf[i] = Timeto(yearf[i], "ordinalf")

    return yearf


def getData(
    sta,
    fstart=None,
    fend=None,
    ref="itrf2008",
    Dir=None,
    tType="TOT",
    uncert=15,
    offset=None,
):
    """
    extracting and filtering data to prepeare for plotting
    """

    import geofunc.geofunc as gf

    if tType == "JOIN":
        tType = "TOT"

    yearf, data, Ddata = openGlobkTimes(sta, Dir=Dir, tType=tType)
    yearf, data, Ddata = dPeriod(yearf, data, Ddata, fstart, fend)
    if yearf is None or len(yearf) == 0:
        print("WARNING: no data for station {}".format(sta))
        return None, None, None, None
    yearf, data, Ddata, offset = iprep(yearf, data, Ddata, uncert=uncert, offset=offset)

    if offset is None:
        print("WARNING: offset determination failure for station {}".format(sta))

    if ref == "plate":
        plateVel = gf.plateVelo([sta])
        data[0, :] = data[0, :] - plateVel[0, 1] * 1000 * (yearf - yearf[0])
        data[1, :] = data[1, :] - plateVel[0, 0] * 1000 * (yearf - yearf[0])

    elif ref == "detrend":
        pN, pE, pU, pb = detrend(yearf, data, sta)
        pb_org = [pN, pE, pU]

        for i in range(3):
            data[i] = -errfunc(pb_org[i], yearf - yearf[0], data[i])

    elif ref == "itrf2008":
        pass

    else:
        plateVel = gf.plateVelo([sta], ref)
        data[0, :] = data[0, :] - plateVel[0, 1] * 1000 * (yearf - yearf[0])
        data[1, :] = data[1, :] - plateVel[0, 0] * 1000 * (yearf - yearf[0])

    return yearf, data, Ddata, offset


#
#   --- Private functions ---
#


def __converter(x):
    """
    The data extracted are converted to float and
    occational ******* in the data files needs to handled as NAN

    """
    import numpy as np

    try:
        return float(x)
    except:
        return np.nan

    # if x == '********':
    #    return np.nan
    # else:
    #    return float(x)
