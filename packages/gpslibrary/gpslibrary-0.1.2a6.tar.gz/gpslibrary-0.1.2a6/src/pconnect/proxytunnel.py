#!/usr/bin/python
# -*- coding: utf-8 -*-

# ###############################
#
# proxytunnel.py
# Code made by fjalar@vedur.is
# Iceland Met Office
# 2013-2014
#
# ###############################


import cparser as parser, pconnect as connect
import sys, getopt,re

def run(p_args):

    # 1 # instatniate a parser object with a specific station
    Parser = parser.Parser()
    #print "Check #1"

    # 2 # get station info for that station
    if p_args['debug']: print "Station: %s" % p_args['sid']
    info = Parser.getStationInfo(p_args['sid'])
    if p_args['debug']: print "Check #2"
    if p_args['debug']: print "INFO: ",info

    # 3 Check if everything is ok
    if info: 

        # 4 # instantiate a connection object for a specific station
        Connection = connect.Connect(info)
        #print "Check #3"

        # 5 # enable debug
        if p_args['debug']: Connection.setDebug()


        if p_args['action'] == 'open':

	    print "Action: Open connection for %s" % p_args['sid']

	    # 6a # Try disconnect existing connection first - this is done twice just to be sure 
	    status_dis_1 = Connection.disconnect()
	    status_dis_2 = Connection.disconnect()

            # 7a # finally connect and catch the status output in the status variable
            status_con = Connection.connect()

	    # 8a # report if not silent
            if p_args['report'] != 'norep': 
	        print status_dis_1
	        print status_dis_2
	        print status_con


        elif p_args['action'] == 'close':

            print "Action: Close connection for %s" % p_args['sid']

            # 6b # Disconnect existing connection
            status_dis_1 = Connection.disconnect()
            status_dis_2 = Connection.disconnect()

            # 7b # report if not silent
            if p_args['report'] != 'norep':
                print status_dis_1
                print status_dis_2

    else:
       print "ERROR: Problem with config file"

######## function - HELP SCREEN #######

def helpScreen():

    # Only help info here
    print "ProxyTunnel is a tunneling through proxy tool that opens a tunnel connection through a proxy to an GPS equipment"
    print ""
    print "Usage:"
    print "  proxytunnel [OPTIONS] [ARGUMENS]"
    print ""
    print "Examples:"
    print "  (1) proxytunnel -o GOLA   - Opens a connection to the GPS station GOLA through proxies kjarni and god"
    print "  (2) proxytunnel -c FTEY   - Closes a connection to the GPS station FTEY through proxies kjarni and fla"
    print ""
    print "Opitions:"
    print "  -o, --open=[station id]       Open a connection."
    print "  -c, --close=[station id]      Close a open/live connection."
    print "  -v, --verbose                 Verbose reporting."
    print "  -n, --no-report               No reporting - Quiet mode."
    print "  -d, --debug                   Print out debug information."
    print ""
    print "Default reporting level is modest."
    print ""


######## function - PROGRAM INFO SCREEN #######

def progInfoScreen():

    # Only splash screen info here
    print ""
    print "Copyright (c) 2013-2014 Icelandic Met Office"
    print "ProxyTunnel 0.1 (21st of November 2013)"
    #print ""

######## function - PROGRAM ERROR OUTPUT SCREEN #######

def errorScreen(message):

    helpScreen()
    print ""
    print "ERROR: %s" % message


def main():


    currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
    progInfoScreen()
    sid = []

    # Variables defined

    p_args = {'sid':None,'report':'default','debug':None}
    # 'report' can be norep, default or verbose. Default is 'default'
    # 'file' is station-list.cfg as default and the file is located under ../../cofigs/ directory.

    # Option and argument parser.

    try:
        opts, args = getopt.getopt(sys.argv[1:],"dhocvn", ["debug","help","open","close","verbose","no-reporting"])
        # semicolon following a option stands for an argument
    except getopt.error, msg:
        helpScreen() #Print out the help screen
        print "ERROR: ", msg
        sys.exit(2)

    # DEBUG
    #print len(sys.argv[1:])
    #print sys.argv[1:]
    #for option, argument in opts:
        #print "option: ",option
        #print "argument: ",argument
    #sys.exit(2)
    # DEBUG

    # If there are no arguments or options print out the help screen.
    if len(sys.argv[1:]) == 0:
        helpScreen()

    # Else, process the options and arguments.
    else:

        for option, argument in opts:
            if option in ("-d","--debug"):
                #print "option: %s " % option
                 p_args['debug'] = 1
                 print "Option(s): %s " % option

            elif option in ("-h", "--help"):
                helpScreen()
                #print "option: %s  a: %s" % (option,argument)
                sys.exit(0)

            elif option in ("-o","--open"):
                p_args['action'] = 'open'
                #p_args['sid'] = argument
                #print "option: %s " % option

            elif option in ("-c","--close"):
                p_args['action'] = 'close'
                #p_args['sid'] = argument
                #print "option: %s " % option

            elif option in ("-v","--verbose"):
                print "option: %s " % option
                #p_args['report'] = 'verbose'

            elif option in ("-n","--no-reporting"):
                print "option: %s" % option

            else:
                assert False, "unhandled option"

        if p_args['debug']: print 'Arguments: ', args
        try:
            if p_args['debug']: print "%s in the try-except method" % currFunc

            matchObj = re.search( r'[A-Z][A-Z][A-Z][A-Z0-9]', args[0], flags=0)
            if matchObj:
                sid.append(matchObj.group())
            
                if p_args['debug']: print "%s >> %s will be processed..." % (currFunc,matchObj.group())

                p_args['sid'] = matchObj.group()
                run(p_args)

        except:
            errorScreen('Station ID missing. Use ALL to process all stations or give a specific station ID, e.g. SOHO')
            sys.exit(0)



if __name__=="__main__":
     main()
