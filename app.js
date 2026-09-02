(function () {
  "use strict";

  var body = document.body;
  var headers = document.querySelectorAll("[data-header]");
  var toggles = document.querySelectorAll(".nav-toggle");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.documentElement.classList.add("js");

  // Header border once the page has scrolled
  if (headers.length) {
    var setScrolled = function () {
      var scrolled = window.scrollY > 8;
      headers.forEach(function (h) { h.classList.toggle("is-scrolled", scrolled); });
    };
    setScrolled();
    window.addEventListener("scroll", setScrolled, { passive: true });
  }

  // Mobile navigation
  function closeNav() {
    body.classList.remove("nav-open");
    toggles.forEach(function (t) {
      t.setAttribute("aria-expanded", "false");
      t.setAttribute("aria-label", "Open navigation");
    });
  }

  toggles.forEach(function (toggle) {
    toggle.addEventListener("click", function () {
      var open = body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
    });
  });

  document.querySelectorAll(".primary-nav a").forEach(function (link) {
    link.addEventListener("click", closeNav);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeNav();
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 900) closeNav();
  });

  // Reveal on scroll
  var revealTargets = document.querySelectorAll("[data-reveal]");
  if (revealTargets.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealTargets.forEach(function (el) { el.classList.add("is-in"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
      revealTargets.forEach(function (el) { io.observe(el); });
    }
  }

  // Hero device entrance
  document.querySelectorAll(".hero").forEach(function (hero) {
    window.requestAnimationFrame(function () {
      hero.classList.add("is-ready");
    });
  });

  // Footer year
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  // Contact form: prepares an email in the visitor's mail app.
  // Nothing is sent or stored by the website.
  document.querySelectorAll("[data-contact-form]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;

      var data = new FormData(form);
      if (String(data.get("website") || "").trim()) return; // honeypot

      var name = String(data.get("name") || "").trim();
      var email = String(data.get("email") || "").trim();
      var company = String(data.get("company") || "").trim();
      var kind = String(data.get("kind") || "").trim();
      var message = String(data.get("message") || "").trim();

      var lines = [
        "Name: " + name,
        "Email: " + email,
        company ? "Company: " + company : null,
        kind ? "Project type: " + kind : null,
        "",
        message
      ].filter(function (line) { return line !== null; });

      var subject = "Project inquiry" + (company ? " from " + company : name ? " from " + name : "");
      var href = "mailto:contact@fintlock.com?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));

      var status = form.querySelector(".form-status");
      if (status) status.textContent = "Your email app should open with the message ready to send.";
      window.location.href = href;
    });
  });
}());
