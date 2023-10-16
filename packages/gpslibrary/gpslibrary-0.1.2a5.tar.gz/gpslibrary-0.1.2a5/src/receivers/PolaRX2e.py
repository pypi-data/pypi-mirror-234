# ###############################
#
# PolaRX2e.py 
#
# Code made by fjalar@vedur.is 
# Iceland Met Office
# 2011-2012
#
# ###############################

######## IMPORT LIBRARIES ########

import sCurl, re, sys, datetime
import checkPort as checkport
    
######## DEFINE CLASS ########

class PolaRX2e:

    # ALL TEXT HERE IN THE DOC NEEDS TO BE REVISED LATER ON
    """A Receiver class designed for Septentrio PolaRX2e receiver type.
    
    Public functions:
    getConnection       -- Get the status of the connection to the router and receiver.
    getVolt             -- Not implemented.
    getTemp             -- Not implemented.
    getLogging          -- Get the logging status of the receiver.
    getSessions         -- List all sessions defined on the receiver and their status; active or inactive.
    getDirList          -- Not implemented.
    getFileList         -- Get a list of files for a specific directory passed as an argument.
    getPosition         -- Get the current position of the receiver.
    getTracking         -- Get the current tracking of satellites.
    getFirmwareVersion  -- Get the current firmware version for the receier.
    getStatus           -- A collective report for the receiver; logging and session.
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
        if self.station_info['proxy']['sshserver'] == '':

            self.ip = station_info['router']['ip']
            self.ipport = self.ip
            self.port = station_info['receiver']['httpport']

        # 3 # If the connection uses a proxy through kjarni the IP is set as localhost to use the ssh-tunnel from the localhost (rek/rek2)
        if station_info['proxy']['sshserver'] != '':         

            self.ip = 'localhost'
            self.ipport = self.ip
            self.port = station_info['proxy']['httpport']

        # 4 # If username and password is required to access the receiver, the user/pass info will be passed to the CURL command in the
            # self.userpass variable (dicitonary)
        if station_info['receiver']['user'] and station_info['receiver']['pwd']:
            self.userpass = {'user':station_info['receiver']['user'],'pass':station_info['receiver']['pwd']}

        # 5 # Set the default value for DEBUG
        self.DEBUG = False
        
        # 6 # Expand IP with port if port is defined
        if self.port:
            self.ipport = '%s:%s'% (self.ip,self.port)
 
        # 8 # Instantiate sCURL object for URL stuff
        self.curl = sCurl.sCurl()
       
        # 8 # Check if station is alive
        self.CONNECTION_STATUS = self.getConnection()
    ## ------------------- getConnection() -------------------##

    def getConnection(self):
        """Fetches connection status with the router and receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        
        result ={'router':None,'receiver':None,}

        result = checkport.isOpen(self.ip,self.port,self.DEBUG)

        return result


    ## ------------------- getVolt() -------------------##

    def getVolt(self):
        """Fetches voltage information from receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc


        result = {'value':'N/S','error':''}
        return result 

    ## ------------------- getTemp() -------------------##

    def getTemp(self):
        """Fetches temperature information from receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc


        result = {'value':'N/S','error':''}
        return result 
    ## ------------------- getLogging() -------------------##
    def getLogging(self):
        """Fetches information about the logging status of the receiver; What files are currently being created"""        

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc
        
        result = {'value':None,'error':None}
        fileList = {'value':None,'error':None}

        # 1 # Get the current file list from the receiver
        fileList = self.__getStuff('filelist')
        
        # 2 # Get the currnent date and time: YYYY MM DD
        now = datetime.datetime.now()

        # 2.1 # Format month correctly by adding 0 in front of single digit numbers
        if len(str(now.month))==1:
            month = '0%s' % now.month
        else:
            month = now.month
        
        # 2.2 # Format day correctly by adding 0 in front of single digit numbers
        if len(str(now.day))==1:
            day = '0%s' % now.day
        else:
            day = now.day

        # 2.3 # Format hour correctly by adding 0 in front of single digit numbers
        if len(str(now.hour))==1:
            hour = '0%s' % now.hour
        else:
            hour = now.hour
        # 2.4 # Then put the "safe" rest to proper variables
        year = now.year
        minute = now.minute

        # 2.5 # DEBUG for date-time formats
        if self.DEBUG: print "%s YEAR: %s MONTH:%s DAY:%s HOUR:%s MINUTE:%s  " % (currFunc,now.year,now.month, now.day, now.hour, now.minute)
        if self.DEBUG: print "%s New MONTH:%s New DAY:%s New HOUR:%s " % (currFunc,month, day, hour)
        if self.DEBUG: print "%s fileList value: %s" % (currFunc,fileList['value'])
        #print "File list error:", fileList['error']
        #print "File list value:", fileList['value']

        # 3 # Find the file in the fileList that has the current date and hour right.. which is the file being currently logged.
        if fileList['value']:
            for f in fileList['value']:
                if f['year'] == str(year) and f['month'] == str(month) and f['day'] == str(day) and f['hour'] == str(hour):
                    result['value'] = f
                    if self.DEBUG: print '%s Current logging file is -> Date: %s-%s-%s Time: %s:%s Size:%s Name:%s' % (
                                                                                            currFunc,
                                                                                            f['year'],
                                                                                            f['month'],
                                                                                            f['day'],
                                                                                            f['hour'],
                                                                                            f['minute'],
                                                                                            f['size'],
                                                                                            f['name'])
                
        else:
            result['error'] = "Error in getLogging()"

        if self.DEBUG: "%s result: %s" % (currFunc,result)
        return result

    ## ------------------- getSession() -------------------##

    def getSessions(self):
        """Fetches information about defined sessions from the receiver; which sessions are active and which are not."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        result = self.__getStuff('sessions')
        return result

    def getPosition(self):
        """Fetches information about the position of the receiver.. from the receiver."""
        
        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        result = self.__getStuff('position')
        return result        

    def getFileList(self,directory=''):
        """Fetches directory listing from a receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        result = self.__getStuff('filelist')
        return result

    def getTracking(self):
        """Fetches tracking status for a receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        result = self.__getStuff('tracking')
        return result

    def getFirmwareVersion(self):
        """Fetches the firmware version for the receiver"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        result = self.__getStuff('firmwareversion')
        return result

    def getStatus(self):
        """Compiles a status report for the receiver; temp, volt, logging, session and returns as a dictionary """

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc
        
        # 1 # Define local variables 

        report = {'connection':'','temp':'','volt':'','logging':'','session':'','position':''}
        
        # 2 # Do the funky dance..
        report['connection'] = self.getConnection()
        report['temp'] = self.getTemp()
        report['volt'] = self.getVolt()
        report['logging'] = self.getLogging()
        report['session'] = self.getSessions()
        report['position'] = self.getPosition()  
  
        
        return report
        
    def setDebug(self):
        """Debug ON/OFF switch."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        if self.DEBUG:
            self.DEBUG = False
            print 'Debug OFF'
        else:
            self.DEBUG = True
            print 'Debug ON'
        

    def info(self):

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        """Information on the object's attributes"""
        print ''
        print 'SID = %s' % self.sid
        print 'IP = %s' % self.ip
        print 'PORT = %s' % self.port
        print 'DEBUG = %s' % self.DEBUG
        print 'ATTRIBUTES =  %s' % dir(self)


    def test(self):
        """Simple method that calls all the public methods in the class without any parameters"""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

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

    
    def __getStuff(self, get_type, recv_dir='',name=''):
        """Method that basically is a big switch statement and is intended to minimize copy-paste in the logical code. 
            For command reference, consult http://www.septentrio.com/sup/secure/polarx3_2_2/secureDownload.php and 
            http://www.septentrio.com/sup/secure/polarx3_2_2/PolaRx2CmdRef.pdf"""        

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print "%s is now running..." % currFunc

        # 1 # Define local variables
        result = {'value':None,'error':None}
        
        # 2 # Define command based on get_type
        if get_type =='sessions':
            url_string = 'http://%s/cgi-bin/anycmd?anycmd=gmi' % self.ipport
        if get_type =='position':
            url_string = 'http://%s/cgi-bin/anycmd?anycmd=grp' % self.ipport
        if get_type =='filelist':
            url_string = 'http://%s/cgi-bin/anycmd?anycmd=gfl' % self.ipport
        if get_type =='tracking':
            url_string = 'http://%s/cgi-bin/anycmd?anycmd=sdo' % self.ipport
        if get_type =='firmwareversion':
            url_string = 'http://%s/cgi-bin/anycmd?anycmd=gvf' % self.ipport

        

        if self.DEBUG: print 'URL string: %s' % url_string

        if self.CONNECTION_STATUS['router'] == True and self.CONNECTION_STATUS['receiver'] == True:
            if self.DEBUG: print "%s Both receiver (stat:%s) and router (stat:%s) are alive.. now some action!" % (currFunc,self.CONNECTION_STATUS['router'],self.CONNECTION_STATUS['receiver'])


            # 3 # Some CURL magic
            if url_string != '':
                if self.DEBUG: print "%s This is the URL string: %s " % (currFunc,url_string)        
                result = self.curl.getURL(url_string,self.userpass,self.DEBUG)
            else:
                print "No URL string defined..."

            # 4 # Some parsing magic
            if self.DEBUG: print '%s Before parsing: %s ' % (currFunc,result['value'])
            if result['value']:
                result['value'] = self.__parseFancy(get_type,result['value'])        
            if self.DEBUG: print '%s After parsing: %s ' % (currFunc,result['value'])         

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
        if self.DEBUG: print "%s is now running..." % currFunc
        
        # 1 # Define variables
        result ='NOT REALLY...'

        if self.DEBUG: print '>>> String type: %s' % string_type

        # 2 # If string type is 'sessions'
        if string_type == 'sessions':        

            # 2.1 # Create a regexp comparison pattern 
            regex=re.compile(".(\d+.\d+).")

            # 2.2 # Try regexp comparison
            try:
                for line in string.split('\n'):
                    if self.DEBUG: print "LINE >>> ", line
                    if '$PolaRx:' in line:
                        if self.DEBUG: print 'Line found: ', line

                        # 2.3.1 # Run regexp
                        p = regex.search(line)         
                        if self.DEBUG: print "p.groups(): ", p.groups()                   

                        # 2.3.2 # Add resulting groups to dictionary
                        result = {'interval':p.group(1)}

                        if self.DEBUG: print '>>> SEARCHES: %s' % result


            except:
                if self.DEBUG: print 'ERROR: Pattern matching in %s failed..' % string_type 

        # 3 # If string type is 'filelist'
        if string_type == 'filelist':

            # 3.1 # Define variables
            result=[]
            patt_found = ''

            # 3.2 # Define regexp pattern 
            regex=re.compile('.(\w{3}).(\d{2}).(\d{4})\s(\d{2}):(\d{2})\s+(\d+)\s*.(PLRX\d{4}\.\d{2}_\.\w{3}).')

            # 3.3 # Define local variables 
            # Months dict is used to replace word-month for number-month                
            months = {  'Jan':'01',
                        'Feb':'02',
                        'Mar':'03',
                        'Apr':'04',
                        'May':'05',
                        'Jun':'06',
                        'Jul':'07',
                        'Aug':'08',
                        'Sep':'09',
                        'Oct':'10',
                        'Nov':'11',
                        'Dec':'12'}
            
            # List to collect dicts in..
            result = []    
                
            # 3.4 # Try regexp comparison
            try:
                for line in string.split('\n'):
                    if 'PolaR&' in line:
                        if self.DEBUG: print 'Line: ', line

                        # 3.4.1 # Run regexp
                        p = regex.search(line)                            

                        # 3.4.2 # Add resulting groups to dictionary
                        p_dict = {'month':months[p.group(1)],
                                    'day':p.group(2),
                                    'year':p.group(3),
                                    'hour':p.group(4),
                                    'minute':p.group(5),
                                    'size':p.group(6),
                                    'name':p.group(7)}

                        if self.DEBUG: print '>>> SEARCHES: %s' % p_dict

                        # 3.4.3 # Add each dict to the result list
                        result.append(p_dict)

            except:
                        
                if self.DEBUG: print 'ERROR: Pattern matching in %s failed..' % string_type 

        # 4 # If string type is 'position'
        if string_type == 'position':        

            # 4.1 # Define variables
            result={'latitude':None,'longitude':None,'altitude':None}
            patt_found = ''

            # 4.2 # Define regexp pattern
            regex=re.compile("(\d+.\d+),\s+(-\d+.\d+),\s+(\d+.\d+)")

            # 4.3 # Try regexp comparison
            try:
                for line in string.split('\n'):
                    if self.DEBUG: print "LINE >>> ", line
                    if '$PolaR#:' in line:
                        if self.DEBUG: print 'Line found: ', line

                        # 4.3.1 # Run regexp
                        p = regex.search(line)         
                        if self.DEBUG: print "p.groups(): ", p.groups()                   

                        # 4.3.2 # Add resulting groups to dictionary
                        result = {'latitude':p.group(1),'longitude':p.group(2),'altitude':p.group(3)}

                        if self.DEBUG: print '>>> SEARCHES: %s' % result


            except:
                if self.DEBUG: print 'ERROR: Pattern matching in %s failed..' % string_type 

        # 5 # If string type is 'tracking'
        if string_type == 'tracking':        

            # 5.1 # Define variables
            result=[]
            patt_found = ''

            # 5.2 # Define regexp pattern
            regex=re.compile("(\d+.\d+),\s+(-\d+.\d+),\s+(\d+.\d+)")

            # 5.3 # Try regexp comparison
            try:
                for line in string.split('\n'):
                    if self.DEBUG: print "LINE >>> ", line
                    #if '$PolaR#:' in line:
                     #   if self.DEBUG: print 'Line found: ', line

                      #  # 5.2.1 # Run regexp
                      #  p = regex.search(line)         
                      #  if self.DEBUG: print "p.groups(): ", p.groups()                   

                        # 5.2.2 # Add resulting groups to dictionary
                      #  result = {'latitude':p.group(1),'logitude':p.group(2),'altitude':p.group(3)}

                      #  if self.DEBUG: print '>>> SEARCHES: %s' % result


            except:
                if self.DEBUG: print 'ERROR: Pattern matching in %s failed..' % string_type 

        # 6 # If string type is 'firmwareversion'
        if string_type == 'firmwareversion':        
 
            # 6.1 # Define variables
            result=[]
            patt_found = ''

            # 6.2 # Define regexp pattern
            regex=re.compile("\s*(\S+):\s*(\S+)\s*")

            # 6.3 # Try regexp comparison
            try:    
                for line in string.split('\n'):
                    if 'firmware' in line:
                        if self.DEBUG: print 'Line: ', line
                        patt_found=regex.findall(line)
                        if self.DEBUG: print '>>> SEARCHES: %s' % patt_found
                        result.append(dict(patt_found))

            except:
                if self.DEBUG: print 'ERROR: %s failed' % string_type        

            
        # 7 # Finally return the result which could have come from step 2-6.
        return result


# HERE IS THE END!
