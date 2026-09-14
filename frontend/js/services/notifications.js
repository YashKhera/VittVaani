(function () {
  "use strict";

  window.Notify = {
    _container: null,
    _ensureContainer: function () {
      if (!this._container) {
        this._container = document.createElement("div");
        this._container.className = "toast-container";
        this._container.setAttribute("role", "status");
        this._container.setAttribute("aria-live", "polite");
        document.body.appendChild(this._container);
      }
      return this._container;
    },
    show: function (message, type, duration) {
      type = type || "info";
      duration = duration || 3500;
      var toast = document.createElement("div");
      toast.className = "toast toast-" + type + " fade-in-up";
      toast.textContent = message;
      this._ensureContainer().appendChild(toast);
      setTimeout(function () {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.3s";
        setTimeout(function () { toast.remove(); }, 320);
      }, duration);
    },
    success: function (msg) { this.show(msg, "success"); },
    error: function (msg) { this.show(msg, "error", 5000); },
    warning: function (msg) { this.show(msg, "warning"); }
  };
})();