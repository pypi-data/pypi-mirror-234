# ###############################
#
# cparse.py 
#
# Code made by fjalar@vedur.is 
# Iceland Met Office
# 2013
#
# ###############################


######## IMPORT LIBRARIES ########
 

class Parser:

    # ALL TEXT HERE IN THE DOC NEEDS TO BE REVISED LATER ON
    """A class designed to ....
    
    Public functions:
      getStationInfo([station_id])          - Get information for a single station. If no id is passed
                                            - information for all the stations in the config will be returned.
      getStationList                        - Get list of all stations.
      getCheckcommConfig()                  --
      getGetdataConfig(()                   --
      getPreprocessConfig()                 --
      getProcessConfig()                    --
      getPostprocessConfig()                --
      getStatus()                           --
      setDebug()                            --

    Private functions:
      __getConfigPaths()            --
      __clear_station_dicts()       --
      __parse_checkcomm_config()    --
      __parse_getdata_config        -- 
      __parse_preprocess_config     --
      __parse_process_config        --
      __parse_postprocess_config        --

    """

    def __init__(self):
        
        # 1 # Predefine few global variables for the class
        self.DEBUG                  = False
        self.CFG_PATH_GLOBAL        = '/net/gpsplot/data/home/gpsops/.gpsconfig/'
        self.CFG_PATH_STATIONS      = None
        self.CFG_PATH_CHECKCOMM     = None
        self.CFG_PATH_GETDATA       = None
        self.CFG_PATH_PREPROCESS    = None
        self.CFG_PATH_PROCESS       = None
        self.CFG_PATH_POSTPROCESS   = None

        # Variables for station config
        self.ALL_STATIONS = None

        # This function opens a config file and loads values to all the CFG_PATH_* variables
        self.__getConfigPaths()


    # ------------------ setDebug() ------------------ #

    def setDebug(self):
        """Debug ON/OFF switch."""
        if self.DEBUG:
            self.DEBUG = False
            print('Debug OFF')
        else:
            self.DEBUG = True
            print('Debug ON'    )

    # ------------------ setDebug() ------------------ #

    def getStatus(self):
        """Prints global variables"""
        print('Global variable status:')
        print('')
        print('DEBUG                    = ',self.DEBUG)
        print('CONFIG_PATH_GLOBAL       = ',self.CFG_PATH_GLOBAL)
        print('CONFIG_PATH_STATIONS     = ',self.CFG_PATH_STATIONS)
        print('CONFIG_PATH_CHECKCOMM    = ',self.CFG_PATH_CHECKCOMM)
        print('CONFIG_PATH_GETDATA      = ',self.CFG_PATH_GETDATA)
        print('CONFIG_PATH_PREPROCESS   = ',self.CFG_PATH_PREPROCESS)
        print('CONFIG_PATH_PROCESS      = ',self.CFG_PATH_PROCESS)
        print('CONFIG_PATH_POSTPROCESS  = ',self.CFG_PATH_POSTPROCESS)


    # ------------------ __getConfigPahts() ------------------ #

    def __getConfigPaths(self):
        # The parser config file should be located with the parser python file itself, in same directory.

        config_file = self.CFG_PATH_GLOBAL
        config = {'id':'','global_path':'','stations':'','checkcomm':'','getdata':'','preprocess':'','process':'','postprocess':''}

        try:
            f = open(config_file,'r')
            for line in f:
            
                # Check for commented lines
                if line.startswith('#') or len(line) == 1:
                    pass
                else:
                    words = line.split()

                    # Break if end of line
                    if words[0] == 'EOC':  
                        break 

                    # Else remove the '=' just leaving the variable name (words[0]) and value (words[1])
                    else:
                        words.remove('=')

                    # Parse config
                    if words[0] == 'Config_ID': config['id'] = words[1]
                    #if words[0] == 'Config_GLOBAL_PATH': self.CFG_PATH_GLOBAL = words[1]
                    if words[0] == 'configPath_STATIONS': self.CFG_PATH_STATIONS = words[1]
                    if words[0] == 'configPath_CHECKCOMM': self.CFG_PATH_CHECKCOMM = words[1]
                    if words[0] == 'configPath_GETDATA': self.CFG_PATH_GETDATA = words[1]
                    if words[0] == 'configPath_PREPROCESS': self.CFG_PATH_PREPROCESS = words[1]
                    if words[0] == 'configPath_PROCESS': self.CFG_PATH_PROCESS = words[1]
                    if words[0] == 'configPath_POSTPROCESS': self.CFG_PATH_POSTPROCESS = words[1]

            if config['id'] != 'parser':
                print('configParser.__getConfigPaths() > Incorrect file or file corrupted!')


        except IOError:
            print('')
            print('configParser.__getConfigPaths() > File (%s) missing!' % config_file)




    # ------------------ getStationConfig() ------------------ #

    def getStationInfo(self,station_id=''):

        stationList = [] # List of all info dictionaries, which contain few different other dictionaries.
        station, receiver, connection, proxy, router, serial, dialup, info = self.__clear_station_dicts() # get clean dictionaries
        stat_count = 0

        try:
            f = open(self.CFG_PATH_STATIONS,'r')

            for line in f:
                if line.startswith('#') or len(line) == 1:
                    #print('line passed')
                    pass
                else:
                    words = line.split()

                    if words[0] == 'EOF':  
                        pass 
                    else:
                        words.remove('=')

                    if words[0] == 'Station_NAME':
                        # Check if station id has been defined before.. which means this station name is new..                         
                        if station['name'] != '':

                            # Pack last station into the info dictionary..
                            info['station'] = station 
                            info['receiver'] = receiver
                            info['connection'] = connection
                            info['proxy'] = proxy
                            info['router'] = router
                            info['serial'] = serial
                            info['dialup'] = dialup

                            # Add the info dictionary to the station list
                            stationList.append(info)

                            if self.DEBUG: print('configParser.parse() >> Station %s appended..' % station['id'])

                            # Reset all dictionaries
                            station, receiver, connection, proxy, router, serial, dialup, info = self.__clear_station_dicts()        
                  

                        else:
                            station['name'] = words[0]
                            station['id']   = words[1]
                    # Station
                    if words[0] == 'Station_NAME': station['name'] = words[1]
                    if words[0] == 'Station_ID': station['id'] = words[1]
                    # Receiver
                    if words[0] == 'Receiver_TYPE': receiver['type'] = words[1]
                    if words[0] == 'Receiver_IP': receiver['ip'] = words[1]
                    if words[0] == 'Receiver_HTTP_PORT': receiver['httpport'] = words[1]            
                    if words[0] == 'Receiver_FTP_PORT': receiver['ftpport'] = words[1]            
                    if words[0] == 'Receiver_TELNET_PORT': receiver['telnetport'] = words[1]            
                    if words[0] == 'Receiver_SERIAL_PORT': receiver['serialport'] = words[1]            
                    if words[0] == 'Receiver_RTP_PORT': receiver['rtpport'] = words[1]            
                    if words[0] == 'Receiver_REFTEK_PORT': receiver['reftekport'] = words[1]            
                    if words[0] == 'Receiver_USER': receiver['user'] = words[1]
                    if words[0] == 'Receiver_PASS': receiver['pwd'] = words[1]
                    if words[0] == 'Receiver_SERVER': receiver['serv'] = words[1]
                    if words[0] == 'Receiver_BAUDRATE': receiver['baud'] = words[1]
                    if words[0] == 'Receiver_PARITY': receiver['parity'] = words[1]
                    if words[0] == 'Receiver_RTSCTS': receiver['rtscts'] = words[1]
                    # Connect
                    if words[0] == 'Connection_TYPE': connection['type'] = words[1].split(',')
                    if words[0] == 'Connection_PORT': connection['port'] = words[1]
                    if words[0] == 'Connection_PPP': connection['ppp'] = words[1]
                    if words[0] == 'Connection_SSH_PORT': connection['sshport'] = words[1]
                    # Proxy
                    if words[0] == 'Proxy_USER': proxy['user'] = words[1] 
                    if words[0] == 'Proxy_SSH_SERVER': proxy['sshserver'] = words[1]
                    if words[0] == 'Proxy_HOST': proxy['host'] = words[1]
                    if words[0] == 'Proxy_HTTP_PORT': proxy['httpport'] = words[1]
                    if words[0] == 'Proxy_FTP_PORT': proxy['ftpport'] = words[1]
                    if words[0] == 'Proxy_SERIAL_PORT': proxy['serialport'] = words[1]
                    # Router
                    if words[0] == 'Router_TYPE': router['type'] = words[1]
                    if words[0] == 'Router_IP': router['ip'] = words[1]
                    if words[0] == 'Router_PHONE_NUMBER': router['phonenumber'] = words[1]
                    if words[0] == 'Router_PORT_FORWARD': router['portforward'] = words[1]
                    # Serial
                    if words[0] == 'Serial_DEVICE': serial['device'] = words[1]
                    # Dialup
                    if words[0] == 'Dialup_DEVICE': dialup['device'] = words[1]
                    if words[0] == 'Dialup_PHONE_NUMBER': dialup['phonenumber'] = words[1]
                    if words[0] == 'Dialup_METH': dialup['meth'] = words[1]
                    if words[0] == 'Dialup_SERVER': dialup['server'] = words[1]
                    # End of file...
                    if words[0] == 'EOF':

                        # Wrap everything up
                        info['station']     = station 
                        info['receiver']    = receiver
                        info['connection']  = connection
                        info['proxy']       = proxy
                        info['router']      = router
                        info['serial']      = serial
                        info['dialup']      = dialup

                        # Append the station to the list
                        stationList.append(info)    

            info = {'station':'','receiver':'','connection':'','rotuer':'','dialup':''}

            if station_id == '':
                self.ALL_STATIONS = stationList
                #print(self.ALL_STATIONS)
                return stationList
            else:
                singleStationInfo = self.__get_single_station(station_id,stationList)
                return singleStationInfo


        except IOError:
            print('configParser.getStationInfo() > File (%s) missing!' % self.CFG_PATH_STATIONS)
        
    # ------------------ getStationList() ------------------ #

    def getStationList(self):

        if not self.ALL_STATIONS: all_info = self.getStationInfo()

        station_list = []

        for s in self.ALL_STATIONS:
            station_list.append(s['station']['id'])

        return station_list



    # ------------------ __get__single_station() ------------------ #
 
    def __get_single_station(self,station_id,stationList):
        for stationInfo in stationList:
            if stationInfo['station']['id'] == station_id:
                return stationInfo
        

    # ------------------ __clear_station_dicts() ------------------ #

    def __clear_station_dicts(self):

        station = { 'id':'',
                    'name':''}

        receiver= { 'type':'',
                    'ip':'',
                    'httpport':'',
                    'ftpport':'',
                    'telnetport':'',
                    'serialport':'',
                    'rtpport':'',
                    'reftekport':'',
                    'user':'',
                    'pwd':'',
                    'serv':'',
                    'baud':'',
                    'parity':'',
                    'rtscts':''}

        connection = {  'type':'',
                        'ppp':'',
                        'port':'',
                        'sshport':''}

        proxy = {   'user':'',
                    'sshserver':'',
                    'host':'',
                    'httpport':'',
                    'ftpport':'',
                    'serialport':''}

        router = {  'type':'',
                    'ip':'',
                    'phonenumber':'',
                    'portforward':''}

        serial = {  'device':''}

        dialup = {  'device':'',
                    'phonenumber':'',
                    'meth':'',
                    'server':''}

        info = {    'station':'',
                    'receiver':'',
                    'connect':'',
                    'proxy':'',
                    'router':'',
                    'serial':'',
                    'dialup':''} 

        return station, receiver, connection, proxy, router, serial, dialup, info


    # ------------------ getCheckcommConfig() ------------------ #

    def getCheckcommInfo(self):
        print('configParser.getCheckcommConfig > Not yet implemented!')

    # ------------------ getGetdataConfig() ------------------ #

    def getDataInfo(self,session_id=''):

        if self.DEBUG: print('configParser.getGetdataConfig() > Running')
        sessionList = [] # List of all info dictionaries, which contain few different other dictionaries.
        session = self.__clear_getdata_dicts() # get clean dictionaries
        stat_count = 0
        config = {'id':''}

        try:
            f = open(self.CFG_PATH_GETDATA,'r')
            if self.DEBUG: print('configParser.getGetdataConfig() > Config file available and open...')

            for line in f:
                if self.DEBUG: print('configParser.getGetdataConfig() > Traversing lines in file...')
                if line.startswith('#') or len(line) == 1:
                    #print('line passed')
                    if self.DEBUG: print('configParser.getGetdataConfig() > Passing line: ',line)
                    #pass
                else:
                    if self.DEBUG: print('configParser.getGetdataConfig() > Splitting line into words...')
                    words = line.split()

                    if words[0] == 'EOF':
                        if self.DEBUG: print('configParser.getGetdataConfig() > EOF found...exiting.'  )
                        pass 
                    else:
                        if self.DEBUG: print('configParser.getGetdataConfig() > Stripping "=" away..')
                        words.remove('=')

                    if words[0] == 'Session_ID':
                        if self.DEBUG: print('configParser.getGetdataConfig() > Session ID >%s< found..' % words[1])

                        # Check if session id has been defined before.. which means this session id is new..                         
                        if session['id'] != '':

                            # Add the session dictionary to the station list
                            sessionList.append(session)

                            if self.DEBUG: print('configParser.getGetdataConfig() > Session %s appended to sessionList' % session['id'])

                            # Reset all dictionaries
                            session = self.__clear_getdata_dicts()  
                            if self.DEBUG: print('configParser.getGetdataConfig() > Session list cleared for the next session...'  )

                            # Save the next session ID to the new session
                            if self.DEBUG: print('configParser.getGetdataConfig() > Next session created.' )
                            session['id']   = words[1]    
                  

                        else:
                            session['id']   = words[1]

                    # Session
                    if self.DEBUG: print('configParser.getGetdataConfig() > Parsing list...')

                    if words[0] == 'Config_ID': config['id'] = words[1]
                    if words[0] == 'Session_ID': session['id'] = words[1]
                    if words[0] == 'Destination_PATH': session['destpath'] = words[1]
                    if words[0] == 'Sample_FREQUENCY': session['samplfreq'] = words[1]
                    if words[0] == 'Store_To_DB': session['storetodb'] = words[1]
                    if words[0] == 'Report_LEVEL': session['reportlevel'] = words[1]

                    if words[0] == 'Days_To_DOWNLOAD': session['daystod'] = words[1]


                    # End of file...
                    if words[0] == 'EOF':

                        # Append the station to the list
                        sessionList.append(session)    

            if config['id'] != 'getdata':

                print('configParser.getGetdataConfig() > Incorrect file or file corrupted!')
                print('configParser.getGetdataConfig() > Config ID: ',config['id'] )
                print('configParser.getGetdataConfig() > sessionList[0]: ',sessionList[0])

            else:

                if session_id == '':
                    return sessionList
                else:
                    singleSessionInfo = self.__get_single_session(session_id,sessionList)
                    return singleSessionInfo

        except IOError:
            print('configParser.getGetdataConfig() > File (%s) missing!' % self.CFG_PATH_GETDATA)
            

    # ------------------ __get__single_station() ------------------ #
 
    def __get_single_session(self,session_id,sessionList):
        for sessionInfo in sessionList:
            if sessionInfo['id'] == session_id:
                return sessionInfo



    # ------------------ __clear_getdata_dicts() ------------------ #

    def __clear_getdata_dicts(self):

        session = { 'id':'',
                    'destpath':'',
                    'samplfreq':'',
                    'storetodb':'',
                    'reportlevel':'',
                    'daystod':''}

        return session
       


    # ------------------ getPreprocessConfig() ------------------ #

    def getPreprocessConfig(self):
        print('configParser.getCheckcommConfig > Not yet implemented!')

    # ------------------ getProcessConfig() ------------------ #

    def getProcessConfig(self):
        print('configParser.getCheckcommConfig > Not yet implemented!')

    # ------------------ getPostprocessConfig() ------------------ #

    def getPostprocessConfig(self):
        """
        Retreive config informaton for gamit time series manupulations
        returns config dictionary.
        currently implementing 
        {'figDir': standard location for saving figures,
         'prePath': path of older time series data,
         'rapPath': path of time series data from last globk run,
         'totPath': path of the compined time series prePath + rapPath,
         'fTypes': list of figure types to be saved currently png ad ppm
         'pfile': Name of a file containing station plate information
         'coordfile': Name of a file containing station coordinates
         'tiefile': Name of a file containing station ties
         'detrendfile': Name of a file containing detrend information
         }

        how time series are handled needs to reveised prePath, rapPath, totPath config will therefore change soon.

        Implemented by bgo@vedur.is, Nov. 2013

        """

        import os

        config_file = self.CFG_PATH_POSTPROCESS
        config = {'figDir':'','prePath':'','rapPath':'','totPath':'','fTypes':'','pfile':'','coordfile':'','tiefile':'','detrendfile':''}

        try:
            f = open(config_file,'r')
            for line in f:

                # Check for commented lines
                if line.startswith('#') or len(line) == 1:
                    pass
                else:
                    words = line.split()

                    # Break if end of line
                    if words[0] == 'EOC':  
                        break 

                    # Else remove the '=' just leaving the variable name (words[0]) and value (words[1])
                    else:
                        words.remove('=')

                    # Parse config
                    if words[0] == 'figDir': config['figDir'] = os.path.expanduser(words[1])
                    if words[0] == 'prePath': config['prePath'] = os.path.expanduser(words[1])
                    if words[0] == 'rapPath': config['rapPath'] = os.path.expanduser(words[1])
                    if words[0] == 'totPath': config['totPath'] = os.path.expanduser(words[1])
                    if words[0] == 'fTypes': config['fTypes'] = os.path.expanduser(words[1])
                    if words[0] == 'pfile': config['pfile'] = os.path.expanduser(words[1])
                    if words[0] == 'coordfile': config['coordfile'] = os.path.expanduser(words[1])
                    if words[0] == 'tiefile': config['tiefile'] = os.path.expanduser(words[1])
                    if words[0] == 'detremdfile': config['detrenddfile'] = os.path.expanduser(words[1])

        except IOError:
            print('configParser.getGetdataConfig() > File (%s) missing!' % config_file)

        return config


    # The kill function for the object
    def kill(self):
        del self


