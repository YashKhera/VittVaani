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

    def test_location_all_states(self):
        profile = make_profile(state="delhi")
        scheme = make_scheme(states=["all"])
        self.assertEqual(self.matcher.match_location(profile, scheme), 15)

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


if __name__ == "__main__":
    unittest.main()