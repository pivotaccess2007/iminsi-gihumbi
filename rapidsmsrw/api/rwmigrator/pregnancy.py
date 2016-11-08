#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from api.rwmigrator import migsettings
from api.messaging.models import SMSReport, SMSReportField
from api.chws.models import Reporter
from api.rwmigrator.utils import *

import datetime

KEYWORD = "PRE"

FILE         = "api/rwmigrator/json/pregnancy.json"
try:    DATA = load(FILE)
except: DATA =  migsettings.DATA
ID           = DATA['last']
WRONG        = DATA['wrong']
LIMIT        = 10

TEXT = "%(keyword)s %(national_id)s %(date)s %(edd_anc2_date)s %(gravity)s %(parity)s %(prev_symptom)s %(curr_symptom)s %(location)s %(mother_weight)s %(mother_height)s %(toilet)s %(handwashing)s"


QUERY = """
            SELECT
                chws_reporter.telephone_moh,
                ubuzima_patient.national_id,
                ubuzima_report.date,
                ubuzima_report.edd_anc2_date,
                ubuzima_report.created,
                ubuzima_report.id
            FROM 
                ubuzima_report
            INNER JOIN
                chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
            INNER JOIN
                ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
            WHERE
                type_id = %s AND ubuzima_report.id < %s
            ORDER BY
                (date)
            DESC
            LIMIT
                %s
        """  

FIELDS_QUERY = """
                    SELECT
                        ubuzima_fieldtype.key,
                        ubuzima_field.value
                    FROM
                        ubuzima_field
                    INNER JOIN
                        ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id ) 
                    WHERE
                        report_id = %s 
               """

def get_records_data(CONN = CONN, QUERY = QUERY, FIELDS_QUERY = FIELDS_QUERY, KEYWORD = KEYWORD,ID =  ID, LIMIT = LIMIT,  DATA = DATA, FILE = FILE):

    TYPE         = migsettings.REPORT_TYPE[KEYWORD]
    SMS          = SMSReport.objects.get( keyword = KEYWORD)
    FIELDS       = SMSReportField.objects.filter(sms_report = SMS)
    QUERY        = QUERY %  (TYPE, ID, LIMIT)   
    ans          = get_records(CONN, QUERY)
    wrong        = []
    for r in ans:
        setattr(r, 'keyword', KEYWORD)
        fs = get_records(CONN, FIELDS_QUERY % r.id)
        for f in fs:
            if f.key in ["parity", "gravity"]: f.value = int(f.value)
            if f.key in ["mother_weight", "child_weight"]: f.value = "WT%.02f" % f.value
            if f.key in ["mother_height", "child_height"]: f.value = "HT%d" % int(f.value)
            if FIELDS.filter(key = f.key, category_en = "Previous symptoms").exists():
                setattr(r, 'prev_symptom', "%s %s" % (getattr(r, 'prev_symptom'), f.key) ) if hasattr(r, 'prev_symptom') else setattr(r, 'prev_symptom', f.key)
            if FIELDS.filter(key = f.key, category_en = "Current Symptoms").exists():
                setattr(r, 'curr_symptom', "%s %s" % (getattr(r, 'curr_symptom'), f.key) ) if hasattr(r, 'curr_symptom') else setattr(r, 'curr_symptom', f.key)
            if FIELDS.filter(key = f.key, category_en = "Location").exists():
                setattr(r, 'location', "%s %s" % (getattr(r, 'location'), f.key) ) if hasattr(r, 'location') else setattr(r, 'location', f.key )
            if FIELDS.filter(key = f.key, category_en = "Handwashing").exists():
                setattr(r, 'handwashing', "%s %s" % (getattr(r, 'handwashing'), f.key) ) if hasattr(r, 'handwashing') else setattr(r, 'handwashing', f.key )
            if FIELDS.filter(key = f.key, category_en = "Toilet").exists():
                setattr(r, 'toilet', "%s %s" % (getattr(r, 'toilet'), f.key) ) if hasattr(r, 'toilet') else setattr(r, 'toilet', f.key )

            setattr(r, f.key, f.value if f.key in ['parity', 'gravity'] or f.value else "%s" % f.key)
        try:
            for key in r.__dict__.keys():
                if type(getattr(r, key)) == datetime.date : setattr(r, key, "%d.%d.%d" % (getattr(r, key).day, getattr(r, key).month, getattr(r, key).year) ) 
            setattr(r,
                "text",
                TEXT % r.__dict__)
        except Exception, e: pass

        if not hasattr(r, "text"): wrong.append(r)
        DATA['last'] = r.id
    for rc in wrong:
        DATA['wrong'].append(rc.id)
        ans.remove(rc)

    write(DATA, FILE)

    return ans


