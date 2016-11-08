
from api.messaging.handlers.smshandler import *
identity = '+250788660270'
text = 'RED 1234567890123457 AP CO HE LA MC PA PS SC SL UN OR wt55.5'
SMSReportHandler.test(text, identity)
#text = 'pre 1234567890123456 21.11.2014 05.02.2015 02 01 nr np hp wt55.5 ht145 nt hw'
#text = 'pre+1234567890123457+21.11.2014+05.02.2015+02+01+nr+np+hp+wt55.5+ht145+nt+hw'
text = 'pre 1234567890123451 21.10.2014 05.02.2015 02 01 GS MU HD RM OL YG KX YJ LZ PC OE NS MA JA FP FE DS DI SA RB NP HY CH AF cl wt55.5 ht145 to hw'
#text = 'pre+1234567890123456+21.11.2014+05.02.2015+02+01+gs+mu+hd+rm+ol+yg+kx+yj+lz+pc+oe+ns+ma+ja+fp+fe+ds+di+sa+rb+hy+ch+af+cl+wt55.5+ht145+to+hw'
text  = 'ANC+1234567890123451+05.01.2015+anc2+VO+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+cl+wt65.5'
text  = 'ANC 1234567890123456 05.01.2015 anc2 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF cl wt65.5'
text  = 'ANC+1234567890123456+06.01.2015+anc3+np+hp+wt66.5'
text  = 'ANC 1234567890123456 06.01.2015 anc3 np hp wt66.5'
text  = 'ANC+1234567890123456+06.01.2015+anc4+np+hp+wt70.5'
text  = 'ANC 1234567890123456 06.01.2015 anc4 np hp wt70.5'

text  = 'RISK 1234567890123456 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF ho wt70'
#text  = 'RISK+1234567890123456+VO+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+ho+wt70'
text  = 'RISK 1234567890123457 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF or wt70'
#text  = 'RISK+1234567890123457+VO+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+or+wt70'

text  = 'RES 1234567890123456 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF hp AA MW'
#text  = 'RES+1234567890123456+VO+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+hp+AA+MW'
text  = 'RES 1234567890123457 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF cl PR MS'
#text  = 'RES+1234567890123457+VO+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+cl+PR+MS'

text  = 'BIR 1234567890123454 01 09.01.2015 BO SB RB AF CI CM IB DB PM hp NB wt2.5'
#text  = 'BIR+1234567890123456+01+09.01.2015+GI+SB+RB+AF+CI+CM+IB+DB+PM+cl+BF1+wt2.8'

text = 'NBC 1234567890123451 01 NBC1 09.01.2015 SB RB AF CI CM FE HY JA NS IB DB PM NB PR CS'
#text = 'NBC+1234567890123456+01+NBC1+09.01.2015+NP+EBF+AA+CW'
#text = 'NBC+1234567890123456+01+NBC1+09.01.2015+NP+CBF+AA+CW'

text = 'PNC 1234567890123451 PNC1 09.01.2015 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF PR MW'
#text = 'PNC+1234567890123456+PNC2+09.01.2015+NP+AA+CW'
#text = 'PNC+1234567890123456+PNC3+09.01.2015+NP+AA+CW'

text = 'CCM 1234567890123451 01 09.01.2015 PC MA DI OI IB DB PR MUAC5.2'
text = 'CCM+1003565890123456+02+13.03.2015+PC+MA+DI+OI+IB+DB+PR+MUAC5.2'
curl -s -D/dev/stdout 'http://41.74.172.34:5000/backend/kannel-smpp/?id=%2B250788660270&text=CCM+1003565890123456+02+13.03.2015+PC+MA+DI+OI+IB+DB+PR+MUAC5.2'
#text = 'CMR 1234567890123451 01 09.01.2015 PC MA DI OI IB DB PR CW'

text = 'CBN 1234567890123456 01 09.01.2015 EBF HT40 WT4.1 MUAC4.6'
#text = 'CBN 1234567890123456 01 09.01.2015 CBF HT40 WT4.1 MUAC4.6'

#text = 'DTH 1234567890123456 01 09.01.2015 HO ND'
text = 'DTH 1234567890123456 HO MD'

text = 'CHI 1234567890123451 01 09.01.2015 V2 VI IB DB HO WT4.5 MUAC5.4'


text  = 'REF 0234567890123457'
#text  = 'DEP 1234567890123457 01 09.01.2015'
#text  = 'DEP 1234567890123457'

text = 'RED 1234567890123451 AP CO HE LA MC PA PS SC SL UN OR wt55.5'

text = 'RAR 1234567890123451 13.01.2015 AP CO HE LA MC PA PS SC SL UN HO AL MW'

sms_report = SMSReport.objects.filter(keyword = text.split()[0].upper())[0]
chw = Reporter.objects.get(telephone_moh = identity)
p = get_sms_report_parts(sms_report, text, DEFAULT_LANGUAGE_ISO = chw.language)
pp = putme_in_sms_reports(sms_report, p, DEFAULT_LANGUAGE_ISO = chw.language)
report = check_sms_report_semantics( sms_report, pp , datetime.datetime.now().date(),DEFAULT_LANGUAGE_ISO = chw.language)
message, created = Message.objects.get_or_create( text  = text, direction = 'I', connection = chw.connection(), contact = chw.contact(), date = datetime.datetime.now() )

ddobj = parseObj(chw, message, errors = report['error'])

track_this_sms_report(report = report, reporter = chw)
DELETE FROM messagelog_message WHERE id > 14585901;



from api.messaging.handlers.smshandler import *
from api.messaging.zdmapper import smsmapper


identity = '+250788660270'
#identity = '+250788614161'
text = 'pre 1234567890123090 21.05.2015 05.07.2015 02 01 GS MU HD RM OL YG KX YJ LZ PC OE NS MA JA FP FE DS DI SA RB HY CH AF cl wt55.5 ht145 to hw'
#text  = 'pre 1234567891124590 15.04.2015 15.06.2015 04 02 GS MU PC OE CH AF hc wt45.5 ht155 nt nh'
#text  = 'PRE 5234567899124999 15.04.2015 15.06.2015 04 02 GS MU PC OE CH AF hc wt45.5 ht155 nt nh'
#text  = 'REF 0234567890123457'
#text  = 'ANC 5234567899124999 05.07.2015 anc2 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF cl wt65.5'
#text  = 'DEP 1234567890123457 01 09.01.2015'
#text  = 'DEP 1234007890123457'
#text  = 'RISK 1234567890123090 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF or wt70'
#text  = 'RES 1234567890123090 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF hp AA MW'
#text = 'red 1234567890123090 AP CO HE LA MC PA PS SC SL UN shb sfh OR wt55.5'
#text = 'RAR 1234567890123090 13.01.2015 AP CO HE LA MC PA PS SC SL UN HO AL MW'
#text  = 'BIR 1234567890123090 01 09.09.2015 BO SB RB AF CI CM IB DB PM hp NB wt2.5'
#text = 'CBN 1234567890123090 01 09.09.2015 EBF HT45 WT4.1 MUAC4.6'
#text = 'CHI 1234567890123090 01 09.09.2015 V2 VI IB DB HO WT4.5 MUAC5.4'
#text = 'DTH 1234567890123090 01 09.09.2015 HO ND'
#text = 'DTH 1234567890123090 HO MD'
#text = 'NBC 1234567890123090 01 NBC3 09.09.2015 SB RB AF CI CM FE HY JA NS IB DB PM NB PR CS'
#text = 'PNC 1234567890123090 PNC2 09.09.2015 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF PR MW'
#text = 'CCM 1234567890123090 01 09.09.2015 PC MA DI OI IB DB PR MUAC5.2'
#text = 'CMR 1234567890123090 01 09.09.2015 PC MA DI OI IB DB PR CW'

#text = "PRE 446"


from api.messaging.handlers.smshandler import *
from api.messaging.zdmapper import smsmapper


identity = '+250788506241'
text = "PRE 0788506241271016 10.09.2016 10.12.2016 03 02 NR NP HC WT63.5 HT168 TO NH MUAC20.5"
sms_report = SMSReport.objects.filter(keyword = text.split()[0].upper())[0]
chw = Reporter.objects.get(telephone_moh = identity)
p = get_sms_report_parts(sms_report, text, DEFAULT_LANGUAGE_ISO = chw.language)
pp = putme_in_sms_reports(sms_report, p, DEFAULT_LANGUAGE_ISO = chw.language)
report = check_sms_report_semantics( sms_report, pp , datetime.datetime.now().date(),DEFAULT_LANGUAGE_ISO = chw.language)
message, created = Message.objects.get_or_create( text  = text, direction = 'I', connection = chw.connection(), contact = chw.contact(), date = datetime.datetime.now() )

rectifier = Rectifier(sms_report, chw, p,  pp, message, orm, GESTATION = settings.GESTATION)
checkers = checker.RECTIFIER_MAPPER.get(sms_report.keyword)(rectifier)

r.patient_nid_missing()
r.invalid_nid()
r.nid_not_16digits()
r.phone_mismatch()
r.misformat_dated_nid()
r.outrange_dated_nid()
r.preg_duplicated_nid()
r.lmp_missing()
r.misformat_lmp()
r.lmp_earlier_9months()
r.lmp_greater_currentdate()
r.anc2_date_missing()
r.misformat_anc2_date()
r.anc2_lesser_currentdate()
r.anc2_date_later_edd()
r.gravidity_missing()
r.misformat_gravidity()
r.gravidity_not_between_1_30()
r.mismatch_gravidity_record()
r.missing_parity()
r.misformat_parity()
r.outrange_parity()
r.missing_previous_symptoms()
r.duplicate_symptom()
r.miscarriage_mismatch()
r.gravidity_mismatch_symptoms()
r.incoherent_jam_nr_symptom()
r.invalid_previous_symptom()
r.missing_current_symptoms()
r.invalid_current_symptom()
r.incoherent_jam_np_symptom()
r.invalid_code()
r.missing_location()
r.invalid_location()
r.missing_mother_weight()
r.invalid_mother_weight()
r.missing_mother_height()
r.invalid_mother_height()
r.missing_toilet()
r.invalid_toilet()
r.missing_handwashing()
r.invalid_handwashing()







x = smsmapper.set_record_attrs(chw, message, report)

y = smsmapper.process_failed_sms(chw, message, report)

z = smsmapper.process_treated_sms(chw, message, report)




PREGNANCY
============
pre+1234567890123092+21.05.2015+05.07.2015+02+01+GS+MU+HD+RM+OL+YG+KX+YJ+LZ+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+cl+wt55.5+ht145+to+hw
pre+1234567890123093+21.05.2015+05.07.2015+02+01+GS+MU+HD+RM+OL+YG+KX+YJ+LZ+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+hc+wt55.5+ht145+to+hw
pre+1234567890123094+21.05.2015+05.07.2015+02+01+GS+MU+HD+RM+OL+YG+KX+YJ+LZ+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+hp+wt55.5+ht145+to+hw
pre+1234567890123095+21.05.2015+05.07.2015+02+01+GS+MU+HD+RM+OL+YG+KX+YJ+LZ+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+hp+wt55.5+ht145+to+hw
pre+1234567890123096+21.05.2015+05.07.2015+02+01+GS+MU+HD+RM+OL+YG+KX+YJ+LZ+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+hp+wt55.5+ht145+to+hw
pre+1234567890123097+21.04.2015+05.06.2015+04+02+GS+MU+PC+OE+CH+AF+hc+wt65.5+ht175+nt+nh
pre+1234567890123098+15.04.2015+15.06.2015+04+02+GS+MU+PC+OE+CH+AF+hc+wt45.5+ht155+nt+nh

ANC
====

from api.messaging.handlers.smshandler import *
identity = '+250788660270'
#text = 'PRE '
#text = 'PRE 1189980056124560 25.02.2016 25.05.2016 02 00 NR SA OE HC WT72.2 HT165 TO NH'
#text = 'PRE 0788660270240516 09.09.2015 29.04.2016 2 1 gs yg ol ma hc WT58.5 HT89 to hw'
#text = 'PRE+0789660270121456+09.09.2015+29.04.2016+2+1+gs+yg+ol+ma+hc+wt58.5+ht89+to+hw'
#text = 'PRE 1234567890123450 09.04.2016 29.06.2016 3 1 gs yg ol ma hc wt58.5 ht89 to hw'
#text  = 'REF 1234567890123451'
#text  = 'DEP 1234567890123451 01 09.01.2015'
#text  = 'DEP 1234567890123451'
#text = 'ANC 1189980056124560 26.05.2016 ANC4 PC HC WT72.2'
#text  = 'ANC 1234567890123450 05.04.2016 anc2 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF cl WT65.5'
#text  = 'ANC 1234567890123451 05.04.2016 anc3 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF cl wt65.5'
#text  = 'ANC+1234567890123451+05.04.2016+anc2+VO+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+cl+wt65.5'
#text  = 'RISK 1234567890123451 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF or wt70'
#text  = 'RISK+1234567890123451+VO+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+or+wt70'
#text  = 'RES 1234567890123451 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF hp AA MW'
#text  = 'RES+1234567890123451+VO+PC+OE+NS+MA+JA+FP+FE+DS+DI+SA+RB+HY+CH+AF+hp+hc+AA+PR+MW+MS'
#text = 'RED 1234567890123451  AP CO HE LA MC PA PS SC SL UN shb sfh OR wt55.5'
#text = 'RED 1234567890123451  01 09.01.2015 AP CO HE LA MC PA PS SC SL UN shb sfh OR wt5.5'
#text = 'RAR 1234567890123451 04.05.2016 AP CO HE LA MC PA PS SC SL UN HO AL MW'
#text = 'RAR 1234567890123451 01 04.05.2016 AP CO HE LA MC PA PS SC SL UN HO AL MW'
#text = 'RAR 1234567890123451 01 13.01.2015 AP CO HE LA MC PA PS SC SL UN HO AL CW'
#text = 'RED 1199980056124560 YU HO WT75.2'
#text = 'RED 1199980056124560  29.05.2015 YU IT HO WT75.2'
#text = 'RAR 1199980056124560 CO HE OR AL MW'
#text  = 'BIR 1234567890123451 01 09.10.2015 BO SB RB AF CI CM IB DB PM hp NB wt2.5'
#text = 'BIR 1197680056124560 01 25.04.2016 GI PM HO BF1 WT3.4'
#text = 'PNC 1234567890123451 PNC1 09.01.2015 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF PR MW'
#text = 'NBC 1234567890123451 01 NBC1 09.01.2015 SB RB AF CI CM FE HY JA NS IB DB PM NB PR CS'
#text = 'CHI 1234567890123451 02 13.03.2015 V2 VI IB DB HO WT4.5 MUAC6.4'
#text  = 'BIR+1234567890123451+01+09.01.2015+GI+SB+RB+AF+CI+CM+IB+DB+PM+cl+BF1+wt2.8'
#text = 'CCM 1234567890123451 01 09.09.2015 PC MA DI OI IB DB PR MUAC5.2'
#text = 'CCM 1199980056124560 01 27.05.2016 MA PR MUAC12.5'
#text='RAR 1199980056124560 CO HE OR AL MW'
#text = 'CMR 1234567890123451 01 09.02.2015 PC MA DI OI IB DB PR CW'
#text = 'CBN 1234567890123451 01 09.01.2015 EBF HT40 WT4.1 MUAC6.6'
#text = 'DTH 1234567890123456 01 09.01.2015 HO ND'
#text = 'DTH 1234567890123456 HO MD'
text = 'NBC 1223380056124560 01 NBC6 08.06.2016 AF NB PR CW'
#text = 'PNC 1223380056124560 PNC2 08.06.2016 NP PR MW'


sms_report = SMSReport.objects.filter(keyword = text.split()[0].upper())[0]
chw = Reporter.objects.get(telephone_moh = identity)
p = get_sms_report_parts(sms_report, text, DEFAULT_LANGUAGE_ISO = chw.language)
pp = putme_in_sms_reports(sms_report, p, DEFAULT_LANGUAGE_ISO = chw.language)
report = check_sms_report_semantics( sms_report, pp , datetime.datetime.now().date(),DEFAULT_LANGUAGE_ISO = chw.language)
message, created = Message.objects.get_or_create( text  = text, direction = 'I', connection = chw.connection(), contact = chw.contact(), date = datetime.datetime.now() )

rectifier = Rectifier(sms_report, chw, p,  pp, message, orm, GESTATION = settings.GESTATION)
checkers = checker.RECTIFIER_MAPPER.get(sms_report.keyword)(rectifier)
checkers.errors








