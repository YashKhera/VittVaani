import unittest

from app.services.understanding_service import (
    _detect_sector,
    UnderstandingService,
)

fallback_understand = UnderstandingService().fallback_understand


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


class TestFallbackUnderstand(unittest.TestCase):
    def test_provider_neutral_keys(self):
        out = fallback_understand("I sell handicraft baskets and pottery")
        self.assertEqual(out["sector"], "handicrafts")
        self.assertTrue(out["summary_en"])
        self.assertTrue(out["summary_hi"])
        self.assertTrue(out["tags"])

    def test_empty_description(self):
        out = fallback_understand("")
        self.assertIsNone(out["sector"])
        self.assertTrue(out["summary_en"])


if __name__ == "__main__":
    unittest.main()