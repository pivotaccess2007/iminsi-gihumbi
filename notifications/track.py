#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from tracknotify import TrackNotify
from twisted.internet import reactor
import settings
from reminders import track_reminders, track_notifications

dsn = 'dbname=%s host=%s port =%d user=%s password=%s' % (settings.DBNAME, settings.DBHOST, settings.DBPORT, settings.DBUSER, settings.DBPASSWORD)

def errorHandler(error):
    print str(error)
    notifier.stop()
    reactor.stop()

def shutdown(notifier):
    print 'Shutting down the reactor'
    reactor.stop()


def tableUpdated(pid, channel, payload):
    # This function is called by magic.
    tablename, op = channel.split('_')
    print 'ITEM %s from %s just occured on %s from process ID %s' % (payload, op, tablename, pid)

class MyTrackNotify(TrackNotify):
    # gotNotify is called with the notification and pid.
    # Override it and do something great.
    def gotTrackNotify(self, pid, channel, payload):
        if channel == 'quit':
            # The stop method will end the deferred thread
            # which is listening for notifications.
            print 'Stopping the listener thread.'
            self.stop()
        elif channel.split('_')[0]  in settings.TRIGGER_TABLES:
            tableUpdated(pid, channel, payload)
            print channel, payload
            tablename = channel.split('_')[0]
            self.trackThis(tablename, payload)
        elif channel == 'test':
            print "got asynchronous notification '%s' from process id '%s' .... Biracamo!" % (channel, pid)
        else:
            print "got asynchronous notification '%s' from process id '%s' ... Ushatse kuvuga iki??" % (channel, pid)


    #### Need to update necessary tables and send necessary notifications
    def trackThis(self, tablename, data_ref):
        ## get the record
        try:
            sql = 'SELECT indexcol, reporter_pk, reporter_phone, health_center_pk, village_pk FROM %s WHERE %s = %s' % ( tablename, 'indexcol', data_ref.strip())        
            self.curs.execute(sql)
            drecord = self.curs.fetchall()[0]
            track_reminders(tablename, drecord)
            track_notifications(tablename, drecord)  
            print "INDEXCOL: %s, " % drecord[0], "REPORTER_PK: %s, " % drecord[1], "PHONE: %s" % drecord[2], 'HC: %s' % drecord[3], 'VILLAGE: %s' % drecord[4]
            print "symptoms: %s" % get_alert( tablename , drecord)
        except Exception, e:
            print e 

notifier = MyTrackNotify(dsn)

# Start listening for subscribed notifications in a deferred thread.
listener = notifier.run()

# What to do when the TrackNotify stop method is called to
listener.addCallback(shutdown)
listener.addErrback(errorHandler)

# Call the gotNotify method when any of the following notifies are detected.
notifier.addTrackNotify('test')

### add notifies from our settings.TRIGGER_TABLES
for tbl in settings.TRIGGER_TABLES:
    #print "\\d %s;" % tbl#, settings.TRIGGER_TABLES.index(tbl)
    notifier.addTrackNotify('%s_insert' % tbl)
    #notifier.addTrackNotify('%s_update' % tbl)
    #notifier.addTrackNotify('%s_delete' % tbl) 

#### HOW DO WE STOP SAFELY THE PROCESS
notifier.addTrackNotify('quit')

# Unsubscribe from one
#reactor.callLater(15, notifier.removeTrackNotify, 'test')

reactor.run()
