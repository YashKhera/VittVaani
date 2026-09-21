import unittest
from types import SimpleNamespace

from app.services.matching_service import AdvancedMatchingService


def make_profile(**kwargs):
    defaults = dict(
        business_sector="food_processing",
        state="maharashtra",
        business_stage="existing",
        annual_revenue="10l_50l",
        gender="female",
        social_category="obc",
        description=None,
        annual_family_income=None,
        education_status=None,
        estimated_project_cost=None,
        project_type=None,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults, requirements=[])


def make_scheme(**kwargs):
    defaults = dict(
        name="Test Scheme",
        description=None,
        benefits=[],
        department="",
        sectors=["food_processing"],
        states=["all"],
        business_stages=["existing"],
        support_types=["loan"],
        entrepreneur_types=["general", "woman"],
        eligibility=["Indian citizen 18+"],
        loan_min=100000,
        loan_max=10000000,
        processing_days=15,
        loan_category=None,
        channel_financed=False,
        interest_rate_min=None,
        interest_rate_max=None,
        moratorium_min_months=None,
        moratorium_max_months=None,
        max_coverage_pct=None,
        max_project_cost=None,
        tenure_min_months=None,
        tenure_max_months=None,
        income_ceiling=None,
        annual_family_income=None,
        education_status=None,
        estimated_project_cost=None,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


class TestAdvancedMatching(unittest.TestCase):
    def setUp(self):
        self.matcher = AdvancedMatchingService()

    def test_sector_match(self):
        profile = make_profile(business_sector="food_processing")
        scheme = make_scheme(sectors=["food_processing"])
        self.assertEqual(self.matcher.match_sector(profile, scheme), 30)
        scheme2 = make_scheme(sectors=["manufacturing"])
        self.assertEqual(self.matcher.match_sector(profile, scheme2), 0)

    def test_sector_match_all_sectors(self):
        profile = make_profile(business_sector="dairy")
        scheme = make_scheme(sectors=["all"])
        self.assertEqual(self.matcher.match_sector(profile, scheme), 18)

    def test_location_all_states(self):
        profile = make_profile(state="delhi")
        scheme = make_scheme(states=["all"])
        self.assertEqual(self.matcher.match_location(profile, scheme), 9)

    def test_location_state_specific(self):
        profile = make_profile(state="maharashtra")
        scheme = make_scheme(states=["maharashtra"])
        self.assertEqual(self.matcher.match_location(profile, scheme), 15)
        scheme2 = make_scheme(states=["kerala"])
        self.assertEqual(self.matcher.match_location(profile, scheme2), 0)

    def test_stage_mapping(self):
        profile = make_profile(business_stage="planning")
        scheme = make_scheme(business_stages=["planning"])
        self.assertEqual(self.matcher.match_stage(profile, scheme), 10)

    def test_entrepreneur_type_woman(self):
        profile = make_profile(gender="female", social_category="general")
        scheme = make_scheme(entrepreneur_types=["woman"])
        self.assertEqual(self.matcher.match_entrepreneur_type(profile, scheme), 10)

    def test_entrepreneur_type_sc(self):
        profile = make_profile(gender="male", social_category="sc")
        scheme = make_scheme(entrepreneur_types=["sc"])
        self.assertEqual(self.matcher.match_entrepreneur_type(profile, scheme), 10)

    def test_support_match(self):
        profile = make_profile()
        profile.requirements = [SimpleNamespace(support_type="loan")]
        scheme = make_scheme(support_types=["loan", "subsidy"])
        self.assertEqual(self.matcher.match_support(profile, scheme), 25)

    def test_level_thresholds(self):
        profile = make_profile()
        profile.requirements = [SimpleNamespace(support_type="loan")]
        scheme = make_scheme()
        match = self.matcher.calculate_match(profile, scheme)
        self.assertGreaterEqual(match["score"], 80)
        self.assertIn(match["level"], ["Excellent Match", "Strong Match"])
        self.assertIn("sector", match["matched_criteria"])

    def test_low_match_does_not_include_irrelevant(self):
        profile = make_profile(business_sector="tech_it", state="kerala", business_stage="expanding",
                               gender="male", social_category="general")
        profile.requirements = [SimpleNamespace(support_type="marketing")]
        scheme = make_scheme(sectors=["handicrafts"], states=["punjab"], business_stages=["planning"],
                             support_types=["loan"], entrepreneur_types=["sc"])
        match = self.matcher.calculate_match(profile, scheme)
        self.assertEqual(match["score"], 0)

    def test_rank_recommendations_top_results(self):
        profile = make_profile()
        profile.requirements = [SimpleNamespace(support_type="loan")]
        schemes = [make_scheme(name=f"S{i}", loan_max=10000000 + i) for i in range(5)]
        schemes[2].sectors = ["manufacturing"]
        schemes[2].states = ["kerala"]
        schemes[3].sectors = ["manufacturing"]
        schemes[3].states = ["kerala"]
        schemes[3].support_types = ["marketing"]
        ranked = self.matcher.rank_recommendations(profile, schemes)
        self.assertTrue(ranked)
        scores = [r["match_score"] for r in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertLessEqual(len(ranked), 15)

    def test_funding_range(self):
        profile = make_profile()
        profile.requirements = []
        scheme = make_scheme(loan_min=100000, loan_max=10000000)
        match = self.matcher.calculate_match(profile, scheme)
        self.assertEqual(match["score"] >= 40, True)

    def test_description_keyword_match_full(self):
        profile = make_profile(description="I run a spice making food business selling spices and pickles to groceries")
        scheme = make_scheme(
            description="Loan support for food processing units making spices and pickles.",
            benefits=["Subsidy for food processing machinery"],
            eligibility=["Food processing units"],
        )
        self.assertEqual(self.matcher.match_description(profile, scheme), 10)

    def test_description_keyword_match_partial(self):
        profile = make_profile(description="I make artisanal handicraft decor items")
        scheme = make_scheme(description="Handloom and handicraft clusters get loans")
        self.assertEqual(self.matcher.match_description(profile, scheme), 5)

    def test_description_no_match(self):
        profile = make_profile(description="I sell garments online to urban customers")
        scheme = make_scheme(description="Dairy farming equipment subsidies")
        self.assertEqual(self.matcher.match_description(profile, scheme), 0)

    def test_description_empty(self):
        profile = make_profile(description=None)
        scheme = make_scheme(description="Food processing loans")
        self.assertEqual(self.matcher.match_description(profile, scheme), 0)

    def test_gap_identification_high_loan(self):
        profile = make_profile(annual_revenue="under_10l")
        scheme = make_scheme(loan_min=1000000, loan_max=50000000)
        gap = self.matcher.identify_gap(profile, scheme)
        self.assertIsNotNone(gap)

    def test_hard_eligibility_blocks_general_user_from_sc_only_scheme(self):
        profile = make_profile(gender="male", social_category="general")
        scheme = make_scheme(entrepreneur_types=["sc"], loan_category=None)
        eligible, reason = self.matcher.hard_eligibility(profile, scheme)
        self.assertFalse(eligible)
        self.assertTrue(reason)

    def test_hard_eligibility_allows_sc_user_sc_only_scheme(self):
        profile = make_profile(gender="male", social_category="sc")
        scheme = make_scheme(entrepreneur_types=["sc"], loan_category=None)
        eligible, _ = self.matcher.hard_eligibility(profile, scheme)
        self.assertTrue(eligible)

    def test_hard_eligibility_gender_and_age_reserved(self):
        woman_scheme = make_scheme(entrepreneur_types=["woman"])
        eligible, _ = self.matcher.hard_eligibility(make_profile(gender="female", social_category="general"), woman_scheme)
        self.assertTrue(eligible)
        eligible2, _ = self.matcher.hard_eligibility(make_profile(gender="male", social_category="general"), woman_scheme)
        self.assertFalse(eligible2)

        youth_scheme = make_scheme(entrepreneur_types=["youth"])
        eligible3, _ = self.matcher.hard_eligibility(make_profile(gender="male", social_category="general", age_group="26-35"), youth_scheme)
        self.assertTrue(eligible3)
        eligible4, _ = self.matcher.hard_eligibility(make_profile(gender="male", social_category="general", age_group="60+"), youth_scheme)
        self.assertFalse(eligible4)

    def test_hard_eligibility_woman_gate_applies_to_combined_schemes(self):
        sc_woman_scheme = make_scheme(entrepreneur_types=["sc", "woman"])
        eligible, reason = self.matcher.hard_eligibility(make_profile(gender="male", social_category="sc"), sc_woman_scheme)
        self.assertFalse(eligible)
        self.assertTrue(reason)
        eligible2, _ = self.matcher.hard_eligibility(make_profile(gender="female", social_category="sc"), sc_woman_scheme)
        self.assertTrue(eligible2)
        woman_eligible = self.matcher.hard_eligibility(make_profile(gender="female", social_category="general"), sc_woman_scheme)
        self.assertTrue(woman_eligible[0])

    def test_hard_eligibility_woman_gate_open_schemes_unaffected(self):
        open_scheme = make_scheme(entrepreneur_types=["general", "woman"])
        eligible, _ = self.matcher.hard_eligibility(make_profile(gender="male", social_category="general"), open_scheme)
        self.assertTrue(eligible)

    def test_hard_eligibility_pwd_category(self):
        pwd_scheme = make_scheme(entrepreneur_types=["pwd"])
        eligible, _ = self.matcher.hard_eligibility(make_profile(gender="male", social_category="pwd"), pwd_scheme)
        self.assertTrue(eligible)
        eligible2, _ = self.matcher.hard_eligibility(make_profile(gender="male", social_category="general"), pwd_scheme)
        self.assertFalse(eligible2)

    def test_sector_specific_scheme_outranks_generic(self):
        profile = make_profile(business_sector="food_processing", state="maharashtra")
        profile.requirements = [SimpleNamespace(support_type="loan")]
        generic = make_scheme(name="GenericAll", sectors=["all"], states=["all"], business_stages=["existing"], entrepreneur_types=["general"])
        specific = make_scheme(name="SectorSpecific", sectors=["food_processing"], states=["all"], business_stages=["existing"], entrepreneur_types=["general"])
        ranked = self.matcher.rank_recommendations(profile, [generic, specific])
        self.assertEqual(ranked[0]["scheme"].name, "SectorSpecific")

    def test_state_specificity_orders_by_user_state(self):
        def with_req(state):
            p = make_profile(state=state)
            p.requirements = [SimpleNamespace(support_type="loan")]
            return p
        national = make_scheme(name="National", sectors=["all"], states=["all"], business_stages=["existing"], entrepreneur_types=["general"])
        local = make_scheme(name="StateSpecific", sectors=["all"], states=["maharashtra"], business_stages=["existing"], entrepreneur_types=["general"])
        order_mah = [r["scheme"].name for r in self.matcher.rank_recommendations(with_req("maharashtra"), [national, local])]
        order_ker = [r["scheme"].name for r in self.matcher.rank_recommendations(with_req("kerala"), [national, local])]
        self.assertEqual(order_mah, ["StateSpecific", "National"])
        self.assertEqual(order_ker, ["National"])


class TestProjectCostTiering(unittest.TestCase):
    def setUp(self):
        self.matcher = AdvancedMatchingService()

    def test_ideal_loan_category_by_cost(self):
        micro = make_profile(gender="male", social_category="sc", estimated_project_cost=100000)
        term = make_profile(gender="male", social_category="sc", estimated_project_cost=300000)
        large = make_profile(gender="male", social_category="sc", estimated_project_cost=6000000)
        unknown = make_profile(gender="male", social_category="sc")
        self.assertEqual(self.matcher.ideal_loan_category(micro), "micro_finance")
        self.assertEqual(self.matcher.ideal_loan_category(term), "term_loan")
        self.assertIsNone(self.matcher.ideal_loan_category(large))
        self.assertIsNone(self.matcher.ideal_loan_category(unknown))

    def test_education_project_type_maps_to_education_loan(self):
        profile = make_profile(project_type="education", estimated_project_cost=300000)
        self.assertEqual(self.matcher.ideal_loan_category(profile), "education")

    def test_project_type_defaults_to_business(self):
        self.assertEqual(self.matcher.project_type(make_profile(project_type="education")), "education")
        self.assertEqual(self.matcher.project_type(make_profile()), "business")

    def test_tier_match_boosts_correct_loan_category(self):
        micro_scheme = make_scheme(loan_category="micro_finance", entrepreneur_types=["sc", "general"])
        term_scheme = make_scheme(loan_category="term_loan", entrepreneur_types=["sc", "general"])
        edu_scheme = make_scheme(loan_category="education", entrepreneur_types=["sc", "general"])

        small_biz = make_profile(gender="male", social_category="sc", estimated_project_cost=100000)
        self.assertEqual(self.matcher.match_tier(small_biz, micro_scheme), 8)
        self.assertEqual(self.matcher.match_tier(small_biz, term_scheme), 0)

        large_biz = make_profile(gender="male", social_category="sc", estimated_project_cost=300000)
        self.assertEqual(self.matcher.match_tier(large_biz, micro_scheme), 0)
        self.assertEqual(self.matcher.match_tier(large_biz, term_scheme), 8)

        student = make_profile(gender="male", social_category="sc", project_type="education",
                               education_status="undergraduate", business_sector="education")
        self.assertEqual(self.matcher.match_tier(student, edu_scheme), 8)
        self.assertEqual(self.matcher.match_tier(student, micro_scheme), 0)

    def test_no_tier_boost_for_schemes_without_loan_category(self):
        profile = make_profile(estimated_project_cost=100000)
        scheme = make_scheme(loan_category=None)
        self.assertEqual(self.matcher.match_tier(profile, scheme), 0)

    def test_breakdown_includes_tier_match(self):
        profile = make_profile(gender="male", social_category="sc", estimated_project_cost=100000)
        profile.requirements = [SimpleNamespace(support_type="loan")]
        micro_scheme = make_scheme(loan_category="micro_finance", entrepreneur_types=["sc", "general"])
        match = self.matcher.calculate_match(profile, micro_scheme)
        self.assertEqual(match["breakdown"]["tier_match"], 8)
        self.assertIn("loan tier (project size / type)", match["matched_criteria"])

    def test_rank_recommendations_puts_aligned_tier_first(self):
        profile = make_profile(gender="male", social_category="sc", business_sector="food_processing",
                               state="maharashtra", business_stage="existing", estimated_project_cost=100000)
        profile.requirements = [SimpleNamespace(support_type="loan")]
        micro_scheme = make_scheme(name="Micro", loan_category="micro_finance", sectors=["all"],
                                   states=["all"], business_stages=["existing"], entrepreneur_types=["sc", "general"])
        term_scheme = make_scheme(name="Term", loan_category="term_loan", sectors=["all"],
                                  states=["all"], business_stages=["existing"], entrepreneur_types=["sc", "general"])
        ranked = self.matcher.rank_recommendations(profile, [micro_scheme, term_scheme])
        self.assertEqual(ranked[0]["scheme"].name, "Micro")
        self.assertGreater(ranked[0]["match_score"], ranked[1]["match_score"])

    def test_education_gate_allows_project_type_education(self):
        profile = make_profile(gender="male", social_category="sc", project_type="education",
                               education_status="not_applicable", business_sector="handicrafts")
        scheme = make_scheme(loan_category="education", entrepreneur_types=["sc", "general"])
        eligible, reason = self.matcher.hard_eligibility(profile, scheme)
        self.assertTrue(eligible, reason)

    def test_education_gate_blocks_tuition_business(self):
        profile = make_profile(gender="male", social_category="sc", project_type="business",
                               education_status="not_applicable", business_sector="education")
        scheme = make_scheme(loan_category="education", entrepreneur_types=["sc", "general"])
        eligible, _ = self.matcher.hard_eligibility(profile, scheme)
        self.assertFalse(eligible)


if __name__ == "__main__":
    unittest.main()