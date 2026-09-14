(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "profile-view") return;

  function esc(s) {
    return String(s === undefined || s === null || s === "" ? "—" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function section(title, rows) {
    var html = '<div class="detail-card"><h2>' + esc(title) + "</h2><div>";
    rows.forEach(function (r) {
      html += '<div class="profile-field"><label>' + esc(r.l) + "</label><span>" + esc(r.v) + "</span></div>";
    });
    return html + "</div></div>";
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!Auth.requireLogin()) return;
    var mount = document.getElementById("profileContent");

    API.get("/api/profile", Auth.token())
      .then(function (p) {
        var fields = [
          { l: I18n.t("profile.fullName"), v: p.full_name, k: "full_name" },
          { l: I18n.t("profile.phone"), v: p.phone_number, k: "phone_number" },
          { l: I18n.t("profile.bizName"), v: p.business_name, k: "business_name" },
          { l: I18n.t("profile.bizSector"), v: p.business_sector, k: "business_sector" },
          { l: I18n.t("profile.bizStage"), v: p.business_stage, k: "business_stage" },
          { l: I18n.t("profile.state"), v: p.state, k: "state" },
          { l: I18n.t("profile.district"), v: p.district, k: "district" },
          { l: I18n.t("profile.age"), v: p.age_group, k: "age_group" },
          { l: I18n.t("profile.gender"), v: p.gender, k: "gender" },
          { l: I18n.t("profile.category"), v: p.social_category, k: "social_category" },
          { l: I18n.t("profile.annualRevenue"), v: p.annual_revenue, k: "annual_revenue" },
          { l: "Employees", v: p.employee_count, k: "employee_count" },
          { l: I18n.t("profile.description"), v: p.description, k: "description" }
        ];
        var support = (Array.isArray(p.support_needs) ? p.support_needs : []).join(", ");

        var filled = 0;
        var tracked = ["full_name", "phone_number", "state", "district", "business_name", "business_sector", "business_stage", "annual_revenue"];
        tracked.forEach(function (k) { if (p[k]) filled++; });
        var pct = Math.round((filled / tracked.length) * 100);

        var required = section(I18n.t("profile.title"), fields);
        var needs = section(I18n.t("profile.supportNeeds"), [{ l: I18n.t("profile.supportNeeds"), v: support || "—" }]);

        mount.innerHTML =
          '<div class="detail-card">' +
          '<h2 data-i18n="profile.completeness">Profile completeness</h2>' +
          '<div class="text-center"><span class="completeness-value">' + pct + '%</span></div>' +
          '<div class="completeness-bar"><div class="completeness-fill" style="width:' + pct + '%"></div></div>' +
          "</div>" +
          required + needs;
        I18n.apply();
      })
      .catch(function () {
        mount.innerHTML =
          '<div class="text-center" style="padding: var(--space-7) 0">' +
          '<h2 data-i18n="profile.notFound">Complete your profile first</h2>' +
          '<p class="text-muted">' + I18n.t("profile.sub") + "</p>" +
          '<a class="btn btn-primary mt-4" href="profile.html" data-i18n="profile.update">Edit profile</a>' +
          "</div>";
        I18n.apply();
      });
  });
})();