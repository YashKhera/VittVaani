(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "login") return;

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("loginForm");
    if (!form) return;
    if (Auth.isLoggedIn()) {
      Auth.routeAfterAuth();
      return;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = document.getElementById("email").value.trim();
      var password = document.getElementById("password").value;
      var errorEl = document.getElementById("formError");
      errorEl.classList.add("hidden");

      if (!Validation.email(email)) {
        errorEl.textContent = I18n.t("auth.email.invalid");
        errorEl.classList.remove("hidden");
        return;
      }
      if (!Validation.password(password)) {
        errorEl.textContent = I18n.t("auth.password.invalid");
        errorEl.classList.remove("hidden");
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = I18n.t("common.loading");

      Auth.login(email, password)
        .then(function () {
          Notify.success(I18n.t("auth.welcome", { name: (Auth.user() && Auth.user().name) || email }));
          Auth.routeAfterAuth();
        })
        .catch(function (err) {
          errorEl.textContent = err.message;
          errorEl.classList.remove("hidden");
          btn.disabled = false;
          btn.textContent = I18n.t("auth.login.btn");
        });
    });
  });
})();