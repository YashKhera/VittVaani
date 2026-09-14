(function () {
  "use strict";
  if (!document.body || document.body.dataset.page !== "reset-password") return;

  document.addEventListener("DOMContentLoaded", function () {
    var emailForm = document.getElementById("emailStep");
    var otpForm = document.getElementById("otpStep");
    var pwForm = document.getElementById("resetPasswordForm");
    if (!emailForm || !otpForm || !pwForm) return;

    var errorEl = document.getElementById("formError");
    var noteEl = document.getElementById("formNote");
    var dots = Array.prototype.slice.call(document.querySelectorAll(".step-dot"));
    var currentEmail = "";
    var resetToken = "";

    function showError(msg) {
      errorEl.textContent = msg;
      errorEl.classList.remove("hidden");
      noteEl.classList.add("hidden");
    }
    function hideError() { errorEl.classList.add("hidden"); }
    function showNote(msg) {
      noteEl.textContent = msg;
      noteEl.classList.remove("hidden");
      errorEl.classList.add("hidden");
    }
    function hideNote() { noteEl.classList.add("hidden"); }
    function goToStep(step) {
      emailForm.classList.toggle("hidden", step !== 1);
      otpForm.classList.toggle("hidden", step !== 2);
      pwForm.classList.toggle("hidden", step !== 3);
      dots.forEach(function (d) { d.classList.toggle("active", parseInt(d.dataset.step, 10) <= step); });
    }
    function setBtn(btn, text, disabled) {
      btn.disabled = disabled;
      btn.textContent = text;
    }

    function sendOtp() {
      hideError();
      var email = document.getElementById("email").value.trim();
      if (!Validation.email(email)) { showError(I18n.t("auth.email.invalid")); return; }
      var btn = emailForm.querySelector('button[type="submit"]');
      setBtn(btn, I18n.t("common.loading"), true);
      API.post("/api/auth/forgot-password", { email: email })
        .then(function () {
          currentEmail = email;
          setBtn(btn, I18n.t("auth.otp.sendBtn"), false);
          hideError();
          showNote(I18n.t("auth.otp.sent"));
          goToStep(2);
          document.getElementById("otp").focus();
        })
        .catch(function (err) {
          setBtn(btn, I18n.t("auth.otp.sendBtn"), false);
          showError(err.message);
        });
    }

    function verifyOtp() {
      hideError();
      var otp = document.getElementById("otp").value.trim();
      if (!/^\d{6}$/.test(otp)) { showError(I18n.t("auth.otp.invalid")); return; }
      if (!currentEmail) { goToStep(1); return; }
      var btn = otpForm.querySelector('button[type="submit"]');
      setBtn(btn, I18n.t("common.loading"), true);
      API.post("/api/auth/verify-otp", { email: currentEmail, otp: otp })
        .then(function (data) {
          resetToken = data.reset_token;
          document.getElementById("resetToken").value = resetToken;
          setBtn(btn, I18n.t("auth.otp.verifyBtn"), false);
          hideNote();
          goToStep(3);
          document.getElementById("newPassword").focus();
        })
        .catch(function (err) {
          setBtn(btn, I18n.t("auth.otp.verifyBtn"), false);
          showError(err.message);
        });
    }

    emailForm.addEventListener("submit", function (e) { e.preventDefault(); sendOtp(); });
    otpForm.addEventListener("submit", function (e) { e.preventDefault(); verifyOtp(); });

    document.getElementById("resendOtp").addEventListener("click", function (e) {
      e.preventDefault();
      if (currentEmail) sendOtp();
    });
    document.getElementById("backToEmail").addEventListener("click", function (e) {
      e.preventDefault();
      hideNote();
      goToStep(1);
    });

    pwForm.addEventListener("submit", function (e) {
      e.preventDefault();
      hideError();
      var pw = document.getElementById("newPassword").value;
      var confirm = document.getElementById("confirmNewPassword").value;
      if (!Validation.password(pw)) { showError(I18n.t("auth.password.invalid")); return; }
      if (!Validation.matches(pw, confirm)) { showError(I18n.t("auth.mismatch")); return; }
      if (!resetToken) { showError(I18n.t("auth.otp.invalid")); goToStep(2); return; }

      var btn = pwForm.querySelector('button[type="submit"]');
      setBtn(btn, I18n.t("common.loading"), true);

      API.post("/api/auth/reset-password", { token: resetToken, new_password: pw })
        .then(function () {
          Notify.success(I18n.t("auth.reset.success"));
          window.location.href = "login.html";
        })
        .catch(function (err) {
          setBtn(btn, I18n.t("auth.reset.btn"), false);
          showError(err.message);
        });
    });

    var params = window.readQuery ? window.readQuery() : {};
    if (params && params.token) {
      resetToken = params.token;
      document.getElementById("resetToken").value = resetToken;
      goToStep(3);
    }
    var otpBox = document.getElementById("otp");
    if (otpBox) {
      otpBox.addEventListener("input", function () { otpBox.value = otpBox.value.replace(/\D/g, "").slice(0, 6); });
    }
  });
})();