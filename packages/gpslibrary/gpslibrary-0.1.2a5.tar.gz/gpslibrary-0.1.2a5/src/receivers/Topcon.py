# ###############################
#
# Topcon.py 
#
# Code made by fjalar@vedur.is 
# Iceland Met Office
# 2014
#
# ###############################

######## IMPORT LIBRARIES ########

import sCurl, re, sys, datetime
import checkPort as checkport
    
######## DEFINE CLASS ########

class Topcon:

    # ALL TEXT HERE IN THE DOC NEEDS TO BE REVISED LATER ON
    """A Receiver class designed for Topcon receiver type.
    
    Public functions:
    getConnection       -- Get the status of the connection to the router and receiver.
    getVolt             -- Not implemented.
    getTemp             -- Not implemented.
    getLogging          -- Not implemented.
    getSessions         -- Not implemented.
    getDirList          -- Not implemented.
    getFileList         -- Not implemented.
    getPosition         -- Not implemented.
    getTracking         -- Not implemented.
    getFirmwareVersion  -- Not implemented.
    getStatus           -- A collective report for the receiver; logging and session. 
    info                -- Reports information on the receiver object.

    Private functions:
    __getStuff          -- Not present.
    __parceFancy        -- Not present.
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
 
        # 8 # Instantiate sCurl object for URL stuff
        self.curl = sCurl.sCurl()
       
        # 8 # Check if station is alive
        self.CONNECTION_STATUS = self.getConnection()
    ## ------------------- getConnection() -------------------##

    def getConnection(self):
        """Fetches connection status with the router and receiver"""
        
        result ={'router':None,'receiver':None,}

        result = checkport.isOpen(self.ip,self.port,self.DEBUG)

        return result


    ## ------------------- getVolt() -------------------##

    def getVolt(self):
        """Fetches voltage information from receiver"""
        result = {'value':'N/S','error':''}
        return result 

    ## ------------------- getTemp() -------------------##

    def getTemp(self):
        """Fetches temperature information from receiver"""
        result = {'value':'N/S','error':''}
        return result 

    ## ------------------- getLogging() -------------------##
    def getLogging(self):
        """Fetches information about the logging status of the receiver; What files are currently being created"""        

        result = {'value':'N/S','error':''}
        return result 

    ## ------------------- getSession() -------------------##

    def getSessions(self):
        """Fetches information about defined sessions from the receiver; which sessions are active and which are not."""

        result = {'value':'N/S','error':''}
        return result 

    def getPosition(self):
        """Fetches information about the position of the receiver.. from the receiver."""
        
        result = {'value':{'latitude':'N/S','longitude':'N/S','altitude':'N/S'},'error':''}

        return result 

    def getFileList(self,directory=''):
        """Fetches directory listing from a receiver"""

        result = {'value':'N/S','error':''}
        return result 

    def getTracking(self):
        """Fetches tracking status for a receiver"""

        result = {'value':'N/S','error':''}
        return result 

    def getFirmwareVersion(self):
        """Fetches the firmware version for the receiver"""

        result = {'value':'N/S','error':''}
        return result 

    def getStatus(self):
        """Compiles a status report for the receiver; temp, volt, logging, session and returns as a dictionary """
        
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

        if self.DEBUG:
            self.DEBUG = False
            print 'Debug OFF'
        else:
            self.DEBUG = True
            print 'Debug ON'
        

    def info(self):
        """Information on the object's attributes"""
        print ''
        print 'SID = %s' % self.sid
        print 'IP = %s' % self.ip
        print 'PORT = %s' % self.port
        print 'DEBUG = %s' % self.DEBUG
        print 'ATTRIBUTES =  %s' % dir(self)


    def test(self):
        """Simple method that calls all the public methods in the class without any parameters"""

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

  
       # ATT!!     
        # The rest is dismissed but a good template for both _getStuff and _parseFancy can be found in the other receiver moudles.

# HERE IS THE END!
