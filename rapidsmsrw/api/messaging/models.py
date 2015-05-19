#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from api.utils import *
from django.contrib.auth.models import Group
from api.chws.models import *


##Start of SMSReport
class SMSReport(models.Model):

    """
        This guide you building your own SMS Report ... the syntax of an SMS please, 
        don't think about other constraints your are not even able to figure out before you go into the DB  

    """
    SEPARATOR_CHOICES = (
        (' ','WhiteSpace ( )'),
        (',','Comma (,)'),
        (';','Semicolon (;)'),
        (':','Colon (:)'),
        ('*','Asterisk (*)'),
    )


    ### This has to be recognized in the language supported
        
    ##START OF SMSReport LANGUAGES
    
    title_en = models.TextField(null = True, blank = True, help_text = 'Title in English ')


    title_rw = models.TextField(null = True, blank = True, help_text = 'Title in Kinyarwanda ')
    ##END OF SMSReport LANGUAGES
    
    keyword = models.CharField(max_length=30, unique=True)

    description =  models.TextField(max_length=255,
                               help_text="Why do we need this SMS Report?")

    field_separator = models.CharField(max_length=1, choices=SEPARATOR_CHOICES, null=True, blank=True,
                                 help_text="What is the separator of your SMS Report Fields?")

    case_sensitive = models.BooleanField(default=False,
                                 help_text="Do we need our SMS Report to react on either Upper or Lower Case?")

    in_use = models.BooleanField(default=True,
                                 help_text="Do we still use this SMS Report?")
    
    syntax_regex = models.TextField(blank = True, null = True,
                                help_text="For Developer ... Don't show on ADMIN SITE")
    
    """

    ### This has to be recognized in the language supported, language tables
    success_response = models.TextField(blank = True, null = True,
                                help_text="You need to define a SMS to be sent to acknowledge the message has been received successfully.")

    
    ### This has to be recognized in the language supported, language tables
    failure_response = models.TextField(blank = True, null = True,
                                help_text="You need to define a SMS to be sent to acknowledge the message has been received with errors.")

    ### This has to be recognized in the language supported, language tables
    failure_reason = models.TextField(blank = True, null = True,
                                help_text="You need to define a SMS to be sent to show the reason of failure.")
    
    """
    
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __unicode__(self):
        return "%s" % self.keyword


##End of SMSReport

##Start of SMSReportField
class SMSReportField(models.Model):


    VALUE_TYPE_CHOICES = (

        ('integer','Integer'),
        ('float','Float'),
        ('date','Date'),
        ('string','String'),
        ('string_digit','String Digit'),
    )

    DEPEDENCY_CHOICES = (
                            ('greater', 'Greater than'),
                            ('greater_or_equal', 'Greater than or Equal'),
                            ('equal', 'Equal'),
                            ('different', 'Different'),
                            ('less', 'Less than'),
                            ('less_or_equal', 'Less than or Equal'),
                            ('jam', 'Jam'),
                         )
    
    sms_report = models.ForeignKey(SMSReport)

    ##START OF SMSReportField LANGUAGES
    
    title_en = models.TextField(null = True, blank = True, help_text = 'Title in English ')

    category_en = models.TextField(null = True, blank = True, help_text = 'Category in English ')
    

    title_rw = models.TextField(null = True, blank = True, help_text = 'Title in Kinyarwanda ')

    category_rw = models.TextField(null = True, blank = True, help_text = 'Category in Kinyarwanda ')
    ##END OF SMSReportField LANGUAGES
    
    prefix = models.CharField(max_length=5, null=True, blank=True,
                                      help_text="Do You prefix this field? E.G: WT50.8")
    key = models.CharField(max_length=30, null=True, blank=True,
                                      help_text="What is the unique key for this Field")
    description = models.TextField(max_length=255,
                               help_text="Why do we need this SMS Report Field?")
    type_of_value =  models.CharField(max_length=20, choices=VALUE_TYPE_CHOICES, null=True, blank=True,
                                 help_text="The type of value the field will have.")
    
    upper_case = models.BooleanField(default=False,
                                 help_text="This SMS Report Field must be Upper Case.")
    lower_case = models.BooleanField(default=False,
                                 help_text="This SMS Report Field must be Lower Case.")
    
    minimum_value = models.FloatField(blank = True, null=True, 
                                      help_text="What is the minimum value for this SMS Report Field?")
    maximum_value = models.FloatField(blank = True, null=True, 
                                      help_text="What is the maximum value for this SMS Report Field?")
    
    minimum_length = models.FloatField(blank = True, null=True, 
                                      help_text="What is the minimum length for this SMS Report Field?")
    maximum_length = models.FloatField(blank = True, null=True, 
                                      help_text="What is the maximum length for this SMS Report Field?")
    
    position_after_sms_keyword = models.PositiveSmallIntegerField(validators = [MinValueValidator(1)])
    depends_on_value_of = models.ForeignKey("SMSReportField", null=True, blank=True, 
                                            related_name="dependent", help_text = "Does this SMS Report Field depend on another?")
    
    dependency = models.CharField(max_length=30, choices=DEPEDENCY_CHOICES, null=True, blank=True,
                                 help_text="How does this SMS Report Field depend on that?")
    
    allowed_value_list = models.TextField(max_length=255, null=True, blank=True,
                               help_text="Does this SMS Report Field have a list of values only allowed? Separate them with semi-colon (;)")
    only_allow_one =  models.BooleanField(default=False,
                                 help_text="Do we only allow one value of the above list for this SMS Report Field?")
    
    required =  models.BooleanField(default=True,
                                 help_text="Is this SMS Report Field mandatory?")
    
    created = models.DateTimeField(auto_now_add=True)
    
    unique_together = (("sms_report", "key", "position_after_sms_keyword"))
    
    def __unicode__(self):
        return "%s-%s" % (self.sms_report, self.description)
    
##End of SMSReportField
    
##Start of SMSLanguage
class SMSLanguage(models.Model):
    
    name = models.CharField(max_length=30, unique = True,
                                 help_text="Language Name or Title")
    
    iso_639_1_code = models.CharField(max_length = 5, unique = True,
                                 help_text="Language Code based on ISO 639-1")
    
    description = models.TextField(max_length=255, null=True, blank=True,
                               help_text="Description of the language")

    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s(%s)" % (self.name, self.iso_639_1_code)    
    
    
##End of SMSLanguage
    
##Start of SMSMessage
class SMSMessage(models.Model):

    """
        This Table Contains Error Code and Message thrown out by supported language, whoever need to customize
        This Messaging Api needs to define appropriate message per error code, where error code can only implemented by skilled developer
    
    """
    
    CODE_CHOICES = (
                            ('reminder', 'Reminder'),
                            ('red_notification', 'Red Alert Notification'),
                            ('poor_weight', 'Underweight/Poor weight'),
                            ('lost_weight', 'Lost Weight'),
                            ('faltering_weight', 'Faltering Weight'),
                            ('poor_height', 'Underweight/Poor height'),
                            ('poor_bmi', 'Poor Body Mass Index (BMI)'),
                            ('poor_weight_for_height', 'Poor Weight for Height'),
                            ('underweight', 'Underweight'),
                            ('stunted', 'Stunted'),
                            ('wasted', 'Wasted'),
                            ('success', 'The SMS Report Has Been Submitted Successfully'),
                            ('unknown_keyword', 'Unknown Keyword'),
                            ('empty_sms_report', 'Empty SMS Report'),
                            ('missing_sms_report_field', 'Missing SMS Report Field'),
                            ('sequence_or_order', 'Sequence or Order Not Correct'),
                            ('unsupported_smsreport_fcode', 'Not Supported SMS Report Field Code'),
                            ('unsupported_prefix', 'Not Supported SMS Report Field Prefix'),
                            ('unknown_field_code', 'Unknown Field Code'),
                            ('only_integer', 'Only Integer Number Supported'),
                            ('only_float', 'Only Decimal Number Supported'),
                            ('only_date', 'Only Date Supported'),
                            ('only_string', 'Only String Supported'),
                            ('only_string_digit', 'Only String of Digit Supported'),
                            ('only_upper_case', 'Only Upper Case Supported'),
                            ('only_lower_case', 'Only Lower Case Supported'),
                            ('not_in_range', 'Length or Value is either Greater or Less Than Allowed'),
                            ('dependency_error', 'Dependency Error'),
                            ('not_in_allowed_values', 'Not In Allowed Values'),
                            ('one_value_of_list', 'Only One Value Is Allowed From The List'),
                            ('is_required', 'This SMS Report Field Is Mandatory'),
                            ('sender_not_registered', 'Sender Not Registered'),
                            ('unknown_error', 'Unknown Error'),
                            ('help', 'Help Text'),
                            ('duplication', 'Duplication'),
                            ('missing_based_data', 'Missing Base Data'),
                            ('expired_based_data', 'Expired Base Data'),
                            ('bad_indangamuntu', 'Bad National ID'),
                            ('bad_date', 'Bad Date'),
                            ('impossible_date', 'Impossible Date'),
                            ('bad_number', 'Bad Number'),
                            ('bad_floated_field', 'Bad Floated Field'),
                            ('bad_numbered_field', 'Bad Numbered Field'),
                            ('unknown_code', 'Unknown Code'),
                            ('bad_text', 'Bad Text'),
                            ('bad_muac_code', 'Bad MUAC Code'),
                            ('bad_muac_date', 'MUAC only after 6 months'),
                            ('bad_height_code', 'Bad Height Code'),
                            ('bad_weight_code', 'Bad Weight Code'),
                            ('bad_phone_id', 'Bad Phone ID'),
                            ('bad_encoding', 'Bad Encoding'),
                            ('incoherent_date_periods', 'Incoherent Date Period'),                           
                            
                          )
    
    message_type = models.CharField(max_length=100, choices = CODE_CHOICES,
                                      help_text="Feedback Message Code")
    sms_report =  models.ForeignKey(SMSReport, blank = True, null = True)
    sms_report_field = models.ForeignKey(SMSReportField, blank = True, null = True)
    destination = models.ForeignKey(Group, blank = True, null = True)
    description = models.TextField(null = True, blank = True, help_text = 'Why This SMS, Have you check none is similar?')
    #Reminder to user_group, of patient, base on sms report table, time column , after  x seconds, y minutes, z hour , m days, n months, p year
    
    ##START OF SMSMessage LANGUAGES

    message_en = models.TextField(null = True, blank = True, help_text = 'Message in English ')
        

    message_rw = models.TextField(null = True, blank = True, help_text = 'Message in Kinyarwanda ')
    ##END OF SMSMessage LANGUAGES
    
    created = models.DateTimeField(auto_now_add=True)

    unique_together = (("message_type", "sms_report", "sms_report_field")) 
    
    def __unicode__(self):
        return "%s-%s" % (self.get_message_type_display(), self.description)   
    
##End of SMSMessage
##all report_keys ; all_distinct_report_fields; all_locations_type; all_message_types; reporter; created


class SMSErrorCode(models.Model):
    """
        Abstract every single message in this table instead of sending nonsense

    """
    message_type    = models.CharField(max_length=100, unique = True,
                                      help_text="Feedback Message Code")
    description = models.TextField(null = True, blank = True, help_text = 'Why This SMS, Have you check none is similar?')

    message_en = models.TextField(null = True, blank = True, help_text = 'Message in English ')        

    message_rw = models.TextField(null = True, blank = True, help_text = 'Message in Kinyarwanda ')
    
    message_fr = models.TextField(null = True, blank = True, help_text = 'Message in French ')

    def __unicode__(self):
        return "%s-%s" % (self.message_type, self.description)

##Start of SMSDBConstraint
class SMSDBConstraint(models.Model):
    """
    Before storing the incoming report, appropriately, you may need some constraint against the DB
    This Model is there for only that reason    
    """

    CONSTRAINT_CHOICES = (

        ('unique','Unique'),
        ('base','Base/Requirer'),
        ('tolerance','Tolerance'),
        ('stopper','Expirer/Stopper'),
        
    )


    sms_report =  models.ForeignKey(SMSReport, related_name = 'sr', blank = True, null = True)
    sms_report_field = models.ForeignKey(SMSReportField, related_name = 'srf', blank = True, null = True)
    constraint = models.CharField(max_length=100, choices = CONSTRAINT_CHOICES,
                                      help_text="Constraint Definition")
    refer_sms_report =  models.ForeignKey(SMSReport, related_name = 'refer_sr', blank = True, null = True)
    refer_sms_report_field = models.ForeignKey(SMSReportField, related_name = 'refer_srf', blank = True, null = True)
    other_fields_keys = models.TextField(max_length=255, null=True, blank=True,
                               help_text="Does it have a list of codes of constraint? Separate them with semi-colon (;)")
    minimum_period_value = models.FloatField(blank = True, null=True, 
                                      help_text="What is the minimum period value?")
    maximum_period_value = models.FloatField(blank = True, null=True, 
                                      help_text="What is the maximum period value?")
    created = models.DateTimeField(auto_now_add=True)

    unique_together = (("constraint", "sms_report", "sms_report_field")) 
    
    def __unicode__(self):
        return "%s-%s-%s" % (self.get_constraint_display(), self.sms_report, self.sms_report_field)   
    
##End of SMSDBConstraint
    
    
def ensure_new_language(sender, **kwargs):
    if kwargs.get('created', False):
        language = kwargs.get('instance')
        #print language
        field_name = 'message_%s' % language.iso_639_1_code
        marker = "LANGUAGES"
        help_text = "Message in %s " % language.name
        model_object = get_model_object(language._meta.app_label, "SMSMessage" )
        filename = '%s/%s/models.py' % (API_PATH, model_object._meta.app_label)
        lang_c = add_column_textfield_to_table(filename, model_object, field_name,  '%s %s' % ( model_object._meta.object_name, marker ), help_text)
        field_name1 = 'title_%s' % language.iso_639_1_code
        help_text1 = "Title in %s " % language.name
        model_object1 = get_model_object(language._meta.app_label, "SMSReport" )
        lang_c1 = add_column_textfield_to_table(filename, model_object1, field_name1,  '%s %s' % ( model_object1._meta.object_name, marker ), help_text1)
        model_object2 = get_model_object(language._meta.app_label, "SMSReportField" )
        lang_c2 = add_column_textfield_to_table(filename, model_object2, field_name1,  '%s %s' % ( model_object2._meta.object_name, marker ), help_text1)
        field_name2 = 'category_%s' % language.iso_639_1_code
        help_text2 = "Category in %s " % language.name
        lang_c3 = add_column_textfield_to_table(filename, model_object2, field_name2,  '%s %s' % ( model_object2._meta.object_name, marker ), help_text2)
        if lang_c and lang_c1 and lang_c2 and lang_c3:    return True
        else:   return False
    
 
post_save.connect(ensure_new_language, sender = SMSLanguage)    
    
