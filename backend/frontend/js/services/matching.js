(function () {
  "use strict";

  window.Matching = {
    scores: { sector: 30, support: 25, location: 15, stage: 10, type: 10, revenue: 10 },
    threshold: 40,

    badgeTier: function (score) {
      if (score >= 80) return "excellent";
      if (score >= 60) return "high";
      if (score >= 40) return "medium";
      return "low";
    },

    breakdown: function (scheme, profile) {
      var b = {};
      var s = this.scores;
      var total = 0;

      var sx = scheme.sector && String(scheme.sector).trim() === String(profile.business_sector || "").trim() ? s.sector : 0;
      if (scheme.sector === "all") sx = Math.round(s.sector * 0.9);
      if (sx) { b.sector = sx; total += sx; }

      var locRun = scheme.location_type === "central" ? Math.round(s.location * 0.9) : 0;
      if (scheme.state && String(scheme.state) === String(profile.state || "")) locRun = s.location;
      else if (scheme.location_type === "central") locRun = Math.round(s.location * 0.6);
      if (locRun) { b.location = locRun; total += locRun; }

      if (scheme.eligibility_based_on_entrepreneur_type && profile.entrepreneur_type) {
        var et = profile.entrepreneur_type;
        if (String(et).indexOf("all") === -1 && String(scheme.eligibility_based_on_entrepreneur_type).indexOf(et) !== -1) {
          b.type = s.type;
          total += s.type;
        }
      }

      if (scheme.stage) {
        var st = this._stageScore(scheme.stage, profile.business_stage);
        if (st) { b.stage = st; total += st; }
      }

      var sr = this._supportScore(scheme.support_percent_wise);
      if (sr) { b.support = sr; total += sr; }

      var totalWeights = s.sector + s.location + s.type + s.stage + s.support + s.revenue;
      return { items: b, total: Math.round((total / totalWeights) * 100) };
    },

    _stageScore: function (schemeStage, userStage) {
      var map = { "new": "new", "existing": "existing", "growing": "existing" };
      var s = map[schemeStage] || userStage;
      return schemeStage === s ? 10 : 0;
    },

    _supportScore: function (support) {
      return support && support !== "all" ? 25 : 0;
    }
  };
})();