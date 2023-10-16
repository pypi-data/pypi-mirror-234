################################
#
# connect.py 
#
# Code made by fjalar@vedur.is 
# Iceland Met Office
# 2011-2012
#
# ###############################


######## IMPORT LIBRARIES ########

#import sys, re, subprocess, getopt, pyinotify, socket, os, serial
import sys, subprocess
#from time import sleep, time


class Connect:

    # ALL TEXT HERE IN THE DOC NEEDS TO BE REVISED LATER ON
    """A class designed to simplify communications between central server and equipment over different protocols and located behinds long links of connections.
    
    Public functions:
    open                -- 
    close               -- 
    getStatus           -- 


    Private functions:
    __openSSH           -- 
    __closeSSH          --
    __checkSSH          --
    __openSerial        --
    __closeSerial       --
    __checkSerial       --
    __openPOT           --
    __closePOT          --
    """

    def __init__(self,stationInfo):
        
        # 1 # Parameters saved and type set to string
        self.DEBUG = False
        self.TUNNEL_UP = 'Tunnel is up'
        self.TUNNEL_DOWN = 'Tunnel is down'

        # 2 # The info parameter is a dictionary that contains five other dictionaries as seen here below, 
        # provided by the configParser from the station config file:
        self.station    = stationInfo['station']    # id, name   
        self.receiver   = stationInfo['receiver']   # type, ip, httpport, ftpport, telnetport, serialport, 
                                                    # ...rtpport, reftekport, user, pwd, serv, baud, parity, rtscts
        self.connection = stationInfo['connection']    # type, ppp, port
        self.proxy      = stationInfo['proxy']        # user, server, host, httpport, ftpport, serialport
        self.router     = stationInfo['router']     # type, ip, phonenumber, portforward
        self.dialup     = stationInfo['dialup']     # device, phoneneumber, meth, server
        self.url        = 'locahost:%s' % self.proxy['httpport'] # self.url is returned by Connect() as the address for the port-forward.

    # ------------------ connect() ------------------ #

    def connect(self, reset=False):
        """This function opens a new connection for local tunnel and Proxy tunnel if they are down. If RESET is required, tunnels that already are up are shut down and new created."""

        # 1 # Name of the current module
        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print '%s connect() is now running... ' % currFunc

        # 2 # Define variables
        result = {'url':'','status':'','comm':''}

        # 3 # Establish connections
        # 3.1 # CONNECTION TYPE: IP direct connections
        if 'IP' in self.connection['type']  and 'direct' in self.connection['type']:

            # 3.1.1 Define variables        
            tunnel = 'direct'

            # 3.1.2 Mix results and done!
            result['url'] = '%s:%s' % (self.router['ip'],self.receiver['httpport'])
            result['status'] = 'ready'
            result['comm'] = 'Direct connection. No tunnels'

        # 3.2 # CONNECTION TYPE: IP via host connections             
        if 'IP' in self.connection['type']  and 'host' in self.connection['type'] and not 'sshserver' in self.connection['type']:

            # 3.2.1 Define variables
            #tunnel ={'local':'','comm':''}

           # 3.3.2 # Check current SSH status
            tunnel = self.__checkSSHTunnel('local')   # Check connection status

            # 3.2.3 If reset required and tunnel is up... take it down..
            if reset: 
                if self.DEBUG: print '%s Reset in progress...' % currFunc
                if tunnel['status'] == self.TUNNEL_UP:
                    tunnel = self.__closeSSHTunnel('local')  # If up; close localhost tunnel
                    if self.DEBUG: print '%s Localhost tunnel status: %s' % (currFunc, tunnel['status'])

            # 3.2.4 # Check the local tunnel and open if down
            if tunnel['status'] == self.TUNNEL_DOWN:  
                if self.DEBUG: print '%s Local tunnel is down. Opening one now...' % currFunc            
                tunnel = self.__openSSHTunnel('local')    # If everything else fails, open connection.
                if self.DEBUG: print '%s Local tunnel status: %s' % (currFunc, tunnel['status'])

            # 3.2.5 Mix results and done!!
            result['url'] = 'localhost:%s' % self.proxy['httpport']
            if tunnel['status'] == 'Tunnel is up':
                result['status'] = 'ready'
            else:
                result['status'] = 'not ready'
            
            result['comm'] = tunnel 


        # 3.3 # CONNECTION TYPE: IP via ssh_server via host connections             
        if 'IP' in self.connection['type']  and 'host' in self.connection['type'] and 'sshserver' in self.connection['type']:

            # 3.3.1 Define variables
            tunnel ={'local':'','local_comm':'','proxy':'','proxy_comm':''}
            
            # 3.3.2 # Check current SSH status
            tunnel_proxy = self.__checkSSHTunnel('proxy')   # Check connection status
            tunnel_local = self.__checkSSHTunnel('local')   # Check connection status

           # 3.3.3 # If reset required and tunnel is up... take it down..
            if reset: 
                if self.DEBUG: print '%s Reset in progress...' % currFunc
                if tunnel_local['status'] == self.TUNNEL_UP:
                    tunnel_local = self.__closeSSHTunnel('local')  # If up; close localhost tunnel
                    if self.DEBUG: print '%s Localhost tunnel status: %s' % (currFunc, tunnel_local['status'])
                if tunnel_proxy['status'] == self.TUNNEL_UP:
                    tunnel_proxy = self.__closeSSHTunnel('proxy')    # If up; close Proxy tunnel
                    if self.DEBUG: print '%s Proxy tunnel status: %s' % (currFunc, tunnel_proxy['status'])

            # 3.3.3 # Check the local tunnel and open if down
            if tunnel_local['status'] == self.TUNNEL_DOWN:  
                if self.DEBUG: print '%s Local tunnel is down. Opening one now...' % currFunc            
                tunnel_local = self.__openSSHTunnel('local')    # If everything else fails, open connection.
                if self.DEBUG: print '%s Local tunnel status: %s' % (currFunc, tunnel_local['status'])

            # 3.3.4 # Check the Proxy tunnel and open if down
            if tunnel_proxy['status'] == self.TUNNEL_DOWN:  
                if self.DEBUG: print '%s Proxy tunnel is down. Opening one now...' % currFunc            
                tunnel_proxy = self.__openSSHTunnel('proxy')    # If everything else fails, open connection.
                if self.DEBUG: print '%s Proxy tunnel status: %s' % (currFunc, tunnel_proxy['status'])

            # 3.3.6 check the status once more and return the results
            tunnel_proxy = self.__checkSSHTunnel('proxy')
            tunnel['proxy'],tunnel['proxy_comm'] = tunnel_proxy['status'],tunnel_proxy['comm']
            tunnel_local = self.__checkSSHTunnel('local')
            tunnel['local'],tunnel['local_comm'] = tunnel_local['status'],tunnel_local['comm']

            # 3.3.7 Mix results and done!!
            result['url'] = 'localhost:%s' % self.proxy['httpport']
            if tunnel['local'] == 'Tunnel is up' and tunnel['proxy'] == 'Tunnel is up':
                result['status'] = 'ready'
            else:
                result['status'] = 'not ready'
            
            result['comm'] = tunnel 

        # 3.4 # CONNECTION TYPE: SERIAL via host connections 
        if 'SERIAL' in self.connection['type']  and 'host' in self.connection['type']:
            print 'IP and host'


        # 3.5 # CONNECTION TYPE: SERIAL via ssh_server via host connections 
        if 'SERIAL' in self.connection['type']  and 'host' in self.connection['type'] and 'sshserver' in self.connection['type']:
            print 'IP, host and sshserver'


        # 4 # Return        
        return result

    # ------------------ disconnect() ------------------ #

    def disconnect(self):
        # Name of the current module
        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print '%s disconnect() is now running...' % currFunc
 
        result = {'status':'','comm':''}

        # 3.1 # CONNECTION TYPE: IP direct connections
        if 'IP' in self.connection['type']  and 'direct' in self.connection['type']:
            result = {'status':'Nothing to disconnect'}

        # 3.2 # CONNECTION TYPE: IP via host connections             
        if 'IP' in self.connection['type']  and 'host' in self.connection['type'] and not 'sshserver' in self.connection['type']:

            # 3.2.1 # Request the tunnels be closed
            tunnel = self.__closeSSHTunnel('local')

            # 3.2.2 # Manage the limited results accordingly and mix final result
            if tunnel['status'] == 'Tunnel is down':
                result['status'] = tunnel['status']
                result['comm'] = tunnel['comm']
                 
            if tunnel['status'] != 'Tunnel is down':
                result['status'] = 'Local tunnel is still up'
                result['comm'] = tunnel['comm']

        # 3.3 # CONNECTION TYPE: IP via ssh_server via host connections             
        if 'IP' in self.connection['type']  and 'host' in self.connection['type'] and 'sshserver' in self.connection['type']:
            
            # 3.3.1 # Request the tunnels be closed
            tunnel_proxy = self.__closeSSHTunnel('proxy')
            tunnel_local = self.__closeSSHTunnel('local')

            # 3.3.2 # Manage the limited results accordingly and mix final result
            if tunnel_proxy['status'] == 'Tunnel is down' and tunnel_local['status'] == 'Tunnel is down':
                result['status'] = 'All tunnels are down'
                result['comm'] = ''
                 
            if tunnel_proxy['status'] == 'Tunnel is down' and tunnel_local['status'] != 'Tunnel is down':
                result['status'] = 'Local tunnel is still up'
                result['comm'] = tunnel_local['comm']

            if tunnel_proxy['status'] != 'Tunnel is down' and tunnel_local['status'] == 'Tunnel is down':
                result['status'] = 'Proxy tunnel is still up'
                result['comm'] = tunnel_proxy['comm']

            if tunnel_proxy['status'] != 'Tunnel is down' and tunnel_local['status'] != 'Tunnel is down':
                result['status'] = 'Both tunnels are still up'
                result['comm'] = (tunnel_proxy['comm'],tunnel_local['comm'])

        # 3.4 # CONNECTION TYPE: SERIAL via host connections 
        if 'SERIAL' in self.connection['type']  and 'host' in self.connection['type']:
            print 'IP and host'

        # 3.5 # CONNECTION TYPE: SERIAL via ssh_server via host connections 
        if 'SERIAL' in self.connection['type']  and 'host' in self.connection['type'] and 'sshserver' in self.connection['type']:
            print 'IP, host and sshserver'


        return result
    # ------------------ checkStatus() ------------------ #

    def getStatus(self):
        # Name of the current module
        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        if self.DEBUG: print '%s getStatus() is now running...' % currFunc
        
        result = {'status':'','comm':''}

        # 3.1 # CONNECTION TYPE: IP direct connections
        if 'IP' in self.connection['type']  and 'direct' in self.connection['type']:
            result = {'status':'Direct connection. No tunnels.'}

        # 3.2 # CONNECTION TYPE: IP via host connections             
        if 'IP' in self.connection['type']  and 'host' in self.connection['type'] and not 'sshserver' in self.connection['type']:

            result = self.__checkSSHTunnel('local')

            if self.DEBUG: 
                if result['status'] != '': print 'Tunnel on localhost: %s' % result['status']
                if result['comm'] != '': print 'Message on localhost: %s' % result['comm']


        # 3.3 # CONNECTION TYPE: IP via ssh_server via host connections             
        if 'IP' in self.connection['type']  and 'host' in self.connection['type'] and 'sshserver' in self.connection['type']:

            result = {'local':'','local_comm':'','proxy':'','proxy_comm':''}
            tunnel_proxy = self.__checkSSHTunnel('proxy')
            tunnel_local = self.__checkSSHTunnel('local')

            result['proxy'],result['proxy_comm'] = tunnel_proxy['status'],tunnel_proxy['comm']
            result['local'],result['local_comm'] = tunnel_local['status'],tunnel_local['comm']

            if self.DEBUG: 
                if result['local'] != '': print 'Tunnel on localhost: %s' % result['local']
                if result['local_comm'] != '': print 'Message on localhost: %s' % result['local_comm']
                if result['proxy'] != '': print 'Tunnel on Proxy server: %s' % result['proxy']
                if result['proxy_comm'] != '': print 'Message on Proxy server: %s' % result['proxy_comm']

        # 3.4 # CONNECTION TYPE: SERIAL via host connections 
        if 'SERIAL' in self.connection['type']  and 'host' in self.connection['type']:
            print 'IP and host'

        # 3.5 # CONNECTION TYPE: SERIAL via ssh_server via host connections 
        if 'SERIAL' in self.connection['type']  and 'host' in self.connection['type'] and 'sshserver' in self.connection['type']:
            print 'IP, host and sshserver'

        
        return result

    # ------------------ setDebug() ------------------ #

    def setDebug(self):
        """Debug ON/OFF switch."""
        if self.DEBUG:
            self.DEBUG = False
            print 'Debug OFF'
        else:
            self.DEBUG = True
            print 'Debug ON'    
    
    # ------------------ info ------------------ #

    def info(self):
        print 'Station ID: ', self.station['id']
        print 'Connection type: ', self.connection['type']
        if 'proxy' in self.connection['type']:
            print 'Proxy server: ',self.proxy['sshserver']
            print 'Proxy host: ',self.proxy['host']
        else:
            print 'Router IP: ', self.router['ip']
        print '....'


    #------------------- __openSSHTunnel ------------------- #

    def __openSSHTunnel(self,location=''):

        # 1 # Define variables
        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'    # Name of the current module 
        if self.DEBUG: print '%s _openSSHTunnel() is now running for location >> %s <<' % (currFunc, location) 

        result = {'status':'','comm':''}        

        # For "few" (one) station the ssh port is defined differently from the standard 22
        sshport = ''
        if 'sshserver' in self.connection['type']: 
            if location == 'proxy' and self.connection['sshport'] != '':
                if self.DEBUG: print ' %s Different ssh port defined for proxy connection: %s ' % (currFunc, self.connection['sshport'])
                sshport = '-p %s' % self.connection['sshport']
        elif 'host' in self.connection['type'] and not 'sshserver' in self.connection['type']:
            if location == 'local' and self.connection['sshport'] != '':
                if self.DEBUG: print '%s Different ssh port defined for local connection: %s ' % (currFunc, self.connection['sshport'])
                sshport = '-p %s' % self.connection['sshport']

        # Do we need a local tunnel?        
        if location == 'local':

            if 'sshserver' not in self.connection['type']:
                command = "ssh %s -fqN -L %s:%s:%s %s@%s" % (sshport, self.proxy['httpport'],self.receiver['ip'],self.receiver['httpport'],self.proxy['user'],self.proxy['host'])
            else:
            # SSH shell command to open a ssh tunnel between host <-> proxy <-> destionation
                command = "ssh %s -fqN -L %s:localhost:%s %s@%s" % (sshport, self.proxy['httpport'],self.proxy['httpport'],self.proxy['user'],self.proxy['sshserver'])        
            if self.DEBUG: print '%s Command to open local tunnel: %s' % (currFunc, command)

            # WARNING:
            #   process.communicate(), the stout communication, can not be saved to a variable here. 
            #   The ssh tunnel goes into background but the python process will hang and wait for the stout
            #   which never comes back...

            # 2 # Execute the command
            return_code, return_comm = self.__shellComm(command, comm='no') # Execute shell command and return code. Communication cannot be saved here. 
            
            # 3 # Manage the output accordingly
            if self.DEBUG: print '%s process.returncode: %s' % (currFunc , return_code)

            if return_code == 0:
                result['status'],result['comm'] = (self.TUNNEL_UP,return_comm)
                if self.DEBUG: print '%s Tunnel is up!' % currFunc
            elif return_code == 255:
                result['status'],result['comm'] = ('Connection timed out...',return_comm)
                if self.DEBUG: print '%s Connection timed out. Return code: %s' % (currFunc , return_code) 
            else:
                result['status'], result['comm'] = ('Tunnel failed to open.', return_comm)
                if self.DEBUG: print return_code

        # Do we need a local tunnel?
        if location == 'proxy':    
            # 4.3.1 # Define variables

            command = "ssh -t %s@%s 'ssh %s -fqN -L %s:%s:%s %s@%s'" % (   self.proxy['user'],self.proxy['sshserver'], sshport, self.proxy['httpport'],self.receiver['ip'],
                                                                        self.receiver['httpport'],self.proxy['user'],self.proxy['host'])
            
            if self.DEBUG: print '%s Command to open Proxy tunnel: %s' % (currFunc , command)

            # 4.3.2 # Execute command

            # WARNING:
            #   process.communicate(), the stout communication, can not be saved to a variable here. 
            #   The ssh tunnel goes into background but the python process will hang and wait for the stout
            #   which never comes back...

            return_code, return_comm = self.__shellComm(command,comm='no')
            if self.DEBUG: print '%s process.returncode: %s ' % (currFunc, return_code)

            if return_code == 0:
                result['status'],result['comm'] = (self.TUNNEL_UP,return_comm)
                if self.DEBUG: print '%s Tunnel is up!' % currFunc
            elif return_code == 255:
                result['status'],result['comm'] = ('Connection timed out...',return_comm)
                if self.DEBUG: print '%s Connection timed out. Return code: %s' % (currFunc , return_code) 
            else:
                result['status'], result['comm'] = ('Tunnel failed to open.', return_comm)
                if self.DEBUG: print return_code

        # 4 # Return returncode and port number
        return result

    #------------------- __checkSSHTunnel------------------- #

    def __checkSSHTunnel(self,location=''):
        """ This function checks if tunnel is up and active on the localhost and on a Proxy server, if needed."""

        # 1 # Define variables 
        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name
        result = {'status':'','comm':''}

        if self.DEBUG: print '%s _checkSSHTunnel() is now running for location >> %s <<' % (currFunc, location)
        
        if location == 'local': # 2 # Check local tunnel

            # 2.1 # Define a 'find tunnel' command with ps... look into suggestion from olstar.
            command = "ps -ef | grep 'ssh' | grep %s | grep -v root | awk '{print $2}'" % self.proxy['httpport']
            if self.DEBUG: print '%s Command to find process on localhost: %s' % (currFunc, command)

            # 2.2 # Execute command
            return_code, return_comm = self.__shellComm(command,comm='yes')        

            # 2.3 # Process return code and communication
            if return_code == 0:
                if return_comm != '': #if the result contains some information...
                    if self.DEBUG: print '%s Open tunnel found on localhost with process number: %s' % (currFunc, return_comm)
                    result['status'],result['comm'] = (self.TUNNEL_UP, return_comm) # Save results to result dictionary
                else:
                    if self.DEBUG: print '%s No tunnel found on localhost...' % (currFunc)
                    result['status'],result['comm'] = (self.TUNNEL_DOWN,return_comm) # Save results to result dictionary
            else:
                print '%s Error in running command | Returncode: %s | Return comm: %s'% (currFunc, return_code, return_comm)

        if location == 'proxy': # 3 # Check Proxy tunnel

            # 3.1 # Define a 'find tunnel' command with ps... look into suggestion from olstar.
            command = "ssh -t %s@%s 'sh /usr/sil/gps/bin/find_tunnel.sh %s %s'" % (self.proxy['user'],self.proxy['sshserver'],self.proxy['httpport'],self.receiver['ip'])
            if self.DEBUG: print '%s Command to find process on Proxy server: %s' % (currFunc,command)

            # 6.2 # Execute the command.
            return_code, return_comm = self.__shellComm(command,comm='yes')        
            
            # 6.3 # Process return code and communication
            if return_code == 0:
                if return_comm != '': #if the result contains some information...
                    if self.DEBUG: print '%s Open tunnel found on Proxy server with process number: %s' % (currFunc, return_comm)
                    result['status'],result['comm'] = (self.TUNNEL_UP, return_comm) # Save results to result dictionary
                else:
                    if self.DEBUG: print '%s No tunnel found on Proxy server...' % (currFunc)
                    result['status'],result['comm'] = (self.TUNNEL_DOWN,return_comm) # Save results to result dictionary
            else:
                print '%s Error in running command | Returncode: %s | Return comm: %s'% (currFunc, return_code, return_comm)

        return result
    
    #------------------- __closeSSHTunnel ------------------- #

    def __closeSSHTunnel(self,location=''):
        """ This function closes ssh tunnels on localhost and Proxy server """

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>' # module.object name

        result = {'status':'','comm':''}

        if self.DEBUG: print '%s __closeSSHTunnel() is now running for location >> %s <<' % (currFunc, location)

        if location == 'proxy':

            result = self.__checkSSHTunnel('proxy')

            if result['status'] == self.TUNNEL_UP:
        
                #(3a)# Define 'Close tunnel' command
                if self.DEBUG: print "%s Tunnel process found on Proxy server and will be closed now." % currFunc
                command = "ssh -t %s@%s 'kill %s'" % (self.proxy['user'],self.proxy['sshserver'],result['comm'])
                if self.DEBUG: print '%s Command to close tunnel on Proxy server: %s' % (currFunc,command)

                return_code, return_comm = self.__shellComm(command,comm='yes')

                if return_code == 0:
                    if self.DEBUG: print '%s Tunnel on Proxy server has been closed.' % currFunc
                    result['status'],result['comm'] = self.TUNNEL_DOWN, return_comm
                else:
                    if self.DEBUG: print '%s Problem closing tunnel on Proxy server | Return code: %s.' % (currFunc, return_code)
                    result['status'],result['comm'] = self.TUNNEL_DOWN, 'Problem closing tunnel on Proxy server: %s' % return_code
  

        if location == 'local':

            result = self.__checkSSHTunnel('local')

            if result['status'] == self.TUNNEL_UP:
        
                #(3a)# Define 'Close tunnel' command
                if self.DEBUG: print "%s Tunnel process found on localhost and will be closed now." % currFunc
                command = "kill %s" % result['comm']

                if self.DEBUG: print '%s Command to close tunnel on localhost: %s' % (currFunc,command)

                return_code, return_comm = self.__shellComm(command,comm='yes')

                if return_code == 0:
                    if self.DEBUG: print '%s Tunnel on localhost has been closed.' % currFunc
                    result['status'],result['comm'] = self.TUNNEL_DOWN, return_comm
                else:
                    if self.DEBUG: print '%s Problem closing tunnel on localhost | Return code: %s.' % (currFunc, return_code)
                    result['local'],result['comm'] = self.TUNNEL_DOWN,'Problem closing tunnel on localhost: %s' % return_code

        return result
        
 
    #------------------- __shellComm ------------------- #

    def __shellComm(self,command,comm='yes'):
        """ This command executes shell commands and returns the results"""

        return_code = ''
        return_comm = ''

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'

        if self.DEBUG: print '%s __shellComm() is now running...' % currFunc

        process = subprocess.Popen( command , shell=True , stdout=subprocess.PIPE) 
        process.wait()
        return_code = process.returncode

        if comm == 'yes':
            return_comm = process.communicate()[0].strip('\n').strip('\r') # strip out the extra hidden characters (newline and carrage return)

        if self.DEBUG: print '%s process.returncode: %s ' % (currFunc, return_code)

        return return_code, return_comm       

