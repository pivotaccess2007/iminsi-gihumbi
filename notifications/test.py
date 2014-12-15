#! /usr/bin/python
# encoding: utf-8
# vim: ai ts=4 sts=4 et sw=4

from messages import rmessages
import messageassocs
import psycopg2
import datetime

conn  = psycopg2.connect(host = '127.0.0.1', port = 5432, dbname = 'thousanddays', user = 'thousanddays', password = 'thousanddays')

def parse(conn = conn, text = '', date = datetime.datetime.now() ):
    try:
        ans, ents = rmessages.ThouMessage.parse(text, messageassocs.ASSOCIATIONS, date)
        print ('Success with %s:\n%s' % (text, str(ans.entries))),
        return (ans, ents)
    except rmessages.ThouMsgError, e:
        print ('Errors with %s:\n%s' % (text, str(e.errors), )),
        return e.errors
        
    return 0



##SELECT failcode, COUNT(*) FROM failed_transfers WHERE failcode NOT LIKE '% %' GROUP BY failcode ORDER BY failcode; ### exclude failcode with escape
## I Think the response object has to combine both failcode and Field ??? Like nbc_code failcode, but because of BreastFeedingField Not equal NBCFieldCode
