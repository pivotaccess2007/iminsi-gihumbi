#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from django.contrib.auth.models import Group, User
from django.db import models
from api.chws.models import *
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator


def get_phone_number_validators():    

    return {'min': 13, 'max': 13}

__TELEPHONE_VALIDATOR__ = get_phone_number_validators()



class Provider(models.Model):
    """ Whoever registered in the system is host in this table referenced with his user accounts """

    language_english	= 'en'
    language_french		= 'fr'
    language_kinyarwanda	= 'rw'

    health_centre_level = 'hc'
    district_hospital_level = 'hd'
    district_level = 'ds'
    province_level = 'pr'
    nation_level   = 'nw'

    AREA_CHOICES = ( (health_centre_level, "Health Centre"),
                        (district_hospital_level, "District Hospital"),
                        (district_level, "District"),
                        (province_level, "Province"),
                        (nation_level, "Nationwide"),
                   )

    LANGUAGE_CHOICES = ( (language_english, "English"),
                (language_french, "French"),
                (language_kinyarwanda, "Kinyarwanda"))
    
    title = models.ForeignKey(Group)
    user  = models.ForeignKey(User)
    telephone = models.CharField( max_length = __TELEPHONE_VALIDATOR__['max'], validators = [RegexValidator(regex='^.{%d}$' % __TELEPHONE_VALIDATOR__['max'],\
                                         message='Length has to be %d' % __TELEPHONE_VALIDATOR__['max'], code='nomatch')], null=True, unique = True)
    
    working_level = models.CharField(max_length = 2, blank=True, null = True, choices= AREA_CHOICES, help_text="Select the level of working")
    language = models.CharField(max_length = 2, blank=True, null = True, choices= LANGUAGE_CHOICES, help_text="Select the preferred language to receive SMS")
    notify_for_red_alert = models.BooleanField(default=False)
    notify_for_malnutrition  = models.BooleanField(default=False)
    notify_for_death         = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()  
    ##START OF LINK TO LOCATION TYPES


    ##START OF NATION LINK
    nation = models.ForeignKey(Nation)
    ##END OF NATION LINK

    ##START OF PROVINCE LINK
    province = models.ForeignKey(Province)
    ##END OF PROVINCE LINK

    ##START OF DISTRICT LINK
    district = models.ForeignKey(District)
    ##END OF DISTRICT LINK

    ##START OF HEALTH_FACILITY LINK
    health_centre = models.ForeignKey(HealthCentre)
    ##END OF HEALTH_FACILITY LINK

    ##START OF HOSPITAL LINK
    hospital = models.ForeignKey(Hospital)
    ##END OF HOSPITAL LINK

    ##END OF LINK TO LOCATION TYPES
    
    class Meta:
        verbose_name = "Web User"
        permissions = (
            ('can_view', 'Can view'),
        )

