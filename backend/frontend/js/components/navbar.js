(function () {
  "use strict";

  window.Navbar = {
    render: function () {
      var header = document.getElementById("navbar");
      if (!header) return;
      var loggedIn = Auth.isLoggedIn();
      var user = Auth.user();
      var currentPath = window.location.pathname || "/";

      var items = [{ href: "/", key: "nav.home" }];
      if (loggedIn) {
        items = items.concat([
          { href: "/questionnaire", key: "nav.questions" },
          { href: "/results", key: "nav.results" },
          { href: "/calculator", key: "nav.calculator" },
          { href: "/partners", key: "nav.partners" },
          { href: "/saved-schemes", key: "nav.saved" },
          { href: "/profile-view", key: "nav.profile" }
        ]);
      }

      var links = items.map(function (item) {
        var active = currentPath === item.href ? " active" : "";
        return '<a class="nav-link' + active + '" href="' + item.href + '" data-i18n="' + item.key + '">' + I18n.t(item.key) + "</a>";
      }).join("");

      var authLinks = loggedIn
        ? '<button class="btn btn-secondary btn-sm" id="logoutBtn" data-i18n="nav.logout">' + I18n.t("nav.logout") + "</button>"
        : '<a class="btn btn-ghost btn-sm" href="/login" data-i18n="nav.login">' + I18n.t("nav.login") + "</a>" +
          '<a class="btn btn-primary btn-sm" href="/register" data-i18n="nav.register">' + I18n.t("nav.register") + "</a>";

      header.innerHTML =
        '<div class="navbar-inner container">' +
        '<a class="navbar-brand" href="/"><img src="/assets/logo.svg" alt="VittVaani logo" aria-hidden="true"/><span data-i18n="app.name">' + I18n.t("app.name") + "</span></a>" +
        '<nav class="navbar-links" aria-label="Primary">' + links + "</nav>" +
        '<div class="navbar-actions">' +
        '<button class="icon-btn" id="themeToggle" aria-label="Toggle theme">' + (Theme.current() === "dark" ? "☀️" : "🌙") + "</button>" +
        '<select id="langSelect" class="no-print" style="width:auto" aria-label="Language">' +
        I18n.optionsHtml() +
        "</select>" +
        authLinks +
        "</div></div>";

      var sel = document.getElementById("langSelect");
      sel.value = I18n.current();
      sel.addEventListener("change", function () {
        I18n.setLanguage(sel.value);
        Navbar.render();
      });
      document.getElementById("themeToggle").addEventListener("click", function () {
        Theme.toggle();
      });
      var logout = document.getElementById("logoutBtn");
      if (logout) {
        logout.addEventListener("click", function () {
          Auth.logout();
          window.location.href = "/";
        });
      }
      I18n.apply();
    },

    setActive: function (key) {
      document.querySelectorAll(".nav-link").forEach(function (a) {
        a.classList.toggle("active", a.getAttribute("data-i18n") === key);
      });
    }
  };
})();