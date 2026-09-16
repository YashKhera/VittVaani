(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "profile") return;

  function optText(o) {
    return I18n.loc(o);
  }

  function fillSelect(id, list, selected) {
    var el = document.getElementById(id);
    if (!el) return;
    var html = '<option value="">-</option>';
    (list || []).forEach(function (o) {
      html += '<option value="' + o.value + '"' + (String(o.value) === String(selected) ? " selected" : "") + ">" + optText(o) + "</option>";
    });
    el.innerHTML = html;
  }

  function isSc() {
    var el = document.getElementById("social_category");
    return el && el.value === "sc";
  }

  function toggleScPanel() {
    var panel = document.getElementById("scPanel");
    if (!panel) return;
    panel.classList.toggle("hidden", !isSc());
    panel.setAttribute("aria-hidden", isSc() ? "false" : "true");
  }

  function collect() {
    return {
      full_name: document.getElementById("full_name").value.trim(),
      phone_number: document.getElementById("phone_number").value.trim(),
      state: document.getElementById("state").value,
      district: document.getElementById("district").value.trim(),
      age_group: document.getElementById("age_group").value,
      gender: document.getElementById("gender").value,
      social_category: document.getElementById("social_category").value,
      annual_family_income: document.getElementById("annual_family_income").value,
      education_status: document.getElementById("education_status").value,
      estimated_project_cost: document.getElementById("estimated_project_cost").value === ""
        ? null
        : Number(document.getElementById("estimated_project_cost").value),
      business_name: document.getElementById("business_name").value.trim(),
      business_sector: document.getElementById("business_sector").value,
      business_stage: document.getElementById("business_stage").value,
      annual_revenue: document.getElementById("annual_revenue").value,
      employee_count: document.getElementById("employee_count").value.trim()
    };
  }

  function apply(p) {
    var map = {
      full_name: "full_name", phone_number: "phone_number", state: "state", district: "district",
      age_group: "age_group", gender: "gender", social_category: "social_category",
      annual_family_income: "annual_family_income", education_status: "education_status",
      estimated_project_cost: "estimated_project_cost",
      business_name: "business_name", business_sector: "business_sector",
      business_stage: "business_stage", annual_revenue: "annual_revenue", employee_count: "employee_count"
    };
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el && p[map[id]] !== undefined && p[map[id]] !== null) el.value = p[map[id]];
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!Auth.requireLogin()) return;

    fillSelect("state", (window.Questions && Questions.states) || [], "");
    fillSelect("business_sector", (window.Questions && Questions.sectors) || [], "");
    fillSelect("annual_revenue", (window.Questions && Questions.revenueGroups) || [], "");
    fillSelect("annual_family_income", (window.Questions && Questions.familyIncomeGroups) || [], "");
    fillSelect("education_status", (window.Questions && Questions.educationStatuses) || [], "");

    API.get("/api/profile", Auth.token())
      .then(function (p) {
        apply(p);
        fillSelect("state", Questions.states, p.state);
        fillSelect("business_sector", Questions.sectors, p.business_sector);
        fillSelect("annual_revenue", Questions.revenueGroups, p.annual_revenue);
        fillSelect("annual_family_income", Questions.familyIncomeGroups, p.annual_family_income);
        fillSelect("education_status", Questions.educationStatuses, p.education_status);
        toggleScPanel();
      })
      .catch(function () { /* no profile yet */ });

    document.getElementById("social_category").addEventListener("change", toggleScPanel);

    document.getElementById("profileForm").addEventListener("submit", function (e) {
      e.preventDefault();
      var errorEl = document.getElementById("formError");
      errorEl.classList.add("hidden");
      var payload = collect();
      if (isSc() && (!payload.annual_family_income || !payload.education_status || payload.estimated_project_cost === null)) {
        errorEl.textContent = I18n.t("profile.sc.required");
        errorEl.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: "smooth" });
        return;
      }
      var btn = document.querySelector('#profileForm button[type="submit"]');
      var btn = document.querySelector('#profileForm button[type="submit"]');
      btn.disabled = true;
      btn.textContent = I18n.t("common.loading");

      function done() {
        Notify.success(I18n.t("profile.saved.toast"));
        window.location.href = "questionnaire.html";
      }
      function fail(err) {
        errorEl.textContent = err.message;
        errorEl.classList.remove("hidden");
        btn.disabled = false;
        btn.textContent = I18n.t("profile.save");
      }

      API.put("/api/profile", payload, Auth.token())
        .then(done)
        .catch(function (err) {
          if (err.status === 404) {
            var minimal = Object.assign({}, payload, {
              full_name: payload.full_name || (Auth.user() && Auth.user().email || ""),
              state: payload.state || "all",
              business_sector: payload.business_sector || "all"
            });
            API.post("/api/profile", minimal, Auth.token()).then(done).catch(fail);
          } else {
            fail(err);
          }
        });
    });
  });
})();