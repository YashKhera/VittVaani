(function () {
  "use strict";

  window.Modal = {
    open: function (title, bodyHtml, opts) {
      opts = opts || {};
      var backdrop = document.createElement("div");
      backdrop.className = "modal-backdrop";
      backdrop.id = "modalBackdrop";

      var content = "";
      if (title) content += '<h2 class="mb-4">' + title + "</h2>";
      content += bodyHtml || "";
      content += opts.footerHtml || "";

      backdrop.innerHTML =
        '<div class="card modal scale-in" role="dialog" aria-modal="true" aria-label="' + (title || "Dialog") + '">' +
        '<button class="btn-icon" data-modal-close style="position:absolute;top:12px;right:12px;font-size:1.4rem">' + I18n.t("common.close") + " \u00d7</button>" +
        '<div class="modal-body">' + content + "</div></div>";

      document.body.appendChild(backdrop);
      document.body.style.overflow = "hidden";

      var close = function () { backdrop.remove(); document.body.style.overflow = ""; };
      backdrop.querySelectorAll("[data-modal-close]").forEach(function (b) {
        b.addEventListener("click", close);
      });
      backdrop.addEventListener("click", function (e) { if (e.target === backdrop) close(); });
      document.addEventListener("keydown", function esc(ev) {
        if (ev.key === "Escape") { close(); document.removeEventListener("keydown", esc); }
      });

      return { close: close, el: backdrop };
    }
  };
})();