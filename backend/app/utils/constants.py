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
    "education",
    "dairy",
    "ecommerce",
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

LOAN_CATEGORIES = ["micro_finance", "term_loan", "education"]

# Annual family income bands -> income value in INR used to compare with
# scheme income ceilings. "above_5l" maps to a sentinel huge value so any
# realistic ceiling disqualifies the applicant.
FAMILY_INCOME_BANDS = {
    "under_2.5l": 250000,
    "2.5l_5l": 500000,
    "above_5l": 10**9,
}

EDUCATION_STATUSES = [
    "not_applicable",
    "school",
    "diploma",
    "undergraduate",
    "postgraduate",
    "research",
]

# Indicative project-cost ceilings (INR) per loan category used for tiering/sizing.
LOAN_CATEGORY_COST_CEILING = {
    "micro_finance": 140000,
    "term_loan": 5000000,
    "education": None,
}

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