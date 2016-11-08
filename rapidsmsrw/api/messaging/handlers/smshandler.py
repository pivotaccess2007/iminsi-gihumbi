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
import sys, traceback

###DEVELOPED APPS
from api.messaging.utils import *
from api.chws.models import *
from api.messaging.handlers.smsreportkeywordhandler import SMSReportKeywordHandler
from rapidsms.conf import settings as RAPIDSMS_SETTINGS
from api.messaging.zdmapper import smsmapper
from api.messaging.zdmapper.messages.utils import *

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

            rectifier = Rectifier(sms_report, self.reporter, p,  pp, message, orm, GESTATION = settings.GESTATION)
            checkers = checker.RECTIFIER_MAPPER.get(sms_report.keyword)(rectifier)
            try:    cs['error'] = checkers.errors
            except Exception, e: pass

            #ddobj = parseObj(self.reporter, message, errors = cs['error'])
            #print "DONE DATA OBJECT: %s" % ddobj
            #print cs
            if cs['error']:
                ans = [ c[1]  for c in cs['error'] if c[1] ]
                response_msg = ", ".join("%s" % msg  for msg in set(ans) )
                failed = smsmapper.process_failed_sms(self.reporter, message, cs) 
                self.respond(response_msg)
            
            else:
                ddobj = smsmapper.set_record_attrs(self.reporter, message, cs)
                if ddobj:
                    response = get_appropriate_response( DEFAULT_LANGUAGE_ISO = self.reporter.language, message_type = 'success', destination = None,
                                                         sms_report = sms_report, sms_report_field = None )
                    treated = smsmapper.process_treated_sms(self.reporter, message, cs)
                    self.respond(response[1])
                else:
                    failed = smsmapper.process_failed_sms(self.reporter, message, cs)
                    self.respond(get_appropriate_response( DEFAULT_LANGUAGE_ISO = self.reporter.language, message_type = 'unknown_error', destination = None,
                                                     sms_report = None, sms_report_field = None )[1])
            
            #track_this_sms_report(report = cs, reporter = self.reporter)
                
        except Exception, e:
            try:    self.respond( traceback.print_exc(file=sys.stdout) )
            except: self.respond("Ikosa, kosora ubutumwa bwawe wongere ugerageze")     
        return True

