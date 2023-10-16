import pycurl, cStringIO, sys

class sCurl():

    # ALL TEXT HERE IN THE DOC NEEDS TO BE REVISED LATER ON
    """A simple CURL class to provide a simple interface on top of pycurl.
    Public functions:
    getURL     -- Get the url for the passed argument.
    info       -- Reports information on the object.
    """

    def __init__(self):
    
    # instantiate pycurl object
        self.curl = pycurl.Curl()


   
    def getURL(self,url,userpass, DEBUG):

        currFunc=__name__+'.'+sys._getframe().f_code.co_name+' >>'
        
        #print 'getURL called witu URL sting: ',url_string        
        # set variables
        result = {'value':None,'error':None}
        response = ''
        error = ''

        # curl magic
        buf = cStringIO.StringIO()             
        
        try:
            self.curl.setopt(self.curl.URL, url)
	    self.curl.setopt(pycurl.CONNECTTIMEOUT, 4)
	    self.curl.setopt(pycurl.TIMEOUT, 4)
	    self.curl.setopt(pycurl.NOSIGNAL, 4)

            if userpass: self.curl.setopt(self.curl.USERPWD, userpass['user'] + ":" +  userpass['pass'])

            self.curl.setopt(self.curl.WRITEFUNCTION, buf.write)
            self.curl.perform()
            result['value'] = buf.getvalue()

            if DEBUG: print '%s Value retrieved: %s URL: %s' % (currFunc,result['value'],url)
        
        except pycurl.error, error:
            errno, errstr = error
            result['error'] = errstr
            if DEBUG: print '%s An error occurred: %s - URL: %s' % (currFunc,errstr,url)
        
        buf.close()

        return result
