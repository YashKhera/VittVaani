(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "saved-schemes") return;

  function esc(s) {
    return String(s === undefined || s === null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function fundingText(s) {
    if (s.loan_min !== null && s.loan_min !== undefined && s.loan_max !== null && s.loan_max !== undefined) {
      return "₹" + Math.round(s.loan_min / 100000) + "L – ₹" + Math.round(s.loan_max / 100000) + "L";
    }
    if (s.loan_max !== null && s.loan_max !== undefined) return "Up to ₹" + Math.round(s.loan_max / 100000) + "L";
    return "Varies";
  }

  function cardHtml(s, id) {
    var sector = Array.isArray(s.sectors) && s.sectors.length ? s.sectors[0] : "all";
    var support = (Array.isArray(s.support_types) ? s.support_types : []).slice(0, 3);
    var tags = support.map(function (t) { return '<span class="badge badge-info">' + esc(t) + "</span>"; }).join(" ");
    return '<article class="card scheme-card fade-in-up" data-saved-id="' + esc(id) + '">' +
      '<div class="scheme-header">' +
      '<div><h3 class="mb-1">' + esc(s.name || "Government Scheme") + "</h3>" +
      '<div class="scheme-meta"><span class="badge badge-info">' + esc(sector) + "</span>" +
      '<span>' + esc(s.government_level || "") + "</span></div></div></div>" +
      (s.description ? '<p class="text-sm mb-0">' + esc(s.description) + "</p>" : "") +
      '<div class="mt-3 text-sm"><strong>' + esc(I18n.t("results.funding.range")) + ": </strong>" + esc(fundingText(s)) + "</div>" +
      (tags ? '<div class="mt-2">' + tags + "</div>" : "") +
      '<div class="scheme-actions mt-4">' +
      '<a class="btn btn-secondary btn-sm" href="/scheme-details?id=' + encodeURIComponent(id) + '">' + esc(I18n.t("common.viewDetails")) + "</a>" +
      '<button class="btn btn-sm btn-error" data-remove-saved="' + encodeURIComponent(id) + '">' + esc(I18n.t("common.remove")) + "</button>" +
      "</div></article>";
  }

  function updateCount(grid, items) {
    var el = document.getElementById("savedCountLabel");
    if (el) el.textContent = String(items.length);
    var unit = document.getElementById("savedCountUnit");
    if (unit) unit.textContent = " " + I18n.t("saved.title").toLowerCase();
  }

  function render(grid, items) {
    grid.innerHTML = items.map(function (e) { return cardHtml(e.scheme || e, e.scheme ? e.scheme.id : (e.id || e.scheme_id)); }).join("");
    var empty = document.getElementById("emptyState");
    if (!items.length) { empty.classList.remove("hidden"); }
    updateCount(grid, items);

    grid.querySelectorAll("[data-remove-saved]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = decodeURIComponent(btn.getAttribute("data-remove-saved"));
        API.del("/api/saved-schemes/" + encodeURIComponent(id), Auth.token())
          .then(function () {
            var card = btn.closest(".scheme-card");
            if (card) card.remove();
            Notify.success(I18n.t("saved.remove.toast"));
            var remaining = grid.querySelectorAll(".scheme-card").length;
            if (remaining) {
              updateCount(grid, [].slice.call(grid.querySelectorAll(".scheme-card")));
            } else {
              updateCount(grid, []);
              document.getElementById("emptyState").classList.remove("hidden");
            }
          })
          .catch(function (e) { Notify.error(e.message); });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!Auth.requireLogin()) return;
    var grid = document.getElementById("savedGrid");
    var empty = document.getElementById("emptyState");
    API.get("/api/saved-schemes", Auth.token())
      .then(function (data) {
        var items = (data && (data.saved_schemes || data.schemes)) || [];
        if (!items.length) { empty.classList.remove("hidden"); updateCount(grid, []); grid.innerHTML = ""; return; }
        render(grid, items);
      })
      .catch(function (e) {
        Notify.warning(e.message);
        empty.classList.remove("hidden");
      });
  });
})();