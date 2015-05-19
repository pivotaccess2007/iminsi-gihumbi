#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from rapidsmsrw1000.apps.api.translate import *
from rapidsmsrw1000.apps.utils import write, load
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


class Command(BaseCommand):
    help = "Translate our Tables. e.g : ./manage.py translate -t pretable -c Pregnancy -p 17"
    option_list = BaseCommand.option_list + (
        make_option('-t', '--table',
                    dest='tablename',
                    help='Executes a translation run, by -d NAM EOF TABLE'),
        )

    option_list = option_list + (
        make_option(
            "-p", 
            "--pk", 
            dest = "pks",
            help = "All Reports ?", 
        ),
    )

    option_list = option_list + (
        make_option(
            "-c", 
            "--category", 
            dest = "category",
            help = "All Category", 
        ),
    )
	
    def handle(self, **options):
        print "Running translation ..."

        if options['tablename'] == None:
            raise CommandError("Option `--tablename=...` must be specified.")
        elif options['category'] == None:
            raise CommandError("Option `--category=...` must be specified.")
        else:
            filename = 'rapidsmsrw1000/apps/api/json/translate.json'
            data = load(filename)
            dat_last = data['last']
            dat_err =  data['error']
            if dat_last.get(options['category']) is None:
                data['last'].update({options['category']: 0})
                dat_last = data['last']
            if dat_err.get(options['category']) is None:
                data['error'].update({options['category']: [0]})
                dat_err = data['error']
            print dat_last, dat_err
            reports = Report.objects.filter(type__name = options['category'], pk__gte = dat_last.get(options['category']) )
            if options['pks']:   reports = reports.filter( pk = int(options['pks']) ) 
            #print reports.count(), options['category'], options['pks']
            count = 0  
            for report in reports:
                #print report
                try:
                    record = Translate(options['tablename'])
                    record.translate(report, uniques = {})
                    dat_last.update({options['category']: report.pk})
                except Exception, e:
                    d = set( dat_err.get(options['category']))
                    d.add(report.pk)
                    dat_err.update({options['category']: list(d)})
                    continue
                count += 1
                data['last'].update(dat_last)
                data['error'].update(dat_err)
                write(data, filename)
                print "Translate Report(%d) %d of %d %s" % (report.pk, count, reports.count(), options['category'])
        print " Translation Done"


