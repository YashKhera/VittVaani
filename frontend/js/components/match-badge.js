(function () {
  "use strict";

  window.MatchBadge = {
    render: function (score) {
      var tier = Matching.badgeTier(score);
      var labels = { low: "results.badge.low", medium: "results.badge.medium", high: "results.badge.high", excellent: "results.badge.excellent" };
      var cls = { low: "badge-error", medium: "badge-warning", high: "badge-success", excellent: "badge-primary" };
      return '<span class="badge ' + cls[tier] + '">' + I18n.t(labels[tier]) + "</span>";
    }
  };
})();