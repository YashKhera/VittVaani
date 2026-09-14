(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    Theme.set(Theme.current());
    I18n.apply();
    if (window.Auth && Auth.isLoggedIn() && !Auth.user()) {
      Auth.me().then(function () {
        Navbar.render();
      }).catch(function () {
        Auth.logout();
      });
    }
    Navbar.render();
    Footer.render();
  });

  window.formatINR = function (num) {
    if (num === null || num === undefined) return "";
    var rupee = "₹";
    if (num >= 10000000) return rupee + (num / 10000000).toFixed(num % 10000000 === 0 ? 0 : 1) + " Cr";
    if (num >= 100000) return rupee + Math.round(num / 100000) + "L";
    if (num >= 1000) return rupee + Math.round(num / 1000) + "K";
    return rupee + Math.round(num);
  };

  window.readQuery = function () {
    var out = {};
    var qs = window.location.search.replace("?", "").split("&");
    qs.forEach(function (kv) {
      if (!kv) return;
      var p = kv.split("=");
      out[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || "");
    });
    return out;
  };
})();