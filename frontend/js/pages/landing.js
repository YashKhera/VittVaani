(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "landing") return;

  function fillStates() {
    var el = document.querySelectorAll("main [data-i18n]");
    el.forEach(function (node) {
      if (node.getAttribute("data-i18n").indexOf("landing.") === 0) node.textContent = I18n.t(node.getAttribute("data-i18n"));
    });
  }

  function renderStats() {
    var stats = [
      { n: "65+", key: "landing.stats.schemes" },
      { n: "14", key: "landing.stats.sectors" },
      { n: "29", key: "landing.stats.states" },
      { n: "2", key: "landing.stats.languages" }
    ];
    var grid = document.querySelectorAll("[data-stat-grid]");
    grid.forEach(function (g) {
      g.innerHTML = stats.map(function (s) {
        return '<div class="stat-item fade-in-up"><div class="stat-number">' + s.n + '</div><div class="stat-label">' + I18n.t(s.key) + "</div></div>";
      }).join("");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    fillStates();
    renderStats();
  });
})();