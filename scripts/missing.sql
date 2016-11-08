
ALTER TABLE rw_ancvisits ADD COLUMN symptom_fp text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_ja text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_ns text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_oe text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_pc text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_vo text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_di text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_ma text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_np text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_ch text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_hy text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_rb text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_sa text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_ds text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_fe text DEFAULT NULL;
ALTER TABLE rw_ancvisits ADD COLUMN symptom_af text DEFAULT NULL;

ALTER TABLE rw_redalerts ADD COLUMN child_number integer;
ALTER TABLE rw_redalerts ADD COLUMN birth_date timestamp without time zone;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_he text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_co text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_ap text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_la text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_mc text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_pa text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_ps text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_sc text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_sl text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_un text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_shb text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_sfh text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN postpartum_red_symptom_cop text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN postpartum_red_symptom_hfp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN postpartum_red_symptom_sbp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN postpartum_red_symptom_shp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN postpartum_red_symptom_bsp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_con text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_wu text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_hbt text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_lbt text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_fb text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_cdg text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_nuf text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_ucb text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_iuc text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_rv text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_ads text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_nsc text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_nbf text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_nhe text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_sp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN newborn_red_symptom_ys text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_cop text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_hfp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_sbp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_shp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_bsp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_con text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_wu text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_hbt text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_lbt text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_fb text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_cdg text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_nuf text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_ucb text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_iuc text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_rv text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_ads text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_nsc text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_nbf text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_nhe text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_sp text DEFAULT NULL;
ALTER TABLE rw_redalerts ADD COLUMN red_symptom_ys text DEFAULT NULL;


ALTER TABLE rw_redalerts ADD COLUMN child_id integer;
ALTER TABLE rw_redalerts ADD COLUMN mother_weight double precision;
ALTER TABLE rw_redalerts ADD COLUMN child_weight double precision;


ALTER TABLE redmessage ADD COLUMN child_number integer;
ALTER TABLE redmessage ADD COLUMN birth_date timestamp without time zone;
ALTER TABLE redmessage ADD COLUMN mother_weight double precision;
ALTER TABLE redmessage ADD COLUMN child_weight double precision;

ALTER TABLE redresultmessage ADD COLUMN child_number integer;
ALTER TABLE redresultmessage ADD COLUMN birth_date timestamp without time zone;


ALTER TABLE redresultmessage ADD COLUMN mc boolean DEFAULT FALSE;

ALTER TABLE mother_track ADD COLUMN pnc4 integer;
ALTER TABLE mother_track ADD COLUMN pnc5 integer;
ALTER TABLE rw_pregnancies ADD COLUMN muac double precision;
ALTER TABLE mother_track ADD COLUMN muac double precision;


