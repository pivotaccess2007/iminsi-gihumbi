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


from notifications.reminders import *
#query = "SELECT * FROM birmessage WHERE indexcol = 1"
#an = get_record_by_query(conn, query)
#anm = Map('birmessage', an)
#anm.pack()

query = "SELECT * FROM pregmessage WHERE indexcol = 1"
an = get_record_by_query(conn, query)
data = Track.process('pregmessage', an)
print data
send_nutrition_notifications(data.table, data)


query = "SELECT * FROM birmessage WHERE indexcol = 1"
an = get_record_by_query(conn, query)
data = Track.process('birmessage', an)
print data

query = "SELECT * FROM nbcmessage WHERE indexcol = 3"
an = get_record_by_query(conn, query)
data = Track.process('nbcmessage', an)
print data


query = "SELECT * FROM ancmessage WHERE indexcol = 3"
an = get_record_by_query(conn, query)
data = Track.process('ancmessage', an)
print data

query = "SELECT * FROM riskmessage WHERE indexcol = 1"
an = get_record_by_query(conn, query)
data = Track.process('riskmessage', an)
print data

query = "SELECT * FROM resultmessage WHERE indexcol = 1"
an = get_record_by_query(conn, query)
data = Track.process('resultmessage', an)
print data

query = "SELECT * FROM ccmmessage WHERE indexcol = 1"
an = get_record_by_query(conn, query)
data = Track.process('ccmmessage', an)
print data

query = "SELECT * FROM cmrmessage WHERE indexcol = 1"
an = get_record_by_query(conn, query)
data = Track.process('cmrmessage', an)
print data

query = "SELECT * FROM cbnmessage WHERE indexcol = 1"
an = get_record_by_query(conn, query)
data = Track.process('cbnmessage', an)
print data


query = "SELECT * FROM childmessage WHERE indexcol = 1"
an = get_record_by_query(conn, query)
data = Track.process('childmessage', an)
print data






