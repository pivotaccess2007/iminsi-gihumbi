#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
import urllib2
import time

class Smser(object):
    help = "To send SMS"	
	
    def send_message_via_kannel(self, identity, message):
	
        try:
            conf = settings.INSTALLED_BACKENDS

            url = "%s?to=%s&text=%s&password=%s&user=%s" % (
                conf['kannel-smpp']['sendsms_url'],
                urllib2.quote(identity.strip()), 
                urllib2.quote(message),
                conf['kannel-smpp']['sendsms_params']['password'],
                conf['kannel-smpp']['sendsms_params']['username'])

            f = urllib2.urlopen(url, timeout=10)
            if f.getcode() / 100 != 2:
                print "Error delivering message to URL: %s" % url
                raise RuntimeError("Got bad response from router: %d" % f.getcode())

            # do things at a reasonable pace
            time.sleep(.2)
            return True
        except Exception, e:
            return False


    def send_message_to_kannel(self, identity, message):
	
        try:
            
            url = "%s/?id=%s&text=%s&charset=UTF-8&coding=0" % (
                        settings.POST_URL,
                        urllib2.quote(identity.strip()), 
                        urllib2.quote(message)
                )

            f = urllib2.urlopen(url, timeout=10)
            if f.getcode() / 100 != 2:
                print "Error delivering message to URL: %s" % url
                raise RuntimeError("Got bad response from router: %d" % f.getcode())

            # do things at a reasonable pace
            time.sleep(.2)
            return True
        except Exception, e:
            return False


### STOP JOKING GUYS
"""


from api.smser import *
import datetime
from api.messagelog.models import *

cmd = Smser()

msgs = Message.objects.filter(text = "Ntabwo tukuzi, banza wiyandikishe ujya ku kigo nderauzima kikwegereye!", direction = 'O', date__gte = datetime.datetime.now() - datetime.timedelta(days = 2))

for msg in msgs: cmd.send_message_via_kannel( msg.connection.identity, "This number you are sending message to, is owned by the Ministry of Health, and is only reserved for Community Health Workers. Please, if you are not a Community Health Worker do not try it again! Iyi Numero uri koherezaho ubutumwa ni iya Ministeri y'Ubuzima y'u Rwanda, igenewe abajyanama b'ubuzima gusa. Niba utariwe ntimwongere.")


"""

	

