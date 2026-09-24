(function () {
  "use strict";

  var API_BASE = (function () {
    var host = window.location && window.location.hostname;
    if (host === "localhost" || host === "127.0.0.1" || host === "0.0.0.0") {
      return "http://" + host + ":8001";
    }
    return "";
  })();

  var API = {
    base: API_BASE,
    request: function (method, path, body, token, opts) {
      opts = opts || {};
      var o = {
        method: method,
        headers: { "Content-Type": "application/json" }
      };
      if (body !== undefined && body !== null) o.body = JSON.stringify(body);
      if (token) o.headers["Authorization"] = "Bearer " + token;

      return fetch(API_BASE + path, o).then(function (res) {
        return res.text().then(function (text) {
          var data = null;
          try { data = text ? JSON.parse(text) : null; } catch (e) { data = text; }
          if (!res.ok) {
            var err = new Error((data && data.detail) || ("Request failed with status " + res.status));
            err.status = res.status;
            err.data = data;
            if (res.status === 401 && token && !opts.skipAuthRedirect) {
              try {
                if (window.Auth) Auth.logout();
              } catch (e) {}
              var path = window.location.pathname || "/";
              if (path !== "/login" && path !== "/register" && path !== "/" &&
                  path.indexOf("/oauth/") !== 0) {
                window.location.href = "/login?next=" + encodeURIComponent(path + window.location.search);
                return;
              }
            }
            throw err;
          }
          return data;
        });
      });
    },
    get: function (path, token, opts) { return this.request("GET", path, null, token, opts); },
    post: function (path, body, token) { return this.request("POST", path, body, token); },
    put: function (path, body, token) { return this.request("PUT", path, body, token); },
    del: function (path, token) { return this.request("DELETE", path, null, token); }
  };

  window.API = API;
})();