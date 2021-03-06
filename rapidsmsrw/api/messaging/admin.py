#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from django.contrib import admin
from .models import *

class SMSReportAdmin(admin.ModelAdmin):                                                        
    list_filter = ()                                                        
    exportable_fields = ( 'title_en', 'title_rw', 'keyword', 'description', 'field_separator', 'in_use' , 'case_sensitive', 'syntax_regex', 'created', )                                                        
    search_fields = ( 'keyword', 'description', 'title_en', 'title_rw', 'field_separator', 'in_use' , 'case_sensitive', 'syntax_regex', 'created', )                                                        
    list_display = ( 'keyword', 'description', 'title_en', 'title_rw', 'field_separator', 'in_use' , 'case_sensitive', 'syntax_regex', 'created', )                                                    
    actions = (export_model_as_csv, export_model_as_excel)
    
class SMSReportFieldAdmin(admin.ModelAdmin):                                                        
    list_filter = ('sms_report',)                                                        
    exportable_fields = ('title_en', 'title_rw', 'category_en', 'category_rw', 'sms_report', 'prefix', 'key', 'description', 'type_of_value', 'upper_case', 'lower_case', 'minimum_value', 'maximum_value', 
                            'minimum_length', 'maximum_length', 'position_after_sms_keyword', 'depends_on_value_of', 'dependency', 
                        'allowed_value_list', 'only_allow_one', 'required', 'created', 
                        )                                                        
    search_fields = ('key', 'description', 'prefix', 'type_of_value' , 'position_after_sms_keyword', 'required', 'created', )                                                                 
    list_display = ('sms_report', 'prefix', 'key', 'description', 'type_of_value', 'upper_case', 'lower_case', 'minimum_value', 'maximum_value', 
                            'minimum_length', 'maximum_length', 'position_after_sms_keyword', 'depends_on_value_of', 'dependency', 
                        'allowed_value_list', 'only_allow_one', 'required', 'created', 
                        ) 
    actions = (export_model_as_csv, export_model_as_excel)  
    
class SMSLanguageAdmin(admin.ModelAdmin):                                                        
    list_filter = ()                                                        
    exportable_fields = ('id', 'name', 'iso_639_1_code', 'description', 'created', )                                                        
    search_fields = ('name', 'iso_639_1_code', 'description', 'created', )                                                           
    list_display = ('name', 'iso_639_1_code', 'description', 'created', )                                                       
    actions = (export_model_as_csv, export_model_as_excel)
    
class SMSMessageAdmin(admin.ModelAdmin):                                                        
    list_filter = ('destination', 'message_type', 'sms_report', 'sms_report_field',)                                                        
    exportable_fields = ('message_type', 'sms_report', 'sms_report_field', 'message_en', 'message_rw', 'created',)                                                        
    search_fields = ('message_type', 'sms_report', 'sms_report_field', 'created', )                                                                   
    list_display = ('message_type', 'sms_report', 'sms_report_field', 'created', )                                                               
    actions = (export_model_as_csv, export_model_as_excel)

class SMSDBConstraintAdmin(admin.ModelAdmin):                                                        
    list_filter = ()                                                        
    exportable_fields = ( 'sms_report', 'sms_report_field', 'constraint', 'minimum_period_value', 'maximum_period_value' , 'refer_sms_report',
                             'refer_sms_report_field', 'created', )                                                        
    search_fields = ( 'sms_report', 'sms_report_field', 'constraint', 'minimum_period_value', 'maximum_period_value' , 'refer_sms_report',
                             'refer_sms_report_field', 'created', )                                   
    list_display = ( 'sms_report', 'sms_report_field', 'constraint', 'minimum_period_value', 'maximum_period_value' , 'refer_sms_report',
                             'refer_sms_report_field', 'created', )                               
    actions = (export_model_as_csv, export_model_as_excel)   

class SMSErrorCodeAdmin(admin.ModelAdmin):                                                        
    list_filter = ('description', 'message_type',)                                                        
    exportable_fields = ('message_type', 'description', 'message_en', 'message_rw', 'message_fr',)                                                        
    search_fields = ('message_type', 'description', )                                                                   
    list_display = ('message_type', 'description', 'message_en', 'message_rw', 'message_fr',)
    actions = (export_model_as_csv, export_model_as_excel)
  

admin.site.register(SMSReport, SMSReportAdmin)
admin.site.register(SMSReportField, SMSReportFieldAdmin)
admin.site.register(SMSLanguage, SMSLanguageAdmin)
admin.site.register(SMSMessage, SMSMessageAdmin)
#admin.site.register(SMSErrorCode, SMSErrorCodeAdmin)
#admin.site.register(SMSDBConstraint, SMSDBConstraintAdmin)

