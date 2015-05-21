LOCATION_INFO = [
			('sector_pk',            'Sector'),
			('cell_pk',            'Cell'),
			('village_pk',            'Village'),
		]

PATIENT_DETAILS = [
			('indangamuntu','Patient/Mother ID'),	
			('reporter_phone','Reporter Phone'),
		  ] + LOCATION_INFO

INDEXED_VALS = {'location': [('province_pk', 'id', 'chws_province', 'Province'),
					('district_pk', 'id',  'chws_district', 'District'),
					('health_center_pk', 'id', 'chws_healthcentre', 'HealthCentre'),
					('sector_pk',  'id',   'chws_sector',        'Sector'),
					('cell_pk',     'id',  'chws_cell' ,     'Cell'),
					('village_pk',  'id',  'chws_village'  ,       'Village'),
			     ]
		}

CHW_DATA = {
		'attrs': [
			('role_id = 1', 'ASM'),
			('role_id = 2', 'Binome'),
			("(last_seen + INTERVAL '15 days') > '%s' AND role_id = 1 /*active*/" , 'ACTIVE ASM'),###ADD COMMENT IN SQL TO MAKE ATTRIBUTES DIFF
			("(last_seen + INTERVAL '15 days') > '%s' AND role_id = 2 /*active*/", 'ACTIVE Binome'),
			("((last_seen + INTERVAL '15 days') <= '%s' OR (last_seen IS NULL)) AND role_id = 1 /*inactive*/" , 'INACTIVE ASM'),
			("((last_seen + INTERVAL '15 days') <= '%s'  OR (last_seen IS NULL)) AND role_id = 2 /*inactive*/", 'INACTIVE Binome')				
			],
		'query_str': 'role_id IS NOT NULL'# AND nation_id != 2'
			
		}

NO_RISK = {'attrs': 
			[('prev_pregnancy_gs IS NULL', 'Previous Obstetric Surgery'), 
			 ('prev_pregnancy_mu IS NULL', 'Multiples'),
			 ('prev_pregnancy_hd IS NULL', 'Previous Home Delivery'), 
			 ('prev_pregnancy_rm IS NULL', 'Repetiive Miscarriage'),
			 ('prev_pregnancy_ol IS NULL', 'Old Age (Over 35)'),
			 ('prev_pregnancy_yg IS NULL', 'Young Age (Under 18)'),
			 ('prev_pregnancy_kx IS NULL', 'Previous Convulsion'),
			 ('prev_pregnancy_yj IS NULL', 'Previous Serious Conditions'),
			 ('prev_pregnancy_lz IS NULL', 'Previous Hemorrhaging/Bleeding'),
			 ('symptom_vo IS NULL', 'Vomiting'),
			 ('symptom_pc IS NULL', 'Pneumonia'),
			 ('symptom_oe IS NULL', 'Oedema'),
			 ('symptom_ns IS NULL', 'Neck Stiffness'),
			 ('symptom_ma IS NULL', 'Malaria'),
			 ('symptom_ja IS NULL', 'Jaundice'),
			 ('symptom_fp IS NULL', 'Fraccid Paralysis'),
			 ('symptom_fe IS NULL', 'Fever'),
			 ('symptom_ds IS NULL', 'Chronic Disease'),
			 ('symptom_di IS NULL', 'Diarrhea'),
			 ('symptom_sa IS NULL', 'Severe Anemia'),
			 ('symptom_rb IS NULL', 'Rapid Breathing'),
			 ('symptom_hy IS NULL', 'Hypothermia'),
			 ('symptom_ch IS NULL', 'Coughing'),
			 ('symptom_af IS NULL', 'Abnormal Fontinel'),
			], 
	'query_str': 
		'prev_pregnancy_gs IS NULL AND prev_pregnancy_mu IS NULL AND prev_pregnancy_hd IS NULL AND prev_pregnancy_rm IS NULL AND prev_pregnancy_ol IS NULL AND prev_pregnancy_yg IS NULL AND prev_pregnancy_kx IS NULL AND prev_pregnancy_yj IS NULL AND prev_pregnancy_lz IS NULL AND symptom_vo IS NULL AND symptom_pc IS NULL AND symptom_oe IS NULL AND symptom_ns IS NULL AND symptom_ma IS NULL AND symptom_ja IS NULL AND symptom_fp IS NULL AND symptom_fe IS NULL AND symptom_ds IS NULL AND symptom_di IS NULL AND symptom_sa IS NULL AND symptom_rb IS NULL AND symptom_hy IS NULL AND symptom_ch IS NULL AND symptom_af IS NULL'
		}

RISK = { 'attrs': 
			[('symptom_vo IS NOT NULL', 'Vomiting'),
			 ('symptom_pc IS NOT NULL', 'Pneumonia'),
			 ('symptom_oe IS NOT NULL', 'Oedema'),
			 ('symptom_ns IS NOT NULL', 'Neck Stiffness'),
			 ('symptom_ma IS NOT NULL', 'Malaria'),
			 ('symptom_ja IS NOT NULL', 'Jaundice'),
			 ('symptom_fp IS NOT NULL', 'Fraccid Paralysis'),
			 ('symptom_fe IS NOT NULL', 'Fever'),
			 ('symptom_ds IS NOT NULL', 'Chronic Disease'),
			 ('symptom_di IS NOT NULL', 'Diarrhea'),
			 ('symptom_sa IS NOT NULL', 'Severe Anemia'),
			 ('symptom_rb IS NOT NULL', 'Rapid Breathing'),
			 ('symptom_hy IS NOT NULL', 'Hypothermia'),
			 ('symptom_ch IS NOT NULL', 'Coughing'),
			 ('symptom_af IS NOT NULL', 'Abnormal Fontinel'),
			], 
	'query_str': 
		'(symptom_vo IS NOT NULL OR symptom_pc IS NOT NULL OR symptom_oe IS NOT NULL OR symptom_ns IS NOT NULL OR symptom_ma IS NOT NULL OR symptom_ja IS NOT NULL OR symptom_fp IS NOT NULL OR symptom_fe IS NOT NULL OR symptom_ds IS NOT NULL OR symptom_di IS NOT NULL OR symptom_sa IS NOT NULL OR symptom_rb IS NOT NULL OR symptom_hy IS NOT NULL OR symptom_ch IS NOT NULL OR symptom_af IS NOT NULL) AND NOT (prev_pregnancy_gs IS NOT NULL OR prev_pregnancy_mu IS NOT NULL OR prev_pregnancy_hd IS NOT NULL OR prev_pregnancy_rm IS NOT NULL OR prev_pregnancy_ol IS NOT NULL OR prev_pregnancy_yg IS NOT NULL OR prev_pregnancy_kx IS NOT NULL OR prev_pregnancy_yj IS NOT NULL OR prev_pregnancy_lz IS NOT NULL)'
		}

HIGH_RISK = { 'attrs': 
			[('prev_pregnancy_gs IS NOT NULL', 'Previous Obstetric Surgery'), 
			 ('prev_pregnancy_mu IS NOT NULL', 'Multiples'),
			 ('prev_pregnancy_hd IS NOT NULL', 'Previous Home Delivery'), 
			 ('prev_pregnancy_rm IS NOT NULL', 'Repetitive Miscarriage'),
			 ('prev_pregnancy_ol IS NOT NULL', 'Old Age (Over 35)'),
			 ('prev_pregnancy_yg IS NOT NULL', 'Young Age (Under 18)'),
			 ('prev_pregnancy_kx IS NOT NULL', 'Previous Convulsion'),
			 ('prev_pregnancy_yj IS NOT NULL', 'Previous Serious Conditions'),
			 ('prev_pregnancy_lz IS NOT NULL', 'Previous Hemorrhaging/Bleeding'),
			], 
		'query_str': 
		'prev_pregnancy_gs IS NOT NULL OR prev_pregnancy_mu IS NOT NULL OR prev_pregnancy_hd IS NOT NULL OR prev_pregnancy_rm IS NOT NULL OR prev_pregnancy_ol IS NOT NULL OR prev_pregnancy_yg IS NOT NULL OR prev_pregnancy_kx IS NOT NULL OR prev_pregnancy_yj IS NOT NULL OR prev_pregnancy_lz IS NOT NULL'

	}
PREGNANCY_DATA = [
      ('lmp', 'LMP'),
      ('gravidity', 'Gravidity'),
      ('parity', 'Parity'),
      ('mother_weight', 'Weight'),
      ('mother_height', 'Height'),
      ('report_date', 'Submission Date'),
    ]

ANC_DATA = { 
	'attrs': [
			('anc_visit = 2', 'ANC2'),
			('anc_visit = 3', 'ANC3'),
			('anc_visit = 4', 'ANC4'),
		],

	'query_str': '((anc_visit = 2) OR (anc_visit = 3) OR (anc_visit = 4))'

	}



CBN_DATA = {		
		'nb': ("lower(breastfeeding) = 'nb'", u'Not Breastfeeding'),
		'ebf': ("lower(breastfeeding) = 'ebf'", u'Exclusive Breastfeeding'),
		'cbf': ("lower(breastfeeding) = 'cbf'", u'Complementary Breastfeeding'),
		'bf1':    ("lower(bf1) = 'bf1'", u'Breastfeeding Within 1 hour'),
		'stunting': (u'height_for_age < -2', u'Stunting'),
		'underweight': (u'weight_for_age < -2', u'Underweight'),
		'wasting':     (u'weight_for_height < -2', u'Wasting'),
		'lostweight':('lostweight IS NOT NULL', 'Lost Weight'),
		'falteringweight':('falteringweight IS NOT NULL', 'Faltering Weight'),
		'gainedweight':('gainedweight IS NOT NULL', 'Gained Weight')

		}

MOTHER_NUTR = {		
		'mother_height_less_145': ("mother_height < 145", u'Proportion of pregnant women with height <150cm at 1st ANC'),
		'mother_weight_less_50': ("mother_weight < 50", u'Proportion of pregnant women with weight < 50kg'),
		'bmi_less_18_dot_5': (" bmi < 18.5", u'Proportion of pregnant women with BMI <18.5 at 1st ANC'),
		'lostweight':('lostweight IS NOT NULL', 'Lost Weight'),
		'falteringweight':('falteringweight IS NOT NULL', 'Faltering Weight'),
		'gainedweight':('gainedweight IS NOT NULL', 'Gained Weight')

		}

MOTHER_DATA = [
      ('indangamuntu', 'Mother ID'),
      ('lmp', 'LMP'),
      #('gravidity', 'Gravidity'),
      #('parity', 'Parity'),
      ('mother_weight', 'Weight'),
      ('mother_height', 'Height'),
      ('bmi', 'BMI'),
      ('pregnancy', "Pregnancy"),
    ]


NBC_DATA = {
		'cols' : [
				      ('birth_date', 'Birth Date'),
				      ('report_date', 'Submission Date'),
				    ],

		'NBC': {
			'attrs':[
					('nbc1 != 0', 'NBC1'),
					('nbc2 != 0', 'NBC2'),
					('nbc3 != 0', 'NBC3'),
					('nbc4 != 0', 'NBC4'),
					('nbc5 != 0', 'NBC5')
					]
			},

		'NO_RISK': { 	'attrs': [
						('symptom_sb IS NULL', 'Stillborn'),
						('symptom_af IS NULL', 'Abnormal Fontinel'),
						('symptom_ci IS NULL', 'Cord Infection'),
						('symptom_cm IS NULL', 'Congenital Malformation'),
						("lower(breastfeeding) != 'nb' ", 'Not Breastfeeding'),
						('symptom_ja IS NULL', 'Jaundice'),
						('symptom_rb IS NULL', 'Rapid Breathing'),
						('symptom_ns IS NULL', 'Neck Stiffness'),
						('symptom_hy IS NULL', 'Hypothermia'),
						('symptom_fe IS NULL', 'Fever'),
						('symptom_pm IS NULL', 'Premature'),
					],
				'query_str': "((symptom_sb IS NULL) AND (symptom_af IS NULL) AND (symptom_ci IS NULL) AND (symptom_cm IS NULL) AND (lower(breastfeeding) != 'nb') AND (symptom_ja IS NULL) AND (symptom_rb IS NULL) AND (symptom_ns IS NULL) AND (symptom_hy IS NULL) AND (symptom_fe IS NULL) AND (symptom_pm IS NULL) )"
				},

		'RISK':	{
					'attrs': [
							('symptom_sb IS NOT NULL', 'Stillborn'),
							('symptom_af IS NOT NULL', 'Abnormal Fontinel'),
							('symptom_ci IS NOT NULL', 'Cord Infection'),
							('symptom_cm IS NOT NULL', 'Congenital Malformation'),
							("lower(breastfeeding) = 'nb' ", 'Not Breastfeeding'), ###add in the querying procedures TODO
							('symptom_ja IS NOT NULL', 'Jaundice'),
							],
					'query_str': "((symptom_sb IS NOT NULL) OR (symptom_af IS NOT NULL) OR (symptom_ci IS NOT NULL) OR (symptom_cm IS NOT NULL) OR (lower(breastfeeding) = 'nb') OR (symptom_ja IS NOT NULL)) AND NOT ((symptom_rb IS NOT NULL) OR (symptom_ns IS NOT NULL) OR (symptom_hy IS NOT NULL) OR (symptom_fe IS NOT NULL) OR (symptom_pm IS NOT NULL))"
	
				},
		'HIGH_RISK':	{
					'attrs': [ 
							('symptom_rb IS NOT NULL', 'Rapid Breathing'),
							('symptom_ns IS NOT NULL', 'Neck Stiffness'),
							('symptom_hy IS NOT NULL', 'Hypothermia'),
							('symptom_fe IS NOT NULL', 'Fever'),
							('symptom_pm IS NOT NULL', 'Premature'),							

							],
					'query_str': '((symptom_rb IS NOT NULL) OR (symptom_ns IS NOT NULL) OR (symptom_hy IS NOT NULL) OR (symptom_fe IS NOT NULL) OR (symptom_pm IS NOT NULL))'
				}
		
		}

PNC_DATA = {

		'PNC': {

			'pnc1': ('pnc1 != 0', 'PNC1'),
			'pnc2': ('pnc2 != 0', 'PNC2'),
			'pnc3': ('pnc3 != 0', 'PNC3')

			},
	
		'NO_RISK': {
			   'attrs':	[
						(u'symptom_af IS NULL', u'Abnormal Fontinel'), 
						(u'symptom_ch IS NULL', u'Coughing'), 
						(u'symptom_hy IS NULL', u'Hypothermia'), 
						(u'symptom_rb IS NULL', u'Rapid Breathing'), 
						(u'symptom_sa IS NULL', u'Severe Anemia'),
						(u'symptom_ds IS NULL', u'Chronic Disease'),
						(u'symptom_fe IS NULL', u'Fever'), 
						(u'symptom_fp IS NULL', u'Fraccid Paralysis'),
						(u'symptom_ja IS NULL', u'Jaundice'),
						(u'symptom_ns IS NULL', u'Neck Stiffness'),
						(u'symptom_oe IS NULL', u'Edema'),
						(u'symptom_pc IS NULL', u'Pneumonia'),
						(u'symptom_vo IS NULL', u'Vomiting'),
						(u'symptom_di IS NULL', u'Diarhea'),
						(u'symptom_ma IS NULL', u'Malaria'),
					],

			   'query_str': '((symptom_af IS NULL) AND (symptom_ch IS NULL) AND (symptom_hy IS NULL) AND (symptom_rb IS NULL) AND (symptom_sa IS NULL) AND (symptom_ds IS NULL) AND (symptom_fe IS NULL) AND (symptom_fp IS NULL) AND (symptom_ja IS NULL) AND (symptom_ns IS NULL) AND (symptom_oe IS NULL) AND (symptom_pc IS NULL) AND (symptom_vo IS NULL) AND (symptom_di IS NULL) AND (symptom_ma IS NULL))'
			},

		'RISK': {
			   'attrs':	[
						(u'symptom_af IS NOT NULL', u'Abnormal Fontinel'), 
						(u'symptom_ch IS NOT NULL', u'Coughing'), 
						(u'symptom_hy IS NOT NULL', u'Hypothermia'), 
						(u'symptom_rb IS NOT NULL', u'Rapid Breathing'), 
						(u'symptom_sa IS NOT NULL', u'Severe Anemia'),
						(u'symptom_ds IS NOT NULL', u'Chronic Disease'),
						(u'symptom_fe IS NOT NULL', u'Fever'), 
						(u'symptom_fp IS NOT NULL', u'Fraccid Paralysis'),
						(u'symptom_ja IS NOT NULL', u'Jaundice'),
						(u'symptom_ns IS NOT NULL', u'Neck Stiffness'),
						(u'symptom_oe IS NOT NULL', u'Edema'),
						(u'symptom_pc IS NOT NULL', u'Pneumonia'),
						(u'symptom_vo IS NOT NULL', u'Vomiting'),
						(u'symptom_di IS NOT NULL', u'Diarhea'),
						(u'symptom_ma IS NOT NULL', u'Malaria'),
					],

			   'query_str': '( (symptom_af IS NOT NULL) OR (symptom_ch IS NOT NULL) OR (symptom_hy IS NOT NULL) OR (symptom_rb IS NOT NULL) OR (symptom_sa IS NOT NULL) OR (symptom_ds IS NOT NULL) OR (symptom_fe IS NOT NULL) OR (symptom_fp IS NOT NULL) OR (symptom_ja IS NOT NULL) OR (symptom_ns IS NOT NULL) OR (symptom_oe IS NOT NULL) OR (symptom_pc IS NOT NULL) OR (symptom_vo IS NOT NULL) OR (symptom_di IS NOT NULL) OR (symptom_ma IS NOT NULL) )'

		}
	}


VAC_DATA = {
		'VAC_SERIES': {

				'attrs': [
						(u'vaccine = 1', u'BCG, PO'),
						(u'vaccine = 2', u'P1, Penta1, PCV1, Rota1'),
						(u'vaccine = 3', u'P2, Penta2, PCV2, Rota2'),
						(u'vaccine = 4', u'P3, Penta3, PCV3, Rota3'),
						(u'vaccine = 5', u'Measles1, Rubella'),
						(u'vaccine = 6', u'Measles2'),					
					],
		
				'query_str': '((vaccine = 1) OR (vaccine = 2) OR (vaccine = 3) OR (vaccine = 4) OR (vaccine = 5) OR (vaccine = 6))'
			},

		'VAC_COMPLETION': {

					'attrs': [
							(u"lower(vacc_completion) = 'vc' ", u'Vaccine Complete'),
							(u"lower(vacc_completion) = 'vi' ", u'Vaccine Incomplete'),
							(u"lower(vacc_completion) = 'nv' ", u'Unimmunized Child'),				
						],
			
					'query_str': "((lower(vacc_completion) = 'vc') OR (lower(vacc_completion) = 'vi') OR (lower(vacc_completion) = 'nv'))"
			},



		}

DEATH_DATA = {
		'attrs': [
						(u"lower(death) = 'md'", u'Maternal Death'),
						(u"lower(death) = 'nd'", u'Newborn Death'),
						(u"lower(death) = 'd'", u'Child Death'),
											
					],

		'query_str': "((lower(death) = 'md' ) OR (lower(death) = 'nd') OR (lower(death) = 'cd' ))",

                'bylocs': {
				'attrs': [
						(u"lower(location) = 'hp'", u'At Hospital'),
						(u"lower(location) = 'cl'", u'At Health Centre'),
						(u"lower(location) = 'or'", u'On Route'),
						(u"lower(location) = 'ho'", u'At home'),
											
					],

				'query_str': "((lower(death) = 'md') OR (lower(death) = 'nd') OR (lower(death) = 'cd')) AND ((lower(location) = 'hp') OR (lower(location) = 'cl') OR (lower(location) = 'or') OR (lower(location) = 'ho'))",

				}

		}

CCM_DATA = {
		'attrs': [
						(u'symptom_di IS NOT NULL', u'Diarrhea'),
						(u'symptom_ma IS NOT NULL', u'Malaria'),
						(u'symptom_pc IS NOT NULL', u'Pneumonia'),
											
					],

		'query_str': '(health_status IS NULL) AND ((symptom_di IS NOT NULL) OR (symptom_ma IS NOT NULL) OR (symptom_pc IS NOT NULL))'
		
		}

CMR_DATA = {
		'attrs': [
						(u"lower(intervention_field) = 'pt' ", u'Patient Treated'),
						(u"lower(intervention_field) = 'pr' ", u'Patient Directly Referred'),
						(u"lower(intervention_field) = 'tr' ", u'Patient Referred After Treatment'),
						(u"lower(intervention_field) = 'aa' ", u'Binome Advice'),
											
					],

		'query_str': " (health_status IS NOT NULL) AND ((lower(intervention_field) = 'pt') OR (lower(intervention_field) = 'pr') OR (lower(intervention_field) = 'tr') OR (lower(intervention_field) = 'aa'))"
		
		}

RED_DATA = {

		'attrs': [
				(u'red_symptom_ap IS NOT NULL', u'Acute Abd Pain Early Pregnancy') ,
				(u'red_symptom_co IS NOT NULL', u'Convulsions') ,
				(u'red_symptom_he IS NOT NULL', u'Hemorrhaging/Bleeding') ,
				(u'red_symptom_la IS NOT NULL', u'Mother in Labor at Home') ,
				(u'red_symptom_mc IS NOT NULL', u'Miscarriage') ,
				(u'red_symptom_pa IS NOT NULL', u'Premature Contraction') ,
				(u'red_symptom_ps IS NOT NULL', u'Labour with Previous C-Section') ,
				(u'red_symptom_sc IS NOT NULL', u'Serious Condition but Unknown') ,
				(u'red_symptom_sl IS NOT NULL', u'Stroke during Labor') ,
				(u'red_symptom_un IS NOT NULL', u'Unconscious'), 
			],

		'query_str': '((red_symptom_ap IS NOT NULL) OR  (red_symptom_co IS NOT NULL) OR  (red_symptom_he IS NOT NULL) OR  (red_symptom_la IS NOT NULL) OR  (red_symptom_mc IS NOT NULL) OR  (red_symptom_pa IS NOT NULL) OR  (red_symptom_ps IS NOT NULL) OR  (red_symptom_sc IS NOT NULL) OR  (red_symptom_un IS NOT NULL)) AND ( (intervention_field IS NULL) AND (emergency_date IS NULL) )'

		}

RAR_DATA = {

		'attrs': [
				(u"lower(intervention_field) = 'al'", u'Ambulance Late') ,
				(u"lower(intervention_field) = 'at'", u'Ambulance on Time') ,
				(u"lower(intervention_field) = 'na'", u'No Ambulance Response') ,
				(u"lower(intervention_field) = 'mw'", u'Mother Well(OK)') ,
				(u"lower(intervention_field) = 'ms'", u'Mother Sick') ,
			],

		'query_str': '( (intervention_field IS NOT NULL) AND (emergency_date IS NOT NULL) )'

		}

DELIVERY_DATA = {
		'attrs': [
				(u"lower(location) = 'hp'", u'At Hospital'),
				(u"lower(location) = 'cl'", u'At Clinic'),
				(u"lower(location) = 'or'", u'On Route'),
				(u"lower(location) = 'ho'", u'At home'),
									
			],

		'query_str':"((lower(location) = 'hp') OR (lower(location) = 'cl') OR (lower(location) = 'or') OR (lower(location) = 'ho'))",
		
		}

RED_ALERT_FIELDS    =   [
    ('Patient ID', 'patient_id'),
    ('Reporter', 'reporter_phone')
]

PREGNANCY_MATCHES = {
  'coughing'  : ('COUNT(*)',  'ch_bool IS NOT NULL'),
  'diarrhoea' : ('COUNT(*)',  'di_bool IS NOT NULL'),
  'fever'     : ('COUNT(*)',  'fe_bool IS NOT NULL'),
  'oedema'    : ('COUNT(*)',  'oe_bool IS NOT NULL'),
  'pneumo'    : ('COUNT(*)',  'pc_bool IS NOT NULL'),
  # 'disab'     : ('COUNT(*)',  'db_bool IS NOT NULL'),
  # 'cordi'     : ('COUNT(*)',  'ci_bool IS NOT NULL'),
  'necks'     : ('COUNT(*)',  'ns_bool IS NOT NULL'),
  'malaria'   : ('COUNT(*)',  'ma_bool IS NOT NULL'),
  'vomiting'  : ('COUNT(*)',  'vo_bool IS NOT NULL'),
  # 'stillb'    : ('COUNT(*)',  'sb_bool IS NOT NULL'),
  'jaun'      : ('COUNT(*)',  'ja_bool IS NOT NULL'),
  # 'hypoth'    : ('COUNT(*)',  'hy_bool IS NOT NULL'),
  'anaemia'   : ('COUNT(*)',  'sa_bool IS NOT NULL')
}
