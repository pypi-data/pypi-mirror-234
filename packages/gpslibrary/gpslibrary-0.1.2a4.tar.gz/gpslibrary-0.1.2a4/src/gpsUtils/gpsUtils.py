#!/usr/bin/python
"""
convllh(llh,radians=True)
extractfromGamitBakf(cfile, stations)
savedisp(dataDict,fname=None, header="")
"""
import subprocess

def run_cmd(check_cmd):
    ## Run command

    process = subprocess.Popen(check_cmd,shell=True,stdout=subprocess.PIPE)
    process.wait()

    proc_check_returncode = process.returncode
    proc_check_comm = process.communicate()[0].strip('\n'.encode())
    
    
    return proc_check_returncode,proc_check_comm

def run_syscmd(check_cmd,p_args):
    """
    """
    ## Run command
    import sys, re, subprocess, getopt, logging, copy, socket, types
    import gpstime

    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name
    if p_args['debug']: print('%s Starting ...' % currfunc)

    process = subprocess.Popen(check_cmd,shell=True,stdout=subprocess.PIPE)
    process.wait()

    proc_check_returncode = process.returncode
    proc_check_comm = process.communicate()[0].strip('\n')
    
    
    #(3)# Make desicions according to output...
    if p_args['debug']: print('%s process.returncode:' % currfunc, proc_check_returncode)
    if p_args['debug']: print(currfunc,'process.communicate():\n---------------\n', proc_check_comm,'\n-------------')
    if proc_check_returncode == 0:
        if p_args['debug']: print("%s Command went well.." % currfunc)
    elif proc_check_returncode == 255:
        if p_args['debug']: print("%s Timeout..." % currfunc)
    else:
        if p_args['debug']: print("%s Command failed... " % currfunc)

def conv2png(psFile,density=90,logo=None,logoloc="+780+0090"):
    """
    """
    import os


    fDir=os.path.dirname(psFile)
    fileName, Ftype = os.path.splitext(psFile)


    tmpFile=os.path.join(fDir, "tmp.png")
    pngFile="%s.%s" % (fileName,"png") 


    psCmd = "convert -density %d %s %s " % (density, psFile, tmpFile)
    run_cmd(psCmd)
        
    trCmd = "convert -trim %s %s " % (tmpFile,pngFile)
    run_cmd(trCmd)
    if os.path.isfile(tmpFile):
        os.remove(tmpFile)

    if logo:
        logoCmd = "composite -compose atop -gravity NorthEast -geometry +{0} -resize '1x1<' -dissolve 70% {1} {2} {3} ".format(logoloc, logo, pngFile, tmpFile)
        run_cmd(logoCmd)
        os.rename(tmpFile,pngFile)

        #logoCmd = "composite -compose atop -gravity NorthEast -geometry +830+0090 -resize '1x1<' -dissolve 50%" +  " %s %s %s " % (logo, pngFile, tmpFile)


def convpng2thum(pngFile):
    """
    """
    import os
    from PIL import Image

    img = Image.open(pngFile)
    filepr, Fend = os.path.splitext(pngFile)
    size = 128, 128
    img.thumbnail(size,Image.ANTIALIAS)
    img.save(filepr+'-small'+ Fend)



def run_netcmd(netcmd,port,station,p_args):

    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
    if p_args['debug']: print('%s Starting ...' % currfunc)

    conntype=station['conn_type'].split(',') # methods defined by conn_type

    #(1)# define how to handle differennt communication types
    if 'tunnel' in conntype:
        # direct ip connection through tunnels 
        if p_args['debug']: print('%s connecting through %s on port %s' % (currfunc,station['rout_ip'], station['recv_httpport']))
        netcmd = netcmd % '%s:%s' % (station['rout_ip'], port )
        if p_args['debug']: print('%s netcmd=' % currfunc,netcmd)

    elif 'sil' in conntype:
        # direct ip connection through sil computer using port forwarding
        if p_args['debug']: print('%s NetRS/NetR9 receiver on a SIL station' % currfunc)
        netcmd = netcmd % '%s:%s' % ('localhost',station['sil_httpport'])
        if p_args['debug']: print('%s netcmd=' % currfunc,netcmd)

    elif 'direct' in conntype:
        # direct ip connection 
        if p_args['debug']: print('%s Direct connection' % currfunc)
        netcmd = netcmd % station['recv_ip']
        if p_args['debug']: print('%s netcmd=' % currfunc,netcmd)
				
    elif 'serial' in conntype:
        if station['sil_computer']:
            pass
					
        elif '3G' in station['conn_type']:
            pass

    #(2)# run the command and return the output to proc_checktemp_comm
    proc_checktemp_returncode, proc_checktemp_comm=run_syscmd(netcmd, p_args)
    
    # Return
    return proc_checktemp_returncode, proc_checktemp_comm

def checkError(proc_check_returncode,proc_check_comm,searchres,p_args):

    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name
    if p_args['debug']: print('%s Starting ...' % currfunc)

    
    if proc_check_returncode == 0 and searchres: 
        if p_args['debug']: print( "%s all is OK" % currfunc)
        return 0
    elif 'ERROR' in proc_check_comm:
        if p_args['debug']: print( "%s proc_check_comm returned: %s" % (currfunc,proc_check_comm))
        return 11
    else:
        if p_args['debug']: print( "%s Something is wrong" % currfunc)
        print("ERROR in matching  proc_checksess_comm =\n",proc_check_comm,\
              " \nand checksess_returncode=",proc_check_returncode,\
              " \nsearchres=", searchres )
        #sys.exit(0)
        return 1

def changeDictKeys(session,chdict,p_args):
    
    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name

    if p_args['debug']: print('%s Starting inplace key change \ ...\n--\n Canging keys: %s\n--\n In: %s\n--\n To: %s' \
                               % (currfunc, chdict.keys(),session,chdict.values()))

    for sess in session:
        for key in set(chdict.keys()) & set(sess.keys()):
            sess[chdict[key]]=sess.pop(key)  

    return session

def checkPort(host,port,p_args):

    # variable port needs to be of type int
    currfunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
    if p_args['debug']: print('%s Starting...' % currfunc)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(2)
        #if p_args['debug']:
        print("%s Success connecting to %s on port: %s" % (currfunc, host, port))
        return 0
    except:
        #if p_args['debug']:
        print("%s Cannot connect to %s on port: %s" % (currfunc, host, port))
        return 1


def getportdict(pref,station,p_args):  

    # Search string to check for defined ports
    #searchstr=re.compile('recv_(\w+)port') 
    searchstr=re.compile('\s*%s_(\w+)port=(\S+)\s*' % pref)
    stationstr= ' '.join([ '%s=%s' % (k,v) for k,v in station.items()])

    # Extracting the port definitions from recv_+port
    searchres=searchstr.findall(stationstr)
    recvport=dict(searchres)

    return recvport

def str_to_class(field):
    return getattr(sys.modules[__name__], field)
    #    try:
    #        identifier = getattr(sys.modules[__name__], field)
    #    except AttributeError:
    #        raise NameError("%s doesn't exist." % field)
    #    if isinstance(identifier, (types.ClassType, types.TypeType)):
    #        return identifier
    #    raise TypeError("%s is not a class." % field)

