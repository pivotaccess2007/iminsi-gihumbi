#!  /usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

import psycopg2
import settings
import re 

conn = psycopg2.connect( host = settings.DBHOST, port = settings.DBPORT, dbname = settings.DBNAME, user = settings.DBUSER, password = settings.DBPASSWORD)

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
 print query_string
 curseur.execute(query_string)
 return curseur

def makecol(s):
  # Remove invalid characters
  s = re.sub('[^0-9a-zA-Z_]', '', s)
  # Remove leading characters until we find a letter or underscore
  s = re.sub('^[^a-zA-Z_]+', '', s)
  return s.lower()

def makedict(x):
 ans = {}
 for y in x: ans[makecol(y[0])] = (y[0], y[1])
 return ans


def build_fields(fields):
 fs = []
 for f in fields:
  for k in f.keys():
   if f[k].__contains__(' '): raise Exception('Invalid Query')
  if 'alias' and 'table' in f.keys(): fs.append("%s.%s AS %s" % (f['table'], f['value'], f['alias']))
  elif 'alias' in f.keys() and 'table' not in f.keys(): fs.append("%s AS %s" % (f['value'], f['alias']))
  elif 'alias' and 'table' not in f.keys(): fs.append("%s" % (f['value']))
  else: fs.append("%s.%s" % (f['table'], f['value']))
 if fs!= []:
  fss = ''.join("%s, " % an for an in fs)
  return fss[0:len(fss)-2]
 return ''

def build_extracts(extracts):
 exs = []
 for ex in extracts:
  if 'alias' in ex.keys(): exs.append("(EXTRACT(%s FROM %s.%s)) AS %s" % (ex['value'], ex['table'], ex['field'], ex['alias']))
  else: exs.append("(EXTRACT(%s FROM %s.%s))" % (ex['value'], ex['table'], ex['field']) )
 if exs!= []:
  exss = ''.join("%s, " % an for an in exs)
  return exss[0:len(exss)-2]
 return ''

def build_inners(primary_table, inner_joins):
 injs = []
 for inj in inner_joins: injs.append("INNER JOIN %s ON (%s.%s = %s.%s)" % (inj['table'], primary_table, inj['outer_field'], inj['table'], inj['field']))
 if injs!= []:
  injss  = ''.join("%s " % an for an in injs)
  return injss 
 return '' 

def build_group_by(group_by):
 if group_by != []:
  gs  = ''.join("%s, " % an for an in group_by)
  return "GROUP BY %s " % gs[0:len(gs)-2]
 return ''

def build_order_by(order_by):
 if order_by != []:
  ors  = ''.join("%s, " % an for an in order_by)
  return "ORDER BY %s " % ors[0:len(ors)-2]
 return ''

def build_tables(tables):
 if tables != []:
  ts  = ''.join("%s, " % an for an in tables)
  return " %s " % ts[0:len(ts)-2]
 return ''

def build_query( fields = [], extracts = [], primary_table = '', tables = [], inner_joins = [], where_clause = '', group_by = [], order_by = []):
  qs = ''
  fields = build_fields(fields)
  extracts = build_extracts(extracts)
  tables = build_tables(tables)
  inner_joins = build_inners(primary_table, inner_joins)
  group_by = build_group_by(group_by)
  order_by = build_order_by(order_by)
  if fields != '' and primary_table != '':
    if extracts != '':
     qs = ' SELECT %s, %s FROM %s %s %s %s %s' % (fields, extracts, primary_table, inner_joins, where_clause, group_by, order_by)
     if tables != '': qs = ' SELECT %s, %s FROM %s, %s %s %s %s %s' % (fields, extracts, primary_table, tables, inner_joins, where_clause, group_by, order_by)
    else:
     qs = ' SELECT %s FROM %s %s %s %s %s' % (fields, primary_table, inner_joins, where_clause, group_by, order_by)
  return qs
  
def summarize_by_location(primary_table = 'pre_table', tables = [], where_clause = [] , 
                                                      MANY_INDICS = [],
                                                      nationwide = True, province = None, district = None, location = None,
                                                      start = None, end = None):

 fields = []
 inner_joins = []
 group_by = []
 wcl = '' 
 #print province, district, location
 if nationwide:
  fields.append( {'value': 'id', 'alias': 'province_id', 'table': 'chws_province'})
  fields.append( {'value': 'name', 'alias': 'province_name', 'table': 'chws_province'} )
  inner_joins.append({'table': 'chws_province', 'field': 'id' , 'outer_field': 'province_pk'})
  group_by.append('chws_province.name')
  group_by.append('chws_province.id')
  if province:
    where_clause.append({'field_name': '%s.province_pk' % primary_table, 'compare': '=', 'value': int(province)})

 if province:
  fields.append( {'value': 'id', 'alias': 'district_id', 'table': 'chws_district'})
  fields.append( {'value': 'name', 'alias': 'district_name', 'table': 'chws_district'} )
  inner_joins.append({'table': 'chws_district', 'field': 'id' ,  'outer_field': 'district_pk'})
  group_by.append('chws_district.name')
  group_by.append('chws_district.id')
  if district:
    where_clause.append({'field_name': '%s.district_pk' % primary_table, 'compare':'=', 'value': int(district)})

 if district:
  fields.append( {'value': 'id', 'alias': 'location_id', 'table': 'chws_healthcentre'})
  fields.append( {'value': 'name', 'alias': 'location_name', 'table': 'chws_healthcentre'} )
  inner_joins.append({'table': 'chws_healthcentre', 'field': 'id' , 'outer_field': 'health_center_pk'})
  group_by.append('chws_healthcentre.name')
  group_by.append('chws_healthcentre.id')
  if location:
    where_clause.append({'field_name': '%s.health_center_pk' % primary_table, 'compare': '=', 'value': int(location)})

 if start:
    where_clause.append({'field_name': '%s.report_date' % primary_table, 'compare': '>=', 'value': "('%s')" % start})
 if end:
    where_clause.append({'field_name': '%s.report_date' % primary_table, 'compare': '<=', 'value': "('%s')" % end})

 if where_clause != []:
  index = 0
  while index < len(where_clause):

    field_name = where_clause[index]['field_name'] 
    if field_name.__contains__(' ') and 'extra' not in where_clause[index].keys(): raise Exception ('Invalid Query')

    if index == 0:
      wcl += " %s %s %s %s " %  ( "WHERE", field_name, where_clause[index]['compare'], where_clause[index]['value'])
    else:
      wcl += " AND %s %s %s " %  ( field_name, where_clause[index]['compare'], where_clause[index]['value'])

    index += 1

 try:
  data = []
  if MANY_INDICS != []:
    for col in MANY_INDICS:
      #print col, len(col)
      qry = build_query( fields = fields + [{'value': 'COUNT(*)', 'alias': '"%s"' % makecol(col[0]) }],
                        extracts = [], primary_table = primary_table, tables = [],
                        inner_joins = inner_joins, where_clause = ' %s %s (%s)' % (wcl, 'AND' if wcl != '' else 'WHERE', col[2] if len(col) == 3 else col[0] ) , 
                        group_by = group_by, order_by = [])#;print qry
      curz = fetch_data_cursor(conn, qry)
      data.append(fetch_data(curz))
  else:
    fields.append( {'value': 'COUNT(*)', 'alias': 'total'} )
    qry = build_query( fields = fields, extracts = [], primary_table = primary_table, tables = [],
                inner_joins = inner_joins, where_clause = wcl if wcl != '' else '', group_by = group_by, order_by = [])#; print qry 
    curz = fetch_data_cursor(conn, qry)
    data = fetch_data(curz)
  return data
 except Exception, e:
  print e;return [] 
 return []

def get_indexed_value(field, table, indexfieldname, indexfield, alias = 'MyName'):
  return "(SELECT %s AS %s FROM %s WHERE %s = %s)" % (field, alias, table, indexfieldname, indexfield)

def give_me_cols(rows):
  cols = []
  data = []
  left_cols = ['province_id', 'province_name', 'district_id', 'district_name', 'location_id', 'location_name', 'total']
  for row in rows:
    row = row.__dict__    
    if row.get('province_id') and 'province_id' not in cols:
      cols.insert(0, 'province_id')
      cols.insert(1, 'province_name')
    if row.get('district_id') and 'district_id' not in cols:
      cols.insert(2, 'district_id')
      cols.insert(3, 'district_name')
    if row.get('location_id') and 'location_id' not in cols:
      cols.insert(4, 'location_id')
      cols.insert(5, 'location_name')
    if row.get('total') and 'total' not in cols:
      cols.insert(6, 'total')
      
    for k in row.keys():
      if k not in left_cols and k not in cols: cols.append(k)
    
    data.append([{ col : row[col]} for col in cols ])
  return [ cols, data ]

def give_me_table(qry_result, MANY_INDICS = [], LOCS = {}):

  indics = [ makecol(x) for x in [y[0] for y in MANY_INDICS] ]
  locs = get_initial_locations(LOCS = LOCS)
  heads = get_heading_cols(HEADERS = indics, LOCS = LOCS)  
  data = get_initial_data(indics_cols = indics, locs = locs)
  #print len(data), data[0]
  index = 0
  
  for qs in qry_result:

    if type(qs) == Record:
      d = give_me_cols(qry_result)
      heads = d[0]
      data = d[1]
      break
    else:
      #print len(qry_result)      
      if index < len(qry_result):        
        d = give_me_cols(qry_result[index])
        cols = d[0]
        rows = d[1]
        
        for row in rows:
          try:
            col = cols[len(cols) - 1]#;print cols
            dt = match_me(data, row, len(cols) - 1 )#;print dt
            for d in dt:
              if d.items()[0][0] == col:  d.update(row[cols.index(col)])
          except IndexError, e:
            continue
        
        index += 1
  
  #print heads, data       
  return {'heads' : heads, 'data' : data}

def match_me(data, row, col_index):
  index = len(data)
  for dt in data:
    if dt[:col_index] == row[:col_index]:
      #print dt, row, col_index
      break
  return dt

## Initialize everything by zero
def get_heading_cols( HEADERS = [], LOCS = {}):
  locs = []
  if LOCS.get('nation') or LOCS.get('nation') is None:  locs += ['province_id', 'province_name']
  if LOCS.get('province'):  locs += ['district_id', 'district_name']
  if LOCS.get('district'):  locs += ['location_id', 'location_name']
  if LOCS.get('location'):
    if 'location_id' not in locs and 'location_name' not in locs: locs += ['location_id', 'location_name']
  cols = locs + HEADERS
  return cols

def get_initial_locations(LOCS = {}):

  ### ONLY RWANDA
  #LOCS.update({'nation': 1})
  qry = "SELECT id AS province_id, name AS province_name FROM chws_province"
  
  if LOCS.get('nation'):
    qry = "SELECT id AS province_id, name AS province_name FROM chws_province WHERE nation_id = %d" % int(LOCS.get('nation'))

  if LOCS.get('province'):
    qry = "SELECT chws_province.id AS province_id, chws_province.name AS province_name, chws_district.id AS district_id \
                    , chws_district.name AS district_name FROM chws_district INNER JOIN chws_province ON (chws_district.province_id = chws_province.id) \
                    WHERE chws_district.province_id = %d" % int(LOCS.get('province'))
  if LOCS.get('district'):
    qry = "SELECT chws_province.id AS province_id, chws_province.name AS province_name, \
                  chws_district.id AS district_id, chws_district.name AS district_name, \
                      chws_healthcentre.id AS location_id, chws_healthcentre.name AS location_name \
                     FROM chws_district INNER JOIN chws_province ON (chws_district.province_id = chws_province.id) \
                      INNER JOIN chws_healthcentre ON (chws_district.id = chws_healthcentre.district_id) \
                    WHERE chws_healthcentre.district_id = %d" % int(LOCS.get('district'))

  if LOCS.get('location'):
    qry = "SELECT chws_province.id AS province_id, chws_province.name AS province_name, \
                  chws_district.id AS district_id, chws_district.name AS district_name, \
                      chws_healthcentre.id AS location_id, chws_healthcentre.name AS location_name \
                     FROM chws_district INNER JOIN chws_province ON (chws_district.province_id = chws_province.id) \
                      INNER JOIN chws_healthcentre ON (chws_district.id = chws_healthcentre.district_id) \
                    WHERE chws_healthcentre.id = %d" % int(LOCS.get('location'))
  if qry != '':
    locs = fetch_data(  fetch_data_cursor( conn, qry ) )
    return locs
  else:
    return []

  return []

def get_initial_data(indics_cols = [], locs = []):
  data = []
  for loc in locs:
    dt = []
    loc = loc.__dict__    
      
    if loc.get('province_id') and loc.get('province_name'):
      dt.insert(0, {'province_id': loc['province_id']})
      dt.insert(1, {'province_name': loc['province_name']})

    if loc.get('district_id') and loc.get('district_name'):
      dt.insert(2, {'district_id': loc['district_id']})
      dt.insert(3, {'district_name': loc['district_name']})

    if loc.get('location_id') and loc.get('location_name'):
      dt.insert(4, {'location_id': loc['location_id']})
      dt.insert(5, {'location_name': loc['location_name']})

    for col in indics_cols: dt.insert( len(dt) + indics_cols.index(col), {col: 0})#; print indics_cols.index(col), col, dt

    data.append(dt) #; print dt 
     
  return data
  
#    for loc in locs:
#      dt = []
#      dt.insert(0, {'province_id': loc.province_id})
#      dt.insert(1, {'province_name': loc.province_name})
#      dt.insert(2, {'district_id': loc.district_id})
#      dt.insert(3, {'district_name': loc.district_name})
#      rows.append(dt)
#    print rows, cols, index
#if LOCS.get('province'):
#cols += ['district_id', 'district_name']
#for loc in locs:
#  rows.insert(2, {'district_id': loc.district_id})
#  rows.insert(3, {'district_name': loc.district_name})
#if LOCS.get('location'):
#cols += ['location_id', 'location_name']
#for loc in locs:
#  rows.insert(4, {'location_id': loc.location_id})
#  rows.insert(5, {'location_name': loc.location_name})
#  return locs


