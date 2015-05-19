#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


##DJANGO LIBRARY
from django.utils.translation import activate, get_language
from django.utils.translation import ugettext as _
from django.conf import settings


###DEVELOPED APPS
from api.messaging.utils import *
from api.chws.models import *
from api.messaging.handlers.smsreportkeywordhandler import SMSReportKeywordHandler
from rapidsms.conf import settings as RAPIDSMS_SETTINGS

DEFAULT_LANGUAGE_ISO = settings.DEFAULT_LANGUAGE_ISO
RAPIDSMS_SETTINGS.DEFAULT_RESPONSE = "RAPIDSMS RWANDA 1000 , Ntabwo ishoboye gusobanukirwa n'ubutumwa bwawe"

class SMSReportHandler (SMSReportKeywordHandler):
    """
    RAPIDSMS RWANDA 1000 Handler
    """

    keyword = settings.DEFINED_REPORTS
    
    def filter(self):
        """ CHECK IF WE HAVE A CONNECTION FOR THE SENDER """
        if not getattr(msg, 'connection', None):
            self.respond(get_appropriate_response( DEFAULT_LANGUAGE_ISO = self.reporter.language, message_type = 'sender_not_registered', destination = None,
                                                     sms_report = None, sms_report_field = None )[1])
            return True 
    def help(self):
        try:
            sms_report = SMSReport.objects.get(keyword = self.sms_report_keyword)
            self.respond(get_appropriate_response( DEFAULT_LANGUAGE_ISO = self.reporter.language, message_type = 'help', destination = None,
                                                     sms_report = sms_report, sms_report_field = None )[1])
        except Exception, e:
            self.respond(get_appropriate_response( DEFAULT_LANGUAGE_ISO = 'rw', message_type = 'unknown_error', destination = None,
                                                     sms_report = None, sms_report_field = None )[1])

    def handle(self, text):
        try:
            self.msg.id = self.msg.logger_msg.id ## You need to add the messagelog in other to get this
            self.yemeze(self.msg)
        except Exception, e:
            #print e
            self.respond(get_appropriate_response( DEFAULT_LANGUAGE_ISO = self.reporter.language, message_type = 'unknown_error', destination = None,
                                                     sms_report = None, sms_report_field = None )[1])
        return True

    def yemeze(self, message):
        try:
            sms_report = SMSReport.objects.get(keyword = self.sms_report_keyword)
            text = message.text           
            p = get_sms_report_parts(sms_report, text, DEFAULT_LANGUAGE_ISO = self.reporter.language)
            pp = putme_in_sms_reports(sms_report, p, DEFAULT_LANGUAGE_ISO = self.reporter.language)
            cs = check_sms_report_semantics( sms_report, pp , message.date.date(), DEFAULT_LANGUAGE_ISO = self.reporter.language)

            ddobj = parseObj(self.reporter, message, errors = cs['error'])
            #print "DONE DATA OBJECT: %s" % ddobj

            if cs['error']:
                response_msg = ", ".join("%s" % c[1] for c in cs['error'])
                self.respond(response_msg)
            
            else:
                
                if ddobj:
                    response = get_appropriate_response( DEFAULT_LANGUAGE_ISO = self.reporter.language, message_type = 'success', destination = None,
                                                         sms_report = sms_report, sms_report_field = None )
                    self.respond(response[1])
                else:
                    self.respond(get_appropriate_response( DEFAULT_LANGUAGE_ISO = self.reporter.language, message_type = 'unknown_error', destination = None,
                                                     sms_report = None, sms_report_field = None )[1])
            
            #track_this_sms_report(report = cs, reporter = self.reporter)
                
        except Exception, e:
            self.respond(get_appropriate_response( DEFAULT_LANGUAGE_ISO = self.reporter.language, message_type = 'unknown_error', destination = None,
                                                     sms_report = None, sms_report_field = None )[1])    
        return True

