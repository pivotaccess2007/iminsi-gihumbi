#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import settings
import psycopg2
from smser import Smser
from translate import *
from abc import abstractmethod

conn = psycopg2.connect(host = settings.DBHOST, port = settings.DBPORT, dbname = settings.DBNAME, user = settings.DBUSER, password = settings.DBPASSWORD)


class Record(object):
 def __init__(self, cursor, registro):
  for (attr, val) in zip((d[0] for d in cursor.description), registro) :
   setattr(self, attr, val)


def fetch_data(cursor):
 ans = []
 try:
  for row in cursor.fetchall() :
   r = Record(cursor, row)
   ans.append(r)
   cursor.close()
 except psycopg2.ProgrammingError, e:
    conn.reset()
 return ans

def fetch_data_cursor(conn, query_string):
 curseur = conn.cursor()
 try:   curseur.execute(query_string)
 except psycopg2.ProgrammingError, e: conn.reset()
 return curseur

def get_record_by_query(conn, query_string):
    cursor = fetch_data_cursor(conn, query_string)
    data = fetch_data(cursor)
    if data: return data[0]    
    return None

def get_records_by_query(conn, query_string):
    cursor = fetch_data_cursor(conn, query_string)
    data = fetch_data(cursor)
    if data: return data    
    return None

def get_record_by_cursor(cursor):
    data = fetch_data(cursor)
    if data: return data[0]    
    return None

def get_record_by_sql(query_string, conn = conn):
    cursor = fetch_data_cursor(conn, query_string)
    data = fetch_data(cursor)
    if data: return data[0]    
    return None

def get_records_by_cursor(cursor):
    data = fetch_data(cursor)
    if data: return data    
    return None

class Track:
    ''' Base defining a track in RapidSMS RWanda 1000 Days'''

    table       = ''
    uniques     = []
    fields      = []
    mother      = None
    pregnancy   = None
    child       = None

    @staticmethod
    def initialize_track(mother_query, pregnancy_query, child_query):
        """ Initialize if the track was already there in db but missing some staff ."""

        print mother_query, pregnancy_query, child_query
        mother      = get_record_by_query(conn, mother_query)  
        pregnancy   = get_record_by_query(conn, pregnancy_query)
        child       = get_record_by_query(conn, child_query)

        return [mother, pregnancy, child]

    @staticmethod
    def pull_from_init(obj, data, fields):
        values = {}
        ans = obj.initialize_track(data.get('mother_query'), data.get('pregnancy_query'), data.get('child_query') )
        print ans
        for f in fields:
            try:
                for x in ans:
                    #print { f[0]: getattr(x, f[0]) }
                    values.update( {f[0] : getattr(x, f[0])} )
            except: continue
        #print values
        return values

    @staticmethod
    def maptrack(sourcetable, drecord):
        """ Need to listen any incoming record up there and map it o this the appropriate tarck"""

        anm = Map(sourcetable, drecord)
        anm.pack()
        #print anm
        return anm

    @staticmethod
    def pull_track_data(keyobj, sourcetable, drecord):
        ''' Pull data '''
        pulldata = keyobj.maptrack(sourcetable, drecord).DATA
        castdata = dict(pulldata)#;print castdata
        init_data = keyobj.pull_from_init(keyobj, castdata, keyobj.fields)
        #print init_data
        pulled = [ (f[0], castdata.get(f[0]) or init_data.get(f[0]) or f[1] ) for f in keyobj.fields ]
        return pulled

    @staticmethod
    def process(sourcetable, drecord):
        objs = TABLEMAP.get(sourcetable)
        data = []
        for obj in objs:
            data = obj.pull_track_data(obj, sourcetable, drecord)
            print obj.table, obj.uniques, data
            data = obj.save_track(obj.table, obj.uniques, data)
        return data

    @staticmethod
    def save_track(table, uniques, data):
        """ save the track """
        #print table, uniques, data
        track = Translate(table)
        track_record = track.translate(uniques, data)
        return track_record
    


class MotherTrack(Track):
    ''' Don't miss any pregnancy on our track so that  we are sure the mother is followed until the sixth week after delivery '''    
    
    table   = 'mother_track'
    uniques = ['pregnancy']

    fields  = [ ('indangamuntu', '1234567890123456'),
                ('reporter_pk', 0), 
			    ('reporter_phone', '+250788660270'),
                ('nation_pk', 0),
                ('province_pk', 0),
                ('district_pk', 0),
                ('health_center_pk', 0),
                ('referral_hospital_pk', 0),
                ('sector_pk', 0),
                ('cell_pk', 0),
                ('village_pk', 0),				
			    ('report_date', 0),
                ('pregnancy', 0 ),
                ('lmp', datetime.today().date() ),
                ('anc2_date', datetime.today().date()),
                ('anc2', 0),
                ('anc3', 0),
                ('anc4', 0),
                ('delivery', 0),
                ('delivery_date', datetime.today().date()),
                ('pnc1', 0),
                ('pnc2', 0),
                ('pnc3', 0),
                ('mother_weight', 0),
                ('mother_height', 0),
                ('bmi', 0.0),  
                ('lostweight', False),
                ('falteringweight', False),
                ('gainedweight', False),
                ('miscarriage', 0),
                ('mdeath', 0)
            ]        
        
class ChildTrack(Track):
    ''' Don't miss any delivery on our track so that  we are sure the child is followed until 3 years old '''
    
    table       = 'child_track'
    uniques     =  ['child']

    fields      = [ ('indangamuntu', '1234567890123456'),
                    ('reporter_pk', 0), 
				    ('reporter_phone', '+250788660270'),
                    ('nation_pk', 0),
                    ('province_pk', 0),
                    ('district_pk', 0),
                    ('health_center_pk', 0),
                    ('referral_hospital_pk', 0),
                    ('sector_pk', 0),
                    ('cell_pk', 0),
                    ('village_pk', 0),				
				    ('report_date', 0),
                    ('mother', 0),
                    ('child', 0),
                    ('gender', ''),
                    ('birth', 0),
                    ('birth_date', datetime.today().date()),
                    ('age_in_months', 0),
                    ('child_number', 0),
                    ('pregnancy', 0),
                    ('premature', ''),
                    ('nbc1', 0),
                    ('nbc2', 0),
                    ('nbc3', 0),
                    ('nbc4', 0),
                    ('nbc5', 0),
                    ('v1', 0),
                    ('v2', 0),
                    ('v3', 0),
                    ('v4', 0),
                    ('v5', 0),
                    ('v6', 0),
                    ('bf1', ''),
                    ('breastfeeding', ''),
                    ('ndeath', 0),
                    ('child_weight', 0),
                    ('child_height', 0),
                    ('weight_for_age', 0.0),  ###underweight when less than < -2 or value to be less than two standard deviations of the WHO Child Growth Standards median
                    ('height_for_age', 0.0),  ###stunted when less than < -2 or value to be less than two standard deviations of the WHO Child Growth Standards median
                    ('weight_for_height', 0.0),   ###wasted when less than < -2 or value to be less than two standard deviations of the WHO Child Growth Standards median
                    ('lostweight', False),
                    ('falteringweight', False),
                    ('gainedweight', False),
                    ('muac', 0),
                    ('cdeath', 0) 
                ] 


class CCMTrack(Track):

    ''' Don't miss any response on our track '''
    
    table = 'ccm_track'
    uniques = ['child', 'ccm']

    fields      = [ ('indangamuntu', '1234567890123456'),
                    ('reporter_pk', 0), 
			        ('reporter_phone', '+250788660270'),
                    ('nation_pk', 0),
                    ('province_pk', 0),
                    ('district_pk', 0),
                    ('health_center_pk', 0),
                    ('referral_hospital_pk', 0),
                    ('sector_pk', 0),
                    ('cell_pk', 0),
                    ('village_pk', 0),	
                    ('mother', 0),
                    ('pregnancy', 0),
                    ('child', 0),
                    ('ccm', 0),
                    ('cmr', 0),
                    ('status', ''),
                    ('intervention', ''),
                    ('issue_date', datetime.today()),
                    ('response_date', datetime.today()),
                ] 

class RiskTrack(Track):

    ''' Don't miss any delivery on our track so that  we are sure the child is followed until 3 years old '''
    
    table = 'risk_track'
    uniques = ['mother', 'risk']

    fields      = [ 
                    ('indangamuntu', '1234567890123456'),
                    ('reporter_pk', 0), 
			        ('reporter_phone', '+250788660270'),
                    ('nation_pk', 0),
                    ('province_pk', 0),
                    ('district_pk', 0),
                    ('health_center_pk', 0),
                    ('referral_hospital_pk', 0),
                    ('sector_pk', 0),
                    ('cell_pk', 0),
                    ('village_pk', 0),	
                    ('mother', 0),
                    ('pregnancy', 0),
                    ('risk', 0),
                    ('res', 0),
                    ('status', ''),
                    ('intervention', ''),
                    ('issue_date', datetime.today()),
                    ('response_date', datetime.today()),
                ] 

class RedTrack(Track):
    ''' Don't miss any delivery on our track so that  we are sure the child is followed until 3 years old '''
    
    table = 'red_track'
    uniques = ['mother', 'red']

    fields      = [ ('indangamuntu', '1234567890123456'),
                    ('reporter_pk', 0), 
			        ('reporter_phone', '+250788660270'),
                    ('nation_pk', 0),
                    ('province_pk', 0),
                    ('district_pk', 0),
                    ('health_center_pk', 0),
                    ('referral_hospital_pk', 0),
                    ('sector_pk', 0),
                    ('cell_pk', 0),
                    ('village_pk', 0),	
                    ('mother', 0),
                    ('pregnancy', 0),
                    ('red', 0),
                    ('rar', 0),
                    ('status', ''),
                    ('intervention', ''),
                    ('issue_date', datetime.today()),
                    ('response_date', datetime.today()),
                ] 


class ReminderTrack:
    ''' Everyone is set by defaul receive all reminders, but this reminder will only be sent if sent status is False and required data is not there '''

    table_name = 'reminder_track'

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


def get_possible_destination(title = None):
    qry = " SELECT id, name FROM auth_group;"
    if title:   qry = " SELECT id, name FROM auth_group WHERE lower(name) = '%s' ;" % title
    #print qry
    curz = fetch_data_cursor(conn, qry)
    return fetch_data(curz)

def get_sms_report(keyword):
    qry = " SELECT * FROM messaging_smsreport WHERE lower(keyword) = '%s' ;" % keyword
    curz = fetch_data_cursor(conn, qry)
    return fetch_data(curz)

def get_alert( language, smsreport, smsreportfield, msgtype, destination):
    ''' Figure out reds symptom and their title in the # languages '''

    try:
        notif = get_appropriate_response(DEFAULT_LANGUAGE_ISO = language, message_type = msgtype, 
                                            sms_report = smsreport, sms_report_field = smsreportfield, destination = destination.id)
        return notif
    except: pass
             
    return [msgtype, '']

def get_appropriate_response( DEFAULT_LANGUAGE_ISO = 'rw', message_type = 'unknown_error', sms_report = None, sms_report_field = None, destination = None ):
    ''' messaging notifications appropriate response '''
    
    colm = 'message_%s' % DEFAULT_LANGUAGE_ISO
    qry = "SELECT %s FROM messaging_smsmessage WHERE message_type = '%s' AND destination_id = %s AND sms_report_id = %s" % (
                                                                                                    colm, message_type, destination, sms_report)
    curz    = fetch_data_cursor(conn, qry)
    msg     = fetch_data(curz)
    try:    return [message_type, getattr(msg[0], colm)]
    except: return [message_type, '']

def fetch_notification( NOTIFS = [] , DESTINATION = [], BASE = []):
    ''' NOTIFS = settings.ANC_REMINDER ... DESTINATION = [('chws__reporter', 'telephone_moh', 'language')] ... BASE  = [('pregnancy' , 'edd' )] '''

    pass#for notif in NOTIFS:

def send_notification( telephone , text ):
    '''  telephone = '+250789634210', text = 'ibusta umubyeyi 1234567890123456 ko igihe cyo kubonana na muganga bwa kabiri cyageze, navayo uduhe raporo.'  '''
    return Smser().send_message_via_kannel(telephone, text)


def send_redalerts_notification(drecord):
    sms_report = get_sms_report('red')#;print sms_report[0].id
    ## Get all possible destinations from messaging_smsmessage
    dests = get_possible_destination()
    for dest in dests:
        ## message to CHW
        if dest.name.lower().strip() == 'chw':
            msg = get_alert(language = 'rw', smsreport = sms_report[0].id, smsreportfield = None, msgtype = 'red_notification', destination = dest)
            send_notification( drecord.reporter_phone ,
                               msg[1] or "Ubutumwa bwanyu turabubonye, gerageza urebeko wafasha uwo mubyeyi, tubimenyesheje inzego zitanga ubufasha baragutabara.")
        ## message to Ambulance
        elif dest.name.lower().strip() == 'amb':
            msg = ''
        ## message to Supervisor
        elif dest.name.lower().strip() == 'sup':
            msg = ''
        ## message to someone at facility
        else:
            msg = ''

    return True

def get_nutrition_notification(language, message_type, destination, reports):
    ''' get matching notifications for matching sms_repots '''

    notifs = []
    for rpt in reports:
        try:
            indexcol = rpt[0].id
            if indexcol:
                notifs.append( 
                                get_alert(language = language, smsreport = indexcol, smsreportfield = None, msgtype = message_type, destination = destination)
                                )
                break   
        except: continue

    return notifs

def mother_nutrition_notifications(track_record):
    ''' get mother nutrition status '''
    nots = []
    reports = [get_sms_report('pre'), get_sms_report('anc'), get_sms_report('risk'), get_sms_report('red')]
    destination = get_possible_destination('chw')[0]
    language = 'rw'
    try:        
        weight = track_record['mother_weight']        
        if weight < 50:
            for notif in get_nutrition_notification(language, 'poor_weight', destination, reports = reports): nots.append(notif)
    except: pass

    try:        
        height = track_record['mother_height']        
        if height < 150:
            for notif in get_nutrition_notification(language, 'poor_height', destination, reports = reports): nots.append(notif)
    except: pass

    try:        
        if track_record['lostweight'] :
            for notif in get_nutrition_notification(language, 'lost_weight', destination, reports = reports): nots.append(notif)
    except: pass


    try:        
        if track_record['falteringweight'] :
            for notif in get_nutrition_notification(language, 'faltering_weight', destination, reports = reports): nots.append(notif)
    except: pass

    return nots

def child_nutrition_notifications(track_record):
    ''' get child nutrition status '''
    nots = []
    reports = [get_sms_report('cbn'), get_sms_report('chi'), get_sms_report('bir')]
    destination = get_possible_destination('chw')[0]
    language = 'rw'
    try:        
        weight = track_record['weight_for_age']        
        if weight < -2 :
            for notif in get_nutrition_notification(language, 'underweight', destination, reports = reports): nots.append(notif)
    except: pass

    try:        
        height = track_record['height_for_age']        
        if height < -2 :
            for notif in get_nutrition_notification(language, 'stunted', destination, reports = reports): nots.append(notif)
    except: pass

    try:        
        weight_height = track_record['weight_for_height']        
        if weight_height < -2 :
            for notif in get_nutrition_notification(language, 'wasted', destination, reports = reports): nots.append(notif)
    except: pass

    try:        
        if track_record['lostweight'] :
            for notif in get_nutrition_notification(language, 'lost_weight', destination, reports = reports): nots.append(notif)
    except: pass


    try:        
        if track_record['falteringweight'] :
            for notif in get_nutrition_notification(language, 'faltering_weight', destination, reports = reports): nots.append(notif)
    except: pass

    return nots

def send_nutrition_notifications(tablename, track_record):
    ''' you need to notify for lost weight, poor weight, poor height or poor bmi '''

    notifs = []

    if tablename == 'mother_track': notifs = mother_nutrition_notifications( track_record )        
    if tablename == 'child_track':  notifs = child_nutrition_notifications( track_record )

    for notif in notifs:
        try:    msg = notif[1] % (track_record['indangamuntu'], track_record['child_number'])
        except: 
            try:    msg = notif[1] % track_record['indangamuntu']
            except: msg = notif[1]
        #print track_record['reporter_phone'] , msg
        send_notification( track_record['reporter_phone'] , msg )       
    
    return True
    

def track_notifications(tablename, drecord):

    ### Send red alert notifications
    track = None
    try: track = Track.process(tablename, drecord)
    except Exception, e: print e;pass

    if tablename == 'redmessage':
       send_redalerts_notification(drecord)
    
    if track:   send_nutrition_notifications(track.table, track)
    
    return True

def track_reminders(tablename, drecord):
    #print  drecord, drecord.indangamuntu , track.reporter_phone
    return True    
        

"""

from notifications.reminders import *
language = "rw"
message_type = 'notification'
sms_report = get_sms_report('red')
dests = get_possible_destination()
ds = None
for dest in dests:
 if dest.name.lower().strip() == 'chw': ds = dest

smsreportfield = None
smsreport = get_sms_report('red')
notif = get_appropriate_response(DEFAULT_LANGUAGE_ISO = language, message_type = message_type, 
                                             sms_report = smsreport, sms_report_field = smsreportfield, destination = ds)


"""

TABLEMAP = {
                'pregmessage'       : [MotherTrack],
                'ancmessage'        : [MotherTrack],
                'redmessage'        : [MotherTrack, RedTrack],
                'redresultmessage'  : [MotherTrack, RedTrack],
                'riskmessage'       : [MotherTrack, RiskTrack],
                'resultmessage'     : [MotherTrack, RiskTrack],
                'birmessage'        : [MotherTrack, ChildTrack],
                'deathmessage'      : [MotherTrack, ChildTrack],
                'pncmessage'        : [MotherTrack],
                'childmessage'      : [ChildTrack],
                'nbcmessage'        : [ChildTrack],
                'ccmmessage'        : [ChildTrack, CCMTrack],
                'cmrmessage'        : [ChildTrack, CCMTrack],
                'cbnmessage'        : [ChildTrack],
                
                }





