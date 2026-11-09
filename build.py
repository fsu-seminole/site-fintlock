#!/usr/bin/env python3
"""Assembles the five Fintlock pages from shared chrome + per-page bodies.
Run: python3 build.py  (writes *.html next to this file)."""

import pathlib
import re
from service_pages import PAGES as SERVICE_PAGES

ROOT = pathlib.Path(__file__).parent
SITE = "https://fintlock.com"
EMAIL = "contact@fintlock.com"
PLANTS_APP_STORE = "https://apps.apple.com/us/app/plants-in-pocket-plant-id/id6790838495"
CSS_V = "6"
JS_V = "6"

ARROW = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EXT = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6 3h7v7M13 3 5 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

NAV = [("services.html", "Services"), ("work.html", "Work"), ("index.html#faq", "FAQ"), ("custom-tv-home-screen.html", "TV SmartHub")]
FONTS = "https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap"
GO = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8"/></svg>'
MARK = '<svg viewBox="0 0 134 186" width="15" height="21" aria-hidden="true"><g transform="translate(-399.3,174.5)" fill="#101d35"><path d="M 440.3 -85 L 440.3 -130 A 26 26 0 0 1 492.3 -130 L 492.3 -85" fill="none" stroke="#101d35" stroke-width="21"/><path d="M 407.3 -55.8 a 59 59 0 1 0 118 0 a 59 59 0 1 0 -118 0 Z M 440.3 -55.8 a 26 26 0 1 0 52 0 a 26 26 0 1 0 -52 0 Z" fill-rule="evenodd"/></g></svg>'


def _inputs_hash():
    import hashlib
    h = hashlib.sha1()
    for name in ["build.py", "service_pages.py", "site.css", "site.js", "_src/home.html", "_src/tv.html"]:
        h.update((ROOT / name).read_bytes())
    return h.hexdigest()[:7]


import datetime as _dt
BUILD_DATE = _dt.date.today()
VERSION = f"{BUILD_DATE:%Y.%m.%d}-{_inputs_hash()}"


def head(title, description, path, og_description=None, preload=None):
    url = SITE + "/" + (path if path != "index.html" else "")
    og = og_description or description
    pre = f'\n  <link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#eef1f7">
  <meta name="fintlock-version" content="{VERSION}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Fintlock">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og}">
  <meta property="og:image" content="{SITE}/assets/brand/fintlock-social-card.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{og}">
  <meta name="twitter:image" content="{SITE}/assets/brand/fintlock-social-card.png">
  <link rel="icon" type="image/svg+xml" href="assets/brand/fintlock-favicon.svg">{pre}
  <script>try{{if(localStorage.getItem("fl-skin")==="navy")document.documentElement.classList.add("skin-navy")}}catch(e){{}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONTS}">
  <link rel="stylesheet" href="site.css?v={CSS_V}">
  <script src="site.js?v={JS_V}" defer></script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
"""


def header(current):
    def href(h):
        return "#faq" if (current == "index.html" and h == "index.html#faq") else h
    links, sheet = [], []
    for h, label in NAV:
        cur = ' aria-current="page"' if h == current else ""
        tv = "tv" in h
        links.append(f'<a href="{href(h)}"{cur}{" class=tvlink" if tv else ""}>{label}{"<i aria-hidden=true></i>" if tv else ""}</a>')
        sheet.append(f'<a href="{href(h)}"{cur}>{label}{"<small class=new>New</small>" if tv else ""}</a>')
    return f"""
  <div class="alt">
  <div class="navpill" id="navpill">
    <a class="logo" href="index.html" aria-label="Fintlock home">{MARK}</a>
    <nav aria-label="Main">{"".join(links)}</nav>
    <button class="icon-btn skin-btn" type="button" aria-label="Switch color theme" title="Switch between light and navy">
      <svg class="sun" viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="3.5" stroke="currentColor" stroke-width="1.6"/><path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.3 4.3l1.4 1.4M14.3 14.3l1.4 1.4M4.3 15.7l1.4-1.4M14.3 5.7l1.4-1.4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
      <svg class="moon" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M16.5 12.2A7 7 0 1 1 7.8 3.5a5.5 5.5 0 0 0 8.7 8.7z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
    </button>
    <a class="go" href="contact.html">Start a project</a>
    <button class="icon-btn menu-btn" type="button" aria-label="Open menu" aria-controls="sheet" aria-expanded="false" id="menu-open"><svg viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M2 5h14M2 9h14M2 13h14" stroke="currentColor" stroke-width="1.6"/></svg></button>
  </div>
  <div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="sheet-top">
      <img class="wm-light" src="assets/brand/fintlock-wordmark-on-light.svg" alt="Fintlock" width="118" height="30"><img class="wm-dark" src="assets/brand/fintlock-wordmark-on-dark.svg" alt="Fintlock" width="118" height="30">
      <button class="close" type="button" aria-label="Close menu" id="menu-close"><svg viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M4 4l10 10M14 4 4 14" stroke="currentColor" stroke-width="1.6"/></svg></button>
    </div>
    <nav aria-label="Mobile"><a href="index.html"{' aria-current="page"' if current == "index.html" else ""}>Home</a>{"".join(sheet)}<a href="contact.html">Contact</a></nav>
    <a class="pbtn" href="contact.html">Start a project {GO}</a>
  </div>

  <main id="main">
"""


def footer(current):
    studio = [("index.html", "Home"), ("work.html", "Work"), ("services.html", "Services"), ("contact.html", "Contact"), ("privacy.html", "Privacy")]
    svc = [(p["slug"], p["short"]) for p in SERVICE_PAGES] + [("custom-tv-home-screen.html", "TV SmartHub")]
    def links(items):
        return "".join(f'<a href="{h}"{" aria-current=page" if h == current else ""}>{l}</a>' for h, l in items)
    return f"""
  </main>

  <footer class="inner site-foot">
    <div class="fgrid">
      <div>
        <a href="index.html" aria-label="Fintlock home"><img class="wm-light" src="assets/brand/fintlock-wordmark-on-light.svg" alt="Fintlock" width="118" height="30" loading="lazy"><img class="wm-dark" src="assets/brand/fintlock-wordmark-on-dark.svg" alt="Fintlock" width="118" height="30" loading="lazy"></a>
        <p class="blurb">An independent software studio in Tampa, Florida. iPhone apps, web software, business tools, and custom TV home screens.</p>
      </div>
      <nav aria-label="Studio"><p class="fh">Studio</p>{links(studio)}</nav>
      <nav aria-label="Services"><p class="fh">Services</p>{links(svc)}</nav>
      <div class="fcol"><p class="fh">Get in touch</p><a href="mailto:{EMAIL}">{EMAIL}</a><span class="muted">Tampa, Florida</span><a href="{PLANTS_APP_STORE}" rel="noopener">Plants in Pocket ↗</a></div>
    </div>
    <div class="fbottom">
      <span>&copy; <span data-year>{BUILD_DATE.year}</span> Fintlock LLC. Designed and built in Tampa.</span>
      <span class="stamp" title="Published {BUILD_DATE:%B %-d, %Y}">v{VERSION}</span>
    </div>
  </footer>
  </div>
</body>
</html>
"""


def cta(heading="What could work <span class=\"u\">better?</span>", sub="The process that eats your afternoons. The app you wish existed. The TV screen your kids keep landing on. Tell us about it. We reply within one business day.", href="contact.html", label="Start a project"):
    return f"""
  <section class="sec inner" id="contact" aria-labelledby="cta-title">
    <div class="cta">
      <h2 id="cta-title">{heading}</h2>
      <p>{sub}</p>
      <a class="pbtn" href="{href}">{label} {GO}</a>
      <a class="cta-mail" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </section>
"""


def modernize(html):
    """Legacy button classes -> soft pill buttons; page intros sit in the rounded frame."""
    html = re.sub(r'class="btn btn-primary[^"]*"', 'class="pbtn"', html)
    html = re.sub(r'class="btn btn-ghost[^"]*"', 'class="gbtn"', html)
    html = html.replace('<section class="page-intro">', '<section class="frame page-intro">')
    return html


SERVICE_LINKS = ["iphone-app-development.html", "custom-business-software.html", "web-app-development.html", "custom-app-development.html", "custom-tv-home-screen.html"]

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
    ("05", "Custom TV home screens", "TV SmartHub",
     "A home screen for your smart TV designed around your household: your apps in your order, your teams' scores, a message for the day, and no ads or autoplaying promos.",
     "We design the screen with you, install it on every TV in the house, and push updates for new apps, teams, and holidays. Installs are done in person in the Tampa Bay area.",
     ["Smart TV", "Families", "Live scores", "Holiday themes"]),
]


def service_rows(long=False):
    out = ['<div class="service-list">']
    for i, (num, name, sub, desc, detail, tags) in enumerate(SERVICES):
        tag_html = "".join(f"<li>{t}</li>" for t in tags)
        more = f'<p class="service-detail">{detail}</p>' if long else ""
        link = SERVICE_LINKS[i]
        link_label = ["iPhone app development", "custom business software", "web app development", "custom app development", "TV SmartHub"][i]
        link_html = f'<a class="text-link" href="{link}" style="margin-top:18px">About {link_label} {ARROW}</a>' if long else ""
        out.append(f"""
        <article class="service-row" data-reveal style="--delay:{i * 60}ms">
          <span class="service-num">{num}</span>
          <h3>{name}<small>{sub}</small></h3>
          <div>
            <p>{desc}</p>{more}{link_html}
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


# ---------------------------------------------------------------- HOME + TV (bodies live in _src/, which Jekyll does not publish)

HOME = (ROOT / "_src" / "home.html").read_text(encoding="utf-8")
TV = (ROOT / "_src" / "tv.html").read_text(encoding="utf-8") + cta("Want a home screen built for <span class=\"u\">your family?</span>", "Tell us which apps you use, which teams you follow, and who's watching. We'll design it, install it, and keep it current.", "contact.html?type=tv", "Ask about TV SmartHub")

# ---------------------------------------------------------------- WORK

WORK_CTA_SUB = 'Every project gets the same treatment: a written scope, working builds to review, and a proper handover. Tell us what you need. We reply within one business day.'

WORK = f"""
    <section class="page-intro">
      <div class="wrap">
        <div class="page-intro-grid">
          <div>
            <p class="label">Work</p>
            <h1>Products and client work, start to finish.</h1>
          </div>
          <p>Our flagship iPhone app, a custom TV home screen for a client, and an app in development, all designed and built in-house. They are the best public record of how we work.</p>
        </div>
        <nav class="product-index" aria-label="Products on this page">
          <a href="#plants-in-pocket"><span class="num">01</span><span><strong>Plants in Pocket</strong><small>Our flagship iPhone app</small></span>{ARROW}</a>
          <a href="#fintley"><span class="num">02</span><span><strong>Fintley</strong><small>Real estate appraisal for iPhone</small></span>{ARROW}</a>
          <a href="#tv-smarthub"><span class="num">03</span><span><strong>Custom TV Home Screen</strong><small>A client's smart TV home screen</small></span>{ARROW}</a>
        </nav>
      </div>
    </section>

    <section class="section" id="plants-in-pocket" aria-labelledby="plants-title">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">01 / Flagship / Plants in Pocket / iPhone</p>
            <h2 id="plants-title">Identify a plant, then keep it alive.</h2>
            <div class="live-app" data-app-store="6790838495" hidden></div>
          </div>
          <p data-reveal style="--delay:100ms">A native iPhone app for people who keep plants. Identify what you have, check its health, and follow a care plan written for that plant.</p>
        </div>

        <div class="case" style="border-top:0;padding-top:0">
          <div class="case-media" data-reveal>
            <div class="plants-panel">
              <img src="assets/work/plants-mark.webp" alt="Plants in Pocket illustrated potted plant" width="640" height="640" decoding="async">
              <div class="plants-steps" aria-hidden="true"><span>Identify</span><span>Check health</span><span>Care plan</span></div>
            </div>
          </div>
          <div class="case-copy" data-reveal style="--delay:120ms">
            <h3>What it does</h3>
            <p class="lead" style="font-size:1rem">Most plant apps stop at the name. Plants in Pocket goes on to the part that matters: is this plant healthy, and what should I do this week? The result is a short, practical plan rather than a wall of botany.</p>
            <dl class="facts">
              <div><dt>Platform</dt><dd>iPhone</dd></div>
              <div><dt>Category</dt><dd>Plant care</dd></div>
              <div><dt>Price</dt><dd>Free</dd></div>
              <div><dt>Status</dt><dd>Live on the App Store</dd></div>
            </dl>
            <div class="actions">
              <a class="btn btn-primary" href="{PLANTS_APP_STORE}" rel="noopener">View on the App Store {EXT}</a>
              <a class="btn btn-ghost" href="https://www.tiktok.com/@plantsinpocket" rel="noopener">Follow @plantsinpocket {EXT}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="fintley" style="border-top:1px solid var(--line)" aria-labelledby="fintley-title">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">02 / Fintley / iPhone / In development</p>
            <h2 id="fintley-title">Any address, appraised in seconds.</h2>
          </div>
          <p data-reveal style="--delay:100ms">Fintley turns an address into a structured investment report. Value, rent, comparable sales, cash flow, and market context, in one native iPhone app.</p>
        </div>

        <div class="screens screens-4" data-reveal aria-label="Fintley screens">
          <figure><figcaption>Home</figcaption><img src="assets/screens/fintley-home-dark.webp" srcset="assets/screens/fintley-home-dark-480.webp 480w, assets/screens/fintley-home-dark.webp 720w" sizes="(max-width: 640px) 62vw, 30vw" alt="Fintley home screen with a search field, recent reports, and featured markets" width="720" height="1565" decoding="async"></figure>
          <figure><figcaption>Appraisal</figcaption><img src="assets/screens/fintley-forecast-dark.webp" srcset="assets/screens/fintley-forecast-dark-480.webp 480w, assets/screens/fintley-forecast-dark.webp 720w" sizes="(max-width: 640px) 62vw, 30vw" alt="Fintley appraisal with a value range, cap rate, rent, cash flow, and map" width="720" height="1565" decoding="async"></figure>
          <figure><figcaption>Deal Lab</figcaption><img src="assets/screens/fintley-deal-lab-dark.webp" srcset="assets/screens/fintley-deal-lab-dark-480.webp 480w, assets/screens/fintley-deal-lab-dark.webp 720w" sizes="(max-width: 640px) 62vw, 30vw" alt="Fintley Deal Lab with adjustable assumptions and monthly cash flow" width="720" height="1565" decoding="async"></figure>
          <figure><figcaption>Markets</figcaption><img src="assets/screens/fintley-markets-dark.webp" srcset="assets/screens/fintley-markets-dark-480.webp 480w, assets/screens/fintley-markets-dark.webp 720w" sizes="(max-width: 640px) 62vw, 30vw" alt="Fintley markets screen ranking US property markets" width="720" height="1565" decoding="async"></figure>
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
              <figure><figcaption>Watchlist</figcaption><img src="assets/screens/fintley-watchlist-dark.webp" srcset="assets/screens/fintley-watchlist-dark-480.webp 480w, assets/screens/fintley-watchlist-dark.webp 720w" sizes="(max-width: 640px) 62vw, 30vw" alt="Fintley watchlist with tracked value, projected cash flow, and saved properties" width="720" height="1565" decoding="async" loading="lazy"></figure>
              <figure><figcaption>Forecast</figcaption><img src="assets/screens/fintley-report-dark.webp" srcset="assets/screens/fintley-report-dark-320.webp 320w, assets/screens/fintley-report-dark.webp 460w" sizes="(max-width: 640px) 62vw, 25vw" alt="Fintley report with a Forecast score gauge" width="460" height="1000" decoding="async" loading="lazy"></figure>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="tv-smarthub" aria-labelledby="tv-work-title" style="border-top:1px solid var(--line)">
      <div class="wrap">
        <div class="section-head">
          <div data-reveal>
            <p class="label">03 / Custom TV Home Screen / Smart TV</p>
            <h2 id="tv-work-title">A home screen built for one family.</h2>
          </div>
          <p data-reveal style="--delay:100ms">A custom home screen for a client's smart TVs, tailored to their interests and app usage.</p>
        </div>
        <div class="case" style="border-top:0;padding-top:0">
          <div class="case-media" data-reveal>
            <div class="tv-bezel"><img src="assets/tv/tv-thanksgiving.webp" alt="Custom smart TV home screen with a Thanksgiving theme, app tiles, and a Game Day scores panel" width="1600" height="900" loading="lazy" decoding="async"></div>
          </div>
          <div class="case-copy" data-reveal style="--delay:120ms">
            <h3>What it does</h3>
            <p class="lead" style="font-size:1rem">Big tiles for the family's streaming apps in their order, live scores and next games for their teams, a verse that changes each time the screen opens, and themes that switch on their own for each holiday. No ads, no autoplaying trailers.</p>
            <dl class="facts">
              <div><dt>Platform</dt><dd>Smart TV</dd></div>
              <div><dt>Category</dt><dd>Client work</dd></div>
              <div><dt>Status</dt><dd>In daily use</dd></div>
            </dl>
            <div class="actions">
              <a class="btn btn-primary" href="custom-tv-home-screen.html">Explore TV SmartHub {ARROW}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

{cta("Have something you need <span class=\"u\">built?</span>", WORK_CTA_SUB)}
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


def faq_item(i, q, a):
    return f'<details{" open" if i == 1 else ""}><summary>{q} <i aria-hidden="true"></i></summary><p>{a}</p></details>'


def faq_html():
    out = ['<div class="faq">']
    for i, (q, a) in enumerate(FAQ, 1):
        out.append(faq_item(i, q, a))
    out.append("</div>")
    return "".join(out)


SERVICES_PAGE = f"""
    <section class="page-intro">
      <div class="wrap page-intro-grid">
        <div>
          <p class="label">Services</p>
          <h1>What we build, and how.</h1>
        </div>
        <p>We work directly with owners and teams to fit software to the way a company already runs. Five kinds of work, all done in-house.</p>
      </div>
    </section>

    <section class="section-tight" aria-label="Services">
      <div class="wrap">
        {service_rows(long=True)}
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

    <section class="section band-light" aria-labelledby="faq-title">
      <div class="wrap faq-grid">
        <div class="stack">
          <p class="label on-light">Questions</p>
          <h2 class="h-lg" id="faq-title">Things people usually ask first.</h2>
        </div>
        {faq_html()}
      </div>
    </section>

{cta()}
"""

# ---------------------------------------------------------------- CONTACT

CONTACT = f"""
    <section class="page-intro">
      <div class="wrap page-intro-grid">
        <div>
          <p class="label">Contact</p>
          <h1>Tell us what needs to work better.</h1>
        </div>
        <p>A few sentences about the problem, the people involved, and what you would like to change is enough to start. No brief or deck required.</p>
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

        <form class="form" data-contact-form action="https://formsubmit.co/{EMAIL}" method="POST">
          <input type="hidden" name="_subject" value="New project inquiry from fintlock.com">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_next" value="{SITE}/contact.html?sent=1">
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
                <option value="TV SmartHub">TV SmartHub (custom TV home screen)</option>
                <option>Something else</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="f-message">What needs to work better?</label>
            <textarea id="f-message" name="message" required placeholder="What happens today, who is involved, and what you would like to change."></textarea>
          </div>
          <p class="honeypot" aria-hidden="true"><label>Leave this empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></p>
          <div class="form-foot">
            <button class="btn btn-primary" type="submit">Send the note {ARROW}</button>
            <small>Your note goes straight to our inbox. We reply within one business day.</small>
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
        <div>
          <p class="label">Privacy</p>
          <h1>Plain terms, minimal collection.</h1>
        </div>
        <p>This notice covers fintlock.com. Individual Fintlock products may publish their own privacy information for the data those products require.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="wrap prose-layout">
        <aside class="prose-aside" data-reveal>
          <div><span>Last updated</span><strong>November 2026</strong></div>
          <div><span>Questions</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        </aside>
        <div class="prose" data-reveal style="--delay:100ms">
          <article>
            <h2>Website data</h2>
            <p>Fintlock collects only what is needed for the website and its products to work. Fintlock does not sell personal data and does not build products around advertising networks.</p>
            <p>This website loads its typefaces from Google Fonts. When a page loads, your browser requests those font files from Google, which may record your IP address as part of serving the request. No analytics or advertising trackers run on this site.</p>
          </article>
          <article>
            <h2>Contact form</h2>
            <p>When you use the contact form, what you enter (your name, email, company, project type, and message) is delivered to <a href="mailto:{EMAIL}">{EMAIL}</a> by FormSubmit (formsubmit.co), a form delivery service. We use it only to reply to you and do not add you to any mailing list. If you prefer, you can email us directly instead.</p>
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
    <section class="frame page-intro">
      <div class="wrap page-intro-grid">
        <div>
          <p class="label">404</p>
          <h1>This page is <em>locked out.</em></h1>
        </div>
        <p>The address may have changed, or the link was typed by hand. Pick the lock below for fun, or head straight to a real page.</p>
      </div>
    </section>
    <section class="section-tight">
      <div class="wrap game" data-lock-game>
        <div class="game-copy">
          <p class="label">Pick the lock</p>
          <h2>Three pins. One tap each.</h2>
          <p>Tap the lock, press the space bar, or click when the white pin is inside the yellow zone. Set all three to open it. Miss and that pin resets.</p>
          <nav class="product-index" aria-label="Site pages" style="margin-top:12px">
            <a href="index.html"><span class="num">01</span><span><strong>Home</strong><small>Custom software studio in Tampa</small></span>{ARROW}</a>
            <a href="work.html"><span class="num">02</span><span><strong>Work</strong><small>Plants in Pocket and more</small></span>{ARROW}</a>
            <a href="custom-tv-home-screen.html"><span class="num">03</span><span><strong>TV SmartHub</strong><small>Custom TV home screens</small></span>{ARROW}</a>
            <a href="contact.html"><span class="num">04</span><span><strong>Contact</strong><small>Start a project</small></span>{ARROW}</a>
          </nav>
        </div>
        <div class="game-board" role="application" aria-label="Lock picking game. Press space or tap to set a pin." tabindex="0">
          <div class="lock" aria-hidden="true"><div class="shackle"></div><div class="body"></div></div>
          <div class="pins" aria-hidden="true">
            <div class="pin"><div class="zone"></div><div class="tick"></div></div>
            <div class="pin"><div class="zone"></div><div class="tick"></div></div>
            <div class="pin"><div class="zone"></div><div class="tick"></div></div>
          </div>
          <p class="game-status" aria-live="polite">Press space or tap to start.</p>
          <div class="game-meta"><span>Time <b data-time>0.0s</b></span><span>Best <b data-best>none</b></span></div>
          <button class="pbtn" type="button" data-reset hidden>Play again</button>
        </div>
      </div>
    </section>
"""

def service_page(p):
    def ul(items):
        return "".join(f"<li>{i}</li>" for i in items)
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["example"][3])
    faq = "".join(faq_item(i, q, a) for i, (q, a) in enumerate(p["faq"], 1))
    by_slug = {x["slug"]: x for x in SERVICE_PAGES}
    related = "".join(
        f'<a href="{s}"><span class="num">0{i+1}</span><span><strong>{by_slug[s]["label"]}</strong><small>{by_slug[s]["blurb"]}</small></span>{ARROW}</a>'
        for i, s in enumerate(p["related"]))
    ex_href, ex_text = p["example"][4]
    ex_external = ex_href.startswith("http")
    ex_rel = ' rel="noopener"' if ex_external else ""
    ex_icon = EXT if ex_external else ARROW
    return f"""
    <section class="page-intro">
      <div class="wrap page-intro-grid">
        <div>
          <p class="label">{p["label"]} / Tampa, Florida</p>
          <h1>{p["h1"]}</h1>
        </div>
        <p>{p["lead"]}</p>
      </div>
    </section>

    <section class="section-tight" style="border-top:1px solid var(--line)">
      <div class="wrap statement">
        <div data-reveal>
          <p class="label">The problem</p>
          <p class="display" style="margin-top:22px">{p["problem"][0]}</p>
        </div>
        <div class="statement-aside" data-reveal style="--delay:100ms">
          {"".join(f"<p>{x}</p>" for x in p["problem"][1])}
        </div>
      </div>
    </section>

    <section class="section-tight" style="border-top:1px solid var(--line)">
      <div class="wrap two-col">
        <div data-reveal>
          <p class="label">What we build</p>
          <h2 style="margin-top:20px;font-size:clamp(1.9rem,3vw,2.6rem)">{p["build"][0]}</h2>
          <p class="muted" style="margin-top:18px">{p["build"][1]}</p>
          <ul class="bullets">{ul(p["build"][2])}</ul>
        </div>
        <aside class="fit-panel" data-reveal style="--delay:100ms">
          <p class="label">{p["fit"][0]}</p>
          <ul class="bullets">{ul(p["fit"][1])}</ul>
          <a class="btn btn-primary" href="contact.html" style="margin-top:24px">Start a project {ARROW}</a>
        </aside>
      </div>
    </section>

    <section class="section" style="border-top:1px solid var(--line)">
      <div class="wrap case" style="border-top:0;padding-block:0">
        <div class="case-copy" data-reveal>
          <p class="label">{p["example"][0]}</p>
          <h2 style="font-size:clamp(2rem,3.6vw,3.2rem)">{p["example"][1]}</h2>
          {"".join(f'<p{" class=lead" if i == 0 else ""}>{x}</p>' for i, x in enumerate(p["example"][2]))}
          <dl class="facts">{facts}</dl>
          <div class="actions"><a class="text-link" href="{ex_href}"{ex_rel}>{ex_text} {ex_icon}</a></div>
        </div>
        <div class="case-media" data-reveal style="--delay:120ms">
          {example_media(p["slug"])}
        </div>
      </div>
    </section>


    <section class="section band-light">
      <div class="wrap faq-grid">
        <div class="stack">
          <p class="label on-light">Questions</p>
          <h2 class="h-lg">Things people ask about {p["topic"]}.</h2>
        </div>
        <div class="faq">{faq}</div>
      </div>
    </section>

    <section class="section-tight" style="border-top:1px solid var(--line)">
      <div class="wrap">
        <p class="label" data-reveal>Related services</p>
        <nav class="product-index product-index-3" aria-label="Related services" data-reveal style="--delay:80ms">{related}</nav>
      </div>
    </section>

{cta()}
"""


def example_media(slug):
    if slug in ("iphone-app-development.html", "web-app-development.html"):
        shots = [("fintley-home-dark", "Home", "Fintley home screen with a search field, recent reports, and featured markets"),
                 ("fintley-forecast-dark", "Appraisal", "Fintley appraisal with a value range, cap rate, rent, and cash flow"),
                 ("fintley-deal-lab-dark", "Deal Lab", "Fintley Deal Lab with adjustable assumptions and monthly cash flow")]
        if slug == "web-app-development.html":
            shots = [("fintley-markets-dark", "Markets", "Fintley markets screen ranking US property markets"),
                     ("fintley-watchlist-dark", "Watchlist", "Fintley watchlist with tracked value and saved properties"),
                     ("fintley-report-dark", "Forecast", "Fintley report with a Forecast score gauge")]
        figs = ""
        for n, cap, alt in shots:
            small, w, h = ("-480", 480, 1043) if n != "fintley-report-dark" else ("-320", 320, 696)
            full_w, full_h = (720, 1565) if n != "fintley-report-dark" else (460, 1000)
            figs += f'<figure><figcaption>{cap}</figcaption><img src="assets/screens/{n}.webp" srcset="assets/screens/{n}{small}.webp {w}w, assets/screens/{n}.webp {full_w}w" sizes="(max-width: 640px) 62vw, 30vw" alt="{alt}" width="{full_w}" height="{full_h}" loading="lazy" decoding="async"></figure>'
        return f'<div class="screens" aria-label="Fintley screens">{figs}</div>'
    if slug == "custom-app-development.html":
        return """<div class="plants-panel">
              <img src="assets/work/plants-mark.webp" alt="Plants in Pocket illustrated potted plant" width="640" height="640" loading="lazy" decoding="async">
              <div class="plants-steps" aria-hidden="true"><span>Identify</span><span>Check health</span><span>Care plan</span></div>
            </div>"""
    # custom-business-software: an abstract spec-check panel drawn in HTML, no invented screenshots
    rows = [("Requirement", "Product data", "Match"),
            ("R-value 19, unfaced", "R-19 unfaced batt, 15 in", "ok"),
            ("Fire rating: Class A", "Class A (ASTM E84)", "ok"),
            ("Width: 16 in on center", "15 in batt", "flag"),
            ("Thickness: 6.25 in", "6.25 in", "ok")]
    body = ""
    for i, (a, b, c) in enumerate(rows):
        if i == 0:
            body += f'<div class="spec-row spec-head"><span>{a}</span><span>{b}</span><span>{c}</span></div>'
        else:
            mark = '<i class="ok">Matches</i>' if c == "ok" else '<i class="flag">Check</i>'
            body += f'<div class="spec-row"><span>{a}</span><span>{b}</span><span>{mark}</span></div>'
    return f"""<div class="spec-panel" aria-label="Illustration of a specification check">
              <div class="spec-bar"><span>Spec check</span><span>Illustration, not client data</span></div>
              {body}
              <div class="spec-foot"><span>1 item to check</span><span>Export record</span></div>
            </div>"""


PAGES = {
    "index.html": ("Fintlock | Custom Software, iPhone Apps &amp; TV Home Screens in Tampa", "Fintlock is a Tampa software studio. We design and build native iPhone apps like Plants in Pocket, web apps, business tools, and custom smart TV home screens.", HOME, "A Tampa software studio building iPhone apps, web software, and custom smart TV home screens."),
    "custom-tv-home-screen.html": ("Custom Smart TV Home Screen | TV SmartHub by Fintlock, Tampa", "TV SmartHub replaces your smart TV's ad-filled home screen with one built for your family: your apps, your teams' live scores, a daily message, and holiday themes. Installed in Tampa Bay.", TV, "A smart TV home screen built for your family. Your apps, your teams, your traditions, and no ads."),
    "work.html": ("Our Work: Plants in Pocket, TV SmartHub and Fintley | Fintlock", "Plants in Pocket, our plant identification and care app for iPhone, a custom smart TV home screen for a client, and Fintley, a real estate appraisal app in development.", WORK, None),
    "services.html": ("iPhone App, Web, Business Software and TV Home Screen Development | Fintlock", "iPhone apps, desktop and internal software, web products and integrations, AI and automation, and custom TV home screens, with a written scope and price before work starts.", SERVICES_PAGE, None),
    "contact.html": ("Start a Software Project | Fintlock", "Tell Fintlock what needs to work better. A few sentences is enough to start, and we reply within one business day.", CONTACT, None),
    "404.html": ("Page Not Found | Fintlock", "That page is not on fintlock.com.", NOT_FOUND, None),
    **{p["slug"]: (p["title"], p["description"], service_page(p), None) for p in SERVICE_PAGES},
    "privacy.html": ("Privacy Notice | Fintlock", "What fintlock.com collects, what it does not, and how the contact form works. Plain terms, minimal collection.", PRIVACY, None),
}

import json as _json
import html as _html


def faq_from(body):
    items = re.findall(r'<summary>(.*?) <i aria-hidden="true"></i></summary><p>(.*?)</p>', body, flags=re.S)
    return [{"@type": "Question", "name": _html.unescape(re.sub("<[^>]+>", "", q)).strip(),
             "acceptedAnswer": {"@type": "Answer", "text": _html.unescape(re.sub("<[^>]+>", "", a)).strip()}} for q, a in items]


ORG = {"@type": "ProfessionalService", "@id": SITE + "/#org", "name": "Fintlock", "legalName": "Fintlock LLC", "url": SITE + "/",
       "logo": SITE + "/assets/brand/fintlock-mark.svg", "image": SITE + "/assets/brand/fintlock-social-card.png", "email": EMAIL,
       "description": "Independent software studio in Tampa, Florida building native iPhone apps, web apps, business tools, and custom smart TV home screens.",
       "address": {"@type": "PostalAddress", "addressLocality": "Tampa", "addressRegion": "FL", "addressCountry": "US"},
       "areaServed": [{"@type": "Country", "name": "United States"}, {"@type": "Place", "name": "Tampa Bay area"}],
       "knowsAbout": ["iPhone app development", "SwiftUI", "custom business software", "web application development", "smart TV apps", "automation"],
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Software development services", "itemListElement":
           [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": p["schema_name"], "url": SITE + "/" + p["slug"]}} for p in SERVICE_PAGES] +
           [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Custom TV Home Screen (TV SmartHub)", "url": SITE + "/custom-tv-home-screen.html"}}]}}
PLANTS_LD = {"@type": "MobileApplication", "name": "Plants in Pocket", "url": PLANTS_APP_STORE, "downloadUrl": PLANTS_APP_STORE,
             "applicationCategory": "LifestyleApplication", "operatingSystem": "iOS 17 or later", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
             "description": "Identify a plant, check its health, and follow a care plan with reminders.", "author": {"@id": SITE + "/#org"},
             "sameAs": ["https://www.tiktok.com/@plantsinpocket"]}


def ld(*nodes):
    return '  <script type="application/ld+json">' + _json.dumps({"@context": "https://schema.org", "@graph": list(nodes)}, ensure_ascii=False) + "</script>\n</head>"


for path, (title, desc, body, og) in PAGES.items():
    preload = {"index.html": "assets/tv/tv-day.webp", "custom-tv-home-screen.html": "assets/tv/tv-night.webp"}.get(path)
    html = head(title, desc, path, og, preload)
    if path == "index.html":
        html = html.replace("</head>", ld(ORG, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Fintlock", "publisher": {"@id": SITE + "/#org"}},
                                           PLANTS_LD, {"@type": "FAQPage", "@id": SITE + "/#faq", "mainEntity": faq_from(body)}))
    elif path == "custom-tv-home-screen.html":
        html = html.replace("</head>", ld({"@type": "Service", "name": "Custom TV Home Screen (TV SmartHub)", "serviceType": "Custom smart TV home screen",
                                            "description": desc, "url": SITE + "/" + path, "areaServed": {"@type": "Place", "name": "Tampa Bay area"},
                                            "provider": {"@id": SITE + "/#org", "@type": "ProfessionalService", "name": "Fintlock", "url": SITE + "/"}},
                                           {"@type": "FAQPage", "mainEntity": faq_from(body)}))
    elif path == "work.html":
        html = html.replace("</head>", ld(PLANTS_LD,
            {"@type": "SoftwareApplication", "name": "Fintley", "url": "https://fintley.app", "applicationCategory": "FinanceApplication", "operatingSystem": "iOS",
             "description": "Real estate appraisal for iPhone. Type an address and get an estimated value, rent, cash flow, comparable sales, and a Forecast score.", "author": {"@id": SITE + "/#org"}}))
    sp = next((p for p in SERVICE_PAGES if p["slug"] == path), None)
    if sp:
        html = html.replace("</head>", ld({"@type": "Service", "name": sp["schema_name"], "serviceType": sp["schema_name"], "description": sp["description"],
                                            "url": SITE + "/" + path, "areaServed": "US", "provider": {"@type": "ProfessionalService", "@id": SITE + "/#org", "name": "Fintlock", "url": SITE + "/"}},
                                           {"@type": "FAQPage", "mainEntity": faq_from(body)}))
    if path in ("services.html",):
        html = html.replace("</head>", ld({"@type": "FAQPage", "mainEntity": faq_from(body)}))
    html = modernize(html + header(path) + body + footer(path))
    (ROOT / path).write_text(html, encoding="utf-8")
    print("wrote", path, len(html))

nf = ROOT / "404.html"
_h = nf.read_text()
_h = _h.replace('<link rel="canonical" href="https://fintlock.com/404.html">', '<meta name="robots" content="noindex">')
_h = re.sub(r'(href|src)="(assets/|site\.css|site\.js)', r'\1="/\2', _h)
_h = re.sub(r'href="([a-z0-9-]+)\.html([#"?])', lambda m: 'href="/' + ('' if m.group(1) == 'index' else m.group(1) + '.html') + m.group(2), _h)
nf.write_text(_h, encoding="utf-8")

sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path in PAGES:
    if path == "404.html":
        continue
    loc = SITE + "/" + (path if path != "index.html" else "")
    sitemap.append(f"  <url><loc>{loc}</loc><lastmod>{BUILD_DATE:%Y-%m-%d}</lastmod></url>")
sitemap.append("</urlset>\n")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")
(ROOT / "version.json").write_text(_json.dumps({"version": VERSION, "published": f"{BUILD_DATE:%Y-%m-%d}"}) + "\n", encoding="utf-8")
print("wrote sitemap.xml, version.json", VERSION)
