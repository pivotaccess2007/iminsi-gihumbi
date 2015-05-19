#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import os
import sys

DBHOST      = '127.0.0.1'
DBPORT      = 5432
DBNAME      = 'thousanddays'
DBUSER      = 'thousanddays'
DBPASSWORD  = 'thousanddays'

SMPP_IP   = '127.0.0.1'
SMPP_PORT = 13013
SMPP_URL  = 'http://%s:%d/cgi-bin/sendsms' % (SMPP_IP, SMPP_PORT)
SMPP_USERNAME = 'kannel_smpp'
SMPP_PASSWORD = 'kannel_smpp'

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            ''))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))
print PROJECT_PATH, PROJECT_ROOT
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'packages')) 


### VARIABLES FOR NOTIFICATIONS, REMINDERS, ALERTS ... A TUPLE (DESCRIPTION, (SIGN) NUMBER_OF_DAYS) ... SIGN - BEFORE AND + AFTER  ###
### IF NUMBER_OF_DAYS == 0 ... PLEASE NO NEED TO WAIT RESPOND AT THE RECEIPT OF THE INFO ###

GESTATION = 270

DELIVERY_NOTIFICATION = [
                            ('EDD_7DAYS_BEFORE', -7   ),
                            ('EDD_14DAYS_BEFORE', -14 ),
                        ]

ANC_REMINDER = [
                    ('ANC2', -150 ),
                    ('ANC3', -60  ),
                    ('ANC4', -14  ),
                ]

NBC_REMINDER = [
                    ('NBC1', +3  ),
                    ('NBC2', +7  ),
                    ('NBC3', +28 ),
                ]

PNC_REMINDER = [
                    ('PNC1', +3  ),
                    ('PNC2', +28 ),
                    ('PNC3', +42 ),
                ]

VACCINATION_REMINDER = [
                            ('V1', +0   ),
                            ('V2', +42  ),
                            ('V3', +70  ),
                            ('V4', +98  ),
                            ('V5', +270 ),
                            ('V6', +450 ),
                        ]


RESPONSE_REMINDER = [
                        ('RED_RESPONSE',  + (2.0/24) ),
                        ('CCM_RESPONSE',  + 4        ),
                        ('RISK_RESPONSE', + 4       ),
                    ]


IMMEDIATE_ALERT = [
            ('RED_ALERT', 0),
            ('LOW_HEIGHT', 0),
            ('FALTERING_WEIGHT'),
            ('WEIGHT_LOSS', 0),
            ('POOR_WEIGHT', 0),
            ('CMR_ADVICE'),
        ]

PROVIDER_GROUPS = [('CHW', ['chws_reporter', 'telephone_moh']), 
                    ('AMB', ['ambulance_ambulance', 'phonenumber']),
                    ('SUP', ['chws_supervisor', 'telephone_moh']),
                    ('FS', ['chws_facilitystaff', 'telephone_moh']),
                  ]

TRACK_UNIQUES = { 'PREGNANCY': ('indangamuntu', 'lmp'), 'CHILD': ('indangamuntu', 'birth_date', 'child_number' ) }

TRIGGER_TABLES = [ 'pregmessage', 'refmessage', 'ancmessage', 'depmessage', 'riskmessage', 'redmessage',
                    'birmessage', 'childmessage', 'deathmessage', 'resultmessage', 'redresultmessage', 'nbcmessage', 'pncmessage',
                    'ccmmessage', 'cmrmessage', 'cbnmessage', 'mother_track', 'child_track' ]


