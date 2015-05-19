#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

MySQL_DATABASE 	= 'rapidsmsrw'
MySQL_USER 		  = 'root'
MySQL_PASSWORD	= '123'
MySQL_HOST		  = '127.0.0.1'
MySQL_PORT		  = 3306

REPORT_TYPE = { "ANC": 1, "BIR": 2, "CMR": 6, "CHI": 5, "CBN": 3, "CCM": 4, "DTH": 7, "DEP": 16, "NBC": 8, "PNC": 9, "PRE": 10, "RED": 12, "RAR": 11, "REF": 15, "RISK": 14, "RES": 13 }

TABLES = { "sms": "ubuzima_report", "fields": "ubuzima_report", "field_type" : "ubuzima_fieldtype", "chws": "chws_reporter" }

DATA = {"last": 10000000000000, "wrong" : []}







