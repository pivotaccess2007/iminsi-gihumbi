from processor import *
from datetime import timedelta
import settings

class IndangamuntuEntity(UniqueEntity):
  unique  = ['indangamuntu']

class IndangamuntuRelativeEntity(IndangamuntuEntity):
  unique  = ['indangamuntu', 'child_number']

class ANCVisit(UniqueEntity):
  table       = 'rw_ancvisits'
  unique      = ['indangamuntu', 'pregnancy_id', 'anc_visit']
  belongs_to  = lambda _: Pregnancy

class PNCVisit(UniqueEntity):
  table       = 'rw_pncvisits'
  unique      = ['indangamuntu', 'pregnancy_id', 'pnc_visit']
  belongs_to  = lambda _: Pregnancy

class Risk(UniqueEntity):
  table       = 'rw_risks'
  unique      = ['indangamuntu', 'report_date']
  belongs_to  = lambda _: Pregnancy

class RedAlert(UniqueEntity):
  table       = 'rw_redalerts'
  unique      = ['indangamuntu', 'report_date']
  belongs_to  = lambda _: Pregnancy

class Pregnancy(IndangamuntuEntity):
  table       = 'rw_pregnancies'
  unique      = ['indangamuntu', 'lmp']
  belongs_to  = lambda _: Mother
  can_have    = lambda _: [ANCVisit, Child, PNCVisit, Risk, RedAlert]

  #pregnancy in case we receive a birth without a pregnancy ... TODO 
  #def get_identifiers(self, _, ents):
  #  return [('indangamuntu', ents['indangamuntu']), ('lmp', ents['birth_date'] - timedelta(days = settings.GESTATION))]

class Mother(IndangamuntuEntity):
  table       = 'rw_mothers'
  can_have    = lambda _: [Pregnancy]

class Departure(IndangamuntuEntity):
  table       = 'rw_departures'
  can_have    = lambda _: [Pregnancy]

class Refusal(IndangamuntuEntity):
  table       = 'rw_refusals'
  can_have    = lambda _: [Pregnancy]

class Child(IndangamuntuRelativeEntity):
  table       = 'rw_children'
  unique      = ['indangamuntu', 'birth_date', 'child_number']
  belongs_to  = lambda _: Pregnancy
  can_have    = lambda _: [NBCVisit, ChildCCM, ChildNutrition]

class ChildCCM(UniqueEntity):
  table       = 'rw_ccms'
  unique      = ['indangamuntu', 'child_id', 'report_date']
  belongs_to  = lambda _: Child

class ChildNutrition(UniqueEntity):
  table       = 'rw_nutritions'
  unique      = ['indangamuntu', 'child_id', 'report_date']
  belongs_to  = lambda _: Child

class ChildHealth(UniqueEntity):
  table       = 'rw_childhealth'
  unique      = ['indangamuntu', 'child_id', 'report_date']
  belongs_to  = lambda _: Child

class NBCVisit(UniqueEntity):
  table       = 'rw_nbcvisits'
  unique      = ['indangamuntu', 'child_id', 'nbc_visit']
  belongs_to  = lambda _: Child

class Death(IndangamuntuRelativeEntity):
  table       = 'rw_deaths'
  # belongs_to  = lambda _: [Mother, Child]

class MotherDeath(IndangamuntuEntity):
  table       = 'rw_deaths'

