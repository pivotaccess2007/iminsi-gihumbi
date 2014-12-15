#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


class TrackNotify():

    ''' 
        Class to trigger a function via PostgreSQL NOTIFY messages.

        Refer to the documentation for more information on LISTEN, NOTIFY and UNLISTEN. 
        http://www.postgresql.org/docs/8.3/static/sql-notify.html

        This obscure feature is very useful. You can create a trigger function on a
        table that executes the NOTIFY command. Then any time something is inserted,
        updated or deleted your Python function will be called using this class.

        Best and maybe unique to PostgreSQL.

    '''

    def __init__(self, dsn):

        '''
            The dsn (data source name) is passed here. 
            This class requires the psycopg2 driver.
        '''

        import psycopg2
        self.conn = psycopg2.connect(dsn)
        self.conn.set_isolation_level(0)
        self.curs = self.conn.cursor()
        self.__listening = False

    def __listen(self):
        from select import select
        if self.__listening:
            return 'already listening!'
        else:
            self.__listening= True
            while self.__listening:
                if select([self.conn],[],[], 60) == ([],[],[]):
                    print "Timeout"
                else:
                    self.conn.poll()
                    while self.conn.notifies:
                        #print self.conn.notifies
                        notify = self.conn.notifies.pop()
                        #print "Got NOTIFY:", notify.pid, notify.channel, notify.payload
                        self.gotTrackNotify(notify.pid, notify.channel, notify.payload)

    def addTrackNotify(self, notify):
        '''Subscribe to a PostgreSQL NOTIFY'''
        sql = "LISTEN %s" % notify
        self.curs.execute(sql)

    def removeTrackNotify(self, notify):
        '''Unsubscribe a PostgreSQL LISTEN'''
        sql = "UNLISTEN %s" % notify
        self.curs.execute(sql)

    def stop(self):
        '''Call to stop the listen thread'''
        self.__listening = False

    def run(self):
        '''Start listening in a thread and return that as a deferred'''
        from twisted.internet import threads
        return threads.deferToThread(self.__listen)

    def gotTrackNotify(self, pid, channel, payload):
        '''
            Called whenever a notification subscribed to by addNotify() is detected.
            Unless you override this method and do someting this whole thing is rather pointless.
        '''
        pass

    def trackThis( self, tablename, data_ref):
        """ Do you data mining here ... update other db tables ... send notifications ... """
        pass
