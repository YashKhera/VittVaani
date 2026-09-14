import unittest

from data.schemes_seed import build_schemes, SCHEMES
from app.utils.constants import SECTORS, SUPPORT_TYPES


class TestSeedCatalog(unittest.TestCase):
    def test_catalog_size(self):
        self.assertGreaterEqual(len(SCHEMES), 60)

    def test_catalog_entries_well_formed(self):
        for name, _short, level, dept, sectors, states, stages, supports, types, mn, mx, days, url in SCHEMES:
            self.assertTrue(name)
            self.assertTrue(dept)
            self.assertIn(level, ["central", "state"])
            self.assertTrue(sectors)
            self.assertTrue(states)
            self.assertTrue(stages)
            self.assertTrue(supports)
            self.assertTrue(types)
            self.assertIsInstance(mn, int)
            self.assertIsInstance(mx, int)
            self.assertIsInstance(days, int)

    def test_government_level_coverage(self):
        levels = {s[2] for s in SCHEMES}
        self.assertIn("central", levels)
        self.assertIn("state", levels)

    def test_sector_keys_valid(self):
        for entry in SCHEMES:
            for sector in entry[4]:
                self.assertIn(sector, SECTORS + ["all"])

    def test_support_keys_valid(self):
        for entry in SCHEMES:
            for support in entry[7]:
                self.assertIn(support, SUPPORT_TYPES)

    def test_build_schemes_maps_fields(self):
        built = build_schemes()
        self.assertEqual(len(built), len(SCHEMES))
        first = built[0]
        for key in ["name", "government_level", "department", "sectors", "states",
                    "business_stages", "support_types", "entrepreneur_types",
                    "benefits", "eligibility", "documents", "loan_min", "loan_max",
                    "processing_days", "official_url", "application_url", "description"]:
            self.assertIn(key, first)
        self.assertIsInstance(first["benefits"], list)
        self.assertIsInstance(first["documents"], list)
        self.assertIn("Aadhaar Card", first["documents"])


if __name__ == "__main__":
    unittest.main()