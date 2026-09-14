(function () {
  "use strict";

  window.MockSchemes = [
    {
      id: "pmegp",
      name: "Prime Minister Employment Generation Programme (PMEGP)",
      sector: "all",
      location_type: "central",
      funding_min: 1000000,
      funding_max: 5000000,
      processing_time: "8-12 weeks",
      summary: "Margin money subsidy for new micro enterprises.",
      support_types: ["capital", "subsidy"],
      eligibility: ["all"],
      explanation: "Ideal for a new business needing seed capital."
    },
    {
      id: "mudra",
      name: "PM Mudra Yojana (Shishu / Kishor / Tarun)",
      sector: "all",
      location_type: "central",
      funding_min: 50000,
      funding_max: 10000000,
      processing_time: "2-4 weeks",
      summary: "Collateral-free loans up to ₹10 lakh.",
      support_types: ["capital"],
      eligibility: ["all"],
      explanation: "Collateral-free loans to help you start or grow."
    },
    {
      id: "pmfme",
      name: "PM Formalisation of Micro Food Processing Enterprises (PMFME)",
      sector: "food_processing",
      location_type: "central",
      funding_min: 100000,
      funding_max: 1000000,
      processing_time: "6-10 weeks",
      summary: "Credit-linked subsidy up to 35% for food processors.",
      support_types: ["capital", "subsidy", "training"],
      eligibility: ["all"],
      explanation: "Made for food processing units — 35% subsidy on eligible credit."
    },
    {
      id: "nbmcf_pm",
      name: "National Beekeeping & Honey Mission (NBHM)",
      sector: "agriculture",
      location_type: "central",
      funding_min: 500000,
      funding_max: 2000000,
      processing_time: "8-12 weeks",
      summary: "Assistance for beekeeping and honey production.",
      support_types: ["capital", "training"],
      eligibility: ["st", "sc", "obc"],
      explanation: "Prioritises farmers and women SHGs in agriculture."
    },
    {
      id: "mahila_udyam_nidhi",
      name: "Mahila Udyam Nidhi Scheme",
      sector: "all",
      location_type: "central",
      funding_min: 50000,
      funding_max: 500000,
      processing_time: "4-8 weeks",
      summary: "Loan support for women entrepreneurs.",
      support_types: ["capital"],
      eligibility: ["woman"],
      explanation: "Reserved for women starting their own enterprise."
    }
  ];
})();