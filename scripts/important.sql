ALTER TABLE chws_facilitystaff ALTER COLUMN service TYPE VARCHAR (50);
ALTER TABLE chws_facilitystaff ALTER COLUMN area_level TYPE VARCHAR (50);
UPDATE chws_facilitystaff SET service  = 'Chief of Medical Staff' WHERE service = 'cmed' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Emergency' WHERE service = 'cemg' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Supervisors' WHERE service = 'csup' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Nursing' WHERE service = 'cnur' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Ambulance Drivers' WHERE service = 'cdrv' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Maternity' WHERE service = 'cmat' ;
