#!  /usr/bin/env python
# encoding: utf-8
import cherrypy
import copy
from datetime import datetime, timedelta
from ectomorph import orm
from jinja2 import Environment, FileSystemLoader
import json
import migrations
import random
import re
import settings
import queries
import sha
import sys
import urllib2, urlparse
from summarize import *
from mapval import *
from pygrowup import helpers, Calculator
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def child_status(weight = None, height = None, date_of_birth = None, sex = None):
 status = {}
 valid_gender = helpers.get_good_sex( sex )
 valid_age = helpers.date_to_age_in_months(date_of_birth)
 cg = Calculator(adjust_height_data=False, adjust_weight_scores=False)

 try:
  wfa = cg.zscore_for_measurement('wfa', weight, valid_age, valid_gender) if weight and valid_age and valid_gender else None
  if wfa and wfa <= -2: status.update({'underweight': 'UNDERWEIGHT'})
 except Exception, e: pass
 try: 
  hfa = cg.zscore_for_measurement('hfa', height , valid_age, valid_gender) if height and valid_age and valid_gender else None
  if hfa and hfa <= -2: status.update({'stunted': 'STUNTED'})
 except Exception, e: pass
 try:
  wfh = cg.zscore_for_measurement('wfh', weight, valid_age, valid_gender, height) if weight and height and valid_age and valid_gender else None
  if wfh and wfh <= -2: status.update({'wasted': 'WASTED'})
 except Exception, e: pass        

 if status == {}:
  status.update({'normal': 'NORMAL'})
 return status

def register_chw(nid, telephone_moh, health_center, referral, village, cell, sector, surname, given_name, sex, role, edu_level, dob, djoin, language):
 chwhc = orm.ORM.query('chws_healthcentre', {'id = %s': health_center})[0]
 chw = orm.ORM.query('chws_reporter', {'telephone_moh = %s': telephone_moh, 'national_id = %s': nid} )[0]
 
 thing = {'surname': surname, 'given_name': given_name, 'sex': sex, 'language': language, 'national_id':nid, 'telephone_moh': telephone_moh,
		'role_id': role, 'education_level': edu_level, 'date_of_birth': dob, 'join_date': djoin,
		'village_id': village, 'cell_id': cell, 'sector_id': sector,
		'district_id': chwhc['district_id'], 'province_id': chwhc['province_id'], 'nation_id': chwhc['nation_id'],
		'health_centre_id': chwhc['id'], 'referral_hospital_id': referral, 
		'deactivated': False, 'is_active': True, 'correct_registration': True
	}
 #print thing
 if chw is None:
  orm.ORM.store('chws_reporter', thing)
 chw = orm.ORM.query('chws_reporter', {'telephone_moh = %s': telephone_moh, 'national_id = %s': nid, 'health_centre_id = %s': health_center} )[0]
 return chw

def get_display(value):
 if type(value) == bool:
  if value == True: return 'Yes'
  else: return ''
 elif value is None: return ''
 else: return value
 return value

def neat_numbers(num):
  pcs = divided_num(str(num), 3)
  return ', '.join(pcs)

def report_summary(row):
  ans = read_record_row(row, orm)
  return ','.join(an for an in ans)

def first_cap(s):
  if not s: return s
  return ' '.join([x[0].upper() + x[1:] for x in re.split(r'\s+', s)])

def divided_num(num, mx = 3):
  if len(num) < (mx + 1):
    return [num]
  lft = num[0:-3]
  rgt = num[-3:]
  return divided_num(lft) + [rgt]

class ThousandLocation:
  def __init__(self, loc, tp, nav, lmt, ttl, chop  = None):
    self.location   = loc
    self.loctype    = tp
    self.navigator  = nav
    self.title      = ttl
    self.limits     = lmt
    self.chop       = chop

  def __unicode__(self):
    nom = self.location['name']
    return u'%s %s' % (nom if not self.chop else self.chop(nom), self.title)

  @property
  def name(self):
    nom = self.location['name']
    return nom if not self.chop else self.chop(nom)

  def link(self, ref):
    pcs, qrs  = self.navigator.pre_link(self.navigator.link(ref))
    for l in self.limits:
      try:              del qrs[l]
      except KeyError:  pass
    return urlparse.urlunsplit((pcs[0], pcs[1], pcs[2], '&'.join(['%s=%s' % (k, urllib2.quote(qrs[k])) for k in qrs if qrs[k]]), pcs[4]))

class ThousandAuth:
  def __init__(self, usn):
    if not usn:
      raise cherrypy.HTTPRedirect('/')
    self.usern  = usn

  def username(self):
    return self.usern

  def check(self, pwd):
    him = orm.ORM.query('ig_admins', {'address = %s': self.usern})
    if him.count() < 1:
      return False
    him = him[0]
    slt = him['salt']
    shp = sha.sha('%s%s' % (slt, pwd)).hexdigest()
    return shp == him['sha1_pass']

  def conditions(self):
    ans = {}
    him = orm.ORM.query('ig_admins', {'address = %s': self.usern})[0]
    if him['province_pk']:
      ans['province_pk = %s'] = him['province_pk']
    if him['district_pk']:
      ans['district_pk = %s'] = him['district_pk']
    if him['health_center_pk']:
      ans['health_center_pk = %s'] = him['health_center_pk']
    return ans

  def checked_conditions(self, pwd):
    if not self.check(pwd):
      raise Exception, 'Access denied.'
    return self.conditions()

  def him(self):
    return orm.ORM.query('ig_admins', {'address = %s': self.usern})[0]

class ThousandNavigation:
  def __init__(self, auth, *args, **kw):
    self.args   = args
    self.kw     = kw
    self.auth   = auth
    td          = datetime.today()
    self.fin    = datetime(year = td.year, month = td.month, day = td.day)
    self.gap    = timedelta(days = 1000 - 1)

  def pages(self, qry, limit = 100):
    tot, etc  = divmod(qry.count(), limit)
    if etc:
      tot = tot + 1
    cpg = int(self.kw.get('page', '0'))
    crg = cpg * limit
    pgs = xrange(tot)
    return (cpg, (crg, crg + limit), pgs)

  def __unicode__(self):
    them  = self.listing
    them.reverse() 
    #print [unicode(x) for x in them]
    return ', '.join([unicode(x) for x in them])

  @property
  def listing(self):
    dem = [ThousandLocation(self.nation(), 'nation', self, ['province', 'district', 'hc', 'page'], '')]
    pcs = {
      'province':{
        'area'  : lambda _: self.province(),
        'miss'  :['district', 'hc'],
        'title' : 'Province',
        'trx'   : lambda x: first_cap(re.sub(u' PROVINCE', '', x).lower())
      },
      'district':{
        'area'  : lambda _: self.district(),
        'miss'  : ['hc'],
        'title' : 'District'
      },
      'hc':{
        'area'  : lambda _: self.hc(),
        'miss'  : [],
        'title' : 'Health Centre'
      }
    }
    # for pc in ['province', 'district', 'hc']:
    for pc in [(self.has_province(), 'province'),
               (self.has_district(), 'district'),
               (self.has_hc(), 'hc')]:
      # if self.kw.get(pc):
      if pc[0]:
        it  = pcs[pc[1]]
        dem.append(ThousandLocation(it['area'](None), pc[1], self, it['miss'], it['title'], it['trx'] if 'trx' in it else None))
    
    return dem

  @property
  def hierarchy(self):
    prv = self.has_province()
    dst = self.has_district()
    ans = []
    if self.has_district():
      return [{'province': self.province()}, {'district':self.district()}]
    if self.has_province():
      return [{'province': self.province()}]
    return []

  def nation(self):
    gat = orm.ORM.query('chws_nation', {'id = 1':''})[0]
    return gat

  def __has_details(self, prv = None):
    return orm.ORM.query('ig_admins', {'address = %s': self.auth.username()})[0]

  def has_province(self, prv = None):
    num = prv or self.kw.get('province')
    if num:
      return int(num)
    return self.__has_details(prv)['province_pk']

  def province(self, prv = None):
    num = self.has_province(prv)
    gat = orm.ORM.query('chws_province', {'id = %s': num})[0]
    return gat

  def has_district(self, prv = None):
    num = prv or self.kw.get('district')
    if num:
      return int(num)
    return self.__has_details(prv)['district_pk']

  def district(self, dst = None):
    num = self.has_district(dst)
    gat = orm.ORM.query('chws_district', {'id = %s': num})[0]
    return gat

  def has_hc(self, prv = None):
    num = prv or self.kw.get('hc')
    if num:
      return int(num)
    return self.__has_details(prv)['health_center_pk']

  def hc(self, h = None):
    num = self.has_hc(h)
    gat = orm.ORM.query('chws_healthcentre', {'id = %s': num})[0]
    return gat

  @property
  def child(self):
    if self.has_hc():       return ''
    if self.has_district(): return 'hc'
    if self.has_province(): return 'district'
    return 'province'

  @property
  def subarea(self):
    return ['province', 'district', 'hc'][len(self.hierarchy)]

  @property
  def childareas(self):
    if self.has_hc():
      return []
    if self.has_district():
      return self.areas('hc')
    if self.has_province():
      return self.areas('district')
    return self.areas('province')

  def areas(self, level = None):
    tbl, sel, etc = {
      'province'  : lambda _: ('chws_province', [self.province()] if self.has_province() else [], {}),
      'district'  : lambda _: ('chws_district', [self.district()] if self.has_district() else [], {'province_id = %s': self.province()['id']}),
      'hc'        : lambda _: ('chws_healthcentre', [], {'province_id = %s':self.province()['id'], 'district_id = %s':self.district()['id']})
    }[level or self.subarea](None)
    prvq      = orm.ORM.query(tbl, etc,
      cols  = ['*'] + ['id = %d AS selected' % (s['id'], ) for s in sel],
      sort  = ('name', 'DESC')
    )
    return prvq.list()

  def conditions(self, tn, ini = None):
    ans = ini.conditions() if ini else {}
    if tn:
      ans.update({
        (tn + ' >= %s')  : self.start,
        (tn + ' <= %s')  : self.finish
      })
    if 'province' in self.kw:
      ans['province_pk = (SELECT id FROM chws_province WHERE id = %s LIMIT 1)']  = self.kw.get('province') or 0
    if 'district' in self.kw:
      ans['district_pk = (SELECT id FROM chws_district WHERE id = %s LIMIT 1)']  = self.kw.get('district') or 0
    if 'hc' in self.kw:
      ans['health_center_pk = (SELECT id FROM chws_healthcentre WHERE id = %s LIMIT 1)']  = self.kw.get('hc') or 0
    return ans

  @property
  def start(self):
    gat = self.kw.get('start', '')
    if not gat:
      return self.fin - self.gap
    return self.make_time(gat)

  @property
  def finish_date(self):
    return self.text_date(self.finish)

  @property
  def start_date(self):
    return self.text_date(self.start)

  def text_date(self, dt):
    return dt.strftime('%d/%m/%Y')

  @property
  def finish(self):
    gat = self.kw.get('finish', '')
    if not gat:
      return self.fin
    return self.make_time(gat)

  def make_time(self, txt):
    '''dd/mm/yyyy'''
    pcs = [int(x) for x in re.split(r'\D', txt)]
    return datetime(year = pcs[2], month = pcs[1], day = pcs[0])

  def pre_link(self, url):
    pcs = urlparse.urlsplit(url)
    qrs = urlparse.parse_qs(pcs[3])
    qrs.update(self.kw)
    return (pcs, qrs)

  def link(self, url, **kw):
    if not self.kw and not kw:
      return url
    pcs, qrs  = self.pre_link(url)
    miss      = kw.pop('minus', [])
    qrs.update(kw)
    return urlparse.urlunsplit((pcs[0], pcs[1], pcs[2], '&'.join(['%s=%s' % (k, urllib2.quote(str(qrs[k]))) for k in qrs if qrs[k] and (not k in miss)]), pcs[4]))

class Application:
  def __init__(self, templates, statics, static_path, app_data, **kw):
    self.templates    = templates
    self.statics      = statics
    self.static_path  = static_path
    self.kw           = kw
    self.app_data     = app_data
    self.jinja        = Environment(loader = FileSystemLoader(templates))
    self.jinja.filters.update({
      'neat_numbers'  : neat_numbers,
      'get_display'  : get_display,
      'report_summary': report_summary
    })
    self.__set_locations()

  def village(self, pk):
    try:
     num = int(pk) if pk else 0
     gat = orm.ORM.query('chws_village', {'id = %s': num})[0]
     return gat
    except: return None

  def cell(self, pk):
    try:
     num = int(pk) if pk else 0
     gat = orm.ORM.query('chws_cell', {'id = %s': num})[0]
     return gat
    except: return None

  def sector(self, pk):
    try:
     num = int(pk) if pk else 0
     gat = orm.ORM.query('chws_sector', {'id = %s': num})[0]
     return gat
    except: return None

  def sectors(self, pk):
    try:
     num = int(pk) if pk else 0
     gat = orm.ORM.query('chws_sector', {'district_id = %s': num})
     return gat.list()
    except: return []

  def cells(self, pk):
    try:
     num = int(pk) if pk else 0
     gat = orm.ORM.query('chws_cell', {'sector_id = %s': num})
     return gat.list()
    except: return []

  def villages(self, pk):
    try:
     num = int(pk) if pk else 0
     gat = orm.ORM.query('chws_village', {'cell_id = %s': num})
     return gat.list()
    except: return []

  def __set_locations(self):
    self.provinces  = {}
    self.districts  = {}
    self.hcs        = {}
    for prv in orm.ORM.query('chws_province', {}).list():
      self.provinces[str(prv['id'])]  = prv['name']
    for dst in orm.ORM.query('chws_district', {}).list():
      self.districts[str(dst['id'])]  = dst['name']
    for hc in orm.ORM.query('chws_healthcentre', {}).list():
      self.hcs[str(hc['id'])]  = hc['name']

  def match(self, url):
    got = url[1:].replace('/', '_') or 'index'
    sys.stderr.write('%40s:\t%s\n' % (url, got))
    return url[1:].replace('/', '_') or 'index'

  def dynamised(self, chart, mapping = {}, *args, **kw):
    info  = {}
    info.update({
      'ref'           : re.sub(r'_table$', '', chart),
      'locations'     : ['TODO'],
      'args'          : kw,
      'nav'           : mapping.get('navb', None),
      'static_path'   : self.static_path
    })
    info.update(self.app_data)
    info.update(kw)
    mapping.pop('self', None)
    info.update({'display': mapping})
    return self.jinja.get_template('%s.html' % (chart, )).render(*args, **info)

  @cherrypy.expose
  def index(self, *args, **kw):
    flash = cherrypy.session.pop('flash', '')
    user  = cherrypy.session.get('user', '')
    return self.dynamised('index', mapping = locals(), *args, **kw)

##### START OF ALL LOCATIONS FILTERING

  @cherrypy.expose
  def locs(self, *args, **kw):
    import json
    auth  = ThousandAuth(cherrypy.session.get('email'))#;print "DIS: %s" % kw.get('district')
    province = auth.him()['province_pk'] or kw.get('province')
    district = auth.him()['district_pk'] or kw.get('district')
    health_center = auth.him()['health_center_pk'] or kw.get('hc')
    wclause = {}
    if province: wclause = {'province_id = %s' : province}
    if district: wclause = {'district_id = %s' : district}
    if health_center: wclause = {'id = %s' : health_center}
    my_locs = {'hcs': [], 'villages': [], 'hps': [] }; 
    data = orm.ORM.query('chws_healthcentre',  wclause).list()
    hps = orm.ORM.query('chws_hospital',  {'district_id = %s': district } if district else {}).list()
    if district:
	villages = orm.ORM.query('chws_village',  {'district_id = %s' : district}).list()
    	for v in villages:
		#print v['name']
		try:
			cel = orm.ORM.query('chws_cell', {'id = %s' : v['cell_id']})[0]
       			sec = orm.ORM.query('chws_sector', {'id = %s' : v['sector_id']})[0]
			dst = orm.ORM.query('chws_district', {'id = %s' : v['district_id']})[0]
       			prv = orm.ORM.query('chws_province', {'id = %s' : v['province_id']})[0]
			myd = {
							'id': v['id'], 'name': v['name'], 'code': v['code'],
							'cell_name': cel['name'], 'cell_id': cel['id'], 'cell_code': cel['code'],
						 	'sector_name': sec['name'], 'sector_id': sec['id'], 'sector_code': sec['code'],
						 	'district_name': dst['name'], 'district_id': dst['id'], 'district_code': dst['code'],
						 	'province_name': prv['name'], 'province_id': prv['id'], 'province_code': prv['code']
						}
			my_locs['villages'].append( myd )
			#if myd['sector_id'] == 222: print myd
		except Exception,e:	continue

    for d in data:
       #print d['name'], d['district'], d['province']
       dst = orm.ORM.query('chws_district', {'id = %s' : d['district_id']})[0]
       prv = orm.ORM.query('chws_province', {'id = %s' : d['province_id']})[0]
       if prv and dst:	my_locs['hcs'].append( 
			{
				'id': d['id'], 'name': d['name'], 'code': d['code'],
			 	'district_name': dst['name'], 'district_id': dst['id'], 'district_code': dst['code'],
			 	'province_name': prv['name'], 'province_id': prv['id'], 'province_code': prv['code']
			}
		      )

    for h in hps:
       #print d['name'], d['district'], d['province']
       dst = orm.ORM.query('chws_district', {'id = %s' : h['district_id']})[0]
       prv = orm.ORM.query('chws_province', {'id = %s' : h['province_id']})[0]
       if prv and dst:	my_locs['hps'].append( 
			{
				'id': h['id'], 'name': h['name'], 'code': h['code'],
			 	'district_name': dst['name'], 'district_id': dst['id'], 'district_code': dst['code'],
			 	'province_name': prv['name'], 'province_id': prv['id'], 'province_code': prv['code']
			}
		      )

    return json.dumps(my_locs)

##### END OF ALL LOCATIONS FILTERING

  @cherrypy.expose
  def charts(self, *args, **kw):
    return ':-\\'

  @cherrypy.expose
  def dashboards_failures(self, *args, **kw):
    auth  = ThousandAuth(cherrypy.session.get('email'))
    navb  = ThousandNavigation(auth, *args, **kw)
    cnds  = navb.conditions(None, auth)
    cnds.update({'NOT success':''})
    nat = orm.ORM.query('treated_messages', cnds, cols = ['oldid'], migrations = migrations.TREATED)
    cpg, (sttit, endit), pgs = navb.pages(nat)
    msgs  = []
    for tm in nat[sttit:endit]:
      msq = orm.ORM.query('failed_transfers', {'oldid = %s': tm['oldid']}, cols = ['failcode'], sort = ('failpos', True), migrations = migrations.FAILED)
      msg = orm.ORM.query('messagelog_message', {'id = %s': tm['oldid']}, cols = ['text', 'contact_id', 'id'])
      msgs.append({'failures':msq, 'message':msg[0]})
    return self.dynamised('failures', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_messages(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions(None, auth)
    msgs    = orm.ORM.query('treated_messages', cnds,
      cols      = ['COUNT(*) AS total'],
      extended  = {
        'failed':     ('COUNT(*)', 'NOT success'),
        'succeeded':  ('COUNT(*)', 'success')
      },
      migrations = migrations.TREATED
    )
    nat       = msgs[0]
    total     = nat['total']
    succeeded = nat['succeeded']
    failed    = nat['failed']
    succpc    = 0.0
    failpc    = 0.0
    if total:
      succpc  = '%.2f' % ((float(succeeded) / float(total)) * 100.0, )
      failpc  = '%.2f' % ((float(failed) / float(total)) * 100.0, )
    return self.dynamised('messages', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_newborn(self, *args, **kw):
    return self.dynamised('newborn', *args, **kw)

  @cherrypy.expose
  def dashboards_death(self, *args, **kw):
    return self.dynamised('death', *args, **kw)

  NUT_DESCR = [
      # ('weight', 'Weight'),
      # ('height', 'Height'),
      # ('muac', 'MUAC'),
      ('stunting', 'Stunting'),
      ('underweight', 'Underweight'),
      ('wasting', 'Wasting'),
      ('exc_breast', 'Exclusive Breastfeeding'),
      ('comp_breast', 'Complimentary Breastfeeding'),
      ('no_breast', 'Not Breastfeeding')
    ]
  @cherrypy.expose
  def dashboards_nut(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('birth_date', auth)
    attrs   = self.NUT_DESCR
    nat     = self.civilised_fetch('ig_babies_adata', cnds, attrs)
    total   = nat[0]['total']
    adata   = []
    return self.dynamised('nut', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_nutr(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions(None, auth)
    nut = orm.ORM.query('child_track', cnds,
			      cols      = ['COUNT(*) AS allnuts'],
			      extended  = {
				'bf1':('COUNT(*)', " lower(bf1) ='bf1' "),
				'nb':('COUNT(*)', "lower(breastfeeding) = 'nb'"),
				'ebf':('COUNT(*)', "lower(breastfeeding) = 'ebf'"),
				'cbf':('COUNT(*)', "lower(breastfeeding) = 'cbf'"),
				'stunting':('COUNT(*)', 'height_for_age < -2'),
				'underweight':('COUNT(*)', 'weight_for_age < -2'),
				'wasting':('COUNT(*)', 'weight_for_height < -2'),
				'lostweight':('COUNT(*)', 'lostweight IS NOT NULL'),
				'falteringweight':('COUNT(*)', 'falteringweight IS NOT NULL'),
				'gainedweight':('COUNT(*)', 'gainedweight IS NOT NULL'),
			      }
			    )
    # raise Exception, nut.query
    preg_cnds = navb.conditions(None, auth)
    preg_cnds.update({"(lmp + INTERVAL '%s days') >= '%s' " % (settings.GESTATION , datetime.today().date()): ''})
    allpregs = orm.ORM.query(  'rw_pregnancies', 
			  preg_cnds,
                          cols = ['COUNT(*) AS total'],
			)
    nut_pre = orm.ORM.query('mother_track', preg_cnds,
			      cols      = ['COUNT(*) AS allpregs'],
			      extended  = {
				'mother_height_less_145':('COUNT(*)', " mother_height < 145 "),
				'mother_weight_less_50':('COUNT(*)', " mother_weight < 50 "),
				'bmi_less_18_dot_5':('COUNT(*)', " bmi < 18.5 "),
				'lostweight':('COUNT(*)', 'lostweight IS NOT NULL'),
				'falteringweight':('COUNT(*)', 'falteringweight IS NOT NULL'),
				'gainedweight':('COUNT(*)', 'gainedweight IS NOT NULL'),
			      }
    			)
    
    total   = nut[0]['allnuts']
    #print nut_pre.query
    return self.dynamised('nutr', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_nutr(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('child',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('child_number',            'Child Number'),
      ('gender',            'Gender'),
      ('birth_date', 'Date of Birth'),
      ('age_in_months', 'Age'),
      ('reporter_phone',            'Reporter Phone'),
      ('bf1',            'Breastfeeding Within 1 hour'),
       ('breastfeeding',            'Breastfeeding'),
	('child_height',            'Height'),
	('child_weight',            'Weight'),
	('muac',            'MUAC')
      
    ] , *args, **kw)
    DESCRI = []
    wcl    = []
    INDICS = [(key, queries.CBN_DATA[key][1], queries.CBN_DATA[key][0] ) for key in queries.CBN_DATA.keys() ]
    PREG_INDICS = [(key, queries.MOTHER_NUTR[key][1], queries.MOTHER_NUTR[key][0] ) for key in queries.MOTHER_NUTR.keys() ]
    cnds    	= navb.conditions(None, auth)
    preg_cnds 	= navb.conditions(None, auth)
    locateds = tabular = None
    if kw.get('subcat') and (kw.get('subcat') not in [ z[0] for z in PREG_INDICS + [('allpregs', 'Allpregs')] ]):
	cnds.update({'(%s)' % queries.CBN_DATA.get(kw.get('subcat'))[0]: ''})
	wcl += [{'field_name': '%s' % queries.CBN_DATA[kw.get('subcat')][0] if queries.CBN_DATA.get(kw.get('subcat')) else '', 
		'compare': '', 'value': '', 'extra': True }]
    elif kw.get('subcat') and (kw.get('subcat') in [ z[0] for z in PREG_INDICS + [('allpregs', 'Allpregs')]]):
	if kw.get('subcat') != 'allpregs':
	 preg_cnds.update({'(%s)' % queries.MOTHER_NUTR.get(kw.get('subcat'))[0]: ''})
         wcl += [{'field_name': '%s' % queries.MOTHER_NUTR[kw.get('subcat')][0] if queries.MOTHER_NUTR.get(kw.get('subcat')) else '', 
			'compare': '', 'value': '', 'extra': True }]

         wcl.append({'field_name': '(%s)' % "(lmp + INTERVAL '%s days') >= '%s' " % (settings.GESTATION , datetime.today().date()),
                  'compare': '', 'value': '', 'extra': True})
    else: pass

    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      locateds = summarize_by_location(primary_table = 'child_track', MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						start =  navb.start,
						end = navb.finish,
											
						)
      if kw.get('subcat') and (kw.get('subcat') in [ z[0] for z in PREG_INDICS + [('allpregs', 'Allpregs')]]):
       locateds += summarize_by_location(primary_table = 'mother_track', MANY_INDICS = PREG_INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						start =  navb.start,
						end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS+PREG_INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ (x[0].split()[0], x[1]) for x in INDICS + PREG_INDICS])

    markup  = {
      'child': lambda x, _, __: '<a href="/tables/childgrowth?pid=%s">%s</a>' % (x, x),
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'child_weight': lambda x, _, __: '%s' % ( x if x else ''),
      'child_height': lambda x, _, __: '%s' % ( x if x > 0 else ''),
      'muac': lambda x, _, __: '%s' % ( x if x > 0 else ''),
      'breastfeeding': lambda x, _, __: '%s' % (x.upper() if x else 'NB'),
      'bf1': lambda x, _, __: '%s' % (x.upper() if x else 'NB'),
      'birth_date': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'lmp': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    
        
    
    if kw.get('subcat') and (kw.get('subcat') in [ z[0] for z in PREG_INDICS + [('allpregs', 'Allpregs')] ] ):
    	cols    = queries.MOTHER_DATA
    	cols 	+= queries.LOCATION_INFO
    	nat     = orm.ORM.query('mother_track', preg_cnds,
		      cols  = [x[0] for x in cols + [('(lmp + INTERVAL \'%d days\') AS edd' % settings.GESTATION, 'EDDate')] ],
		      
		    );

    else:
    	cols    += queries.LOCATION_INFO  
    	nat     = orm.ORM.query('child_track', cnds,
	      cols  = [x[0] for x in cols + [('(((EXTRACT(DAYS FROM (NOW() - birth_date)) / 30)) :: INTEGER) AS age_in_months', 'Age')] ],
	      
	    ); 
    print nat.query
    desc  = 'Nutrition%s' % (' (%s)' % (
					self.find_descr([ (x[0], x[1]) for x in INDICS+PREG_INDICS], kw.get('subcat')),
												 ) if kw.get('subcat') else '', )
    return self.dynamised('nutr_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_redalert(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    attrs   = self.PREGNANCIES_DESCR
    # nat     = self.civilised_fetch('red_table', cnds, attrs)
    nat     = orm.ORM.query('red_table', cnds)
    # raise Exception, str(nat.query)
    # total   = nat[0]['total']
    fields  = queries.RED_ALERT_FIELDS
    return self.dynamised('redalert', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_pnc(self, *args, **kw):
    return self.dynamised('pnc', *args, **kw)

  @cherrypy.expose
  def dashboards_anc(self, *args, **kw):
    return self.dynamised('anc', *args, **kw)

  @cherrypy.expose
  def dashboards_ccm(self, *args, **kw):
    return self.dynamised('ccm', *args, **kw)

  def locals_for_births(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    pcnds   = copy.copy(cnds)
    pcnds[("lmp + ('%d DAYS' :: INTERVAL)" % (settings.GESTATION, )) + ' <= %s']  = navb.finish
    delivs  = orm.ORM.query('bir_table', cnds,
      extended  = {
        'home'      : ('COUNT(*)', 'ho_bool IS NOT NULL'),
        'clinic'    : ('COUNT(*)', 'cl_bool IS NOT NULL'),
        'hospital'  : ('COUNT(*)', 'hp_bool IS NOT NULL'),
        'allbirs'   : ('COUNT(*)', 'TRUE'),
        'enroute'   : ('COUNT(*)', 'or_bool IS NOT NULL'),
        'boys'      : ('COUNT(*)', 'bo_bool IS NOT NULL AND gi_bool IS NULL'),
        'girls'     : ('COUNT(*)', 'gi_bool IS NOT NULL AND bo_bool IS NULL'),
        'prema'     : ('COUNT(*)', 'pm_bool IS NOT NULL'),
        'bfeed'     : ('COUNT(*)', 'bf1_bool IS NOT NULL'),
        'nbfeed'    : ('COUNT(*)', 'nb_bool IS NOT NULL')
      },
      cols  = ['indangamuntu']  # , 'COUNT(*) AS allbirs']
    )
    congs     = []
    for mum in delivs.list():
      congs.append(mum['indangamuntu'])
    exped   = orm.ORM.query('pre_table', pcnds,
      extended  = {
        # 'alldelivs' : 'COUNT(*)',
        'untracked' : (
          'COUNT(*)', 
            'RANDOM() <= 0.5'
            # 'delivered'
            #'indangamuntu NOT IN %s'
          )
      },
      cols  = ['COUNT(*) AS alldelivs']
    )
    ttl       = orm.ORM.query('anc_table', cnds,
      cols      = ['COUNT(*) AS allancs'],
      extended  = {
        'anc1'    : ('COUNT(*)', 'anc_bool IS NOT NULL'),
        'anc2'    : ('COUNT(*)', 'anc2_bool IS NOT NULL'),
        'anc3'    : ('COUNT(*)', 'anc3_bool IS NOT NULL'),
        'anc4'    : ('COUNT(*)', 'anc4_bool IS NOT NULL')
      }
    )[0]
    ancs      = range(4)
    tous      = ttl['allancs']
    tousf     = float(tous)
    dmax      = float(max([ttl['anc1'], ttl['anc2'], ttl['anc3'], ttl['anc4']]))
    for a in ancs:
      cpt     = ttl['anc%d' % (a + 1, )]
      rpc     = 0.0
      pc      = 0.0
      if tous > 0:
        pc  = 100.0 * (float(cpt) / tous)
      if dmax > 0:
        rpc = 100.0 * (float(cpt) / float(dmax))
      ancs[a] = {'total':cpt, 'pc':pc, 'rpc':rpc}
    expected  = exped[0]['alldelivs']
    births    = delivs[0]['allbirs']
    unknowns  = exped[0]['untracked']
    boys      = delivs[0]['boys']
    girls     = delivs[0]['girls']
    boyspc    = 0.0
    girlspc   = 0.0
    if births > 0:
      boyspc  = (float(boys) / float(births)) * 100.0
      girlspc = (float(girls) / float(births)) * 100.0
    locations = delivs[0]
    plain     = orm.ORM.query('pre_table', pcnds,
      cols  = ['COUNT(*) AS allpregs']
    )
    thinq     = plain.specialise({'mother_weight_float < %s': settings.MIN_WEIGHT})
    fatq      = plain.specialise({'mother_weight_float > %s': settings.MAX_WEIGHT})
    fats      = fatq[0]['allpregs']
    thins     = thinq[0]['allpregs']
    fatpc     = 0.0
    thinpc    = 0.0
    midweight = expected - (fats + thins)
    midpc     = 0.0
    expf      = float(max([midweight, fats, thins]))
    if expf > 0:
      fatpc   = (float(fats) / expf) * 100.0
      thinpc  = (float(thins)  / expf) * 100.0
      midpc   = (float(midweight)  / expf) * 100.0
    return locals()

  @cherrypy.expose
  def dashboards_birthreport(self, *args, **kw):
    return self.dynamised('birthreport', mapping = self.locals_for_births(*args, **kw), *args, **kw)

  @cherrypy.expose
  def dashboards_childhealth(self, *args, **kw):
    return self.dynamised('childhealth', mapping = self.locals_for_births(*args, **kw), *args, **kw)

  @cherrypy.expose
  def dashboards_nbc(self, *args, **kw):
    return self.dynamised('nbc', mapping = self.locals_for_births(*args, **kw), *args, **kw)

  @cherrypy.expose
  def dashboards_delivery(self, *args, **kw):
    return self.dynamised('delivery', mapping = self.locals_for_births(*args, **kw), *args, **kw)

  @cherrypy.expose
  def dashboards_vaccination(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    vacced  = orm.ORM.query('chi_table', cnds,
      cols  = ['COUNT(*) AS allkids'],
      extended  = {
        'v1'      : ('COUNT(*)', 'v1_bool IS NOT NULL'),
        'v2'      : ('COUNT(*)', 'v2_bool IS NOT NULL'),
        'v3'      : ('COUNT(*)', 'v3_bool IS NOT NULL'),
        'v4'      : ('COUNT(*)', 'v4_bool IS NOT NULL'),
        'v5'      : ('COUNT(*)', 'v5_bool IS NOT NULL'),
        'v6'      : ('COUNT(*)', 'v6_bool IS NOT NULL'),
        'fully'   : ('COUNT(*)', 'vc_bool IS NOT NULL'),
        'partly'  : ('COUNT(*)', 'vi_bool IS NOT NULL'),
        'never'   : ('COUNT(*)', 'nv_bool IS NOT NULL')
      }
    )
    fully     = vacced[0]['fully']
    never     = vacced[0]['never']
    partly    = vacced[0]['partly']
    totvacc   = fully + partly
    allkids   = vacced[0]['allkids']
    vaccs     = []
    fullypc   = 0.0
    partlypc  = 0.0
    if totvacc > 0:
      fullypc   = 100.0 * (float(fully) / float(totvacc))
      partlypc  = 100.0 * (float(partly) / float(totvacc))
    if allkids > 0:
      vs    = [vacced[0]['v%d' % (vc + 1)] for vc in range(6)]
      kmax  = max(vs)
      pos   = 0
      prv   = 0
      for it in vs:
        pos       = pos + 1
        fit       = float(it)
        dat       = {'value': it, 'rpc': 100.0 * (float(fit) / float(kmax)), 'pc': 100.0 * (float(fit) / float(allkids))}
        if pos > 1:
          gap         = prv - it
          dat['diff'] = gap
          pc          = 0.0
          if prv > 0:
            pc  = 100.0 * (float(gap) / float(prv))
          dat['dpc']  = pc
        prv = it
        vaccs.append(dat)
    return self.dynamised('vaccination', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_nutrition(self, *args, **kw):
    nut = orm.ORM.query('cbn_table',
      cols      = ['COUNT(*) AS allnuts'],
      extended  = {
        'notbreast':('COUNT(*)', 'nb_bool IS NOT NULL'),
        'breast':('COUNT(*)', 'ebf_bool IS NOT NULL OR cbf_bool IS NOT NULL'),
        'unknown':('COUNT(*)', 'cbf_bool IS NULL AND ebf_bool IS NULL AND nb_bool IS NULL')
      }
    )
    weighed = orm.ORM.query('pre_table', {
      'mother_height_float > 100.0 AND mother_weight_float > 15.0':''
      },
      cols      = ['COUNT(*) AS mums'],
      extended  = {
        'short':('COUNT(*)', 'mother_height_float < 150.0'),
      }
    )
    thins   = weighed.specialise({'(mother_weight_float / ((mother_height_float * mother_height_float) / 10000.0)) < %s': settings.BMI_MIN})
    fats    = weighed.specialise({'(mother_weight_float / ((mother_height_float * mother_height_float) / 10000.0)) > %s': settings.BMI_MAX})
    bir = orm.ORM.query('bir_table',
      cols      = ['COUNT(*) AS allbirs'],
      extended  = {
        'hour1':('COUNT(*)', 'bf1_bool IS NOT NULL')
      }
    )
    return self.dynamised('nutrition', mapping = locals(), *args, **kw)

  def tables_preg_extras(self, dest, *args, **kw):
    navb, cnds, cols    = self.tables_in_general(*args, **kw)
    upds  = {'pregcough':'coughing', 'pregdiarrhea':'diarrhoea', 'pregfever':'fever', 'pregmalaria':'malaria', 'pregvomit':'vomiting', 'pregstill':'stillb', 'pregedema':'oedema', 'pregjaundice':'jaun', 'pregpneumonia':'pneumo', 'pregdisability':'disab', 'preganemia':'anaemia', 'pregcord':'cordi', 'pregneck':'necks', 'preghypothemia':'hypoth'}
    exts  = {queries.PREGNANCY_MATCHES[upds[dest]][1]:''}
    cnds.update(exts)
    nat     = orm.ORM.query('pre_table', cnds,
      cols  = [x[0] for x in cols if x[0][0] != '_'],
    )
    desc    = kw.pop('desc', '')
    return self.dynamised('pregnancy_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_risks(self, *args, **kw):
    navb, cnds, cols    = self.tables_in_general(*args, **kw)
    cnds.update(queries.RISK_MOD)
    nat     = orm.ORM.query('pre_table', cnds,
      cols  = [x[0] for x in cols if x[0][0] != '_'],
    )
    desc = 'High-Risk Mothers'
    return self.dynamised('pregnancy_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_pregcough(self, *args, **kw):
    return self.tables_preg_extras('pregcough', desc = 'Mothers With Cough', *args, **kw)

  @cherrypy.expose
  def tables_pregdiarrhea(self, *args, **kw):
    return self.tables_preg_extras('pregdiarrhea', desc = 'Mothers With Diarrhœa', *args, **kw)

  @cherrypy.expose
  def tables_pregfever(self, *args, **kw):
    return self.tables_preg_extras('pregfever', desc = 'Mothers With a Fever', *args, **kw)

  @cherrypy.expose
  def tables_pregmalaria(self, *args, **kw):
    return self.tables_preg_extras('pregmalaria', desc = 'Mothers With Malaria', *args, **kw)


  @cherrypy.expose
  def tables_pregvomit(self, *args, **kw):
    return self.tables_preg_extras('pregvomit', desc = 'Vomiting Mothers', *args, **kw)

  @cherrypy.expose
  def tables_pregstill(self, *args, **kw):
    return self.tables_preg_extras('pregstill', desc = 'Mothers With Still Births', *args, **kw)

  @cherrypy.expose
  def tables_pregedema(self, *args, **kw):
    return self.tables_preg_extras('pregedema', desc = u'Mothers With Œdema', *args, **kw)

  @cherrypy.expose
  def tables_pregjaundice(self, *args, **kw):
    return self.tables_preg_extras('pregjaundice', desc = 'Mothes With Jaundice', *args, **kw)

  @cherrypy.expose
  def tables_pregpneumonia(self, *args, **kw):
    return self.tables_preg_extras('pregpneumonia', desc = 'Mothers With Pneumonia', *args, **kw)

  @cherrypy.expose
  def tables_preganemia(self, *args, **kw):
    return self.tables_preg_extras('preganemia', desc = u'Mothers With Anæmia', *args, **kw)

  @cherrypy.expose
  def tables_pregdisability(self, *args, **kw):
    return self.tables_preg_extras('pregdisability', desc = 'Mothers With Disabled Children', *args, **kw)

  @cherrypy.expose
  def tables_preghypothemia(self, *args, **kw):
    return self.tables_preg_extras('preghypothemia', desc = 'Cool Mothers', *args, **kw)

  @cherrypy.expose
  def tables_pregcord(self, *args, **kw):
    return self.tables_preg_extras('pregcord', desc = 'Mothers Whose Babies Have Infected Cords', *args, **kw)

  @cherrypy.expose
  def tables_pregneck(self, *args, **kw):
    return self.tables_preg_extras('pregneck', desc = 'Mothers With Neck-Stiffness', *args, **kw)

  @cherrypy.expose
  def tables_delivery(self, *args, **kw):
    navb, cnds, cols    = self.tables_in_general(*args, **kw)
    nat     = orm.ORM.query('bir_table', cnds,
      cols  = [x[0] for x in cols if x[0][0] != '_'],
    )
    desc  = 'Delivery Reports'
    return self.dynamised('delivery_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_pregnancy(self, *args, **kw):
    navb, cnds, cols    = self.tables_in_general(*args, **kw)
    nat     = orm.ORM.query('pre_table', cnds,
      cols  = [x[0] for x in cols if x[0][0] != '_'],
    )
    desc  = 'Pregnancy Reports'
    return self.dynamised('pregnancy_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_pregnancies(self, *args, **kw):
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     wcl = [{'field_name': '%s' % kw.get('subcat'), 'compare': '', 'value': ''}] if kw.get('subcat') else []
     locateds = summarize_by_location(primary_table = 'ig_pregnancies', where_clause = wcl, 
						province = province,
						district = district,
						location = location 
											
						);

    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('report_date',       'Date'),
      ('mother',            'Mother ID'),
    ], *args, **kw)
    sc      = kw.get('subcat')
    markup  = {
      'reporter': lambda x, _, __: '<a href="/tables/reporters?id=%s">%s</a>' % (x, x),
      'indangamuntu': lambda x, _, __: '<a href="/tables/mothers?pid=%s">%s</a>' % (x, x),
      'mother': lambda x, _, __: '<a href="/tables/mothers?id=%s">%s</a>' % (x, x),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), )
    }
    if sc:
      cnds[sc]  = ''
    attrs = self.PREGNANCIES_DESCR
    nat     = orm.ORM.query('ig_pregnancies', cnds,
      cols  = [x[0] for x in (cols + attrs) if x[0][0] != '_'],
    )
    desc  = 'Pregnancies%s' % (' (%s)' % (self.find_descr(self.PREGNANCIES_DESCR, sc), ) if sc else '', )
    return self.dynamised('pregnancies_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_nut(self, *args, **kw):
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
    navb, auth, cnds, cols    = self.neater_tables(sorter = 'birth_date', basics = [
      ('indexcol',          'Entry ID'),
      ('birth_date',        'Birth Date'),
      ('height',            'Height'),
      ('weight',            'Weight'),
      ('baby',              'Baby ID'),
      ('muac',              'MUAC')
    ], *args, **kw)
    sc      = kw.get('subcat')
    markup  = {
      'reporter': lambda x, _, __: '<a href="/tables/reporters?id=%s">%s</a>' % (x, x),
      'baby': lambda x, _, __: '<a href="/tables/child?id=%s">%s</a>' % (x, x),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), )
    }
    if sc:
      cnds[sc]  = ''
    attrs   = self.NUT_DESCR
    nat     = orm.ORM.query('ig_babies_adata', cnds,
      cols  = [x[0] for x in (cols + attrs) if x[0][0] != '_'],
    )
    desc  = 'Nutrition%s' % (' (%s)' % (self.find_descr(self.NUT_DESCR, sc), ) if sc else '', )
    return self.dynamised('babies_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_babies(self, *args, **kw):
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     wcl = [{'field_name': '%s' % kw.get('subcat'), 'compare': '', 'value': ''}] if kw.get('subcat') else []
     locateds = summarize_by_location(primary_table = 'ig_babies', where_clause = wcl, 
						province = province,
						district = district,
						location = location 
											
						);
    navb, auth, cnds, cols    = self.neater_tables(sorter = 'birth_date', basics = [
      ('indexcol',          'Entry ID'),
      ('birth_date',        'Birth Date'),
      ('height',            'Height'),
      ('weight',            'Weight'),
      ('cnumber',           'Child Number'),
      ('pregnancy',         'Pregnancy ID')
    ], *args, **kw)
    sc      = kw.get('subcat')
    markup  = {
      'reporter': lambda x, _, __: '<a href="/tables/reporters?id=%s">%s</a>' % (x, x),
      'indangamuntu': lambda x, _, __: '<a href="/tables/mothers?pid=%s">%s</a>' % (x, x),
      'pregnancy': lambda x, _, __: '<a href="/tables/pregnancies?id=%s">%s</a>' % (x, x),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), )
    }
    if sc:
      cnds[sc]  = ''
    attrs   = self.BABIES_DESCR
    nat     = orm.ORM.query('ig_babies', cnds,
      cols  = [x[0] for x in (cols + attrs) if x[0][0] != '_'],
    )
    desc  = 'Babies%s' % (' (%s)' % (self.find_descr(self.BABIES_DESCR, sc), ) if sc else '', )
    return self.dynamised('babies_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_mothers(self, *args, **kw):
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     wcl = [{'field_name': '%s' % kw.get('subcat'), 'compare': '', 'value': ''}] if kw.get('subcat') else []
     locateds = summarize_by_location(primary_table = 'ig_mothers', where_clause = wcl, 
						province = province,
						district = district,
						location = location 
											
						);

    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('report_date',       'Date'),
      ('indangamuntu',        'Patient ID'),
      ('reporter',          'Reporter ID'),
      ('height',            'Height'),
      ('weight',            'Weight'),
      # ('reporter',          'Reporter ID'),
      ('pregnancies',       'Pregnancies')
    ], *args, **kw)
    sc      = kw.get('subcat')
    markup  = {
      'reporter': lambda x, _, __: '<a href="/tables/reporters?id=%s">%s</a>' % (x, x),
      'indangamuntu': lambda x, _, __: '<a href="/tables/mothers?pid=%s">%s</a>' % (x, x),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), )
    }
    if sc:
      cnds[{'withprev':'pregnancies > 1'}.get(sc, sc)]  = ''
    attrs   = self.MOTHERS_DESCR
    nat     = orm.ORM.query('ig_mothers', cnds,
      cols  = [x[0] for x in (cols + attrs) if x[0][0] != '_'],
    )
    #raise Exception, nat.query
    desc  = 'Mothers%s' % (' (%s)' % (self.find_descr(self.MOTHERS_DESCR, sc), ) if sc else '', )
    return self.dynamised('mothers_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_reports(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('report_date',       'Date'),
      ('reporter_pk',       'Reporter ID'),
      ('reporter_phone',    'Reporter Phone'),
      ('report_type',       'Report Type')
    ], *args, **kw)
    desc    = 'Reports'
    sc      = kw.get('subcat')
    markup  = {}
    if sc:
      cnds.update({'report_type = %s': sc})
      desc  = '%s (%s Reports)' % (desc, sc)
    nat     = orm.ORM.query('thousanddays_reports', cnds,
      cols  = [x[0] for x in cols if x[0][0] != '_'],
      sort  = ('report_date', False)
    )
    return self.dynamised('reports_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_reporters(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(
      sorter  = None,
      basics  = [
        ('indexcol',          'Entry ID'),
        ('phone_number',      'Phone Number'),
        ('province_pk',       'Date'),
        ('district_pk',       'District')
        # ('health_center_pk',  'Health Centre')
      ], *args, **kw)
    markup  = {
      'indexcol': lambda x, _, __: '<a href="/tables/reporters?id=%s">%s</a>' % (x, x),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), )
    }
    nat     = orm.ORM.query('ig_reporters', cnds,
      cols  = [x[0] for x in cols if x[0][0] != '_'],
      sort  = ('created_at', False)
    )
    desc  = 'Reports'
    return self.dynamised('reporter_table', mapping = locals(), *args, **kw)

  def find_descr(self, desc, key):
    for k, d in desc:
      if k == key: return d
    return None

  def neater_tables(self, sorter = 'report_date', basics = [], extras = [], *args, **kw):
    return self.tables_in_general(sorter, basics, extras, *args, **kw)

  def tables_in_general(self, sorter = 'report_date', basics = [
      ('indexcol',          'Report ID'),
      ('report_date',       'Date'),
      ('reporter_phone',    'Reporter'),
      ('reporter_pk',       'Reporter ID')
    ], extras = [
      ('indangamuntu',        'Mother ID'),
      ('lmp',               'LMP')
    ], *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = {}
    pid     = kw.get('pid')
    tid     = kw.get( 'id')
    if pid:
      cnds  = {'indangamuntu = %s': pid}
    elif tid:
      cnds  = {'indexcol  = %s':  tid}
    else:
      cnds  = navb.conditions(sorter, auth)
    cols  = (basics + (([] if 'province' in kw else [('province_pk',       'Province')]) +
     ([] if 'district' in kw else [('district_pk',       'District')]) +
     ([] if 'hc' in kw else [('health_center_pk',  'Health Centre')])) + extras)
    return (navb, auth, cnds, cols)

  @cherrypy.expose
  def dashboards_home(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    return self.dynamised('home', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def authentication(self, *args, **kw):
    eml                       = kw.get('addr')
    pwd                       = kw.get('pwd')
    auth                      = ThousandAuth(eml)
    cherrypy.session['user']  = eml
    if kw.get('logout'):
      cherrypy.session.pop('email', '')
      raise cherrypy.HTTPRedirect('/')
    if auth.check(pwd):
      cherrypy.session['email'] = eml
    else:
      cherrypy.session['flash'] = 'Access Denied'
      raise cherrypy.HTTPRedirect('/')
    if kw.get('next'):
      raise cherrypy.HTTPRedirect(kw.get('next'))
    raise cherrypy.HTTPRedirect(settings.AUTH_HOME)

  EXPORT_MIGS = [
    ('total', 0),
    ('sofar', 0)
  ]
  # TODO:
  # 1.  Data type specification
  # 2.  DB-validated tracking of current position
  @cherrypy.expose
  def exports_general(self, *args, **kw):
    auth      = ThousandAuth(cherrypy.session.get('email'))
    navb      = ThousandNavigation(auth, *args, **kw)
    tbl, srt  = settings.EXPORT_KEYS.get(kw.get('key', '_'))
    cnds  = navb.conditions(srt or 'report_date', auth)
    btc   = 5000
    pos   = int(kw.get('pos', '0'))
    eid   = kw.get('eid')
    tot   = 0
    beg   = False;print tbl
    if not eid:
      toq = orm.ORM.query(tbl, cnds, cols = ['COUNT(*) AS total'])#;print toq.query
      tot = toq[0]['total']
      eid = orm.ORM.store('exports_table', {'total': tot, 'sofar': 0})
      beg = True
    else:
      eid = int(eid)
      toq = orm.ORM.query('exports_table', {'indexcol = %s': eid})
      tot = toq[0]['total']
    pgs, rmd  = divmod(tot, btc)
    pgs       = pgs + (1 if rmd else rmd)
    dst       = 'frontend/static/downloads/%d.xls' % (eid, )
    stt       = pos * btc
    if pos > pgs:
      with open(dst, 'a') as fch:
        fch.write('E\n')
      # cherrypy.response.headers['Content-Type']         = 'application/vnd.ms-excel; charset=UTF-8'
      # cherrypy.response.headers['Content-Disposition']  = 'attachment; filename=download-%d.xls' % (eid, )
      raise cherrypy.HTTPRedirect('/static/downloads/%d.xls' % (eid, ))
    with open(dst, 'a') as fch:
      nat = orm.ORM.query(tbl, cnds, sort = ('indexcol', True))
      nat[0]
      if beg:
        fch.write('ID;P\n')
        stt = stt + 1
        xps = 0
        for hd in nat.cursor.description:
          xps = xps + 1
          fch.write('C;Y%d;X%d;K%s\n' % (stt, xps, json.dumps(hd.name)))
        pass
      rng = pos * btc
      for row in nat[rng : rng + btc]:
        stt = stt + 1
        xps = 0
        for hd in nat.cursor.description:
          xps = xps + 1
          fch.write('C;Y%d;X%d;K%s\n' % (stt, xps, json.dumps(str(row[hd.name]))))
    # raise cherrypy.HTTPRedirect('/exports/general?pos=%d&eid=%d' % (pos + 1, eid))
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.headers['Location']     = '/exports/general?lmt=%d&pos=%d&eid=%d' % (pgs, pos + 1, eid)
    cherrypy.response.status                  = 303
    return json.dumps({'total': tot, 'id': eid, 'pos': pos + 1, 'limit': pgs})

  @cherrypy.expose
  def exports_delivery(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    nat     = orm.ORM.query('bir_table', cnds)
    nat[0]
    raise Exception, str(nat.cursor.description)
    raise Exception, str(nat.cols)
    raise Exception, str(nat.query)

  @cherrypy.expose
  def dashboards_reporting(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions(None, auth)
    nat     = orm.ORM.query('ig_reporters', cnds, cols = ['COUNT(*) AS total'])
    total   = nat[0]['total']
    rps     = orm.ORM.query('thousanddays_reports', cnds, cols = ['COUNT(*) AS total'])
    reptot  = rps[0]['total']
    ncnds   = copy.copy(cnds)
    ncnds.update({'report_type IS NOT NULL':''})
    rpts    = orm.ORM.query('thousanddays_reports', ncnds, cols = ['DISTINCT report_type', "(report_type || ' Reports') AS nom"], sort = ('report_type', True)).list()
    return self.dynamised('reporting', mapping = locals(), *args, **kw)

  PREGNANCIES_DESCR = [
      # ('soon', 'Clinic'),
      # ('at_clinic', 'Confirmed at Clinic'),
      # ('at_home', 'Confirmed at Home'),
      # ('at_hospital', 'Confirmed at Hospital'),
      # ('en_route', 'Confirmed en route'),
      ('no_problem', 'Pregnancy Without Risk'),
      ('no_prev_risks', 'No Previous Risks'),
      ('rapid_breathing', 'Rapid Breathing'),
      ('multiples', 'Multiples'),
      ('young_mother', 'Young Mother'),
      ('asm_advice', 'ASM Advice Given'),
      ('malaria', 'With Malaria'),
      ('vomiting', 'Vomiting'),
      ('coughing', 'Coughing'),
      ('referred', 'Referred'),
      ('diarrhoea', u'With Diarrhœa'),
      ('oedema', u'With Œdema'),
      ('fever', 'With Fever'),
      ('stiff_neck', 'With Stiff Neck'),
      ('jaundice', 'With Jaundice'),
      ('pneumonia', 'With Pneumonia'),
      ('hypothermia', 'With Hypothermia'),
      ('previous_serious_case', 'With History of Serious Cases'),
      ('severe_anaemia', u'With Severe Anæmia'),
      ('previous_haemorrhage', u'With History of Hæmorrhage'),
      ('mother_sick', 'With Unspecifed Sickness'),
      ('previous_convulsion', 'With History of Convulsions'),
    ]
  @cherrypy.expose
  def dashboards_pregnancies(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    attrs   = self.PREGNANCIES_DESCR
    nat     = self.civilised_fetch('ig_pregnancies', cnds, attrs)
    total   = nat[0]['total']
    return self.dynamised('pregnancies', mapping = locals(), *args, **kw)

##### START OF NEW UZD #####
  #### START OF PREGNANCY ###
  @cherrypy.expose
  def dashboards_predash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) : ''})
    #cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.finish) : ''})

    exts = {}
    total = orm.ORM.query(  'rw_pregnancies', 
			  cnds,
                          cols = ['COUNT(*) AS total'],
			)[0]['total']
    if kw.get('group') == 'no_risk':
      title = 'No Risk'
      group = 'no_risk'
      cnds.update({queries.NO_RISK['query_str']: ''})
      nat = orm.ORM.query(  'rw_pregnancies', 
			  cnds,
                          cols = ['COUNT(*) AS total'],
			)
    elif kw.get('group') == 'at_risk':
      title = 'At Risk'
      group = 'at_risk'
      cnds.update({queries.RISK['query_str']: ''})
      attrs = [(makecol(x[0]), x[1]) for x in queries.RISK['attrs']]
      exts.update(dict([( makecol(x[0]), ('COUNT(*)',x[0]) ) for x in queries.RISK['attrs'] ]))
      nat = orm.ORM.query(  'rw_pregnancies', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts,
			)
    elif kw.get('group') == 'high_risk':
      title = 'High Risk'
      group = 'high_risk'
      cnds.update({queries.HIGH_RISK['query_str']: ''})
      attrs = [( makecol(x[0]), x[1]) for x in queries.HIGH_RISK['attrs'] ]
      exts.update(dict([( makecol(x[0]), ('COUNT(*)',x[0]) ) for x in queries.HIGH_RISK['attrs'] ]))
      nat = orm.ORM.query(  'rw_pregnancies', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts,
			)
    else:
      nat = orm.ORM.query(  'rw_pregnancies', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = {'no_risk': ('COUNT(*)', queries.NO_RISK['query_str']), 
					'at_risk': ('COUNT(*)', queries.RISK['query_str']),
					'high_risk': ('COUNT(*)', queries.HIGH_RISK['query_str']),
					}
			)
    return self.dynamised('predash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_predash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      
    ] + queries.PREGNANCY_DATA , *args, **kw)
    DESCRI = []

    HIGHRISKDICT = makedict(queries.HIGH_RISK['attrs'])
    RISKDICT = makedict(queries.RISK['attrs'])
    INDICS = []
    wcl = []

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) : ''})
    #cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.finish) : ''})
    
    if kw.get('subcat'):
     if kw.get('group'):
      if kw.get('group') == 'no_risk':
       cnds.update({'(%s)' % queries.NO_RISK['query_str']: ''})
      else:
       if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.HIGH_RISK['attrs']]:
        cnds.update({queries.HIGH_RISK['query_str']: ''})
        cnds.update({ HIGHRISKDICT[kw.get('subcat')][0] : ''})
        INDICS = [HIGHRISKDICT[kw.get('subcat')]] 
       if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.RISK['attrs']]:
        cnds.update({queries.RISK['query_str']: ''})
        cnds.update({ RISKDICT[kw.get('subcat')][0] : ''})
        INDICS = [RISKDICT[kw.get('subcat')]]

  
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = RISKDICT if kw.get('subcat') in [x[0] for x in queries.RISK['attrs']] else  HIGHRISKDICT
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []
     if kw.get('subcat') is None:
      if kw.get('group') == 'no_risk':
       wcl.append({'field_name': '(%s)' % queries.NO_RISK['query_str'], 'compare': '', 'value': '', 'extra': True})
       INDICS = []
      if kw.get('group') == 'at_risk':
       wcl.append({'field_name': '(%s)' % queries.RISK['query_str'], 'compare': '', 'value': '', 'extra': True})
       INDICS = [RISKDICT[key] for key in RISKDICT.keys()]
      if kw.get('group') == 'high_risk':
       wcl.append({'field_name': '(%s)' % queries.HIGH_RISK['query_str'], 'compare': '', 'value': '', 'extra': True})
       INDICS = [HIGHRISKDICT[key] for key in HIGHRISKDICT.keys()]
      if kw.get('group') is None:
       INDICS = [('no_risk', 'No Risk', '(%s)' % queries.NO_RISK['query_str'] ), 
		('at_risk', 'At Risk', '(%s)' % queries.RISK['query_str']),
		 ('high_risk', 'High Risk', '(%s)' % queries.HIGH_RISK['query_str']),
		]#; print INDICS

     wcl.append({'field_name': '(%s)' % ("(report_date) <= '%s'" % ( navb.finish) ), 'compare': '', 'value': '', 'extra': True})
     wcl.append({'field_name': '(%s)' % ("(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) ), 'compare': '', 'value': '', 'extra': True})
     
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      #print INDICS
      locateds = summarize_by_location(primary_table = 'rw_pregnancies', MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						#start =  navb.start,
						#end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ ( makecol(x[0]), x[1]) for x in INDICS])

    sc      = kw.get('subcat')
    
    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'gravidity': lambda x, _, __: '%s' % (int(x) if x else ''),
      'parity': lambda x, _, __: '%s' % (int(x) if x else ''),
      'lmp': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'edd': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    
    
    if kw.get('group') == 'no_risk':
     cnds.update({'(%s)' % queries.NO_RISK['query_str']: ''})
     DESCRI.append(('no_risk', 'No Risk'))
    if kw.get('group') == 'at_risk':
     cnds.update({'(%s)' % queries.RISK['query_str']: ''})
     DESCRI.append(('at_risk', 'At Risk'))
    if kw.get('group') == 'high_risk':
     cnds.update({'(%s)' % queries.HIGH_RISK['query_str']: ''})
     DESCRI.append(('high_risk', 'High Risk'))

    cols    += queries.LOCATION_INFO   
    nat     = orm.ORM.query('rw_pregnancies', cnds,
      cols  = [x[0] for x in (cols + [
					('(lmp + INTERVAL \'%d days\') AS edd' % settings.GESTATION, 'EDDate'),
					('(%s) AS at_risky' % queries.RISK['query_str'], 'AtRisky'), 
					('(%s) AS high_risky' % queries.HIGH_RISK['query_str'], 'HighRisky'),
 
					] ) if x[0][0] != '_'],
      
    )
    desc  = 'Pregnancies%s' % (' (%s)' % (self.find_descr(DESCRI + [(makecol(x[0]), x[1]) for x in INDICS], sc or kw.get('group')), 
					) if sc or kw.get('group') else '', )
    return self.dynamised('predash_table', mapping = locals(), *args, **kw)

  ### END OF PREGNANCY ####

  ### START OF ANC ###

  @cherrypy.expose
  def dashboards_ancdash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
    pre_cnds    = navb.conditions(None, auth)
    pre_cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    pre_cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) : ''})

    exts = {}
    attrs = [(makecol(x[0]), x[1]) for x in queries.ANC_DATA['attrs'] ]

    pre = orm.ORM.query(  'rw_pregnancies', 
			  pre_cnds, 
			  cols = ['COUNT(*) AS total']
			)

    cnds    = navb.conditions(None, auth)
    cnds.update({queries.ANC_DATA['query_str']: ''})
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    #cnds.update({"(anc_date + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION - settings.ANC_GAP, navb.start) : ''})
    #print cnds
    exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.ANC_DATA['attrs'] ])) 
    nat = orm.ORM.query(  'rw_ancvisits', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts
			)#;print nat.query
    return self.dynamised('ancdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_ancdash(self, *args, **kw):
    navb, auth, cnds, cols   = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      
    ] , *args, **kw)
    DESCRI = []
    ANCDICT = makedict(queries.ANC_DATA['attrs'])
    INDICS = [ANCDICT[key] for key in ANCDICT.keys()]
    wcl = []

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
    cnds    = navb.conditions(None, auth)
    cnds.update({queries.ANC_DATA['query_str']: ''})
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    #cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION - settings.ANC_GAP, navb.start) : ''})
    primary_table = 'rw_ancvisits'

    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.ANC_DATA['attrs']]:
     cnds.update({queries.ANC_DATA['query_str']: ''})
     cnds.update({ ANCDICT[kw.get('subcat')][0] : ''})
     INDICS = [ANCDICT[kw.get('subcat')]]
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = ANCDICT if kw.get('subcat') in [x[0] for x in queries.ANC_DATA['attrs']] else  {}
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []
     
     if kw.get('group') == 'anc1':
      primary_table = 'rw_pregnancies'
      wcl.append({'field_name': '(%s)' % ("(report_date) <= '%s'" % ( navb.finish) ), 'compare': '', 'value': '', 'extra': True})
      wcl.append({'field_name': '(%s)' % ("(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) ), 'compare': '', 'value': '', 'extra': True})
      INDICS = [('no_risk', 'No Risk', '(%s)' % queries.NO_RISK['query_str'] ), 
		('at_risk', 'At Risk', '(%s)' % queries.RISK['query_str']),
		 ('high_risk', 'High Risk', '(%s)' % queries.HIGH_RISK['query_str']),
		]
     else: 
      wcl.append({'field_name': '(%s)' % ("(report_date) <= '%s'" % ( navb.finish) ), 'compare': '', 'value': '', 'extra': True})
      wcl.append({'field_name': '(%s)' % ("(anc_date + INTERVAL \'%d days\') >= '%s'" % (
							settings.GESTATION - settings.ANC_GAP, navb.start) ), 'compare': '', 'value': '', 'extra': True})
      wcl.append({'field_name': '(%s)' % queries.ANC_DATA['query_str'], 'compare': '', 'value': '', 'extra': True})
      
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      #print INDICS
      locateds = summarize_by_location(primary_table = primary_table, MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						#start =  navb.start,
						#end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ (makecol(x[0]), x[1]) for x in INDICS])

    sc      = kw.get('subcat')

    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }

    preg_cnds = navb.conditions(None, auth)

    if sc:
      cnds.update({"(anc_date + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION - settings.ANC_GAP, navb.start) : ''})
      cnds[ANCDICT[sc][0]] = ''
      ancs     = orm.ORM.query( 'rw_ancvisits' , cnds, cols = ['pregnancy_id'])
      pregs = [an['pregnancy_id'] for an in ancs.list()]#;print pregs
      if len(pregs) > 1: preg_cnds.update({'indexcol IN %s' % str(tuple(pregs))  : ''})
      if len(pregs) == 1: preg_cnds.update({'indexcol = %s' % str(pregs[0])  : ''})   
    # TODO: optimise
    #attrs = queries.ANC_DATA['attrs']
    #print cnds
    cols    += queries.LOCATION_INFO
     
    

    if kw.get('group') == 'anc1':
     navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
     preg_cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
     preg_cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) : ''})
     primary_table = 'rw_pregnancies'
     attrs = [('(%s) AS at_risky' % queries.RISK['query_str'], 'AtRisky'),]
     DESCRI.append(('anc1', 'Pregnancy')) 

    #print cnds  
    nat     = orm.ORM.query( 'rw_pregnancies' , preg_cnds,
      cols  = [x[0] for x in (cols + [
					('(lmp + INTERVAL \'%d days\') AS edd' % settings.GESTATION, 'EDDate'),
					('(%s) AS high_risky' % queries.HIGH_RISK['query_str'], 'HighRisky'),
 
					]) if x[0][0] != '_'],
      
    )#;print nat.query
    desc  = 'ANC%s' % (' (%s)' % (self.find_descr(DESCRI + [(makecol(x[0]), x[1]) for x in INDICS], kw.get('subcat')),
									) if kw.get('subcat') else 'ALL', )
    return self.dynamised('ancdash_table', mapping = locals(), *args, **kw)

  ### END OF ANC ###

  #### START OF RED ALERT ###
  @cherrypy.expose
  def dashboards_reddash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions('report_date', auth)
    exts = {}
    
    red_attrs = [(makecol(x[0]), x[1]) for x in queries.RED_DATA['attrs']]
    red_exts = exts
    red_cnds = cnds
    red_cnds.update({queries.RED_DATA['query_str']: ''})
    #red_cnds.update({ 'emergency_date IS NULL AND intervention_field IS NULL': ''})
    red_exts.update(dict([(makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.RED_DATA['attrs']]))
    red = orm.ORM.query(  'rw_redalerts', 
			  red_cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = red_exts,
			)#;print red.query

    rar_attrs = [(makecol(x[0]), x[1]) for x in queries.RAR_DATA['attrs']]
    rar_cnds = navb.conditions('report_date')
    rar_cnds.update({queries.RAR_DATA['query_str']: ''})
    #rar_cnds.update({ 'emergency_date IS NOT NULL AND intervention_field IS NOT NULL': ''})
    rar_exts = dict([(makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.RAR_DATA['attrs']])
    rar = orm.ORM.query(  'rw_redalerts', 
			  rar_cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = rar_exts,
			)#;print rar.query

    return self.dynamised('reddash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_reddash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      
    ] , *args, **kw)
    DESCRI = []
    REDDICT = makedict(queries.RED_DATA['attrs'])
    RARDICT = makedict(queries.RAR_DATA['attrs'])
    INDICS = [ REDDICT[key] for key in REDDICT.keys() ] +  [ RARDICT[key] for key in RARDICT.keys() ]
    wcl = []
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) >= '%s'" % (navb.start) : ''})
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    primary_table = 'rw_redalerts'
  
    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.RAR_DATA['attrs']]:
     cnds.update({queries.RAR_DATA['query_str']: ''})
     cnds.update({ RARDICT[kw.get('subcat')][0] : ''})
     INDICS = [RARDICT[kw.get('subcat')]] 
    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.RED_DATA['attrs']]:
     DATADICT = makedict(queries.RED_DATA['attrs'])
     cnds.update({queries.RED_DATA['query_str']: ''})
     cnds.update({ REDDICT[kw.get('subcat')][0] : ''})
     INDICS = [REDDICT[kw.get('subcat')]] 
    #print cnds,INDICS 
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = RARDICT if kw.get('subcat') in [x[0] for x in queries.RAR_DATA['attrs']] else  REDDICT
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []

     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      locateds = summarize_by_location(primary_table = primary_table, MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						start =  navb.start,
						end = navb.finish,
											
						)
      
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ ( makecol(x[0]), x[1]) for x in INDICS ])#;print INDICS_HEADERS,tabular

    sc      = kw.get('subcat')
    
    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'wt_float': lambda x, _, __: '%s' % (int(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    
    # TODO: optimise
    attrs = []
    
    cols    += queries.LOCATION_INFO   
    nat     = orm.ORM.query(primary_table, cnds,
      cols  = [x[0] for x in (cols + attrs) if x[0][0] != '_'],
      
    )#;print nat.query
    desc  = 'Red Alerts %s' % (' (%s)' % (self.find_descr(DESCRI + [(makecol(x[0]), x[1]) for x in INDICS], 
						sc) or 'ALL', 
					) )
    return self.dynamised('reddash_table', mapping = locals(), *args, **kw)


  #### END OF RED ALERT ###

  #### START OF DELIVERY ###

  @cherrypy.expose
  def dashboards_deliverynotdash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    exts = {}
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    pre_cnds    = navb.conditions(None, auth)
    pre_cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    pre_cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) : ''})
    pre = orm.ORM.query(  'rw_pregnancies', 
			  pre_cnds, 
			  cols = ['COUNT(*) AS total']
			)
    
    today = navb.start#datetime.today().date()
    next_monday = today + timedelta(days=-today.weekday(), weeks=1)
    next_sunday = next_monday + timedelta(days = 6)
    next_two_monday = today + timedelta(days=-today.weekday(), weeks=2)
    next_two_sunday = next_two_monday + timedelta(days = 6)

    attrs = [
	('next_week', 'Deliveries in Next Week', "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_monday, next_sunday)),
	('next_two_week', 'Deliveries in Next two Weeks', "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_two_monday, next_two_sunday)),
	]
    exts.update(dict([(x[0], ('COUNT(*)',x[2])) for x in attrs]))
    nat = orm.ORM.query(  'rw_pregnancies', 
    			  cnds, 
    			  cols = ['COUNT(*) AS total'],
                          extended = exts, 
    			)#; print nat.query

    details = {}
    for attr in attrs:
     attr_cnds = navb.conditions(None, auth)
     attr_cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
     attr_cnds.update({attr[2]: ''})
     #print attr_cnds
     details.update({ 
			attr[0] :
			orm.ORM.query(  'rw_pregnancies', 
			  attr_cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = {'no_risk': ('COUNT(*)', queries.NO_RISK['query_str']), 
					'at_risk': ('COUNT(*)', queries.RISK['query_str']),
					'high_risk': ('COUNT(*)', queries.HIGH_RISK['query_str']),
					}
			) 
		   })
    

    return self.dynamised('deliverynotdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_deliverynotdash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      ('lmp',            'LMP'),
      
    ] , *args, **kw)

    today = navb.start#;print cnds#datetime.today().date()
    next_monday = today + timedelta(days=-today.weekday(), weeks=1)
    next_sunday = next_monday + timedelta(days = 6)
    next_two_monday = today + timedelta(days=-today.weekday(), weeks=2)
    next_two_sunday = next_two_monday + timedelta(days = 6)

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
    pre_cnds    = navb.conditions(None, auth)
    cnds    = navb.conditions(None, auth)
    pre_cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    pre_cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) : ''})

    DESCRI = [('next_week', 'Deliveries in Next Week'), ('next_two_week', 'Deliveries in Next two Weeks')]
    INDICS = [
	('pre', 'Pregnancies', "(report_date <= '%s') AND (lmp + INTERVAL '%s days') >= '%s'" % ( navb.finish, settings.GESTATION , navb.start)),
	('next_week', 'Deliveries in Next Week', "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_monday, next_sunday)),
	('next_two_week', 'Deliveries in Next two Weeks', "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_two_monday, next_two_sunday)),
	
	]

    SUB_INDICS = { 'no_risk': '(%s)' % queries.NO_RISK['query_str'] , 
		   'at_risk': '(%s)' % queries.RISK['query_str'],
		   'high_risk': '(%s)' % queries.HIGH_RISK['query_str'],
		 }
    if kw.get('subgroup'): cnds.update({SUB_INDICS[kw.get('subgroup')]: ''})
    if kw.get('group') == 'next_week':
     INDICS = [
	('next_week', 'Deliveries in Next Week', "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_monday, next_sunday))
	]
     start = next_monday; end = next_sunday
     cnds.update({"(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , start, end): ''})
    elif kw.get('group') == 'next_two_week':
     INDICS = [
	('next_two_week', 'Deliveries in Next two Weeks', "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_two_monday, next_two_sunday)),
	]
     start = next_two_monday; end = next_two_sunday
     cnds.update({"(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , start, end): ''})
    elif kw.get('group') == 'pre':
     INDICS = [
	('pre', 'Pregnancies', "(report_date <= '%s') AND (lmp + INTERVAL '%s days') >= '%s'" % ( navb.finish, settings.GESTATION , navb.start)),
	]
     cnds.update({"(report_date <= '%s') AND (lmp + INTERVAL '%s days') >= '%s'" % ( navb.finish, settings.GESTATION , navb.start): ''})
    else:
     cnds.update({  "%s OR %s" % ( 
			"(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_monday, next_sunday),
			"(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_two_monday, next_two_sunday) 			
			) : ''})

    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     wcl = [{'field_name': '%s' % kw.get('subcat'), 
		'compare': '%s' % kw.get('compare') if kw.get('compare') else '', 
		'value': '%s' % kw.get('value') if kw.get('value') else '' 
	   }] if kw.get('subcat') else []

     if kw.get('group') == 'next_week':
      start = next_monday; end = next_sunday
      wcl.append({'field_name': '(%s)' % "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , start, end),
                  'compare': '', 'value': '', 'extra': True})

     if kw.get('group') == 'next_two_week':
      start = next_two_monday; end = next_two_sunday
      wcl.append({'field_name': '(%s)' % "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , start, end),
                  'compare': '', 'value': '', 'extra': True})

     if kw.get('group') == 'pre':
      wcl.append({'field_name': '(%s)' % ("(report_date) <= '%s'" % ( navb.finish) ), 'compare': '', 'value': '', 'extra': True})
      wcl.append({'field_name': '(%s)' % ("(lmp + INTERVAL \'%d days\') >= '%s'" % (settings.GESTATION, navb.start) ), 'compare': '', 'value': '', 'extra': True})

     if kw.get('subgroup'):	wcl.append({'field_name': '(%s)' % SUB_INDICS[kw.get('subgroup')], 'compare': '', 'value': '', 'extra': True}) 
    
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      locateds = summarize_by_location(primary_table = 'rw_pregnancies', MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						#start =  navb.start,
						#end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ (x[0].split()[0], x[1]) for x in INDICS])

    sc      = kw.get('subcat')
    if kw.get('compare') and kw.get('value'): sc += kw.get('compare') + kw.get('value')
    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'mother_weight': lambda x, _, __: '%s' % (int(x) if x else ''),
      'lmp': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    if sc:
      cnds[sc]  = ''
    # TODO: optimise
    attrs = []
    
    cols    += queries.LOCATION_INFO
    if kw.get('group') == 'pre':
     DESCRI.append(('pre', 'Pregnancies'))
     cnds = pre_cnds   
    nat     = orm.ORM.query('rw_pregnancies', cnds,
      cols  = [x[0] for x in (cols + [
					('(lmp + INTERVAL \'%d days\') AS edd' % settings.GESTATION, 'EDDate'),
					('(%s) AS at_risky' % queries.RISK['query_str'], 'AtRisky'), 
					('(%s) AS high_risky' % queries.HIGH_RISK['query_str'], 'HighRisky'),

					] + attrs) if x[0][0] != '_'],
      
    )#;print nat.query
    desc  = 'Deliveries Notifications %s' % (' (%s)' % (self.find_descr(DESCRI , 
						sc or kw.get('group') ) or 'ALL', 
					) )
    return self.dynamised('deliverynotdash_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_deliverydash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions('report_date', auth)
    exts = {}
    
    attrs = [(makecol(x[0]), x[1]) for x in queries.DELIVERY_DATA['attrs']]
    cnds.update({queries.DELIVERY_DATA['query_str']: ''})
    exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.DELIVERY_DATA['attrs']]))#;print exts
    nat = orm.ORM.query(  'rw_children', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts,
			)#;print nat.query
    
    today = datetime.today().date()
    next_monday = today + timedelta(days=-today.weekday(), weeks=1)
    next_sunday = next_monday + timedelta(days = 6)
    next_week_cnds = navb.conditions('report_date')
    next_week_cnds.update({"(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_monday, next_sunday): ''})
    next_week = orm.ORM.query(  'rw_pregnancies', 
    			  next_week_cnds, 
    			  cols = ['COUNT(*) AS total']
    			)

    next_two_monday = today + timedelta(days=-today.weekday(), weeks=2)
    next_two_sunday = next_two_monday + timedelta(days = 6)
    next_two_week_cnds = navb.conditions('report_date')
    next_two_week_cnds.update({"(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , next_two_monday, next_two_sunday): ''})
    next_two_week = orm.ORM.query(  'rw_pregnancies', 
    			  next_two_week_cnds, 
    			  cols = ['COUNT(*) AS total'],
    			)

    return self.dynamised('deliverydash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_deliverydash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      ('birth_date',            'Date Of Birth'),
      
    ] , *args, **kw)
    DESCRI = []
    DELDICT = makedict(queries.DELIVERY_DATA['attrs'])
    INDICS = [ DELDICT[key] for key in DELDICT.keys() ] 
    wcl = []
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) >= '%s'" % (navb.start) : ''})
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    primary_table = 'rw_children'

    if kw.get('group'):
     primary_table = 'rw_pregnancies'
     today = datetime.today().date()
     if kw.get('group') == 'next_week': weeks = 1
     if kw.get('group') == 'next_two_week': weeks = 2
     start = today + timedelta(days=-today.weekday(), weeks=weeks)
     end = start + timedelta(days = 6)
     cnds.update({"(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , start, end): ''})
    else:
     cnds.update({queries.DELIVERY_DATA['query_str']: ''})
    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.DELIVERY_DATA['attrs']]:
     cnds.update({queries.DELIVERY_DATA['query_str']: ''})
     cnds.update({ DELDICT[kw.get('subcat')][0] : ''})
     INDICS = [DELDICT[kw.get('subcat')]]
    else:
     if kw.get('group'): DESCRI = [('next_week', 'Deliveries in Next Week'), ('next_two_week', 'Deliveries in Next two Weeks')]
     else: INDICS = INDICS#;print INDICS
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = DELDICT if kw.get('subcat') in [x[0] for x in queries.DELIVERY_DATA['attrs']] else  {}
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []

     if kw.get('group'):
      wcl.append({'field_name': '(%s)' % "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (settings.GESTATION , start, end),
                  'compare': '', 'value': '', 'extra': True})
     else: wcl.append({'field_name': '(%s)' % queries.DELIVERY_DATA['query_str'], 'compare': '', 'value': '', 'extra': True})
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      locateds = summarize_by_location(primary_table = primary_table, MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						start =  navb.start,
						end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )#;print tabular
      INDICS_HEADERS = dict([ (makecol(x[0]), x[1]) for x in INDICS])

    sc      = kw.get('subcat')
    
    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'birth_date': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    if sc:
      cnds[DELDICT[sc][0]] = ''
    # TODO: optimise
    attrs = []
    
    cols    += queries.LOCATION_INFO   
    nat     = orm.ORM.query(primary_table, cnds,
      cols  = [x[0] for x in (cols + [
					
					] + attrs) if x[0][0] != '_'],
      
    )
    desc  = 'Deliveries %s' % (' (%s)' % (self.find_descr([(makecol(x[0]), x[1]) for x in INDICS], kw.get('subcat')),
												 ) if kw.get('subcat') else 'ALL', )
    return self.dynamised('deliverydash_table', mapping = locals(), *args, **kw)


  #### END OF DELIVERY ###


  #### START OF NEWBORN ###
  @cherrypy.expose
  def dashboards_nbcdash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    cnds.update({"(birth_date + INTERVAL \'%d days\') >= '%s'" % (settings.NBC_GESTATION, navb.start) : ''})
    exts = {}
    newborns = orm.ORM.query(  'rw_children', 
			  cnds,
                          cols = ['COUNT(*) AS total'],
			)#; print newborns.query
    total = newborns[0]['total']

    if kw.get('group') == 'no_risk':
      title = 'No Risk'
      group = 'no_risk'
      cnds.update({queries.NBC_DATA['NO_RISK']['query_str']: ''})
      nat = orm.ORM.query(  'rw_children', 
			  cnds,
                          cols = ['COUNT(*) AS total'],
			)
    elif kw.get('group') == 'at_risk':
      title = 'At Risk'
      group = 'at_risk'
      cnds.update({queries.NBC_DATA['RISK']['query_str']: ''})
      attrs = [(makecol(x[0]), x[1]) for x in queries.NBC_DATA['RISK']['attrs'] ]
      exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.NBC_DATA['RISK']['attrs']] ))
      nat = orm.ORM.query(  'rw_children', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts,
			)
    elif kw.get('group') == 'high_risk':
      title = 'High Risk'
      group = 'high_risk'
      cnds.update({queries.NBC_DATA['HIGH_RISK']['query_str']: ''})
      attrs = [(makecol(x[0]), x[1]) for x in queries.NBC_DATA['HIGH_RISK']['attrs'] ]
      exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.NBC_DATA['HIGH_RISK']['attrs']] ))
      nat = orm.ORM.query(  'rw_children', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts,
			)
    elif kw.get('group') in  [ makecol(x[0]) for x in queries.NBC_DATA['NBC']['attrs'] ] :
      title = makedict(queries.NBC_DATA['NBC']['attrs'])[kw.get('group')][1]
      group = kw.get('group')
      cnds.update({makedict(queries.NBC_DATA['NBC']['attrs'])[group][0]: ''})
      nat = orm.ORM.query(  'child_track', 
			  cnds, 
			  cols = ['COUNT(*) AS total'],
			)
    else:
      nat = orm.ORM.query(  'rw_children', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = {'no_risk': ('COUNT(*)', queries.NBC_DATA['NO_RISK']['query_str']), 
					'at_risk': ('COUNT(*)', queries.NBC_DATA['RISK']['query_str']),
					'high_risk': ('COUNT(*)', queries.NBC_DATA['HIGH_RISK']['query_str']),
					}
			)
    
      visits = orm.ORM.query(  'child_track', 
			  cnds,
                          cols = ['COUNT(*) AS total'],
			  extended = dict([ ( makecol(x[0]), ('COUNT(*)', x[0]) ) for x in queries.NBC_DATA['NBC']['attrs'] ])
			)#; print visits.query;


    return self.dynamised('nbcdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_nbcdash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      ('birth_date',            'Date Of Birth'),
      ('child_number', 'Child Number'),
      ('gender', 'Sex'),
      ('breastfeeding', 'Breastfeeding'),
      ('child_weight', 'Weight')
      
    ] , *args, **kw)
    auth    = ThousandAuth(cherrypy.session.get('email'))
    DESCRI = []
    NBCDICT = makedict(queries.NBC_DATA['NBC']['attrs'])
    NBCRISKDICT = makedict(queries.NBC_DATA['RISK']['attrs'])
    NBCHIGHRISKDICT = makedict(queries.NBC_DATA['HIGH_RISK']['attrs'])
    INDICS = []
    NBC_INDICS = [ NBCDICT[key] for key in NBCDICT.keys() ]
    RISK_INDICS = [ NBCRISKDICT[key] for key in NBCRISKDICT.keys() ] 
    HIGH_RISK_INDICS = [ NBCHIGHRISKDICT[key] for key in NBCHIGHRISKDICT.keys() ]
    wcl = []
    nbc_wcl = []
    nbc_cnds 	= navb.conditions(None, auth)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    cnds.update({"(birth_date + INTERVAL \'%d days\') >= '%s'" % (settings.NBC_GESTATION, navb.start) : ''})

    if kw.get('group') and kw.get('group') == 'no_risk':
    	cnds.update({queries.NBC_DATA['NO_RISK']['query_str']: ''})
    if kw.get('group') and (kw.get('group') in [ makecol(z[0]) for z in NBC_INDICS ]):
    	nbc_cnds.update({ NBCDICT[kw.get('group')][0] : ''})
    	NBC_INDICS = [NBCDICT[kw.get('group')]]
    if kw.get('subcat') and (kw.get('subcat') in [ makecol(z[0]) for z in RISK_INDICS ]):
        cnds.update({queries.NBC_DATA['RISK']['query_str']: ''})
	cnds.update({ NBCRISKDICT[kw.get('subcat')][0] : ''})
    	INDICS = [NBCRISKDICT[kw.get('subcat')]]
    if kw.get('subcat') and (kw.get('subcat') in [ makecol(z[0]) for z in HIGH_RISK_INDICS ]):
    	cnds.update({queries.NBC_DATA['HIGH_RISK']['query_str']: ''})
	cnds.update({ NBCHIGHRISKDICT[kw.get('subcat')][0] : ''})
    	INDICS = [NBCHIGHRISKDICT[kw.get('subcat')]]
       
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = {}
      if kw.get('subcat') in [ makecol(x[0]) for x in NBC_INDICS ]:
      	DATADICT = NBCDICT
      	nbc_wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []
      else:
      	if kw.get('subcat') in [ makecol(x[0]) for x in RISK_INDICS ]: DATADICT = NBCRISKDICT
      	if kw.get('subcat') in [ makecol(x[0]) for x in HIGH_RISK_INDICS ]: DATADICT = NBCHIGHRISKDICT
      	wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []
     
     if kw.get('subcat') is None:
      if kw.get('group') == 'no_risk':
       wcl.append({'field_name': '(%s)' % queries.NBC_DATA['NO_RISK']['query_str'], 'compare': '', 'value': '', 'extra': True})
       INDICS = []
      if kw.get('group') == 'at_risk':
       wcl.append({'field_name': '(%s)' % queries.NBC_DATA['RISK']['query_str'], 'compare': '', 'value': '', 'extra': True})
       INDICS = RISK_INDICS
      if kw.get('group') == 'high_risk':
       wcl.append({'field_name': '(%s)' % queries.NBC_DATA['HIGH_RISK']['query_str'], 'compare': '', 'value': '', 'extra': True})
       INDICS = HIGH_RISK_INDICS
      if kw.get('group') is None:
       INDICS = [('no_risk', 'No Risk', '(%s)' % queries.NBC_DATA['NO_RISK']['query_str'] ), 
		('at_risk', 'At Risk', '(%s)' % queries.NBC_DATA['RISK']['query_str']),
		 ('high_risk', 'High Risk', '(%s)' % queries.NBC_DATA['HIGH_RISK']['query_str']),
		]#; print INDICS

     wcl.append({'field_name': '(%s)' % ("(report_date) <= '%s'" % ( navb.finish) ), 'compare': '', 'value': '', 'extra': True})
     wcl.append({'field_name': '(%s)' % ("(birth_date + INTERVAL \'%d days\') >= '%s'" % (settings.NBC_GESTATION, navb.start) ), 'compare': '', 'value': '', 'extra': True})
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      #print INDICS, wcl
      locateds = summarize_by_location(primary_table = "rw_children", MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						#start =  navb.start,
						#end = navb.finish,
											
						)
      locateds2 = summarize_by_location(primary_table = "child_track", MANY_INDICS = NBC_INDICS, where_clause = nbc_wcl, 
						province = province,
						district = district,
						location = location,
						#start =  navb.start,
						#end = navb.finish,
											
						)#;print locateds,locateds2, province,district,location, wcl, nbc_wcl
      if locateds == [] or type(locateds[0]) == Record: locateds = [locateds] + locateds2
      else: locateds += locateds2 
      tabular = give_me_table(locateds, MANY_INDICS = INDICS + NBC_INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ ( makecol(x[0]), x[1]) for x in INDICS ]  + [ ( makecol(x[0]), x[1]) for x in NBC_INDICS] )

    sc      = kw.get('subcat')

    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/nbcchild?pid=%s">%s</a>' % (x, x),
      'child_weight': lambda x, _, __: '%s' % (int(x) if x else ''),
      'gender': lambda x, _, __: '%s' % ( 'M' if x else 'F'),
      'birth_date': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }#;print cnds,kw.get('value')
    
      
    attrs = []
    if kw.get('group') == 'no_risk':
     cnds.update({'(%s)' % queries.NBC_DATA['NO_RISK']['query_str']: ''})
     DESCRI.append(('no_risk', 'No Risk'))
    if kw.get('group') == 'at_risk':
     cnds.update({'(%s)' % queries.NBC_DATA['RISK']['query_str']: ''})
     DESCRI.append(('at_risk', 'At Risk'))
    if kw.get('group') == 'high_risk':
     cnds.update({'(%s)' % queries.NBC_DATA['HIGH_RISK']['query_str']: ''})
     DESCRI.append(('high_risk', 'High Risk'))

    cols    += queries.LOCATION_INFO 
    #print cnds, sc
    if kw.get('subcat') and (kw.get('subcat') in [ makecol(z[0]) for z in NBC_INDICS ] ):
     if sc:
      nbc_cnds[NBCDICT[sc][0]] = ''
     nbcnat     = orm.ORM.query('child_track', nbc_cnds,
		      cols  = ['child'],
		      
		    )
     nbcindexcol = [x['child'] for x in nbcnat.list()];print nbcindexcol
     if len(nbcindexcol) > 1: cnds.update({'indexcol IN %s' % str(tuple(nbcindexcol))  : ''})
     if len(nbcindexcol) == 1: cnds.update({'indexcol = %s' % str(nbcindexcol[0])  : ''})      
    nat     = orm.ORM.query('rw_children', cnds,
      cols  = [x[0] for x in (cols + [
					('(%s) AS at_risky' % queries.NBC_DATA['RISK']['query_str'], 'AtRisky'), 
					('(%s) AS high_risky' % queries.NBC_DATA['HIGH_RISK']['query_str'], 'HighRisky')
 
					] + attrs) if x[0][0] != '_'],
      
    )#;print nat.query
    desc  = 'Newborn Visits%s' % (' (%s)' % (self.find_descr(DESCRI + [( makecol(x[0]), x[1]) for x in INDICS
									] + [ ( makecol(x[0]), x[1]) for x in NBC_INDICS], 
						sc or kw.get('group')), 
					) if sc or kw.get('group') else '', );print desc
    return self.dynamised('nbcdash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_nbcchild(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = queries.PATIENT_DETAILS , *args, **kw)
    attrs = [ (' %s AS %s' % (x[0], makecol(x[0])), x[1]) for x in queries.NBC_DATA['RISK']['attrs'] + queries.NBC_DATA['HIGH_RISK']['attrs']  
		] + [('nbc_visit', 'Number Of Visit')]
    indexed_attrs = [ ('%s' % get_indexed_value('name', x[2], x[1], x[0], x[3]), x[3]) for x in queries.INDEXED_VALS['location']]
    nat     = orm.ORM.query('rw_nbcvisits', cnds,
      				cols  = [x[0] for x in (cols + indexed_attrs + queries.NBC_DATA['cols'] + attrs) if x[0][0] != '_'] ,
				sort = ('report_date', False),
    			)#;print nat.query
    patient = nat[0]  
    reminders = []
    nbc_reports = [ x for x in nat.list() ]#; print attrs
    cbn_reports =   orm.ORM.query('rw_nutritions', cnds)
    return self.dynamised('newborn_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def __tables_child(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = queries.PATIENT_DETAILS , *args, **kw)
    attrs = [ (' %s AS %s' % (x[0], makecol(x[0])), x[1]) for x in queries.NBC_DATA['RISK']['attrs'] + queries.NBC_DATA['HIGH_RISK']['attrs'] ]
    indexed_attrs = [ ('%s' % get_indexed_value('name', x[2], x[1], x[0], x[3]), x[3]) for x in queries.INDEXED_VALS['location']]
    nat     = orm.ORM.query('nbc_table', cnds,
      				cols  = [x[0] for x in (cols + indexed_attrs + queries.NBC_DATA['cols'] + attrs) if x[0][0] != '_'],
				sort = ('report_date', False),
    			)
    patient = nat[0]  
    reminders = []
    nbc_reports = [ x for x in nat.list() ]#; print attrs
    cbn_reports =   orm.ORM.query('cbn_table', cnds)
    return self.dynamised('child_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_childgrowth(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      ('birth_date',            'Date Of Birth'),
      ('child_number', 'Child Number'),
      ('gender', 'Sex'),
      ('breastfeeding', 'Breastfeeding'),
      ('child_weight', 'Weight')
      
    ] , *args, **kw)
    cnds    = navb.conditions(None, auth)
    ncnds    = navb.conditions(None, auth)
    cnds.update({'indexcol = %s' % kw.get('pid'): ''})
    ncnds.update({'child_id = %s' % kw.get('pid'): ''})
    indexed_attrs = [ ('%s' % get_indexed_value('name', x[2], x[1], x[0], x[3]), x[3]) for x in queries.INDEXED_VALS['location']]
    nat     = orm.ORM.query('rw_children', cnds,
      				cols  = [x[0] for x in (cols + indexed_attrs) if x[0][0] != '_'],
				sort = ('report_date', False),
    			)
    patient = nat[0]  
    reminders = []
    nbc_reports = [ x for x in nat.list() ]#; print cols, cnds, ncnds
    cbn_reports =   orm.ORM.query('rw_nutritions', ncnds, cols = [
							"indangamuntu AS indangamuntu", 
							"child_number",
							"birth_date", 
							"report_date",
							"child_weight AS weight",  
							"child_height AS height",
							],
						 )#;print cbn_reports.query
    chartData = json.dumps([ {'weight': cbn['weight'] , 'height': cbn['height'], 'age': (cbn['report_date'] - cbn['birth_date']).days / 30.4374 
				} for cbn in cbn_reports.list()])
    #print chartData
    
    return self.dynamised('growthchart', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_grownthcharts(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = queries.PATIENT_DETAILS , *args, **kw)
    #cnds    = navb.conditions(None, auth)
    #boys_cnds = navb.conditions(None, auth)
    
    #boys_data =   orm.ORM.query('nutrition_childnutrition', cnds, cols = [
	#							"DISTINCT ON (child_id, age) child_id",
	#						"gender", 
	#						"age_in_months AS age",
	#						"weight",  
	#						"height",
	#						],
	#						sort = ('age', 'DESC')
	#					 )
    #boys = json.dumps([ {'weight': cbn['weight'] , 'height': cbn['height'], 'age': cbn['age'] } for cbn in boys_data.list()])
    #print boys	
    chart_data = json.dumps({'boys': [{'id':1, 'weight': 3.5 , 'height': 59, 'age': 2},{'id':2, 'weight': 4.5 , 'height': 59, 'age': 3 }, {'id':3, 'weight': 5.5 , 'height': 60, 'age': 4 },{'id':4, 'weight': 7.5 , 'height': 67.6, 'age': 6 }, {'id':5, 'weight': 5.8 , 'height': 67.9, 'age': 7 }, {'id':6, 'weight': 6.0 , 'height': 68.6, 'age': 8 }, {'id':7, 'weight': 6.5 , 'height': 70.6, 'age': 9 }, {'id':8, 'weight': 8 , 'height': 73.6, 'age': 10}], 'girls': [{'id':1, 'weight': 3.5 , 'height': 59, 'age': 2},{'id':2, 'weight': 4.5 , 'height': 59, 'age': 3 }, {'id':3, 'weight': 5.5 , 'height': 60, 'age': 4 },{'id':4, 'weight': 7.5 , 'height': 67.6, 'age': 6 }, {'id':5, 'weight': 5.8 , 'height': 67.9, 'age': 7 }, {'id':6, 'weight': 6.0 , 'height': 68.6, 'age': 8 }, {'id':7, 'weight': 6.5 , 'height': 70.6, 'age': 9 }, {'id':8, 'weight': 8 , 'height': 73.6, 'age': 10}] })
    return self.dynamised('_nutrition_charts', mapping = locals(), *args, **kw)
  ### END OF NEWBORN ####

  #### START OF POSTNATAL ###
  @cherrypy.expose
  def dashboards_pncdash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    vcnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    vcnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    cnds.update({"(birth_date + INTERVAL \'%d days\') >= '%s'" % (settings.PNC_GESTATION, navb.start) : ''})
    vcnds.update({"(delivery_date + INTERVAL \'%d days\') >= '%s'" % (settings.PNC_GESTATION, navb.start) : ''})
    exts = {}
    total = orm.ORM.query(  'rw_pncvisits', 
			  cnds,
                          cols = ['COUNT(*) AS total'],
			)[0]['total']
    if kw.get('group') == 'no_risk':
      title = 'No Risk'
      group = 'no_risk'
      cnds.update({queries.PNC_DATA['NO_RISK']['query_str']: ''})
      nat = orm.ORM.query(  'rw_pncvisits', 
			  cnds,
                          cols = ['COUNT(*) AS total'],
			)
    elif kw.get('group') == 'at_risk':
      title = 'At Risk'
      group = 'at_risk'
      cnds.update({queries.PNC_DATA['RISK']['query_str']: ''})
      attrs = [(x.split()[0], dict(queries.PNC_DATA['RISK']['attrs'])[x]) for x in dict (queries.PNC_DATA['RISK']['attrs'])]
      exts.update(dict([(x.split()[0], ('COUNT(*)',x)) for x in dict (queries.PNC_DATA['RISK']['attrs'])]))
      nat = orm.ORM.query(  'rw_pncvisits', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts,
			)
    elif kw.get('group') in queries.PNC_DATA['PNC'].keys() :
      title = queries.PNC_DATA['PNC'][kw.get('group')][1]
      group = kw.get('group')
      vcnds.update({queries.PNC_DATA['PNC'][group][0]: ''})
      nat = orm.ORM.query(  'mother_track', 
			  vcnds, 
			  cols = ['COUNT(*) AS total'],
			)
    else:
      nat = orm.ORM.query(  'rw_pncvisits', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = {'no_risk': ('COUNT(*)', queries.PNC_DATA['NO_RISK']['query_str']), 
					'at_risk': ('COUNT(*)', queries.PNC_DATA['RISK']['query_str']),
					}
			)#;print nat.query

      visits = orm.ORM.query(  'mother_track', 
			  vcnds,
                          cols = ['COUNT(*) AS total'],
			  extended = dict([ ( x, ('COUNT(*)', queries.PNC_DATA['PNC'][x][0]) ) for x in queries.PNC_DATA['PNC'].keys() ])
			)
    return self.dynamised('pncdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_pncdash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      ('birth_date',            'Delivery Date'),
      
    ] , *args, **kw)
    DESCRI = []
    INDICS = []
    PNC_INDICS = [(key, queries.PNC_DATA['PNC'][key][1], queries.PNC_DATA['PNC'][key][0] ) for key in queries.PNC_DATA['PNC'].keys() ]
    pnc_cnds 	= navb.conditions(None, auth)

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    cnds.update({"(birth_date + INTERVAL \'%d days\') >= '%s'" % (settings.PNC_GESTATION, navb.start) : ''})

    if kw.get('subcat') and kw.get('subcat').__contains__('symptom_'):
     if kw.get('group'):
      if kw.get('group') == 'no_risk':
       cnds.update({'(%s)' % queries.PNC_DATA['NO_RISK']['query_str']: ''})
      else:
       kw.update({'compare': ' IS NOT'})
       kw.update({'value': ' NULL'})

    if kw.get('group') and (kw.get('group') in [ z[0] for z in PNC_INDICS ]):
	pnc_cnds.update({'(%s)' % queries.PNC_DATA['PNC'].get(kw.get('group'))[0]: ''})

    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     wcl = [{'field_name': '%s' % kw.get('subcat'), 
		'compare': '%s' % kw.get('compare') if kw.get('compare') else '', 
		'value': '%s' % kw.get('value') if kw.get('value') else '' 
	   }] if kw.get('subcat') else []
     if kw.get('subcat') is None:
      if kw.get('group') == 'no_risk':
       wcl.append({'field_name': '(%s)' % queries.PNC_DATA['NO_RISK']['query_str'], 'compare': '', 'value': '', 'extra': True})
       INDICS = []
      if kw.get('group') == 'at_risk':
       wcl.append({'field_name': '(%s)' % queries.PNC_DATA['RISK']['query_str'], 'compare': '', 'value': '', 'extra': True})
       INDICS = queries.PNC_DATA['RISK']['attrs']
      if kw.get('group') is None:
       INDICS = [('no_risk', 'No Risk', '(%s)' % queries.PNC_DATA['NO_RISK']['query_str'] ), 
		('at_risk', 'At Risk', '(%s)' % queries.PNC_DATA['RISK']['query_str']),
		]#; print INDICS
     
     wcl.append({'field_name': '(%s)' % ("(report_date) <= '%s'" % ( navb.finish) ), 'compare': '', 'value': '', 'extra': True})
     wcl.append({'field_name': '(%s)' % ("(birth_date + INTERVAL \'%d days\') >= '%s'" % (settings.PNC_GESTATION, navb.start) ), 'compare': '', 'value': '', 'extra': True})

     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      locateds = summarize_by_location(primary_table = 'rw_pncvisits', MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						#start =  navb.start,
						#end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ (x[0].split()[0], x[1]) for x in INDICS])

    sc      = kw.get('subcat')
    if kw.get('compare') and kw.get('value'): sc += kw.get('compare') + kw.get('value')
    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'birth_date': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    if sc:
      cnds[sc]  = ''
    attrs = []
    if kw.get('group') == 'no_risk':
     cnds.update({'(%s)' % queries.PNC_DATA['NO_RISK']['query_str']: ''})
     DESCRI.append(('no_risk', 'No Risk'))
    if kw.get('group') == 'at_risk':
     cnds.update({'(%s)' % queries.PNC_DATA['RISK']['query_str']: ''})
     DESCRI.append(('at_risk', 'At Risk'))

    cols    += queries.LOCATION_INFO

    if kw.get('group') and (kw.get('group') in [ z[0] for z in PNC_INDICS ] ):
     pncnat     = orm.ORM.query('mother_track', pnc_cnds,
		      cols  = [kw.get('group')],
		      
		    )
     pncindexcol = [x[kw.get('group')] for x in pncnat.list()]#;print pncindexcol
     if len(pncindexcol) > 1: cnds.update({'indexcol IN %s' % str(tuple(pncindexcol))  : ''})
     if len(pncindexcol) == 1: cnds.update({'indexcol = %s' % str(pncindexcol[0])  : ''})
        
    nat     = orm.ORM.query('rw_pncvisits', cnds,
      cols  = [x[0] for x in (cols + [
					('(birth_date) AS dob', 'Delivery Date'),
 
					] + attrs) if x[0][0] != '_'],
      
    )
    desc  = 'Postnatal Visits%s' % (' (%s)' % (self.find_descr(DESCRI + queries.PNC_DATA['RISK']['attrs'] + [(x[0], x[1]) for x in PNC_INDICS], 
						sc or kw.get('group')), 
					) if sc or kw.get('group') else '', )
    return self.dynamised('pncdash_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def tables_child(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = queries.PATIENT_DETAILS , *args, **kw)
    attrs = [ (' %s AS %s' % ( x[0], makecol(x[0]) ), x[1]) for x in queries.NBC_DATA['RISK']['attrs'] + queries.NBC_DATA['HIGH_RISK']['attrs'] ]
    indexed_attrs = [ ('%s' % get_indexed_value('name', x[2], x[1], x[0], x[3]), x[3]) for x in queries.INDEXED_VALS['location']]
    nat     = orm.ORM.query('rw_children', cnds,
      				cols  = [x[0] for x in (cols + indexed_attrs + queries.NBC_DATA['cols'] + attrs) if x[0][0] != '_'],
				sort = ('report_date', False),
    			)
    patient = nat[0]  
    reminders = []
    nbc_reports = [ x for x in nat.list() ]#; print attrs
    cbn_reports = orm.ORM.query('rw_nutritions', cnds)
    return self.dynamised('child_table', mapping = locals(), *args, **kw)

  ### END OF POSTNATAL ####

  #### START OF VACCINATION ###
  @cherrypy.expose
  def dashboards_vaccindash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions('report_date', auth)
    exts = {}
    
    vac_comps_attrs = [(makecol(x[0]), x[1]) for x in queries.VAC_DATA['VAC_COMPLETION']['attrs']]
    vac_comps_exts = exts
    vac_comps_exts.update(dict([(makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.VAC_DATA['VAC_COMPLETION']['attrs']]))
    vac_comps = orm.ORM.query(  'rw_childhealth', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = vac_comps_exts,
			)

    vac_series_attrs = [(makecol(x[0]), x[1]) for x in queries.VAC_DATA['VAC_SERIES']['attrs']]
    vac_series_exts = exts
    vac_series_exts.update(dict([(makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.VAC_DATA['VAC_SERIES']['attrs']]))
    vac_series = orm.ORM.query(  'rw_childhealth', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = vac_series_exts,
			)



    return self.dynamised('vaccindash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_vaccindash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      ('birth_date',            'Date Of Birth'),
      
    ] , *args, **kw)
    DESCRI = []
    VACDICT = makedict(queries.VAC_DATA['VAC_COMPLETION']['attrs'])
    SERIESDICT = makedict(queries.VAC_DATA['VAC_SERIES']['attrs'])
    INDICS = [VACDICT[key] for key in VACDICT] + [SERIESDICT[key] for key in SERIESDICT.keys()] #;print INDICS
    wcl = []

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) >= '%s'" % (navb.start) : ''})
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})

    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.VAC_DATA['VAC_COMPLETION']['attrs']]:
     cnds.update({queries.VAC_DATA['VAC_COMPLETION']['query_str']: ''})
     cnds.update({ VACDICT[kw.get('subcat')][0] : ''})
     INDICS = [VACDICT[kw.get('subcat')]]

    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.VAC_DATA['VAC_SERIES']['attrs']]:
     cnds.update({queries.VAC_DATA['VAC_SERIES']['query_str']: ''})
     cnds.update({ SERIESDICT[kw.get('subcat')][0] : ''})
     INDICS = [SERIESDICT[kw.get('subcat')]]

    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = {}
      if kw.get('subcat') in [makecol(x[0]) for x in queries.VAC_DATA['VAC_COMPLETION']['attrs']]: DATADICT = VACHDICT
      if kw.get('subcat') in [makecol(x[0]) for x in queries.VAC_DATA['VAC_SERIES']['attrs']]: DATADICT = SERIESDICT
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []

     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      locateds = summarize_by_location(primary_table = 'rw_childhealth', MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						start =  navb.start,
						end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ (makecol(x[0]), x[1]) for x in INDICS])

    sc      = kw.get('subcat')
    
    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/child?pid=%s">%s</a>' % (x, x),
      'wt_float': lambda x, _, __: '%s' % (int(x) if x else ''),
      'lmp': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    if sc:
      pass#cnds[sc]  = ''
    attrs = []
    
    cols    += queries.LOCATION_INFO   
    nat     = orm.ORM.query('rw_childhealth', cnds,
      cols  = [x[0] for x in (cols + attrs) if x[0][0] != '_'],
      
    )
    desc  = 'Vaccination %s' % (' (%s)' % (self.find_descr(DESCRI + [ (makecol(x[0]), x[1]) for x in INDICS ], 
						sc) or 'ALL', 
					) )
    return self.dynamised('vaccindash_table', mapping = locals(), *args, **kw)


  #### END OF VACCINATION ###

  #### START OF CCM ###
  @cherrypy.expose
  def dashboards_ccmdash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions('report_date')
    exts = {}
    
    ccm_attrs = [( makecol(x[0]), x[1]) for x in queries.CCM_DATA['attrs']]
    ccm_exts = exts
    ccm_cnds = cnds
    ccm_cnds.update({queries.CCM_DATA['query_str']: ''})
    ccm_exts.update(dict([( makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.CCM_DATA['attrs']]))
    ccm = orm.ORM.query(  'rw_ccms', 
			  ccm_cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = ccm_exts,
			)

    cmr_attrs = [( makecol(x[0]), x[1]) for x in queries.CMR_DATA['attrs']]
    cmr_cnds = navb.conditions('report_date')
    cmr_cnds.update({queries.CMR_DATA['query_str']: ''})
    cmr_exts = dict([( makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.CMR_DATA['attrs']])
    cmr = orm.ORM.query(  'rw_ccms', 
			  cmr_cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = cmr_exts,
			)

    return self.dynamised('ccmdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_ccmdash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      ('birth_date',            'Date Of Birth'),
      ('symptom_ma',            'Malaria'),
      ('symptom_pc',            'Pneumonia'),
      ('symptom_di',            'Diarrhea'),
      
    ] , *args, **kw)
    DESCRI = []
    CCMDICT = makedict(queries.CCM_DATA['attrs'])
    CMRDICT = makedict(queries.CMR_DATA['attrs'])
    INDICS = [CCMDICT[key] for key in CCMDICT] + [CMRDICT[key] for key in CMRDICT.keys()] #;print INDICS
    wcl = []

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) >= '%s'" % (navb.start) : ''})
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    primary_table = 'rw_ccms'

    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.CCM_DATA['attrs']]:
     cnds.update({queries.CCM_DATA['query_str']: ''})
     cnds.update({ CCMDICT[kw.get('subcat')][0] : ''})
     INDICS = [CCMDICT[kw.get('subcat')]]

    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.CMR_DATA['attrs']]:
     cnds.update({queries.CMR_DATA['query_str']: ''})
     cnds.update({ CMRDICT[kw.get('subcat')][0] : ''})
     INDICS = [CMRDICT[kw.get('subcat')]]


    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = {}
      if kw.get('subcat') in [makecol(x[0]) for x in queries.CCM_DATA['attrs']]: DATADICT = CCMDICT;wcl.append({'field_name': '(%s)' % queries.ANC_DATA['query_str'], 'compare': '', 'value': '', 'extra': True})
      if kw.get('subcat') in [makecol(x[0]) for x in queries.CMR_DATA['attrs']]: DATADICT = CMRDICT
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []

      
      if kw.get('subcat') in [makecol(x[0]) for x in queries.CCM_DATA['attrs']]:
      	wcl.append({'field_name': '(%s)' % queries.CCM_DATA['query_str'], 'compare': '', 'value': '', 'extra': True})
      if kw.get('subcat') in [makecol(x[0]) for x in queries.CMR_DATA['attrs']]:
      	wcl.append({'field_name': '(%s)' % queries.CMR_DATA['query_str'], 'compare': '', 'value': '', 'extra': True})

     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      locateds = summarize_by_location(primary_table = primary_table, MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						start =  navb.start,
						end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ ( makecol(x[0]), x[1]) for x in INDICS])

    sc      = kw.get('subcat')

    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/child?pid=%s">%s</a>' % (x, x),
      'birth_date': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'symptom_ma': lambda x, _, __: '%s' % ( 'Malaria' if x else ''),
      'symptom_pc': lambda x, _, __: '%s' % ( 'Pneumonia' if x else ''),
      'symptom_di': lambda x, _, __: '%s' % ( 'Diarrhea' if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    if sc:
      pass ##cnds[sc]  = ''
    attrs = []
    
    cols    += queries.LOCATION_INFO   
    nat     = orm.ORM.query(primary_table, cnds,
      cols  = [x[0] for x in (cols + attrs) if x[0][0] != '_'],
      
    )
    desc  = 'CCM %s' % (' (%s)' % (self.find_descr(DESCRI + [ (makecol(x[0]) , x[1]) for x in INDICS ], 
						sc) or 'ALL', 
					) )
    return self.dynamised('ccmdash_table', mapping = locals(), *args, **kw)


  #### END OF CCM ###


  #### START OF DEATH ###

  @cherrypy.expose
  def dashboards_deathdash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions('report_date', auth)
    exts = {}
    
    attrs = [(makecol(x[0]), x[1]) for x in queries.DEATH_DATA['attrs']]
    cnds.update({queries.DEATH_DATA['query_str']: ''})
    exts.update(dict([(makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.DEATH_DATA['attrs']]))
    nat = orm.ORM.query(  'rw_deaths', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts,
			);print nat.query

    bylocs_attrs = [(makecol(x[0]), x[1]) for x in queries.DEATH_DATA['bylocs']['attrs']]
    bylocs_cnds = navb.conditions('report_date')
    bylocs_cnds.update({queries.DEATH_DATA['bylocs']['query_str']: ''})
    bylocs_exts = dict([(makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.DEATH_DATA['bylocs']['attrs']])
    bylocs = orm.ORM.query(  'rw_deaths', 
			  bylocs_cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = bylocs_exts,
			)

    return self.dynamised('deathdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_deathdash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [
      ('indexcol',          'Entry ID'),
      ('indangamuntu',            'Mother ID'),
      ('reporter_phone',            'Reporter Phone'),
      ('lmp',            'Date Of Birth'),
      
    ] , *args, **kw)
    DESCRI = []
    DEATHDICT = makedict(queries.DEATH_DATA['attrs'])
    LOCSDICT = makedict(queries.DEATH_DATA['bylocs']['attrs'])
    INDICS = [DEATHDICT[key] for key in DEATHDICT.keys()] + [LOCSDICT[key] for key in LOCSDICT.keys()]
    wcl = []
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions(None, auth)
    cnds.update({"(report_date) >= '%s'" % (navb.start) : ''})
    cnds.update({"(report_date) <= '%s'" % (navb.finish) : ''})
    cnds.update({queries.DEATH_DATA['query_str']: ''})

    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.DEATH_DATA['attrs']]:
     cnds.update({queries.DEATH_DATA['query_str']: ''})
     cnds.update({ DEATHDICT[kw.get('subcat')][0] : ''})
     INDICS = [DEATHDICT[kw.get('subcat')]]

    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.DEATH_DATA['bylocs']['attrs']]:
     cnds.update({queries.DEATH_DATA['bylocs']['query_str']: ''})
     cnds.update({ LOCSDICT[kw.get('subcat')][0] : ''})
     INDICS = [LOCSDICT[kw.get('subcat')]]

    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = {}
      if kw.get('subcat') in [makecol(x[0]) for x in queries.DEATH_DATA['attrs']]: DATADICT = DEATHDICT
      if kw.get('subcat') in [makecol(x[0]) for x in queries.DEATH_DATA['bylocs']['attrs']]: DATADICT = LOCSDICT
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []

     wcl.append({'field_name': '(%s)' % queries.DEATH_DATA['query_str'], 'compare': '', 'value': '', 'extra': True})
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      locateds = summarize_by_location(primary_table = 'rw_deaths', MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						start =  navb.start,
						end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ ( makecol(x[0]), x[1]) for x in INDICS])

    sc      = kw.get('subcat')
    
    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'birth_date': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    if sc:
      pass#cnds[sc]  = ''
    attrs = []
    
    cols    += queries.LOCATION_INFO   
    nat     = orm.ORM.query('rw_deaths', cnds,
      cols  = [x[0] for x in (cols + attrs) if x[0][0] != '_'],
      
    )
    desc  = 'Death %s' % (' (%s)' % (self.find_descr(DESCRI + [ (makecol(x[0]), x[1]) for x in INDICS], 
						sc ) or 'ALL', 
					) )
    return self.dynamised('deathdash_table', mapping = locals(), *args, **kw)


  #### END OF DEATH ###


  @cherrypy.expose
  def tables_patient(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = queries.PATIENT_DETAILS , *args, **kw)
    rattrs = [ (' %s AS %s' % (x[0], x[0].split()[0]), x[1]) for x in queries.RISK['attrs'] ]
    hattrs = [ (' %s AS %s' % (x[0], x[0].split()[0]), x[1]) for x in queries.HIGH_RISK['attrs'] ]
    indexed_attrs = [ ('%s' % get_indexed_value('name', x[2], x[1], x[0], x[3]), x[3]) for x in queries.INDEXED_VALS['location']]
    nat     = orm.ORM.query('rw_pregnancies', cnds,
      				cols  = [x[0] for x in (cols + indexed_attrs + queries.PREGNANCY_DATA + rattrs + hattrs) if x[0][0] != '_'] + ['indexcol'],
				sort = ('report_date', False),
    			)#;print nat.query, cnds
    patient = nat[0]
    pregnancy = [patient]  
    reminders = []
    red_notifications = []
    nutr_notifications = []
    pre_reports = [ x for x in nat.list() ]
    cnds.update({'pregnancy_id = %s' % patient['indexcol']: ''})
    anc_reports = orm.ORM.query('rw_ancvisits', cnds, sort = ('report_date', False) );print anc_reports.query, cnds
    #risk_reports = orm.ORM.query('rw_risks', cnds, sort = ('report_date', False) )
    #red_reports = orm.ORM.query('rw_redalerts', cnds, sort = ('report_date', False) )
    #bir_reports = orm.ORM.query('rw_children', cnds, sort = ('report_date', False) )
    #pnc_reports = orm.ORM.query('rw_pncvisits', cnds, sort = ('report_date', False) )
    return self.dynamised('patient_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_patienthistory(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = queries.PATIENT_DETAILS , *args, **kw)
    data = []
    for key in REPORTS.keys():
     report = REPORTS[key]
     table  = report[1]
     attrs  = FIELDS.get(key).get('attrs')
     reports = orm.ORM.query( table, cnds, cols = [x[0] for x in attrs] , sort = ('report_date', False) )
     data.append( { 'report'  : report, 'attrs': attrs, 'reports' : reports }  
		)#; print reports.query
    #print data
    return self.dynamised('patienthistory', mapping = locals(), *args, **kw)

##### END OF NEW UZD #######

  BABIES_DESCR  = [
    ('boy', 'Male'),
    ('girl', 'Female'),
    ('abnormal_fontanelle', 'Abnormal Fontanelle'),
    ('cord_infection', 'With Cord Infection'),
    ('congenital_malformation', 'With Congenital Malformation'),
    # ('ibirari', 'Bafite Ibibari'),
    ('disabled', 'With Disability'),
    ('stillborn', 'Stillborn'),
    ('no_problem', 'With No Problem')
  ]
  @cherrypy.expose
  def dashboards_babies(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('birth_date', auth)
    attrs   = self.BABIES_DESCR
    nat     = self.civilised_fetch('ig_babies', cnds, attrs)
    total   = nat[0]['total']
    return self.dynamised('babies', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_delivs(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('lmp', auth)
    cnds[("""(lmp + '%d DAYS')""" % (settings.GESTATION, )) + """ >= %s"""] = navb.finish
    attrs   = self.PREGNANCIES_DESCR
    nat     = self.civilised_fetch('ig_pregnancies', cnds, attrs)
    total   = nat[0]['total']
    return self.dynamised('pregnancies', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_admins(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    naddr   = kw.get('addr')
    dadmin  = kw.get('del')
    if dadmin:
      orm.ORM.delete('ig_admins', dadmin)
      raise cherrypy.HTTPRedirect(cherrypy.request.headers.get('Referer') or '/dashboards/admins')
    prv   = kw.get('province')
    dst   = kw.get('district')
    hc    = kw.get('hc')
    if naddr:
      npwd  = kw.get('pwd')
      salt  = str(random.random()).join([str(random.random()) for x in range(settings.SALT_STRENGTH)])
      rslt  = sha.sha('%s%s' % (salt, npwd))
      thing = {'salt': salt, 'address': naddr, 'sha1_pass': rslt.hexdigest(), 'district_pk': dst, 'province_pk': prv, 'health_center_pk': hc}
      orm.ORM.store('ig_admins', thing, migrations  = migrations.ADMIN_MIGRATIONS)
      raise cherrypy.HTTPRedirect(cherrypy.request.headers.get('Referer') or '/dashboards/admins')
    cnds    = navb.conditions(None, auth)
    if not prv:
      cnds['province_pk IS NULL'] = ''
    if not dst:
      cnds['district_pk IS NULL'] = ''
    if not hc:
      cnds['health_center_pk IS NULL'] = ''
    nat     = orm.ORM.query('ig_admins', cnds, sort = ('address', True), migrations = migrations.ADMIN_MIGRATIONS)
    return self.dynamised('admins', mapping = locals(), *args, **kw)

  def civilised_fetch(self, tbl, cnds, attrs):
    exts    = {}
    ncnds   = copy.copy(cnds)
    for ext in attrs:
      if len(ext) > 3:
        for cs in ext[3]:
	  print cs
          ncnds[cs[0]] = cs[1]
      else:
        exts[ext[0]] = ('COUNT(*)' if len(ext) < 3 else ext[2], ext[0])
    return orm.ORM.query(tbl, ncnds, cols = ['COUNT(*) AS total'], extended = exts)

  MOTHERS_DESCR = [
      ('young_mother', 'Under 18'),
      ('old', 'Over 35'),
      ('surgeries', 'With Previous Obstetric Surgery'),
      ('miscarries', 'With Previous Miscarriage'),
      ('prev_home_deliv', 'Previous Home Delivery'),
      ('chronic_disease', 'With Chronic Disease'),
      ('toilet', 'With Toilet'),
      ('no_toilet', 'No Toilet'),
      ('handwashing', 'With Water Tap'),
      ('no_handwashing', 'No Water Tap'),
    ]
  @cherrypy.expose
  def dashboards_mothers(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    pregs   = orm.ORM.query('ig_mothers', cnds, cols = ['(SUM(pregnancies) - COUNT(*)) AS total'])[0]['total']
    attrs   = self.MOTHERS_DESCR
    nat     = self.civilised_fetch('ig_mothers', cnds, attrs)
    total   = nat[0]['total']
    return self.dynamised('mothers', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_pregnancy(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    nat     = orm.ORM.query('pre_table', cnds,
      cols      = ['COUNT(*) AS allpregs'],
      extended  = queries.PREGNANCY_MATCHES,
      migrations  = migrations.PREGNANCY_MIGRATIONS
    )
    toi     = nat.specialise({'to_bool IS NOT NULL':''})
    hnd     = nat.specialise({'hw_bool IS NOT NULL':''})
    weighed = nat.specialise({'mother_height_float > 100.0 AND mother_weight_float > 15.0':''})
    thinq   = weighed.specialise({'(mother_weight_float / ((mother_height_float * mother_height_float) / 10000.0)) < %s': settings.BMI_MIN})
    fatq    = weighed.specialise({'(mother_weight_float / ((mother_height_float * mother_height_float) / 10000.0)) > %s': settings.BMI_MAX})
    riskys  = nat.specialise(queries.RISK_MOD)
    info    = nat[0]
    rez     = orm.ORM.query('res_table',
      cnds,
      cols        = ['COUNT(*) AS allreps'],
    )
    recovs  = rez.specialise({'mw_bool IS NOT NULL':''})
    aarecov = recovs.specialise({'aa_bool IS NOT NULL':''})
    prrecov = recovs.specialise({'pr_bool IS NOT NULL':''})
    total   = nat[0]['allpregs']
    totalf  = float(total)
    toilets = toi[0]['allpregs']
    handw   = hnd[0]['allpregs']
    risks   = riskys[0]['allpregs']
    rezes   = rez[0]['allreps']
    thins   = thinq[0]['allpregs']
    fats    = fatq[0]['allpregs']
    rezf    = float(rezes)
    toilpc  = 0.0
    handpc  = 0.0
    riskpc  = 0.0
    rezpc   = 0.0
    aapc    = 0.0
    prpc    = 0.0
    try:
      toilpc  = (float(toilets) / totalf) * 100.0
      handpc  = (float(handw) / totalf) * 100.0
      riskpc  = (float(risks) / totalf) * 100.0
      rezpc   = (rezf / totalf) * 100.0
    except ZeroDivisionError, zde:
      pass
    aa      = aarecov[0]['allreps']
    pr      = prrecov[0]['allreps']
    if rezf > 0.0:
      aapc  = (float(aa) / rezf) * 100.0
      prpc  = (float(pr) / rezf) * 100.0
    qs    = range(12)
    tot   = 0
    dmax  = 0
    cits  = cnds.items()
    for mpos in qs:
      got = orm.ORM.query('pre_table', dict(cits + [('EXTRACT(MONTH FROM report_date) = %s', mpos + 1)]), cols = ['COUNT(*) AS allpregs'])[0]['allpregs']
      qs[mpos]  = got
      tot       = tot + got
      dmax      = max(dmax, got)
    monthavgs = [{'value' : x, 'pc' : (100.0 * (float(x) / tot)) if tot > 0 else 0, 'rpc': (100.0 * (float(x) / dmax)) if dmax > 0 else 0} for x in qs]
    monthavg  = float(tot) / 12.0
    ls    = range(9)
    tot   = 0
    dmax  = 0
    for mpos in ls:
      got       = orm.ORM.query('pre_table', dict(cits + [('EXTRACT(MONTH FROM lmp) = (EXTRACT(MONTH FROM NOW()) - %s)', len(ls) - (mpos + 1))]), cols = ['COUNT(*) AS allpregs'])[0]['allpregs']
      ls[mpos]  = got
      tot       = tot + got
      dmax      = max(dmax, got)
    tot   = float(tot)
    lmps  = [{'value' : x, 'pc' : (100.0 * (float(x) / tot)) if tot > 0 else 0, 'rpc': (100.0 * (float(x) / dmax)) if dmax > 0 else 0} for x in ls]
    return self.dynamised('pregnancy', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def data_reports(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions('report_date', auth)
    cnds.update({'report_type = %s':kw.get('subcat')})
    cherrypy.response.headers['Content-Type'] = 'application/json'
    reps   = orm.ORM.query('thousanddays_reports', cnds, cols = ['COUNT(*) AS total'])[0]['total']
    return json.dumps({'total': neat_numbers(reps)})


## START MARVIN VIEWS

  @cherrypy.expose
  def dashboards_chw(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions(None, auth)
    navb.gap= timedelta(days = 0)
    cnds.update({ queries.CHW_DATA['query_str'] : ''})
    attrs = [( makecol(x[0]), x[1]) for x in queries.CHW_DATA['attrs'] ]
    exts = {}
    ###REMEMBER TO DOCUMENT THIS TRICK OF BOTH SQL COMMENTS HELPFUL IN NAMING 
    exts.update(dict([( makecol(x[0]), ('COUNT(*)', (x[0] % navb.start) if x[0].__contains__("%s") else x[0] ) ) for x in queries.CHW_DATA['attrs'] ]))
    #print exts,navb.start
    cnds = change_pks_cnds(cnds)
    chws = orm.ORM.query(  'chws_reporter', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts
			)
    return self.dynamised('chw', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_reminder(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions(None, auth)
    navb.gap= timedelta(days = 0)
    cnds.update({"(date) >= '%s'" % (navb.start) : ''})
    cnds.update({"(date) <= '%s'" % (navb.finish) : ''})#;print cnds
    #cnds.update({ queries.REMINDER_DATA['query_str'] : ''})
    attrs = [( makecol(x[0]), x[1]) for x in queries.REMINDER_DATA['attrs'] ]
    exts = {}
    ###REMEMBER TO DOCUMENT THIS TRICK OF BOTH SQL COMMENTS HELPFUL IN NAMING 
    exts.update(dict([( makecol(x[0]), ('COUNT(*)',  x[0] ) ) for x in queries.REMINDER_DATA['attrs'] ]))
    #print exts,navb.start
    cnds = change_pks_cnds(cnds)#;print cnds
    nat = orm.ORM.query(  'ubuzima_reminder', 
			  cnds, 
			  cols = ['COUNT(*) AS total'], 
			  extended = exts
			)#;print "query : %s" %nat.query
    return self.dynamised('reminder', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_reportsdash(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions(None, auth)
    navb.gap= timedelta(days = 0)
    #cnds.update({ queries.REMINDER_DATA['query_str'] : ''})
    attrs = [( makecol(x), REPORTS_LOGS[x][0][0]) for x in REPORTS_LOGS.keys() ];print attrs
    exts = {}
    cnds = change_pks_cnds(cnds)#;print cnds
    data = {}
    for key in attrs:
      try: data[key[0]] = orm.ORM.query( REPORTS_LOGS[key[0].upper()][1][0], cnds, cols = ['COUNT(*) AS total'])[0]['total']
      except: data[key[0]] = 0
    
    return self.dynamised('reportsdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_reportsdash(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [] , *args, **kw)
    sc = kw.get('subcat')
    cols = FIELDS.get(kw.get('subcat').upper())['attrs']
    cnds = change_pks_cnds(cnds)#;print cnds
    DESCRI = []
    markup  = {
      'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'province_pk': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_pk': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_center_pk': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      'sector_pk': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_pk': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_pk': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    nat     = orm.ORM.query(REPORTS_LOGS[kw.get('subcat').upper()][1][0], cnds,
				      cols  = [x[0] for x in cols ],
				      
				    )
    desc  = 'Reports%s' % (' (%s)' % (self.find_descr(DESCRI + [(x[0], x[1]) for x in cols], sc or kw.get('subcat')), 
					) if sc or kw.get('subcat') else '', )
    
    return self.dynamised('reportsdash_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def tables_chw(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [] , *args, **kw)
    cols = [
		('id', 'ID'),                   
		('surname',  'Surname'),               
		('given_name',  'Given Name'),             
		('role_id',  'Role'),                
		('sex',  'Sex'),                    
		('education_level',  'Education Level'),        
		('date_of_birth',  'Date Of Birth'),          
		('join_date',  'Join Date'),              
		('national_id',  'National ID'),            
		('telephone_moh',  'Telephone'),          
		('village_id',  'Village'),             
		('cell_id',  'Cell'),                
		('sector_id',  'Sector'),              
		('health_centre_id',  'Health Center'),       
		#('referral_hospital_id',  'Hospital'),   
		('district_id',  'District'),            
		('province_id',  'Province'),            
		('nation_id',  'Country'),              
		('created',  'Created'),                
		('updated',  'Updated'),                
		('language',  'Language'),               
		('deactivated',  'Deactivated'),            
		('is_active',  'Is Active'),              
		('last_seen',  'Last Seen')    
      
    ]
    DESCRI = []

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
    cnds    = navb.conditions(None, auth)
    cnds.update({ queries.CHW_DATA['query_str'] : ''})

    DICT = replaceindictcol(makedict(queries.CHW_DATA['attrs']), navb.start)
    INDICS = [DICT[key] for key in DICT.keys()]
    #print INDICS, DICT
    wcl = []
    wcl.append({'field_name': '(%s)' % queries.CHW_DATA['query_str'], 'compare': '', 'value': '', 'extra': True})
    
    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.CHW_DATA['attrs']]:
     cnds.update({ DICT[kw.get('subcat')][0] : ''})
     INDICS = [DICT[kw.get('subcat')]]
  
    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = DICT if kw.get('subcat') in [x[0] for x in queries.CHW_DATA['attrs']] else  {}
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []
      
     if kw.get('subcat') is None:
      pass
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      #print INDICS
      locateds = summarize_by_location(primary_table = 'chws_reporter', MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						#start =  navb.start,
						#end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ ( makecol(x[0]), x[1]) for x in INDICS])

    sc      = kw.get('subcat')
    
    markup  = {
      #'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'role_id': lambda x, _, __: '%s' % ("Binome" if x == 2 else 'ASM'),
      'province_id': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_id': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_centre_id': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      #'referral_hospital_id': lambda x, _, __: '%s' % (self.hps.get(str(x)), ),
      'sector_id': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_id': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_id': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    
    
    cnds = change_pks_cnds(cnds)
    nat     = orm.ORM.query('chws_reporter', cnds,
				      cols  = [x[0] for x in cols ],
				      
				    )
    desc  = 'CHWs%s' % (' (%s)' % (self.find_descr(DESCRI + [(makecol(x[0]), x[1]) for x in INDICS], sc or kw.get('group')), 
					) if sc or kw.get('group') else '', )
    return self.dynamised('chw_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def tables_reminder(self, *args, **kw):
    navb, auth, cnds, cols    = self.neater_tables(basics = [] , *args, **kw)
    cols = [
		('id', 'ID'),                   
		('type_id',  'Role'),                
		('village_id',  'Village'),             
		('cell_id',  'Cell'),                
		('sector_id',  'Sector'),              
		('health_centre_id',  'Health Center'),       
		('district_id',  'District'),            
		('province_id',  'Province'),            
		#('nation_id',  'Country'),              
		('date',  'Sent On')    
      
    ]
    DESCRI = []

    DICT = makedict(queries.REMINDER_DATA['attrs'])
    INDICS = [DICT[key] for key in DICT.keys()]
    wcl = []

    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
    cnds    = navb.conditions(None, auth)
    cnds.update({"(date) >= '%s'" % (navb.start) : ''})
    cnds.update({"(date) <= '%s'" % (navb.finish) : ''})
    #cnds.update({ queries.REMINDER_DATA['query_str'] : ''})
    
    if kw.get('subcat') and kw.get('subcat') in [makecol(x[0]) for x in queries.REMINDER_DATA['attrs']]:
     cnds.update({ DICT[kw.get('subcat')][0] : ''})
     INDICS = [DICT[kw.get('subcat')]]

    if kw.get('summary'):
     province = kw.get('province') or auth.him()['province_pk']
     district = kw.get('district') or auth.him()['district_pk']
     location = kw.get('hc') or auth.him()['health_center_pk']
     if kw.get('subcat'):
      DATADICT = DICT if kw.get('subcat') in [x[0] for x in queries.REMINDER_DATA['attrs']] else  {}
      wcl = [
		{'field_name': '(%s)' % DATADICT[kw.get('subcat')][0], 'compare': '', 'value': '', 'extra': True}

		] if DATADICT.get(kw.get('subcat')) else []
     if kw.get('subcat') is None:
      pass
     
     if kw.get('view') == 'table' or kw.get('view') != 'log' :
      #print INDICS, wcl
      locateds = summarize_by_location(primary_table = 'ubuzima_reminder', MANY_INDICS = INDICS, where_clause = wcl, 
						province = province,
						district = district,
						location = location,
						#start =  navb.start,
						#end = navb.finish,
											
						)
      tabular = give_me_table(locateds, MANY_INDICS = INDICS, LOCS = { 'nation': None, 'province': province, 'district': district, 'location': location } )
      INDICS_HEADERS = dict([ ( makecol(x[0]), x[1]) for x in INDICS])

    sc      = kw.get('subcat')

    markup  = {
      #'indangamuntu': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'type_id': lambda x, _, __: '%s' % ( DICT.get('type_id%d'%x)[1] if DICT.get('type_id%d'%x) else ''),
      'province_id': lambda x, _, __: '%s' % (self.provinces.get(str(x)), ),
      'district_id': lambda x, _, __: '%s' % (self.districts.get(str(x)), ),
      'health_centre_id': lambda x, _, __: '%s' % (self.hcs.get(str(x)), ),
      #'referral_hospital_id': lambda x, _, __: '%s' % (self.hps.get(str(x)), ),
      'sector_id': lambda x, _, __: '%s' % (self.sector(str(x))['name'] if self.sector(str(x)) else '', ),
      'cell_id': lambda x, _, __: '%s' % (self.cell(str(x))['name'] if self.cell(str(x)) else '', ),
      'village_id': lambda x, _, __: '%s' % (self.village(str(x))['name'] if self.village(str(x)) else '', ),
    }
    
    
    cnds = change_pks_cnds(cnds)
    nat     = orm.ORM.query('ubuzima_reminder', cnds,
				      cols  = [x[0] for x in cols ],
				      
				    )
    desc  = 'Reminders%s' % (' (%s)' % (self.find_descr(DESCRI + [(makecol(x[0]), x[1]) for x in INDICS], sc or kw.get('subcat')), 
					) if sc or kw.get('subcat') else '', )
    return self.dynamised('reminder_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_chwreg(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions(None, auth)
    navb.gap= timedelta(days = 0)
    cnds.update({ queries.CHW_DATA['query_str'] : ''})
    hc	    = {'id': auth.him()['health_center_pk'] or kw.get('hc'), 'name': self.hcs.get(str(auth.him()['health_center_pk'] or kw.get('hc'))) }
    sectors = self.sectors(auth.him()['district_pk'] or kw.get('district') )
    cnds = change_pks_cnds(cnds)
    roles =  orm.ORM.query(  'chws_role', {}).list()
    nat = orm.ORM.query(  'chws_reporter', 
			  cnds, 
			  cols = ['COUNT(*) AS total']
			)
    ###start checking and register TODO
    error = ""
    success = ""
    nodata = False
    chw = None
    nid = kw.get('nid')
    surname = kw.get('surname')
    given_name = kw.get('given_name')
    sex = kw.get('sex')
    role = kw.get('role')
    edu_level = kw.get('edu_level')
    dob = navb.make_time(kw.get('dob')) if kw.get('dob') else kw.get('dob') 
    djoin = navb.make_time(kw.get('djoin')) if kw.get('djoin') else kw.get('djoin')
    sector = kw.get('sector')
    cell = kw.get('cell')
    telephone_moh = "+25%s" % kw.get('telephone_moh') if kw.get('telephone_moh') else kw.get('telephone_moh')
    health_center = kw.get('health_center')
    village = kw.get('village')
    language = kw.get('language')
    referral = kw.get('referral')
    formdata = [nid, telephone_moh, health_center, referral, village, cell, sector, surname, given_name, sex, role, edu_level, dob, djoin, language]
    for xd in formdata :
     if xd == '' or xd is None:
      nodata = True
      break
     
    if error == "":
     try:
	chw = register_chw(nid, telephone_moh, health_center, referral, village, cell, sector, surname, given_name, sex, role, edu_level, dob, djoin, language)
	success = "%s(%s) Registered" % (chw['surname'], chw['telephone_moh'])
     except Exception, e:
     	orm.ORM.connection();orm.ORM.connection().reset()
     	if nodata == False:	error = e
    
    return self.dynamised('chwreg', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_chwtrail(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    cnds    = navb.conditions('report_date')
    exts = {}

    return self.dynamised('chwtrail', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_chwamb(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
    
    return self.dynamised('chwamb', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_chwstaff(self, *args, **kw):
    auth    = ThousandAuth(cherrypy.session.get('email'))
    navb    = ThousandNavigation(auth, *args, **kw)
    cnds    = navb.conditions(None, auth)
    navb.gap= timedelta(days = 0)
    cnds.update({ queries.STAFF_DATA['query_str'] : ''})
    hc	    = {'id': auth.him()['health_center_pk'] or kw.get('hc'), 'name': self.hcs.get(str(auth.him()['health_center_pk'] or kw.get('hc'))) }
    sectors = self.sectors(auth.him()['district_pk'] or kw.get('district') )
    cnds = change_pks_cnds(cnds)
    roles =  orm.ORM.query(  'chws_role', {}).list()
    nat = orm.ORM.query(  'chws_facilitystaff', 
			  cnds, 
			  cols = ['COUNT(*) AS total']
			)
    ###start checking and register TODO
    error = ""
    success = ""
    nodata = False
    chw = None
    nid = kw.get('nid')
    surname = kw.get('surname')
    given_name = kw.get('given_name')
    sex = kw.get('sex')
    role = kw.get('role')
    edu_level = kw.get('edu_level')
    dob = navb.make_time(kw.get('dob')) if kw.get('dob') else kw.get('dob') 
    djoin = navb.make_time(kw.get('djoin')) if kw.get('djoin') else kw.get('djoin')
    sector = kw.get('sector')
    cell = kw.get('cell')
    telephone_moh = "+25%s" % kw.get('telephone_moh') if kw.get('telephone_moh') else kw.get('telephone_moh')
    health_center = kw.get('health_center')
    village = kw.get('village')
    language = kw.get('language')
    referral = kw.get('referral')
    formdata = [nid, telephone_moh, health_center, referral, village, cell, sector, surname, given_name, sex, role, edu_level, dob, djoin, language]
    for xd in formdata :
     if xd == '' or xd is None:
      nodata = True
      break
     
    if error == "":
     try:
	chw = register_chw(nid, telephone_moh, health_center, referral, village, cell, sector, surname, given_name, sex, role, edu_level, dob, djoin, language)
	success = "%s(%s) Registered" % (chw['surname'], chw['telephone_moh'])
     except Exception, e:
     	orm.ORM.connection();orm.ORM.connection().reset()
     	if nodata == False:	error = e
    
    return self.dynamised('chwstaff', mapping = locals(), *args, **kw)


#### END OF MARVIN VIEWS

