#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import settings
import urllib2
import time

class Smser(object):
    
    def __init__(self):
        ''' Initialize the Smser object with parameters used in the Backend to Send our text  ... as defined by the system '''

        self.url        = settings.SMPP_URL
        self.username   = settings.SMPP_USERNAME
        self.password   = settings.SMPP_PASSWORD    
	
	
    def send_message_via_kannel(self, phonenumber, messagetext):
	
        try:
            url = "%s?to=%s&text=%s&password=%s&user=%s" % (
                                                                self.url,
                                                                urllib2.quote(phonenumber.strip()), 
                                                                urllib2.quote(messagetext),
                                                                self.password,
                                                                self.username
                                                            )

            f = urllib2.urlopen(url, timeout=10)
            if f.getcode() / 100 != 2:
                print "Error delivering message to URL: %s" % url
                raise RuntimeError("Got bad response from router: %d" % f.getcode())

            # do things at a reasonable pace
            time.sleep(.2)
            return True
        except KeyError:
            return False




	

