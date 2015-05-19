#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from api.rwmigrator.pregnancy import *

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    help = "Translate our Tables. e.g : ./manage.py translate -k PRE -l 10"
    option_list = BaseCommand.option_list + (
        make_option('-k', '--keyword',
                    dest='keywords',
                    help='Executes a migration run, by -k Keyword of the SMS Report'),
        )

    option_list = option_list + (
        make_option(
            "-l", 
            "--limit", 
            dest = "limits",
            help = "Limit of Reports or by default only 10?", 
        ),
    )

    def handle(self, **options):
        print "Running Migration ..."

        if options['keywords'] == None:
            raise CommandError("Option `--keyword=...` must be specified.")
        elif options['limits'] == None:
            raise CommandError("Option `--limit=...` must be specified.")
        else:
            #Override KEYWORD FROM pregnancy.py
            KEYWORD = options['keywords'].upper()
            LIMIT = options['limits']
            try:
                ans = get_records_data( KEYWORD = KEYWORD, LIMIT = LIMIT)
                print " Migration Start"
                count = 1
                total = len(ans)
                for record in ans:
                    print "%d of %d:\t%s" % (count, total, record.text)
                    #send_record_to_smpp(record)
                    send_record_to_smshandler(record)
                    count += 1
                    
            except Exception, e: print e

        print " Migration Done"
