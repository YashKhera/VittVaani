"""Seed catalog for VittVaani v2 - schemes (central + state)."""

import os
import sys

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (name, short_name, level, department, sectors, states, stages, supports,
#  types, loan_min, loan_max, processing_days, official_url)

SCHEMES = [
    # ---------------- CENTRAL ----------------
    ("PM MUDRA Yojana", "MUDRA", "central", "Ministry of Finance", ["retail", "services", "manufacturing"], ["all"],
     ["planning", "existing"], ["loan"], ["general", "woman", "youth"], 300000, 10000000, 15, "https://www.mudra.org.in"),
    ("Stand-Up India Scheme", "Stand-Up India", "central", "Ministry of Finance", ["all"], ["all"],
     ["planning", "existing"], ["loan"], ["sc", "st", "woman"], 1000000, 10000000, 20, "https://www.standupmitra.in"),
    ("Prime Minister's Employment Generation Programme", "PMEGP", "central", "Ministry of MSME", ["all"], ["all"],
     ["planning", "existing"], ["grant", "loan", "training"], ["general", "woman", "youth"], 500000, 5000000, 30, "https://www.kviconline.gov.in"),
    ("PM Formalization of Micro Food Processing Enterprises", "PMFME", "central", "Ministry of Food Processing Industries", ["food_processing"], ["all"],
     ["existing"], ["subsidy", "equipment"], ["general", "woman"], 100000, 10000000, 45, "https://pmfme.mofpi.gov.in"),
    ("Startup India Seed Fund Scheme", "SISFS", "central", "Department for Promotion of Industry and Internal Trade", ["tech_it", "edtech", "services"], ["all"],
     ["planning", "existing", "expanding"], ["funding", "mentorship"], ["general", "youth"], 1000000, 50000000, 45, "https://www.startupindia.gov.in"),
    ("Credit Guarantee Fund for Micro and Small Enterprises", "CGTMSE", "central", "Ministry of MSME", ["all"], ["all"],
     ["planning", "existing"], ["loan", "insurance"], ["general"], 100000, 20000000, 15, "https://www.cgtmse.in"),
    ("National SC-ST Hub Scheme", "SC-ST Hub", "central", "Ministry of MSME", ["all"], ["all"],
     ["planning", "existing", "expanding"], ["grant", "market_access", "training"], ["sc", "st"], 0, 1500000, 30, "https://www.msme.gov.in"),
    ("Women Entrepreneurship Platform", "WEP", "central", "NITI Aayog", ["all"], ["all"],
     ["planning", "existing", "expanding"], ["training", "mentorship", "market_access"], ["woman"], 0, 0, 10, "https://wep.gov.in"),
    ("PM Vishwakarma Scheme", "Vishwakarma", "central", "Ministry of MSME", ["handicrafts", "manufacturing"], ["all"],
     ["planning", "existing"], ["loan", "subsidy", "training", "equipment"], ["general", "woman"], 100000, 3000000, 20, "https://pmvishwakarma.gov.in"),
    ("SFURTI - Scheme of Fund for Regeneration of Traditional Industries", "SFURTI", "central", "Ministry of MSME", ["handicrafts", "textiles_apparel"], ["all"],
     ["existing", "expanding"], ["grant", "equipment"], ["sc", "st", "general", "woman"], 0, 2000000, 60, "https://www.msme.gov.in"),
    ("MSME Credit Linked Capital Subsidy Scheme", "CLCSS", "central", "Ministry of MSME", ["manufacturing", "food_processing"], ["all"],
     ["existing", "expanding"], ["subsidy", "loan"], ["general"], 0, 10000000, 30, "https://www.msme.gov.in"),
    ("Technology Upgradation Fund Scheme", "TUFS", "central", "Ministry of Textiles", ["textiles_apparel"], ["all"],
     ["existing", "expanding"], ["subsidy", "loan"], ["general", "woman"], 500000, 50000000, 45, "https://www.texmin.nic.in"),
    ("SVANidhi - PM Street Vendor's Scheme", "SVANidhi", "central", "Ministry of Housing & Urban Affairs", ["retail", "services"], ["all"],
     ["existing"], ["loan"], ["general", "woman"], 10000, 50000, 7, "https://pmsvanidhi.mohua.gov.in"),
    ("One District One Product", "ODOP", "central", "DPIIT", ["food_processing", "handicrafts", "manufacturing", "textiles_apparel"], ["all"],
     ["existing", "expanding"], ["grant", "marketing", "market_access"], ["general", "woman"], 0, 2000000, 45, "https://onedistrictoneproduct.gov.in"),
    ("Startup India Tax Exemption", "SITE", "central", "DPIIT", ["tech_it", "edtech", "services"], ["all"],
     ["expanding"], ["tax_benefit"], ["general", "youth"], 0, 0, 30, "https://www.startupindia.gov.in"),
    ("NIDHI Seed Support Scheme", "NIDHI-SSS", "central", "Department of Science & Technology", ["tech_it", "edtech", "healthcare"], ["all"],
     ["planning", "existing"], ["funding", "mentorship"], ["youth", "general"], 500000, 5000000, 30, "https://seedfund.gov.in"),
    ("NewGen Innovation and Entrepreneurship Development Centre", "NewGen IEDC", "central", "DST", ["tech_it", "edtech"], ["all"],
     ["planning"], ["funding", "training"], ["youth"], 250000, 2500000, 30, "https://dst.gov.in"),
    ("National Scheduled Castes Finance and Development Corporation", "NSFDC", "central", "Ministry of Social Justice & Empowerment", ["all"], ["all"],
     ["planning", "existing"], ["loan", "training"], ["sc"], 100000, 10000000, 25, "https://nsfdc.gov.in"),
    ("National Backward Classes Finance and Development Corporation", "NBCFDC", "central", "Ministry of Social Justice & Empowerment", ["all"], ["all"],
     ["planning", "existing"], ["loan", "training"], ["obc"], 100000, 10000000, 25, "https://nbcfindia.org"),
    ("National Minorities Finance and Development Corporation", "NMDFC", "central", "Ministry of Minority Affairs", ["all"], ["all"],
     ["planning", "existing"], ["loan", "training"], ["minority"], 100000, 10000000, 25, "https://nmdfc.org"),
    ("National Handicapped Finance and Development Corporation", "NHFDC", "central", "Ministry of Social Justice & Empowerment", ["all"], ["all"],
     ["planning", "existing"], ["loan", "training", "equipment"], ["pwd"], 100000, 10000000, 25, "https://www.nhfdc.nic.in"),
    ("Venture Capital Scheme for Scheduled Castes", "VC-SC", "central", "NSFDC", ["tech_it", "services", "manufacturing"], ["all"],
     ["existing", "expanding"], ["funding"], ["sc"], 1000000, 15000000, 45, "https://nsfdc.gov.in"),
    ("Venture Capital Scheme for Divyangjan Entrepreneurs", "VC-Div", "central", "NHFDC", ["tech_it", "services", "manufacturing"], ["all"],
     ["existing", "expanding"], ["funding"], ["pwd"], 1000000, 15000000, 45, "https://www.nhfdc.nic.in"),
    ("AGRI-UDAAN - Food & Agribusiness Accelerator", "AGRI-UDAAN", "central", "Ministry of Agriculture", ["agriculture", "food_processing"], ["all"],
     ["planning", "existing"], ["funding", "mentorship", "market_access"], ["youth", "general"], 500000, 30000000, 45, "https://www.manage.gov.in"),
    ("Mission for Integrated Development of Horticulture", "MIDH", "central", "Ministry of Agriculture", ["agriculture", "food_processing"], ["all"],
     ["planning", "existing"], ["subsidy"], ["general"], 50000, 2500000, 30, "https://midh.gov.in"),
    ("Animal Husbandry Infrastructure Development Fund", "AHIDF", "central", "Ministry of Fisheries/Animal Husbandry", ["agriculture", "food_processing"], ["all"],
     ["existing", "expanding"], ["loan", "subsidy"], ["general"], 500000, 50000000, 40, "https://www.dahd.nic.in"),
    ("PM SAMPADA - Integrated Cold Chain Scheme", "PM SAMPADA", "central", "Ministry of Food Processing Industries", ["food_processing"], ["all"],
     ["existing", "expanding"], ["subsidy", "loan"], ["general"], 1000000, 50000000, 60, "https://mofpi.gov.in"),
    ("BioNEST - Bio-Incubators Nurturing Entrepreneurship", "BioNEST", "central", "BIRAC", ["healthcare", "tech_it"], ["all"],
     ["planning", "existing"], ["funding", "mentorship", "equipment"], ["general", "youth"], 500000, 25000000, 30, "https://birac.nic.in"),
    ("Khadi and Village Industries Commission Margin Money", "KVIC", "central", "Ministry of MSME", ["handicrafts", "textiles_apparel"], ["all"],
     ["planning", "existing"], ["loan", "subsidy", "training"], ["general", "woman"], 100000, 2500000, 20, "https://www.kvic.gov.in"),
    ("Software Technology Parks of India - Incubation", "STPI", "central", "Ministry of Electronics & IT", ["tech_it", "edtech"], ["all"],
     ["planning", "expanding"], ["funding", "equipment"], ["general", "youth"], 0, 5000000, 30, "https://www.stpi.in"),
    ("BPO Promotion Scheme (Remote Villages)", "BFS", "central", "Ministry of Electronics & IT", ["services", "tech_it"], ["all"],
     ["planning", "existing"], ["grant", "training"], ["woman", "youth"], 0, 5000000, 30, "https://www.meity.gov.in"),
    ("MSME ZED Certification", "ZED", "central", "Ministry of MSME", ["manufacturing", "services"], ["all"],
     ["existing"], ["grant", "training"], ["general"], 0, 5000000, 20, "https://zed.msme.gov.in"),
    ("e-NAM - National Agriculture Market", "e-NAM", "central", "Ministry of Agriculture", ["agriculture", "retail"], ["all"],
     ["existing", "expanding"], ["market_access", "mentorship"], ["general"], 0, 0, 15, "https://www.enam.gov.in"),
    ("Rashtriya Krishi Vikas Yojana - Agri Business", "RKVY", "central", "Ministry of Agriculture", ["agriculture", "food_processing"], ["all"],
     ["planning", "existing"], ["subsidy", "grant"], ["general", "woman"], 50000, 2000000, 40, "https://rkvy.nic.in"),
    ("SIDBI Fund of Funds for Startups", "FFS", "central", "SIDBI", ["tech_it", "edtech", "services", "healthcare"], ["all"],
     ["expanding"], ["funding"], ["general", "youth"], 1000000, 100000000, 60, "https://www.sidbi.in"),
    ("Wadhwani Foundation - National Entrepreneurship Network", "NEN", "central", "Wadhwani Foundation", ["all"], ["all"],
     ["idea", "planning"], ["training", "mentorship"], ["youth"], 0, 0, 10, "https://www.wfglobal.org"),

    # ---------------- STATE LEVEL ----------------
    ("Delhi Udyam Vikas Yojana", "DELHI UVY", "state", "Delhi Government", ["manufacturing", "services"], ["delhi"],
     ["planning", "existing"], ["subsidy", "loan"], ["general", "woman"], 50000, 5000000, 20, "https://delhi.gov.in"),
    ("Delhi MSME Business Loan Promotion Scheme", "Delhi MSME", "state", "Delhi Government", ["all"], ["delhi"],
     ["planning", "existing"], ["subsidy"], ["general", "woman", "sc", "st"], 100000, 10000000, 30, "https://delhi.gov.in"),
    ("Maharashtra State Margin Money Subsidy Scheme", "MSME-MMS", "state", "Maharashtra Government", ["manufacturing", "food_processing", "handicrafts"], ["maharashtra"],
     ["planning", "existing"], ["subsidy", "loan"], ["sc", "st", "obc", "woman"], 50000, 5000000, 30, "https://www.maharashtra.gov.in"),
    ("Maharashtra Self Employment Guarantee (MSEGN)", "MSEGN", "state", "Maharashtra Government", ["all"], ["maharashtra"],
     ["planning", "existing"], ["training", "grant"], ["youth", "woman"], 0, 1000000, 30, "https://www.msme.maharashtra.gov.in"),
    ("Gujarat Capital Subsidy for New MSMEs", "GJ-CS", "state", "Gujarat Government", ["manufacturing", "food_processing"], ["gujarat"],
     ["existing", "expanding"], ["subsidy"], ["general", "woman"], 500000, 5000000, 35, "https://www.gujarat.gov.in"),
    ("Karnataka Startup Ecosystem - Elevate", "ELEVATE", "state", "Karnataka Government", ["tech_it", "edtech", "healthcare"], ["karnataka"],
     ["planning", "existing"], ["funding", "mentorship"], ["youth", "general"], 500000, 5000000, 30, "https://startup.karnataka.gov.in"),
    ("Tamil Nadu Startup Seed Fund", "TNSSF", "state", "Tamil Nadu Government", ["tech_it", "services"], ["tamil_nadu"],
     ["planning", "existing"], ["funding", "mentorship"], ["youth"], 250000, 2500000, 30, "https://startuptn.in"),
    ("Tamil Nadu Micro & Small Industries Subsidy", "TN-MSM", "state", "Tamil Nadu Government", ["manufacturing", "textiles_apparel"], ["tamil_nadu"],
     ["existing", "expanding"], ["subsidy"], ["general", "woman"], 50000, 5000000, 40, "https://www.tn.gov.in"),
    ("West Bengal Swabalambi Scheme", "Swabalambi", "state", "West Bengal Government", ["all"], ["west_bengal"],
     ["planning", "existing"], ["loan", "training"], ["general", "woman"], 50000, 1000000, 30, "https://www.wb.gov.in"),
    ("West Bengal MSME Shed & Subsidy", "WB-MSM", "state", "West Bengal Government", ["manufacturing", "food_processing"], ["west_bengal"],
     ["existing", "expanding"], ["subsidy", "equipment"], ["general"], 200000, 10000000, 45, "https://www.msme.gov.in"),
    ("Uttar Pradesh Udyami Startup Yojana", "UP-USY", "state", "Uttar Pradesh Government", ["all"], ["uttar_pradesh"],
     ["planning", "existing"], ["grant", "training"], ["general", "sc", "st", "woman"], 50000, 1000000, 25, "https://msme.up.gov.in"),
    ("Uttar Pradesh Khadi Village Industries", "UP-KVIC", "state", "Uttar Pradesh Government", ["handicrafts", "textiles_apparel"], ["uttar_pradesh"],
     ["planning", "existing"], ["loan", "subsidy", "training"], ["woman", "general"], 50000, 2000000, 25, "https://upkvic.org.in"),
    ("Rajasthan iStart Startup Fund", "iStart", "state", "Rajasthan Government", ["tech_it", "edtech", "services"], ["rajasthan"],
     ["planning", "existing"], ["funding", "mentorship", "training"], ["youth", "woman"], 500000, 2000000, 30, "https://istart.rajasthan.gov.in"),
    ("Punjab Youth Loan Scheme", "Punjab YL", "state", "Punjab Government", ["all"], ["punjab"],
     ["planning", "existing"], ["loan", "training"], ["youth"], 100000, 5000000, 25, "https://punjab.gov.in"),
    ("Kerala Startup Mission - Seed Fund", "KSUM", "state", "Kerala Government", ["tech_it", "edtech", "healthcare", "agriculture"], ["kerala"],
     ["planning", "existing"], ["funding", "mentorship"], ["youth", "woman"], 500000, 3000000, 30, "https://startupmission.kerala.gov.in"),
    ("Kerala Kudumbashree Entrepreneurship", "KSREE", "state", "Kerala Government", ["food_processing", "textiles_apparel", "retail"], ["kerala"],
     ["planning", "existing"], ["training", "loan", "market_access"], ["woman"], 100000, 1000000, 20, "https://www.kudumbashree.org"),
    ("Madhya Pradesh Yuva Udyami Yojana", "MP-YU", "state", "Madhya Pradesh Government", ["all"], ["madhya_pradesh"],
     ["planning", "existing"], ["grant", "loan"], ["youth", "woman"], 50000, 2000000, 25, "https://www.mp.gov.in"),
    ("Madhya Pradesh Khadi Promotion", "MP-Khadi", "state", "Madhya Pradesh Government", ["handicrafts", "textiles_apparel"], ["madhya_pradesh"],
     ["planning", "existing"], ["subsidy", "training"], ["general"], 50000, 1500000, 25, "https://www.mp.gov.in"),
    ("Bihar Yuva Udyami Yojana", "Bihar YU", "state", "Bihar Government", ["all"], ["bihar"],
     ["planning", "existing"], ["loan", "training"], ["youth", "woman"], 50000, 1000000, 20, "https://state.bihar.gov.in"),
    ("Bihar Mega Food Park/Agri Support", "Bihar-Agri", "state", "Bihar Government", ["agriculture", "food_processing"], ["bihar"],
     ["existing"], ["subsidy", "equipment"], ["general", "sc", "st"], 100000, 5000000, 40, "https://state.bihar.gov.in"),
    ("Telangana T-Hub Incubation", "T-Hub", "state", "Telangana Government", ["tech_it", "edtech", "healthcare"], ["telangana"],
     ["planning", "existing", "expanding"], ["mentorship", "funding", "market_access"], ["youth", "general"], 500000, 5000000, 30, "https://t-hub.co"),
    ("Telangana MSME Incentives", "TS-MSME", "state", "Telangana Government", ["manufacturing", "food_processing"], ["telangana"],
     ["existing", "expanding"], ["subsidy", "equipment"], ["general", "woman"], 500000, 10000000, 40, "https://www.tsmsme.in"),
    ("Odisha Startup O-Hub", "O-Hub", "state", "Odisha Government", ["tech_it", "services", "healthcare"], ["odisha"],
     ["planning", "existing"], ["funding", "mentorship"], ["youth", "woman"], 500000, 2000000, 30, "https://startupodisha.gov.in"),
    ("Odisha Youth Employment Programme (MSME)", "OYEM", "state", "Odisha Government", ["handicrafts", "services", "manufacturing"], ["odisha"],
     ["planning", "existing"], ["loan", "training"], ["youth", "general"], 100000, 2000000, 25, "https://odisha.gov.in"),
    ("Haryana Startup Fund", "H-START", "state", "Haryana Government", ["tech_it", "edtech", "agriculture"], ["haryana"],
     ["planning", "existing"], ["funding", "mentorship"], ["youth", "woman"], 500000, 2000000, 30, "https://startupharyana.gov.in"),
    ("Chhattisgarh Yuva Swabhiman Yojana", "CG-YU", "state", "Chhattisgarh Government", ["all"], ["chhattisgarh"],
     ["planning", "existing"], ["loan", "training"], ["youth", "woman"], 50000, 1500000, 20, "https://cggovt.nic.in"),
    ("Jharkhand Young Entrepreneurship", "JYEP", "state", "Jharkhand Government", ["handicrafts", "agriculture", "services"], ["jharkhand"],
     ["planning", "existing"], ["loan", "training"], ["youth", "sc", "st"], 50000, 1000000, 25, "https://www.jharkhand.gov.in"),
    ("Assam Chief Minister's Swaniyojan Scheme", "Swaniyojan", "state", "Assam Government", ["all"], ["assam"],
     ["planning", "existing"], ["loan", "training"], ["general", "woman"], 50000, 1000000, 25, "https://assam.gov.in"),
    ("Himachal Pradesh Startup Fund", "HP-Start", "state", "Himachal Pradesh Government", ["tech_it", "agriculture", "tourism"], ["himachal_pradesh"],
     ["planning", "existing"], ["funding", "mentorship"], ["youth", "general"], 500000, 2000000, 30, "https://himachal.gov.in"),
]

SECTOR_DOCS = {
    "food_processing": ["FSSAI license", "Udyam Registration Certificate"],
    "agriculture": ["Land ownership/revenue records", "FSA/KCC details if applicable"],
    "handicrafts": ["Artisan/registration details", "Sample product photographs"],
    "textiles_apparel": ["Power loom/weaving registration", "Sample product photographs"],
    "tech_it": ["Incorporation certificate", "Pitch deck and business plan"],
    "edtech": ["Incorporation certificate", "Pitch deck and business plan"],
    "healthcare": ["Business license", "Regulatory approvals if applicable"],
    "transport": ["Vehicle registration / operator permit"],
    "construction": ["Contractor license (if applicable)"],
}

GENERAL_DOCS = ["Aadhaar Card", "PAN Card", "Bank account details", "Udyam Registration (if applicable)"]

SUPPORT_BENEFITS = {
    "loan": "Collateral-free/concessional business loan",
    "subsidy": "Capital subsidy on eligible investments",
    "grant": "Direct grant support for your business",
    "funding": "Seed or venture-stage funding support",
    "training": "Free skill and business training",
    "mentorship": "Mentorship and guidance network",
    "equipment": "Support for machinery/equipment",
    "marketing": "Marketing and branding support",
    "insurance": "Insurance coverage support",
    "tax_benefit": "Tax exemptions and benefits",
    "market_access": "Market access and buyer connections",
}


def build_schemes() -> list[dict]:
    out = []
    for name, short, level, dept, sectors, states, stages, supports, types, mn, mx, days, url in SCHEMES:
        benefits = [SUPPORT_BENEFITS[s] for s in supports]
        docs = list(GENERAL_DOCS)
        for s in sectors:
            if s in SECTOR_DOCS:
                docs.extend(SECTOR_DOCS[s])
        eligibility = ["Indian citizen 18+", "Business belongs to an eligible sector", "No prior default on government loans"]
        if level == "state":
            eligibility.append("Applicant must be a resident of the state")
        desc = (
            f"{name}"
            f"{(' (' + short + ')' if short != name else '')} offers "
            f"{', '.join(supports)} support for {', '.join(sectors).replace('_', ' ')} businesses."
        )
        out.append({
            "name": name,
            "short_name": short if short != name else None,
            "government_level": level,
            "department": dept,
            "description": desc,
            "sectors": sectors,
            "states": states,
            "business_stages": stages,
            "support_types": supports,
            "entrepreneur_types": types,
            "benefits": benefits,
            "eligibility": eligibility,
            "documents": docs,
            "loan_min": mn if mn else None,
            "loan_max": mx if mx else None,
            "processing_days": days,
            "official_url": url,
            "application_url": url,
        })
    return out


def seed_schemes(db) -> int:
    from app.models.scheme import Scheme
    from app.utils.helpers import normalize_list

    existing_names = set()
    for row in db.query(Scheme).all():
        existing_names.add(normalize_list([row.name])[0] if row.name else "")

    count = 0
    for data in build_schemes():
        if data["name"] in existing_names:
            continue
        db.add(Scheme(**data))
        count += 1
    db.commit()
    return count


def scheme_count() -> int:
    return len(SCHEMES)


if __name__ == "__main__":
    from app import models  # noqa: F401  (register tables before create_all)
    from app.database import Base, SessionLocal, engine
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    added = seed_schemes(db)
    from app.models.scheme import Scheme
    total = db.query(Scheme).count()
    print(f"Added {added} schemes. Total schemes in DB: {total}")
    db.close()