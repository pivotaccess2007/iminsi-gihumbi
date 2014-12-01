# encoding: UTF-8
import datetime
from ectomorph import orm
import entities
from messages import rmessages
import messageassocs
import migrations
import re, sys, os
from optparse import OptionParser
import psycopg2
import time as times

TREATED = ('treated_messages', migrations.TREATED)
FAILED  = 'failed_transfers'

orm.ORM.connect(dbname = 'thousanddays', user = 'thousanddays', password = 'thousanddays')

def handle_messages(args, options):
  def gun():
    postgres  = psycopg2.connect(
          dbname = 'thousanddays',
            user = 'thousanddays',
        password = 'thousanddays'
    )
    once  = True
    while once:
      once  = single_handle(TREATED, postgres, args, options) and options.get('REPEAT', not once)
    postgres.close()
  if options.get('BACKGROUND'):
    chp = os.fork()
    if chp:
      print 'Background:', chp
      return
    gun()
  else:
    gun()

def single_handle(tbn, pgc, args, options):
  cpt   = int(options.get('NUMBER', 5000))
  force = options.get('FORCE', False)
  qry   = orm.ORM.query(tbn[0], {'NOT deleted':''}, migrations  = tbn[1])
  dsiz  = qry.count()
  seen  = set()
  upds  = []
  deler = options.get('DELETE', False)
  if deler:
    upds  = []
  curs  = pgc.cursor()
  for ix in range(dsiz):
    row   = qry[ix]
    if not row: break
    ixnum = row['oldid']
    act   = 'Loaded'
    if deler:
      try:
        curs.execute('UPDATE messagelog_message SET transferred = TRUE WHERE id = %d' % (ixnum, ))
        orm.ORM.store(tbn[0], {'indexcol': row['indexcol'], 'deleted': True})
      except Exception, e:
        pass
      upds.append(str(row['indexcol']))
    act   = 'Deleted'
    sys.stdout.flush()
    seen.add(str(ixnum))
  curs.close()
  curz    = pgc.cursor()
  delcur  = pgc.cursor()
  gat     = options.get('TYPE', None)
  nar     = 'TRUE'
  if not seen:
    seen.add('0')
  if gat:
    nar = "LOWER(SUBSTR(text, 0, 4)) = '%s'" % (gat.lower(), )
  query = '''
    SELECT
      Message.id,
      Message.contact_id,
      Message.connection_id,
      Message.date,
      Message.text,
      (SELECT province_id FROM chws_reporter Reporter WHERE Reporter.id = Message.contact_id) AS province_pk,
      (SELECT district_id FROM chws_reporter Reporter WHERE Reporter.id = Message.contact_id) AS district_pk,
      (SELECT health_centre_id FROM chws_reporter Reporter WHERE Reporter.id = Message.contact_id) AS health_center_pk,
    FROM
      messagelog_message Message
    WHERE
      (%s) AND (Message.id NOT IN (%s)) AND (NOT Message.transferred)
    ORDER BY
      Message.date
    ASC LIMIT %d''' % (nar, ', '.join(seen), cpt)
  curz.execute(query)
  tot   = curz.rowcount
  if not tot: return False
  cpt   = min(tot, cpt)
  reps  = curz.fetchmany(cpt)
  print ('Already got %d of %d, now moving %d ...' % (len(seen), tot, cpt))
  cpt   = float(cpt)
  pos   = 0
  maxw  = 80
  stbs  = set()
  sttm  = times.time()
  for rep in reps:
    fps   = float(pos + 1)
    pct   = (fps / cpt) * 100.0
    gap   = ' ' * max(0, (int(((fps / cpt) * float(maxw))) - len('100.0%') - len(str(pos + 1)) - 2))
    ctm   = times.time() - sttm
    dlt   = datetime.timedelta(seconds = int(ctm * (cpt / fps)))
    eta   = datetime.datetime.now() + dlt
    pad   = ((' %s ' % (str(dlt), )) + (' ' * maxw))
    org   = rep[4].decode('utf-8')
    succ  = False
    acrow = 0
    try:
      # _ = org.encode('ascii') # Exception trigger. Necessary?
      if not options.get('BACKGROUND'):
        rsp = ('%d %s%3.1f%%%s' % (pos + 1, gap, pct, pad))
        sys.stdout.write('\r' + rsp[0:maxw])
        sys.stdout.flush()
      try:
        ans, ents = rmessages.ThouMessage.parse(org, messageassocs.ASSOCIATIONS, rep[3])
        mname = str(ans.__class__).split('.')[-1].lower()
        succ  = True
        nstbs = store_components(mname, ans, org, rep[0], rep)
        stbs.add(mname)
        stbs  = stbs.union(nstbs)
        etbs  = entities.process_entities(ans, ents)
      except rmessages.ThouMsgError, e:
        store_failures(e, org, rep[0], rep)
      acrow = store_treatment(rep[0], succ, rep)
    except UnicodeEncodeError, e:
      # Is this sufficient?
      store_failures(rmessages.ThouMsgError('Badly-encoded message.', [('bad_encoding', None)]), 'Badly-encoded message #%d' % (rep[0], ), rep[0])
    if deler and force:
      delcur.execute('UPDATE messagelog_message SET transferred = TRUE WHERE id = %d' % (rep[0], ))
      orm.ORM.store(tbn[0], {'indexcol': acrow, 'deleted': True})
    pos = pos + 1
    pgc.commit()
  print 'Done converting ...'
  print 'List of secondary tables:'
  for tbn in stbs:
    print tbn
  curz.close()
  delcur.close()
  pgc.commit()
  return True

def store_components(mname, msg, msgtxt, fid, rep):
  princ = {'oldid': fid, 'message': msgtxt}
  auxil = {}
  loxer = {
    'province_pk': rep[5],
    'district_pk': rep[6],
    'health_center_pk': rep[7]
  }
  seen  = set()
  for k in msg.entries.keys():
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
  for k in auxil.keys():
    val = auxil[k]
    for v in val:
      tst = {'principal': ix, 'value': v}
      tst.update(loxer)
      orm.ORM.store(k, tst)
  return seen

def store_failures(err, msg, fid, rep):
  pos   = 0
  loxer = {
    'province_pk': rep[5],
    'district_pk': rep[6],
    'health_center_pk': rep[7]
  }
  for fc in err.errors:
    fc  = fc[0] if type(fc) == type(('', None)) else fc
    tst = {'oldid': fid, 'message': msg, 'failcode': fc, 'failpos': pos}
    tst.update(loxer)
    orm.ORM.store('failed_transfers', tst)
    pos = pos + 1

def store_treatment(fid, stt, rep):
  tst = {
    'province_pk': rep[5],
    'district_pk': rep[6],
    'health_center_pk': rep[7],
    'oldid': fid,
    'success': stt
  }
  return orm.ORM.store(TREATED[0], tst, migrations = TREATED[1])

def imain(args):
  handle_messages(args, os.environ)
  return 0

sys.exit(imain(sys.argv))
