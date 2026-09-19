(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "register") return;

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("registerForm");
    if (!form) return;
    if (Auth.isLoggedIn()) {
      Auth.routeAfterAuth();
      return;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = document.getElementById("name").value.trim();
      var email = document.getElementById("email").value.trim();
      var phone = document.getElementById("phone").value.trim();
      var password = document.getElementById("password").value;
      var confirm = document.getElementById("confirm").value;
      var errorEl = document.getElementById("formError");
      errorEl.classList.add("hidden");

      if (!Validation.email(email)) {
        errorEl.textContent = I18n.t("auth.email.invalid");
        errorEl.classList.remove("hidden");
        return;
      }
      if (!Validation.phone(phone)) {
        errorEl.textContent = I18n.t("auth.phone.invalid");
        errorEl.classList.remove("hidden");
        return;
      }
      if (!Validation.password(password)) {
        errorEl.textContent = I18n.t("auth.password.invalid");
        errorEl.classList.remove("hidden");
        return;
      }
      if (!Validation.matches(password, confirm)) {
        errorEl.textContent = I18n.t("auth.mismatch");
        errorEl.classList.remove("hidden");
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = I18n.t("common.loading");

      Auth.register(email, password, name, phone)
        .then(function (data) {
          if (data && data.access_token) {
            VStore.set("token", data.access_token);
            if (data.user) VStore.set("user", data.user);
          }
          Notify.success(I18n.t("auth.welcome", { name: name || email }));
          Auth.routeAfterAuth();
        })
        .catch(function (err) {
          errorEl.textContent = err.message;
          errorEl.classList.remove("hidden");
          btn.disabled = false;
          btn.textContent = I18n.t("auth.register.btn");
        });
    });
  });
})();