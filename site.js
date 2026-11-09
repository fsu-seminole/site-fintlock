/* Fintlock site script. Plain JavaScript, no dependencies. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function store(key, val) {
    try { if (val === undefined) return localStorage.getItem(key); localStorage.setItem(key, val); } catch (e) { return null; }
  }

  // ---- Light / navy switch (the class is set before paint by an inline script in <head>)
  document.querySelectorAll(".skin-btn").forEach(function (btn) {
    function label() { btn.setAttribute("aria-label", doc.classList.contains("skin-navy") ? "Switch to light colors" : "Switch to navy colors"); }
    label();
    btn.addEventListener("click", function () {
      var navy = doc.classList.toggle("skin-navy");
      store("fl-skin", navy ? "navy" : "light");
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute("content", navy ? "#050b18" : "#eef1f7");
      label();
    });
  });

  // ---- Floating nav shadow + mobile menu
  var pill = document.getElementById("navpill");
  if (pill) {
    var onScroll = function () { pill.classList.toggle("scrolled", window.scrollY > 20); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }
  var sheet = document.getElementById("sheet"), openBtn = document.getElementById("menu-open"), closeBtn = document.getElementById("menu-close");
  if (sheet && openBtn && closeBtn) {
    var setMenu = function (open) {
      sheet.classList.toggle("open", open);
      openBtn.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
      (open ? closeBtn : openBtn).focus({ preventScroll: true });
    };
    openBtn.addEventListener("click", function () { setMenu(true); });
    closeBtn.addEventListener("click", function () { setMenu(false); });
    sheet.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && sheet.classList.contains("open")) setMenu(false); });
  }

  // ---- TV theme tabs: rotate until someone picks one
  document.querySelectorAll(".tabs").forEach(function (tabsEl) {
    var tabs = [].slice.call(tabsEl.querySelectorAll(".tab"));
    var host = tabsEl.parentElement;
    var imgs = [].slice.call(host.querySelectorAll(".shots img"));
    if (!tabs.length || !imgs.length) return;
    var cur = 0, timer = null, picked = false;
    function show(i) {
      cur = i;
      tabs.forEach(function (t, n) { t.setAttribute("aria-selected", String(n === i)); t.tabIndex = n === i ? 0 : -1; });
      imgs.forEach(function (m, n) { m.classList.toggle("on", n === i); });
    }
    function stop() { clearInterval(timer); timer = null; }
    tabs.forEach(function (t, n) {
      t.addEventListener("click", function () { picked = true; stop(); show(n); });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        e.preventDefault(); picked = true; stop();
        var next = (cur + d + tabs.length) % tabs.length; show(next); tabs[next].focus();
      });
    });
    show(0);
    if (!reduce && "IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting && !timer && !picked) timer = setInterval(function () { show((cur + 1) % tabs.length); }, 3800);
          else if (!en.isIntersecting) stop();
        });
      }, { threshold: 0.4 }).observe(host);
    }
  });

  // ---- Live App Store details (Apple's public lookup service)
  var appEls = document.querySelectorAll("[data-app-store]");
  if (appEls.length && window.fetch) {
    var id = appEls[0].getAttribute("data-app-store");
    var cacheKey = "fl-app-" + id, cached = null;
    try { cached = JSON.parse(store(cacheKey) || "null"); } catch (e) { cached = null; }
    var render = function (r) {
      var updated = new Date(r.currentVersionReleaseDate);
      var bits = ['<span class="dot">Live on the App Store</span>', "<span>Version " + r.version + "</span>"];
      if (!isNaN(updated)) bits.push("<span>Updated " + updated.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) + "</span>");
      if (r.formattedPrice) bits.push("<span>" + r.formattedPrice + "</span>");
      if (r.userRatingCount >= 1) bits.splice(1, 0, "<span>★ " + Number(r.averageUserRating).toFixed(1) + " (" + r.userRatingCount + (r.userRatingCount === 1 ? " rating" : " ratings") + ")</span>");
      appEls.forEach(function (el) { el.innerHTML = bits.join(""); el.hidden = false; });
    };
    if (cached && Date.now() - cached.t < 6 * 3600 * 1000) render(cached.r);
    else fetch("https://itunes.apple.com/lookup?id=" + id + "&country=us")
      .then(function (res) { return res.json(); })
      .then(function (d) { var r = d.results && d.results[0]; if (!r) return; store(cacheKey, JSON.stringify({ t: Date.now(), r: { version: r.version, currentVersionReleaseDate: r.currentVersionReleaseDate, formattedPrice: r.formattedPrice, averageUserRating: r.averageUserRating || 0, userRatingCount: r.userRatingCount || 0 } })); render(r); })
      .catch(function () { /* leave the badges hidden */ });
  }

  // ---- Contact form: send through FormSubmit, fall back to the visitor's email app
  var form = document.querySelector("[data-contact-form]");
  if (form) {
    var params = new URLSearchParams(location.search);
    var kind = form.querySelector('[name="kind"]');
    if (kind && params.get("type") === "tv") kind.value = "TV SmartHub";
    var status = form.querySelector(".form-status");
    if (params.get("sent") === "1" && status) { status.textContent = "Thanks. Your note is in our inbox, and we'll reply within one business day."; status.className = "form-status ok"; }
    var src = document.createElement("input");
    src.type = "hidden"; src.name = "came_from"; src.value = document.referrer ? document.referrer.replace(location.origin, "") || "/" : "direct";
    form.appendChild(src);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      if (String(data.get("_honey") || "").trim()) return;
      var btn = form.querySelector('[type="submit"]');
      if (btn) btn.disabled = true;
      if (status) { status.textContent = "Sending…"; status.className = "form-status"; }
      var payload = {};
      data.forEach(function (v, k) { payload[k] = v; });
      payload._subject = "Project inquiry" + (payload.kind ? " (" + payload.kind + ")" : "") + " from " + (payload.company || payload.name || "fintlock.com");
      fetch("https://formsubmit.co/ajax/contact@fintlock.com", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().then(function (j) { if (!r.ok || String(j.success) === "false") throw new Error(j.message || "Send failed"); }); })
        .then(function () {
          form.reset();
          if (status) { status.textContent = "Thanks. Your note is in our inbox, and we'll reply within one business day."; status.className = "form-status ok"; }
        })
        .catch(function () {
          var body = ["Name: " + (payload.name || ""), "Email: " + (payload.email || ""), payload.company ? "Company: " + payload.company : "", payload.kind ? "Project type: " + payload.kind : "", "", payload.message || ""].filter(Boolean).join("\n");
          if (status) { status.innerHTML = 'That didn\'t send. <a href="mailto:contact@fintlock.com?subject=' + encodeURIComponent(payload._subject) + "&body=" + encodeURIComponent(body) + '">Send it from your email app instead</a>.'; status.className = "form-status err"; }
        })
        .then(function () { if (btn) btn.disabled = false; });
    });
  }

  // ---- 404: pick the lock
  var game = document.querySelector("[data-lock-game]");
  if (game) {
    var board = game.querySelector(".game-board"), lock = game.querySelector(".lock");
    var pins = [].slice.call(game.querySelectorAll(".pin")), say = game.querySelector(".game-status");
    var timeEl = game.querySelector("[data-time]"), bestEl = game.querySelector("[data-best]"), again = game.querySelector("[data-reset]");
    var best = parseFloat(store("fl-lock-best") || "0") || 0;
    if (best) bestEl.textContent = best.toFixed(1) + "s";
    var idx, pos, dir, speed, zones, running, started, raf, H = 120 - 8;
    function reset() {
      idx = 0; pos = 0; dir = 1; speed = 1.6; running = false; started = 0; zones = [];
      pins.forEach(function (p) {
        p.className = "pin";
        var z = 14 + Math.random() * (H - 50); zones.push(z);
        p.querySelector(".zone").style.top = z + "px";
        p.querySelector(".tick").style.transform = "translateY(0)";
      });
      lock.classList.remove("open"); again.hidden = true; timeEl.textContent = "0.0s";
      say.textContent = "Press space or tap to start.";
    }
    function loop(t) {
      if (!running) return;
      pos += dir * speed * (reduce ? 0.6 : 1);
      if (pos <= 0 || pos >= H) { dir *= -1; pos = Math.max(0, Math.min(H, pos)); }
      pins[idx].querySelector(".tick").style.transform = "translateY(" + pos + "px)";
      timeEl.textContent = ((performance.now() - started) / 1000).toFixed(1) + "s";
      raf = requestAnimationFrame(loop);
    }
    function act() {
      if (idx >= pins.length) return;
      if (!running) { running = true; started = started || performance.now(); say.textContent = "Pin 1 of 3. Tap inside the yellow zone."; raf = requestAnimationFrame(loop); return; }
      var z = zones[idx], center = pos + 4;
      if (center >= z && center <= z + 22) {
        pins[idx].classList.add("set"); idx++;
        speed += 0.7;
        if (idx === pins.length) {
          running = false; cancelAnimationFrame(raf);
          var secs = (performance.now() - started) / 1000;
          lock.classList.add("open");
          var record = !best || secs < best;
          if (record) { best = secs; store("fl-lock-best", String(secs)); bestEl.textContent = secs.toFixed(1) + "s"; }
          say.textContent = "Unlocked in " + secs.toFixed(1) + "s" + (record ? ". New best!" : ".") + " Now, where were you headed?";
          again.hidden = false;
        } else { pos = 0; dir = 1; say.textContent = "Pin " + (idx + 1) + " of 3."; }
      } else {
        var p = pins[idx]; p.classList.remove("miss"); void p.offsetWidth; p.classList.add("miss");
        say.textContent = "Missed. Pin " + (idx + 1) + " of 3, try again.";
      }
    }
    board.addEventListener("pointerdown", function (e) { if (e.target.closest("[data-reset]")) return; e.preventDefault(); act(); });
    board.addEventListener("keydown", function (e) { if (e.key === " " || e.key === "Enter") { if (e.target.closest("[data-reset]")) return; e.preventDefault(); act(); } });
    document.addEventListener("keydown", function (e) { if (e.key === " " && document.activeElement === document.body) { e.preventDefault(); act(); } });
    again.addEventListener("click", function () { cancelAnimationFrame(raf); reset(); board.focus(); });
    reset();
  }

  // ---- Footer year
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  // ---- A note for the curious
  try {
    var v = (document.querySelector('meta[name="fintlock-version"]') || {}).content || "";
    var y = "color:#ffd438;font-family:monospace;font-size:12px;line-height:1.15";
    console.log(
      "%c      ████████\n    ██        ██\n    ██        ██\n  ████████████████\n  ██████    ██████\n  ████        ████\n  ██████    ██████\n  ████████████████", y);
    console.log("%cfintlock%c  v" + v, "font:600 22px Sora,system-ui,sans-serif;color:#101d35;background:#ffd438;padding:4px 12px;border-radius:99px", "color:#7c89a3;font:12px monospace");
    console.log("%cLike poking around under the hood? So do we.\nThis site is plain HTML, CSS and a little JavaScript. No frameworks, no trackers.\nSay hi: contact@fintlock.com  ·  Psst: try fintlock.com/404", "font:14px/1.6 'DM Sans',system-ui,sans-serif;color:#5b6579");
  } catch (e) {}
})();
