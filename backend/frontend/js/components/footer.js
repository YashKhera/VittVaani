(function () {
  "use strict";

  window.Footer = {
    render: function () {
      var el = document.getElementById("siteFooter");
      if (!el) return;
      el.innerHTML =
        '<footer class="footer no-print">' +
        '<div class="container">' +
        '<p class="mb-2" data-i18n="footer.about">' + I18n.t("footer.about") + "</p>" +
        '<p class="text-sm mb-0">&copy; ' + new Date().getFullYear() + " VittVaani. <span data-i18n=\"footer.rights\">" + I18n.t("footer.rights") + "</span></p>" +
        "</div></footer>";
      I18n.apply();
    }
  };
})();

window.Skeleton = {
  show: function (mount, count) {
    count = count || 3;
    mount.innerHTML = "";
    for (var i = 0; i < count; i++) {
      var s = document.createElement("div");
      s.className = "skeleton";
      s.style.height = "120px";
      s.style.marginBottom = "16px";
      mount.appendChild(s);
    }
  }
};