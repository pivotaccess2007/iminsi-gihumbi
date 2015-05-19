#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from api.messaging.handlers.smshandler import *


class Command(BaseCommand):
    help = "Test Our SMS Report. e.g : ./manage.py test_messaging -t '+250788660270' 'RED 1234567890123456 he or wt55.6' "
    option_list = BaseCommand.option_list + (
        make_option('-p', '--phone',
                    dest='telephone',
                    help='Try to test the sms, by -p and telephone number'),
        )

    option_list = option_list + (
        make_option(
            "-t", 
            "--text", 
            dest = "text",
            help = "Where is text ?", 
        ),
    )

    def handle(self, **options):
        print "\nRunning test ...\n"

        if options['telephone'] == None:
            raise CommandError("Option `--phone=...` must be specified.")
        if options['text'] == None:
            raise CommandError("Option `--text=...` must be specified.")
        else:
            identity = options['telephone']
            print "Telephone: %s" % identity

            text = options['text']
            print "TEXT MESSAGE: %s" % text
    
            sms_report = SMSReport.objects.get( keyword = text.split()[0])
            print "SMS REPORT TYPE: %s" % sms_report.description

            chw = Reporter.objects.get(telephone_moh = identity)
            print "FROM: %s" % chw

            p = get_sms_report_parts(sms_report, text, DEFAULT_LANGUAGE_ISO = chw.language)
            print "PARTS LIST: %s" % p

            pp = putme_in_sms_reports(sms_report, p, DEFAULT_LANGUAGE_ISO = chw.language)
            print "MATCH PARTS: %s" % pp

            report = check_sms_report_semantics( sms_report, pp , datetime.datetime.now().date(),DEFAULT_LANGUAGE_ISO = chw.language)
            print "REPORT: %s" % report

            x = check_bases(sms_report, report, DEFAULT_LANGUAGE_ISO)
            print "BASES: %s" % x

            s = check_stoppers(sms_report, report, DEFAULT_LANGUAGE_ISO)
            print "STOPPERS: %s" % s
 
            y = check_uniqueness(sms_report, report, DEFAULT_LANGUAGE_ISO)
            print "UNIQUES: %s" % y

            z = check_tolerances(sms_report, report, DEFAULT_LANGUAGE_ISO)
            print "TOLERANCES: %s" % z

            message, created = Message.objects.get_or_create( text  = text, direction = 'I', connection = chw.connection(),
                                                                 contact = chw.contact(), date = datetime.datetime.now() )

            ddobj = parseObj(chw, message, errors = report['error'])
            print "Object Processed: %s" % ddobj

            print "\nERRORS: %s\n" % report['error']


        print "\nTest Done...\n"


"""
from api.messaging.handlers.smshandler import *
identity = '+250788660270'
text = 'RED 1234567890123456 he or wt55.5'
sms_report = SMSReport.objects.get( keyword = text.split()[0])
chw = Reporter.objects.get(telephone_moh = identity)
p = get_sms_report_parts(sms_report, text, DEFAULT_LANGUAGE_ISO = chw.language)
pp = putme_in_sms_reports(sms_report, p, DEFAULT_LANGUAGE_ISO = chw.language)
report = check_sms_report_semantics( sms_report, pp , datetime.datetime.now().date(),DEFAULT_LANGUAGE_ISO = chw.language)

x = check_bases(sms_report, report, DEFAULT_LANGUAGE_ISO)
s = check_stoppers(sms_report, report, DEFAULT_LANGUAGE_ISO) 
y = check_uniqueness(sms_report, report, DEFAULT_LANGUAGE_ISO)
z = check_tolerances(sms_report, report, DEFAULT_LANGUAGE_ISO)
 

constraints = get_smsdbconstraints(sms_report)
const = constraints[0]
fields_keys = get_constraint_fields(const, report)
refer_sms_report = get_sms_report_by_id(sms_report.id)
start   = (datetime.datetime.now() - datetime.timedelta(days = 1)) + datetime.timedelta(days = const.minimum_period_value)
end     = datetime.datetime.now() + datetime.timedelta(days = const.maximum_period_value)
got = get_violation(  conn = conn, start = start, end = end, refer_sms_report = refer_sms_report, fields_keys = fields_keys)
start   = (datetime.datetime.now() - datetime.timedelta(days = 15)) + datetime.timedelta(days = const.minimum_period_value)
got = get_violation(  conn = conn, start = start, end = end, refer_sms_report = refer_sms_report, fields_keys = fields_keys)
"""
