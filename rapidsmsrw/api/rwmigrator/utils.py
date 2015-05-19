#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from api.rwmigrator import migsettings

import MySQLdb
import MySQLdb.cursors
import warnings
import json
from api.smser import Smser
from api.messaging.models import SMSReport
from api.messaging.utils import parseObj, get_sms_report_parts, putme_in_sms_reports, check_sms_report_semantics
from api.messagelog.models import Message
from api.chws.models import Reporter, Hospital, HealthCentre
import datetime

CONN = MySQLdb.connect(
                        host = migsettings.MySQL_HOST,
                        port = migsettings.MySQL_PORT,
                        user = migsettings.MySQL_USER, 
                        passwd = migsettings.MySQL_PASSWORD, 
                        db = migsettings.MySQL_DATABASE
                       )

class Record(object):
    def __init__(self, cursor, registro):
        for (attr, val) in zip((d[0] for d in cursor.description), registro) :
            setattr(self, attr, val)

def fetch_data(cursor):
    ans = []
    try:
        for row in cursor.fetchall() :
            r = Record(cursor, row)
            #print row, r.__dict__
            ans.append(r)
            cursor.close()
    except MySQLdb.ProgrammingError, e:
        return None
    return ans

def fetch_data_cursor(CONN, query_string):
    curseur = CONN.cursor()
    try:   curseur.execute(query_string)
    except MySQLdb.ProgrammingError, e: return None
    return curseur


def get_records(CONN, query_string):
    cursor = fetch_data_cursor(CONN, query_string)        
    return fetch_data(cursor) if cursor else None


def write(data, filename):
    with open(filename, 'w') as output:
        json.dump(data, output)
        return True

def load(filename):
    with open(filename, 'r') as input:
        data = json.load(input)
        return data

def parse_date(value):
    try:
        m3 = re.search("^(\d+)\.(\d+)\.(\d+)$", value) 
        if m3:
            dd = int(m3.group(1))
            mm = int(m3.group(2))
            yyyy = int(m3.group(3))

            d = datetime.date( yyyy, mm, dd )
            return d
    except Exception, e: pass
    return None

def send_record_to_smpp(record):
    return Smser().send_message_to_kannel(record.telephone_moh, record.text)

def send_record_to_smshandler(record):

    sms_report = SMSReport.objects.filter(keyword = record.keyword)[0]
    chw = Reporter.objects.get(telephone_moh = record.telephone_moh)
    date = record.created
    p = get_sms_report_parts(sms_report, record.text, DEFAULT_LANGUAGE_ISO = chw.language)
    pp = putme_in_sms_reports(sms_report, p, DEFAULT_LANGUAGE_ISO = chw.language)
    report = check_sms_report_semantics( sms_report, pp , date.date() or datetime.datetime.now().date(), DEFAULT_LANGUAGE_ISO = chw.language)
    message, created = Message.objects.get_or_create( text  = record.text, direction = 'I', connection = chw.connection(),
                                                         contact = chw.contact(), date = date or datetime.datetime.now() )

    ddobj = parseObj(chw, message, errors = report['error'])

    return True

def migrate_hospitals():
    hospitals = Hospital.objects.all().exclude(name = "TEST")
    FILE         = "api/rwmigrator/json/hospital.json"
    try:    DATA = load(FILE)
    except: DATA =  []
    if DATA == []:
        for h in hospitals:
            try:   DATA.append({"name": h.name, "code": h.code, "sector": h.sector.code if h.sector else "", "district" :h.district.code})
            except: print h
        write(DATA, FILE)
        return DATA
    else:
        return DATA
    return True

def migrate_healthcenters():
    hcs = HealthCentre.objects.all().exclude(name = "TEST")
    FILE         = "api/rwmigrator/json/healthcenter.json"
    try:    DATA = load(FILE)
    except: DATA =  []
    if DATA == []:
        for h in hcs:
            try:    DATA.append({"name": h.name, "code": h.code, "sector": h.sector.code if h.sector else "", "district" :h.district.code})
            except: print h
        write(DATA, FILE)
        return DATA
    else:
        return DATA
    return True


def migrate_facilities():
    hps = Hospital.objects.all().exclude(name = "TEST")
    hcs = HealthCentre.objects.all().exclude(name = "TEST")
    FILE         = "api/rwmigrator/json/facilities.json"
    try:    DATA = load(FILE)
    except: DATA =  []
    if DATA == []:

        for hp in hps:
            try:

                DATA.append({"name": hp.name, "code": hp.code, "sector": hp.sector.code if hp.sector else "", "type": "HD", 
                            "district" :hp.district.code, "referral": "" })
            except: print hp

        for hc in hcs:
            try:
                rep = Reporter.objects.filter(health_centre = hc)
                DATA.append({"name": hc.name, "code": hc.code, "sector": hc.sector.code if hc.sector else "", "type": "HC", 
                            "district" :hc.district.code, "referral": rep[0].referral_hospital.code if rep.exists() and rep[0].referral_hospital else "" })
            except: print hc

        write(DATA, FILE)
        return DATA
    else:
        return DATA
    return True
