DROP TRIGGER redmessage_trigger ON redmessage;
DROP FUNCTION track_notify_trigger();
-- DROP TABLE pregmessage ;

-- CREATE TABLE PREGMESSAGE(
--   INDEXCOL  SERIAL PRIMARY KEY,
--   REPORTER_PK          INT      NOT NULL,
--   REPORTER_PHONE       TEXT      NOT NULL,
--   NATION_PK		INT      NOT NULL,
--   PROVINCE_PK		INT      NOT NULL,
--   DISTRICT_PK		INT      NOT NULL,
--   HEALTH_CENTER_PK	INT      NOT NULL,
--   SECTOR_PK		INT      NOT NULL,
--   CELL_PK		INT      NOT NULL,
--   VILLAGE_PK		INT      NOT NULL
   -- AGE            INT       NOT NULL,
   -- ADDRESS        CHAR(50),
   -- SALARY         REAL
--);

CREATE OR REPLACE FUNCTION track_notify_trigger() RETURNS trigger AS $$

DECLARE

BEGIN
  EXECUTE 'NOTIFY ' || TG_TABLE_NAME || '_' || TG_OP || ',' ||  quote_literal(NEW.indexcol::text) ;
  RETURN NEW;
END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER redmessage_trigger AFTER insert or update or delete on redmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();

-- CREATE TRIGGER table1_trigger AFTER insert or update or delete on table1 execute procedure track_notify_trigger();
-- http://www.divillo.com/
-- HOWTO: Automatically Responding To PostgreSQL Table Changes With Twisted
