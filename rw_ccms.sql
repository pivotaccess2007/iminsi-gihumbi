--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: rw_ccms; Type: TABLE; Schema: public; Owner: thousanddays; Tablespace: 
--

CREATE TABLE rw_ccms (
    indexcol integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    indangamuntu text,
    child_id integer,
    report_date timestamp without time zone,
    muac double precision,
    village_pk integer,
    cell_pk integer,
    mother_id integer,
    reporter_phone text,
    symptom_pc text,
    district_pk integer,
    child_number integer,
    nation_pk integer,
    symptom_ib text,
    symptom_ma text,
    province_pk integer,
    symptom_oi text,
    symptom_db text,
    intervention_field text,
    health_center_pk integer,
    sector_pk integer,
    symptom_di text,
    reporter_pk integer,
    referral_hospital_pk integer,
    birth_date timestamp without time zone,
    health_status boolean
);


ALTER TABLE public.rw_ccms OWNER TO thousanddays;

--
-- Name: rw_ccms_indexcol_seq; Type: SEQUENCE; Schema: public; Owner: thousanddays
--

CREATE SEQUENCE rw_ccms_indexcol_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rw_ccms_indexcol_seq OWNER TO thousanddays;

--
-- Name: rw_ccms_indexcol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: thousanddays
--

ALTER SEQUENCE rw_ccms_indexcol_seq OWNED BY rw_ccms.indexcol;


--
-- Name: indexcol; Type: DEFAULT; Schema: public; Owner: thousanddays
--

ALTER TABLE ONLY rw_ccms ALTER COLUMN indexcol SET DEFAULT nextval('rw_ccms_indexcol_seq'::regclass);


--
-- Data for Name: rw_ccms; Type: TABLE DATA; Schema: public; Owner: thousanddays
--

INSERT INTO rw_ccms (indexcol, created_at, indangamuntu, child_id, report_date, muac, village_pk, cell_pk, mother_id, reporter_phone, symptom_pc, district_pk, child_number, nation_pk, symptom_ib, symptom_ma, province_pk, symptom_oi, symptom_db, intervention_field, health_center_pk, sector_pk, symptom_di, reporter_pk, referral_hospital_pk, birth_date, health_status) VALUES (1, '2015-04-15 11:12:23.693657', '1003565890123456', 5, '2015-04-15 11:12:19.517496', 5.20000000000000018, 16405, 2243, 89, '+250788660270', 'PC', 31, 2, 2, 'IB', 'MA', 6, 'OI', 'DB', 'PR', 571, 417, 'DI', 4206, 46, '2015-03-13 00:00:00', NULL);
INSERT INTO rw_ccms (indexcol, created_at, indangamuntu, child_id, report_date, muac, village_pk, cell_pk, mother_id, reporter_phone, symptom_pc, district_pk, child_number, nation_pk, symptom_ib, symptom_ma, province_pk, symptom_oi, symptom_db, intervention_field, health_center_pk, sector_pk, symptom_di, reporter_pk, referral_hospital_pk, birth_date, health_status) VALUES (2, '2015-04-15 11:14:15.959231', '1003565890123456', 5, '2015-04-15 11:14:14.008871', NULL, 16405, 2243, 89, '+250788660270', 'PC', 31, 2, 2, 'IB', 'MA', 6, 'OI', 'DB', 'PR', 571, 417, 'DI', 4206, 46, '2015-03-13 00:00:00', true);


--
-- Name: rw_ccms_indexcol_seq; Type: SEQUENCE SET; Schema: public; Owner: thousanddays
--

SELECT pg_catalog.setval('rw_ccms_indexcol_seq', 2, true);


--
-- PostgreSQL database dump complete
--

