import unittest

from app.services.gemini_client import is_live_model
from app.services.understanding_service import (
    _detect_project_type,
    _detect_sector,
    _detect_stage,
    _detect_support_needs,
    UnderstandingService,
)

fallback_understand = UnderstandingService().fallback_understand


class TestModelRouting(unittest.TestCase):
    def test_live_model_matches(self):
        self.assertTrue(is_live_model("gemini-2.5-flash-preview-native-audio-dialog"))
        self.assertTrue(is_live_model("gemini-3.1-flash-live-preview"))
        self.assertTrue(is_live_model("gemini-2.5-flash-native-audio-preview-12-2025"))

    def test_non_live_model_does_not_match(self):
        self.assertFalse(is_live_model("gemini-3.6-flash"))
        self.assertFalse(is_live_model("antigravity-preview-09-2026"))
        self.assertFalse(is_live_model(""))
        self.assertFalse(is_live_model(None))


class TestSectorDetection(unittest.TestCase):
    def test_clear_english(self):
        cases = [
            ("I run a dairy farm with cows and sell milk", "dairy"),
            ("I make pickle namkeen and snacks at home", "food_processing"),
            ("I want an education loan to study further", "education"),
            ("We sell sarees and apparel in our shop", "textile"),
            ("Coaching classes and tuition for students", "education"),
            ("Solar panel installation and inverter supply", "solar_energy"),
        ]
        for desc, expected in cases:
            self.assertEqual(_detect_sector(desc), expected, desc)

    def test_ambiguity_disambiguation(self):
        self.assertEqual(_detect_sector("I do house renovation and construction"), "construction")
        self.assertEqual(_detect_sector("I repair mobile phones and laptops"), "electronics")
        self.assertEqual(_detect_sector("I have an online store selling clothes"), "ecommerce")

    def test_multiword_phrase_outranks_single_words(self):
        self.assertEqual(_detect_sector("real estate construction business"), "construction")
        self.assertEqual(_detect_sector("mobile repair shop"), "electronics")

    def test_no_match_returns_none(self):
        self.assertIsNone(_detect_sector(""))
        self.assertIsNone(_detect_sector("hello world this is a test"))
        self.assertIsNone(_detect_sector(None))

    def test_stopword_text_no_false_sector(self):
        desc = "i want need help with my business start small day"
        self.assertIsNone(_detect_sector(desc))


class TestStageDetection(unittest.TestCase):
    def test_existing_stage(self):
        self.assertEqual(_detect_stage("I run a dairy farm since 3 years"), "existing")
        self.assertEqual(_detect_stage("mera business chal raha hai 2 saal se"), "existing")
        self.assertEqual(_detect_stage("already running for last 6 months"), "existing")

    def test_new_stage(self):
        self.assertEqual(_detect_stage("I want to start a bakery business"), "new")
        self.assertEqual(_detect_stage("planning to open a tuition centre"), "new")
        self.assertEqual(_detect_stage("main restaurant shuru karna chahta hoon"), "new")

    def test_ambiguous_returns_none(self):
        self.assertIsNone(_detect_stage(""))
        self.assertIsNone(_detect_stage("I have a shop"))
        self.assertIsNone(_detect_stage(None))


class TestSupportNeedsDetection(unittest.TestCase):
    def test_loan_and_training(self):
        needs = _detect_support_needs("I want a loan for the shop and training for my workers")
        self.assertIn("capital", needs)
        self.assertIn("training", needs)

    def test_subsidy_and_marketing(self):
        needs = _detect_support_needs("need subsidy and help selling my products online")
        self.assertIn("subsidy", needs)
        self.assertIn("marketing", needs)

    def test_legal_and_tech(self):
        needs = _detect_support_needs("need GST registration and a computer machine")
        self.assertIn("legal", needs)
        self.assertIn("tech", needs)

    def test_empty(self):
        self.assertEqual(_detect_support_needs(""), [])
        self.assertEqual(_detect_support_needs(None), [])


class TestProjectTypeDetection(unittest.TestCase):
    def test_self_study_intent_is_education(self):
        cases = [
            "I want an education loan to study further",
            "loan for my college degree",
            "I am studying BSc nursing and need fees help",
            "want admission in university, need money for fees",
            "padhai ke liye loan chahiye",
        ]
        for desc in cases:
            self.assertEqual(_detect_project_type(desc), "education", desc)

    def test_business_default(self):
        cases = [
            "I make pickles and namkeen in my small kitchen",
            "I run a dairy selling milk and ghee",
            "I want to start a bakery business",
            "I sell sarees and apparel online",
        ]
        for desc in cases:
            self.assertEqual(_detect_project_type(desc), "business", desc)

    def test_teaching_centre_is_business_not_education(self):
        cases = [
            "I run a coaching centre for students",
            "planning to open tuition classes",
            "I want to start a training institute",
            "I teach computer classes in my village",
        ]
        for desc in cases:
            self.assertEqual(_detect_project_type(desc), "business", desc)

    def test_empty_and_none(self):
        self.assertIsNone(_detect_project_type(""))
        self.assertIsNone(_detect_project_type(None))


class TestFallbackUnderstandProjectType(unittest.TestCase):
    def test_fallback_returns_project_type(self):
        out = fallback_understand("I want a loan to study nursing in college")
        self.assertEqual(out["project_type"], "education")
        out2 = fallback_understand("I run a coaching centre near my school")
        self.assertEqual(out2["project_type"], "business")

    def test_empty_description_returns_none_project_type(self):
        out = fallback_understand("")
        self.assertIsNone(out["project_type"])


class TestFallbackUnderstand(unittest.TestCase):
    def test_provider_neutral_keys(self):
        out = fallback_understand("I sell handicraft baskets and pottery")
        self.assertEqual(out["sector"], "handicrafts")
        self.assertTrue(out["summary_en"])
        self.assertTrue(out["summary_hi"])
        self.assertTrue(out["tags"])

    def test_extracted_stage_and_needs(self):
        out = fallback_understand("I run a dairy since 3 years and want a loan to buy a milking machine")
        self.assertEqual(out["stage"], "existing")
        self.assertIn("capital", out["support_needs"])
        self.assertIn("tech", out["support_needs"])

    def test_empty_description(self):
        out = fallback_understand("")
        self.assertIsNone(out["sector"])
        self.assertTrue(out["summary_en"])


if __name__ == "__main__":
    unittest.main()