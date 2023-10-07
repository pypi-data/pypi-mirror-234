# ###############################
#
# netr.py 
# Code made by bgo@vedur.is
# Iceland Met Office
# 2011-2012
#
# ###############################


"""
Special module to handle Trimble 4700 receivers
In this program are the following functions:

1.  checkVolt(station_info)      - Open a ssh tunnel to a station.
2.  checkTemp(station_info)      - Open a ssh tunnel to a station.
3.  checkSession(station_info)   - Open a ssh tunnel to a station.
4.  checkLogging(station_info)   - Open a ssh tunnel to a station.
5.  commReport(station_info)
6.  download(station_info)       - Close a ssh tunnel to a station.

"""
######## IMPORT LIBRARIES ########

import sys, re, subprocess,copy
import utils.gpslib as gpslib
import utils.gpstime as gpstime
import utils.sshtc as sshtc
import trm4700

######## METHODS ########
def checkVolt(station,p_args,DEV,BAUD=9600,PAR="n",HTCR="--rtscts",state=None):
    
    trm = trm4700.trm4700(station,DEV)
    result=trm.getVolt()
    print result[value]
    return result[value]

def runStatus(station,p_args,DEV,BAUD=9600,PAR="n",HTCR="--rtscts",optionlist=("state",),path="/home/mogi/bin/rutils/242b/"):
    # call the rstatus command from rutils: by default -state is called, options awailable are  (svtracking,logging,station,session,state)

    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name

    if p_args['debug']: print currfunc,'Starting...'
    if p_args['debug']: print currfunc,'Trimble 4700 Receivers'

    options=""
    for item in optionlist:
        options += " -"+item
    print options


    # Run the rutil CMD and return output and returncode
    serialcmd = "%srstatus -D%s -P%s -B%s %s%s" % (path,DEV,PAR,BAUD,HTCR,options)
    proc_checkvolt_returncode, proc_checkvolt_comm=gpslib.run_syscmd(serialcmd,p_args)

    status=gpslib.checkError(proc_checkvolt_returncode,proc_checkvolt_comm,1,p_args)


    if status == 0:
        value=proc_checkvolt_comm
    else:
        value=None

    return value

##

def runFile(station,p_args,DEV,BAUD=9600,PAR="n",HTCR="--rtscts",optionlist=("T",),path="/home/mogi/bin/rutils/242b/"):
    # call the rfile command from rutils: by default -T is called (lists files on receiver), options awailable are  (N,F,J,T,K"findex",-U"findex",-I"findex,local_filename")

    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name

    if p_args['debug']: print currfunc,'Starting...'
    if p_args['debug']: print currfunc,'Trimble 4700 Receivers'

    options=""
    for item in optionlist:
        options += " -"+item
    print options


    # Run the curl CMD and return output and returncode
    serialcmd = "%srfile -D%s -P%s -B%s %s%s" % (path,DEV,PAR,BAUD,HTCR,options)
    proc_checkvolt_returncode, proc_checkvolt_comm=gpslib.run_syscmd(serialcmd,p_args)

    status=gpslib.checkError(proc_checkvolt_returncode,proc_checkvolt_comm,1,p_args)


    if status == 0:
        value=proc_checkvolt_comm
    else:
        value=None

    return value
def setSurvey(station,p_args,DEV):

    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name

    if p_args['debug']: print currfunc,'Starting...'
    if p_args['debug']: print currfunc,'Trimble 4700 Receivers'

    print "Trimble 4700"    
    # Delete current survey
    serialcmd = "/home/mogi/bin/rutils/242b/rsurvey -D%s -B9600 -Pn --rtscts -E" % (DEV,)
    #serialcmd = "/home/mogi/python/trimble/gps/lapd/bin/242a/rsuvey -D/home/mogi/dev/%s -B9600 -Pn --rtscts -E" % (station['recv_id'])

    # Run the curl CMD and return output and returncode
    proc_checkvolt_returncode, proc_checkvolt_comm=gpslib.run_syscmd(serialcmd,p_args)

    # Start new survey
    serialcmd = "/home/mogi/bin/rutils/242b/rsurvey -D%s -B9600 -Pn --rtscts -Q -L15 -Z0 -K60" % (DEV)
    #serialcmd = "/home/mogi/python/trimble/gps/lapd/bin/242a/rsurvey -D/home/mogi/dev/%s -B9600 -Pn --rtscts -Q -L15 -K1440" % (station['recv_id'])
#    return integer

    # Run the curl CMD and return output and returncode
    proc_checkvolt_returncode, proc_checkvolt_comm=gpslib.run_syscmd(serialcmd,p_args)

    value=0
    if p_args['debug']: print  "%s value returned %s:" % (currfunc ,value)
    return value

