#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from rapidsmsrw1000.apps.chws.models import Reporter, get_correct_registered_reporters
from rapidsms.models import Contact, Connection, Backend
from django.core.management.base import NoArgsCommand
from django.utils.importlib import import_module


class Command(NoArgsCommand):
    help = "Update Reporter based on a successful registration."

    def handle_noargs(self, **options):
        reporters = get_correct_registered_reporters()
        print "Update Correct CHW Registration Starts ...."
        reporters.update(correct_registration = True)
        print "Update Correct CHW Registration is Complete!!!"
        

