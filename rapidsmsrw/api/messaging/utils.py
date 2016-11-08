#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from .models import *
from xlrd import open_workbook ,cellname,XL_CELL_NUMBER,XLRDError
from api.utils import get_block_of_text_link, replace_block_of_text_link


from ectomorph import orm
from entities import processor
from messages import rmessages
import messageassocs
import migrations
import psycopg2
from notifications.reminders import get_record_by_cursor, get_record_by_sql, track_reminders, track_notifications
from api.smser import *
import random
import sha

TREATED = ('treated_messages', migrations.TREATED)
FAILED  = 'failed_transfers'
orm.ORM.connect(    host    =   settings.DATABASES['default']['HOST'],
                    port    =   settings.DATABASES['default']['PORT'],
                    dbname  =   settings.DATABASES['default']['NAME'],
                    user    =   settings.DATABASES['default']['USER'],
                    password  =   settings.DATABASES['default']['PASSWORD']
                )

conn = psycopg2.connect(            host    =   settings.DATABASES['default']['HOST'],
                                    port    =   settings.DATABASES['default']['PORT'],
                                    dbname  =   settings.DATABASES['default']['NAME'],
                                    user    =   settings.DATABASES['default']['USER'],
                                    password  =   settings.DATABASES['default']['PASSWORD']
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


def get_sms_report(keyword, conn = conn):
    qry = " SELECT * FROM messaging_smsreport WHERE lower(keyword) = '%s' ;" % keyword.lower()
    curz = fetch_data_cursor(conn, qry)
    d = fetch_data(curz)
    return d[0] if len(d) > 0 else None

def get_sms_report_by_id(sid, conn = conn):
    qry = " SELECT * FROM messaging_smsreport WHERE id = %d ;" % sid
    curz = fetch_data_cursor(conn, qry)
    d = fetch_data(curz)
    return d[0] if len(d) > 0 else None

def get_sms_reportfield(smsreport, key, conn = conn):
    qry = " SELECT * FROM messaging_smsreportfield WHERE lower(key) = '%s' AND sms_report_id = %d ;" % (key.lower(), smsreport)
    curz = fetch_data_cursor(conn, qry)
    d = fetch_data(curz)
    return d[0] if len(d) > 0 else None

def get_sms_reportfield_by_id(sid, conn = conn):
    qry = " SELECT * FROM messaging_smsreportfield WHERE id = %d ;" % sid
    curz = fetch_data_cursor(conn, qry)
    d = fetch_data(curz)
    return d[0] if len(d) > 0 else None

def get_smsdbconstraints(sms_report, conn = conn):
    qry = " SELECT * FROM messaging_smsdbconstraint WHERE sms_report_id = %d ;" % sms_report.id
    curz = fetch_data_cursor(conn, qry)
    return fetch_data(curz)

def get_appropriate_response( DEFAULT_LANGUAGE_ISO = 'rw', message_type = 'unknown_error', sms_report = None, sms_report_field = None, destination = None, key_value = None, error_code = None ):
    try:
        colm = 'message_%s' % DEFAULT_LANGUAGE_ISO
        msg = SMSMessage.objects.get(message_type = message_type, sms_report = sms_report, sms_report_field = sms_report_field)
        return [message_type, getattr(msg, colm) if getattr(msg, colm) else "" ] 
    except Exception, e:
        try:
            msg = SMSMessage.objects.get(message_type = message_type, sms_report = sms_report, sms_report_field = sms_report_field)
            return [message_type, msg.get_message_type_display() if msg.get_message_type_display() else "" ]
        except Exception, e:
            return ["unknown_error", "Ikosa, kosora ubutumwa bwawe wongere ugerageze"]
    

def get_sms_report_parts(sms_report = None , text = None, DEFAULT_LANGUAGE_ISO = 'rw'):
    """
        You need to return appropriate sms, per appropriate position
    """
    sms_parts = [] ## Store parts of appropriate SMS
    try:
        p = text.split(sms_report.field_separator)### use defined SMS separator to split our sms into parts
        ans = []###store parts that has data
        i = 0 ## i position in parts
        while i < len(p):
            an = p[i]
            if an:
                ans.append(an)
            i += 1
        ### Push all our parts into correct position based on the SMSReport of the Database
        sms_parts = ans
    except Exception, e:
        return e
        
    return sms_parts

def putme_in_sms_reports(sms_report = None, sms_parts = None, DEFAULT_LANGUAGE_ISO = 'rw'):
    positioned_sms = []
    i = 0
    fields = SMSReportField.objects.filter(sms_report = sms_report)
    ##DO I exists as a key the SMSReport?? Then push me to the right position, else leave me where the CHW choose to report me
    while i < len(sms_parts):
        val = sms_parts[i]
        found = False
        try:
            for fp in fields:
                #print val, fp
                ### get in field the ones with key 
                if val == fp.key or val.lower() == fp.key :
                    #print val, fp, i, fp.position_after_sms_keyword
                    positioned_sms = get_my_position(sms_report, positioned_sms, fp, val)
                    #print positioned_sms
                    found = True
                    break
                ### get field with prefix based on data
                elif fp.prefix:
                    if val.__contains__(fp.prefix) or val.__contains__(fp.prefix.upper()):
                        #print val, fp, i, fp.position_after_sms_keyword
                        positioned_sms = get_my_position(sms_report, positioned_sms, fp, val)
                        #print positioned_sms
                        found = True                        
                        break
           
            ### if not found get field at the position then
            if found == False:
                sf = SMSReportField.objects.filter(sms_report = sms_report, position_after_sms_keyword = i)
                key = ''
                if sf.count() > 1:
                    key = val
                elif sf.count() == 1:
                    key = sf[0].key#; print sf
                positioned_sms.append({'position': i, 'value': val, 'key': key })            
                
        except Exception, e:
            print e, val
        i += 1 
    return positioned_sms
        

def get_my_position(sms_report, positioned_sms, fp, val, DEFAULT_LANGUAGE_ISO = 'rw'):
    found = False
    if len(positioned_sms) > 0:         
        for ps in positioned_sms:
            if ps['position'] == int(fp.position_after_sms_keyword):
                new_val = '%s%s%s' % ( ps['value'], sms_report.field_separator, val)
                key_val = ps['key']
                if fp.key in key_val.split(sms_report.field_separator): pass
                else:   key_val = '%s%s%s' % ( ps['key'], sms_report.field_separator, fp.key )
                positioned_sms[positioned_sms.index(ps)] = {'position': int(fp.position_after_sms_keyword), 'value': new_val, 'key': key_val}
                found = True
                break
            else:
                continue
        if found == False  :
            positioned_sms.append({'position': int(fp.position_after_sms_keyword), 'value': val, 'key': fp.key })
    else  :
        positioned_sms.append({'position': int(fp.position_after_sms_keyword), 'value': val, 'key': fp.key })

    return positioned_sms

#from rapidsmsrw1000.apps.api.messaging.utils import *
#sms = SMSReport.objects.get(pk = 1)
#text = 'PRE            1198270072829064                 25.08.2013           11.11.2013        03 02        NR GS YG NP MA DI CL HP WT64.0 HT115 TO NT NH HW 0788660270'
#p = get_sms_report_parts(sms, text)
#pp = putme_in_sms_reports(sms, p)
#check_sms_report_semantics( sms, pp )


def check_sms_report_semantics( sms_report, positioned_sms , today, DEFAULT_LANGUAGE_ISO = 'rw'):
    report = { 'error': [] }
    for ps in positioned_sms:
        try:
            pos = ps['position']
            value = ps['value']
            key = ps['key']
            got = key.split(sms_report.field_separator)
            got_val = value.split(sms_report.field_separator)
            if pos == 0:
            #print value, key
                report.update({'keyword': value})
                continue
            if len(got) > 1:
                for value in got:
                    field = SMSReportField.objects.filter(sms_report = sms_report, position_after_sms_keyword = pos, key = value)
                    if field.exists():
                        report.update({'%s' % value: validate_field(sms_report, report, field[0], got_val[got.index(value)], today, 
                                                                        DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)})
                    else:
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                               message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0],
                                                 '%s(%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                               message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value)])
            else:
                if len(value.split(sms_report.field_separator)) > 1:
                    for value in value.split(sms_report.field_separator):
                        if value.lower()  != key.lower():
                            report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                               message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0],
                                                     '%s(%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                               message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value)])
                        else:
                            field = SMSReportField.objects.filter(sms_report = sms_report, position_after_sms_keyword = pos, key = key)
                            if field.exists():  report.update({'%s' % key: validate_field(sms_report, report, field[0], value, today, DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)})
                            else:
                                report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                                       message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                                        '%s(%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                                       message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value)])
                else:
                    if key:                        
                        field = SMSReportField.objects.filter(sms_report = sms_report, position_after_sms_keyword = pos, key = key)
                        if field.exists():  report.update({'%s' % key: validate_field(sms_report, report, field[0], value, today, DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)})
                        else:
                            report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                                   message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], ', %s(%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                                   message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value)])
                    else:
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                               message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                                '%s(%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = None,
                                                               message_type = 'unknown_field_code', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value)])
        except Exception, e:
            #print e, DEFAULT_LANGUAGE_ISO
            report['error'].append([ 'unknown_error', '%s(%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                           message_type = 'unknown_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1] , ps['value'] ) ])
    try:
        ## Check for dependencies
        parse_dependencies(sms_report, report, DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)
        ## Check for one allowed 
        parse_only_one(sms_report, report, DEFAULT_LANGUAGE_ISO  = DEFAULT_LANGUAGE_ISO)
        ## Check for required and not there
        parse_missing(sms_report, report, DEFAULT_LANGUAGE_ISO  = DEFAULT_LANGUAGE_ISO)
        ## CHECK FOR DB CONSTRAINT
        #### ADD OR OTHER CONSTRAINTS HERE ####
        #if report.get('muac'):            
        #    if (datetime.date.today() - report.get('birth_date')).days < 180:
        #                        report['error'].append(get_error_msg(sms_report = sms_report, sms_report_field = None, 
        #                                   message_type = 'bad_muac_date', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO))

        #if report['error'] == []:   parse_db_constraints(sms_report, report, DEFAULT_LANGUAGE_ISO  = DEFAULT_LANGUAGE_ISO)
    except Exception, e:
        report['error'].append(get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                           message_type = 'unknown_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO))
        
    return report

def validate_field(sms_report, report, field, value, today, DEFAULT_LANGUAGE_ISO ):
    #integer
    #float
    #date
    #string
    #string_digit
 
    if field.prefix:
        if value.__contains__(field.prefix): value = value.replace(field.prefix, '')
        else:   value = value.replace(field.prefix.upper(), '')

    if field.type_of_value == 'string_digit':
        value = parse_length(sms_report, report, field, value, DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)

    elif field.type_of_value == 'string':
        value = parse_length(sms_report, report, field, value, DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)

    elif field.type_of_value == 'date':
        value = parse_date(sms_report, report, field, value, today, DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)

    elif field.type_of_value == 'integer':
        try:
            value = parse_value(sms_report, report, field, int(value), DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)
        except Exception, e:
             report['error'].append([get_appropriate_response( sms_report = sms_report, sms_report_field = field,
                                             message_type = 'only_integer', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0],
                                              '%s (%s)' % (get_appropriate_response( sms_report = sms_report, sms_report_field = field,
                                             message_type = 'only_integer', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO), value )[1] ])

    elif field.type_of_value == 'float':
        try:
            value = parse_value(sms_report, report, field, float(value), DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)
        except Exception, e:
            report['error'].append([get_appropriate_response( sms_report = sms_report, sms_report_field = field,
                                             message_type = 'only_float', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                    '%s (%s)' % (get_appropriate_response( sms_report = sms_report, sms_report_field = field,
                                             message_type = 'only_float', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value ) ] )

    return value
        
def parse_length(sms_report, report, field, value, DEFAULT_LANGUAGE_ISO ):
    if field.minimum_length <= len(value.strip()) <= field.maximum_length:
        return value.strip()
    else:
        response = SMSMessage.objects.filter(sms_report = sms_report, sms_report_field = field, message_type = 'not_in_range')
        if response.exists():
            report['error'].append(['not_in_range',  getattr(response[0], 'message_%s' % DEFAULT_LANGUAGE_ISO) ] )
        else:
            report['error'].append([get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                    '%s (%s)' % (get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value ) ] )

def parse_value(sms_report, report, field, value, DEFAULT_LANGUAGE_ISO ):
    if field.minimum_value <= value <= field.maximum_value:
        return value
    else:
        response = SMSMessage.objects.filter(sms_report = sms_report, sms_report_field = field, message_type = 'not_in_range')
        if response.exists():
            report['error'].append(['not_in_range',  getattr(response[0], 'message_%s' % DEFAULT_LANGUAGE_ISO) ] )
        else:
            report['error'].append([get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0],
                                     '%s (%s)' % (get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value ) ] )

def parse_date(sms_report, report, field, value, today, DEFAULT_LANGUAGE_ISO):

    m3 = re.search("^(\d+)\.(\d+)\.(\d+)$", value) 
    if m3:
        dd = int(m3.group(1))
        mm = int(m3.group(2))
        yyyy = int(m3.group(3))

        d = datetime.date( yyyy, mm, dd )

        if today + datetime.timedelta(days = field.minimum_value) <= d <= today + datetime.timedelta(days = field.maximum_value):
            return d
        else:
            response = SMSMessage.objects.filter(sms_report = sms_report, sms_report_field = field, message_type = 'not_in_range')
            if response.exists():
                report['error'].append(['not_in_range',  getattr(response[0], 'message_%s' % DEFAULT_LANGUAGE_ISO) ] )
            else:
                report['error'].append([get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                        '%s (%s)' % (get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value ) ] )
        
    else:
        response = SMSMessage.objects.filter(sms_report = sms_report, sms_report_field = field, message_type = 'only_date')
        if response.exists():
            report['error'].append(['not_in_range',  getattr(response[0], 'message_%s' % DEFAULT_LANGUAGE_ISO) ] )
        else:
            report['error'].append([get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], ' %s (%s)' % (get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], value ) ] )

def parse_dependencies(sms_report, report, DEFAULT_LANGUAGE_ISO ):

    for r in report.keys():
        field = SMSReportField.objects.filter(sms_report = sms_report, key = r)
        if field.exists():
            field = field[0]
            if field.depends_on_value_of:
                dep  = None
                try:    dep = report[field.depends_on_value_of.key]
                except: continue
                if field.dependency == 'greater':
                    if report[r] > dep:
                        continue
                    else:
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0],
                                                 '%s' % get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1]])
                elif field.dependency == 'greater_or_equal':
                    if report[r] >= dep:
                        continue
                    else:
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0],
                                                 '%s' % get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1]])
                elif field.dependency == 'equal':
                    if report[r] == dep:
                        continue
                    else:
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                                '%s' % get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1]])

                elif field.dependency == 'different':
                    if report[r] != dep:
                        continue
                    else:
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                                '%s' % get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1]])
                elif field.dependency == 'less':
                    if report[r] < dep:
                        continue
                    else:
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                                '%s' % get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1]])
                elif field.dependency == 'less_or_equal':
                    if report[r] <= dep:
                        continue
                    else:
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                                '%s' % get_error_msg(sms_report = sms_report, sms_report_field = field, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1]])
                elif field.dependency == 'jam':                    
                    if dep:
                        jam = SMSReportField.objects.filter(sms_report = sms_report, key = dep.lower())[0]
                        report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = jam, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                                '%s (%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = jam, 
                                                                    message_type = 'dependency_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], field.key)])
                    else:
                        continue
                else:
                    pass
            else:
                continue

    return True

def parse_only_one(sms_report, report, DEFAULT_LANGUAGE_ISO ):
    seens = {}    
    for r in report.keys():
        field = SMSReportField.objects.filter(sms_report = sms_report, only_allow_one = True, key = r )
        if field.exists():
            for f in field:
                if f.position_after_sms_keyword in seens.keys():
                    seens[f.position_after_sms_keyword] += ' %s' % r
                    report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                                   message_type = 'one_value_of_list', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                                            '%s (%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                                   message_type = 'one_value_of_list', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], seens[f.position_after_sms_keyword])])
                    
                else:
                    seens[f.position_after_sms_keyword] = ' %s' % r
                    continue
    #print "THERE : %s" % DEFAULT_LANGUAGE_ISO
    return True


def parse_missing(sms_report, report, DEFAULT_LANGUAGE_ISO ):
    field = SMSReportField.objects.filter(sms_report = sms_report, required = True).order_by('position_after_sms_keyword')
    gots = SMSReportField.objects.filter(sms_report = sms_report, key__in = report.keys())
    onces = [] 
    for f in field:
        if f.key in report.keys():
            continue            
        else:
            if f.dependency == 'jam' and f.depends_on_value_of.key in report.keys():   continue
            elif gots.filter( position_after_sms_keyword = f.position_after_sms_keyword ).exists():   continue
            elif f.position_after_sms_keyword in onces:   continue
            else:
                title = 'title_%s' %  DEFAULT_LANGUAGE_ISO
                category = 'category_%s' %  DEFAULT_LANGUAGE_ISO 
                report['error'].append([get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                           message_type = 'missing_sms_report_field', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0],
                                         '%s (%s)' % (get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                           message_type = 'missing_sms_report_field', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1], 
                                                getattr(f, category) or  getattr(f, title))])
                onces.append(f.position_after_sms_keyword)#;print f.position_after_sms_keyword, onces
    
    return True

def check_tolerances(sms_report, report, DEFAULT_LANGUAGE_ISO):
    tolerances = [ cst for cst in get_smsdbconstraints(sms_report) if cst.constraint == 'tolerance']
    ans = []
    for const in tolerances:
        start   = (datetime.datetime.now() - datetime.timedelta(days = 1)) + datetime.timedelta(days = const.minimum_period_value)
        end     = datetime.datetime.now() + datetime.timedelta(days = const.maximum_period_value)
        refer_sms_report = get_sms_report_by_id(const.refer_sms_report_id)
        fields_keys = get_constraint_fields(const, report)
        got = get_violation(  conn = conn,
                    start = start,
                    end = end,
                    refer_sms_report = refer_sms_report,
                    fields_keys = fields_keys
                 )

        if got: ans.append(got)

    return ans

def check_uniqueness(sms_report, report, DEFAULT_LANGUAGE_ISO):
    uniques = [ cst for cst in get_smsdbconstraints(sms_report) if cst.constraint == 'unique']
    tolerances = check_tolerances(sms_report, report, DEFAULT_LANGUAGE_ISO)
    ans = []
    try:
        for const in uniques:
            start   = (datetime.datetime.now() - datetime.timedelta(days = 1)) + datetime.timedelta(days = const.minimum_period_value)
            end     = datetime.datetime.now() + datetime.timedelta(days = const.maximum_period_value)
            refer_sms_report = get_sms_report_by_id(const.refer_sms_report_id)
            fields_keys = get_constraint_fields(const, report)
            got = get_violation(  conn = conn,
                        start = start,
                        end = end,
                        refer_sms_report = refer_sms_report,
                        fields_keys = fields_keys
                     )

            if got: 
                if sms_report.keyword == "DTH":
                    try:
                        ## check if maternal death
                        if got.death and report.get('md'):
                            query = "SELECT * FROM rw_deaths WHERE indangamuntu = '%s' AND lower(death) LIKE '%s' " % (report.get('nid'), '%md%')
                            got = get_record_by_sql(query);print query
                            if got:   ans.append(got)
                        else: pass
                    except Exception, e: pass;print e
                        
                    try:
                        ## check if the same baby
                        if report.get('child_number') and got.child_number and report.get('birth_date') and got.birth_date:
                            if int(report.get('child_number')) == got.child_number and report.get('birth_date') == got.birth_date.date():
                                ans.append(got)
                        else: pass
                    except Exception, e: pass;print e
                else:
                    ans.append(got) 
 
        if ans and not tolerances:
            report['error'].append(get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                           message_type = 'duplication', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO))

    except Exception, e:
        report['error'].append(get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                           message_type = 'unknown_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO))
    
    return ans

def check_stoppers(sms_report, report, DEFAULT_LANGUAGE_ISO):
    stoppers =  [ cst for cst in get_smsdbconstraints(sms_report) if cst.constraint == 'stopper']
    ans = [] 
    try:
        for const in stoppers:
            start   = (datetime.datetime.now() - datetime.timedelta(days = 1)) + datetime.timedelta(days = const.minimum_period_value)
            end     = datetime.datetime.now() + datetime.timedelta(days = const.maximum_period_value)
            refer_sms_report = get_sms_report_by_id(const.refer_sms_report_id)
            fields_keys = get_constraint_fields(const, report)
            got = get_violation(  conn = conn,
                        start = start,
                        end = end,
                        refer_sms_report = refer_sms_report,
                        fields_keys = fields_keys
                     )

            if got:
                #print got.child_number, got.birth_date, int(report.get('child_number')), report.get('birth_date'), report.get('md'), got.death 
                if sms_report.keyword == "DTH":
                    try:
                        ## check if maternal death
                        if got.death and report.get('md'):
                            query = "SELECT * FROM rw_deaths WHERE indangamuntu = '%s' AND lower(death) LIKE '%s' " % (report.get('nid'), '%md%')
                            got = get_record_by_sql(query)
                            if got:   ans.append(got)
                        else: pass
                    except Exception, e: pass;print e
                        
                    try:
                        ## check if the same baby
                        if report.get('child_number') and got.child_number and report.get('birth_date') and got.birth_date:
                            if int(report.get('child_number')) == got.child_number and report.get('birth_date') == got.birth_date.date():
                                ans.append(got)
                        else: pass
                    except Exception, e: pass;print e
                    
                else:
                    ans.append(got) 
        if ans:
            report['error'].append(get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                           message_type = 'expired_based_data', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO))

    except Exception, e:
        report['error'].append(get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                       message_type = 'unknown_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO))
    
    
    return ans

def check_bases(sms_report, report, DEFAULT_LANGUAGE_ISO):
    bases = [ cst for cst in get_smsdbconstraints(sms_report) if cst.constraint == 'base']
    ans = []
    try:
        for const in bases:
            start   = (datetime.datetime.now() - datetime.timedelta(days = 1)) + datetime.timedelta(days = const.minimum_period_value)
            end     = datetime.datetime.now() + datetime.timedelta(days = const.maximum_period_value)
            refer_sms_report = get_sms_report_by_id(const.refer_sms_report_id)
            fields_keys = get_constraint_fields(const, report)
            got = get_violation(  conn = conn,
                        start = start,
                        end = end,
                        refer_sms_report = refer_sms_report,
                        fields_keys = fields_keys
                     )

            if got: ans.append(got)
 
        if bases and not ans:
            report['error'].append(get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                           message_type = 'missing_based_data', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO))
    except Exception, e:
        report['error'].append(get_error_msg(sms_report = sms_report, sms_report_field = None, 
                                       message_type = 'unknown_error', DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO))
    
    return ans

#motherdeath   = "SELECT indexcol FROM deathmessage WHERE indangamuntu = %s AND lower(death) = 'md' " % ( self.fields[0].data() )
#
#childdeath    = "SELECT indexcol FROM deathmessage WHERE indangamuntu = %s AND number =  %s AND birth_date = %s ;" % (
#											self.fields[0].data(), self.fields[1].data(), , self.fields[2].data())
#
#miscarriage   = "SELECT (SELECT principal FROM redmessage_red_symptom WHERE principal = redmessage.indexcol AND lower(value) = 'he' ) 
#			FROM redmessage WHERE indangamuntu = '%s' AND report_date BETWEEN %s AND %s ;" % ( self.fields[0].data() )
#
#pregnancy = "SELECT indexcol FROM pregmessage WHERE indangamuntu = %s AND lmp BETWEEN %s AND %s;" % (
#												self.fields[0].data(), self.fields[1].data())
#
#birth  = "SELECT indexcol FROM birmessage WHERE indangamuntu = %s AND number =  %s AND birth_date = %s;" % (
#											self.fields[0].data(), self.fields[1].data(), , self.fields[2].data())

#get a violation per constraint
## if unique
# get if we have a record that violate this then throw it
# refer to between maximum_period_value, minimum_period_value
#other_fields_keys
#refer_sms_report_field_id
#refer_sms_report_id
#sms_report_field_id
#sms_report_id

def get_violation(  conn = conn,
                    start = datetime.datetime.now() - datetime.timedelta(days = 1),
                    end = datetime.datetime.now(),
                    refer_sms_report = None,
                    fields_keys = None
                 ):
    table = settings.TABLE_MAP.get(refer_sms_report.keyword)
    if not table: return []    
    qry = " SELECT * FROM %s WHERE report_date BETWEEN '%s' AND '%s' " % (table, start, end)
    if fields_keys:
        wcllist = []
        for x in fields_keys:
            if x[1]: dt = " %s = '%s' " % (settings.KEYS_MAP.get(x[0]) if settings.KEYS_MAP.get(x[0]) else x[0], x[1])
            #elif table in ["deathmessage", "rw_deaths"]:    dt = " %s = '%s' " % (settings.KEYS_MAP.get(x[0]) if settings.KEYS_MAP.get(x[0]) else x[0], x[0]) 
            else:    dt = " %s IS NOT NULL" % (settings.KEYS_MAP.get(x[0]) if settings.KEYS_MAP.get(x[0]) else x[0])    
            wcllist.append(dt)
        wcl = "AND".join( m for m in wcllist )
        if wcl.strip() != '':   qry = " %s AND %s ;" % (qry, wcl)
    ### TODO in case column does not exists ... now is returning []
    ##print qry, fields_keys, dt
    curz = fetch_data_cursor(conn, qry)
    d = fetch_data(curz)
    return d[0] if len(d) > 0  else None

def get_constraint_fields(const, report):
    allfs = const.other_fields_keys.split(";") if const.other_fields_keys else []
    fs = [af for af in allfs if report.get(af)]
    fs.append(get_sms_reportfield_by_id( const.refer_sms_report_field_id).key)
    fields_keys = []
    for f in fs:
        if f != 'created':  fields_keys.append((f, report.get(f) if f not in settings.NUMBER_KEYS_MAP else settings.NUMBER_KEYS_MAP.get(f)))#;print const.constraint, report
    return fields_keys or None

def parse_db_constraints(sms_report, report, DEFAULT_LANGUAGE_ISO):
    """ Make you will save it in the DB correctly"""
    check_uniqueness(sms_report, report, DEFAULT_LANGUAGE_ISO)
    check_bases(sms_report, report, DEFAULT_LANGUAGE_ISO)
    check_stoppers(sms_report, report, DEFAULT_LANGUAGE_ISO)

    return True


def get_error_msg(sms_report , sms_report_field , DEFAULT_LANGUAGE_ISO , message_type = 'unknown_error', key_value = None, error_code = None): 
    response = SMSMessage.objects.filter(sms_report = sms_report, sms_report_field = sms_report_field, message_type = message_type)
    if response.exists():
        return [message_type, getattr(response[0], 'message_%s' % DEFAULT_LANGUAGE_ISO)]
    else:
        if sms_report_field:
            title = 'title_%s' %  DEFAULT_LANGUAGE_ISO
            category = 'category_%s' %  DEFAULT_LANGUAGE_ISO   
            return [get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], '%s (%s)' % (get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1],
                                     getattr(sms_report_field, category) or  getattr(sms_report_field, title))]
        return [get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[0], 
                ' %s' % get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO)[1]]

def locate_object(object_inst, ref):
    for l in LocationType.objects.all():
        setattr(    object_inst, 
                    camel_to_underscore_lower(l.name), 
                    getattr(ref, camel_to_underscore_lower(l.name))
                )
    return object_inst

def locate_chw(chw):
    loxn  = {
		    'province_pk': chw.province.pk or 0,
		    'district_pk': chw.district.pk or 0,
		    'health_center_pk': chw.health_centre.pk or 0,
            'referral_hospital_pk': chw.referral_hospital.pk or 0,
		    'sector_pk': chw.sector.pk or 0,
		    'cell_pk': chw.cell.pk or 0,
		    'village_pk': chw.village.pk or 0,
		    'nation_pk': chw.nation.pk or 0,
		    'reporter_pk': chw.pk or 0,
		    'reporter_phone': chw.telephone_moh or ''
	    }
    
    return loxn

def message_details(chw, msg):
    loxn = locate_chw(chw)
    loxn.update({'report_date': msg.date})
    return loxn


def store_components(mname, msg, msgtxt, fid, loxer):
  princ = {'oldid': fid, 'message': msgtxt}
  auxil = {}
  seen  = set()
  for k in msg.entries:
    chose = msg.entries[k]
    if chose.several_fields:
      subk  = '%s_%s' % (mname, k)
      seen.add(subk)
      naux  = auxil.get(subk, [])
      naux.extend(chose.data())
      auxil[subk] = naux
    else:
      princ[k]  = chose.data()
  princ.update(loxer)
  ix  = orm.ORM.store(mname, princ)

  for k in auxil:
    val = auxil[k]
    for v in val:
      tst = {'principal': ix, 'value': v}
      tst.update(loxer)
      orm.ORM.store(k, tst)
  return seen, ix

def store_failures(err, msg, fid, loxer):
  pos   = 0
  for fc in err.errors:
    fc  = fc[0] if type(fc) == type(('', None)) else fc
    tst = {'oldid': fid, 'message': msg, 'failcode': fc, 'failpos': pos}
    tst.update(loxer)
    orm.ORM.store('failed_transfers', tst)
    pos = pos + 1

def store_treatment(fid, stt, loxer):
  tst = {
    'oldid': fid,
    'success': stt
  }
  tst.update(loxer)
  return orm.ORM.store(TREATED[0], tst, migrations = TREATED[1])

def get_sms_error_code( error, DEFAULT_LANGUAGE_ISO = 'rw'):
    try:
        msg_type = error[0]
        err = error[1][0].column_name if type(error[1]) == tuple else error[1].column_name
        msg, created = SMSErrorCode.objects.get_or_create(message_type = msg_type)
        #print "There :%s " % msg
        return [msg.message_type, getattr(msg, "message_%s" % DEFAULT_LANGUAGE_ISO) if hasattr(msg, "message_%s" % DEFAULT_LANGUAGE_ISO) else '']
    except Exception, e: 
        #print e
        return get_appropriate_response( DEFAULT_LANGUAGE_ISO = DEFAULT_LANGUAGE_ISO, message_type = 'unknown_error')

def parseObj(chw, message, pgc = conn, errors = []):
    try:
        org = message.text
        tbn = TREATED    	
        loxn    =   message_details(chw, message)
        curz    =   pgc.cursor()
        acrow   =   0
        succ    =   False
        stbs  = set()
        try:

            try:
                ans, ents = rmessages.ThouMessage.parse(message.text, messageassocs.ASSOCIATIONS, message.date)
                ans.add_extra(loxn)
                mname = str(ans.__class__).split('.')[-1].lower()#;print ans.data()
                if errors:
                    for err in errors:
                        store_failures(rmessages.ThouMsgError('%s' % err[1], [('%s' % err[0], None)]), '%s #%d' % (err[1], message.id ), message.id, loxn)
                    raise rmessages.ThouMsgError('%s' % err[1], [('%s' % err[0], None)])
                else:
                    
                    nstbs, ix = store_components(mname, ans, message.text, message.id, loxn)
                    stbs.add(mname)
                    stbs  = stbs.union(nstbs)
                    etbs  = processor.process_entities(ans, ents)
                    #print ans, ents
                    stbs  = stbs.union(etbs)
                    succ  = True
                    #print mname, nstbs, etbs
                    # TRACK IT ##
                    sql = 'SELECT * FROM %s WHERE %s = %s' % ( mname, 'indexcol', ix)
                    drecord = get_record_by_sql(sql)
                    #print drecord, sql
                    track_notifications(mname, drecord)
                    ## END OF TRACK IT ##
            except rmessages.ThouMsgError, e:
                for err in e.errors: errors.append(get_sms_error_code( err, DEFAULT_LANGUAGE_ISO = chw.language))##;print err
                store_failures(e, message.text, message.id, loxn)

            acrow = store_treatment(message.id, succ, loxn)
                
        except UnicodeEncodeError, e:
            errors.append(get_appropriate_response( DEFAULT_LANGUAGE_ISO = chw.language, message_type = 'bad_encoding'))
            # Is this sufficient?
            store_failures(rmessages.ThouMsgError('Badly-encoded message.', [('bad_encoding', None)]), 'Badly-encoded message #%d' % (message.id, ), message.id, loxn)

        curz.execute('UPDATE messagelog_message SET transferred = TRUE WHERE id = %d' % (message.id, ))
        orm.ORM.store(tbn[0], {'indexcol': acrow, 'deleted': True})
        curz.close()
        pgc.commit()
        #for tb in stbs: print tb
        if succ == False:
        #    errors.append([ 'unknown_error', 'Error(Ikosa)'])
            return False
        return True 

    except Exception, e:
        print e
        #errors.append([ 'unknown_error', 'Error(Ikosa)'])
        pass#print e
        
    return False

def track_this_sms_report(report = None, reporter = None):
    if report is None:
        pass
    else:
        m = SMSReportTrack()
        for key in report.keys():
            if key == 'error':
                for k in report['error']: setattr(m, k[0], k[1])
            elif key == 'keyword':
                setattr(m, 'keyword', report['keyword'])
            else:   setattr(m, '%s_key' % key, report[key])
            
        ans = []
        m.save()
        return m
    return True

def distinct_sms_report_fields():
    """ 
        mysql backend does not support distinct
    """
   
    fs_keys = SMSReportField.objects.all().values_list('key').distinct()
    ans = [ SMSReportField.objects.filter(key__in = f)[0].id for f in fs_keys ]
    fs = SMSReportField.objects.filter( pk__in  = ans ) 
    
    return fs.order_by('key')


def get_field_name(f):
    f_key = getattr(f, 'key')
    f_key = "%s_key" % f_key
    return f_key

def get_model_object(app_label, model_name):
    app = get_app(app_label)
    m = get_models(app)
    for m1 in m:
        if m1.__name__ == model_name:
            return m1
    return None

def propagate_db(model_object):

    try:
        
        try: 
            obj = model_object()
            table = obj._meta.db_table
            cursor = connection.cursor()
            cursor.execute("drop table %s" % table)
            cursor.close()
        except Exception, e:
            pass
            
        return_code = subprocess.call("cd %s && ./manage.py syncdb" % os.getcwd(), shell=True)  
    except Exception,e:
        return False
        
    return True
    

def create_or_update_model(app_label = 'messaging', model_name = 'Test', model_fields = [], filters = [], custom = [],
                                         links = [], locations = [], default_return = 'raw_sms'):
    """
        Field in the form of {key, type_of_value, length(min, max), required, value(min,max)} 
        locations are all Location Types already defined        
    """

    try:
        tab = add_four_space()
        status = False
        start_text = "##Start of %s" % model_name
        end_text = "##End of %s" % model_name

        start_fields_text = "##Start of %s Fields" % model_name
        end_fields_text = "##End of %s Fields" % model_name

        start_meta_text = "##Start of %s Meta" % model_name
        end_meta_text = "##End of %s Meta" % model_name

        start_methods_text = "##Start of %s Methods" % model_name
        end_methods_text =  "##End of %s Methods" % model_name
        
        locs_data = "".join("\n%s%s = models.ForeignKey(%s, null = True, blank = True)" % (tab, camel_to_underscore_lower(l), camelCase(l)) for l in locations)
        links_data = "".join("\n%s%s = models.ForeignKey(%s, null = True, blank = True)" % (tab, camel_to_underscore_lower(l), camelCase(l)) for l in links)
        custom_data = "".join("%s" % c['data'] for c in custom)
        ans = []
        for f in model_fields:
            min_lf = getattr(f, 'minimum_length')
            max_lf = getattr(f, 'maximum_length')
            min_vf = getattr(f, 'minimum_value')
            max_vf = getattr(f, 'maximum_value')
            type_of_vf = getattr(f, 'type_of_value')
            required_f = getattr(f, 'required')
            
            if  type_of_vf == 'integer':
                
                vf = "\n%s%s = models.IntegerField(validators = [MinValueValidator(%d), MaxValueValidator(%d)], null = %s,  blank = %s)" % (tab,
                                                                                 get_field_name(f), min_vf, max_vf, required_f, required_f)
                
            elif  type_of_vf == 'float':
                
                vf = "\n%s%s = models.IntegerField(validators = [MinValueValidator(%d), MaxValueValidator(%d)], null = %s,  blank = %s)" % (tab,
                                                                                 get_field_name(f), min_vf, max_vf, required_f, required_f)
                
            elif type_of_vf == 'string':
                
                vf = "\n%s%s = models.CharField(max_length = %d , validators = [MinLengthValidator(%d)], null = %s,  blank = %s)" % (tab, 
                                                    get_field_name(f), max_lf, min_lf, required_f, required_f)
                
            elif type_of_vf == 'string_digit':
                
                vf = "\n%s%s = models.CharField(max_length = %d , validators = [MinLengthValidator(%d)], null = %s,  blank = %s)" % (tab,
                                                                         get_field_name(f), max_lf, min_lf, required_f, required_f)
                              
            elif type_of_vf == 'date':
                
                vf = "\n%s%s = models.DateField(validators = [MinValueValidator(%d), MaxValueValidator(%d)], null = %s,  blank = %s)" % (tab, 
                                                                            get_field_name(f), min_vf, max_vf, required_f, required_f)
                
            else:
                vf = "\n%s%s = models.TextField(validators = [MinLengthValidator(%d), MaxLengthValidator(%d)], null = %s,  blank = %s)" % (tab,
                                                                         get_field_name(f), min_lf, max_lf, required_f, required_f)
            ans.append(vf)
            
               
        default_value = "\n\n%sdef __unicode__(self):\n%s%sreturn self.%s" % (tab, tab, tab, default_return)
        meta_value = "\n\n%sclass Meta:\n%s%spermissions = (\n%s%s%s('can_view', 'Can view'),\n%s%s)" % (tab, tab, tab, tab, tab, tab, tab, tab )
        admin_locs = "".join("'%s', "  % camel_to_underscore_lower(l) for l in locations )
        admin_links = "".join("'%s', "  % camel_to_underscore_lower(l) for l in links )
        admin_fields = "".join("'%s', "  % get_field_name(f).lower() for f in model_fields )
        filter_fields = "".join("'%s', "  % f for f in filters )
        variables_data = "".join("%s" % an for an in ans)
        
        admin_value = "\n%s\nclass %sAdmin(admin.ModelAdmin):\
                                                        \n%slist_filter = (%s )\
                                                        \n%sexportable_fields = (%s %s )\
                                                        \n%ssearch_fields = (%s %s )\
                                                        \n%slist_display = (%s %s )\
                                                    \n%sactions = (export_model_as_csv, export_model_as_excel)\
                        \n\nadmin.site.register(%s, %sAdmin)\n%s\n" \
                        % (start_text, model_name, 
                           tab, filter_fields,
                           tab, filter_fields, admin_fields,
                           tab, filter_fields, admin_fields, 
                           tab, filter_fields, admin_fields,
                           tab,
                           model_name, model_name, end_text)
        admin_rep = "\nclass %sAdmin(admin.ModelAdmin):\
                                                        \n%slist_filter = (%s )\
                                                        \n%sexportable_fields = (%s %s )\
                                                        \n%ssearch_fields = (%s %s )\
                                                        \n%slist_display = (%s %s )\
                                                    \n%sactions = (export_model_as_csv, export_model_as_excel)\
                        \n\nadmin.site.register(%s, %sAdmin)\n" \
                        % (model_name, 
                           tab, filter_fields, 
                           tab, filter_fields, admin_fields,
                           tab, filter_fields, admin_fields,
                           tab, filter_fields, admin_fields,
                           tab,
                           model_name, model_name)
        data = "\n%s\nclass %s(models.Model):\n%s%s%s%s%s\n%s\n" \
                    % (start_text, model_name, custom_data, variables_data, locs_data, default_value, meta_value, end_text)
        data_rep = "\nclass %s(models.Model):\n%s%s%s%s%s\n" \
                    % (model_name, custom_data, variables_data, locs_data, default_value, meta_value)

                
        ##CHEK IF MODEL NOT DEFINED ALREADY
        m_filename = '%s/%s/models.py' % (API_PATH, app_label)
        m_f = get_block_of_text_link(m_filename, model_name, start_text,  end_text)
        
        if m_f:
            #print "THERE 1"
            if m_f['lines'] and m_f['start'] and m_f['end']:
                x = replace_block_of_text_link(m_filename, m_f['lines'], m_f['start'], m_f['end'], replace_with = data_rep)
                #print x 
            else:
                with open(m_filename, "a") as f:
                    f.write(data)
                    f.close()
        
        ##CHEK IF MODEL IN ADMIN NOT DEFINED ALREADY
        a_filename = '%s/%s/admin.py' % (API_PATH, app_label)
        a_f = get_block_of_text_link(a_filename, model_name, start_text,  end_text)
        if a_f:
            if a_f['lines'] and a_f['start'] and a_f['end']:
                y = replace_block_of_text_link(a_filename, a_f['lines'], a_f['start'], a_f['end'], replace_with = admin_rep) 
                #print y
            else:
                with open(a_filename, "a") as f:
                    f.write(admin_value)
                    f.close()

        status = propagate_db(get_model_object(app_label, model_name))
                                   
        return status

    except Exception, e:
        #print e
        return False
"""
def fast_chw_correction(telephone_moh)
    chw = Reporter.objects.get(telephone_moh = telephone_moh)
    contact, created = Contact.objects.get_or_create(name = chw.national_id)
    contact.language = chw.language
    contact.save()
    b = Backend.objects.get(id = 1)
    connection, created = Connection.objects.get_or_create(contact = contact, backend = b, identity = chw.telephone_moh)
    connection.save()
    return True
"""
def import_staff(filepath = "api/messaging/xls/staff.xls", sheetname = "staff"):
    book = open_workbook(filepath)
    sheet = book.sheet_by_name(sheetname)
    
    for row_index in range(sheet.nrows):
        if row_index < 1: continue   
        try:
            surname             = sheet.cell(row_index,1).value
            fosa                = str(int(sheet.cell(row_index,2).value))
            telephone           = str(sheet.cell(row_index,5).value)
            national_id         = str(sheet.cell(row_index,6).value)
            
            
            hospital = Hospital.objects.get(code = fosa)
            hc = HealthCentre.objects.get( code = Reporter.objects.filter(referral_hospital = hospital)[5].health_centre.code )
            village = Village.objects.get( code = Reporter.objects.filter( health_centre = hc)[5].village.code )
            role = Role.objects.get(code = 'asm')
            if len(national_id.strip()) != 16: national_id = telephone.strip() + "000000"
            if len(telephone) == 10: telephone = "+25" + telephone.strip() 
            #print surname, fosa, telephone, national_id
            chw, created = Reporter.objects.get_or_create( telephone_moh = telephone )
                        
            chw.surname = surname
            chw.role = role
            chw.telephone_moh = telephone
            chw.national_id = national_id
            chw.referral_hospital = hospital
            chw.health_centre = hc
            chw.village = village
            chw.cell = village.cell
            chw.sector = village.sector
            chw.district = hospital.district
            chw.province = hospital.province
            chw.nation = hospital.nation
            chw.language = "rw"
            chw.deactivated = False
            chw.is_active = True
            chw.correct_registration = True
            try:
                chw.save()
                contact, created = Contact.objects.get_or_create(name = chw.national_id)
                contact.language = chw.language
                contact.save()
                b = Backend.objects.get(id = 1)
                connection, created = Connection.objects.get_or_create(backend = b, identity = chw.telephone_moh)
                connection.contact = contact
                connection.save(); print chw, contact, connection
                naddr = "test%s" % chw.id
                npwd = "test%s" % chw.id
                salt  = str(random.random()).join([str(random.random()) for x in range(2)])
                rslt  = sha.sha('%s%s' % (salt, npwd))
                thing = {'salt': salt, 'address': naddr, 'sha1_pass': rslt.hexdigest(), 'district_pk': chw.district.id, 'province_pk': chw.province.id, 'health_center_pk': chw.health_centre.id}
                orm.ORM.store('ig_admins', thing)
                cmd = Smser()
                message = "Dear %s, you are registered to RAPIDSMS RWANDA, as %s, in the village of %s, %s Health Centre, for testing purpose. Your username is %s and password is %s, login at http://41.74.172.34:8081 .Thank you!" % (chw.surname, chw.role.name, chw.village.name, chw.health_centre.name, naddr, npwd)
                print message
                cmd.send_message_via_kannel(chw.telephone_moh, message )
            except Exception, e:
                print e, chw.telephone_moh, chw.national_id
                        
            """print  (chw.id, 
                    chw.surname,
                    chw.role,
                    chw.sex,
                    chw.education_level,
                    chw.date_of_birth,
                    chw.join_date,
                    chw.national_id,
                    chw.telephone_moh,
                    chw.village,
                    chw.cell,
                    chw.sector,
                    chw.health_centre,
                    chw.referral_hospital,
                    chw.district,
                    chw.province,
                    chw.nation,
                    chw.created,
                    chw.updated,
                    chw.language,
                    chw.deactivated,
                    chw.is_active,
                    chw.last_seen,
                    chw.correct_registration)"""

    
        except Exception, e:
            print e, row_index
            pass

def import_sms_report(filepath = "api/messaging/smsreport.xls", sheetname = "smsreport"):
    book = open_workbook(filepath)
    sheet = book.sheet_by_name(sheetname)
    
    for row_index in range(sheet.nrows):
        if row_index < 1: continue   
        try:
            title_en            = sheet.cell(row_index,0).value
            title_rw            = sheet.cell(row_index,1).value
            keyword             = sheet.cell(row_index,2).value
            description         = sheet.cell(row_index,3).value
            field_separator     = sheet.cell(row_index,4).value
            in_use              = sheet.cell(row_index,5).value
            case_sensitive      = sheet.cell(row_index,6).value
            syntax_regex        = sheet.cell(row_index,7).value
            #created             = sheet.cell(row_index,8).value 

            #print title, keyword, description, field_separator, in_use , case_sensitive, syntax_regex, created
            sms_report, created = SMSReport.objects.get_or_create(keyword = keyword)

            sms_report.title_en = title_en
            sms_report.title_rw = title_rw
            sms_report.description = description
            sms_report.field_separator = field_separator
            sms_report.in_use = in_use
            sms_report.case_sensitive = case_sensitive
            sms_report.syntax_regex = syntax_regex
            #sms_report.created = created
                        
            sms_report.save()                   
            
            print "\ntitle : %s\n keyword : %s\n description : %s\n field_separator : %s\n in_use : %s\n case_sensitive: %s\n syntax_regex : %s\n \
                    created: %s \n" % (sms_report.title_en, sms_report.keyword, sms_report.description, sms_report.field_separator, sms_report.in_use, 
                        sms_report.case_sensitive, sms_report.syntax_regex, sms_report.created)
            
        except Exception, e:
            print e, row_index
            pass

def import_sms_report_field(filepath = "api/messaging/smsreportfield.xls", sheetname = "smsreportfield"):
    book = open_workbook(filepath)
    sheet = book.sheet_by_name(sheetname)
    
    for row_index in range(sheet.nrows):
        if row_index < 1: continue   
        try:
            title_en                    = sheet.cell(row_index, 0).value
            title_rw                    = sheet.cell(row_index, 1).value
            category_en                 = sheet.cell(row_index, 2).value
            category_rw                 = sheet.cell(row_index, 3).value
            sms_report_keyword          = sheet.cell(row_index, 4).value 
            prefix                      = sheet.cell(row_index, 5).value
            key                         = sheet.cell(row_index, 6).value 
            description                 = sheet.cell(row_index, 7).value 
            type_of_value               = sheet.cell(row_index, 8).value 
            upper_case                  = sheet.cell(row_index, 9).value 
            lower_case                  = sheet.cell(row_index, 10).value 
            try:    minimum_value               = int( sheet.cell(row_index, 11).value )
            except Exception, e: minimum_value = None
            try:    maximum_value               = int( sheet.cell(row_index, 12).value )
            except Exception, e: maximum_value = None
            try:    minimum_length              = int( sheet.cell(row_index, 13).value )
            except Exception, e: minimum_length = None
            try:    maximum_length              = int( sheet.cell(row_index, 14).value )
            except Exception, e: maximum_length = None 
            try:    position_after_sms_keyword  = int( sheet.cell(row_index, 15).value )
            except Exception, e: position_after_sms_keyword = None 
            depends_on_value_of         = sheet.cell(row_index, 16).value 
            dependency                  = sheet.cell(row_index, 17).value 
            allowed_value_list          = sheet.cell(row_index, 18).value 
            only_allow_one              = sheet.cell(row_index, 19).value 
            required                    = sheet.cell(row_index, 20).value 
            
            #print sms_report_keyword, prefix, key, description, type_of_value, upper_case, lower_case, minimum_value, maximum_value,\
            #        minimum_length, maximum_length, position_after_sms_keyword, depends_on_value_of, dependency, allowed_value_list, only_allow_one, required
            
            sms_report                                   = SMSReport.objects.get(keyword = sms_report_keyword)
            try:    dep                                  = SMSReportField.objects.get(key = depends_on_value_of, sms_report = sms_report)
            except Exception, e:    dep                  = None#;print e
            sms_report_field, created                    = SMSReportField.objects.get_or_create(key = key, sms_report = sms_report, 
                                                                                                    position_after_sms_keyword = position_after_sms_keyword)
            sms_report_field.title_en                    = title_en
            sms_report_field.title_rw                    = title_rw 
            sms_report_field.category_en                 = category_en
            sms_report_field.category_rw                 = category_rw            
            sms_report_field.prefix                      = prefix
            sms_report_field.description                 = description
            sms_report_field.type_of_value               = type_of_value
            sms_report_field.upper_case                  = upper_case
            sms_report_field.lower_case                  = lower_case
            sms_report_field.minimum_value               = minimum_value
            sms_report_field.maximum_value               = maximum_value
            sms_report_field.minimum_length              = minimum_length
            sms_report_field.maximum_length              = maximum_length
            sms_report_field.depends_on_value_of         = dep#;print "DEPEND:: %s" % depends_on_value_of
            sms_report_field.dependency                  = dependency
            sms_report_field.allowed_value_list          = allowed_value_list
            sms_report_field.only_allow_one              = only_allow_one
            sms_report_field.required                    = required
            #print sms_report_field, minimum_value, maximum_value, minimum_length, maximum_length, position_after_sms_keyword
            sms_report_field.save()                   
            
            print   sms_report_field.sms_report                  ,\
                    sms_report_field.prefix                      ,\
                    sms_report_field.key                         ,\
                    sms_report_field.description                 ,\
                    sms_report_field.type_of_value               ,\
                    sms_report_field.upper_case                  ,\
                    sms_report_field.lower_case                  ,\
                    sms_report_field.minimum_value               ,\
                    sms_report_field.maximum_value               ,\
                    sms_report_field.minimum_length              ,\
                    sms_report_field.maximum_length              ,\
                    sms_report_field.position_after_sms_keyword  ,\
                    sms_report_field.depends_on_value_of         ,\
                    sms_report_field.dependency                  ,\
                    sms_report_field.allowed_value_list          ,\
                    sms_report_field.only_allow_one              ,\
                    sms_report_field.required                    

            
        except Exception, e:
            print e, row_index
            pass

def import_sms_language(filepath = "api/messaging/smslanguage.xls", sheetname = "smslanguage"):
    book = open_workbook(filepath)
    sheet = book.sheet_by_name(sheetname)
    
    for row_index in range(sheet.nrows):
        if row_index < 1: continue   
        try:
            language_id                 = sheet.cell(row_index, 0).value
            language_name               = sheet.cell(row_index, 1).value
            language_iso_639_1_code     = sheet.cell(row_index, 2).value 
            language_description        = sheet.cell(row_index, 3).value
            language_created            = sheet.cell(row_index, 4).value
            
            #print language_id, language_name, language_iso_639_1_code, language_description, language_created
            
            sms_language, created                         = SMSLanguage.objects.get_or_create(
                                                                                            iso_639_1_code = language_iso_639_1_code
                                                                                            
                                                                                            )

            sms_language.name           = language_name                                                                                            
            sms_language.description    = language_description
            #sms_language.created        = language_created
            
            sms_language.save()                   
            
            print   sms_language.iso_639_1_code , sms_language.name, sms_language.description, sms_language.created                                   
            
        except Exception, e:
            print e, row_index
            pass

def import_sms_message(filepath = "api/messaging/smsmessage.xls", sheetname = "smsmessage"):
    book = open_workbook(filepath)
    sheet = book.sheet_by_name(sheetname)
    
    for row_index in range(sheet.nrows):
        if row_index < 1: continue   
        try:
            message_type                = sheet.cell(row_index, 0).value
            sms_report_keyword          = sheet.cell(row_index, 1).value 
            sms_report_field_key        = sheet.cell(row_index, 2).value
            dest                        = sheet.cell(row_index, 3).value
            description                 = sheet.cell(row_index, 4).value
            message_en                  = sheet.cell(row_index, 5).value 
            message_rw                  = sheet.cell(row_index, 6).value 
            
            #print message_type, sms_report_keyword, sms_report_field_key, message_en, message_rw
            
            try:    sms_report                           = SMSReport.objects.get(keyword = sms_report_keyword)
            except Exception, e:    sms_report           = None
            try:    destination                          = Group.objects.get(name__iexact = dest)
            except Exception, e:    destination          = None
            try:    sms_report_field                     = SMSReportField.objects.get( key = sms_report_field_key, sms_report = sms_report)
            except Exception, e:    sms_report_field     = None
            
            sms_message, created                         = SMSMessage.objects.get_or_create(message_type = message_type, sms_report = sms_report,
                                                                                                 sms_report_field = sms_report_field)

            sms_message.sms_report                       = sms_report
            sms_message.sms_report_field                 = sms_report_field
            sms_message.destination                      = destination
            sms_message.description                      = description
            sms_message.message_en                       = message_en
            sms_message.message_rw                       = message_rw

            
            sms_message.save()                   
            
            print   sms_message.message_type                        ,\
                    sms_message.sms_report                          ,\
                    sms_message.sms_report_field                    ,\
                    sms_message.destination                          ,\
                    sms_message.message_en                          ,\
                    sms_message.message_rw                          
            
        except Exception, e:
            print e, row_index
            pass

def import_sms_db_constraint(filepath = "api/messaging/smsdbconstraint.xls", sheetname = "smsdbconstraint"):
    book = open_workbook(filepath)
    sheet = book.sheet_by_name(sheetname)
    
    for row_index in range(sheet.nrows):
        if row_index < 1: continue   
        try:
            sms_report_keyword          = sheet.cell(row_index, 0).value
            sms_report_field_key        = sheet.cell(row_index, 1).value 
            constraint                  = sheet.cell(row_index, 2).value
            fields_list                 = sheet.cell(row_index, 3).value
            minimum_period_value        = sheet.cell(row_index, 4).value
            maximum_period_value        = sheet.cell(row_index, 5).value
            refer_sms_report_keyword    = sheet.cell(row_index, 6).value 
            refer_sms_report_field_key  = sheet.cell(row_index, 7).value 
             
            
            #print message_type, sms_report_keyword, sms_report_field_key, message_en, message_rw
            
            try:    sms_report                           = SMSReport.objects.get(keyword = sms_report_keyword)
            except Exception, e:    sms_report           = None
            try:    sms_report_field                     = SMSReportField.objects.get( key = sms_report_field_key, sms_report = sms_report)
            except Exception, e:    sms_report_field     = None
            
            try:    refer_sms_report                           = SMSReport.objects.get(keyword = refer_sms_report_keyword)
            except Exception, e:    refer_sms_report           = None
            try:    refer_sms_report_field                     = SMSReportField.objects.get( key = refer_sms_report_field_key, sms_report = refer_sms_report)
            except Exception, e:    refer_sms_report_field     = None
            
            sms_db_constraint, created                   = SMSDBConstraint.objects.get_or_create(sms_report = sms_report,
                                                                                                 sms_report_field = sms_report_field, constraint = constraint)

            sms_db_constraint.refer_sms_report                       = refer_sms_report
            sms_db_constraint.refer_sms_report_field                 = refer_sms_report_field
            sms_db_constraint.minimum_period_value                   = minimum_period_value
            sms_db_constraint.maximum_period_value                   = maximum_period_value
            sms_db_constraint.other_fields_keys                      = fields_list

            
            sms_db_constraint.save()                   
            
            print   sms_db_constraint.sms_report                        ,\
                    sms_db_constraint.sms_report_field                  ,\
                    sms_db_constraint.constraint                   ,\
                    sms_db_constraint.refer_sms_report                        ,\
                    sms_db_constraint.refer_sms_report_field                  ,\
                    sms_db_constraint.minimum_period_value                    ,\
                    sms_db_constraint.maximum_period_value                    ,\
            
        except Exception, e:
            print e, row_index
            pass
    
