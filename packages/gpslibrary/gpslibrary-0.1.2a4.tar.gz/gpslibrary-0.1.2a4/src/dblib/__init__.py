# ###############################
#
# dblib.py Database Function Library
#
# Code made by fjalar@vedur.is 
# Iceland Met Office
# 2014
#
# ###############################


######## IMPORT LIBRARIES ########

import sys
# mysql library
#import MySQLdb as mdb
# postgresql library
#import _pg
import psycopg2 as pgdb


class dblib:

    # ALL TEXT HERE IN THE DOC NEEDS TO BE REVISED LATER ON
    """A class designed to ....
    
    Public functions:
      getNextBatch()                --
      addReportToDB()               --
      setDebug()                    --

    Private functions:
      No private functions defined.
    """

    def __init__(self,db_info):
        
        # 1 # Predefine few global variables for the class
        self.DEBUG      = False
        self.HOST       = db_info['host']
        self.DBNAME     = db_info['dbname']
        self.USER       = db_info['user']
        self.PASSWORD   = db_info['password']
        self.DB_TABLE   = db_info['dbtable']

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        self.CONNECT_STRING = 'host=%s dbname=%s user=%s password=%s' % (self.HOST,self.DBNAME,self.USER,self.PASSWORD)


    # ------------------ setDebug() ------------------ #

    def setDebug(self):
        """Debug ON/OFF switch - handy when debugging."""
        if self.DEBUG:
            self.DEBUG = False
            print 'Debug OFF'
        else:
            self.DEBUG = True
            print 'Debug ON'    

    # ------------------ getNextBatch() ------------------ #

    def getNextBatch(self):
        """Fetches the next batch number in the checkcomm table from the database to be incremented by 1 and used when the next report is submitted."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print '%s is now running...' % currFunc

        if self.DEBUG: print "%s Connecting to database\n   ->%s" % (currFunc,self.CONNECT_STRING)
        # 2 # Open a connection to the db
        try:
            CONNECTION = pgdb.connect(self.CONNECT_STRING);

        except mdb.Error, e:
            print "%s Error %d: %s" % (currFunc,e.args[0],e.args[1])
            sys.exit(1)


        # Define query
        query_string ="SELECT batch FROM %s ORDER BY batch DESC LIMIT 1;" % self.DB_TABLE #This query finds out which batch was the last.

        # Execute query
        # Use try beause if the table is empty there is no batch number and that causes disgraceful exit.
        # Open a cursor to the connection.
        CURSOR = CONNECTION.cursor()
        if self.DEBUG: print "%s Sending query to the database for the batch number" % currFunc        
        CURSOR.execute(query_string)
        row = CURSOR.fetchone()
        # Use try beause if the table is empty there is no batch number and that causes disgraceful exit.
        try:
            current_batch=row[0]
            if self.DEBUG: print "%s Current batch number is: %s" % (currFunc, current_batch)        
        except:
            current_batch=0

        next_batch = current_batch + 1
        if self.DEBUG: print "%s Next batch number is: %s" % (currFunc, next_batch)        

        CURSOR.close()
        CONNECTION.close()

        return next_batch
    
    # ------------------ addReportToDB() ------------------ #

    def addReportToDB(self,station_info,station_status,next_batch):
        """Adds a checkomm report to the database."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print '%s is now running...' % currFunc

        if self.DEBUG: print "%s Connecting to database\n   ->%s" % (currFunc,self.CONNECT_STRING)
        # 2 # Open a connection to the db
        try:
            CONNECTION = pgdb.connect(self.CONNECT_STRING);

        except mdb.Error, e:
            print "%s Error %d: %s" % (currFunc,e.args[0],e.args[1])
            sys.exit(1)

        # All the data tailoring that happens here below should not be part of this module
        # The data fed to the module should be more unified.

        table = 'checkcomm'
        pos_lat = 0
        pos_lon = 0
        pos_alt = 0
        volt    = 0
        temp    = 0
        receiver= 0
        router  = 0


        # This transform is necessary for the structure of the checkomm table
        if station_status['connection']['router'] and station_status['connection']['router'] != 'N/N' and station_status['connection']['router'] != 'False':
            router = 1 

        if station_status['connection']['receiver'] and station_status['connection']['receiver'] != 'N/N' and station_status['connection']['receiver']     != 'False' :
            receiver = 1

        # This checks if the temp value is a number or not. If this fails then the default value, 0, just stays 0
        try:
            float(station_status['temp']['value'])
            temp = station_status['temp']['value'] 
        except:
            pass

        # This checks if the volt value is a number or not. If this fails then the default value, 0, just stays 0
        try:
            float(station_status['volt']['value'])
            volt = station_status['volt']['value'] 
        except:
            pass

        # This checks if latitude, longitude and altitude exist under 'value' and saves the values.
        try:
                float(station_status['position']['value']['longitude'])
                pos_lon = station_status['position']['value']['longitude']
        except:
            pass

        try:
                float(station_status['position']['value']['altitude'])
                pos_alt = station_status['position']['value']['altitude']
        except:
            pass

        try:
                float(station_status['position']['value']['latitude'])
                pos_lat = station_status['position']['value']['latitude']
        except:
            pass


        if station_info['proxy']['user'] == 'sil':
            router_ip = 'localhost'
        else:
            router_ip = station_info['router']['ip']

        # Next assemble a data variable 
        data = (
                station_info['station']['id'],
                router_ip,
                router,
                receiver,
                temp,
                volt,
                next_batch,
                pos_lat,
                pos_lon,
                pos_alt)

        
        if self.DEBUG: print "%s data to be sent: %s" % (currFunc,data)

        # Then, define a query
        insert_string ="INSERT INTO %s (sid, ip, rout_stat, recv_stat, recv_temp, recv_volt, batch, pos_lat, pos_lon, pos_alt) VALUES('%%s' , '%%s' , '%%s', '%%s', '%%s', '%%s', '%%s', '%%s', '%%s', '%%s');" % self.DB_TABLE

        if self.DEBUG: print "%s Just about to execute the 'put' command with string: %s " % (currFunc, insert_string)

        query_string = insert_string % data

        if self.DEBUG: print "%s Query string: %s" % (currFunc,query_string)

        # FINALLY : Execute query
        # Use try beause if the table is empty there is no batch number and that causes disgraceful exit.
        # Open a cursor to the connection.
        CURSOR = CONNECTION.cursor()

        if self.DEBUG: print "%s Sending data to database" % currFunc

        try:
            CURSOR.execute(query_string)

        except Exception , e:
            print 'ERROR:', e[0]
        
            

        CURSOR.close()
        CONNECTION.commit()
        CONNECTION.close()

    # ------------------ checkIfFileExists() ------------------ #
    def checkIfFileExists(self):
        """Checks if file metadata exists in the database."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if p_args['debug']: print '%s is now running...' % currFunc

    # ------------------ addFileToDB() ------------------ #
    def addFileToDB(self):
        """Adds file metadata to the database."""

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if p_args['debug']: print '%s is now running...' % currFunc

