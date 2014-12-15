#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from rapidsmsrw1000.apps.chws.models import Reporter
from rapidsms.models import Contact, Connection, Backend
from django.core.management.base import NoArgsCommand
from django.utils.importlib import import_module
import datetime


class Command(NoArgsCommand):
    help = "Update is_active status on Reporter based on last active date."

    def handle_noargs(self, **options):
        print "Update Active reporters ...."
        reporters = Reporter.objects.filter(last_seen__gte = datetime.date.today() - datetime.timedelta(days = 14))
        reporters.update(is_active = True)
        print "Update Inactive reporters ...."
        reporters = Reporter.objects.filter(last_seen__lt = datetime.date.today() - datetime.timedelta(days = 14))
        reporters.update(is_active = False)
        print "Active/inactive update complete ...."

"""
    def handle_noargs(self, **options):
        reporters = Reporter.objects.filter(deactivated = False, is_active = True) ###Since at every report the flag is_active is sent to True
        for reporter in reporters:
            active_status = True
            if reporter.is_expired():
                active_status = False
            reporter.is_active = active_status
            reporter.save()
"""


