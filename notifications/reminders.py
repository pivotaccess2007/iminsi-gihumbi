#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import settings
import psycopg2
from smser import Smser

conn = psycopg2.connect(host = settings.DBHOST, port = settings.DBPORT, dbname = settings.DBNAME, user = settings.DBUSER, password = settings.DBPASSWORD)

class Record(object):
 def __init__(self, cursor, registro):
  for (attr, val) in zip((d[0] for d in cursor.description), registro) :
   setattr(self, attr, val)


def fetch_data(cursor):
 ans = []
 for row in cursor.fetchall() :
  r = Record(cursor, row)
  ans.append(r)
  cursor.close()
 return ans

def fetch_data_cursor(conn, query_string):
 curseur = conn.cursor()
 curseur.execute(query_string)
 return curseur


class MotherTrack:
    ''' Don't miss any pregnancy on our track so that  we are sure the mother is followed until the sixth week after delivery '''    
    
    table_name = 'pregnancytrack'

    def __init__(self, pre):
        self.pre = pre
        
class ChildTrack:
    ''' Don't miss any delivery on our track so that  we are sure the child is followed until 3 years old '''
    
    table_name = 'childtrack'

    def __init__(self, delivery):
        self.delivery = delivery

class ResponseTrack:
    ''' Don't miss any delivery on our track so that  we are sure the child is followed until 3 years old '''
    
    table_name = 'childtrack'

    def __init__(self, delivery):
        self.delivery = delivery

class ReminderTrack:
    ''' Everyone is set by defaul receive all reminders, but this reminder will only be sent if sent status is False and required data is not there '''

    table_name = 'remindertrack'

    def __init__( self):
        self.mothertrack     = None
        self.childtrack      = None
        self.responsetrack   = None
        self.date            = None
        ##rem_type_true_or_false_as sent [anc2, anc3, anc4, deliv7, deliv8, pnc1, pnc2, pnc3, nbc1, nbc2, nbc3, nbc4, nbc5, v1, v2, v3, v4, v5, v6, ]
        ##locs [province, district, ..., village]
    
class Notification:

    def __init__(self, text, category, destination):
        ''' Text for anc4 reminder you will send to the Supervisor is not the same you will send to the CHW '''

        self.category       = category
        self.destination    =   destination
        self.text           = text

def match_notifications(track, base , NOTIFS = [] ):
    ''' A track is normally a list of mothers, children, or waiting responses on track list 
        base is the field we check to find out and match a notification be sent out based on timelines in NOTIFS
    '''

    ans  = []

    ### Check required info by getting from track if nottif[0] is NULL
    ### Check if reminder type was sent 

    for notif in NOTIFS:
        curz  = conn.cursor()
        curz.execute('''SELECT indexcol, patient_id, telephone, text FROM %s WHERE %s IS NULL AND %s IS NULL ''' % ( base1, base2, compare, notif[0], notif[0]) )
        got = curz.fetchone()            
    
    return ans


def get_possible_destination():
    qry = " SELECT id, name FROM auth_group;"
    curz = fetch_data_cursor(conn, qry)
    return fetch_data(curz)

def get_sms_report(keyword):
    qry = " SELECT * FROM messaging_smsreport WHERE lower(keyword) = '%s' ;" % keyword
    curz = fetch_data_cursor(conn, qry)
    return fetch_data(curz)

def get_alert(table, language, smsreport, msgtype):
    ''' Figure out reds symptom and their title in the # languages '''

    ## Get all possible destinations from messaging_smsmessage
    dests = get_possible_destination()
    notifs = {}
    for dst in dests:
        notif = get_appropriate_response(DEFAULT_LANGUAGE_ISO = language, message_type = msgtype, sms_report = smsreport, sms_report_field = None, destination = dst.id)
        notifs.update({ dst.name.lower(): notif})        
    return notifs

def get_appropriate_response( DEFAULT_LANGUAGE_ISO = 'rw', message_type = 'unknown_error', sms_report = None, sms_report_field = None, destination = None ):
    ''' messaging notifications appropriate response '''
    try:
        colm = 'message_%s' % DEFAULT_LANGUAGE_ISO
        qry = "SELECT %s FROM messaging_smsmessage WHERE message_type = '%s' AND destination_id = %s AND sms_report_id = %s" % (colm, message_type, destination, sms_report)
        curz = conn.cursor()
        curz.execute(qry)
        msg = curz.fetchone()
        curz.close()
        return [message_type, msg[0]]
    except Exception, e:
        try:
            return [message_type, "%s" % e]
        except Exception, e:
            return [get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO )[0], get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO )[1]]
    

def fetch_notification( NOTIFS = [] , DESTINATION = [], BASE = []):
    ''' NOTIFS = settings.ANC_REMINDER ... DESTINATION = [('chws__reporter', 'telephone_moh', 'language')] ... BASE  = [('pregnancy' , 'edd' )] '''

    pass#for notif in NOTIFS:

def send_notification( telephone , text ):
    '''  telephone = '+250789634210', text = 'ibusta umubyeyi 1234567890123456 ko igihe cyo kubonana na muganga bwa kabiri cyageze, navayo uduhe raporo.'  '''
    return Smser().send_message_via_kannel(telephone, text)


def track_notifications(tablename, drecord):
    if tablename == 'redmessage':
        sms_report = get_sms_report('red')#;print sms_report[0].id
        notifs = get_alert(table = tablename, language = 'rw', smsreport = sms_report[0].id, msgtype = 'notification')
        if notifs.get('chw'):    send_notification( drecord[2] , notifs.get('chw')[1])        
    else:
        pass
    return True
def track_reminders(tablename, drecord):
    return True    
        




