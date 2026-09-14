SECTORS = [
    "agriculture",
    "food_processing",
    "manufacturing",
    "textiles_apparel",
    "handicrafts",
    "retail",
    "services",
    "tech_it",
    "edtech",
    "healthcare",
    "construction",
    "transport",
    "tourism",
    "renewable_energy",
]

SUPPORT_TYPES = [
    "loan",
    "subsidy",
    "grant",
    "funding",
    "training",
    "mentorship",
    "equipment",
    "marketing",
    "insurance",
    "tax_benefit",
    "market_access",
]

BUSINESS_STAGES = ["idea", "planning", "existing", "expanding"]

ENTREPRENEUR_TYPES = ["general", "woman", "youth", "sc", "st", "obc", "minority", "pwd"]

GOVERNMENT_LEVELS = ["central", "state"]

AGE_GROUPS = ["18-25", "26-35", "36-45", "46-60", "60+"]

REVENUE_BANDS = ["none", "under_10l", "10l_50l", "50l_1cr", "above_1cr"]

SOCIAL_CATEGORIES = ["general", "obc", "sc", "st", "minority"]

MATCH_WEIGHTS = {
    "sector": 30,
    "support": 25,
    "location": 15,
    "stage": 10,
    "entrepreneur_type": 10,
    "description": 10,
    "registration": 5,
    "experience": 5,
}

STATE_KEYS = [
    "andhra_pradesh", "arunachal_pradesh", "assam", "bihar", "chhattisgarh",
    "delhi", "goa", "gujarat", "haryana", "himachal_pradesh", "jharkhand",
    "karnataka", "kerala", "madhya_pradesh", "maharashtra", "manipur",
    "meghalaya", "mizoram", "nagaland", "odisha", "punjab", "rajasthan",
    "sikkim", "tamil_nadu", "telangana", "tripura", "uttar_pradesh",
    "uttarakhand", "west_bengal",
]