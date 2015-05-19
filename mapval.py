#!  /usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab


def fans( sms_report = [] ):
 ans = {}
 for sms in sms_report: ans.update({sms.keyword: (sms.title_en, sms.title_rw)})
 return ans

def get_attrs():
  ans = set()
  for x in FIELDS.keys():
    if FIELDS.get(x).get('attrs'):
      for an in FIELDS.get(x).get('attrs'): ans.add(an)
  return ans

def get_symptoms():
  ans = set()
  for x in FIELDS.keys():
    if FIELDS.get(x).get('symptoms'):
      for an in FIELDS.get(x).get('symptoms'): ans.add(an)
  return ans

def get_previous_symptoms():
  ans = set()
  for x in FIELDS.keys():
    if FIELDS.get(x).get('previous_symptoms'):
      for an in FIELDS.get(x).get('previous_symptoms'): ans.add(an)
  return ans

def read_record_row(row, orm):
  ans = []
  try:
    nat = orm.ORM.query(row.query.tablenm, {'indexcol=%s': row['indexcol']}, cols = ["*"])[0]
    for x in get_attrs():
      try:  ans.append("%s=%s" % (x[1], nat[x[0]]) )
      except KeyError,e:  continue
    
    for y in get_symptoms().union(get_previous_symptoms()):
      try:
        for k in nat.query.cols.keys():
          d = nat[k]
          if str(d).lower() == str(y[0]).lower(): ans.append("%s" % y[1] )
      except KeyError,e:  continue

  except Exception, e:
    print e;pass
  return ans

def fields(fs = [], ans = {}):
 fans = {}
 for an in ans.keys(): fans.update({an: []})
 for ff in fs:
  d = fans.get(ff.sms_report.keyword)#; print d
  key = ff.key
  ## muac, date_of_birth, date_of_emergency, af, db
  ##if key in ['mother_weight', 'mother_height', 'child_weight', 'child_height', 'child_number', 'gravidity', 'parity']: key = '%s' % key
  ##else:	key = '%s' % key 
  ##if key == 'gravidity': key = 'gravity' 
  if key == 'nid':
   dd = ('indangamuntu', ff.title_en, ff.title_rw)
   d.append(dd)
   d.append(('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama"))
   d.append(('report_date', 'Submission Date', "Itariki yatanzweho"))   
  else:
    dd = (key, ff.title_en, ff.title_rw)
    d.append(dd)
  fans.update({ff.sms_report.keyword: d })
 
 return fans
 
#FIELDS = fields(fs = sms_report_fields, fans = fans(sms_reports))

REPORTS = {
            'PRE' : ((u'Pregnancy', u'Ugusama'), 'pregmessage') ,
            'DTH' : ((u'Death', u'Urupfu'), 'deathmessage') ,
            'RISK' : ((u'Risk', u'Ibibazo mpuruza'), 'riskmessage') ,
            'ANC' : ((u'AntenatalConsultation', u'Ukwipimisha'), 'ancmessage') ,
            #'DEP' : ((u'Departure', u'Ukwimuka'), 'depmessage') ,
            'RES' : ((u'RiskResult', u'Igisubizo ku bibazo mpuruza'), 'resultmessage') ,
            'CBN' : ((u'CommunityBasedNutrition', u'Imirire') , 'cbnmessage'),
            #'CCM' : ((u'CommunityCaseManagement', u'Ukuvura abana'), 'ccmmessage' ) ,
            'RAR' : ((u'RedAlertResult', u'Igisubizo ku bibazo simusiga') , 'redresultmessage'),
            #'REF' : ((u'Refusal', u'Ukwanga') , 'refmessage'),
            'CHI' : ((u'ChildHealth', u'Ugukingira') , 'childmessage'),
            'NBC' : ((u'NewbornCare', u"Isurwa ry'uruhinja") , 'nbcmessage'),
            'PNC' : ((u'PostnatalCare', u"Isurwa ry'umubyeyi") , 'pncmessage'),
            'BIR' : ((u'Birth', u'Ukuvuka') , 'birmessage'),
            #'CMR' : ((u'CaseManagementResponse', u"Iherezo ry'uburwayi") , 'cmrmessage'),
            'RED' : ((u'RedAlert', u'Ibibazo simusiga'), 'redmessage') 
        }


FIELDS = {
          'PRE' : { 'attrs':
                     [
	                   ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                      ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama"),
                      ('report_date', 'Submission Date', "Itariki yatanzweho"), 
                      #(u'mother_phone', u"Mother's Telephone", u"Telephoni y'umubyeyi") ,
                      (u'lmp', u'Last Menstrual Period', u"Itariki ya nyuma y'imihango"),
                      (u'parity', u'Parity', u"Umubare w'imbyaro") ,
                      ('gravidity', u'Gravidity', u'Inshuro yasamye') ,
                      #(u'anc2_date', u'Second ANC Appointment Date', u'Itariki yo gusubira kwipimisha') ,
                      (u'mother_height', u'Mother Height', u"Uburebure bw'umubyeyi") ,
                      (u'mother_weight', u'Mother Weight', u"Ibiro by'umubyeyi")

                    ],
        
                  'symptoms':
  
               [(u'nh', u'Has no Handwashing', u'Ntafite Kandagira Ukarabe') ,
                      (u'nt', u'Has no Toilet', u'Ntafite ubwiherero') ,
                      (u'hw', u'Has Handwashing', u'Afite Kandagira Ukarabe') ,
                      (u'to', u'Has Toilet', u'Afite ubwiherero') ,
                      (u'cl', u'At Clinic Facility', u'Ku Kigo nderabuzima/Ivuriri') ,
                      (u'hp', u'At hospital facility', u'Ku bitaro') ,
                      (u'af', u'Abnormal Fontinel', u'Igihorihori kibyimbye/gitebeye') ,
                      (u'ch', u'Coughing', u'Inkorora') ,
                      (u'hy', u'Hypothermia', u'Ubukonje bukabije') ,
                      (u'rb', u'Rapid Breathing', u'Guhumeka vuba') ,
                      (u'sa', u'Severe Anemia', u'Kubura amaraso') ,
                      (u'ds', u'Chronic disease', u'indwara idakira') ,
                      (u'fe', u'Fever', u'umuriro ukabije') ,
                      (u'fp', u'Fraccid paralysis', u'Uburema bushya') ,
                      (u'ja', u'Jaundice', u'Umubiri wabaye umuhondo') ,
                      (u'ns', u'Neck Stiffness', u'Yagagaye iosi') ,
                      (u'oe', u'Edema', u'Kubyimbagana') ,
                      (u'pc', u'Pneumonia', u'Umusonga') ,
                      (u'vo', u'Vomiting', u'Kuruka') ,
                      (u'di', u'Diarhea', u'Impiswi') ,
                      (u'ma', u'Malaria', u'Malariya') ,
                      (u'np', u'No Problem', u'Ntakibazo')],


                    'previous_symptoms':

                     [   (u'lz', u'Previous Hemorrhaging/Bleeding', u'Yigeze kuva amaraso') ,
                        (u'yj', u'Previous Serious Conditions', u'Yigeze agira ikibazo gikomeye kidasobanutse') ,
                        (u'kx', u'Previous Convulsion', u'Yigeze kugagara') ,
                        (u'yg', u'Young Age(Under 18)', u'Yasamye atarageza ku myaka 18') ,
                        (u'ol', u'Old Age(Over 35)', u'Yasamye arengeje imyaka 35') ,
                        (u'rm', u'Repetitive Miscarriage', u'Yakuyemo inda') ,
                        (u'hd', u'Previous Home Delivery', u'Yigeze kubyarira mu rugo') ,
                        (u'mu', u'Multiples', u'Atwite abana barenze umwe') ,
                        (u'gs', u'Previous Obstetric Surgery', u'Yigeze kubagwa abyara') ,
                        (u'nr', u'No Previous Risk', u'Ntakibazo yagize ku nda yabanje')
                      ]

                  }
                      
                ,
          'DTH' : { 'attrs': [ 
	          
                            ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                            ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                            ('report_date', 'Submission Date', "Itariki yatanzweho"),
                            (u'child_number', u'Child number', u"Nimero y'umwana") ,
                            (u'birth_date', u'Date of Birth', u"Itariki y'amavuko")
                      ],

                    'symptoms':
 
                    [
                        (u'ho', u'At Home', u'Mu rugo') ,
                        (u'or', u'On Route', u'Mu nzira') ,
                        (u'cl', u'At Clinic Facility', u'Ku Kigo nderabuzima/Ivuriri') ,
                        (u'hp', u'At hospital facility', u'Ku bitaro') ,
                        (u'md', u'Maternal death', u"Urupfu rw'umubyeyi") ,
                        (u'nd', u'Newborn death', u"Urupfu rw'uruhinja") ,
                        (u'cd', u'Child death', u"Urupfu rw'umwana") 
                    ]
                },

            'RISK' : { 'attrs':
                        [
                          ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                          ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                          ('report_date', 'Submission Date', "Itariki yatanzweho"),
                          (u'mother_weight', u'Mother Weight', u"Ibiro by'umubyeyi")
                        ],

                      'symptoms':
                      [
                        (u'af', u'Abnormal Fontinel', u'Igihorihori kibyimbye/gitebeye') ,
                        (u'ch', u'Coughing', u'Inkorora') ,
                        (u'hy', u'Hypothermia', u'Ubukonje bukabije') ,
                        (u'rb', u'Rapid Breathing', u'Guhumeka vuba') ,
                        (u'sa', u'Severe Anemia', u'Kubura amaraso') ,
                        (u'ds', u'Chronic disease', u'indwara idakira') ,
                        (u'fe', u'Fever', u'umuriro ukabije') ,
                        (u'fp', u'Fraccid paralysis', u'Uburema bushya') ,
                        (u'ja', u'Jaundice', u'Umubiri wabaye umuhondo') ,
                        (u'ns', u'Neck Stiffness', u'Yagagaye iosi') ,
                        (u'oe', u'Edema', u'Kubyimbagana') ,
                        (u'pc', u'Pneumonia', u'Umusonga') ,
                        (u'vo', u'Vomiting', u'Kuruka') ,
                        (u'di', u'Diarhea', u'Impiswi') ,
                        (u'ma', u'Malaria', u'Malariya') ,
                        (u'ho', u'At Home', u'Mu rugo') ,
                        (u'or', u'On Route', u'Mu nzira') ,
                        (u'cl', u'At Clinic Facility', u'Ku Kigo nderabuzima/Ivuriri') ,
                        (u'hp', u'At hospital facility', u'Ku bitaro')
                      ]
                    },

              'ANC' : { 'attrs':
	                      [
                          ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                          ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                          ('report_date', 'Submission Date', "Itariki yatanzweho"),
                          (u'anc_date', u'Date of ANC', u'Itariki yisuzumirishejeho') ,
                          (u'mother_weight', u'Mother Weight', u"Ibiro by'umubyeyi")
                        ],
                  
                      'symptoms':
                      [
                        (u'anc2', u'Second ANC', u'Yipimishije inshuro ya 2') ,
                        (u'anc3', u'Third ANC', u'Yipimishije inshuro ya 3') ,
                        (u'anc4', u'Fourth ANC', u'Yipimishije inshuro ya 4') ,
                        #(u'af', u'Abnormal Fontinel', u'Igihorihori kibyimbye/gitebeye') ,
                        (u'ch', u'Coughing', u'Inkorora') ,
                        (u'hy', u'Hypothermia', u'Ubukonje bukabije') ,
                        (u'rb', u'Rapid Breathing', u'Guhumeka vuba') ,
                        (u'sa', u'Severe Anemia', u'Kubura amaraso') ,
                        (u'ds', u'Chronic disease', u'indwara idakira') ,
                        (u'fe', u'Fever', u'umuriro ukabije') ,
                        (u'fp', u'Fraccid paralysis', u'Uburema bushya') ,
                        (u'ja', u'Jaundice', u'Umubiri wabaye umuhondo') ,
                        (u'ns', u'Neck Stiffness', u'Yagagaye iosi') ,
                        (u'oe', u'Edema', u'Kubyimbagana') ,
                        (u'pc', u'Pneumonia', u'Umusonga') ,
                        (u'vo', u'Vomiting', u'Kuruka') ,
                        (u'di', u'Diarhea', u'Impiswi') ,
                        (u'ma', u'Malaria', u'Malariya') ,
                        (u'np', u'No Problem', u'Ntakibazo') ,
                        (u'cl', u'At Clinic Facility', u'Ku Kigo nderabuzima/Ivuriri') ,
                        (u'hp', u'At hospital facility', u'Ku bitaro')

                      ]
                      
                   },

              'DEP' : { 'attrs':
	                        [
                            ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                            ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                            ('report_date', 'Submission Date', "Itariki yatanzweho"),
                            (u'child_number', u'Child number', u"Nimero y'umwana") ,
                            (u'birth_date', u'Date of Birth', u"Itariki y'amavuko")
                          ]
                   },

              'RES' : { 'attrs':
                          [
	              
                            ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                            ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                            ('report_date', 'Submission Date', "Itariki yatanzweho")
                          ],
                        
                      'symptoms': 
                        [              
                          (u'af', u'Abnormal Fontinel', u'Igihorihori kibyimbye/gitebeye') ,
                          (u'ch', u'Coughing', u'Inkorora') ,
                          (u'hy', u'Hypothermia', u'Ubukonje bukabije') ,
                          (u'rb', u'Rapid Breathing', u'Guhumeka vuba') ,
                          (u'sa', u'Severe Anemia', u'Kubura amaraso') ,
                          (u'ds', u'Chronic disease', u'indwara idakira') ,
                          (u'fe', u'Fever', u'umuriro ukabije') ,
                          (u'fp', u'Fraccid paralysis', u'Uburema bushya') ,
                          (u'ja', u'Jaundice', u'Umubiri wabaye umuhondo') ,
                          (u'ns', u'Neck Stiffness', u'Yagagaye iosi') ,
                          (u'oe', u'Edema', u'Kubyimbagana') ,
                          (u'pc', u'Pneumonia', u'Umusonga') ,
                          (u'vo', u'Vomiting', u'Kuruka') ,
                          (u'di', u'Diarhea', u'Impiswi') ,
                          (u'ma', u'Malaria', u'Malariya') ,
                          (u'ho', u'At Home', u'Mu rugo') ,
                          (u'or', u'On Route', u'Mu nzira') ,
                          (u'cl', u'At Clinic Facility', u'Ku Kigo nderabuzima/Ivuriri') ,
                          (u'hp', u'At hospital facility', u'Ku bitaro') ,
                          (u'aa', u'ASM Advice', u"Inama y'umujyanama") ,
                          (u'pr', u'Patient Directly Referred', u'Yahise yoherezwa kwa muganga ako kanya') ,
                          (u'mw', u'Mother Well', u'Umubyeyi ameze neza') ,
                          (u'ms', u'Mother Sick', u'Umubyeyi ararwaye')
                         ]
            
                        },

              'BIR' :  { 'attrs':
                          [

                            ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                            ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                            ('report_date', 'Submission Date', "Itariki yatanzweho"),
                            (u'child_number', u'Child number', u"Nimero y'umwana") ,
                            (u'birth_date', u'Date of Birth', u"Itariki y'amavuko") ,
                            (u'child_weight', u'Child Weight', u"Ibiro by'umwana")
                          ],

                         'symptoms':
                        [
                            (u'bo', u'Male', u'Umuhungu') ,
                            (u'gi', u'Female', u'Umukobwa') ,
                            (u'sb', u'Stillborn', u'Umwana avutse apfuye') ,
                            (u'rb', u'Rapid Breathing', u'Guhumeka vuba') ,
                            (u'af', u'Abnormal Fontinel', u'Igihorihori kibyimbye/gitebeye') ,
                            (u'ci', u'Cord Infection', u"Ukwandura k'urureri") ,
                            (u'cm', u'Congenital Malformation', u'Kuvukana ubumuga') ,
                            (u'ib', u'Cleft Palate/Lip', u'Ibibari') ,
                            (u'db', u'Children Living With Disability', u"Abana n'ubumuga") ,
                            (u'pm', u'Premature', u'Umwana yavutse adashyitse') ,
                            (u'np', u'No Problem', u'Ntakibazo') ,
                            (u'ho', u'At Home', u'Mu rugo') ,
                            (u'or', u'On Route', u'Mu nzira') ,
                            (u'cl', u'At Clinic Facility', u'Ku Kigo nderabuzima/Ivuriri') ,
                            (u'hp', u'At hospital facility', u'Ku bitaro') ,
                            (u'bf1', u'Breastfeeding within 1 Hour of Birth', u'Konsa mu isaha ya mbere akivuka') ,
                            (u'nb', u'Not Breastfeeding', u'Ntiyonka')
                          ]
                      },

              'CBN' :  { 'attrs':
	                        [
                            ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                            ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                            ('report_date', 'Submission Date', "Itariki yatanzweho"),
                            (u'child_number', u'Child number', u"Nimero y'umwana") ,
                            (u'birth_date', u'Date of Birth', u"Itariki y'amavuko") ,
                            (u'child_height', u'Child Height', u"Uburebure bw'umwana") ,
                            (u'child_weight', u'Child Weight', u"Ibiro by'umwana") ,
                            (u'muac', u'MUAC', u'Ibipimo bya MUAC')
                          ],

                        'symptoms':
                        [
                          (u'ebf', u'Exclusive Breastfeeding', u'Aronka gusa') ,
                          (u'nb', u'Not Breastfeeding', u'Ntiyonka') ,
                          (u'cbf', u'Complementary Breastfeeding', u'Inyunganirabere')
                          ]
                      },

                'CCM' :  { 'attrs':
                            [
                              ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                              ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                              ('report_date', 'Submission Date', "Itariki yatanzweho"),
                              (u'child_number', u'Child number', u"Nimero y'umwana") ,
                              (u'birth_date', u'Date of Birth', u"Itariki y'amavuko") ,
                              (u'muac', u'MUAC', u'Ibipimo bya MUAC')
                             ],

                        'symptoms':
                          [
                            (u'pc', u'Pneumonia', u'Umusonga') ,
                            (u'di', u'Diarhea', u'Impiswi') ,
                            (u'ma', u'Malaria', u'Malariya') ,
                            (u'ib', u'Cleft Palate/Lip', u'Ibibari') ,
                            (u'db', u'Children Living With Disability', u"Abana n'ubumuga") ,
                            (u'nv', u'Unimmunized Child', u'Ntiyigeze akingirwa') ,
                            (u'oi', u'Other Infection', u'Indi ndwara') ,
                            (u'np', u'No Problem', u'Ntakibazo') ,
                            (u'aa', u'ASM Advice', u"Inama y'umujyanama") ,
                            (u'pr', u'Patient Directly Referred', u'Yahise yoherezwa kwa muganga ako kanya') ,
                            (u'pt', u'Patient Treated', u'Yavuwe') ,
                            (u'tr', u'Patient Referred After Treatment', u'Yoherejwe ku ivuriro nyuma yo kuvurwa')
                          ]
                          
                        },

                'RAR' :   { 'attrs':
	                          [
                              ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                              ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                              ('report_date', 'Submission Date', "Itariki yatanzweho"),
                              (u'emergency_date', u'Date of Emergency', u'Itariki yagiriye ibibazo') 
                              ],

                          'symptoms':
                            [
                              (u'ap', u'Acute Abd Pain Early Pregnancy', u'Ububare butunguranye bukabije') ,
                              (u'co', u'Convulsions', u'Kugagara') ,
                              (u'he', u'Hemorrhaging/Bleeding', u'Kuva amaraso') ,
                              (u'la', u'Mother in labor at home', u'atangiye ibise ari mu rugo') ,
                              (u'mc', u'Miscarriage', u'Gukuramo inda') ,
                              (u'pa', u'Premature Contraction', u'Kujya ku bise inda itarageza igihe') ,
                              (u'ps', u'Labour with Previous C-Section', u'Kujya ku nda yarabazwe abyara') ,
                              (u'sc', u'Serious Condition but Unknown', u'Ikibazo gikomeye kidasobanutse') ,
                              (u'sl', u'Stroke during Labor', u'Paralize') ,
                              (u'un', u'Unconscious', u'Guta ubwenge') ,
                              (u'ho', u'At Home', u'Mu rugo') ,
                              (u'or', u'On Route', u'Mu nzira') ,
                              (u'cl', u'At Clinic Facility', u'Ku Kigo nderabuzima/Ivuriri') ,
                              (u'hp', u'At hospital facility', u'Ku bitaro') ,
                              (u'al', u'Ambulance Late', u'Ambilansi yatinze') ,
                              (u'at', u'Ambulance on Time', u'Ambilansi yahageze ku gihe') ,
                              (u'na', u'No Ambulance Response', u'Ambilansi ntiyaje') ,
                              (u'mw', u'Mother Well', u'Umubyeyi ameze neza') ,
                              (u'ms', u'Mother Sick', u'Umubyeyi ararwaye')
                             ]
                        },

                'CHI' :   { 'attrs':
	                          [
                              ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                              ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                              ('report_date', 'Submission Date', "Itariki yatanzweho"),
                              (u'child_number', u'Child number', u"Nimero y'umwana") ,
                              (u'birth_date', u'Date of Birth', u"Itariki y'amavuko") ,
                              (u'child_weight', u'Child Weight', u"Ibiro by'umwana") ,
                              (u'muac', u'MUAC', u'Ibipimo bya MUAC')
                             ],
                          
                            'symptoms':
                              [
                                (u'v1', u'BCG, PO', u'BCG, PO') ,
                                (u'v2', u'P1, Penta1, PCV1, Rota1', u'P1, Penta1, PCV1, Rota1') ,
                                (u'v3', u'P2, Penta2, PCV2, Rota2', u'P2, Penta2, PCV2, Rota2') ,
                                (u'v4', u'P3, Penta3, PCV3, Rota3', u'P3, Penta3, PCV3, Rota3') ,
                                (u'v5', u'Measles1, Rubella', u'Iseru1, Rubewole') ,
                                (u'v6', u'Measles2', u'Iseru2') ,
                                (u'vc', u'Vaccine Complete', u'Yarangije inkingo zose ziteganijwe') ,
                                (u'vi', u'Vaccine Incomplete', u'Ntiyarangije inkingo zose ziteganijwe') ,
                                (u'nv', u'Unimmunized Child', u'Ntiyigeze akingirwa') ,
                                (u'sb', u'Stillborn', u'Umwana avutse apfuye') ,
                                (u'rb', u'Rapid Breathing', u'Guhumeka vuba') ,
                                (u'af', u'Abnormal Fontinel', u'Igihorihori kibyimbye/gitebeye') ,
                                (u'ci', u'Cord Infection', u"Ukwandura k'urureri") ,
                                (u'cm', u'Congenital Malformation', u'Kuvukana ubumuga') ,
                                (u'ib', u'Cleft Palate/Lip', u'Ibibari') ,
                                (u'db', u'Children Living With Disability', u"Abana n'ubumuga") ,
                                (u'pm', u'Premature', u'Umwana yavutse adashyitse') ,
                                (u'np', u'No Problem', u'Ntakibazo') ,
                                (u'ho', u'At Home', u'Mu rugo') ,
                                (u'or', u'On Route', u'Mu nzira') ,
                                (u'cl', u'At Clinic Facility', u'Ku Kigo nderabuzima/Ivuriri') ,
                                (u'hp', u'At hospital facility', u'Ku bitaro')
                               ]
                                                  
                        },

                  'NBC' :  { 'attrs':
	                            [
                                ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                                ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                                ('report_date', 'Submission Date', "Itariki yatanzweho"),
                                (u'child_number', u'Child number', u"Nimero y'umwana") ,
                                (u'birth_date', u'Date of Birth', u"Itariki y'amavuko")
                               ], 
                            
                          'symptoms':
                            [
                              (u'nbc1', u'First NBC', u'Gusura uruhinja bwa mbere mu rugo') ,
                              (u'nbc2', u'Second NBC', u'Gusura uruhinja bwa kabiri mu rugo') ,
                              (u'nbc3', u'Third NBC', u'Gusura uruhinja bwa gatatu mu rugo') ,
                              (u'nbc4', u'Fourth NBC', u'Gusura uruhinja bwa kane mu rugo') ,
                              (u'nbc5', u'Fifth NBC', u'Gusura uruhinja bwa gatanu mu rugo') ,
                              (u'sb', u'Stillborn', u'Umwana avutse apfuye') ,
                              (u'rb', u'Rapid Breathing', u'Guhumeka vuba') ,
                              (u'af', u'Abnormal Fontinel', u'Igihorihori kibyimbye/gitebeye') ,
                              (u'ci', u'Cord Infection', u"Ukwandura k'urureri") ,
                              (u'cm', u'Congenital Malformation', u'Kuvukana ubumuga') ,
                              (u'ib', u'Cleft Palate/Lip', u'Ibibari') ,
                              (u'db', u'Children Living With Disability', u"Abana n'ubumuga") ,
                              (u'pm', u'Premature', u'Umwana yavutse adashyitse') ,
                              (u'np', u'No Problem', u'Ntakibazo') ,
                              (u'ebf', u'Exclusive Breastfeeding', u'Aronka gusa') ,
                              (u'nb', u'Not Breastfeeding', u'Ntiyonka') ,
                              (u'cbf', u'Complementary Breastfeeding', u'Inyunganirabere') ,
                              (u'aa', u'ASM Advice', u"Inama y'umujyanama") ,
                              (u'pr', u'Patient Directly Referred', u'Yahise yoherezwa kwa muganga ako kanya') ,
                              (u'cw', u'Child well(OK)', u'umwana ameze neza') ,
                              (u'cs', u'Child sick', u'Umwana ararwaye')
                             ]
                         
                          },

                    'PNC' :   { 'attrs':
	                            [
                                ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                                ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                                ('report_date', 'Submission Date', "Itariki yatanzweho"),
                                (u'birth_date', u'Date of Birth', u"Itariki y'amavuko") 
                                
                                ],
                          
                            'symptoms':
                              [
                                (u'pnc1', u'First PNC', u'Gusura umubyeyi wabyaye bwa mbere mu rugo') ,
                                (u'pnc2', u'Second PNC', u'Gusura umubyeyi wabyaye bwa kabiri mu rugo') ,
                                (u'pnc3', u'Third PNC', u'Gusura umubyeyi wabyaye bwa gatatu mu rugo') ,
                                (u'af', u'Abnormal Fontinel', u'Igihorihori kibyimbye/gitebeye') ,
                                (u'ch', u'Coughing', u'Inkorora') ,
                                (u'hy', u'Hypothermia', u'Ubukonje bukabije') ,
                                (u'rb', u'Rapid Breathing', u'Guhumeka vuba') ,
                                (u'sa', u'Severe Anemia', u'Kubura amaraso') ,
                                (u'ds', u'Chronic disease', u'indwara idakira') ,
                                (u'fe', u'Fever', u'umuriro ukabije') ,
                                (u'fp', u'Fraccid paralysis', u'Uburema bushya') ,
                                (u'ja', u'Jaundice', u'Umubiri wabaye umuhondo') ,
                                (u'ns', u'Neck Stiffness', u'Yagagaye iosi') ,
                                (u'oe', u'Edema', u'Kubyimbagana') ,
                                (u'pc', u'Pneumonia', u'Umusonga') ,
                                (u'vo', u'Vomiting', u'Kuruka') ,
                                (u'di', u'Diarhea', u'Impiswi') ,
                                (u'ma', u'Malaria', u'Malariya') ,
                                (u'np', u'No Problem', u'Ntakibazo') ,
                                (u'aa', u'ASM Advice', u"Inama y'umujyanama") ,
                                (u'pr', u'Patient Directly Referred', u'Yahise yoherezwa kwa muganga ako kanya') ,
                                (u'mw', u'Mother Well', u'Umubyeyi ameze neza') ,
                                (u'ms', u'Mother Sick', u'Umubyeyi ararwaye')
                              ]

                             },

                        'REF' :   { 'attrs':
	                                  [
                                      ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                                      ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama"),
                                      ('report_date', 'Submission Date', "Itariki yatanzweho")
                                     ]
                                  },

                          'CMR' :   { 'attrs':
	                                    [
                                        ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                                        ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                                        ('report_date', 'Submission Date', "Itariki yatanzweho"),
                                        (u'child_number', u'Child number', u"Nimero y'umwana") ,
                                        (u'birth_date', u'Date of Birth', u"Itariki y'amavuko") 
                                     ],
                                  
                                    'symptoms':
                                      [
                                        
                                      (u'pc', u'Pneumonia', u'Umusonga') ,
                                      (u'di', u'Diarhea', u'Impiswi') ,
                                      (u'ma', u'Malaria', u'Malariya') ,
                                      (u'ib', u'Cleft Palate/Lip', u'Ibibari') ,
                                      (u'db', u'Children Living With Disability', u"Abana n'ubumuga") ,
                                      (u'nv', u'Unimmunized Child', u'Ntiyigeze akingirwa') ,
                                      (u'oi', u'Other Infection', u'Indi ndwara') ,
                                      (u'np', u'No Problem', u'Ntakibazo') ,
                                      (u'aa', u'ASM Advice', u"Inama y'umujyanama") ,
                                      (u'pr', u'Patient Directly Referred', u'Yahise yoherezwa kwa muganga ako kanya') ,
                                      (u'pt', u'Patient Treated', u'Yavuwe') ,
                                      (u'tr', u'Patient Referred After Treatment', u'Yoherejwe ku ivuriro nyuma yo kuvurwa') ,
                                      (u'cw', u'Child well(OK)', u'umwana ameze neza') ,
                                      (u'cs', u'Child sick', u'Umwana ararwaye')
                                    ]
                                  
                                  },

                            'RED' :  { 'attrs':
	                                    [
                                        ('indangamuntu', u'National Identifier', u"Numero y'irangamuntu y'umubyeyi") ,
                                        ('reporter_phone', 'Reporter Telephone', "Telefoni y'Umujyanama") ,
                                        ('report_date', 'Submission Date', "Itariki yatanzweho")
                                        ],
                                    
                                      'symptoms':
                                        [
                                          
                                      (u'ap', u'Acute Abd Pain Early Pregnancy', u'Ububare butunguranye bukabije') ,
                                      (u'co', u'Convulsions', u'Kugagara') ,
                                      (u'he', u'Hemorrhaging/Bleeding', u'Kuva amaraso') ,
                                      (u'la', u'Mother in labor at home', u'atangiye ibise ari mu rugo') ,
                                      (u'mc', u'Miscarriage', u'Gukuramo inda') ,
                                      (u'pa', u'Premature Contraction', u'Kujya ku bise inda itarageza igihe') ,
                                      (u'ps', u'Labour with Previous C-Section', u'Kujya ku nda yarabazwe abyara') ,
                                      (u'sc', u'Serious Condition but Unknown', u'Ikibazo gikomeye kidasobanutse') ,
                                      (u'sl', u'Stroke during Labor', u'Paralize') ,
                                      (u'un', u'Unconscious', u'Guta ubwenge') ,
                                      (u'ho', u'At Home', u'Mu rugo') ,
                                      (u'or', u'On Route', u'Mu nzira')
                                    ]

                                }
                  }



