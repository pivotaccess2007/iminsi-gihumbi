from entities import rentities
from messages import rmessages

ASSOCIATIONS = {
  'PRE':  (rmessages.PregMessage,
    {'initialises': [rentities.Mother, rentities.Pregnancy]}
  ),
  'REF':  (rmessages.RefMessage,
    {'initialises': [rentities.Mother, rentities.Refusal]}
  ),
  'ANC':  (rmessages.ANCMessage,
    {'initialises': [rentities.Mother, rentities.Pregnancy, rentities.ANCVisit]}
  ),
  'DEP':  (rmessages.DepMessage,
    {'initialises': [rentities.Mother, rentities.Child, rentities.Departure]}
  ),
  'ALTDEP':  (rmessages.DepMessage,
    {'initialises': [rentities.Mother, rentities.Departure]}
  ),
  'RISK': (rmessages.RiskMessage,
    {'initialises': [rentities.Mother, rentities.Pregnancy, rentities.Risk]}
  ),
  'RED':  (rmessages.RedMessage,
    {'initialises': [rentities.Mother, rentities.Pregnancy, rentities.RedAlert]}
  ),
  'BIR':  (rmessages.BirMessage,
    {'initialises': [rentities.Mother, rentities.Pregnancy, rentities.Child]}
  ),
  'CHI':  (rmessages.ChildMessage,
    {'initialises': [rentities.Mother, rentities.Child, rentities.ChildHealth]}
  ),
  'ALTCHI':  (rmessages.ChildMessage,
    {'initialises': [rentities.Mother, rentities.Child, rentities.ChildHealth]}
  ),
  'DTH':  (rmessages.DeathMessage,
    {'initialises': [rentities.Mother, rentities.Child, rentities.Death]}
  ),
  'ALTDTH':  (rmessages.DeathMessage,
    {'initialises': [rentities.Mother, rentities.MotherDeath]}
  ),
  'RES':  (rmessages.ResultMessage,
    {'initialises': [rentities.Mother, rentities.Pregnancy, rentities.Risk]}
  ),
  'RAR':  (rmessages.RedResultMessage,
    {'initialises': [rentities.Mother, rentities.Pregnancy, rentities.RedAlert]}
  ),
  'NBC':  (rmessages.NBCMessage,
    {'initialises': [rentities.Mother, rentities.Child, rentities.NBCVisit]}
  ),
  'PNC':  (rmessages.PNCMessage,
    {'initialises': [rentities.Mother, rentities.Pregnancy, rentities.PNCVisit]}
  ),
  'CCM':  (rmessages.CCMMessage,
    {'initialises': [rentities.Mother, rentities.Child, rentities.ChildCCM]}
  ),
  'CMR':  (rmessages.CMRMessage,
    {'initialises': [rentities.Mother, rentities.Child, rentities.ChildCCM]}
  ),
  'CBN':  (rmessages.CBNMessage,
    {'initialises': [rentities.Mother, rentities.Child, rentities.ChildNutrition]}
  )
}
