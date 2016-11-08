ALTER TABLE rw_pregnancies ADD COLUMN bmi double precision DEFAULT 0.0;
UPDATE rw_pregnancies SET bmi = (mother_weight / ((mother_height * mother_height) / 10000.0)) ;
UPDATE mother_track SET bmi = (mother_weight / ((mother_height * mother_height) / 10000.0)) ;
ALTER TABLE chws_facilitystaff ALTER COLUMN service TYPE VARCHAR (50);
ALTER TABLE chws_facilitystaff ALTER COLUMN area_level TYPE VARCHAR (50);
UPDATE chws_facilitystaff SET service  = 'Chief of Medical Staff' WHERE service = 'cmed' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Emergency' WHERE service = 'cemg' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Supervisors' WHERE service = 'csup' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Nursing' WHERE service = 'cnur' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Ambulance Drivers' WHERE service = 'cdrv' ;
UPDATE chws_facilitystaff SET service  = 'Chief of Maternity' WHERE service = 'cmat' ;


ALTER TABLE chws_reporter ADD COLUMN indexcol integer DEFAULT NULL;
UPDATE chws_reporter SET  indexcol = id;

ALTER TABLE chws_registrationconfirmation ADD COLUMN indexcol integer DEFAULT NULL;
UPDATE chws_registrationconfirmation SET  indexcol = id;


ALTER TABLE rw_ancvisits ADD COLUMN lmp timestamp without time zone;
--ALTER TABLE ancmessage DROP COLUMN lmp timestamp without time zone;
ALTER TABLE rw_risks ADD COLUMN lmp timestamp without time zone;
ALTER TABLE rw_risks ADD COLUMN risk_date timestamp without time zone;
--ALTER TABLE riskmessage ADD COLUMN lmp timestamp without time zone;
ALTER TABLE rw_redalerts ADD COLUMN lmp timestamp without time zone;
--ALTER TABLE redmessage ADD COLUMN lmp timestamp without time zone;
ALTER TABLE rw_pncvisits ADD COLUMN lmp timestamp without time zone;
--ALTER TABLE pncmessage ADD COLUMN lmp timestamp without time zone;
ALTER TABLE rw_ccms ADD COLUMN case_date timestamp without time zone;

ALTER TABLE messagelog_message ADD COLUMN deleted boolean;

ALTER TABLE dlr ADD COLUMN indexcol integer NOT NULL;
CREATE SEQUENCE dlr_indexcol_seq;
ALTER TABLE dlr ALTER indexcol SET DEFAULT NEXTVAL('dlr_indexcol_seq');
ALTER TABLE dlr ADD COLUMN msgid text NOT NULL UNIQUE;


CREATE SEQUENCE dlr_indexcol_seq;

CREATE TABLE dlr (
    smsc character varying(48),
    ts character varying(48),
    destination character varying(48),
    source character varying(48),
    service character varying(48),
    url character varying(255),
    mask integer,
    status integer,
    boxc character varying(48),
    indexcol integer DEFAULT nextval('dlr_indexcol_seq'::regclass) NOT NULL,
    msgid text NOT NULL UNIQUE,
    message text NOT NULL
);


CREATE SEQUENCE handset_indexcol_seq;

CREATE TABLE handset (
    destination character varying(48) NOT NULL,
    source character varying(48) NOT NULL,
    text character varying(255) NOT NULL,
    sent_when character varying(48) NOT NULL,
    status integer,
    indexcol integer DEFAULT nextval('handset_indexcol_seq'::regclass) NOT NULL
);

