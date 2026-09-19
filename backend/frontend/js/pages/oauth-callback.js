(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "oauth") return;

  document.addEventListener("DOMContentLoaded", function () {
    var params = window.readQuery ? window.readQuery() : {};
    if (params.error) {
      window.location.href = "../login.html?error=" + encodeURIComponent(params.error);
      return;
    }
    var token = params.token || params.access_token || params.code || params.oauthtoken || "";
    if (!token) {
      var spinner = document.querySelector(".spinner");
      if (spinner) spinner.classList.add("hidden");
      var msg = document.getElementById("oauthMessage");
      if (msg) msg.classList.remove("hidden");
      return;
    }
    VStore.set("token", token);
    if (params.email) {
      VStore.set("user", { email: params.email, name: params.name || "Google User", google: true });
    }
    Auth.routeAfterAuth();
  });
})();