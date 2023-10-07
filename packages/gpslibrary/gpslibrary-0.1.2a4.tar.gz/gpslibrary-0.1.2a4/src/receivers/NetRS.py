# ###############################
#
# NetRS.py
#
# Code made by fjalar@vedur.is
# Iceland Met Office
# 2011-2016
#
# ###############################

######## IMPORT LIBRARIES ########
import sCurl, re, sys
import checkPort as checkport


######## DEFINE CLASS ########
class NetRS:

    # ALL TEXT HERE IN THE DOC NEEDS TO BE REVISED LATER ON
    """A Receiver class designed for Trimble NetRS receiver type.

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

        # 4 # If username and password is required to access the receiver, the user/pass info will be passed to the CURL command in the
            # self.userpass variable (dicitonary)
        if station_info['receiver']['user'] and station_info['receiver']['pwd']:
            self.userpass = {'user':station_info['receiver']['user'],'pass':station_info['receiver']['pwd']}

        # 5 # Set the default value for DEBUG
        self.DEBUG = False

        # 6 # Expand IP with port if port is defined
        if self.port:
            self.ipport = '%s:%s'% (self.ip,self.port)

        # 7 # Instantiate gpsCURL object for URL stuff
        self.curl = sCurl.sCurl()

        # 8 # Check if station is alive
        self.CONNECTION_STATUS = self.getConnection()

    def getConnection(self):
        """Fetches connection status with the router and receiver"""

        result ={'router':False,'receiver':False,}

        result = checkport.isOpen(self.ip,self.port,self.DEBUG)

        return result

    def getVolt(self):
        """Fetches voltage information from receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = {'value':None, 'error':None}

        # 2 # Get result for different voltport
        self.voltport = '1'
        resp_vp1 = self.__getStuff('volt')
        self.voltport = '2'
        resp_vp2 = self.__getStuff('volt')

        # Append resulting dicts in a proper format for return.. looks messy :/
        # Only the actual voltage value is returned and not the both ports.
        # At least not for now...
        if self.DEBUG: print resp_vp1,resp_vp2

        # 3 # Fish the proper voltage and add to result
        if resp_vp1 ['value'] != None and resp_vp2['value'] != None:
            if float(resp_vp1['value']) > float(resp_vp2['value']):
                if self.DEBUG: print "%s port 1: %s bigger than port 2:%s " % (currFunc,resp_vp1['value'],resp_vp2['value'])
                result['value'] = resp_vp1['value']
            else:
                if self.DEBUG: print "%s port 1: %s less than port 2:%s " % (currFunc,resp_vp1['value'],resp_vp2['value'])
                result['value'] = resp_vp2['value']
            result['error'] = None

        if self.DEBUG: print "%s The return is: %s" % (currFunc, result)
        # 4 # Return
        return result

    def getTemp(self):
        """Fetches temperature information from receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('temp')
        return result

    def getLogging(self):
        """Fetches information about the logging status of the receiver; What files are currently being created"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('logging')
        return result

    def getSessions(self):
        """Fetches information about defined sessions from the receiver; which sessions are active and which are not."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        result = self.__getStuff('sessions')
        return result

    def getFileList(self,months=99):
        """Fetches file listing from the receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        # 1 # Define variables.. dictionary and a list
        filedict = {'month':'','freq':'','file':'','size':''}   # Dictionary for a single file
        fileList = []                                           # List of file dictionaries
        rootDir = ''                                            # The root of the directory list on this type of receiver
        monthCount = 0                                          # Counter variable for months
        monthFreq = {'value':None,'error':None}
        result = {'value':None,'error':None}

        # 2 # Get list of month directories from the root
        monthList = self.getDirList(rootDir)

        # 3 # Always the lesser value is chosen. This is done to prevent index-out-of-bound problems
        months = min(len(monthList['value']),months)

        # 4 # Traverse the whole tree and map
        for month in reversed(monthList['value']):
            # A simple counter that breaks if nubmer of months passed as value is reached.
            # 4.1 # If no value was passed months is set to 99 which basically means that the whole tree will be traversed.
            if monthCount == months:
                break
            monthCount += 1

            if self.DEBUG: print month['name']

            # 4.2 # Get list of frequency directories form the month
            monthFreq = self.getDirList(rootDir+month['name'])
	    if monthFreq:
		    if self.DEBUG: print monthFreq

		    # 4.3 # Loop through each frequency directory
		    for freq in monthFreq['value']:

		        # 4.3.1 # Get list of each file in the directory
		        files = self.getDirList(rootDir+month['name']+'/'+freq['name'])

		        # 4.3.2 # Loop through each file
		        for nfile in files['value']:

		            # 4.3.2.1 # Create a new dictionary for each fiel from all the collected data..
		            filedict = {'month':month['name'],'freq':freq['name'],'file':nfile['name'],'size':nfile['size']}

		            # 4.3.2.2 # Add the new file dictionary to a file list
		            fileList.append(filedict)

		    result['value'] = fileList

	    else:

		result['error'] = nothFreq['error']


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

        # 1 # Define dictionary
        result = {'connection':self.CONNECTION_STATUS,'temp':{'value':None},'volt':{'value':None},'logging':{'value':None},'session':{'value':None},'position':{'value':None}}

        # 2 # Do the funky dance..
        if self.CONNECTION_STATUS['router']:
            result['connection'] = self.getConnection()
            result['temp'] = self.getTemp()
            result['volt'] = self.getVolt()
            result['logging'] = self.getLogging()
            result['session'] = self.getSessions()
            result['position'] = self.getPosition()
            #result['tracking'] = self.getTracking()

        # 3 # Return
        return result

    def test(self):
        """Simple method that calls all the public methods in the class without any parameters"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        test = {'connection':'','temp':'','volt':'','logging':'','session':'','filelist':'','position':''}

        #self.setDebug()
        test['connection'] = self.getConnection()
        test['temp'] = self.getTemp()
        test['volt'] = self.getVolt()
        test['logging'] = self.getLogging()
        test['sessions'] = self.getSessions()
        test['filelist'] = self.getFileList()
        test['position'] = self.getPosition()

        return test

    def setDebug(self):
        """Debug ON/OFF switch."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        if self.DEBUG:
            self.DEBUG = False
            print '%s Debug is now off OFF' % currFunc
        else:
            self.DEBUG = True
            print '%s Debug is now ON' % currFunc

    def info(self):
        """Information on the object's attributes"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        print ''
        print '%s SID = %s' % (currfunc,self.sid)
        print '%s IP = %s' % (currfunc,self.ip)
        print '%s PORT = %s' % (currfunc,self.port)
        print '%s DEBUG = %s' % (currfunc,self.DEBUG)
        print '%s ATTRIBUTES =  %s' % (currfunc,dir(self))

    def __getStuff(self, get_type, recv_dir='',filename=''):
        """Method that basically is a big switch statement and is intended to minimize copy-paste in the logical code."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        #if self.DEBUG: print 'DEBUG is ON'
        # 1 # Define variables
        result = {'value':None,'error':None}

        #if self.DEBUG: print '%s Station info:' % (currFunc)
        #if self.DEBUG: print "%s Station INFO: %s" % (currFunc,self.station_info)

        # 2 # Define command based on get_type
        if get_type == 'volt':
            url_string = 'http://%s/prog/show?Voltage&input=%s' % (self.ipport,self.voltport)
        if get_type =='temp':
            url_string = 'http://%s/prog/show?Temperature' % (self.ipport)
        if get_type =='logging':
            url_string = 'http://%s/prog/show?loggingstatus' % (self.ipport)
        if get_type =='sessions':
            url_string = 'http://%s/prog/show?sessions' % (self.ipport)
        if get_type =='dirlist':
            url_string = 'http://%s/prog/show?loggedfiles&directory=/%s' % (self.ipport,recv_dir)
        if get_type =='position':
            url_string = 'http://%s/prog/show?position' % (self.ipport)
        if get_type =='tracking':
            url_string = 'http://%s/prog/show?trackingstatus' % (self.ipport)
        if get_type == 'firmwareversion':
            url_string = 'http://%s/prog/show?firmwareversion' % (self.ipport)


        if self.DEBUG: print '%s URL string: %s' % (currFunc,url_string)
        if self.DEBUG: print "%s Router  status: %s " % (currFunc,self.CONNECTION_STATUS['router'])
        if self.DEBUG: print "%s Receiver status: %s" % (currFunc,self.CONNECTION_STATUS['receiver'])

        if self.CONNECTION_STATUS['router'] == True and self.CONNECTION_STATUS['receiver'] == True:
            if self.DEBUG:
                print "%s Both receiver (stat:%s) and router (stat:%s) are alive.. now some action!" % (currFunc,self.CONNECTION_STATUS['router'],self.CONNECTION_STATUS['receiver'])

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

            # 2.1 # Define variables
            patt_found = None

            if self.DEBUG: print "%s String before parsing: %s" % (currFunc,string)
            if self.DEBUG: print "%s Voltport: %s" % (currFunc,self.voltport)

            # 2.2 # Define regexp pattern
            regex=re.compile('(?:input|port)=%s volts=(\d+(?:\.\d*)?)' % self.voltport)

            try:
                patt_found = regex.search(string)
                result = patt_found.group(1)

            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 3 # If string type is 'temp'
        if string_type == 'temp':

            # 3.1 # Define variables
            patt_found = None

            # 3.2 # Define regexp pattern
            regex=re.compile('Temperature temp=(\d+(?:\.\d*)?)')

            try:
                patt_found = regex.search(string)
                result = patt_found.group(1)
            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 4 # If string type is 'logging' or 'sessions'
        if string_type == 'logging' or string_type == 'sessions':

            # 4.1 # Define variables
            result=[]
            patt_found = None

            # 4.2 # Define regexp pattern
            regex=re.compile("\s*(\S+)=(\S+)\s*")

            try:
                for line in string.split('\n'):
                    if 'name' in line:
                        if self.DEBUG: print 'Line: ', line
                        patt_found=regex.findall(line)
                        if self.DEBUG: print '%s Pattern: %s' % (currFunc,patt_found)
                        result.append(dict(patt_found))

            except:
                if self.DEBUG: print 'ERROR: %s failed' % string_type

        # 5 # If string type is 'filelist'
        if string_type == 'dirlist':

            # 5.1 # Define variables
            result=[]
            patt_found = None

            # 5.2 # Define regexp pattern
            regex=re.compile("\s*(\S+)=(\S+)\s*")

            try:
                for line in string.split('\n'):
                    if 'name' in line:
                        if self.DEBUG: print 'Line: ', line
                        patt_found=regex.findall(line)
                        if self.DEBUG: print '%s Pattern: %s' % (currFunc,patt_found)
                        result.append(dict(patt_found))

            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 6 # If string type is 'filelist'
        if string_type == 'position':

            # 6.1 # Define variables
            result = {'latitude':None,'longitude':None,'altitude':None}
            patt_found = None

            # 6.2 # Define regexp pattern
            regex=re.compile("(\w+)\s*(-?\w+.\w+)\s+(\w{3,6})")


            try:
                for line in string.split('\n'):

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

            # 7.1 # Define variables
            result=[]
            patt_found = None

            # 7.2 # Define regexp pattern
            regex=re.compile("\s*(\S+)=(\S+)\s*")

            try:
                for line in string.split('\n'):
                    if line.startswith('Chan'):
                        if self.DEBUG: print 'Line: ', line
                        patt_found=regex.findall(line)
                        if self.DEBUG: print '%s Pattern: %s' % (currFunc,patt_found)
                        result.append(dict(patt_found))
            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc, string_type)

        # 8 # If string type is 'firmwareversion'
        if string_type == 'firmwareversion':

            # 8.1 # Define variables
            patt_found = None

            # 8.2 # Define regexp pattern
            regex=re.compile("\s*(\S+)=(\S+)\s*")

            try:
                patt_found=regex.findall(string)
                result = dict(patt_found)

            except:
                if self.DEBUG: print '%s ERROR: %s failed' % (currFunc,string_type)

        # 9 # Return
        return result

# HERE IS THE END!