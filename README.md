TL;DR: The VerifiedHTTPSHandler class provides a way to do certificate-verified secure, HTTPS communication with urllib2.

## Motivation 

For Granola (http://grano.la), we needed a way to communicate with our REST server over a cert-verified HTTPS connection. urllib2 (http://docs.python.org/library/urllib2.html) provides a rich interface for opening URLs of various types, but it lacked certificate verification. This class provides an HTTPSHandler subclass (and associated connection class) for doing just that.

## Example

See the file example.py for example usage. Note that the handler will do domain verification as well (assuming the flag is set), but I don't have a server with an installed signed cert with the wrong domain to test against.
