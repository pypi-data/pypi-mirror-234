# ###############################
#
# NetR9.py
#
# Code made by fjalar@vedur.is
# Iceland Met Office
# 2011-2012
#
# ###############################

######## IMPORT LIBRARIES ########

import sCurl, re, sys
import checkPort as checkport

######## DEFINE CLASS ########

class NetR9:

    # ALL TEXT HERE IN THE DOC NEEDS TO BE REVISED LATER ON
    """A Receiver class designed for Trimble NetR9 receiver type.

    Public functions:
    getConnection       -- Get the status of the connection to the router and receiver.
    getVolt             -- Get voltage as measured from one of two ports on the receiver.
    getTemp             -- Get the temperature as measured in the containment of the receiver.
    getLogging          -- Get the logging status of the receiver.
    getSessions         -- List all sessions defined on the receiver and their status; active or inactive.
    getDirList          -- Get a list of subdirectories for a certain directiory.
    getFileList         -- Get a list of files for a specific directory passed as an argument.
    getPosition         -- Get the current position of the receiver.
    getTracking         -- Get the current tracking of satellites.
    getFirmwareVersion  -- Get the current firmware version for the receier.
    getStatus           -- A collective report for the receiver; volt, temp, logging and sessions.
    info                -- Reports information on the receiver object.

    Private functions:
    __getStuff          -- The function that combines the similar actions of getTemp, getVolt, getLogging and getSessions.
    __parceFancy        -- Parcing method used by the Public methods to trim and cut the http result and return values in dictionaries instead of a singel string.
    """

    def __init__(self,station_info):

        # 1 # Parameters saved and type set to string
        self.station_info = station_info
        self.sid = self.station_info['station']['id']
        self.userpass = None
        self.CONNECTION_STATUS = {'router':None,'receiver':None}

        # 2 # The router IP here is the ip on the router/receiver connected to a SIL station. IP is on the form 192.168.100.XX
        if station_info['proxy']['httpport'] != '':

            self.ip = 'localhost'
            self.ipport = self.ip
            self.port = station_info['proxy']['httpport']


        elif self.station_info['proxy']['httpport'] == '':

            self.ip = station_info['router']['ip']
            self.ipport = self.ip
            self.port = station_info['receiver']['httpport']

        # 3 # If the connection uses a proxy through kjarni the IP is set as localhost to use the ssh-tunnel from the localhost (rek/rek2)

        # 4 # If username and password is required to access the receiver, the user/pass info will be passed to the CURL command in the
            # self.userpass variable (dicitonary)
        if station_info['receiver']['user'] and station_info['receiver']['pwd']:
            self.userpass = {'user':station_info['receiver']['user'],'pass':station_info['receiver']['pwd']}

        # 5 # Set the default value for DEBUG
        self.DEBUG = False

        # 6 # Set the default volt port (both are checked though)
        self.voltport = 2

        # 7 # Expand IP with port if port is defined
        if self.port:
            self.ipport = '%s:%s'% (self.ip,self.port)

        # 8 # Instantiate gpsCURL object for URL stuff
        self.curl = sCurl.sCurl()

        # 8 # Check if station is alive
        self.CONNECTION_STATUS = self.getConnection()

    ## ------------------- getConnection() -------------------##

    def getConnection(self):
        """Fetches connection status with the router and receiver"""

        result ={'router':False,'receiver':False,}

        result = checkport.isOpen(self.ip,self.port,self.DEBUG)

        return result

    ## ------------------- getVolt() -------------------##

    def getVolt(self):
        """Fetches voltage information from receiver"""

        max_res = 0

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('volt')

        if self.DEBUG: print "%s Result from fancyParcing: %s" % (currFunc,result['value'])

        if result['value']:
            for r in result['value']:
                #print "%s r: " % (currFunc,r)
                #print "%s max_res " % (currFunc,max_res)

                if float(r) > float(max_res):
                    max_res = r

                #print "%s new max_res: " % (currFunc,max_res)


            if self.DEBUG: print "%s Maxiumum volt value: %s" % (currFunc,max_res)
            result['value'] = max_res


        if self.DEBUG: print "%s Result after comparison: %s" % (currFunc,result)

        return result

    ## ------------------- getTemp() -------------------##

    def getTemp(self):
        """Fetches temperature information from receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('temp')
        return result

    ## ------------------- getLogging() -------------------##

    def getLogging(self):
        """Fetches information about the logging status of the receiver; What files are currently being created"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        if self.DEBUG: print "%s is now running" % currFunc
        # 1 # Define variables
        files = []
        sfile = {'session':'','status':'','file':''}
        result = {'value':None, 'error':None}
        fileList = {'value':None, 'error':None}

        # 2 # Get list of files for current month
        fileList = self.getFileList(1)
        if self.DEBUG: print "%s fileList: %s" % (currFunc,fileList)

        # 3 # Loop through the files and pick out the one file with the .T0"B" ending.. the currently logged file.
        if fileList['value']:
            for nfile in fileList['value']:
                if 'T0B' in nfile['file']:
                    # 3.1 # Save the resulting file in a format compatible to NetRS.
                    sfile = {'session':nfile['freq'],'status':'Logging','file':'/Internal/'+nfile['month']+'/'+nfile['freq']+'/'+nfile['file']}
                    # 3.2 # Append the current session file to the list of files currently logging.
                    files.append(sfile)

            result['value'] = files
        else:
            result['error'] = fileList['error']


        # 5 # Return
        return result

    ## ------------------- getSession() -------------------##

    def getSessions(self):
        """Fetches information about defined sessions from the receiver; which sessions are active and which are not."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('sessions')
        return result

    def getFileList(self,months=99):
        """Fetches file listing from the receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        # For months=0 we traverse the whole data tree and return list of all files on the receiver.

        # 1 # Define variables.. dictionary and a list
        filedict = {'month':'','freq':'','file':'','size':'','ctime':''}    # Dictionary for a single file
        fileList = []                                                       # List of file dictionaries
        rootDir = 'Internal/'                                               # The root of the directory list on this type of receiver
        monthList = {'value':None,'error':None}
        result    = {'value':None,'error':None}
        monthFreq = {'value':None,'error':None}
        monthCount = 0                                                      # Counter variable for months

        # 2 # Get list of month directories from the root
        monthList = self.getDirList(rootDir)
        #print monthList

        # NEEDS A BETTER FIX.
        # I had to put try here to plug in some crash holes in the code block here below
        # It seems that when the connection to a station is bad, values in the lists
        # can be somewhat random
        try:
            # 3 # Always the lesser value is chosen. This is done to prevent index-out-of-bound problems
            if monthList['value']:

                months = min(len(monthList['value']),months)

                # 4 # Traverse the whole tree and map
                for month in reversed(monthList['value']):
                    if self.DEBUG: print 'month: %s' % month['name']

                    # Skip over this annoying case in the NetR9 folder structure.
                    if month == 'Clone':
                        pass
                    else:
                        # A simple counter that breaks if nubmer of months passed as value is reached.
                        # 4.1 # If no value was passed months is set to 99 which basically means that the whole tree will be traversed.
                        if monthCount == months:
                            break
                        monthCount += 1

                        # 4.2 # Get list of frequency directories form the month
                        monthFreq = self.getDirList(rootDir+month['name'])

                        if type(monthFreq) != 'NoneType':
                            if self.DEBUG: print 'monthFreq: %s' % monthFreq

                            # 4.3 # Loop through each frequency directory
                            for freq in monthFreq['value']:

                                # 4.3.1 # Get list of each file in the directory
                                files = self.getDirList(rootDir+month['name']+'/'+freq['name'])

                                if type(files) != 'NoneType':
                                    if self.DEBUG: print 'files: %s' % files
                                    # 4.3.2 # Loop through each file
                                    for nfile in files['value']:

                                        # 4.3.2.1 # Create a new dictionary for each fiel from all the collected data..
                                        filedict = {'month':month['name'],'freq':freq['name'],'file':nfile['name'],'size':nfile['size'], 'ctime':nfile['ctime']}

                                        # 4.3.2.2 # Add the new file dictionary to a file list
                                        fileList.append(filedict)
                result['value'] = fileList
            else:
                result['error'] = monthFreq['error']

        except Exception, error:
            result['error'] = error


        # 6 # Return
        return result

    def getDirList(self,directory=''):
        """Fetches directory listing from the receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('dirlist',directory)
        return result

    def getPosition(self):
        """Fetches the set position of the receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('position')
        return result

    def getTracking(self):
        """Fetches the set position of the receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('tracking')
        return result

    def getFirmwareVersion(self):
        """Fetches the firmware version for the receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('firmwareversion')
        return result

    def getStatus(self):
        """Compiles a status report for the receiver; temp, volt, logging, session and returns as a dictionary """

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        # 1 # Define a report dictionary
        result = {'connection':self.CONNECTION_STATUS,'temp':{'value':None},'volt':{'value':None},'logging':{'value':None},'session':{'value':None},'position':{'value':None}}


        # 2 # Do the funky dance..
        if self.CONNECTION_STATUS['router']:
            result['connection'] = self.getConnection()
            if self.DEBUG: print "Getting temp.."
            result['temp'] = self.getTemp()
            if self.DEBUG: print "Getting volt.."
            result['volt'] = self.getVolt()
            if self.DEBUG: print "Getting logging.."
            result['logging'] = self.getLogging()
            if self.DEBUG: print "Getting sessions.."
            result['session'] = self.getSessions()
            if self.DEBUG: print "Getting position.."
            result['position'] = self.getPosition()

        return result

    def test(self):
        """Simple method that calls all the public methods in the class without any parameters"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        test = {'connection':'','temp':'','volt':'','logging':'','session':'','filelist':'','position':'','tracking':'','firmware':''}

        #self.setDebug()
        test['connection'] = self.getConnection()
        test['temp'] = self.getTemp()
        test['volt'] = self.getVolt()
        test['logging'] = self.getLogging()
        test['sessions'] = self.getSessions()
        test['filelist'] = self.getFileList(3)
        test['position'] = self.getPosition()
        test['tracking'] = self.getTracking()
        test['firmware'] = self.getFirmwareVersion()

        return test


    def setDebug(self):
        """Debug ON/OFF switch."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        if self.DEBUG:
            self.DEBUG = False
            print '%s Debug OFF' % currFunc
        else:
            self.DEBUG = True
            print '%s Debug ON' % currFunc


    def info(self):
        """Information on the object's attributes"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        print ''
        print '%s SID = %s' % (currFunc,self.sid)
        print '%s IP = %s' % (currFunc,self.ip)
        print '%s PORT = %s' % (currFunc,self.port)
        print '%s VOLT PORT =  %s' % (currFunc,self.voltport)
        print '%s DEBUG = %s' % (currFunc,self.DEBUG)
        print '%s ATTRIBUTES =  %s' % (currFunc,dir(self))


    def __getStuff(self, get_type, recv_dir=''):
        """Method that basically is a big switch statement and is intended to minimize copy-paste in the logical code."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        #if self.DEBUG: print 'DEBUG is ON'

        # 1 # Define variables
        result = {'value':None,'error':None}

        if self.DEBUG: print '%s Station info:' % (currFunc)
        if self.DEBUG: print self.station_info

        # 2 # Define command based on get_type
        if get_type == 'volt':
            url_string = 'http://%s/prog/show?Voltages' % (self.ipport)
        if get_type == 'temp':
            url_string = 'http://%s/prog/show?Temperature' % (self.ipport)
        if get_type == 'sessions':
            url_string = 'http://%s/prog/show?sessions' % self.ipport
        if get_type == 'dirlist':
            url_string = 'http://%s/prog/show?directory&path=/%s' % (self.ipport,recv_dir)
        if get_type == 'position':
            url_string = 'http://%s/prog/show?position' % (self.ipport)
        if get_type =='tracking':
            url_string = 'http://%s/prog/show?trackingstatus' % (self.ipport)
        if get_type == 'firmwareversion':
            url_string = 'http://%s/prog/show?firmwareversion' % (self.ipport)

        if self.DEBUG: print '%s URL string: %s' % (currFunc,url_string)

        if self.CONNECTION_STATUS['router'] and self.CONNECTION_STATUS['receiver']:

            if self.DEBUG: print "%s Both receiver (stat:%s) and router (stat:%s) are alive.. now some action!" % (currFunc,self.CONNECTION_STATUS['router'],self.CONNECTION_STATUS['receiver'])

            # 3 # Some CURL magic
            if url_string != '':
                if self.DEBUG: print "%s This is the URL string: %s " % (currFunc,url_string)
                curl_result = self.curl.getURL(url_string,self.userpass,self.DEBUG)
            else:
                if self.DEBUG: print "No URL string defined..."

            # If the was no error in the reply from the sCurl then continue
            if curl_result['value']:

                # 4 # Some parsing magic
                if self.DEBUG: print '%s Before parsing, value: %s error: %s ' % (currFunc,curl_result['value'],curl_result['error'])

                result['value'] = self.__parseFancy(get_type,curl_result['value'])

                if self.DEBUG: print '%s After parsing, value: %s error: %s ' % (currFunc,result['value'],result['error'])
            else:
                result['error'] = "Connection ERROR: "+curl_result['error']

        else:

            # just a little return formatting in case of empty/no reply
            if get_type == 'position':
                result['value'] = {'latitude':None,'longitude':None,'altitude':None}
            else:
                result['value'] = None


            if not self.CONNECTION_STATUS['router']:

                result['error'] = "Connection ERROR: ROUTER OFFLINE"
            else:
                result['error'] = "Connection ERROR: RECEIVER UNREACHABLE"

        # 5 # Return
        return result



    def __parseFancy(self, string_type, string):
        """Parses the return strings from the receiver and retuns only the relevant information in a dictionary """

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        # 1 # Define variables
        result = None

        if self.DEBUG: print '%s String type: %s' % (currFunc,string_type)

        # 2 # If string type is 'volt'
        if string_type == 'volt':

            # 1 # Define variables
            patt_found = ''

            # 2 # Define regexp pattern
            #regex=re.compile('(?:input|port)=%s volts=(\d+(?:\.\d*)?)' % self.voltport)
            regex=re.compile('(?:input|port)=%s\s+?:\S+|\s+volts=(\d+(?:\.\d*))' % self.voltport)

            try:
                #patt_found = regex.search(string)
                #result = patt_found.group(1)
                patt_found = regex.findall(string)

                # this is done to raise exception when the group is empty
                if patt_found != []: result = patt_found

            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 3 # If string type is 'temp'
        if string_type == 'temp':

            regex=re.compile('Temperature temp=(\d+(?:\.\d*)?)')

            try:
                patt_found = regex.search(string)
                result = patt_found.group(1)
            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 4 # If string type is 'sessions'
        if string_type == 'sessions':

            # 1 # Define variables
            result = []
            patt_found = ''

            # 2 # Define regexp pattern
            regex=re.compile("\s*(\S+)=(\S+)\s*")

            try:
                for line in string.split('\n'):
                    if 'name' in line:
                        if self.DEBUG: print '%s Line: %s' % (currFunc,line)
                        patt_found = regex.findall(line)
                        if self.DEBUG: print '%s  Pattern: %s' % (currFunc,patt_found)
                        result.append(dict(patt_found))

            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 5 # If string type is 'dirlist'
        if string_type == 'dirlist':

            # 1 # Define variables
            result=[]
            patt_found = ''

            # 2 # Define regexp pattern
            regex=re.compile("\s*(\S+)=(\S+)\s*")

            try:
                for line in string.split('\n'):
                    if 'name=' in line and 'lost' not in line:
                        if self.DEBUG: print '%s Line: %s' % (currFunc,line)
                        patt_found = regex.findall(line)
                        if self.DEBUG: print '%s  SEARCHES: %s' % (currFunc,patt_found)
                        result.append(dict(patt_found))

            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)


        # 6 # If string type is 'position'
        if string_type == 'position':

            # 1 # Define variables
            result = {'latitude':None,'longitude':None,'altitude':None}
            patt_found = ''

            # 2 # Define regexp pattern
            regex=re.compile("(\w+)\s*(-?\w+.\w+)\s+(\w{3,6})")

            try:
                for line in string.split('\n'):

                #  if line.startswith('Latitude') or line.startswith('Longitude') or line.startswith('Altitude'):
                #  if self.DEBUG: print 'Line: ', line
                #  patt_found=regex.findall(line)
                #  if self.DEBUG: print '%s Pattern: %s' % (currFunc,patt_found)
                #  result.append(patt_found[0])

                    if line.startswith('Latitude'):
                        if self.DEBUG: print 'Line: ', line
                        patt_found=regex.findall(line)
                        if self.DEBUG: print '%s Pattern: %s' % (currFunc,patt_found)
                        result['latitude'] = patt_found[0][1]

                    if line.startswith('Longitude'):
                        if self.DEBUG: print 'Line: ', line
                        patt_found=regex.findall(line)
                        if self.DEBUG: print '%s Pattern: %s' % (currFunc,patt_found)
                        result['longitude'] = patt_found[0][1]

                    if line.startswith('Altitude'):
                        if self.DEBUG: print 'Line: ', line
                        patt_found=regex.findall(line)
                        if self.DEBUG: print '%s Pattern: %s' % (currFunc,patt_found)
                        result['altitude'] = patt_found[0][1]


            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 7 # If string type is 'tracking'
        if string_type == 'tracking':

            # 1 # Define variables
            result=[]
            patt_found = ''

            # 2 # Define regexp pattern
            regex=re.compile("\s*(\S+)=(\S+)\s*")

            try:
                for line in string.split('\n'):
                    if line.startswith('Prn'):
                        if self.DEBUG: print '%s Line: %s' % (currFunc,line)
                        patt_found = regex.findall(line)
                        if self.DEBUG: print '%s  Pattern: %s' % (currFunc,patt_found)
                        result.append(dict(patt_found))
            except:
                if self.DEBUG: print 'ERROR: %s failed' % string_type

        # 8 # If string type is 'firmwareversion'
        if string_type == 'firmwareversion':

            # 1 # Define variables
            result=[]
            patt_found = ''

            # 2 # Define regexp pattern
            regex=re.compile("\s*(\S+)=(\S+)\s*")

            try:
                patt_found = regex.findall(string)
                result = dict(patt_found)

            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 9 # Return
        return result

# HERE IS THE END!
