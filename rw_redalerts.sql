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
-- Name: rw_redalerts; Type: TABLE; Schema: public; Owner: thousanddays; Tablespace: 
--

CREATE TABLE rw_redalerts (
    indexcol integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    indangamuntu text,
    report_date timestamp without time zone,
    nation_pk integer,
    cell_pk integer,
    mother_id integer,
    reporter_phone text,
    district_pk integer,
    province_pk integer,
    village_pk integer,
    pregnancy_id integer,
    health_center_pk integer,
    sector_pk integer,
    reporter_pk integer,
    red_symptom_he text,
    referral_hospital_pk integer,
    mother_weight double precision,
    location text,
    intervention_field text,
    emergency_date timestamp without time zone,
    health_status boolean,
    red_symptom_co text,
    red_symptom_ps text,
    red_symptom_ap text,
    red_symptom_la text,
    red_symptom_mc text,
    red_symptom_pa text,
    red_symptom_sc text,
    red_symptom_sl text,
    red_symptom_un text
);


ALTER TABLE public.rw_redalerts OWNER TO thousanddays;

--
-- Name: rw_redalerts_indexcol_seq; Type: SEQUENCE; Schema: public; Owner: thousanddays
--

CREATE SEQUENCE rw_redalerts_indexcol_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rw_redalerts_indexcol_seq OWNER TO thousanddays;

--
-- Name: rw_redalerts_indexcol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: thousanddays
--

ALTER SEQUENCE rw_redalerts_indexcol_seq OWNED BY rw_redalerts.indexcol;


--
-- Name: indexcol; Type: DEFAULT; Schema: public; Owner: thousanddays
--

ALTER TABLE ONLY rw_redalerts ALTER COLUMN indexcol SET DEFAULT nextval('rw_redalerts_indexcol_seq'::regclass);


--
-- Data for Name: rw_redalerts; Type: TABLE DATA; Schema: public; Owner: thousanddays
--

INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (1, '2015-03-09 16:52:13.517526', '1234567890121456', '2015-03-09 16:52:12.235374', 2, 2243, 2, '+250788660270', 31, 6, 16405, 2, 571, 417, 4206, 'HE', 46, 55, 'HO', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (2, '2015-03-14 11:45:00.604112', '1198870086996039', '2015-03-14 11:44:59.81693', 2, 2243, 34, '+250788660270', 31, 6, 16405, 34, 571, 417, 4206, 'he', 46, NULL, 'hp', 'AL', '2015-03-09 00:00:00', true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (3, '2015-03-14 12:31:27.446897', '1204507803102450', '2015-03-14 12:31:26.984464', 2, 2243, 9, '+250788660270', 31, 6, 16405, 9, 571, 417, 4206, NULL, 46, 55, 'ho', NULL, NULL, NULL, 'co', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (4, '2015-03-14 12:34:39.636589', '1204507803102450', '2015-03-14 12:34:39.213578', 2, 2243, 9, '+250788660270', 31, 6, 16405, 9, 571, 417, 4206, 'he', 46, NULL, 'hp', 'AL', '2015-03-14 00:00:00', true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (5, '2015-03-14 12:44:48.555973', '1198070128433071', '2015-03-14 12:44:48.184066', 2, 2243, 94, '+250788660270', 31, 6, 16405, 95, 571, 417, 4206, NULL, 46, 55, 'ho', NULL, NULL, NULL, 'co', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (6, '2015-03-14 12:46:05.790001', '1198070128433071', '2015-03-14 12:46:05.3977', 2, 2243, 94, '+250788660270', 31, 6, 16405, 95, 571, 417, 4206, 'he', 46, NULL, 'hp', 'AL', '2015-03-14 00:00:00', true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (7, '2015-03-14 12:47:38.760446', '0782930255260814', '2015-03-14 12:47:38.467571', 2, 2243, 93, '+250788660270', 31, 6, 16405, 94, 571, 417, 4206, NULL, 46, 55, 'ho', NULL, NULL, NULL, 'co', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (8, '2015-03-14 13:06:15.792139', '0782930255260814', '2015-03-14 13:06:15.355238', 2, 2243, 93, '+250788660270', 31, 6, 16405, 94, 571, 417, 4206, 'he', 46, NULL, 'hp', 'AL', '2015-03-14 00:00:00', true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (9, '2015-03-14 13:08:51.179812', '1198970146072037', '2015-03-14 13:08:49.98718', 2, 2243, 67, '+250788660270', 31, 6, 16405, 67, 571, 417, 4206, NULL, 46, 55, 'ho', NULL, NULL, NULL, 'co', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (10, '2015-03-14 13:10:54.463623', '1198970146072037', '2015-03-14 13:10:54.02695', 2, 2243, 67, '+250788660270', 31, 6, 16405, 67, 571, 417, 4206, 'he', 46, NULL, 'hp', 'AL', '2015-03-14 00:00:00', true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (11, '2015-03-14 13:16:55.68079', '1197270070624085', '2015-03-14 13:16:55.353279', 2, 2243, 65, '+250788660270', 31, 6, 16405, 65, 571, 417, 4206, NULL, 46, 55, 'ho', NULL, NULL, NULL, 'co', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (12, '2015-03-14 13:17:39.055313', '1197270070624085', '2015-03-14 13:17:38.67085', 2, 2243, 65, '+250788660270', 31, 6, 16405, 65, 571, 417, 4206, 'he', 46, NULL, 'hp', 'AL', '2015-03-14 00:00:00', true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO rw_redalerts (indexcol, created_at, indangamuntu, report_date, nation_pk, cell_pk, mother_id, reporter_phone, district_pk, province_pk, village_pk, pregnancy_id, health_center_pk, sector_pk, reporter_pk, red_symptom_he, referral_hospital_pk, mother_weight, location, intervention_field, emergency_date, health_status, red_symptom_co, red_symptom_ps, red_symptom_ap, red_symptom_la, red_symptom_mc, red_symptom_pa, red_symptom_sc, red_symptom_sl, red_symptom_un) VALUES (13, '2015-03-14 13:20:35.075045', '1197870038408005', '2015-03-14 13:20:34.76867', 2, 2243, 64, '+250788660270', 31, 6, 16405, 64, 571, 417, 4206, NULL, 46, 55, 'ho', NULL, NULL, NULL, 'co', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);


--
-- Name: rw_redalerts_indexcol_seq; Type: SEQUENCE SET; Schema: public; Owner: thousanddays
--

SELECT pg_catalog.setval('rw_redalerts_indexcol_seq', 13, true);


--
-- PostgreSQL database dump complete
--

