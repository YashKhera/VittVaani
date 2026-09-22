(function () {
  "use strict";

  if (!document.body || document.body.dataset.page !== "partners") return;
  if (!window.Auth || !window.API) return;
  if (!Auth.isLoggedIn()) { window.location.href = "login.html"; return; }

  var I18n = window.I18n;
  var API = window.API;
  var AuthNS = window.Auth;

  function esc(s) {
    return String(s === undefined || s === null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function el(id) { return document.getElementById(id); }

  var STATE_KEYS = [
    "andhra_pradesh", "arunachal_pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal_pradesh", "jharkhand", "karnataka",
    "kerala", "madhya_pradesh", "maharashtra", "manipur", "meghalaya",
    "mizoram", "nagaland", "odisha", "punjab", "rajasthan", "sikkim",
    "tamil_nadu", "telangana", "tripura", "uttar_pradesh", "uttarakhand",
    "west_bengal", "delhi", "jammu_kashmir", "ladakh"
  ];

  var TYPE_KEYS = [
    { v: "sca", k: "partners.type.sca" },
    { v: "psb", k: "partners.type.psb" },
    { v: "rrb", k: "partners.type.rrb" },
    { v: "nbfc_mfi", k: "partners.type.nbfc" }
  ];

  var CAT_KEYS = [
    { v: "micro_finance", k: "partners.cat.micro" },
    { v: "term_loan", k: "partners.cat.term" },
    { v: "education", k: "partners.cat.educ" }
  ];

  var map = null;
  var markers = null;
  var located = null;

  function inr(n) {
    if (n === null || n === undefined || isNaN(Number(n))) return "\u20B90";
    return "\u20B9" + Math.round(Number(n)).toLocaleString("en-IN");
  }

  function fmtKm(n) {
    if (n === null || n === undefined || isNaN(Number(n))) return "\u2014";
    var v = Number(n);
    if (v < 1) return Math.round(v * 1000) + " m";
    if (v < 10) return v.toFixed(1) + " km";
    return Math.round(v) + " km";
  }

  function fmtPct(n) {
    if (n === null || n === undefined || isNaN(Number(n))) return "\u2014";
    return Number(n).toFixed(1) + "%";
  }

  function healthClass(p) {
    var u = parseFloat(p.fund_utilization_pct);
    var n = parseFloat(p.npa_pct);
    var o = parseFloat(p.overdue_pct);
    if ((isFinite(n) && n > 8) || (isFinite(o) && o > 10)) return "bad";
    if ((isFinite(n) && n > 5) || (isFinite(o) && o > 6) || (isFinite(u) && u < 40)) return "warn";
    return "ok";
  }

  function chip(label, cls, val) {
    return '<span class="chip ' + cls + '">' + label + ": " + val + "</span>";
  }

  function directionsUrl(p) {
    if (p.latitude === null || p.latitude === undefined || p.longitude === null || p.longitude === undefined) {
      var q = encodeURIComponent([p.name, p.city, p.state].filter(Boolean).join(", "));
      return "https://www.google.com/maps/dir/?api=1&destination=" + q;
    }
    return "https://www.google.com/maps/dir/?api=1&destination=" + p.latitude + "," + p.longitude;
  }

  function partnerCard(p, idx) {
    var meta = [p.name + " (" + esc(p.partner_type) + ")"];
    if (p.distance_km !== null && p.distance_km !== undefined) {
      meta.push('<span class="distance-tag">' + fmtKm(p.distance_km) + "</span>");
    }
    var stats =
      chip(I18n.t("partners.utilization"), healthClass(p) === "bad" ? "bad" : "ok", fmtPct(p.fund_utilization_pct)) +
      chip(I18n.t("partners.npa"), healthClass(p) === "bad" ? "bad" : "warn", fmtPct(p.npa_pct)) +
      chip(I18n.t("partners.overdue"), healthClass(p) === "bad" ? "bad" : "warn", fmtPct(p.overdue_pct));

    var loc = [p.state, p.city, p.district, p.pincode].filter(Boolean).join(", ");
    var actions =
      (p.phone ? '<a class="btn btn-secondary btn-sm" href="tel:' + esc(p.phone) + '">' + I18n.t("partners.call") + "</a>" : "") +
      '<a class="btn btn-ghost btn-sm" href="' + directionsUrl(p) + '" target="_blank" rel="noopener">' + I18n.t("partners.directions") + "</a>" +
      (p.website ? '<a class="btn btn-ghost btn-sm" href="' + esc(p.website) + '" target="_blank" rel="noopener">' + I18n.t("partners.website") + "</a>" : "");

    return '<article class="partner-card" data-id="' + p.id + '">' +
      '<div class="rank">' + (idx + 1) + "</div>" +
      '<div class="flex-1">' +
      "<h3>" + esc(p.name) + "</h3>" +
      '<div class="meta">' + meta.join(" · ") + "</div>" +
      (loc ? '<div class="text-muted" style="font-size:var(--font-size-sm)">' + esc(loc) + "</div>" : "") +
      '<div class="stats mt-2">' + stats + "</div>" +
      '<div class="actions mt-2">' + actions + "</div>" +
      "</div></article>";
  }

  function bind(elId, fn, evt) {
    var e = el(elId);
    if (e) e.addEventListener(evt || "click", fn);
    return e;
  }

  function t(key) { return I18n.t(key); }

  function populateSelects() {
    var stateSel = el("stateSelect");
    if (stateSel) {
      var shtml = '<option value=""></option>';
      STATE_KEYS.forEach(function (k) {
        shtml += '<option value="' + k + '">' + t("states." + k) + "</option>";
      });
      stateSel.innerHTML = shtml;
    }

    var typeSel = el("typeSelect");
    if (typeSel) {
      var thtml = '<option value=""></option>';
      TYPE_KEYS.forEach(function (o) {
        thtml += '<option value="' + o.v + '">' + t(o.k) + "</option>";
      });
      typeSel.innerHTML = thtml;
    }

    var catSel = el("schemeInput");
    if (catSel) {
      var chtml = '<option value=""></option>';
      CAT_KEYS.forEach(function (o) {
        chtml += '<option value="' + o.v + '">' + t(o.k) + "</option>";
      });
      catSel.innerHTML = chtml;
    }
  }

  function readFilters() {
    return {
      partner_type: (el("typeSelect") && el("typeSelect").value) || "",
      state: (el("stateSelect") && el("stateSelect").value) || "",
      pincode: (el("pincodeInput") && el("pincodeInput").value.trim()) || "",
      loan_category: (el("schemeInput") && el("schemeInput").value) || ""
    };
  }

  function buildQuery(f) {
    var parts = [];
    if (f.partner_type) parts.push("partner_type=" + encodeURIComponent(f.partner_type));
    if (f.state) parts.push("state=" + encodeURIComponent(f.state));
    if (f.pincode) parts.push("pincode=" + encodeURIComponent(f.pincode));
    if (f.loan_category) parts.push("loan_category=" + encodeURIComponent(f.loan_category));
    return parts.join("&");
  }

  function showStatus(msg, isError) {
    var s = el("locateStatus");
    if (!s) return;
    s.textContent = msg;
    s.classList.toggle("text-error", !!isError);
    s.classList.remove("hidden");
  }

  function locateByBrowser() {
    if (!navigator.geolocation) {
      showStatus(t("partners.error.geolocation"), true);
      return;
    }
    showStatus(t("partners.locating"));
    navigator.geolocation.getCurrentPosition(
      function (pos) {
        located = { lat: pos.coords.latitude, lon: pos.coords.longitude };
        showStatus(t("partners.located") + " " + pos.coords.latitude.toFixed(3) + ", " + pos.coords.longitude.toFixed(3));
        run({
          lat: located.lat,
          lon: located.lon,
          partner_type: (el("typeSelect") && el("typeSelect").value) || "",
          loan_category: (el("schemeInput") && el("schemeInput").value) || ""
        });
      },
      function () { showStatus(t("partners.error.location"), true); },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  }

  function run(q) {
    var list = el("partnerList");
    var sum = el("resultSummary");
    var btn = el("searchBtn");
    if (btn) { btn.disabled = true; btn.textContent = t("partners.loading"); }

    var path;
    if (q.lat !== undefined && q.lon !== undefined) {
      path = "/api/partners/nearest?lat=" + encodeURIComponent(q.lat) + "&lon=" + encodeURIComponent(q.lon) +
        "&max_distance_km=50" + (q.partner_type ? "&partner_type=" + encodeURIComponent(q.partner_type) : "") +
        (q.loan_category ? "&loan_category=" + encodeURIComponent(q.loan_category) : "") + "&limit=20";
      API.get(path, AuthNS.token()).then(function (d) {
        render(d.partners || [], d, q);
      }).catch(function (err) {
        if (list) list.innerHTML = '<p class="text-muted p-3">' + esc(err.message) + "</p>";
      }).finally(function () {
        if (btn) { btn.disabled = false; btn.textContent = t("partners.search"); }
      });
      return;
    }

    var f = readFilters();
    if (!f.state && !f.pincode) {
      if (list) list.innerHTML = '<p class="text-muted p-3">' + esc(t("partners.error.filters")) + "</p>";
      if (btn) { btn.disabled = false; btn.textContent = t("partners.search"); }
      return;
    }

    path = "/api/partners?" + buildQuery(f) + "&limit=50";
    API.get(path, AuthNS.token()).then(function (d) {
      render(d.partners || [], d, { lat: null, lon: null });
    }).catch(function (err) {
      if (list) list.innerHTML = '<p class="text-muted p-3">' + esc(err.message) + "</p>";
    }).finally(function () {
      if (btn) { btn.disabled = false; btn.textContent = t("partners.search"); }
    });
  }

  function render(items, d, q) {
    var list = el("partnerList");
    var sum = el("resultSummary");
    if (!list) return;

    if (!items.length) {
      list.innerHTML = '<p class="text-muted p-3">' + esc(t("partners.none")) + "</p>";
      if (sum) sum.textContent = "0 " + t("partners.found");
      return;
    }

    var sorted = items.slice().sort(function (a, b) {
      var da = a.distance_km === null || a.distance_km === undefined ? Infinity : Number(a.distance_km);
      var db = b.distance_km === null || b.distance_km === undefined ? Infinity : Number(b.distance_km);
      if (da !== db) return da - db;
      var ha = (Number(a.npa_pct) || 0) + (Number(a.overdue_pct) || 0) - (Number(a.fund_utilization_pct) || 0);
      var hb = (Number(b.npa_pct) || 0) + (Number(b.overdue_pct) || 0) - (Number(b.fund_utilization_pct) || 0);
      return ha - hb;
    });

    list.innerHTML = sorted.map(function (p, i) { return partnerCard(p, i); }).join("");
    if (sum) sum.textContent = items.length + " " + t("partners.found");

    if (q.lat !== undefined && q.lon !== undefined && q.lat !== null) {
      initShownMap(sorted, q);
    } else {
      var w = el("partnerMap");
      if (w) w.innerHTML = '<div class="partner-map-placeholder">' + esc(t("partners.map.hint")) + "</div>";
    }
  }

  function initShownMap(items, q) {
    var wrap = el("partnerMap");
    if (!wrap) return;
    if (!window.L) {
      wrap.innerHTML = '<div class="partner-map-placeholder">' + esc(t("partners.map.unavailable")) + "</div>";
      return;
    }

    if (!map) {
      map = L.map(wrap).setView([q.lat, q.lon], 12);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      markers = L.layerGroup().addTo(map);
    } else {
      map.setView([q.lat, q.lon], Math.max(map.getZoom(), 11));
    }

    markers.clearLayers();
    var bounds = L.latLngBounds([[q.lat, q.lon]]);
    L.marker([q.lat, q.lon], { icon: userIcon() }).addTo(markers).bindPopup(t("partners.you"));

    items.forEach(function (p) {
      if (p.latitude === null || p.latitude === undefined || p.longitude === null || p.longitude === undefined) return;
      var icon = healthIcon(healthClass(p));
      var popup =
        '<div class="popup-name">' + esc(p.name) + "</div>" +
        '<div class="popup-meta">' + esc([p.city, p.state].filter(Boolean).join(", ")) + "</div>" +
        (p.distance_km !== null && p.distance_km !== undefined ? '<div class="popup-meta">' + fmtKm(p.distance_km) + "</div>" : "") +
        '<div class="popup-meta">' + I18n.t("partners.utilization") + ": " + fmtPct(p.fund_utilization_pct) + "</div>" +
        '<div class="popup-meta">' + I18n.t("partners.npa") + ": " + fmtPct(p.npa_pct) + "</div>" +
        '<div class="popup-meta">' + I18n.t("partners.overdue") + ": " + fmtPct(p.overdue_pct) + "</div>" +
        '<a class="btn btn-primary btn-sm mt-1" href="' + directionsUrl(p) + '" target="_blank" rel="noopener">' + I18n.t("partners.directions") + "</a>";
      L.marker([p.latitude, p.longitude], { icon: icon }).addTo(markers)
        .bindPopup(popup, { maxWidth: 280 });
      bounds.extend([p.latitude, p.longitude]);
    });

    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
    if (map.once) map.once("popupopen", function () {});
  }

  function userIcon() {
    return L.divIcon({
      className: "map-pin user",
      html: '<div class="map-pin-dot user"></div>',
      iconSize: [14, 14]
    });
  }

  function healthIcon(cls) {
    return L.divIcon({
      className: "map-pin " + (cls || "ok"),
      html: '<div class="map-pin-dot ' + (cls || "ok") + '"></div>',
      iconSize: [14, 14]
    });
  }

  function init() {
    populateSelects();
    bind("searchBtn", function () { run({ lat: undefined, lon: undefined }); });
    bind("locateBtn", locateByBrowser);
    var form = el("partnerSearchForm");
    if (form) form.addEventListener("submit", function (e) { e.preventDefault(); run({ lat: undefined, lon: undefined }); });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
