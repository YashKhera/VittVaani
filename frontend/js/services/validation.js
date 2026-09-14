(function () {
  "use strict";

  window.Validation = {
    email: function (val) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(val || "").trim());
    },
    password: function (val) {
      return String(val || "").length >= 8 && /\d/.test(val);
    },
    phone: function (val) {
      return /^[6-9]\d{9}$/.test(String(val || "").trim());
    },
    required: function (val) {
      return String(val || "").trim().length > 0;
    },
    matches: function (a, b) {
      return String(a || "") === String(b || "");
    },
    messages: function (fieldKey, value) {
      return {
        email: I18n.t("auth.email.invalid"),
        password: I18n.t("auth.password.invalid"),
        phone: I18n.t("auth.phone.invalid"),
        required: I18n.t("common.required")
      }[fieldKey];
    }
  };
})();