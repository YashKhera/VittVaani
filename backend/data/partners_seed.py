"""Seed data: channel partners (SCAs, PSBs, RRBs, NBFC-MFIs) across India."""

import os
import random
import sys

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (name, partner_type, state, city, district, pincode, lat, lng,
#  loan_categories, fund_utilization_pct, npa_pct, overdue_pct, phone)
PARTNERS = [
    # ---------------- MAHARASHTRA ----------------
    ("Maharashtra State SC Finance & Dev Corp – Mumbai RO", "sca", "maharashtra", "Mumbai", "Mumbai Suburban", "400001", 19.0760, 72.8777, ["micro_finance", "term_loan", "education"], 82.4, 4.2, 6.1, "022-22662632"),
    ("State Bank of India – Mumbai LHO", "psb", "maharashtra", "Mumbai", "Mumbai Suburban", "400021", 19.0596, 72.8295, ["micro_finance", "term_loan", "education"], 91.0, 5.5, 7.8, "022-22741342"),
    ("Bank of India – Nariman Point", "psb", "maharashtra", "Mumbai", "Mumbai Suburban", "400021", 18.9322, 72.8265, ["micro_finance", "term_loan"], 88.7, 6.3, 8.9, "022-22022415"),
    ("Vidarbha Konkan Gramin Bank – Nagpur", "rrb", "maharashtra", "Nagpur", "Nagpur", "440001", 21.1458, 79.0882, ["micro_finance", "term_loan"], 74.5, 3.1, 5.4, "0712-2533410"),
    ("Union Bank of India – Pune", "psb", "maharashtra", "Pune", "Pune", "411001", 18.5204, 73.8567, ["micro_finance", "term_loan"], 79.8, 4.8, 7.2, "020-25535356"),
    ("Concordia MFI – Pune", "nbfc_mfi", "maharashtra", "Pune", "Pune", "411030", 18.5236, 73.9166, ["micro_finance"], 96.2, 1.8, 2.9, "020-27444861"),
    ("Sahayog Link Office – Nashik", "nbfc_mfi", "maharashtra", "Nashik", "Nashik", "422001", 19.9975, 73.7898, ["micro_finance", "term_loan"], 71.3, 2.4, 4.1, "0253-2314470"),
    ("Bank of Baroda – Thane", "psb", "maharashtra", "Thane", "Thane", "400601", 19.2183, 72.9781, ["micro_finance", "term_loan", "education"], 84.1, 5.0, 7.5, "022-25346427"),

    # ---------------- DELHI ----------------
    ("Delhi SC & OBC Finance & Dev Corp – Delhi HO", "sca", "delhi", "New Delhi", "New Delhi", "110001", 28.6139, 77.2090, ["micro_finance", "term_loan"], 68.9, 6.8, 9.3, "011-23383310"),
    ("Punjab National Bank – Connaught Place", "psb", "delhi", "New Delhi", "New Delhi", "110001", 28.6328, 77.2197, ["micro_finance", "term_loan", "education"], 92.5, 4.4, 6.0, "011-23418155"),
    ("Canara Bank – Barakhamba Rd", "psb", "delhi", "New Delhi", "New Delhi", "110001", 28.6270, 77.2175, ["micro_finance", "term_loan"], 86.0, 4.9, 7.1, "011-23316362"),
    ("Satin Creditcare – Dwarka", "nbfc_mfi", "delhi", "New Delhi", "South West Delhi", "110075", 28.5921, 77.0460, ["micro_finance"], 93.4, 2.2, 3.4, "011-28067782"),

    # ---------------- TAMIL NADU ----------------
    ("Tamil Nadu SC Finance & Dev Corp – Chennai", "sca", "tamil_nadu", "Chennai", "Chennai", "600001", 13.0827, 80.2707, ["micro_finance", "term_loan"], 77.2, 3.6, 5.5, "044-25224162"),
    ("Indian Overseas Bank – Anna Salai", "psb", "tamil_nadu", "Chennai", "Chennai", "600002", 13.0827, 80.2707, ["micro_finance", "term_loan", "education"], 89.1, 7.2, 9.8, "044-28514913"),
    ("Gramalaya Microfin – Trichy", "nbfc_mfi", "tamil_nadu", "Tiruchirappalli", "Tiruchirappalli", "620001", 10.7905, 78.7047, ["micro_finance"], 95.0, 1.5, 2.6, "0431-4020250"),
    ("Pallavan Grama Bank – Madurai", "rrb", "tamil_nadu", "Madurai", "Madurai", "625001", 9.9252, 78.1198, ["micro_finance", "term_loan"], 72.8, 3.9, 6.0, "0452-2740100"),

    # ---------------- KARNATAKA ----------------
    ("Karnataka SC/ST Finance & Dev Corp – Bengaluru", "sca", "karnataka", "Bengaluru", "Bengaluru Urban", "560001", 12.9716, 77.5946, ["micro_finance", "term_loan"], 80.5, 4.0, 5.8, "080-22232144"),
    ("State Bank of India – Bengaluru LHO", "psb", "karnataka", "Bengaluru", "Bengaluru Urban", "560001", 12.9756, 77.5907, ["micro_finance", "term_loan", "education"], 90.2, 5.2, 7.4, "080-25582500"),
    ("Karnataka Vikas Grameena Bank – Dharwad", "rrb", "karnataka", "Hubballi", "Dharwad", "580020", 15.3647, 75.1240, ["micro_finance", "term_loan"], 77.9, 3.3, 5.1, "0836-2358021"),
    ("Arohan Financial – Mysuru", "nbfc_mfi", "karnataka", "Mysuru", "Mysuru", "570001", 12.2958, 76.6394, ["micro_finance"], 94.1, 2.0, 3.2, "0821-2516489"),

    # ---------------- WEST BENGAL ----------------
    ("West Bengal SC/ST Finance & Dev Corp – Kolkata", "sca", "west_bengal", "Kolkata", "Kolkata", "700001", 22.5726, 88.3639, ["micro_finance", "term_loan"], 70.4, 7.0, 9.6, "033-22486163"),
    ("UCO Bank – Dalhousie Square", "psb", "west_bengal", "Kolkata", "Kolkata", "700001", 22.5726, 88.3639, ["micro_finance", "term_loan", "education"], 85.6, 6.6, 9.0, "033-22305390"),
    ("Bandhan Microfinance – Salt Lake", "nbfc_mfi", "west_bengal", "Kolkata", "North 24 Parganas", "700091", 22.5847, 88.4189, ["micro_finance"], 97.0, 1.2, 2.0, "033-23587542"),
    ("Bangiya Gramin Vikash Bank – Siliguri", "rrb", "west_bengal", "Siliguri", "Darjeeling", "734001", 26.7271, 88.3953, ["micro_finance", "term_loan"], 75.3, 4.5, 6.9, "0353-2431106"),

    # ---------------- UTTAR PRADESH ----------------
    ("Uttar Pradesh SC Finance & Dev Corp – Lucknow", "sca", "uttar_pradesh", "Lucknow", "Lucknow", "226001", 26.8467, 80.9462, ["micro_finance", "term_loan"], 66.0, 8.5, 11.2, "0522-2238056"),
    ("Bank of Baroda – Lucknow", "psb", "uttar_pradesh", "Lucknow", "Lucknow", "226001", 26.8467, 80.9462, ["micro_finance", "term_loan", "education"], 87.4, 6.0, 8.3, "0522-2206130"),
    ("Pratiyogita Gramin Bank – Varanasi", "rrb", "uttar_pradesh", "Varanasi", "Varanasi", "221001", 25.3176, 82.9739, ["micro_finance", "term_loan"], 71.1, 5.3, 7.7, "0542-2403723"),
    ("Annapurna Finance – Agra", "nbfc_mfi", "uttar_pradesh", "Agra", "Agra", "282001", 27.1767, 78.0081, ["micro_finance"], 92.8, 2.5, 3.9, "0562-2446050"),

    # ---------------- ANDHRA PRADESH ----------------
    ("Andhra Pradesh SC Finance Corp – Amaravati", "sca", "andhra_pradesh", "Amaravati", "Guntur", "520004", 16.5411, 80.5144, ["micro_finance", "term_loan"], 83.7, 4.6, 6.4, "0863-2234921"),
    ("Andhra Pragathi Grameena Bank – Kadapa", "rrb", "andhra_pradesh", "Kadapa", "YSR Kadapa", "516001", 14.4674, 78.8241, ["micro_finance", "term_loan"], 76.0, 4.1, 6.2, "08562-244182"),
    ("Saptagiri Grameena Bank – Tirupati", "rrb", "andhra_pradesh", "Tirupati", "Chittoor", "517501", 13.6288, 79.4192, ["micro_finance", "term_loan"], 78.4, 3.7, 5.6, "0877-2236113"),

    # ---------------- TELANGANA ----------------
    ("Telangana SC/ST Finance Corp – Hyderabad", "sca", "telangana", "Hyderabad", "Hyderabad", "500001", 17.3850, 78.4867, ["micro_finance", "term_loan", "education"], 85.3, 4.8, 6.7, "040-24614230"),
    ("Punjab National Bank – Hyderabad", "psb", "telangana", "Hyderabad", "Hyderabad", "500082", 17.4401, 78.3489, ["micro_finance", "term_loan", "education"], 90.6, 5.7, 7.9, "040-23355318"),
    ("Telangana Grameena Bank – Warangal", "rrb", "telangana", "Warangal", "Warangal Urban", "506001", 17.9810, 79.5936, ["micro_finance", "term_loan"], 74.9, 3.5, 5.3, "0870-2441168"),
    ("Arikin Finance – Gachibowli", "nbfc_mfi", "telangana", "Hyderabad", "Rangareddy", "500032", 17.4455, 78.3470, ["micro_finance"], 95.7, 1.9, 3.0, "040-23009263"),

    # ---------------- GUJARAT ----------------
    ("Gujarat SC Finance & Dev Corp – Gandhinagar", "sca", "gujarat", "Gandhinagar", "Gandhinagar", "382010", 23.2156, 72.6369, ["micro_finance", "term_loan"], 79.4, 3.9, 5.7, "079-23248776"),
    ("Bank of Baroda – Ahmedabad ZO", "psb", "gujarat", "Ahmedabad", "Ahmedabad", "380001", 23.0225, 72.5714, ["micro_finance", "term_loan", "education"], 93.0, 4.7, 6.6, "079-25507385"),
    ("Surat Sahakari Bank – Surat", "psb", "gujarat", "Surat", "Surat", "395003", 21.1702, 72.8311, ["micro_finance", "term_loan"], 82.1, 5.1, 7.4, "0261-2432447"),
    ("Baroda Gujarat Gramin Bank – Vadodara", "rrb", "gujarat", "Vadodara", "Vadodara", "390001", 22.3072, 73.1812, ["micro_finance", "term_loan"], 77.6, 3.4, 5.2, "0265-2433928"),

    # ---------------- RAJASTHAN ----------------
    ("Rajasthan SC Finance & Dev Corp – Jaipur", "sca", "rajasthan", "Jaipur", "Jaipur", "302001", 26.9124, 75.7873, ["micro_finance", "term_loan"], 69.7, 6.4, 8.8, "0141-2228936"),
    ("Baroda Rajasthan Kshetriya Gramin Bank – Ajmer", "rrb", "rajasthan", "Ajmer", "Ajmer", "305001", 26.4499, 74.6399, ["micro_finance", "term_loan"], 73.0, 4.2, 6.3, "0145-2621612"),
    ("Rajasthan Marudhara Gramin Bank – Jodhpur", "rrb", "rajasthan", "Jodhpur", "Jodhpur", "342001", 26.2389, 73.0243, ["micro_finance", "term_loan"], 72.5, 4.4, 6.5, "0291-2430810"),

    # ---------------- BIHAR ----------------
    ("Bihar SC Finance & Dev Corp – Patna", "sca", "bihar", "Patna", "Patna", "800001", 25.5941, 85.1376, ["micro_finance", "term_loan"], 58.2, 9.1, 12.5, "0612-2223618"),
    ("Dakshin Bihar Gramin Bank – Patna", "rrb", "bihar", "Patna", "Patna", "800001", 25.5941, 85.1376, ["micro_finance", "term_loan"], 65.8, 6.9, 9.7, "0612-2202530"),
    ("Uttar Bihar Gramin Bank – Muzaffarpur", "rrb", "bihar", "Muzaffarpur", "Muzaffarpur", "842001", 26.1211, 85.3484, ["micro_finance", "term_loan"], 64.0, 7.4, 10.1, "0621-2290164"),

    # ---------------- ODISHA ----------------
    ("Odisha SC/OBC Finance & Dev Corp – Bhubaneswar", "sca", "odisha", "Bhubaneswar", "Khordha", "751001", 20.2961, 85.8245, ["micro_finance", "term_loan"], 78.8, 4.3, 6.1, "0674-2391058"),
    ("Utkal Grameen Bank – Bhubaneswar", "rrb", "odisha", "Bhubaneswar", "Khordha", "751001", 20.2961, 85.8245, ["micro_finance", "term_loan"], 76.5, 3.8, 5.9, "0674-2392095"),
    ("Odisha Gramya Bank – Cuttack", "rrb", "odisha", "Cuttack", "Cuttack", "753001", 20.4625, 85.8828, ["micro_finance", "term_loan"], 75.0, 4.0, 6.0, "0671-2313302"),

    # ---------------- KERALA ----------------
    ("Kerala SC Develop Corp – Thiruvananthapuram", "sca", "kerala", "Thiruvananthapuram", "Thiruvananthapuram", "695001", 8.5241, 76.9366, ["micro_finance", "term_loan"], 84.6, 2.9, 4.3, "0471-2331470"),
    ("Kerala Gramin Bank – Thrissur", "rrb", "kerala", "Thrissur", "Thrissur", "680001", 10.5276, 76.2144, ["micro_finance", "term_loan"], 81.2, 2.6, 3.8, "0487-2331422"),
    ("Emirates MFI – Kochi", "nbfc_mfi", "kerala", "Kochi", "Ernakulam", "682001", 9.9312, 76.2673, ["micro_finance"], 96.8, 1.4, 2.2, "0484-2374104"),

    # ---------------- MADHYA PRADESH ----------------
    ("MP SC Finance & Dev Corp – Bhopal", "sca", "madhya_pradesh", "Bhopal", "Bhopal", "462001", 23.2599, 77.4126, ["micro_finance", "term_loan"], 72.3, 5.6, 7.8, "0755-2553821"),
    ("Madhya Pradesh Gramin Bank – Rewa", "rrb", "madhya_pradesh", "Rewa", "Rewa", "486001", 24.5306, 81.3036, ["micro_finance", "term_loan"], 74.2, 4.9, 7.0, "07662-240142"),
    ("Narmada Jhabua Gramin Bank – Indore", "rrb", "madhya_pradesh", "Indore", "Indore", "452001", 22.7196, 75.8577, ["micro_finance", "term_loan"], 73.7, 4.6, 6.8, "0731-2432081"),

    # ---------------- PUNJAB ----------------
    ("Punjab SC Finance & Dev Corp – Chandigarh", "sca", "punjab", "Chandigarh", "Chandigarh", "160017", 30.7333, 76.7794, ["micro_finance", "term_loan"], 80.1, 4.1, 5.9, "0172-2704768"),
    ("Punjab Gramin Bank – Ludhiana", "rrb", "punjab", "Ludhiana", "Ludhiana", "141001", 30.9010, 75.8573, ["micro_finance", "term_loan"], 82.6, 3.2, 4.9, "0161-2443955"),
    ("Suryoday Microfinance – Amritsar", "nbfc_mfi", "punjab", "Amritsar", "Amritsar", "143001", 31.6340, 74.8723, ["micro_finance"], 93.9, 1.7, 2.7, "0183-2555560"),

    # ---------------- HARYANA ----------------
    ("Haryana SC Finance & Dev Corp – Panchkula", "sca", "haryana", "Panchkula", "Panchkula", "134109", 30.6942, 76.8606, ["micro_finance", "term_loan"], 83.9, 4.0, 5.8, "0172-2582081"),
    ("Haryana Gramin Bank – Rohtak", "rrb", "haryana", "Rohtak", "Rohtak", "124001", 28.8955, 76.6066, ["micro_finance", "term_loan"], 79.0, 3.6, 5.4, "01262-244105"),
    ("Canara Bank – Gurugram", "psb", "haryana", "Gurugram", "Gurugram", "122001", 28.4595, 77.0266, ["micro_finance", "term_loan", "education"], 89.8, 4.5, 6.4, "0124-2214479"),

    # ---------------- UTTARAKHAND ----------------
    ("Uttarakhand SC Finance & Dev Corp – Dehradun", "sca", "uttarakhand", "Dehradun", "Dehradun", "248001", 30.3165, 78.0322, ["micro_finance", "term_loan"], 76.9, 4.4, 6.3, "0135-2629386"),
    ("Uttarakhand Gramin Bank – Haldwani", "rrb", "uttarakhand", "Haldwani", "Nainital", "263139", 29.2225, 79.5286, ["micro_finance", "term_loan"], 75.4, 4.2, 6.1, "05946-224081"),

    # ---------------- JHARKHAND ----------------
    ("Jharkhand SC Finance & Dev Corp – Ranchi", "sca", "jharkhand", "Ranchi", "Ranchi", "834001", 23.3441, 85.3096, ["micro_finance", "term_loan"], 68.3, 7.3, 10.0, "0651-2330081"),
    ("Jharkhand Rajya Gramin Bank – Ranchi", "rrb", "jharkhand", "Ranchi", "Ranchi", "834001", 23.3441, 85.3096, ["micro_finance", "term_loan"], 70.5, 6.1, 8.5, "0651-2350118"),
    ("Padiyala Microfinance – Jamshedpur", "nbfc_mfi", "jharkhand", "Jamshedpur", "East Singhbhum", "831001", 22.8046, 86.2029, ["micro_finance"], 91.7, 2.8, 4.2, "0657-2440425"),

    # ---------------- CHHATTISGARH ----------------
    ("Chhattisgarh SC Finance & Dev Corp – Raipur", "sca", "chhattisgarh", "Raipur", "Raipur", "492001", 21.2514, 81.6296, ["micro_finance", "term_loan"], 71.9, 5.8, 8.1, "0771-2221570"),
    ("Chhattisgarh Rajya Gramin Bank – Bilaspur", "rrb", "chhattisgarh", "Bilaspur", "Bilaspur", "495001", 22.0797, 82.1409, ["micro_finance", "term_loan"], 73.6, 5.0, 7.3, "07752-223041"),
    ("Janalaxmi Microfinance – Raipur", "nbfc_mfi", "chhattisgarh", "Raipur", "Raipur", "492001", 21.2514, 81.6296, ["micro_finance"], 92.4, 2.3, 3.6, "0771-4042445"),

    # ---------------- ASSAM / NE ----------------
    ("Assam SC Finance & Dev Corp – Guwahati", "sca", "assam", "Guwahati", "Kamrup", "781001", 26.1445, 91.7362, ["micro_finance", "term_loan"], 67.7, 5.2, 7.5, "0361-2542231"),
    ("Assam Gramin Vikash Bank – Guwahati", "rrb", "assam", "Guwahati", "Kamrup", "781001", 26.1445, 91.7362, ["micro_finance", "term_loan"], 72.1, 4.7, 6.9, "0361-2343742"),
    ("Arunachal Pradesh SC Finance & Dev Corp – Itanagar", "sca", "arunachal_pradesh", "Itanagar", "Papum Pare", "791111", 27.0844, 93.6053, ["micro_finance", "term_loan"], 64.4, 4.9, 7.2, "0360-2290323"),
    ("Meghalaya SC Finance & Dev Corp – Shillong", "sca", "meghalaya", "Shillong", "East Khasi Hills", "793001", 25.5788, 91.8933, ["micro_finance", "term_loan"], 66.2, 4.6, 6.8, "0364-2225636"),
    ("Manipur SC Finance & Dev Corp – Imphal", "sca", "manipur", "Imphal", "Imphal West", "795001", 24.8170, 93.9368, ["micro_finance", "term_loan"], 63.0, 5.4, 7.9, "0385-2451590"),
    ("Mizoram SC Finance & Dev Corp – Aizawl", "sca", "mizoram", "Aizawl", "Aizawl", "796001", 23.7271, 92.7176, ["micro_finance", "term_loan"], 62.7, 4.3, 6.6, "0389-2323550"),
    ("Nagaland SC Finance & Dev Corp – Kohima", "sca", "nagaland", "Kohima", "Kohima", "797001", 25.6751, 94.1086, ["micro_finance", "term_loan"], 61.9, 4.8, 7.0, "0370-2279032"),
    ("Tripura SC Finance & Dev Corp – Agartala", "sca", "tripura", "Agartala", "West Tripura", "799001", 23.8315, 91.2868, ["micro_finance", "term_loan"], 63.8, 4.5, 6.7, "0381-2225331"),
    ("Sikkim Industrial Dev & Investment Corp – Gangtok", "psb", "sikkim", "Gangtok", "East Sikkim", "737101", 27.3389, 88.6065, ["micro_finance", "term_loan", "education"], 70.9, 3.1, 4.8, "03592-202183"),

    # ---------------- HIMACHAL / J&K ----------------
    ("HP SC Finance & Dev Corp – Shimla", "sca", "himachal_pradesh", "Shimla", "Shimla", "171001", 31.1048, 77.1734, ["micro_finance", "term_loan"], 78.0, 3.4, 5.1, "0177-2624240"),
    ("Himachal Pradesh Gramin Bank – Mandi", "rrb", "himachal_pradesh", "Mandi", "Mandi", "175001", 31.7087, 76.9310, ["micro_finance", "term_loan"], 80.7, 3.0, 4.5, "01905-223041"),
    ("Uttarakhand SC Finance & Dev Corp – Rishikesh", "sca", "uttarakhand", "Rishikesh", "Dehradun", "249201", 30.0869, 78.2676, ["micro_finance", "term_loan"], 67.3, 5.9, 8.2, "0135-2431708"),

    # ---------------- GOA / CENTRAL ADDITIONS ----------------
    ("Goa SC Finance & Dev Corp – Panaji", "sca", "goa", "Panaji", "North Goa", "403001", 15.4909, 73.8278, ["micro_finance", "term_loan"], 83.1, 2.8, 4.1, "0832-2226571"),
    ("Small Industries Dev Bank of India – New Delhi", "psb", "delhi", "New Delhi", "New Delhi", "110016", 28.5467, 77.1954, ["micro_finance", "term_loan", "education"], 94.4, 3.7, 5.2, "011-26520847"),
    ("National SC Finance & Dev Corp – Delhi", "sca", "delhi", "New Delhi", "New Delhi", "110003", 28.5894, 77.1995, ["micro_finance", "term_loan", "education"], 91.8, 4.3, 6.0, "011-24364939"),
    ("NSFDC Regional Office – Chennai", "sca", "tamil_nadu", "Chennai", "Chennai", "600017", 13.0827, 80.2707, ["micro_finance", "term_loan", "education"], 88.9, 4.1, 5.7, "044-28152822"),
    ("NSFDC Regional Office – Kolkata", "sca", "west_bengal", "Kolkata", "Kolkata", "700016", 22.5726, 88.3639, ["micro_finance", "term_loan", "education"], 86.2, 4.8, 6.6, "033-40082971"),
    ("Education Loan Cell – Vidya Lakshmi Portal Partner, Mumbai", "psb", "maharashtra", "Mumbai", "Mumbai Suburban", "400059", 19.1127, 72.8497, ["education"], 95.1, 1.9, 2.4, "022-29260904"),
    ("Education Loan Cell – Chennai", "psb", "tamil_nadu", "Chennai", "Chennai", "600008", 13.0569, 80.2425, ["education"], 93.6, 2.1, 2.7, "044-28524142"),
    ("Education Loan Cell – Bengaluru", "psb", "karnataka", "Bengaluru", "Bengaluru Urban", "560009", 12.9720, 77.5844, ["education"], 92.7, 2.4, 3.0, "080-22622402"),
]

# Generated variants to reach 100+ (realistic branch variations per state)
_VARIANT_TYPES = {
    "nbfc_mfi": ["MFI Branch", "Service Area Office"],
    "rrb": ["Regional Office", "Zonal Office"],
    "sca": ["District Office", "Branch"],
    "psb": ["Branch", "MSME Cell"],
}
_MFI_NAMES = [
    "AINMOF", "Annapurna", "Arohan", "Bandhan", "Belstar", "Disha", "GramaVikas",
    "Janalakshmi", "KrazyBee", "Mimo", "Navadisha", "Saija", "Satin", "Sonata",
    "Suryoday", "Ujjivan", "VFS", "Womens World Banking Program",
]
_PARTNER_TYPES = ["sca", "psb", "rrb", "nbfc_mfi"]


def _mn_name(i, state):
    base = _MFI_NAMES[i % len(_MFI_NAMES)]
    return f"{base} Microfinance – {state.replace('_', ' ').title()} {i % 3 + 1}"


# Official websites for well-known institutions (only certain domains).
_WEBSITES = [
    ("State Bank of India", "https://sbi.co.in"),
    ("Bank of India", "https://bankofindia.co.in"),
    ("Bank of Baroda", "https://bankofbaroda.in"),
    ("Union Bank of India", "https://unionbankofindia.co.in"),
    ("Punjab National Bank", "https://pnbindia.in"),
    ("Canara Bank", "https://canarabank.com"),
    ("UCO Bank", "https://ucobank.com"),
    ("Indian Overseas Bank", "https://iob.in"),
    ("National SC Finance", "https://nsfdc.nic.in"),
    ("NSFDC", "https://nsfdc.nic.in"),
    ("Small Industries Dev Bank of India", "https://sidbi.in"),
    ("Vidya Lakshmi", "https://vidyalakshmi.co.in"),
]


def _website_for(name: str) -> str | None:
    for key, url in _WEBSITES:
        if key.lower() in name.lower():
            return url
    return None


def _spread_coords(lat: float, lng: float, seen: dict) -> tuple[float, float]:
    """Nudge stacked pins apart so same-city branches resolve distinctly.

    Deterministic spiral in ~150m steps; keeps every branch within ~1km of
    its true point so directions stay honest.
    """
    key = (round(lat, 4), round(lng, 4))
    n = seen.get(key, 0)
    seen[key] = n + 1
    if n == 0:
        return round(lat, 4), round(lng, 4)
    step = 0.0015 * ((n - 1) // 8 + 1)
    angle = ((n - 1) % 8) * (3.14159 / 4)
    import math as _math
    return (round(lat + step * _math.cos(angle), 4),
            round(lng + step * _math.sin(angle), 4))


def build_partners() -> list[dict]:
    out = []
    seed = random.Random(42)
    seen: dict = {}

    for idx, row in enumerate(PARTNERS):
        (name, ptype, state, city, district, pincode, lat, lng,
         loan_categories, util, npa, overdue, phone) = row
        lat, lng = _spread_coords(lat, lng, seen)
        out.append({
            "name": name,
            "partner_type": ptype,
            "state": state,
            "city": city,
            "district": district,
            "pincode": pincode,
            "latitude": lat,
            "longitude": lng,
            "loan_categories": loan_categories,
            "fund_utilization_pct": util,
            "npa_pct": npa,
            "overdue_pct": overdue,
            "phone": phone,
            "address": f"{city} District, {state.replace('_', ' ').title()}",
            "website": _website_for(name),
            "official_url": _website_for(name),
        })

    # Add generated branches so catalog exceeds 100 partners
    extra = 0
    target = 120
    states_used = [r[2] for r in PARTNERS]
    while len(out) < target:
        state = states_used[extra % len(states_used)]
        base_rows = [r for r in PARTNERS if r[2] == state]
        if not base_rows:
            extra += 1
            continue
        base = base_rows[extra % len(base_rows)]
        ptype = _PARTNER_TYPES[extra % len(_PARTNER_TYPES)]
        city = base[3]
        district = base[4]
        pincode = base[5]
        lat = round(base[6] + (seed.uniform(-0.02, 0.02)), 4)
        lng = round(base[7] + (seed.uniform(-0.02, 0.02)), 4)
        lat, lng = _spread_coords(lat, lng, seen)
        is_sca = ptype == "sca"
        cats = ["micro_finance", "term_loan"] if not is_sca else ["micro_finance", "term_loan", "education"]
        name = _mn_name(extra, state) if ptype == "nbfc_mfi" else (
            _VARIANT_TYPES[ptype][extra % len(_VARIANT_TYPES[ptype])] +
            " – " + base[3] + (f" ({base[5]})" if base[5] else "")
        )
        out.append({
            "name": name,
            "partner_type": ptype,
            "state": state,
            "city": city,
            "district": district,
            "pincode": pincode,
            "latitude": lat,
            "longitude": lng,
            "loan_categories": cats,
            "fund_utilization_pct": round(60.0 + seed.uniform(0, 38), 1),
            "npa_pct": round(2.0 + seed.uniform(0, 7), 1),
            "overdue_pct": round(3.0 + seed.uniform(0, 8), 1),
            "phone": f"1800-{1800 + extra % 4000}",
            "address": f"{city}, {district} District, {state.replace('_', ' ').title()}",
            "website": None,
            "official_url": None,
        })
        extra += 1

    return out


_MUTABLE_FIELDS = (
    "partner_type", "state", "city", "district", "pincode",
    "latitude", "longitude", "loan_categories", "fund_utilization_pct",
    "npa_pct", "overdue_pct", "phone", "address", "website", "official_url",
)


def seed_partners(db) -> int:
    """Insert missing partners; UPDATE existing rows by name (upsert).

    Upsert matters because coordinate/contact corrections must reach
    databases seeded earlier (e.g. production) on the next seed run.
    Returns the number of inserted rows.
    """
    from app.models.channel_partner import ChannelPartner

    existing = {p.name: p for p in db.query(ChannelPartner).all()}
    count = 0
    for data in build_partners():
        row = existing.get(data["name"])
        if row is None:
            db.add(ChannelPartner(**data))
            count += 1
            continue
        for field in _MUTABLE_FIELDS:
            setattr(row, field, data[field])
    db.commit()
    return count


def partner_count() -> int:
    return len(build_partners())


if __name__ == "__main__":
    from app import models  # noqa: F401
    from app.database import Base, SessionLocal, engine
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    added = seed_partners(db)
    from app.models.channel_partner import ChannelPartner
    total = db.query(ChannelPartner).count()
    print(f"Added {added} partners. Total partners in DB: {total}")
    db.close()