# -*- coding: utf-8 -*-

import urllib2
import httplib
import socket

try:
    import ssl
except ImportError:
    import ssl_compat as ssl

class SSLVerificationError(Exception):
    pass

# subclass of HTTPSConnection to do cert verification and domain verification
class VerifiedHTTPSConnection(httplib.HTTPSConnection):
    do_verification = True
    do_domain_verification = True
    certs_file = '/full/path/to/RootCertFile'
    def connect(self):
        # overrides the version in httplib so that we do certificate verification
        try:
            # this is a convenience function added in python 2.6
            sock = socket.create_connection((self.host, self.port), self.timeout)
        except AttributeError:
            # There is no timeout attribute in earlier versions of this object.
            # The only option available is to set a global default timeout for
            # all socket objects.
            socket.setdefaulttimeout(10)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))

        # This code is not available for older versions of python and seems to
        # have no effect on establishing a verified https connection.
        #if self._tunnel_host:
        #    self.sock = sock
        #    self._tunnel()

        # wrap the socket using verification with the Thawte root cert
        if VerifiedHTTPSConnection.do_verification:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.certs_file) 
            if VerifiedHTTPSConnection.do_domain_verification:
                cert_subject = self.sock.getpeercert()['subject']
                cert_dict = {}
                for c in cert_subject:
                    cert_dict.update(c)
                cert_host = cert_dict['commonName']
                if self.host != cert_host:
                    raise SSLVerificationError("Certificate doesn't match domain; untrusted connection")
        else:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file) 

class VerifiedHTTPSHandler(urllib2.HTTPSHandler):
    ''' VerifiedHTTPSHandler wraps https connections with ssl certificate verification '''
    def __init__(self, connection_class = VerifiedHTTPSConnection):
        self.specialized_conn_class = connection_class
        urllib2.HTTPSHandler.__init__(self)
    def https_open(self, req):
        return self.do_open(self.specialized_conn_class, req)

