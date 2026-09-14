(function () {
  "use strict";

  window.ProgressRing = {
    defaults: { size: 120, stroke: 10, color: "#667eea", track: "#e5e7eb", value: 0, label: null, sublabel: null },
    render: function (mount, opts) {
      var o = Object.assign({}, this.defaults, opts || {});
      var size = o.size, stroke = o.stroke;
      var r = (size - stroke) / 2;
      var c = 2 * Math.PI * r;
      var pct = Math.max(0, Math.min(100, o.value));
      var offset = c - (pct / 100) * c;
      var prev = parseFloat(mount.getAttribute("data-value") || "0");
      mount.setAttribute("data-value", String(pct));

      mount.innerHTML =
        '<div class="progress-ring-wrap" style="width:' + size + 'px;height:' + size + 'px">' +
        '<svg width="' + size + '" height="' + size + '" class="progress-ring-svg">' +
        '<circle stroke="' + o.track + '" stroke-width="' + stroke + '" fill="none" cx="' + size / 2 + '" cy="' + size / 2 + '" r="' + r + '"/>' +
        '<circle class="progress-ring-circle" stroke="' + o.color + '" stroke-width="' + stroke + '" fill="none" ' +
        'cx="' + size / 2 + '" cy="' + size / 2 + '" r="' + r + '" stroke-linecap="round" stroke-dasharray="' + c + '" ' +
        'stroke-dashoffset="' + c + '" transform="rotate(-90 ' + size / 2 + ' ' + size / 2 + ')"/>' +
        '</svg>' +
        '<div class="progress-ring-value">' +
        '<span class="match-score-value">' + Math.round(pct) + '%</span>' +
        (o.label ? '<span class="text-sm text-muted">' + o.label + '</span>' : '') +
        (o.sublabel ? '<span class="text-sm">' + o.sublabel + '</span>' : '') +
        '</div></div>';

      requestAnimationFrame(function () {
        var circle = mount.querySelector(".progress-ring-circle");
        if (!circle) return;
        var fromOffset = c - (prev / 100) * c;
        circle.style.transition = "none";
        circle.style.strokeDashoffset = String(fromOffset);
        requestAnimationFrame(function () {
          circle.style.transition = "stroke-dashoffset 1s ease";
          circle.style.strokeDashoffset = String(offset);
        });
      });
    }
  };
})();