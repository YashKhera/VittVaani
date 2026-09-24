(function () {
  "use strict";

  var TOKEN_KEY = "token";
  var USER_KEY = "user";

  window.Auth = {
    register: function (email, password, name, phone) {
      return API.post("/api/auth/register", { email: email, password: password, name: name, phone_number: phone || "" });
    },
    login: function (email, password) {
      return API.post("/api/auth/login", { email: email, password: password }).then(function (data) {
        if (data && data.access_token) {
          VStore.set(TOKEN_KEY, data.access_token);
        }
        if (data && data.user) {
          VStore.set(USER_KEY, data.user);
        }
        return data;
      });
    },
    logout: function () {
      VStore.remove(TOKEN_KEY);
      VStore.remove(USER_KEY);
      if (window.AppStore && AppStore.clearUserData) AppStore.clearUserData();
    },
    token: function () {
      return VStore.get(TOKEN_KEY, null);
    },
    userId: function () {
      var u = this.user();
      return u && u.id;
    },
    me: function () {
      var token = this.token();
      if (!token) return Promise.reject(new Error("Not authenticated"));
      return API.get("/api/auth/me", token).then(function (user) {
        if (user) VStore.set(USER_KEY, user);
        return user;
      });
    },
    user: function () {
      return VStore.get(USER_KEY, null);
    },
    isLoggedIn: function () {
      return !!this.token();
    },
    requireLogin: function (nextPage) {
      if (this.isLoggedIn()) return true;
      var path = nextPage || window.location.pathname || "/";
      window.location.href = "/login?next=" + encodeURIComponent(path + window.location.search);
      return false;
    },
    routeAfterAuth: function () {
      function dest(clean) {
        return clean; // all routes are root-relative clean URLs
      }
      if (!this.isLoggedIn()) {
        var path = window.location.pathname || "/";
        window.location.href = "/login?next=" + encodeURIComponent(path + window.location.search);
        return;
      }
      API.get("/api/profile", this.token(), { skipAuthRedirect: true })
        .then(function (profile) {
          if (profile && profile.ai_confirmed) {
            window.location.href = dest("/results");
          } else if (profile) {
            window.location.href = dest("/questionnaire");
          } else {
            window.location.href = dest("/profile");
          }
        })
        .catch(function (err) {
          if (err && err.status === 404) {
            window.location.href = dest("/profile");
          } else {
            window.location.href = dest("/results");
          }
        });
    },
    updateUser: function (user) {
      VStore.set(USER_KEY, user);
    }
  };
})();