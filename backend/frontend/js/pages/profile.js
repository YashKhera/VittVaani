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

  function isEducation() {
    var el = document.getElementById("project_type");
    return el && el.value === "education";
  }

  function toggleScPanel() {
    var panel = document.getElementById("scPanel");
    if (!panel) return;
    panel.classList.toggle("hidden", !isSc());
    panel.setAttribute("aria-hidden", isSc() ? "false" : "true");
  }

  function toggleSections() {
    var edu = isEducation();
    var bizSection = document.getElementById("businessSection");
    var eduSection = document.getElementById("educationSection");
    if (bizSection) bizSection.style.display = edu ? "none" : "";
    if (eduSection) eduSection.style.display = edu ? "" : "none";
  }

  function collect() {
    var edu = isEducation();
    var income, eduStatus, projectCost;
    if (edu) {
      var e2 = document.getElementById("education_status2");
      var i2 = document.getElementById("annual_family_income2");
      var c2 = document.getElementById("estimated_project_cost2");
      eduStatus = e2 ? e2.value : "";
      income = i2 ? i2.value : "";
      projectCost = c2 && c2.value !== "" ? Number(c2.value) : null;
    } else {
      income = document.getElementById("annual_family_income").value;
      eduStatus = document.getElementById("education_status").value;
      projectCost = document.getElementById("estimated_project_cost").value === ""
        ? null
        : Number(document.getElementById("estimated_project_cost").value);
    }
    return {
      full_name: document.getElementById("full_name").value.trim(),
      phone_number: document.getElementById("phone_number").value.trim(),
      state: document.getElementById("state").value,
      district: document.getElementById("district").value.trim(),
      age_group: document.getElementById("age_group").value,
      gender: document.getElementById("gender").value,
      social_category: document.getElementById("social_category").value,
      project_type: document.getElementById("project_type").value,
      annual_family_income: income,
      education_status: eduStatus,
      estimated_project_cost: projectCost,
      business_name: edu ? "" : document.getElementById("business_name").value.trim(),
      business_sector: edu ? "education" : document.getElementById("business_sector").value,
      business_stage: edu ? "planning" : document.getElementById("business_stage").value,
      annual_revenue: edu ? "" : document.getElementById("annual_revenue").value,
      employee_count: edu ? "" : document.getElementById("employee_count").value.trim()
    };
  }

  function apply(p) {
    var map = {
      full_name: "full_name", phone_number: "phone_number", state: "state", district: "district",
      age_group: "age_group", gender: "gender", social_category: "social_category", project_type: "project_type",
      annual_family_income: "annual_family_income", education_status: "education_status",
      estimated_project_cost: "estimated_project_cost",
      business_name: "business_name", business_sector: "business_sector",
      business_stage: "business_stage", annual_revenue: "annual_revenue", employee_count: "employee_count"
    };
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el && p[map[id]] !== undefined && p[map[id]] !== null) el.value = p[map[id]];
    });
    if (isEducation()) {
      var e2 = document.getElementById("education_status2");
      var i2 = document.getElementById("annual_family_income2");
      var c2 = document.getElementById("estimated_project_cost2");
      if (e2) e2.value = p.education_status || "";
      if (i2) i2.value = p.annual_family_income || "";
      if (c2) c2.value = p.estimated_project_cost || "";
    }
  }

  function syncEducationFields() {
    var edu = isEducation();
    var sc = isSc();
    if (!edu && sc) {
      var src = document.getElementById("education_status");
      var dst = document.getElementById("education_status2");
      var srcI = document.getElementById("annual_family_income");
      var dstI = document.getElementById("annual_family_income2");
      if (dst && src) dst.value = src.value;
      if (dstI && srcI) dstI.value = srcI.value;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!Auth.requireLogin()) return;

    fillSelect("state", (window.Questions && Questions.states) || [], "");
    fillSelect("business_sector", (window.Questions && Questions.sectors) || [], "");
    fillSelect("annual_revenue", (window.Questions && Questions.revenueGroups) || [], "");
    fillSelect("annual_family_income", (window.Questions && Questions.familyIncomeGroups) || [], "");
    fillSelect("education_status", (window.Questions && Questions.educationStatuses) || [], "");
    fillSelect("education_status2", (window.Questions && Questions.educationStatuses) || [], "");
    fillSelect("annual_family_income2", (window.Questions && Questions.familyIncomeGroups) || [], []);

    toggleSections();

    API.get("/api/profile", Auth.token())
      .then(function (p) {
        apply(p);
        fillSelect("state", Questions.states, p.state);
        fillSelect("business_sector", Questions.sectors, p.business_sector);
        fillSelect("annual_revenue", Questions.revenueGroups, p.annual_revenue);
        fillSelect("annual_family_income", Questions.familyIncomeGroups, p.annual_family_income);
        fillSelect("education_status", Questions.educationStatuses, p.education_status);
        fillSelect("education_status2", Questions.educationStatuses, p.education_status);
        fillSelect("annual_family_income2", Questions.familyIncomeGroups, p.annual_family_income);
        toggleScPanel();
        toggleSections();
      })
      .catch(function () { /* no profile yet */ });

    document.getElementById("social_category").addEventListener("change", function () {
      toggleScPanel();
      syncEducationFields();
    });
    document.getElementById("project_type").addEventListener("change", function () {
      toggleSections();
      syncEducationFields();
    });

    document.getElementById("profileForm").addEventListener("submit", function (e) {
      e.preventDefault();
      var errorEl = document.getElementById("formError");
      errorEl.classList.add("hidden");
      var payload = collect();
      if (!payload.state || payload.state === "") {
        errorEl.textContent = I18n.t("profile.state") + " is required";
        errorEl.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: "smooth" });
        return;
      }
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
