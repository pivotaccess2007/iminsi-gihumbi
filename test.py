from messages import rmessages
from entities import processor
from datetime import datetime
import messageassocs
import psycopg2

date = datetime.now()


conn  = psycopg2.connect(
          dbname = 'thousanddays',
          host 	 = 'localhost',
            user = 'thousanddays',
        password = 'thousanddays'
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

def get_record_by_query(conn, query_string):
    cursor = fetch_data_cursor(conn, query_string)
    data = fetch_data(cursor)
    if data: return data[0]    
    return None


def locate_chw(chw, date):
    loxn  = {
		    'province_pk': chw.province_id or 0,
		    'district_pk': chw.district_id or 0,
		    'health_center_pk': chw.health_centre_id or 0,
		    'sector_pk': chw.sector_id or 0,
		    'cell_pk': chw.cell_id or 0,
		    'village_pk': chw.village_id or 0,
		    'nation_pk': chw.nation_id or 0,
		    'reporter_pk': chw.id or 0,
		    'reporter_phone': chw.telephone_moh or '',
		    'report_date': date
	    }
    
    return loxn



text1 = 'DEP 1234567890123456'
text2 = 'DEP 1234567890123456 01 12.12.2013'
ans, ents = rmessages.ThouMessage.parse(text1, messageassocs.ASSOCIATIONS, date)
print [ an.data() for an in ans.fields]
print ents
etbs  = processor.process_entities(ans, ents)
ans, ents = rmessages.ThouMessage.parse(text2, messageassocs.ASSOCIATIONS, date)
print [ an.data() for an in ans.fields]
print ents
etbs  = processor.process_entities(ans, ents)
etbs  = processor.process_entities(ans, ents)

text4 = 'DTH 1234567890123456 01 12.12.2013 HO ND'
text5 = 'DTH 1234567890123456 HO MD'
ans, ents = rmessages.ThouMessage.parse(text4, messageassocs.ASSOCIATIONS, date)
print [ an.data() for an in ans.fields]
print ents
etbs  = processor.process_entities(ans, ents)
ans, ents = rmessages.ThouMessage.parse(text5, messageassocs.ASSOCIATIONS, date)
print [ an.data() for an in ans.fields]
print ents
etbs  = processor.process_entities(ans, ents)

text6 = 'CHI 1234567890123456 02 13.08.2013 v2 VC np cl wt4.5 muac5.4'
text7 = 'CHI 1234567890123456 02 13.08.2013 Nv np cl wt4.5 muac5.4'
ans, ents = rmessages.ThouMessage.parse(text6, messageassocs.ASSOCIATIONS, date)
print [ an.data() for an in ans.fields]
print ents
etbs  = processor.process_entities(ans, ents)
ans, ents = rmessages.ThouMessage.parse(text7, messageassocs.ASSOCIATIONS, date)
print [ an.data() for an in ans.fields]
print ents
etbs  = processor.process_entities(ans, ents)


text = 'CHI 1234567890123456 02 13.08.2013 v2 VC np cl wt0.5 muac5.4'
try:	ans, ents = rmessages.ThouMessage.parse(text, messageassocs.ASSOCIATIONS, date)
except rmessages.ThouMsgError, e:	print e.errors

print [ an.data() for an in ans.fields]

text = 'pre 1234567890123456 21.11.2014 05.02.2015 02 01 nr np hp wt55.5 ht145 to nh'
ans, ents = rmessages.ThouMessage.parse(text, messageassocs.ASSOCIATIONS, date)

