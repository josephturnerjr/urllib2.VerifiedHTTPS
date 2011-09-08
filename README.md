TL;DR: The VerifiedHTTPSHandler class provides a way to do certificate-verified secure, HTTPS communication with urllib2.

## Motivation 

For Granola (http://grano.la), we needed a way to communicate with our REST server over a cert-verified HTTPS connection. urllib2 (http://docs.python.org/library/urllib2.html) provides a rich interface for opening URLs of various types, but it lacked certificate verification. This class provides an HTTPSHandler subclass (and associated connection class) for doing just that.
