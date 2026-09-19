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
      var page = nextPage || window.location.pathname.split("/").pop() || "";
      window.location.href = "login.html?next=" + encodeURIComponent(page + window.location.search);
      return false;
    },
    routeAfterAuth: function () {
      function dest(rel) {
        return (window.location.pathname.indexOf("/oauth/") !== -1 ? "../" : "") + rel;
      }
      if (!this.isLoggedIn()) {
        var page = window.location.pathname.split("/").pop() || "";
        window.location.href = "login.html?next=" + encodeURIComponent(page + window.location.search);
        return;
      }
      API.get("/api/profile", this.token(), { skipAuthRedirect: true })
        .then(function (profile) {
          if (profile && profile.ai_confirmed) {
            window.location.href = dest("results.html");
          } else if (profile) {
            window.location.href = dest("questionnaire.html");
          } else {
            window.location.href = dest("profile.html");
          }
        })
        .catch(function (err) {
          if (err && err.status === 404) {
            window.location.href = dest("profile.html");
          } else {
            window.location.href = dest("results.html");
          }
        });
    },
    updateUser: function (user) {
      VStore.set(USER_KEY, user);
    }
  };
})();