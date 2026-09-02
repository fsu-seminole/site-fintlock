#!/usr/bin/env python3
"""Assembles the five Fintlock pages from shared chrome + per-page bodies.
Run: python3 build.py  (writes *.html next to this file)."""

import pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://fintlock.com"
EMAIL = "contact@fintlock.com"
CSS_V = "2"
JS_V = "2"

ARROW = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EXT = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6 3h7v7M13 3 5 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

NAV = [("work.html", "Work"), ("services.html", "Services"), ("contact.html", "Contact")]


def head(title, description, path, og_description=None):
    url = SITE + "/" + (path if path != "index.html" else "")
    og = og_description or description
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <meta property="og:site_name" content="Fintlock">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/brand/fintlock-social-card.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#060c18">
  <link rel="icon" type="image/svg+xml" href="assets/brand/fintlock-favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400..600&family=Geist+Mono:wght@400;500&display=swap">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400..600&family=Geist+Mono:wght@400;500&display=swap" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400..600&family=Geist+Mono:wght@400;500&display=swap"></noscript>
  <link rel="stylesheet" href="styles.css?v={CSS_V}">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
"""


def header(current):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    links.append('<a class="btn btn-primary btn-sm nav-cta" href="contact.html">Start a project</a>')
    return f"""
  <header class="site-header" data-header>
    <div class="wrap header-inner">
      <a class="brand" href="index.html" aria-label="Fintlock home">
        <img src="assets/brand/fintlock-wordmark-on-dark.svg" alt="Fintlock" width="108" height="28">
      </a>
      <nav class="primary-nav" id="primary-nav" aria-label="Primary">
        {"".join(links)}
      </nav>
      <button class="nav-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="primary-nav"><span></span><span></span></button>
    </div>
  </header>

  <main id="main">
"""


def footer(current):
    links = []
    for href, label in NAV + [("privacy.html", "Privacy")]:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <a class="footer-brand" href="index.html" aria-label="Fintlock home"><img src="assets/brand/fintlock-wordmark-on-dark.svg" alt="Fintlock" width="100" height="26"></a>
          <p>A software studio in Tampa, Florida. iPhone apps, desktop tools, and web software for businesses with specific needs.</p>
        </div>
        <nav class="footer-nav" aria-label="Footer">
          {"".join(links)}
        </nav>
        <div class="footer-meta">
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <span>Tampa, Florida</span>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span data-year>2026</span> Fintlock LLC</span>
        <span>Custom software, designed and built in Tampa</span>
      </div>
    </div>
  </footer>

  <script src="app.js?v={JS_V}" defer></script>
</body>
</html>
"""


def cta(heading="Tell us what needs to work better.", sub="A few sentences about the problem, who deals with it, and what you would like to change is enough to start. We reply within one business day."):
    return f"""
    <section class="cta">
      <div class="wrap cta-grid">
        <div data-reveal>
          <p class="label">Contact</p>
          <h2 style="margin-top:20px">{heading}</h2>
          <p>{sub}</p>
        </div>
        <div class="cta-side" data-reveal style="--delay:120ms">
          <a class="btn btn-primary" href="contact.html">Start a project {ARROW}</a>
          <a class="email" href="mailto:{EMAIL}">{EMAIL}</a>
          <small>Tampa, Florida. Working with clients across the US.</small>
        </div>
      </div>
    </section>
"""


SERVICES = [
    ("01", "iPhone apps", "Native, start to finish",
     "Product planning, interface design, native Swift development, testing, and App Store submission. We build the whole app, not a wrapper around a website.",
     "A typical engagement covers the whole path: sketching the flows, designing the screens, building the app in Swift, getting it through TestFlight with your own testers, and handling the App Store listing and review. If the app needs a backend, we build that too.",
     ["SwiftUI", "StoreKit", "TestFlight", "App Store Connect"]),
    ("02", "Desktop and internal software", "Windows and Mac",
     "Tools for documents, reporting, specialized data, and the repetitive work that has outgrown a spreadsheet. Built for the handful of people who use them every day.",
     "These are the tools a company runs on and nobody outside it ever sees: estimating, quoting, spec checking, document generation, and reporting that pulls three systems into one screen. We build them to run well on the hardware you already have and to be simple enough to hand to a new hire.",
     ["Windows", "macOS", "Reporting", "Document workflows"]),
    ("03", "Web products and integrations", "Browser software and APIs",
     "Customer portals, internal browser tools, and connections between the systems you already pay for, so information stops being retyped from one to the next.",
     "A portal where clients can check the status of an order. An internal tool that replaces the shared spreadsheet. An integration that moves data between your accounting, CRM, and field systems without anyone copying and pasting. Built for the browser, so there is nothing to install.",
     ["Portals", "Internal tools", "API integration", "Automation"]),
    ("04", "Technology integration", "AI, automation, and data",
     "Practical help evaluating and adopting AI, automation, connected systems, and modern data tools. We have particular depth in construction and building materials.",
     "New tools arrive faster than anyone can evaluate them. We help you work out which ones are worth adopting, then connect them to the way you already operate. In construction and building materials, that tends to mean quoting, supplier data, specifications, and job documentation.",
     ["AI", "Automation", "Connected systems", "Construction"]),
]


def service_rows(long=False):
    out = ['<div class="service-list">']
    for i, (num, name, sub, desc, detail, tags) in enumerate(SERVICES):
        tag_html = "".join(f"<li>{t}</li>" for t in tags)
        more = f'<p class="service-detail">{detail}</p>' if long else ""
        out.append(f"""
        <article class="service-row" data-reveal style="--delay:{i * 60}ms">
          <span class="service-num">{num}</span>
          <h3>{name}<small>{sub}</small></h3>
          <div>
            <p>{desc}</p>{more}
            <ul aria-label="Typical work">{tag_html}</ul>
          </div>
        </article>""")
    out.append("</div>")
    return "".join(out)


PROCESS = """
    <div class="process" data-reveal>
      <div>
        <span class="step-num">1</span>
        <h3>Scope</h3>
        <p>We start with a conversation about what happens today and what needs to change. From that you get a written scope and a price before any code is written.</p>
        <div class="step-out"><span>You get</span>A written scope and a fixed price</div>
      </div>
      <div>
        <span class="step-num">2</span>
        <h3>Build</h3>
        <p>Design and development run in short cycles. You review working software as it comes together, on your own phone or desk, rather than a slide deck about it.</p>
        <div class="step-out"><span>You get</span>Working builds to review along the way</div>
      </div>
      <div>
        <span class="step-num">3</span>
        <h3>Launch</h3>
        <p>App Store submission, deployment, documentation, and a proper handover. When it ships, your team can run it, and we are still reachable when something needs attention.</p>
        <div class="step-out"><span>You get</span>A shipped product and the keys to it</div>
      </div>
    </div>
"""


# ---------------------------------------------------------------- HOME

HOME = f"""
    <section class="hero">
      <div class="wrap">
        <div class="hero-top">
          <p class="label" data-reveal>Software studio / Tampa, Florida</p>
          <h1 data-reveal style="--delay:60ms">iPhone apps and business software, made to <em>fit.</em></h1>
        </div>
        <div class="hero-grid">
          <div class="hero-copy">
            <p class="lead" data-reveal style="--delay:120ms">Fintlock is a small software studio in Tampa, Florida. We design and build native iPhone apps, desktop tools, and web software for businesses with specific needs, and we help teams put AI and automation to practical use.</p>
            <div class="actions" data-reveal style="--delay:180ms">
              <a class="btn btn-primary" href="contact.html">Start a project {ARROW}</a>
              <a class="text-link" href="work.html">See the work {ARROW}</a>
            </div>
            <div class="hero-meta" data-reveal style="--delay:240ms">
              <span>Swift and SwiftUI</span>
              <span>Web and desktop</span>
              <span>Direct collaboration</span>
            </div>
          </div>

          <a class="stage" href="work.html#fintley" aria-label="Fintley, a native iPhone app built by Fintlock">
            <div class="stage-caption"><span>Built by Fintlock</span><strong>Fintley / Native iPhone</strong></div>
            <div class="device-fan" aria-hidden="true">
              <div class="device device-2"><img src="assets/screens/fintley-forecast-dark-480.webp" srcset="assets/screens/fintley-forecast-dark-480.webp 480w, assets/screens/fintley-forecast-dark.webp 720w" sizes="(max-width: 640px) 160px, 232px" alt="" width="480" height="1043" decoding="async"></div>
              <div class="device device-1"><img src="assets/screens/fintley-home-dark-480.webp" srcset="assets/screens/fintley-home-dark-480.webp 480w, assets/screens/fintley-home-dark.webp 720w" sizes="(max-width: 640px) 160px, 232px" alt="" width="480" height="1043" decoding="async" fetchpriority="high"></div>
              <div class="device device-3"><img src="assets/screens/fintley-deal-lab-dark-480.webp" srcset="assets/screens/fintley-deal-lab-dark-480.webp 480w, assets/screens/fintley-deal-lab-dark.webp 720w" sizes="(max-width: 640px) 160px, 232px" alt="" width="480" height="1043" decoding="async"></div>
            </div>
          </a>
        </div>

        <div class="proof" aria-label="How Fintlock works">
          <div data-reveal><span>Before we start</span><strong>A written scope and a price</strong></div>
          <div data-reveal style="--delay:60ms"><span>While we build</span><strong>Working builds you can review</strong></div>
          <div data-reveal style="--delay:120ms"><span>Who you talk to</span><strong>The people writing the code</strong></div>
          <div data-reveal style="--delay:180ms"><span>When it ships</span><strong>You own the code and the accounts</strong></div>
        </div>
      </div>
    </section>

    <section class="section" id="work" aria-labelledby="work-title">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">Selected work</p>
            <h2 id="work-title">Products we designed and built.</h2>
          </div>
          <p data-reveal style="--delay:100ms">Fintlock builds its own iPhone products alongside client work. They are the clearest way to see how we think about an interface, and how much we care about the details.</p>
        </div>

        <article class="case" id="fintley">
          <div class="case-copy" data-reveal>
            <p class="label">01 / Fintley / iPhone</p>
            <h3 class="display">Any address, appraised in seconds.</h3>
            <p class="lead">Type an address and Fintley returns a full investment read: estimated value, rent, comparable sales, cash flow, and a Forecast score from 1 to 100.</p>
            <p>Built in SwiftUI, with a Deal Lab for testing your own assumptions, a Watchlist, and market overviews across the US.</p>
            <dl class="facts">
              <div><dt>Platform</dt><dd>iPhone</dd></div>
              <div><dt>Built with</dt><dd>SwiftUI</dd></div>
              <div><dt>Website</dt><dd>fintley.app</dd></div>
            </dl>
            <div class="actions">
              <a class="text-link" href="work.html#fintley">More about Fintley {ARROW}</a>
              <a class="text-link" href="https://fintley.app" rel="noopener">fintley.app {EXT}</a>
            </div>
          </div>
          <div class="case-media" data-reveal style="--delay:120ms">
            <div class="screens" aria-label="Fintley screens">
              <figure><figcaption>Home</figcaption><img src="assets/screens/fintley-home-dark.webp" alt="Fintley home screen with a search field, recent reports, and featured markets" width="720" height="1565" decoding="async" loading="lazy"></figure>
              <figure><figcaption>Forecast</figcaption><img src="assets/screens/fintley-forecast-dark.webp" alt="Fintley appraisal with a value range, cap rate, rent, cash flow, and Forecast score" width="720" height="1565" decoding="async" loading="lazy"></figure>
              <figure><figcaption>Deal Lab</figcaption><img src="assets/screens/fintley-deal-lab-dark.webp" alt="Fintley Deal Lab with adjustable assumptions and monthly cash flow" width="720" height="1565" decoding="async" loading="lazy"></figure>
            </div>
          </div>
        </article>

        <article class="case" id="plants-in-pocket">
          <div class="case-copy" data-reveal>
            <p class="label">02 / Plants in Pocket / iPhone</p>
            <h3 class="display">Identify a plant, then keep it alive.</h3>
            <p class="lead">Identify a plant, check its health, and turn the result into a care plan you can follow. Built for people who keep plants and would like fewer surprises.</p>
            <dl class="facts">
              <div><dt>Platform</dt><dd>iPhone</dd></div>
              <div><dt>Category</dt><dd>Plant care</dd></div>
              <div><dt>Status</dt><dd>Launching 2026</dd></div>
            </dl>
            <div class="actions">
              <a class="text-link" href="work.html#plants-in-pocket">More about Plants in Pocket {ARROW}</a>
              <a class="text-link" href="https://www.tiktok.com/@plantsinpocket" rel="noopener">@plantsinpocket {EXT}</a>
            </div>
          </div>
          <div class="case-media" data-reveal style="--delay:120ms">
            <div class="plants-panel">
              <img src="assets/work/plants-primary-logo.webp" alt="Plants in Pocket logo: a potted plant beside the name" width="430" height="243" decoding="async" loading="lazy">
              <div class="plants-steps" aria-hidden="true"><span>Identify</span><span>Check health</span><span>Care plan</span></div>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="services-title" style="border-top:1px solid var(--line)">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">Services</p>
            <h2 id="services-title">What we build.</h2>
          </div>
          <p data-reveal style="--delay:100ms">Four kinds of work, all done in-house. Every project starts with a conversation about the problem, not a template.</p>
        </div>
        {service_rows()}
        <div style="margin-top:32px" data-reveal><a class="text-link" href="services.html">How a project runs {ARROW}</a></div>
      </div>
    </section>

    <section class="section" aria-labelledby="process-title" style="border-top:1px solid var(--line)">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">Process</p>
            <h2 id="process-title">From a first email to a working product.</h2>
          </div>
          <p data-reveal style="--delay:100ms">Three stages, each ending with something you can hold, read, or install. You have a price before work starts, and the invoice matches it.</p>
        </div>
        {PROCESS}
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="studio-title" style="border-top:1px solid var(--line)">
      <div class="wrap statement">
        <div data-reveal>
          <p class="label" id="studio-title">The studio</p>
          <p class="display" style="margin-top:22px">Small on purpose. The people you talk to on the first call are the people writing the code, all the way to launch.</p>
        </div>
        <div class="statement-aside" data-reveal style="--delay:120ms">
          <p>Fintlock is based in Tampa, Florida and works with owners and teams directly. Most of what we build lives inside a business and never appears on a website, which is exactly the kind of software that has to be right.</p>
          <div class="stack" aria-label="Where we work">
            <div><span>Mobile</span><span>Swift, SwiftUI</span></div>
            <div><span>Desktop</span><span>Windows, macOS</span></div>
            <div><span>Web</span><span>Browser apps, APIs</span></div>
            <div><span>Based in</span><span>Tampa, FL</span></div>
          </div>
        </div>
      </div>
    </section>

{cta()}
"""

# ---------------------------------------------------------------- WORK

WORK_CTA_SUB = 'Both apps went through the same process we use for client work: a written scope, working builds to review, and a proper handover. <a href="services.html" style="color:var(--ink);border-bottom:1px solid var(--line-3)">See how a project runs</a>, or tell us what you need. We reply within one business day.'

WORK = f"""
    <section class="page-intro">
      <div class="wrap">
        <div class="page-intro-grid">
          <div data-reveal>
            <p class="label">Work</p>
            <h1>Two products, start to finish.</h1>
          </div>
          <p data-reveal style="--delay:100ms">Both were designed and built in-house, from the first sketch to the App Store listing. They are the best public record of how we work.</p>
        </div>
        <nav class="product-index" aria-label="Products on this page" data-reveal style="--delay:160ms">
          <a href="#fintley"><span class="num">01</span><span><strong>Fintley</strong><small>Real estate appraisal for iPhone</small></span>{ARROW}</a>
          <a href="#plants-in-pocket"><span class="num">02</span><span><strong>Plants in Pocket</strong><small>Plant identification and care for iPhone</small></span>{ARROW}</a>
        </nav>
      </div>
    </section>

    <section class="section" id="fintley" aria-labelledby="fintley-title">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">01 / Fintley / iPhone</p>
            <h2 id="fintley-title">Any address, appraised in seconds.</h2>
          </div>
          <p data-reveal style="--delay:100ms">Fintley turns an address into a structured investment report. Value, rent, comparable sales, cash flow, and market context, in one native iPhone app.</p>
        </div>

        <div class="screens screens-4" data-reveal aria-label="Fintley screens">
          <figure><figcaption>Home</figcaption><img src="assets/screens/fintley-home-dark.webp" alt="Fintley home screen with a search field, recent reports, and featured markets" width="720" height="1565" decoding="async"></figure>
          <figure><figcaption>Appraisal</figcaption><img src="assets/screens/fintley-forecast-dark.webp" alt="Fintley appraisal with a value range, cap rate, rent, cash flow, and map" width="720" height="1565" decoding="async"></figure>
          <figure><figcaption>Deal Lab</figcaption><img src="assets/screens/fintley-deal-lab-dark.webp" alt="Fintley Deal Lab with adjustable assumptions and monthly cash flow" width="720" height="1565" decoding="async"></figure>
          <figure><figcaption>Markets</figcaption><img src="assets/screens/fintley-markets-dark.webp" alt="Fintley markets screen ranking US property markets" width="720" height="1565" decoding="async"></figure>
        </div>

        <div class="case" style="border-top:0;padding-bottom:0">
          <div class="case-copy" data-reveal>
            <h3>What it does</h3>
            <p class="lead" style="font-size:1rem">Type an address. Fintley returns an estimated value and range, projected rent, cap rate, monthly cash flow, and a Forecast score from 1 to 100, with a short plain-language read on the deal. Deal Lab lets you change the assumptions and watch the numbers move. Watchlist keeps the properties you are tracking in one place, with the numbers that matter beside each one.</p>
            <dl class="facts">
              <div><dt>Platform</dt><dd>iPhone</dd></div>
              <div><dt>Built with</dt><dd>SwiftUI</dd></div>
              <div><dt>Website</dt><dd><a href="https://fintley.app" rel="noopener">fintley.app</a></dd></div>
            </dl>
            <div class="actions">
              <a class="btn btn-ghost" href="https://fintley.app" rel="noopener">Visit fintley.app {EXT}</a>
            </div>
          </div>
          <div class="case-media" data-reveal style="--delay:120ms">
            <div class="screens screens-2" aria-label="More Fintley screens">
              <figure><figcaption>Watchlist</figcaption><img src="assets/screens/fintley-watchlist-dark.webp" alt="Fintley watchlist with tracked value, projected cash flow, and saved properties" width="720" height="1565" decoding="async" loading="lazy"></figure>
              <figure><figcaption>Forecast</figcaption><img src="assets/screens/fintley-report-dark.webp" alt="Fintley report with a Forecast score gauge" width="460" height="1000" decoding="async" loading="lazy"></figure>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="plants-in-pocket" aria-labelledby="plants-title" style="border-top:1px solid var(--line)">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">02 / Plants in Pocket / iPhone</p>
            <h2 id="plants-title">Identify a plant, then keep it alive.</h2>
          </div>
          <p data-reveal style="--delay:100ms">A native iPhone app for people who keep plants. Identify what you have, check its health, and follow a care plan written for that plant.</p>
        </div>

        <div class="case" style="border-top:0;padding-top:0">
          <div class="case-media" data-reveal>
            <div class="plants-panel">
              <img src="assets/work/plants-primary-logo.webp" alt="Plants in Pocket logo: a potted plant beside the name" width="430" height="243" decoding="async">
              <div class="plants-steps" aria-hidden="true"><span>Identify</span><span>Check health</span><span>Care plan</span></div>
            </div>
          </div>
          <div class="case-copy" data-reveal style="--delay:120ms">
            <h3>What it does</h3>
            <p class="lead" style="font-size:1rem">Most plant apps stop at the name. Plants in Pocket goes on to the part that matters: is this plant healthy, and what should I do this week? The result is a short, practical plan rather than a wall of botany.</p>
            <dl class="facts">
              <div><dt>Platform</dt><dd>iPhone</dd></div>
              <div><dt>Category</dt><dd>Plant care</dd></div>
              <div><dt>Status</dt><dd>Launching 2026</dd></div>
            </dl>
            <div class="actions">
              <a class="btn btn-ghost" href="https://www.tiktok.com/@plantsinpocket" rel="noopener">Follow @plantsinpocket {EXT}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

{cta("Have something you need built?", WORK_CTA_SUB)}
"""

# ---------------------------------------------------------------- SERVICES

FAQ = [
    ("What does a project cost?",
     "It depends on the scope, which is why we write the scope down first. You will have a number before any work starts, and it does not move unless the scope does."),
    ("How long does an iPhone app take?",
     "A focused first version usually takes a few months from kickoff to App Store submission. Larger products take longer. After the first conversation we can tell you roughly where yours lands."),
    ("Who owns the code?",
     "You do. The source code, the App Store listing, and the accounts the software runs on are set up in your name from the start."),
    ("Do you work with companies outside Tampa?",
     "Yes. We are based in Tampa, Florida and work with clients across the country. Most of the collaboration happens over email, calls, and shared builds, and we are happy to meet in person when we are nearby."),
    ("What happens after launch?",
     "Software needs looking after. We can stay on for updates, new features, and the yearly round of operating system changes, or hand everything over cleanly to your own team. Either way the code is documented and yours."),
    ("Can you take over an existing app or tool?",
     "Often, yes. Send us what you have and we will tell you plainly whether it makes sense to continue with it or start again."),
]


def faq_html():
    out = ['<div class="faq" data-reveal>']
    for q, a in FAQ:
        out.append(f"<details><summary>{q}</summary><p>{a}</p></details>")
    out.append("</div>")
    return "".join(out)


SERVICES_PAGE = f"""
    <section class="page-intro">
      <div class="wrap page-intro-grid">
        <div data-reveal>
          <p class="label">Services</p>
          <h1>What we build, and how.</h1>
        </div>
        <p data-reveal style="--delay:100ms">We work directly with owners and teams to fit software to the way a company already runs. Four kinds of work, all done in-house.</p>
      </div>
    </section>

    <section class="section-tight" aria-label="Services">
      <div class="wrap">
        {service_rows(long=True)}
      </div>
    </section>

    <section class="section" aria-labelledby="process-title" style="border-top:1px solid var(--line)">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">Process</p>
            <h2 id="process-title">Three stages, each with something to show for it.</h2>
          </div>
          <p data-reveal style="--delay:100ms">You should never wonder what is happening with your project. Every stage ends with something you can hold, read, or install.</p>
        </div>
        {PROCESS}
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="working-title" style="border-top:1px solid var(--line)">
      <div class="wrap statement">
        <div data-reveal>
          <p class="label" id="working-title">Working with us</p>
          <p class="display" style="margin-top:22px">Fitted to your business and built inside it, with the people who do the work in the room.</p>
        </div>
        <div class="statement-aside" data-reveal style="--delay:120ms">
          <p>We start by understanding the day-to-day operation, then design and integrate software around it. That means talking to the people who will use the thing, not only the people paying for it.</p>
          <p>Communication is direct. You have a person to email rather than a ticket queue, and you hear from us with working software, not status reports.</p>
          <div class="stack" aria-label="Where we work">
            <div><span>Mobile</span><span>Swift, SwiftUI</span></div>
            <div><span>Desktop</span><span>Windows, macOS</span></div>
            <div><span>Web</span><span>Browser apps, APIs</span></div>
            <div><span>Integration</span><span>AI, automation, data</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title" style="border-top:1px solid var(--line)">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">Questions</p>
            <h2 id="faq-title">Things people usually ask first.</h2>
          </div>
        </div>
        {faq_html()}
      </div>
    </section>

{cta("What needs to work better?", "Tell us what your team or your customers are trying to do. A few sentences is enough, and we reply within one business day.")}
"""

# ---------------------------------------------------------------- CONTACT

CONTACT = f"""
    <section class="page-intro">
      <div class="wrap page-intro-grid">
        <div data-reveal>
          <p class="label">Contact</p>
          <h1>Tell us what needs to work better.</h1>
        </div>
        <p data-reveal style="--delay:100ms">A few sentences about the problem, the people involved, and what you would like to change is enough to start. No brief or deck required.</p>
      </div>
    </section>

    <section class="section-tight" aria-label="Ways to reach Fintlock">
      <div class="wrap contact-grid">
        <div class="contact-direct" data-reveal>
          <p class="label">Direct email</p>
          <a class="contact-email" href="mailto:{EMAIL}?subject=Project%20inquiry">{EMAIL}</a>
          <p>We reply within one business day, from Tampa, Florida.</p>
          <ul class="contact-notes" aria-label="What helps us reply well">
            <li><span>01</span><div><strong>What happens today</strong><small>The current process, even if it is a spreadsheet and a group chat.</small></div></li>
            <li><span>02</span><div><strong>Who is involved</strong><small>The people who do the work and the people who depend on it.</small></div></li>
            <li><span>03</span><div><strong>What you want to change</strong><small>The outcome you are after, in your own words.</small></div></li>
          </ul>
        </div>

        <form class="form" data-contact-form data-reveal style="--delay:120ms" action="mailto:{EMAIL}" method="post" enctype="text/plain">
          <div class="form-row">
            <div class="field">
              <label for="f-name">Name</label>
              <input id="f-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="f-email">Email</label>
              <input id="f-email" name="email" type="email" autocomplete="email" required>
            </div>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="f-company">Company <small>optional</small></label>
              <input id="f-company" name="company" type="text" autocomplete="organization">
            </div>
            <div class="field">
              <label for="f-kind">Project type</label>
              <select id="f-kind" name="kind">
                <option value="">Not sure yet</option>
                <option>iPhone app</option>
                <option>Desktop or internal software</option>
                <option>Web product or integration</option>
                <option>AI or automation</option>
                <option>Something else</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="f-message">What needs to work better?</label>
            <textarea id="f-message" name="message" required placeholder="What happens today, who is involved, and what you would like to change."></textarea>
          </div>
          <p class="honeypot" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
          <div class="form-foot">
            <button class="btn btn-primary" type="submit">Send the note {ARROW}</button>
            <small>This opens a prepared message in your own email app. Nothing is sent or stored by this website.</small>
          </div>
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>
"""

# ---------------------------------------------------------------- PRIVACY

PRIVACY = f"""
    <section class="page-intro">
      <div class="wrap page-intro-grid">
        <div data-reveal>
          <p class="label">Privacy</p>
          <h1>Plain terms, minimal collection.</h1>
        </div>
        <p data-reveal style="--delay:100ms">This notice covers fintlock.com. Individual Fintlock products may publish their own privacy information for the data those products require.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="wrap prose-layout">
        <aside class="prose-aside" data-reveal>
          <div><span>Last updated</span><strong>September 2026</strong></div>
          <div><span>Questions</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        </aside>
        <div class="prose" data-reveal style="--delay:100ms">
          <article>
            <h2>Website data</h2>
            <p>Fintlock collects only what is needed for the website and its products to work. Fintlock does not sell personal data and does not build products around advertising networks.</p>
            <p>This website loads its typefaces from Google Fonts. When a page loads, your browser requests those font files from Google, which may record your IP address as part of serving the request. No other third-party scripts or trackers run on this site.</p>
          </article>
          <article>
            <h2>Contact form</h2>
            <p>The contact form prepares an email in your own email application. The website does not send or store what you enter. You choose whether to send the completed email to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
          </article>
          <article>
            <h2>External websites</h2>
            <p>This website links to other websites, including individual Fintlock product sites and social profiles. Those websites apply their own privacy practices when you visit them.</p>
          </article>
          <article>
            <h2>Questions</h2>
            <p>Questions about this notice or about a Fintlock product can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
          </article>
        </div>
      </div>
    </section>
"""

NOT_FOUND = f"""
    <section class="page-intro">
      <div class="wrap page-intro-grid">
        <div>
          <p class="label">404</p>
          <h1>That page is not here.</h1>
        </div>
        <p>The address may have changed, or the link was typed by hand. Everything on the site is one click away.</p>
      </div>
    </section>
    <section class="section-tight">
      <div class="wrap">
        <nav class="product-index" aria-label="Site pages">
          <a href="index.html"><span class="num">01</span><span><strong>Home</strong><small>iPhone apps and business software</small></span>{ARROW}</a>
          <a href="work.html"><span class="num">02</span><span><strong>Work</strong><small>Fintley and Plants in Pocket</small></span>{ARROW}</a>
          <a href="services.html"><span class="num">03</span><span><strong>Services</strong><small>What we build, and how</small></span>{ARROW}</a>
          <a href="contact.html"><span class="num">04</span><span><strong>Contact</strong><small>Start a project</small></span>{ARROW}</a>
        </nav>
      </div>
    </section>
"""

PAGES = {
    "index.html": ("Custom Software and iPhone App Development, Tampa | Fintlock", "Fintlock is a software studio in Tampa, Florida. We design and build native iPhone apps, desktop tools, and web software for businesses with specific needs.", HOME, "iPhone apps and business software, made to fit. A software studio in Tampa, Florida."),
    "work.html": ("Our Work: Fintley and Plants in Pocket | Fintlock", "Two iPhone apps designed and built by Fintlock: Fintley, a real estate appraisal app, and Plants in Pocket, a plant identification and care app.", WORK, None),
    "services.html": ("iPhone App, Desktop and Web Software Development | Fintlock", "iPhone apps, desktop and internal software, web products and integrations, and practical AI and automation help, with a written scope and price before work starts.", SERVICES_PAGE, None),
    "contact.html": ("Start a Software Project | Fintlock", "Tell Fintlock what needs to work better. A few sentences is enough to start, and we reply within one business day.", CONTACT, None),
    "404.html": ("Page Not Found | Fintlock", "That page is not on fintlock.com.", NOT_FOUND, None),
    "privacy.html": ("Privacy Notice | Fintlock", "What fintlock.com collects, what it does not, and how the contact form works. Plain terms, minimal collection.", PRIVACY, None),
}

JSONLD = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {"@type":"Organization","@id":"https://fintlock.com/#org","name":"Fintlock","legalName":"Fintlock LLC","url":"https://fintlock.com/","logo":"https://fintlock.com/assets/brand/fintlock-social-card.png","email":"contact@fintlock.com","description":"A software studio in Tampa, Florida that designs and builds native iPhone apps, desktop tools, and web software for businesses.","address":{"@type":"PostalAddress","addressLocality":"Tampa","addressRegion":"FL","addressCountry":"US"},"areaServed":"US","knowsAbout":["iPhone app development","SwiftUI","custom business software","web application development","system integration","automation"]},
    {"@type":"WebSite","@id":"https://fintlock.com/#site","url":"https://fintlock.com/","name":"Fintlock","publisher":{"@id":"https://fintlock.com/#org"}}
  ]}
  </script>
"""

WORK_JSONLD = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {"@type":"SoftwareApplication","name":"Fintley","url":"https://fintley.app","applicationCategory":"FinanceApplication","operatingSystem":"iOS","description":"Real estate appraisal for iPhone. Type an address and get an estimated value, rent, cash flow, comparable sales, and a Forecast score.","author":{"@id":"https://fintlock.com/#org"}},
    {"@type":"SoftwareApplication","name":"Plants in Pocket","applicationCategory":"LifestyleApplication","operatingSystem":"iOS","description":"Plant identification, health checks, and care plans for iPhone.","author":{"@id":"https://fintlock.com/#org"},"sameAs":["https://www.tiktok.com/@plantsinpocket"]}
  ]}
  </script>
"""

for path, (title, desc, body, og) in PAGES.items():
    html = head(title, desc, path, og)
    if path == "index.html":
        html = html.replace("</head>", JSONLD + "</head>")
    if path == "work.html":
        html = html.replace("</head>", WORK_JSONLD + "</head>")
    html += header(path) + body + footer(path)
    (ROOT / path).write_text(html, encoding="utf-8")
    print("wrote", path, len(html))

nf = ROOT / "404.html"
nf.write_text(nf.read_text().replace('<link rel="canonical" href="https://fintlock.com/404.html">', '<meta name="robots" content="noindex">').replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('href="styles.css', 'href="/styles.css').replace('src="app.js', 'src="/app.js').replace('href="index.html"', 'href="/"').replace('href="work.html"', 'href="/work.html"').replace('href="services.html"', 'href="/services.html"').replace('href="contact.html"', 'href="/contact.html"').replace('href="privacy.html"', 'href="/privacy.html"'), encoding="utf-8")

sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path in PAGES:
    if path == "404.html":
        continue
    loc = SITE + "/" + (path if path != "index.html" else "")
    sitemap.append(f"  <url><loc>{loc}</loc><lastmod>2026-09-02</lastmod></url>")
sitemap.append("</urlset>\n")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")
print("wrote sitemap.xml")
