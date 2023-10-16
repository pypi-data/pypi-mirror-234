from django.test import TestCase
from edc_constants.constants import FEMALE, MALE, NO, NOT_APPLICABLE, TBD, YES

from intecomm_eligibility.eligibility import ScreeningEligibility


class EligibilityTests(TestCase):
    @staticmethod
    def get_cleaned_data(**kwargs) -> dict:
        cleaned_data = dict(
            age_in_years=None,
            art_adherent=None,
            art_stable=None,
            art_unchanged_3m=None,
            dia_blood_pressure_avg=None,
            dia_blood_pressure_one=None,
            dia_blood_pressure_two=None,
            dm_complications=None,
            dm_dx=None,
            dm_dx_6m=None,
            excluded_by_bp_history=None,
            excluded_by_gluc_history=None,
            gender=None,
            hiv_dx=None,
            hiv_dx_6m=None,
            htn_complications=None,
            htn_dx=None,
            htn_dx_6m=None,
            in_care_6m=None,
            lives_nearby=None,
            pregnant=None,
            requires_acute_care=None,
            staying_nearby_6=None,
            sys_blood_pressure_avg=None,
            sys_blood_pressure_one=None,
            sys_blood_pressure_two=None,
            unsuitable_for_study=None,
            unsuitable_agreed=None,
        )
        cleaned_data.update(**kwargs)
        return cleaned_data

    @property
    def basic_data(self) -> dict:
        return dict(
            age_in_years=25,
            consent_ability=YES,
            excluded_by_bp_history=NO,
            excluded_by_gluc_history=NO,
            gender=MALE,
            hiv_dx=YES,
            hiv_dx_6m=YES,
            in_care_6m=YES,
            lives_nearby=YES,
            pregnant=NOT_APPLICABLE,
            requires_acute_care=NO,
            staying_nearby_6=YES,
            unsuitable_for_study=NO,
            unsuitable_agreed=NOT_APPLICABLE,
        )

    @property
    def bp_data(self) -> dict:
        return dict(
            sys_blood_pressure_one=140,
            sys_blood_pressure_two=140,
            dia_blood_pressure_one=90,
            dia_blood_pressure_two=90,
        )

    def test_ok(self):
        eligibility = ScreeningEligibility(cleaned_data=self.get_cleaned_data())
        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, TBD)
        self.assertNotEqual(eligibility.reasons_ineligible, {})

    def test_basic_attrs(self):
        # age_in_years
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(age_in_years=15)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("age_in_years", eligibility.reasons_ineligible)

        cleaned_data.update(age_in_years=25)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("age_in_years", eligibility.reasons_ineligible)

        # consent ability
        cleaned_data.update(consent_ability=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("consent_ability", eligibility.reasons_ineligible)

        # consent ability
        cleaned_data.update(consent_ability=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("consent_ability", eligibility.reasons_ineligible)

        # gender
        cleaned_data.update(gender=None)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("gender", eligibility.reasons_ineligible)

        cleaned_data.update(gender=MALE)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("gender", eligibility.reasons_ineligible)

        # in_care_6m
        cleaned_data.update(in_care_6m=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("in_care_6m", eligibility.reasons_ineligible)

        cleaned_data.update(in_care_6m=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("in_care_6m", eligibility.reasons_ineligible)

        # lives_nearby
        cleaned_data.update(lives_nearby=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("lives_nearby", eligibility.reasons_ineligible)

        cleaned_data.update(lives_nearby=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("lives_nearby", eligibility.reasons_ineligible)

        # staying_nearby_6
        cleaned_data.update(staying_nearby_6=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("staying_nearby_6", eligibility.reasons_ineligible)

        cleaned_data.update(staying_nearby_6=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("staying_nearby_6", eligibility.reasons_ineligible)

        # requires_acute_care
        cleaned_data.update(requires_acute_care=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("requires_acute_care", eligibility.reasons_ineligible)

        cleaned_data.update(requires_acute_care=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("requires_acute_care", eligibility.reasons_ineligible)

        # excluded_by_bp_history
        cleaned_data.update(excluded_by_bp_history=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("excluded_by_bp_history", eligibility.reasons_ineligible)

        cleaned_data.update(excluded_by_bp_history=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("excluded_by_bp_history", eligibility.reasons_ineligible)

        # excluded_by_gluc_history
        cleaned_data.update(excluded_by_gluc_history=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("excluded_by_gluc_history", eligibility.reasons_ineligible)

        cleaned_data.update(excluded_by_gluc_history=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("excluded_by_gluc_history", eligibility.reasons_ineligible)

        # unsuitable_for_study
        cleaned_data.update(unsuitable_for_study=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("unsuitable_for_study", eligibility.reasons_ineligible)
        self.assertIn("unsuitable_agreed", eligibility.reasons_ineligible)

        cleaned_data.update(unsuitable_for_study=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("unsuitable_for_study", eligibility.reasons_ineligible)

        # unsuitable_agreed
        cleaned_data.update(unsuitable_agreed=NOT_APPLICABLE)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("unsuitable_agreed", eligibility.reasons_ineligible)

        cleaned_data.update(unsuitable_for_study=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("unsuitable_for_study", eligibility.reasons_ineligible)

        cleaned_data.update(pregnant=NOT_APPLICABLE)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("pregnant", eligibility.reasons_ineligible)

        # has a condition
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("no_conditions", eligibility.reasons_ineligible)

        cleaned_data.update(hiv_dx=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("no_conditions", eligibility.reasons_ineligible)

        cleaned_data.update(hiv_dx=YES, hiv_dx_6m=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("no_conditions", eligibility.reasons_ineligible)

        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

    def test_bp(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(**self.basic_data)

        # BP not done
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("bp_not_done", eligibility.reasons_ineligible)

        cleaned_data.update(sys_blood_pressure_one=120)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("bp_not_done", eligibility.reasons_ineligible)

        cleaned_data.update(sys_blood_pressure_two=120)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("bp_not_done", eligibility.reasons_ineligible)

        cleaned_data.update(dia_blood_pressure_one=80)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("bp_not_done", eligibility.reasons_ineligible)

        cleaned_data.update(dia_blood_pressure_two=80)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("bp_not_done", eligibility.reasons_ineligible)

        # BP high
        cleaned_data.update(
            sys_blood_pressure_one=161,
            sys_blood_pressure_two=161,
            dia_blood_pressure_one=101,
            dia_blood_pressure_two=101,
        )
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("bp_high", eligibility.reasons_ineligible)

        cleaned_data.update(**self.bp_data)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("bp_high", eligibility.reasons_ineligible)

        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

    def test_conditions_hiv(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(**self.basic_data)
        cleaned_data.update(**self.bp_data)

        # HIV
        cleaned_data.update(hiv_dx=YES, hiv_dx_6m=None)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("hiv_dx_duration_unknown", eligibility.reasons_ineligible)

        cleaned_data.update(hiv_dx=YES, hiv_dx_6m=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("hiv_art_unknown", eligibility.reasons_ineligible)

        cleaned_data.update(hiv_dx=YES, hiv_dx_6m=YES, art_unchanged_3m=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("hiv_art_unknown", eligibility.reasons_ineligible)

        cleaned_data.update(hiv_dx=YES, hiv_dx_6m=YES, art_unchanged_3m=YES, art_stable=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("hiv_art_unknown", eligibility.reasons_ineligible)

        cleaned_data.update(
            hiv_dx=YES, hiv_dx_6m=YES, art_unchanged_3m=YES, art_stable=YES, art_adherent=YES
        )
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("hiv_art_unknown", eligibility.reasons_ineligible)

        cleaned_data.update(
            hiv_dx=YES, hiv_dx_6m=YES, art_unchanged_3m=NO, art_stable=YES, art_adherent=YES
        )
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("art_unchanged_3m", eligibility.reasons_ineligible)

        cleaned_data.update(
            hiv_dx=YES, hiv_dx_6m=YES, art_unchanged_3m=YES, art_stable=NO, art_adherent=YES
        )
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("art_stable", eligibility.reasons_ineligible)

        cleaned_data.update(
            hiv_dx=YES, hiv_dx_6m=YES, art_unchanged_3m=YES, art_stable=YES, art_adherent=NO
        )
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("art_adherent", eligibility.reasons_ineligible)

        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

    def test_conditions_dm(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(**self.basic_data)
        cleaned_data.update(**self.bp_data)

        cleaned_data.update(dm_dx=YES, dm_dx_6m=None)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("dm_dx_duration_unknown", eligibility.reasons_ineligible)
        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

        cleaned_data.update(dm_dx=YES, dm_dx_6m=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("dm_complications_unknown", eligibility.reasons_ineligible)
        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

        cleaned_data.update(dm_dx=YES, dm_dx_6m=YES, dm_complications=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("dm_complications", eligibility.reasons_ineligible)
        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

        cleaned_data.update(dm_dx=YES, dm_dx_6m=YES, dm_complications=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("dm_complications", eligibility.reasons_ineligible)
        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

    def test_conditions_htn(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(**self.basic_data)
        cleaned_data.update(**self.bp_data)

        cleaned_data.update(hiv_dx=NO, dm_dx=NO)

        cleaned_data.update(htn_dx=YES, htn_dx_6m=None)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("htn_dx_duration_unknown", eligibility.reasons_ineligible)
        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

        cleaned_data.update(htn_dx=YES, htn_dx_6m=YES, htn_complications=None)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("htn_complications_unknown", eligibility.reasons_ineligible)
        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

        cleaned_data.update(htn_dx=YES, htn_dx_6m=YES, htn_complications=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("htn_complications", eligibility.reasons_ineligible)
        self.assertFalse(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, NO)

        cleaned_data.update(htn_dx=YES, htn_dx_6m=YES, htn_complications=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("htn_complications", eligibility.reasons_ineligible)

        self.assertTrue(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, YES)

    def test_pregnant(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(**self.basic_data)
        cleaned_data.update(**self.bp_data)
        cleaned_data.update(hiv_dx=NO, dm_dx=NO)
        cleaned_data.update(htn_dx=YES, htn_dx_6m=YES, htn_complications=NO)

        # pregnant / MALE
        cleaned_data.update(gender=MALE, pregnant=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("pregnant", eligibility.reasons_ineligible)

        cleaned_data.update(gender=MALE, pregnant=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("pregnant", eligibility.reasons_ineligible)

        cleaned_data.update(gender=MALE, pregnant=NOT_APPLICABLE)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("pregnant", eligibility.reasons_ineligible)

        # pregnant / FEMALE
        cleaned_data.update(gender=FEMALE, pregnant=None)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("pregnant", eligibility.reasons_ineligible)

        cleaned_data.update(gender=FEMALE, pregnant=NOT_APPLICABLE)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("pregnant", eligibility.reasons_ineligible)

        cleaned_data.update(pregnant=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertNotIn("pregnant", eligibility.reasons_ineligible)

        cleaned_data.update(pregnant=YES)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertIn("pregnant", eligibility.reasons_ineligible)

    def test_eligible(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(**self.basic_data)
        cleaned_data.update(**self.bp_data)
        cleaned_data.update(hiv_dx=NO, dm_dx=NO)
        cleaned_data.update(htn_dx=YES, htn_dx_6m=YES, htn_complications=NO)
        eligibility = ScreeningEligibility(cleaned_data=cleaned_data)
        self.assertTrue(eligibility.is_eligible)
        self.assertEqual(eligibility.eligible, YES)
        self.assertEqual({}, eligibility.reasons_ineligible)
