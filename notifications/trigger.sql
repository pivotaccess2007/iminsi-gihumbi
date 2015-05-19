DROP TRIGGER redmessage_trigger ON redmessage;
DROP TRIGGER pregmessage_trigger ON pregmessage;
DROP TRIGGER refmessage_trigger ON refmessage;
DROP TRIGGER ancmessage_trigger ON ancmessage;
DROP TRIGGER depmessage_trigger ON depmessage;
DROP TRIGGER riskmessage_trigger ON riskmessage;
DROP TRIGGER redmessage_trigger ON redmessage;
DROP TRIGGER birmessage_trigger ON birmessage;
DROP TRIGGER childmessage_trigger ON childmessage;
DROP TRIGGER deathmessage_trigger ON deathmessage;
DROP TRIGGER resultmessage_trigger ON resultmessage;
DROP TRIGGER redresultmessage_trigger ON redresultmessage;
DROP TRIGGER nbcmessage_trigger ON nbcmessage;
DROP TRIGGER pncmessage_trigger ON pncmessage;
DROP TRIGGER ccmmessage_trigger ON ccmmessage;
DROP TRIGGER cmrmessage_trigger ON cmrmessage;
DROP TRIGGER cbnmessage_trigger ON cbnmessage;
DROP TRIGGER mother_track_trigger ON mother_track;
DROP TRIGGER child_track_trigger ON child_track;

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
CREATE TRIGGER pregmessage_trigger AFTER insert or update or delete on pregmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER refmessage_trigger AFTER insert or update or delete on refmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER ancmessage_trigger AFTER insert or update or delete on ancmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER depmessage_trigger AFTER insert or update or delete on depmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER riskmessage_trigger AFTER insert or update or delete on riskmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER redmessage_trigger AFTER insert or update or delete on redmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER birmessage_trigger AFTER insert or update or delete on birmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER childmessage_trigger AFTER insert or update or delete on childmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER deathmessage_trigger AFTER insert or update or delete on deathmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER resultmessage_trigger AFTER insert or update or delete on resultmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER redresultmessage_trigger AFTER insert or update or delete on redresultmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER nbcmessage_trigger AFTER insert or update or delete on nbcmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER pncmessage_trigger AFTER insert or update or delete on pncmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER ccmmessage_trigger AFTER insert or update or delete on ccmmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER cmrmessage_trigger AFTER insert or update or delete on cmrmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER cbnmessage_trigger AFTER insert or update or delete on cbnmessage FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER mother_track_trigger AFTER insert or update or delete on mother_track FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();
CREATE TRIGGER child_track_trigger AFTER insert or update or delete on child_track FOR EACH ROW EXECUTE PROCEDURE track_notify_trigger();

-- CREATE TRIGGER table1_trigger AFTER insert or update or delete on table1 execute procedure track_notify_trigger();
-- http://www.divillo.com/
-- HOWTO: Automatically Responding To PostgreSQL Table Changes With Twisted
