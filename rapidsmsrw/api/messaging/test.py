
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
