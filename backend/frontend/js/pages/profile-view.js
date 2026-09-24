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

  function optLabel(list, value) {
    if (!Array.isArray(list) || !value) return value || "";
    var o = list.filter(function (x) { return x.value === value; })[0];
    return o ? I18n.loc(o) : value;
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
          { l: I18n.t("profile.projectType"), v: p.project_type ? (I18n.t("projectType." + p.project_type) || p.project_type) : "", k: "project_type" },
          { l: I18n.t("profile.familyIncome"), v: optLabel(Questions.familyIncomeGroups, p.annual_family_income), k: "annual_family_income" },
          { l: I18n.t("profile.educationStatus"), v: optLabel(Questions.educationStatuses, p.education_status), k: "education_status" },
          { l: I18n.t("profile.projectCost"), v: p.estimated_project_cost !== null && p.estimated_project_cost !== undefined ? "₹" + Number(p.estimated_project_cost).toLocaleString("en-IN") : "", k: "estimated_project_cost" },
          { l: I18n.t("profile.bestLoanFit"), v: p.ideal_loan_category ? (I18n.t("loanCategory." + p.ideal_loan_category) || p.ideal_loan_category) : "", k: "best_loan_fit" },
          { l: I18n.t("profile.annualRevenue"), v: p.annual_revenue, k: "annual_revenue" },
          { l: "Employees", v: p.employee_count, k: "employee_count" },
          { l: I18n.t("profile.description"), v: p.description, k: "description" }
        ];
        var support = (Array.isArray(p.support_needs) ? p.support_needs : []).join(", ");
        if (p.project_type === "education") {
          var bizKeys = { business_name: 1, business_sector: 1, business_stage: 1, annual_revenue: 1, employee_count: 1 };
          fields = fields.filter(function (f) { return !bizKeys[f.k]; });
        }

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
          '<a class="btn btn-primary mt-4" href="/profile/edit" data-i18n="profile.update">Edit profile</a>' +
          "</div>";
        I18n.apply();
      });
  });
})();