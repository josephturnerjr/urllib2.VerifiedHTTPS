import urllib2
from VerifiedHTTPS import *


def read_granola():
    # create the handler
    #   this handler will use the cert file specified above
    https_handler = VerifiedHTTPSHandler()
    # build the urllib2 opener, using the VerifiedHTTPS handler
    url_opener = urllib2.build_opener(https_handler)
    # build the request object
    req = urllib2.Request("https://grano.la")
    # get a handle to the url
    handle = url_opener.open(req)
    # read data from the url
    response = handle.read()
    print response

def main():
    # set the certificate file 
    #   grano.la uses a Thawte-signed SSL cert
    VerifiedHTTPSConnection.certs_file = 'thawte.pem'
    read_granola()
    # an attempt to read the URL with the wrong cert 
    #   (verisign root in this case) will result in an SSL exception
    VerifiedHTTPSConnection.certs_file = 'verisign.pem'
    read_granola() # will raise a urllib2.UrlError with SSL error information

if __name__ == "__main__":
    main()
    
