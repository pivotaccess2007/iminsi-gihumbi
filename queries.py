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
		("(last_seen + INTERVAL '15 days') > '%s' AND role_id = 1 /*activeasm*/" , 'ACTIVE ASM'),###ADD COMMENT IN SQL TO MAKE ATTRIBUTES DIFF
		("(last_seen + INTERVAL '15 days') > '%s' AND role_id = 2 /*activebinome*/", 'ACTIVE Binome'),
		("((last_seen + INTERVAL '15 days') <= '%s' OR (last_seen IS NULL)) AND role_id = 1 /*inactiveasm*/" , 'INACTIVE ASM'),
		("((last_seen + INTERVAL '15 days') <= '%s'  OR (last_seen IS NULL)) AND role_id = 2 /*inactivebinome*/", 'INACTIVE Binome')				
		],
	'query_str': 'role_id IS NOT NULL'# AND nation_id != 2'
			
		}

STAFF_DATA = {
	'attrs': [
			("service = 'Chief of Ambulance Drivers'", 'Chief of Ambulance Drivers'),
			("service = 'Chief of Emergency'", 'Chief of Emergency'),
			("service = 'Chief of Supervisors'", 'Chief of Supervisors'),
			("service = 'Chief of Maternity'", 'Chief of Maternity'),
			("service = 'Chief of Nursing'", 'Chief of Nursing'),
			("service = 'Chief of Medical Staff'", 'Chief of Medical Staff'),
			("service = 'Supervisor'", 'Supervisor'),
			("service = 'Data Manager'", 'Data Manager'),
			("service = 'Monitor Evaluator'", 'Monitor Evaluator'),
			("service = 'Hospital Director'", 'Hospital Director')				
		],
	'query_str': 'service IS NOT NULL'# AND nation_id != 2'
			
		}

REMINDER_DATA = {
			'attrs': [
					('type_id = 1', '2nd ANC Visit'),
					('type_id = 2', '3rd ANC Visit'),
					('type_id =  3', '4th ANC Visit'),
					('type_id = 4', 'Two Weeks Before Expected Delivery Date'),
					('type_id = 5', 'Week Before Expected Delivery Date'),
					('type_id = 6', 'Inactive Reporter'),
					('type_id = 7', 'Due Date '),
					('type_id = 8', 'Week After Due Date'),
					('type_id = 9', 'PNC visit after 2 days of Delivery Date'),
					('type_id = 10', 'PNC visit after 6 days of Delivery Date'),
					('type_id = 11', 'PNC visit after 28 days of Delivery Date'),
					('type_id = 13', 'Child Health after 6 months of Delivery Date'),
					('type_id = 14', 'Child Health after 9 months of Delivery Date'),
					('type_id = 15', 'Child Health after 18 months of Delivery Date'),
					('type_id = 16', 'Child Health after 24 months of Delivery Date'),
					('type_id = 17', 'Active Reporter Feedback'),
					('type_id = 18', 'Inactive Reporter Feedback'),
					('type_id = 19', 'Red Alert Result'),
					('type_id = 20', 'Risk Result'),
					('type_id = 21', 'Case Management Response')
					],
			 'query_str': ''
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
      ('bmi', 'BMI'),
      ('report_date', 'Submission Date'),
    ]

ANC_DATA = { 
	'attrs': [
			('anc_visit = 2', 'ANC2'),
			('anc_visit = 3', 'ANC3'),
			('anc_visit = 4', 'ANC4'),
			('anc_visit = 2 AND (lmp + INTERVAL \'150 days\') <= anc_date', 'Standard ANC2'),
			('anc_visit = 3 AND (lmp + INTERVAL \'180 days\') <= anc_date', 'Standard ANC3'),
			('anc_visit = 4 AND (lmp + INTERVAL \'270 days\') <= anc_date', 'Standard ANC4')
		],

	'query_str': '((anc_visit = 2) OR (anc_visit = 3) OR (anc_visit = 4))'

	}



CBN_DATA = {		
		'nb': ("lower(breastfeeding) = 'nb'", u'Not Breastfeeding'),
		'ebf': ("lower(breastfeeding) = 'ebf'", u'Exclusive Breastfeeding'),
		'cbf': ("lower(breastfeeding) = 'cbf'", u'Complementary Breastfeeding'),
		'bf1':    ("lower(bf1) = 'bf1'", u'Breastfeeding Within 1 hour'),
		#'stunting': (u'height_for_age < -2', u'Stunting'),
		'underweight': (u'weight_for_age < -2', u'Underweight'),
		#'wasting':     (u'weight_for_height < -2', u'Wasting'),
		#'lostweight':('lostweight IS NOT NULL', 'Lost Weight'),
		#'falteringweight':('falteringweight IS NOT NULL', 'Faltering Weight'),
		#'gainedweight':('gainedweight IS NOT NULL', 'Gained Weight')
		'lostweight':('lostweight', 'Lost Weight'),
		'falteringweight':('falteringweight', 'Faltering Weight'),
		'gainedweight':('gainedweight', 'Gained Weight'),
		'muacred': ('muac < 11.5', 'MUAC < 11.5 cm'),
		'muacyellow': ('muac >= 11.5 AND muac < 12.5', 'MUAC 11.5 - 12.5 cm'),
		'muacgreen': ('muac > 12.5', 'MUAC > 12.5 cm'),

		}

MOTHER_NUTR = {		
		'mother_height_less_145': ("mother_height < 145", u'Proportion of pregnant women with height <150cm at 1st ANC'),
		'mother_weight_less_50': ("mother_weight < 50", u'Proportion of pregnant women with weight < 50kg'),
		'bmi_less_18_dot_5': (" bmi < 18.5", u'Proportion of pregnant women with BMI <18.5 at 1st ANC'),
		#'lostweight':('lostweight IS NOT NULL', 'Lost Weight'),
		#'falteringweight':('falteringweight IS NOT NULL', 'Faltering Weight'),
		#'gainedweight':('gainedweight IS NOT NULL', 'Gained Weight')
		'lostweight':('lostweight', 'Lost Weight'),
		'falteringweight':('falteringweight', 'Faltering Weight'),
		'gainedweight':('gainedweight', 'Gained Weight'),
		'mmuacred': ('muac < 18.5', 'MUAC < 18.5 cm'),
		'mmuacyellow': ('muac >= 18.5 AND muac < 21.0', 'MUAC 18.5 - 21.0 cm'),
		'mmuacgreen': ('muac > 21.0', 'MUAC > 21.0 cm'),

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
			'pnc3': ('pnc3 != 0', 'PNC3'),
			'pnc4': ('pnc4 != 0', 'PNC4'),
			'pnc5': ('pnc5 != 0', 'PNC5')

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
						(u"lower(death) = 'cd'", u'Child Death'),
											
					],

		'query_str': "((lower(death) = 'md' ) OR (lower(death) = 'nd') OR (lower(death) = 'cd' ))",
		
		'attr_bylocs': {
				"lowerdeathmd": {'attrs': [
						(u"lower(location) = 'hp' AND lower(death) = 'md'", u'At Hospital'),
						(u"(lower(location) = 'cl' OR lower(location) = 'hc') AND lower(death) = 'md'", u'At Health Centre'),
						(u"lower(location) = 'or' AND lower(death) = 'md'", u'En Route'),
						(u"lower(location) = 'ho' AND lower(death) = 'md'", u'At home'),
					
					],

				'query_str': "( lower(death) = 'md') AND ((lower(location) = 'hp') OR (lower(location) = 'cl'  OR lower(location) = 'hc') OR (lower(location) = 'or') OR (lower(location) = 'ho'))",
					},

				"lowerdeathnd": {'attrs': [
						(u"lower(location) = 'hp' AND lower(death) = 'nd'", u'At Hospital'),
						(u"(lower(location) = 'cl' OR lower(location) = 'hc') AND lower(death) = 'nd'", u'At Health Centre'),
						(u"lower(location) = 'or' AND lower(death) = 'nd'", u'En Route'),
						(u"lower(location) = 'ho' AND lower(death) = 'nd'", u'At home'),
					
					],

				'query_str': " (lower(death) = 'nd') AND ((lower(location) = 'hp') OR (lower(location) = 'cl'  OR lower(location) = 'hc') OR (lower(location) = 'or') OR (lower(location) = 'ho'))",
					},

				"lowerdeathcd": {'attrs': [
						(u"lower(location) = 'hp' AND lower(death) = 'cd'", u'At Hospital'),
						(u"(lower(location) = 'cl' OR lower(location) = 'hc') AND lower(death) = 'cd'", u'At Health Centre'),
						(u"lower(location) = 'or' AND lower(death) = 'cd'", u'En Route'),
						(u"lower(location) = 'ho' AND lower(death) = 'cd'", u'At home'),
					
					],

				'query_str': " (lower(death) = 'cd') AND ((lower(location) = 'hp') OR (lower(location) = 'cl'  OR lower(location) = 'hc') OR (lower(location) = 'or') OR (lower(location) = 'ho'))",
					}
				
				},

                'bylocs': {
				'attrs': [
						(u"lower(location) = 'hp'", u'At Hospital'),
						(u"lower(location) = 'cl' OR lower(location) = 'hc'", u'At Health Centre'),
						(u"lower(location) = 'or'", u'En Route'),
						(u"lower(location) = 'ho'", u'At home'),
											
					],

				'query_str': "((lower(death) = 'md') OR (lower(death) = 'nd') OR (lower(death) = 'cd')) AND ((lower(location) = 'hp') OR (lower(location) = 'cl'  OR lower(location) = 'hc') OR (lower(location) = 'or') OR (lower(location) = 'ho'))",

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
				( u'red_symptom_shp IS NOT NULL', u'Severe headache and/or blurry vision' ), 
				 ( u'red_symptom_bsp IS NOT NULL', u'Bad/foul smelling vaginal discharge' ), 
				 ( u'red_symptom_wu IS NOT NULL', u'Weak or unconscious or unresponsive to touch' ), 
				 ( u'red_symptom_hbt IS NOT NULL', u'High body temperature' ), 
				 ( u'red_symptom_lbt IS NOT NULL', u'Low body temperature or cold' ), 
				 ( u'red_symptom_fb IS NOT NULL', u'Fast or dicult breathing' ), 
				 ( u'red_symptom_cdg IS NOT NULL', u'Chest in-drawing or gasping' ), 
				 ( u'red_symptom_cop IS NOT NULL', u'Convulsions or is unconscious' ), 
				 ( u'red_symptom_hfp IS NOT NULL', u'High fever' ), 
				 ( u'red_symptom_con IS NOT NULL', u'Convulsion or fit' ), 
				 ( u'red_symptom_sbp IS NOT NULL', u'Sever bleeding' ), 
				 ( u'red_symptom_nuf IS NOT NULL', u'Not able to feed since birth/stopped feeding well' ), 
				 ( u'red_symptom_ucb IS NOT NULL', u'Umbilical cord bleeding' ), 
				 ( u'red_symptom_iuc IS NOT NULL', u'Infected umbilical cord' ), 
				 ( u'red_symptom_rv IS NOT NULL', u'Repeated Vomiting ' ), 
				 ( u'red_symptom_ads IS NOT NULL', u'Abdominal distension and stool arrest' ), 
				 ( u'red_symptom_nsc IS NOT NULL', u'Non stop crying' ), 
				 ( u'red_symptom_nbf IS NOT NULL', u'Bulging fontanel ' ), 
				 ( u'red_symptom_nhe IS NOT NULL', u'Hemorrhage ' ), 
				 ( u'red_symptom_ys IS NOT NULL', u'Yellow soles' ), 
				 ( u'red_symptom_sp IS NOT NULL', u'Skin pustules' ),  
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
				(u"lower(location) = 'cl'", u'At Health Centre'),
				(u"lower(location) = 'or'", u'En Route'),
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
