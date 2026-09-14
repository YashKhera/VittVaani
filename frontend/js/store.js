(function () {
  "use strict";

  var USER_KEYS = ["answers", "lastMatch", "cachedSchemes", "savedIds"];

  function scoped(key) {
    var uid = (window.Auth && Auth.user() && Auth.user().id) || "anon";
    var sc = "u" + String(uid) + ":";
    return key.indexOf(sc) === 0 ? key : sc + key;
  }

  window.AppStore = {
    _keys: {
      answers: "answers",
      lastMatch: "lastMatch",
      cachedSchemes: "cachedSchemes",
      savedIds: "savedIds"
    },

    scopeFor: function (userId) {
      var uid = userId !== undefined && userId !== null ? String(userId) : "anon";
      return "u" + uid + ":";
    },

    getAnswers: function () {
      return VStore.get(scoped(this._keys.answers), {});
    },
    saveAnswers: function (answers) {
      return VStore.set(scoped(this._keys.answers), answers);
    },
    clearAnswers: function () {
      VStore.remove(scoped(this._keys.answers));
    },

    getLastMatch: function () {
      return VStore.get(scoped(this._keys.lastMatch), null);
    },
    saveLastMatch: function (result) {
      return VStore.set(scoped(this._keys.lastMatch), result);
    },

    getCachedSchemes: function () {
      return VStore.get(scoped(this._keys.cachedSchemes), null);
    },
    cacheSchemes: function (schemes) {
      return VStore.set(scoped(this._keys.cachedSchemes), schemes);
    },

    getSavedIds: function () {
      return VStore.get(scoped(this._keys.savedIds), []);
    },
    setSavedIds: function (ids) {
      return VStore.set(scoped(this._keys.savedIds), ids);
    },

    getLast: function () {
      return this.getLastMatch();
    },
    setLast: function (match) {
      return this.saveLastMatch(match);
    },

    clearUserData: function () {
      USER_KEYS.forEach(function (key) {
        VStore.remove(scoped(key));
        VStore.remove(key);
      });
    },

    enqueueRecommendations: function (list) {
      var cached = this.getCachedSchemes() || [];
      var byId = {};
      cached.forEach(function (s) {
        var id = s.id !== undefined ? s.id : s.scheme_id;
        if (id !== undefined) byId[id] = true;
      });
      (list || []).forEach(function (item) {
        var s = item.scheme ? item.scheme : item;
        var id = s.id !== undefined ? s.id : (s.scheme_id !== undefined ? s.scheme_id : item.id);
        if (id !== undefined && !byId[id]) {
          byId[id] = true;
          cached.push(s);
        }
      });
      return this.cacheSchemes(cached);
    }
  };
})();