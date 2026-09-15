(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "questionnaire") return;

  var profile = null;
  var steps = [];
  var STEP_TOTAL = 0;
  var step = 0;
  var answers = {};

  // Static questions (Questions.list) whose values are already captured on the
  // profile page — we prefill them, never re-ask them, and only show chips.
  var PROFILE_LOOKUP = [
    { id: "full_name", field: "full_name", kind: "text", labelKey: "questionnaire.auto.name" },
    { id: "phone_number", field: "phone_number", kind: "text", labelKey: "questionnaire.auto.phone" },
    { id: "age_group", field: "age_group", kind: "opts", options: "ageGroups", labelKey: "questionnaire.auto.age" },
    { id: "gender", field: "gender", kind: "opts", options: "genders", labelKey: "questionnaire.auto.gender" },
    { id: "business_sector", field: "business_sector", kind: "opts", options: "sectors", labelKey: "questionnaire.auto.sector" },
    { id: "state", field: "state", kind: "opts", options: "states", labelKey: "questionnaire.auto.state" },
    { id: "business_stage", field: "business_stage", kind: "opts", options: "stages", labelKey: "questionnaire.auto.stage" },
    { id: "annual_revenue", field: "annual_revenue", kind: "opts", options: "revenueGroups", labelKey: "questionnaire.auto.revenue" },
    { id: "entrepreneur_type", field: "social_category", kind: "category", labelKey: "questionnaire.auto.category" }
  ];

  var POST_PROFILE_IDS = { financial: true, non_financial: true, description: true };
  var FINAL_IDS = ["understand", "review"];

  function optText(o) {
    return I18n.current() === "hi" ? o.hi : o.en;
  }

  function optionsFor(q) {
    var key = q.options;
    if (Array.isArray(key)) return key;
    if (typeof key === "function") return key();
    if (key === "financial" || key === "nonFinancial") return Questions.supportNeeds[key] || [];
    return Questions[key] || [];
  }

  function selectedValues(inputs) {
    return Array.prototype.slice.call(inputs).filter(function (i) { return i.checked; }).map(function (i) { return i.value; });
  }

  function textValue() {
    var el = document.getElementById("q-input");
    return el ? el.value.trim() : "";
  }

  function answeredCount() {
    return steps.filter(function (q) {
      if (q.type === "review") return false;
      var v = answers[q.id];
      if (q.type === "understand") return !!(v && v.understand_confirmed === true);
      if (q.type === "textarea" || q.type === "text") return !!(v && String(v).trim());
      if (q.type === "multi") return v && v.length > 0;
      return !!v;
    }).length;
  }

  function answeredPercent() {
    var total = STEP_TOTAL - 1;
    return total > 0 ? Math.round((answeredCount() / total) * 100) : 0;
  }

  function profileFilledCount() {
    var n = 0;
    PROFILE_LOOKUP.forEach(function (l) {
      if (prefilledValue(l)) n++;
    });
    return n;
  }

  function prefilledValue(l) {
    if (!profile) return null;
    if (l.kind === "category") return profile.social_category || null;
    var v = profile[l.field];
    return (v === undefined || v === null || v === "") ? null : v;
  }

  function prefillFromProfile() {
    PROFILE_LOOKUP.forEach(function (l) {
      var raw = prefilledValue(l);
      if (!raw) return;
      if (answers && Object.prototype.hasOwnProperty.call(answers, l.id)) return;
      if (l.kind === "category") {
        var map = { sc: "sc", st: "st", obc: "obc" };
        answers[l.id] = map[raw] ? map[raw] : (raw === "general" ? "general" : undefined);
      } else {
        answers[l.id] = raw;
      }
    });
  }

  function sectorLabel(sector) {
    if (!sector) return "";
    var list = Questions.sectors.filter(function (s) { return s.value === sector; });
    return list.length ? optText(list[0]) : sector;
  }

  function buildSteps(dynamicQuestions) {
    steps = [];
    var dyn = dynamicQuestions || [];
    dyn.forEach(function (q) { steps.push(q); });
    ["financial", "non_financial", "description"].forEach(function (id) {
      if (POST_PROFILE_IDS[id]) {
        var q = Questions.find(id);
        if (q) steps.push(q);
      }
    });
    FINAL_IDS.forEach(function (id) {
      var q = Questions.find(id);
      if (q) steps.push(q);
    });
    STEP_TOTAL = steps.length;
  }

  function autoNote() {
    var filled = [];
    PROFILE_LOOKUP.forEach(function (l) { if (prefilledValue(l)) filled.push(l.labelKey); });
    if (!filled.length) return "";

    var chips = filled.map(function (k) {
      return '<span class="tag-chip">' + I18n.t(k) + " ✓</span>";
    }).join(" ");
    var sub = I18n.t("questionnaire.auto.sub", { sector: sectorLabel(profile ? profile.business_sector : "") || "" });
    return '<div class="auto-fill-note">' +
      '<p class="text-sm text-muted mb-2"><strong>' + I18n.t("questionnaire.auto.title") + "</strong></p>" +
      '<p class="text-sm mb-2">' + sub + "</p>" +
      '<p class="mb-0">' + chips + "</p>" +
      "</div>";
  }

  var persistTimer = null;
  function schedulePersist() {
    if (!Auth.token()) return;
    clearTimeout(persistTimer);
    persistTimer = setTimeout(function () { persist(); }, 600);
  }

  function persist(cb) {
    if (!Auth.token()) {
      if (cb) cb();
      return;
    }
    API.put("/api/questionnaire/progress", { answers: answers, step: step }, Auth.token())
      .then(function () { if (cb) cb(); })
      .catch(function () { if (cb) cb(); });
  }

  function render() {
    var q = steps[step];
    var mount = document.getElementById("questionMount");
    var title = I18n.current() === "hi" ? q.title.hi : q.title.en;
    var help = q.help ? (I18n.current() === "hi" ? q.help.hi : q.help.en) : "";
    var savedValue = answers[q.id];

    var body = "";
    if (q.type === "review") {
      body = "<div class=\"card mb-4\"><h3 class=\"mb-3\">" + title + "</h3>" + buildReview() + "</div>";
    } else if (q.type === "understand") {
      body = '<div id="understandingMount"></div>';
    } else if (q.type === "textarea") {
      body = '<textarea id="q-input" rows="4" placeholder="' + help + '">' + (savedValue || "") + "</textarea>";
    } else if (q.type === "text") {
      body = '<input id="q-input" type="text" placeholder="' + help + '" value="' + (savedValue || "") + '" autocomplete="off">';
    } else {
      var opts = optionsFor(q);
      var fields = "";
      opts.forEach(function (o) {
        var checked = "";
        if (q.type === "multi") {
          checked = (savedValue || []).indexOf(o.value) !== -1 ? " checked" : "";
        } else {
          checked = savedValue === o.value ? " checked" : "";
        }
        var input = q.type === "multi" ? "checkbox" : "radio";
        fields += '<label class="option-' + (q.type === "multi" ? "checkbox" : "radio") + '">' +
          '<input type="' + input + '" name="q" value="' + o.value + '"' + checked + "> " + optText(o) + "</label>";
      });
      body = fields;
    }

    var auto = step === 0 && q.type !== "review" && q.type !== "understand" ? autoNote() : "";

    mount.innerHTML =
      '<div class="question-card fade-in">' +
      auto +
      '<h2 class="question-text">' + title + "</h2>" +
      (help && q.type !== "textarea" && q.type !== "text" ? '<p class="mb-4">' + help + "</p>" : "") +
      body +
      '<div class="question-actions">' +
      (step > 0 ? '<button class="btn btn-secondary" id="prevBtn">' + I18n.t("common.previous") + "</button>" : '<a class="btn btn-secondary" href="index.html">' + I18n.t("common.cancel") + "</a>") +
      '<button class="btn ' + (q.type === "review" ? "btn-primary btn-lg" : "btn-primary") + '" id="nextBtn">' + (q.type === "review" ? I18n.t("questionnaire.finish") : I18n.t("common.next")) + "</button>" +
      "</div></div>";

    renderHeader();

    document.getElementById("nextBtn").addEventListener("click", onNext);
    var prev = document.getElementById("prevBtn");
    if (prev) prev.addEventListener("click", function () { step--; scrollTop(); render(); });

    if (q.type === "understand") {
      renderUnderstand(q);
    } else if (q.type !== "review") {
      bindLive(q);
    }
  }

  function bindLive(q) {
    var inputs = document.querySelectorAll('#questionMount input[name="q"]');
    Array.prototype.forEach.call(inputs, function (i) {
      i.addEventListener("change", function () {
        collect();
        renderHeader();
        schedulePersist();
      });
    });
    var inputEl = document.getElementById("q-input");
    if (inputEl) {
      inputEl.addEventListener("input", function () {
        answers[q.id] = textValue();
        renderHeader();
        schedulePersist();
      });
    }
  }

  function scrollTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function collect() {
    var q = steps[step];
    if (q.type === "review" || q.type === "understand") return;
    if (q.type === "textarea" || q.type === "text") {
      answers[q.id] = textValue();
      return;
    }
    var inputs = document.querySelectorAll('#questionMount input[name="q"]');
    if (q.type === "multi") {
      answers[q.id] = selectedValues(inputs);
    } else {
      var checked = Array.prototype.slice.call(inputs).filter(function (i) { return i.checked; });
      answers[q.id] = checked.length ? checked[0].value : null;
    }
  }

  function hasValue(q) {
    var v = answers[q.id];
    if (q.type === "review") return true;
    if (q.type === "understand") return !!(v && v.understand_confirmed === true);
    if (q.type === "textarea") return true;
    if (q.type === "text") return !!(v && String(v).trim());
    if (q.type === "multi") return v && v.length > 0;
    return !!v;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function understandingSummary(u) {
    return I18n.current() === "hi" ? (u.summary_hi || u.summary_en) : (u.summary_en || u.summary_hi);
  }

  function renderUnderstand(q) {
    var mount = document.getElementById("understandingMount");
    if (!mount) return;
    var saved = answers.understand || null;
    if (saved && saved.understand_confirmed === true && saved.summary_en && saved.description === (answers.description || "")) {
      renderUnderstandingResult(mount, saved, true);
      return;
    }
    var desc = answers.description || "";
    if (!desc) {
      mount.innerHTML =
        '<div class="understanding-tip">' +
        '<p class="text-muted mb-3">' + I18n.t("questionnaire.understand.noDescription") + "</p>" +
        '<textarea id="understandText" rows="4" placeholder="' + I18n.t("questionnaire.understand.editPlaceholder") + '"></textarea>' +
        '<div class="question-actions" style="margin-top:var(--space-3);justify-content:flex-start">' +
        '<button class="btn btn-primary" id="understandReBtn">' + I18n.t("questionnaire.understand.reunderstand") + "</button>" +
        "</div></div>";
      document.getElementById("understandReBtn").addEventListener("click", reunderstand);
      return;
    }
    var draft = answers._understandDraft || null;
    if (draft && draft.summary_en && draft.description === desc) {
      renderUnderstandingResult(mount, draft, false);
      return;
    }
    mount.innerHTML = '<div class="text-center py-4"><div class="spinner"></div><p class="mt-3 text-muted">' + I18n.t("questionnaire.understand.think") + "</p></div>";
    API.post("/api/ai/understand", { description: desc }, Auth.token())
      .then(function (u) {
        answers._understandDraft = {
          description: desc,
          sector: u.sector,
          tags: u.tags || [],
          summary_en: u.summary_en || "",
          summary_hi: u.summary_hi || ""
        };
        persist();
        renderUnderstandingResult(mount, u, false);
      })
      .catch(function () {
        mount.innerHTML = '<p class="text-muted">' + I18n.t("questionnaire.understand.failed") + "</p>";
      });
  }

  function renderUnderstandingResult(mount, u, confirmed) {
    var summary = understandingSummary(u) || I18n.t("questionnaire.understand.noSummary");
    var sector = sectorLabel(u.sector);
    var tags = u.tags || [];
    var empty = "";
    if (!summary) empty = " empty-result";

    var html = '<div class="understanding-tip">';
    if (confirmed) {
      html += '<p class="understanding-confirmed-note">' + I18n.t("questionnaire.understand.confirmed") + "</p>";
    }
    html += "<h3 class=\"question-text\" style=\"font-size:1.05rem\">" + I18n.t("questionnaire.understand.explain") + "</h3>";
    html += '<p class="understanding-summary' + empty + '">' + (summary ? escapeHtml(summary) : "—") + "</p>";
    if (sector) {
      html += '<p class="understanding-row"><span class="understanding-label">' + I18n.t("questionnaire.understand.sector") + "</span> <strong>" + escapeHtml(sector) + "</strong></p>";
    }
    if (tags.length) {
      html += '<p class="understanding-row"><span class="understanding-label">' + I18n.t("questionnaire.understand.tags") + "</span> " +
        tags.map(function (t) { return '<span class="tag-chip">' + escapeHtml(t) + "</span>"; }).join(" ") + "</p>";
    }
    html += '<div class="question-actions" style="margin-top:var(--space-4);justify-content:flex-start">' +
      '<button class="btn btn-primary" id="understandYesBtn">' + I18n.t("questionnaire.understand.yes") + "</button>" +
      '<button class="btn btn-secondary" id="understandNoBtn">' + I18n.t("questionnaire.understand.no") + "</button>" +
      "</div>" +
      '<div class="under-edit hidden" id="understandingEdit">' +
      '<p class="text-sm text-muted mb-2">' + I18n.t("questionnaire.understand.edit") + "</p>" +
      '<textarea id="understandText" rows="4">' + escapeHtml(answers.description || "") + "</textarea>" +
      '<div class="question-actions" style="margin-top:var(--space-3);justify-content:flex-start">' +
      '<button class="btn btn-primary" id="understandReBtn">' + I18n.t("questionnaire.understand.reunderstand") + "</button>" +
      '<button class="btn btn-secondary" id="understandCancelBtn">' + I18n.t("common.cancel") + "</button>" +
      "</div></div></div>";

    mount.innerHTML = html;

    document.getElementById("understandYesBtn").addEventListener("click", function () { confirmUnderstanding(u); });
    var noBtn = document.getElementById("understandNoBtn");
    noBtn.addEventListener("click", function () {
      document.getElementById("understandingEdit").classList.remove("hidden");
      noBtn.disabled = true;
    });
    document.getElementById("understandReBtn").addEventListener("click", reunderstand);
    document.getElementById("understandCancelBtn").addEventListener("click", function () {
      renderUnderstandingResult(mount, u, confirmed);
    });
  }

  function confirmUnderstanding(u) {
    if (!Auth.token()) return;
    var desc = answers.description || "";
    API.post("/api/ai/confirm", {
      description: desc,
      sector: u.sector || null,
      tags: u.tags || [],
      summary_en: u.summary_en || "",
      summary_hi: u.summary_hi || ""
    }, Auth.token())
      .then(function (res) {
        answers.understand = {
          understand_confirmed: true,
          description: desc,
          sector: res.sector,
          tags: res.tags || u.tags || [],
          summary_en: res.summary_en,
          summary_hi: res.summary_hi
        };
        answers._understandDraft = null;
        persist();
        renderHeader();
        Notify.show(I18n.t("questionnaire.understand.confirmed"), "success", 1500);
        step++;
        scrollTop();
        render();
      })
      .catch(function (err) {
        Notify.error(err && err.message ? err.message : I18n.t("questionnaire.understand.failed"));
      });
  }

  function reunderstand() {
    var ta = document.getElementById("understandText");
    var text = ta ? ta.value.trim() : "";
    if (!text) {
      Notify.warning(I18n.t("common.required"));
      return;
    }
    answers.description = text;
    answers.understand = null;
    answers._understandDraft = null;
    persist();
    var mount = document.getElementById("understandingMount");
    if (!mount) return;
    mount.innerHTML = '<div class="text-center py-4"><div class="spinner"></div><p class="mt-3 text-muted">' + I18n.t("questionnaire.understand.think") + "</p></div>";
    API.post("/api/ai/understand", { description: text }, Auth.token())
      .then(function (u) {
        answers._understandDraft = {
          description: text,
          sector: u.sector,
          tags: u.tags || [],
          summary_en: u.summary_en || "",
          summary_hi: u.summary_hi || ""
        };
        persist();
        renderUnderstandingResult(mount, u, false);
      })
      .catch(function () { mount.innerHTML = '<p class="text-muted">' + I18n.t("questionnaire.understand.failed") + "</p>"; });
  }

  function onNext() {
    var q = steps[step];
    if (q.type !== "review") {
      collect();
      if (!hasValue(q)) {
        Notify.warning(I18n.t("common.required"));
        return;
      }
      persist();
      Notify.show(I18n.t("questionnaire.toast.saved"), "success", 1200);
    }
    step++;
    if (step >= STEP_TOTAL) {
      renderHeader();
      buildReview();
      submit();
      return;
    }
    scrollTop();
    render();
  }

  function displayValue(q, val) {
    if (val === undefined || val === null || val === "") return "—";
    if (q.type === "multi") {
      return ([]).concat(val).map(function (v) {
        var o = optionsFor(q).filter(function (x) { return x.value === v; })[0];
        return o ? optText(o) : v;
      }).join(", ") || "—";
    }
    var o = optionsFor(q).filter(function (x) { return x.value === val; })[0];
    return o ? optText(o) : String(val);
  }

  function reviewItem(label, display) {
    return '<div class="breakdown-item"><span class="text-sm">' + label + "</span><strong class=\"text-sm\">" + display + "</strong></div>";
  }

  function buildReview() {
    var html = '<div class="card" style="text-align:left"><h3 class="mb-4">' + I18n.t("questionnaire.review") + "</h3>";

    if (profileFilledCount()) {
      html += '<h4 class="text-sm text-muted mb-2">' + I18n.t("questionnaire.review.fromProfile") + "</h4>";
      PROFILE_LOOKUP.forEach(function (l) {
        var raw = prefilledValue(l);
        if (!raw) return;
        var q = Questions.find(l.id);
        if (!q) return;
        var display = l.kind === "category"
          ? (function () { var o = optionsFor(q).filter(function (x) { return x.value === answers[l.id]; })[0]; return o ? optText(o) : (answers[l.id] || raw); })()
          : displayValue(q, answers[l.id]);
        html += reviewItem(I18n.current() === "hi" ? q.title.hi : q.title.en, display);
      });
    }

    for (var i = 0; i < steps.length; i++) {
      var q = steps[i];
      if (q.type === "review" || q.type === "textarea") continue;
      var val = answers[q.id];
      var labelText = I18n.current() === "hi" ? q.title.hi : q.title.en;
      html += reviewItem(labelText, displayValue(q, val));
    }
    if (answers.description) {
      html += reviewItem(I18n.t("profile.description"), escapeHtml(answers.description));
    }
    if (answers.understand && answers.understand.understand_confirmed === true) {
      var ua = answers.understand;
      var usum = I18n.current() === "hi" ? (ua.summary_hi || ua.summary_en) : (ua.summary_en || ua.summary_hi);
      if (usum) {
        html += reviewItem(I18n.t("questionnaire.understand.label"), escapeHtml(usum));
      }
    }
    return html + "</div>";
  }

  function positionPercent() {
    var total = STEP_TOTAL - 1;
    return total > 0 ? Math.round((step / total) * 100) : 0;
  }

  function renderHeader() {
    var ring = document.getElementById("progressRing");
    if (ring) {
      ProgressRing.render(ring, { size: 96, stroke: 8, value: positionPercent(), label: I18n.t("questionnaire.ring") });
    }
    var label = document.getElementById("stepLabel");
    if (label) label.textContent = I18n.t("questionnaire.sub", { step: step + 1, total: STEP_TOTAL });
    var counter = document.getElementById("markedCounter");
    if (counter) counter.textContent = I18n.t("questionnaire.marked", { pct: answeredPercent() });
  }

  function submit() {
    if (!Auth.requireLogin()) return;

    step = STEP_TOTAL - 1;
    persist();

    var socialCategory = profile && profile.social_category ? profile.social_category : "general";
    if (["sc", "st", "obc"].indexOf(socialCategory) === -1) socialCategory = "general";

    var payload = {
      full_name: answers.full_name || "",
      phone_number: answers.phone_number || "",
      age_group: answers.age_group || "",
      gender: answers.gender || "other",
      social_category: socialCategory,
      sector: answers.business_sector,
      business_sector: answers.business_sector,
      state: answers.state,
      business_stage: answers.business_stage,
      annual_revenue: answers.annual_revenue,
      entrepreneur_type: ([]).concat(answers.entrepreneur_type || []).join(",") || null,
      support_needs: ([]).concat(answers.financial || [], answers.non_financial || [])
    };

    var mount = document.getElementById("questionMount");
    mount.innerHTML = '<div style="text-align:center;padding:var(--space-7) 0"><div class="spinner"></div><p class="mt-4">' + I18n.t("common.loading") + "</p></div>";

    var token = Auth.token();

    function done() {
      window.location.href = "results.html";
    }

    API.get("/api/profile", token, { skipAuthRedirect: true })
      .then(function (profile) {
        return API.put("/api/profile", Object.assign({}, payload, {
          full_name: answers.full_name || profile.full_name || "",
          phone_number: answers.phone_number || profile.phone_number || "",
          age_group: answers.age_group || profile.age_group || "",
          gender: answers.gender || profile.gender || "other",
          social_category: socialCategory || profile.social_category || "general",
          sector: undefined,
          business_name: profile.business_name || "",
          district: profile.district || "",
          employee_count: profile.employee_count || "",
          description: answers.description || profile.description || ""
        }), token);
      })
      .catch(function () {
        return API.post("/api/profile", Object.assign({}, payload, {
          business_name: "", district: "", employee_count: "",
          description: answers.description || ""
        }), token);
      })
      .then(done)
      .catch(function (err) {
        Notify.error(err.message);
        window.location.href = "results.html";
      });
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!Auth.requireLogin()) return;

    var token = Auth.token();

    function start() {
      API.get("/api/profile", token, { skipAuthRedirect: true })
        .then(function (p) {
          profile = p;
          prefillFromProfile();
          return API.get("/api/questionnaire/progress", token, { skipAuthRedirect: true });
        })
        .then(function (prog) {
          answers = (prog && prog.answers && typeof prog.answers === "object") ? prog.answers : {};
          prefillFromProfile();
          step = (prog && typeof prog.step === "number") ? prog.step : 0;
          return API.post("/api/questionnaire/dynamic", { answers: answers }, token);
        })
        .then(function (dyn) {
          buildSteps((dyn && dyn.questions) || []);
          if (step >= STEP_TOTAL) step = STEP_TOTAL - 1;
          render();
        })
        .catch(function (err) {
          if (err && err.status === 404) {
            window.location.href = "profile.html";
            return;
          }
          buildSteps([]);
          if (step >= STEP_TOTAL) step = STEP_TOTAL - 1;
          render();
        });
    }

    start();
  });
})();