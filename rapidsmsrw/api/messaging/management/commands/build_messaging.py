#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from api.messaging.utils import *
from django.core.management.base import BaseCommand
from optparse import make_option


class Command(BaseCommand):
    help = "Build our Tables. Run in the cron, daily at 1 am"
    option_list = BaseCommand.option_list + (
        make_option('-d', '--dry',
                    action='store_true',
                    dest='dry',
                    default=False,
                    help='Executes a dry run, doesnt send messages or update the db.'),
        )
	
    def handle(self, **options):
        print "Running build SMS tables..."

        tab = add_four_space()
        filters = ['keyword']
        responses = [ {'name': y, 'data' : "".join("\n%s%s = models.CharField(max_length=50)" % (tab, y )) } for y in [ x[0] for x in SMSMessage.CODE_CHOICES]]
        custom = [ {'name': 'keyword', 'data' : "".join("\n%skeyword = models.CharField(max_length=30)" % (tab)) }, 
                     {'name': 'raw_sms', 'data' : "".join("\n%sraw_sms = models.TextField()" % (tab)) } ] 
        for r in responses:    custom.append(r)       
        #create_or_update_model(app_label = 'messaging', model_name = 'SMSReportTrack', model_fields = distinct_sms_report_fields(), filters = filters,
        #                                 custom = custom, links = [], locations = [
        #                                                                            #l.name for l in LocationType.objects.all() 
        #                                                                            l for l in ['Nation', 'Province', 'District', 'HealthFacility']
        #                                                                            ], default_return = 'raw_sms')
        import_sms_report()
        import_sms_report_field()
        import_sms_language()
        import_sms_message()
        import_sms_db_constraint()

        print " Building SMS tables Done"

"""
from rapidsmsrw1000.apps.api.messaging.handlers.smshandler import *
m = create_or_update_sms_report_model(app_label = 'messaging', model_name = 'SMSReportTrack', model_fields = distinct_sms_report_fields(),
                                         links = [], locations = [], default_return = 'raw_sms')


tab = add_four_space()
filters = ['keyword']
errors = [ {'name': y, 'data' : "".join("\n%s%s = models.CharField(max_length=50)" % (tab, y )) } for y in [ x[0] for x in SMSMessage.CODE_CHOICES]]
custom = [ {'name': 'keyword', 'data' : "".join("\n%skeyword = models.CharField(max_length=30)" % (tab)) },  

            {'name': 'raw_sms', 'data' : "".join("\n%sraw_sms = models.TextField()" % (tab)) } ]

"""
