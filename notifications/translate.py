#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


#### PLEASE USE IT CAREFULLY, MAKE SURE YOU HAVE TABLES REQUIRED IN THE DB FOR A TRANSLATION
from ectomorph import orm
import settings
from pygrowup import helpers, Calculator
from datetime import datetime, timedelta

orm.ORM.connect(host = settings.DBHOST, port = settings.DBPORT, dbname = settings.DBNAME, user = settings.DBUSER, password = settings.DBPASSWORD)


class RecordTrack:
  def __init__(self, tbl):
    self.table    = tbl
    self.attrs    = {}

  def save(self):
    got = orm.ORM.store(self.table, self.attrs)
    return got

  def set(self, key, val):
    self.attrs[key] = val

  def get(self, key):
    return self.attrs[key]

  def __setitem__(self, key, val):
    return self.set(key, val)

  def __getitem__(self, key):
    return self.get(key)

  def copy(self, source, cols):
    for col in cols:
      ncol  = col
      ocol  = col
      if type(col) == type(('', '')):
        ocol  = col[0]
        ncol  = col[1]
      self.set(ncol, source[ocol])
    return self

  def copy_presence(self, source, cols):
    for col in cols:
      ncol  = col
      ocol  = col
      if type(col) == type(('', '')):
        ocol  = col[0]
        ncol  = col[1]
      self.set(ncol, False if (source[ocol] is None) else True)
    return self


class Map:

    def __init__(self, tablename, record):
        self.table = tablename
        self.record     = record
        self.DATA = self.initial_data()

    def initial_data(self):
        who = [
				
                ('indangamuntu', self.record.indangamuntu),
				 
				('reporter_pk', self.record.reporter_pk), 
				('reporter_phone', self.record.reporter_phone),

                ('nation_pk', self.record.nation_pk),
                ('province_pk', self.record.province_pk),
                ('district_pk', self.record.district_pk),
                ('health_center_pk', self.record.health_center_pk),
                ('referral_hospital_pk', self.record.referral_hospital_pk),
                ('sector_pk', self.record.sector_pk),
                ('cell_pk', self.record.cell_pk),
                ('village_pk', self.record.village_pk),				
				('report_date', self.record.report_date)

			]
            
        return who

    def pack(self):
        ''' Process all tracks '''

        self.pregnant()
        self.ancvisit()
        self.delivery()
        self.pncvisit()
        self.nbcvisit()
        self.miscarriage()
        self.death()
        self.ourmother()
        self.ourchild()
        self.ourpregnancy()
        self.motherid()
        self.childid()
        self.pregnancyid()
        self.childgender()
        self.childvaccine()
        self.childnutrition()
        self.result()
        self.intervention()
        self.health_status()
        self.child_nutrition_status()
        self.mother_bmi()

        return True    
    
    def ourchild(self):
        try:   
            chid = orm.ORM.query('rw_children', 
                        { 'indangamuntu = %s': self.record.indangamuntu,'child_number = %s': self.record.child_number, 'birth_date = %s' : self.record.birth_date }
                     )
            self.DATA.append(('child_query', chid.query))
            return chid[0]
        except: return False
        
        return True

    def ourmother(self):
        try:
            moth = orm.ORM.query('rw_mothers', 
                        { 'indangamuntu = %s': self.record.indangamuntu}
                     )
            self.DATA.append(('mother_query', moth.query))
            return moth[0]
        except: return False

        return True

    def ourpregnancy(self):
        try:
            pregnancy = orm.ORM.query('rw_pregnancies', 
                                {'indangamuntu = %s': self.record.indangamuntu, 'lmp >= %s' : self.record.report_date - timedelta(days = settings.GESTATION)},
                                 sort = ('lmp', False)
                                )
            self.DATA.append(('pregnancy_query', pregnancy.query))
            return pregnancy[0]
        except: return False

        return True

    def ourrisk(self):
        try:   
            risk = orm.ORM.query('rw_risks', 
                        { 'mother_id = %s': self.ourmother()['indexcol'],'pregnancy_id = %s': self.ourpregnancy()['indexcol'],
                            'health_status IS NULL': '' , 'intervention_field IS NULL': ''},
                        sort = ('report_date', False)
                     )

            self.DATA.append(('risk_query', risk.query))
            #print "RISK: (\n %s \n)" % risk.query
            self.DATA.append( ('risk', risk[0]['indexcol'] if risk[0] else 0 ) )
            return risk[0]
        except: return False
        
        return True

    def ourres(self):
        try:   
            res = orm.ORM.query('rw_risks', 
                        { 'mother_id = %s': self.ourmother()['indexcol'],'pregnancy_id = %s': self.ourpregnancy()['indexcol'],
                            'health_status IS NOT NULL': '' , 'intervention_field IS NOT NULL': ''},
                        sort = ('report_date', False)
                     )
            
            self.DATA.append(('res_query', res.query))
            self.DATA.append( ('res', res[0]['indexcol'] if res[0] else 0 ) )
            return res[0]
        except: return False
        
        return True

    def ourred(self):
        try:   
            red = orm.ORM.query('rw_redalerts', 
                        { 'mother_id = %s': self.ourmother()['indexcol'],'pregnancy_id = %s': self.ourpregnancy()['indexcol'],
                            'health_status IS NULL': '' , 'intervention_field IS NULL': ''},
                        sort = ('report_date', False)
                     )

            self.DATA.append(('red_query', red.query))
            #print "RISK: (\n %s \n)" % risk.query
            self.DATA.append( ('red', red[0]['indexcol'] if red[0] else 0 ) )
            return red[0]
        except: return False
        
        return True

    def ourrar(self):
        try:   
            rar = orm.ORM.query('rw_redalerts', 
                        { 'mother_id = %s': self.ourmother()['indexcol'],'pregnancy_id = %s': self.ourpregnancy()['indexcol'],
                            'health_status IS NOT NULL': '' , 'intervention_field IS NOT NULL': ''},
                        sort = ('report_date', False)
                     )
            
            self.DATA.append(('rar_query', rar.query))
            self.DATA.append( ('rar', rar[0]['indexcol'] if rar[0] else 0 ) )
            return rar[0]
        except: return False
        
        return True

    def ourccm(self):
        try:   
            ccm = orm.ORM.query('rw_ccms', 
                        { 'mother_id = %s': self.ourmother()['indexcol'],'pregnancy_id = %s': self.ourpregnancy()['indexcol'],
                            'health_status IS NULL': '' , 'intervention_field IS NULL': ''},
                        sort = ('report_date', False)
                     )

            self.DATA.append(('ccm_query', ccm.query))
            #print "RISK: (\n %s \n)" % risk.query
            self.DATA.append( ('ccm', ccm[0]['indexcol'] if ccm[0] else 0 ) )
            return ccm[0]
        except: return False
        
        return True

    def ourcmr(self):
        try:   
            cmr = orm.ORM.query('rw_ccms', 
                        { 'mother_id = %s': self.ourmother()['indexcol'],'pregnancy_id = %s': self.ourpregnancy()['indexcol'],
                            'health_status IS NOT NULL': '' , 'intervention_field IS NOT NULL': ''},
                        sort = ('report_date', False)
                     )
            
            self.DATA.append(('cmr_query', cmr.query))
            self.DATA.append( ('cmr', cmr[0]['indexcol'] if cmr[0] else 0 ) )
            return cmr[0]
        except: return False
        
        return True

    def motherid(self):
        self.DATA.append( ('mother', self.ourmother()['indexcol'] if self.ourmother() else 0 ) )
        return True

    def childid(self):
        self.DATA.append( ('child', self.ourchild()['indexcol'] if self.ourchild() else 0 ) )
        return True

    def pregnancyid(self):
        if self.ourchild(): self.DATA.append( ('pregnancy', self.ourchild()['pregnancy_id']) )
        else:   self.DATA.append( ('pregnancy', self.ourpregnancy()['indexcol'] if self.ourpregnancy() else 0) )
        return True

    def childgender(self):
        self.DATA.append( ('gender', 'M' if self.ourchild() and self.ourchild()['gender'] else 'F') )
        return True

    def pregnant(self):
        if self.table == 'pregmessage':
            self.DATA.append( ('lmp', self.record.lmp))
            self.DATA.append( ('anc2_date', self.record.anc2_date))

        return True
        
    def ancvisit(self):
        if self.table == 'ancmessage':
            self.DATA.append( ('anc%s' % self.record.anc_visit, self.record.indexcol))
        return True

    def delivery(self):
        if self.table == 'birmessage':
            self.DATA.append( ('birth', self.record.indexcol) )
            self.DATA.append( ('delivery', self.record.indexcol) )
        if hasattr(self.record, 'birth_date'):
            self.DATA.append( ('delivery_date', self.record.birth_date) )
            self.DATA.append( ('birth_date', self.record.birth_date) )
        if hasattr(self.record, 'child_number'):    self.DATA.append( ('child_number', self.record.child_number) )
        return True

    def pncvisit(self):
        if self.table == 'pncmessage':
            self.DATA.append( ('pnc%s' % self.record.pnc_visit, self.record.indexcol))
        return True

    def nbcvisit(self):
        if self.table == 'nbcmessage':
            self.DATA.append( ('nbc%s' % self.record.nbc_visit, self.record.indexcol))
        return True

    def childvaccine(self):
        if self.table == 'childmessage':
            self.DATA.append( ('v%s' % self.record.vaccine, self.record.indexcol))
        return True
    
    def childnutrition(self):
        ''' Try Get All nutritions details for the baby '''
        
        if hasattr(self.record, 'child_weight'): self.DATA.append( ('child_weight', self.record.child_weight))
        if hasattr(self.record, 'child_height'): self.DATA.append( ('child_height', self.record.child_height))
        if hasattr(self.record, 'muac'): self.DATA.append( ('muac', self.record.muac))
        try: self.DATA.append( ('premature', self.ourchild()['symptom_pm']))
        except: pass
        if hasattr(self.record, 'breastfeeding'): self.DATA.append( ('breastfeeding', self.record.breastfeeding))
        if hasattr(self.record, 'birth_date'):
            if self.table == 'birmessage':
                self.DATA.append( ('age_in_months', 0) )
                self.DATA.append( ('bf1', self.record.breastfeeding))
            else: self.DATA.append( ('age_in_months', helpers.date_to_age_in_months( self.record.birth_date.date() ) ) )

        return True

    def miscarriage(self):
        if self.table == 'redmessage_red_symptom':
            if self.record.value.lower() == 'mc': self.DATA.append( ('miscarriage', self.record.principal))
        return True

    def death(self):
        if self.table == 'deathmessage':
            if self.record.death.lower() == 'md': self.DATA.append( ('mdeath', self.record.indexcol))
            if self.record.death.lower() == 'nd': self.DATA.append( ('ndeath', self.record.indexcol))
            if self.record.death.lower() == 'cd': self.DATA.append( ('cdeath', self.record.indexcol))
        return True

    def result(self):
        if self.table == 'ccmmessage': self.DATA.append( ('ccm', self.record.indexcol) )
        if self.table == 'cmrmessage':
            self.DATA.append( ('ccm', self.ourccm()['indexcol'] ) )
            self.DATA.append( ('cmr', self.ourcmr()['indexcol']) )
        if self.table == 'redmessage': self.DATA.append( ('red', self.record.indexcol) )
        if self.table == 'redresultmessage':
            self.DATA.append( ('red', self.ourred()['indexcol'] ) )
            self.DATA.append( ('rar', self.ourrar()['indexcol']) )
        if self.table == 'riskmessage': self.DATA.append( ('risk', self.ourrisk()['indexcol'] ) )
        if self.table == 'resultmessage':
            self.DATA.append( ('risk', self.ourrisk()['indexcol'] ) )
            self.DATA.append( ('res', self.ourres()['indexcol']) )
        return True

    def intervention(self):
        if hasattr(self.record, 'intervention_field'):    self.DATA.append( ('intervention', self.record.intervention_field) )
        return True

    def health_status(self):
        if hasattr(self.record, 'health_status'):
            if self.ourchild(): self.DATA.append( ('status', "CW" if self.record.health_status else "CS") )
            else: self.DATA.append( ('status', "MW" if self.record.health_status else "MS") )
        return True

    def mother_bmi(self):
        if hasattr(self.record, 'mother_weight'):
            self.DATA.append( ('mother_weight', self.record.mother_weight))
            try:
                new_value = float(self.record.mother_weight)
                old_value = float(self.ourpregnancy()['mother_weight'])
                if new_value < old_value:
                    self.DATA.append(('lostweight', True))
                    self.DATA.append( ('gainedweight', False))
                if new_value == old_value:
                    self.DATA.append( ('falteringweight', True))
                    self.DATA.append(('lostweight', False))
                    self.DATA.append( ('gainedweight', False))
            except Exception, e: pass
            
        if hasattr(self.record, 'mother_height'):   self.DATA.append( ('mother_height', self.record.mother_height))
        if hasattr(self.record, 'mother_weight') and hasattr(self.record, 'mother_height'):
            self.DATA.append( ('bmi', (self.record.mother_weight * 10000) / (self.record.mother_height  * self.record.mother_height) ))
        return True

    def child_nutrition_status(self):
        try:
            
            data = dict(self.DATA)
            valid_gender = helpers.get_good_sex( data.get('gender') )
            valid_age = helpers.date_to_age_in_months(data.get('birth_date').date())
            cg = Calculator(adjust_height_data=False, adjust_weight_scores=False)

            try:
                            
                new_value = float(self.record.child_weight)
                old_value = float(self.ourchild()['child_weight'])
                if self.table != 'birmessage':
                    if new_value < old_value:
                        self.DATA.append(('lostweight', True))
                        self.DATA.append( ('gainedweight', False))
                    if new_value > old_value:
                        self.DATA.append(('lostweight', False))
                        self.DATA.append( ('gainedweight', True))
                    if new_value == old_value:
                        self.DATA.append( ('falteringweight', True))
                        self.DATA.append(('lostweight', False))
                        self.DATA.append( ('gainedweight', False))

                wfa = cg.zscore_for_measurement('wfa', data.get('child_weight'), valid_age, valid_gender)
                self.DATA.append( ('weight_for_age', float(wfa)))
            except Exception, e: pass
            try: 
                hfa = cg.zscore_for_measurement('hfa', data.get('child_height') , valid_age, valid_gender)
                self.DATA.append( ('height_for_age', float(hfa) ))
            except Exception, e: pass
            try:
                
                wfh = cg.zscore_for_measurement('wfh', data.get('child_weight'), valid_age, valid_gender, data.get('child_height'))
                self.DATA.append( ('weight_for_height', float(wfh) ))
            except Exception, e: pass
        except: return False 

        return True

class Translate(RecordTrack):

  def verify_new_values(self, got, data):
    for x in data:
        new_value = x[1]
        old_value = got[ x[0] ]
        if x[0] in ['lostweight', 'gainedweight', 'falteringweight']: continue
        if new_value == 0 or None: self[ x[0] ] = old_value  
        else: self[ x[0] ] = new_value
        if x[0] in ['mother_weight', 'child_weight']:
            if new_value < old_value:
                self['lostweight'] = True
                self['gainedweight'] = False
            if new_value > old_value:
                self.DATA.append(('lostweight', False))
                self.DATA.append( ('gainedweight', True))
            if new_value == old_value:
                self['falteringweight'] = True
                self['lostweight'] = False
                self['gainedweight'] = False
                #print old_value, new_value, self['lostweight'], data
    
    return self

  def translate(self, uniques, data):
    uniques_d = {}
    self.copy(dict(data), [x[0] for x in data])
    for x in uniques: uniques_d.update( { x + ' = %s': dict(data).get(x)} )
    #print self.table, self.attrs, uniques_d
    gat = orm.ORM.query(self.table, uniques_d, migrations = data)
    #print gat.query
    if gat.count():
      self.verify_new_values(gat[0], data)    
    if not gat.count():
      self.save()
      return self.translate(uniques, data)
    self['indexcol']    = gat[0]['indexcol']
    self.save()
    return self

    

    
