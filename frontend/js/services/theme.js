(function () {
  "use strict";

  var THEME_KEY = "theme";

  window.Theme = {
    current: function () {
      return document.documentElement.getAttribute("data-theme") || VStore.get(THEME_KEY, "") || "light";
    },
    toggle: function () {
      this.set(this.current() === "dark" ? "light" : "dark");
      return this.current();
    },
    set: function (theme) {
      VStore.set(THEME_KEY, theme);
      document.documentElement.setAttribute("data-theme", theme);
      var btn = document.getElementById("themeToggle");
      if (btn) {
        btn.textContent = theme === "dark" ? "☀️" : "🌙";
        btn.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
      }
      this.refreshMeta();
    },
    refreshMeta: function () {
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) {
        meta.setAttribute("content", this.current() === "dark" ? "#0f1117" : "#ffffff");
      }
    }
  };
})();