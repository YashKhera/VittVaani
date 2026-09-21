(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "calculator") return;

  var schemeParam = null;
  var schemesCache = null;

  function esc(s) {
    return String(s === undefined || s === null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function inr(n) {
    if (n === null || n === undefined || isNaN(n)) return "₹0";
    var v = Math.round(Number(n));
    return "₹" + v.toLocaleString("en-IN");
  }

  function fmtLakh(n) {
    var v = Math.round(Number(n));
    var l = v / 100000;
    if (l >= 100) return "₹" + (l / 100).toFixed(1).replace(/\.0$/, "") + " Cr";
    if (l >= 1) return "₹" + (l % 1 === 0 ? l.toFixed(0) : l.toFixed(1).replace(/\.0$/, "")) + "L";
    return inr(v);
  }

  function bindRange(id, outputId, fmt) {
    var el = document.getElementById(id);
    var out = outputId ? document.getElementById(outputId) : null;
    if (!el) return null;
    var update = function () {
      if (out) out.textContent = fmt ? fmt(parseFloat(el.value)) : el.value;
    };
    el.addEventListener("input", update);
    update();
    return el;
  }

  function readCost() { return parseFloat(document.getElementById("costInput").value) || 0; }
  function readRate() { return parseFloat(document.getElementById("rateInput").value) || 0; }
  function readTenure() { return parseInt(document.getElementById("tenureInput").value, 10) || 0; }
  function readCoverage() { return parseFloat(document.getElementById("coverageInput").value) || 0; }
  function readMora() { return parseInt(document.getElementById("moraInput").value, 10) || 0; }
  function readSubsidy() { return parseFloat(document.getElementById("subsidyInput").value) || 0; }
  function readUpfront() { return parseFloat(document.getElementById("upfrontInput").value) || 0; }

  function amortizationTable(rows) {
    if (!rows || !rows.length) return "";
    var thead = "<thead><tr><th>Mo</th><th>Opening</th><th>EMI</th><th>Interest</th><th>Principal</th><th>Closing</th></tr></thead>";
    var tbody = rows.map(function (r) {
      return "<tr>" +
        "<td>" + r.month + "</td>" +
        "<td>" + fmtLakh(r.opening_balance) + "</td>" +
        "<td>" + inr(r.emi) + "</td>" +
        "<td>" + inr(r.interest) + "</td>" +
        "<td>" + inr(r.principal) + "</td>" +
        "<td>" + fmtLakh(r.closing_balance) + "</td>" +
        "</tr>";
    }).join("");
    return '<table class="compare-table"><' + thead + '<tbody>' + tbody + "</tbody></table>";
  }

  function renderResult(d) {
    document.getElementById("calcPlaceholder").classList.add("hidden");
    var res = document.getElementById("calcResults");
    res.classList.remove("hidden");
    document.getElementById("resEMI").textContent = inr(d.emi);
    document.getElementById("resFinanced").textContent = fmtLakh(d.financed_amount);
    document.getElementById("resInterest").textContent = inr(d.total_interest);
    document.getElementById("resTotal").textContent = fmtLakh(d.total_payment);
    document.getElementById("resMora").textContent = inr(d.moratorium_interest || 0);
    document.getElementById("resYears").textContent = ((d.tenure_months || 0) / 12).toFixed(1);
    document.getElementById("moraNote").classList.toggle("hidden", !(d.moratorium_months > 0));
    document.getElementById("amortTableWrap").innerHTML = amortizationTable(d.amortization || []);
  }

  function calculate() {
    var btn = document.getElementById("calcBtn");
    btn.disabled = true;
    btn.textContent = I18n.t("calculator.loading");
    API.post("/api/calculator", {
      project_cost: readCost(),
      interest_rate_annual: readRate(),
      tenure_months: readTenure(),
      coverage_percent: readCoverage(),
      moratorium_months: readMora(),
      subsidy_amount: readSubsidy(),
      upfront_payment: readUpfront()
    }, Auth.token()).then(function (d) {
      renderResult(d);
    }).catch(function (err) {
      Notify.error(err.message);
    }).finally(function () {
      btn.disabled = false;
      btn.textContent = I18n.t("calculator.calculate");
    });
  }

  function loadSchemes() {
    var list = document.getElementById("schemeList");
    if (schemesCache) { renderSchemeList(list, schemesCache); return Promise.resolve(schemesCache); }
    API.get("/api/calculator/schemes", Auth.token(), { skipAuthRedirect: true })
      .then(function (data) {
        schemesCache = data.items || [];
        renderSchemeList(list, schemesCache);
      })
      .catch(function (err) {
        list.innerHTML = '<p class="text-muted p-3">' + esc(err.message) + "</p>";
      });
  }

  function renderSchemeList(list, items) {
    if (!items.length) { list.innerHTML = '<p class="text-muted p-3">' + I18n.t("common.notFound") + "</p>"; return; }
    list.innerHTML = items.map(function (s) {
      return '<label class="compare-item">' +
        '<input type="checkbox" value="' + s.scheme_id + '"' +
        (schemeParam && String(s.scheme_id) === String(schemeParam) ? " checked" : "") + "> " +
        "<span>" + esc(s.scheme_name) + "</span>" +
        "<span class=\"text-sm text-muted\"> — " + s.interest_rate + "% · " + Math.round(s.coverage_percent) + "% cov." + "</span>" +
        "</label>";
    }).join("");
  }

  function selectedSchemeIds() {
    return Array.prototype.map.call(
      document.querySelectorAll("#schemeList input[type=checkbox]:checked"),
      function (cb) { return parseInt(cb.value, 10); }
    );
  }

  function compare() {
    var ids = selectedSchemeIds();
    if (!ids.length) { Notify.warning(I18n.t("common.required")); return; }
    if (ids.length > 5) { Notify.warning("Max 5"); return; }
    var btn = document.getElementById("compareBtn");
    btn.disabled = true;
    btn.textContent = I18n.t("calculator.loading");
    API.post("/api/calculator/schemes", {
      scheme_ids: ids,
      project_cost: readCost(),
      tenure_months: parseInt(document.getElementById("cmpTenure").value, 10) || 60,
      default_coverage_percent: 100
    }, Auth.token()).then(function (d) {
      var body = document.getElementById("compareBody");
      body.innerHTML = d.items.map(function (it) {
        return "<tr><td>" + esc(it.scheme_name) + "</td>" +
          "<td>" + it.interest_rate + "%</td>" +
          "<td>" + Math.round(it.coverage_percent) + "%</td>" +
          "<td>" + it.moratorium_months + "</td>" +
          "<td><strong>" + inr(it.emi) + "</strong></td>" +
          "<td>" + inr(it.total_interest) + "</td></tr>";
      }).join("");
      document.getElementById("compareResult").classList.remove("hidden");
      document.getElementById("compareResult").scrollIntoView({ behavior: "smooth", block: "nearest" });
    }).catch(function (err) {
      Notify.error(err.message);
    }).finally(function () {
      btn.disabled = false;
      btn.textContent = I18n.t("calculator.compare.btn");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!Auth.requireLogin()) return;
    var params = window.readQuery ? window.readQuery() : {};
    schemeParam = params.scheme ? decodeURIComponent(params.scheme) : null;

    bindRange("costInput", "costOutput", fmtLakh);
    bindRange("rateInput", "rateOutput", function (v) { return v + "%"; });
    bindRange("tenureInput", "tenureOutput", function (v) { return v + " mo"; });
    bindRange("coverageInput", "coverageOutput", function (v) { return v + "%"; });
    bindRange("moraInput", "moraOutput", function (v) { return v + " mo"; });
    bindRange("subsidyInput", "subsidyOutput", fmtLakh);
    bindRange("upfrontInput", "upfrontOutput", fmtLakh);
    bindRange("cmpTenure", null, null);

    var cmpTenure = document.getElementById("cmpTenure");
    var cmpLabel = document.getElementById("cmpTenureLabel");
    cmpTenure.addEventListener("input", function () {
      cmpLabel.textContent = this.value + " months";
    });
    cmpLabel.textContent = cmpTenure.value + " months";

    document.getElementById("calcBtn").addEventListener("click", calculate);
    document.getElementById("compareBtn").addEventListener("click", compare);

    if (schemeParam && params.autocalc === "1") {
      loadSchemes().then(function () { compare(); });
    } else {
      loadSchemes();
      calculate();
    }
  });
})();