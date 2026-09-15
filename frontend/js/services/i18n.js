(function () {
  "use strict";

  var LANG_KEY = "language";

  window.I18n = {
    current: function () {
      return VStore.get(LANG_KEY, "en");
    },
    setLanguage: function (lang) {
      if (lang !== "en" && lang !== "hi") lang = "en";
      VStore.set(LANG_KEY, lang);
      document.documentElement.lang = lang;
      this.apply();
      window.dispatchEvent(new Event("languagechange"));
    },
    t: function (key, params) {
      var lang = this.current();
      var dict = (window.Translations && Translations[lang]) || {};
      var fallback = (window.Translations && Translations.en) || {};
      var text = dict[key] || fallback[key] || key;
      if (params) {
        text = text.replace(/\{(\w+)\}/g, function (m, k) {
          return params[k] !== undefined ? params[k] : m;
        });
      }
      return text;
    },
    apply: function () {
      var lang = this.current();
      document.documentElement.lang = lang;
      document.querySelectorAll("[data-i18n]").forEach(function (el) {
        var key = el.getAttribute("data-i18n");
        if (key === "landing.hero.h1") {
          el.innerHTML = (window.I18n.t("landing.hero.h1") + " <span class=\"" + el.getAttribute("data-i18n-accent-class") + "\">" + window.I18n.t("landing.hero.h1.accent") + "</span>");
        } else {
          el.textContent = window.I18n.t(key);
        }
      });
      document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
        el.placeholder = window.I18n.t(el.getAttribute("data-i18n-placeholder"));
      });
    }
  };
})();