# ###############################
#
# checkPort.py 
#
# Code made by fjalar@vedur.is 
# Iceland Met Office
# 2014
#
# ###############################

######## IMPORT LIBRARIES ########

import socket, sys


        # NOTE: There is no PING check in this version of the module but should be part of it.
        #       The result is that less is known about the connection - is it the IP(router) that is not picking up
        #       or is it the receiver behind the port. 
        #       FUTURE DEVELOPER: look into paramiko or similar mouduels.

def isOpen(ip,receiver_port,DEBUG = False):

    #print "IP for checkPort: %s:%s" % (ip,port)
    currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'    

    result = {'router':None,'receiver':None}
    router_port = '80'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if DEBUG: print "%s Checking IP: %s SOCKET: %s" % (currFunc,ip,receiver_port)
        s.settimeout(5)
        s.connect((ip, int(receiver_port)))
        s.settimeout(None)
        s.close()
        if DEBUG: print "%s Receiver success!" % currFunc
        result['router'] = True
        result['receiver'] = True

    except:
        if DEBUG: print "%s RECEIVER socket failed" % currFunc 
        result['receiver'] = False


    ## Althoug the socket to the receiver is down, the router may be up. Let's check that out.
    if result['receiver'] == False and ip != "localhost":
        if DEBUG: print "%s Cheking the Router next..." % currFunc

        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            if DEBUG: print "%s Checking IP: %s SOCKET: %s" % (currFunc,ip,router_port)
            s2.settimeout(3)
            s2.connect((ip, int(router_port)))
            s.settimeout(None)
            s2.close()
            if DEBUG: print "%s Router success!" % currFunc
            result['router'] = True

        except:
            if DEBUG: print "%s ROUTER socket failed" % currFunc 
            result['router'] = False

    # we have to handle 'localhost' and the ssh tunnels differently because the connection through them cannot be easily checked
    # if the equipment at the end of the tunnel does not answer. The answer given is simply N/N - not known.
    elif result['receiver'] == False and ip == 'localhost':
    
        result['router'] = 'N/N'
        
    
    return result
