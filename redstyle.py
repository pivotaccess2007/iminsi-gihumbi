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

