#!/usr/bin/env python3
"""Assemble les pages statiques du site ACDC dans dist/.

Header, footer, formulaire et grille de galerie vivent ici : c'est la source
unique, les huit pages en decoulent. Sortie = HTML autonome, l'hebergeur
n'execute rien.

    python3 tools/build.py
"""
import html
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

# Bascule de publication. Par defaut on construit la maquette : noindex partout
# et bandeau de demonstration. Pour le site reel :
#     SITE_URL=https://acdcair.com.au DEMO=0 npm run build
SITE_URL = os.environ.get("SITE_URL", "https://example.invalid").rstrip("/")
# Le CSS est injecte dans chaque page : une requete bloquante en moins, et
# 6,7 Ko gzip absorbes par la reponse HTML qui part de toute facon.
CRITICAL_CSS = ""
DEMO = os.environ.get("DEMO", "1") != "0"

# --------------------------------------------------------------------------
# Donnees reelles. Rien ici n'est invente : ce qui manque est un [placeholder].
# --------------------------------------------------------------------------
TEL_LAND = ("+61894466146", "9446 6146")
TEL_MOB = ("+61432230757", "0432 230 757")
EMAIL = "daniel@acdcair.com.au"
# Relevee sur la fiche Google / les annuaires. A faire confirmer par Daniel.
ADDRESS = ("57A Boronia St", "Innaloo", "WA", "6018")
TAGLINE = "Fast &amp; reliable heating and air conditioning service in Perth Metropolitan area"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("gallery.html", "Gallery"),
    ("contact.html", "Contact"),
]

SERVICE_PAGES = [
    ("air-conditioning.html", "Air Conditioning"),
    ("mechanical-ventilation.html", "Mechanical Ventilation"),
    ("maintenance.html", "Maintenance"),
]

# Marques : 7 logos fournis, Daikin et LG en mot (aucun logo fourni).
BRAND_LOGOS = [
    ("brand-actronair", "Actron Air", 287),
    ("brand-fujitsu", "Fujitsu", 170),
    ("brand-hitachi", "Hitachi", 186),
    ("brand-mitsubishi", "Mitsubishi", 285),
    ("brand-panasonic", "Panasonic", 228),
    ("brand-samsung", "Samsung", 201),
    ("brand-toshiba", "Toshiba", 201),
]
BRAND_WORDS = ["Daikin", "LG"]

# Galerie : uniquement des photos ACDC authentiques. Le stock fourni
# (technicien generique, toitures americaines, rendus 3D) est ecarte.
# Notes publiques par plateforme. Volontairement non fusionnees en une seule
# moyenne : les trois panels n'ont ni la meme taille ni le meme public.
RATINGS = [
    ("Google", "5.0", 5, "https://www.google.com/search?q=acdc+air+innaloo"),
    ("ServiceSeeking", "4.9", 12, None),
    ("Birdeye", "4.4", 8, None),
]

# Avis publics releves sur la fiche Google et sur ServiceSeeking.
# Textes repris mot pour mot, avec leur source : rien n'est reformule.
REVIEWS = [
    ("yulisese d", "Google", "5/5", "11 months ago",
     "Dan is a very experienced technician who goes above and beyond. "
     "He&rsquo;s very knowledgeable and makes you feel comfortable with his advice."),
    ("Review on ServiceSeeking", "ServiceSeeking", "5/5", "6 years ago",
     "Arrived on time and did a great job. Will definitely use again."),
    ("Prabal Pokharel", "Google", "5/5", "8 months ago",
     "Easily 5 stars. &hellip;"),
]

GALLERY = [
    ("vrv-outdoor-units-rooftop-platform-perth",
     "Three VRV outdoor units installed on a rooftop plant platform, Perth",
     "VRV plant platform"),
    ("daikin-vrv-condensers-commercial-rooftop-perth",
     "Daikin VRV condensers installed on a commercial rooftop, Perth",
     "Daikin VRV condensers"),
    ("crane-lifting-air-conditioning-unit-house-perth",
     "Crane lifting an air conditioning unit over a house during installation, Perth",
     "Crane lift, residential install"),
    ("technician-testing-condenser-electrical-panel-perth",
     "Technician testing the electrical panel of a rooftop condenser during commissioning",
     "Commissioning and electrical testing"),
    ("fujitsu-dc-inverter-units-steel-frame-perth",
     "Two Fujitsu DC Inverter outdoor units mounted on a steel frame, Perth",
     "Fujitsu DC Inverter, frame mounted"),
    ("daikin-outdoor-units-roof-walkway-perth",
     "Daikin outdoor units installed along a roof walkway, Perth",
     "Roof walkway installation"),
    ("daikin-outdoor-unit-metal-roof-perth",
     "Daikin outdoor unit installed on a metal roof beside an apartment building, Perth",
     "Metal roof installation"),
    ("actronair-outdoor-unit-residential-perth",
     "Actron Air outdoor unit installed beside a rendered wall at a Perth home",
     "Actron Air, residential"),
    ("acdc-service-vans-perth-street",
     "Two ACDC Air Conditioning service vans parked on a Perth street",
     "The ACDC service vans"),
    ("actronair-mitsubishi-units-loaded-ute-perth",
     "Actron Air and Mitsubishi Heavy Industries units loaded on the ACDC ute before installation",
     "Stock loaded for the day"),
    ("daikin-split-system-showroom-display-perth",
     "Daikin split system on display with energy saving information",
     "Choosing the right split system"),
]


SNOWFLAKE = ('<svg class="flake" viewBox="0 0 64 64" aria-hidden="true">'
             '<path d="M32 8v48M11.2 20l41.6 24M11.2 44l41.6-24"/>'
             '<path d="M32 8l-6 7M32 8l6 7M32 56l-6-7M32 56l6-7"/>'
             '<path d="M11.2 20l1.2-9.2M11.2 20l-9 2.4M52.8 44l-1.2 9.2M52.8 44l9-2.4"/>'
             '<path d="M11.2 44l-9-2.4M11.2 44l1.2 9.2M52.8 20l9 2.4M52.8 20l-1.2-9.2"/>'
             '</svg>')


def stars(score):
    """Cinq etoiles dont les pleines correspondent a la note arrondie."""
    full = round(float(score))
    out = ""
    for i in range(5):
        cls = "star" if i < full else "star star-off"
        out += (f'<svg class="{cls}" viewBox="0 0 20 20" aria-hidden="true">'
                f'<path d="M10 1.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L1.6 7.7l5.8-.8z"/>'
                f'</svg>')
    return f'<span class="stars" role="img" aria-label="{score} out of 5">{out}</span>'


def pending(label):
    """Marqueur d'information manquante : une croix + le libelle.

    Un seul composant pour tout le site, pour qu'on repere d'un coup d'oeil
    ce qui reste a obtenir pendant la presentation.
    """
    return (f'<span class="pending"><svg viewBox="0 0 16 16" aria-hidden="true">'
            f'<path d="M4 4l8 8M12 4l-8 8"/></svg>{label} '
            f'<i>to confirm with Daniel</i></span>')


def img(stem, alt, widths, sizes, *, lazy=True, cls="", extra=""):
    """<picture> AVIF puis WebP. width/height fixes : aucun saut de mise en page."""
    biggest = max(widths)
    ratio = 549 / 720 if stem.startswith("hero-") else 600 / 800
    loading = ('loading="lazy" decoding="async"' if lazy
               else 'fetchpriority="high" decoding="async"')
    sources = "".join(
        f'<source type="image/{ext}" sizes="{sizes}" srcset="'
        + ", ".join(f"img/{stem}-{w}.{ext} {w}w" for w in widths) + '">'
        for ext in ("avif", "webp")
    )
    return (f'<picture>{sources}'
            f'<img src="img/{stem}-{biggest}.webp" alt="{alt}" '
            f'width="{biggest}" height="{round(biggest * ratio)}" '
            f'{loading} class="{cls}"{extra}></picture>')


def breadcrumbs(page, label):
    if page == "index.html":
        return ""
    return f""",
  {{
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_URL}/" }},
      {{ "@type": "ListItem", "position": 2, "name": "{label}",
         "item": "{SITE_URL}/{page.replace('.html', '')}" }}
    ]
  }}"""


def jsonld(page_name, label=""):
    return f"""<script type="application/ld+json">
{{ "@context": "https://schema.org", "@graph": [
{{
  "@type": "HVACBusiness",
  "@id": "{SITE_URL}/#business",
  "url": "{SITE_URL}/",
  "name": "ACDC Air Conditioning",
  "slogan": "Fast & reliable heating and air conditioning service in Perth Metropolitan area",
  "email": "{EMAIL}",
  "telephone": ["{TEL_LAND[0]}", "{TEL_MOB[0]}"],
  "areaServed": {{ "@type": "City", "name": "Perth Metropolitan Area, Western Australia" }},
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{ADDRESS[0]}",
    "addressLocality": "{ADDRESS[1]}",
    "addressRegion": "{ADDRESS[2]}",
    "postalCode": "{ADDRESS[3]}",
    "addressCountry": "AU"
  }},
  "knowsAbout": ["Split system installation", "Ducted air conditioning",
                 "Refrigerated air conditioning", "Mechanical ventilation",
                 "Preventative maintenance"],
  "brand": ["Actron Air", "Daikin", "Fujitsu", "LG", "Mitsubishi", "Samsung",
            "Panasonic", "Hitachi", "Toshiba"]
  }}{breadcrumbs(page_name, label)}
] }}
</script>"""


def head(page, title, description, label="", og_image="hero-crane-lift-perth-720"):
    links = "\n".join(
        f'        <a href="{href}" class="nav-link{" is-current" if href == page else ""}">{label_}</a>'
        for href, label_ in NAV
    )
    canonical = f"{SITE_URL}/" if page == "index.html" else f"{SITE_URL}/{page.replace('.html', '')}"
    # la 404 ne doit jamais entrer dans l'index, meme hors demo
    robots = ("noindex, nofollow" if DEMO or page == "404.html"
              else "index, follow, max-image-preview:large, max-snippet:-1")
    plain_title = html.unescape(title).replace("&", "&amp;")

    demo_banner = ("""<p class="demo-banner">
  Demonstration mock-up &mdash; proposed redesign.
  <span>Not the official ACDC Air Conditioning website.</span>
</p>
""" if DEMO else "")

    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="website">
<meta property="og:locale" content="en_AU">
<meta property="og:site_name" content="ACDC Air Conditioning">
<meta property="og:title" content="{plain_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/img/{og_image}.webp">
<meta property="og:image:alt" content="Crane lifting an air conditioning unit over a house in Perth">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{plain_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/img/{og_image}.webp">

<meta name="geo.region" content="AU-WA">
<meta name="geo.placename" content="Innaloo, Perth">
<meta name="geo.position" content="-31.893;115.795">
<meta name="ICBM" content="-31.893, 115.795">
<meta name="theme-color" content="#000000">

<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="assets/open-sans.woff2" crossorigin>
<link rel="preload" as="image" href="img/{og_image}.avif" type="image/avif" fetchpriority="high">
<style>{CRITICAL_CSS}</style>
{jsonld(page, label)}
</head>
<body>

<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span id="scrollBar"></span></div>
<div class="cursor" id="cursor" aria-hidden="true"></div>

{demo_banner}
<div class="topbar">
  <div class="lane flex flex-wrap items-center justify-between gap-4 py-2">
    <p>Perth Metropolitan Area, Western Australia</p>
    <p class="flex items-center gap-2">
      <a href="tel:{TEL_LAND[0]}" class="font-semibold text-white hover:text-signal-blue">{TEL_LAND[1]}</a>
      <span aria-hidden="true" class="text-slate">/</span>
      <a href="tel:{TEL_MOB[0]}" class="font-semibold text-white hover:text-signal-blue">{TEL_MOB[1]}</a>
    </p>
  </div>
</div>

<header class="nav" id="nav">
  <div class="lane flex min-h-16 items-center gap-6">
    <a href="index.html" class="flex items-center" data-magnetic>
      <picture>
        <source type="image/avif" srcset="img/acdc-logo-313.avif">
        <source type="image/webp" srcset="img/acdc-logo-313.webp">
        <img src="img/acdc-logo.png" alt="ACDC Air Conditioning" width="313" height="147"
             class="h-9 w-auto object-contain" fetchpriority="high" decoding="async">
      </picture>
    </a>

    <nav class="relative mx-auto hidden gap-6 md:flex" id="navLinks" aria-label="Main">
{links}
      <span class="nav-ink" id="navInk" aria-hidden="true"></span>
    </nav>

    <div class="ml-auto flex items-center gap-4 md:ml-0">
      <a href="tel:{TEL_MOB[0]}" class="hidden items-center gap-2 text-[14px] font-semibold text-iron hover:text-signal-blue sm:flex">
        <svg class="icon" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3h3l1.5 4-2 1.5a8 8 0 0 0 4 4L13 10.5 17 12v3a2 2 0 0 1-2 2A12 12 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>
        {TEL_MOB[1]}
      </a>
      <a href="contact.html#quote" class="btn btn-blue hidden md:inline-flex" data-magnetic>Get a free quote</a>
      <button class="flex h-8 w-8 flex-col justify-center gap-[5px] md:hidden" id="burger"
              aria-label="Menu" aria-expanded="false" aria-controls="mobileNav">
        <span class="block h-px bg-iron transition-transform duration-300"></span>
        <span class="block h-px bg-iron transition-transform duration-300"></span>
      </button>
    </div>
  </div>

  <nav id="mobileNav" class="max-h-0 overflow-hidden bg-white transition-[max-height] duration-500 md:hidden"
       aria-label="Mobile">
    <div class="lane py-2">
{links.replace('class="nav-link', 'class="block border-b border-fog py-4 nav-link')}
      <a href="contact.html#quote" class="btn btn-blue my-4">Get a free quote</a>
    </div>
  </nav>
</header>

<main id="main">
"""


def footer():
    cols = [
        ("Services", [("air-conditioning.html", "Air conditioning"),
                      ("mechanical-ventilation.html", "Mechanical ventilation"),
                      ("maintenance.html", "Maintenance"),
                      ("services.html", "All services")]),
        ("Company", [("about.html", "About ACDC"), ("gallery.html", "Our work"),
                     ("contact.html", "Contact"), ("contact.html#quote", "Request a quote")]),
    ]
    nav_cols = ""
    for title, items in cols:
        rows = "".join(f'<a href="{h}">{t}</a>' for h, t in items)
        nav_cols += (f'<div><h2 class="footer-head">{title}</h2>'
                     f'<nav class="footer-nav">{rows}</nav></div>')

    brands = " &middot; ".join(["Actron Air", "Daikin", "Fujitsu", "LG", "Mitsubishi",
                               "Samsung", "Panasonic", "Hitachi", "Toshiba"])

    return f"""</main>

<footer class="footer">
  <div class="lane">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="index.html" class="footer-mark" aria-label="ACDC Air Conditioning, home">
          {SNOWFLAKE}
          <span class="footer-mark-word">ACDC</span>
          <span class="footer-mark-sub">Air-conditioning &middot; Domestic &middot; Commercial<br>
            Service &amp; Installation</span>
        </a>
        <p class="footer-tagline">{TAGLINE}.</p>
        <p>{pending("High-resolution logo")}</p>
      </div>

      <address class="footer-contact">
        <a href="tel:{TEL_LAND[0]}" class="footer-tel">{TEL_LAND[1]}</a>
        <a href="tel:{TEL_MOB[0]}" class="footer-tel">{TEL_MOB[1]}</a>
        <a href="mailto:{EMAIL}" class="footer-mail">{EMAIL}</a>
        <p class="footer-addr">{ADDRESS[0]}, {ADDRESS[1]} {ADDRESS[2]} {ADDRESS[3]}<br>
          Serving the Perth Metropolitan Area</p>
      </address>
    </div>

    <div class="footer-grid">
      {nav_cols}
      <div>
        <h2 class="footer-head">Trading hours</h2>
        <p>{pending("Opening hours")}</p>
        <h2 class="footer-head mt-8">Licensing</h2>
        <p>{pending("ARC / electrical licence")}</p>
        <p>{pending("ABN")}</p>
      </div>
      <div>
        <h2 class="footer-head">Legal</h2>
        <nav class="footer-nav">
          <a href="privacy.html">Privacy &amp; terms</a>
        </nav>
        <h2 class="footer-head mt-8">Follow</h2>
        <p>{pending("Facebook &amp; Instagram")}</p>
        <p><a href="https://www.google.com/search?q=acdc+air+innaloo" rel="noopener"
              class="footer-link-inline">Google reviews <span class="chev">&rsaquo;</span></a></p>
      </div>
    </div>

    <p class="footer-brands">We install and service {brands}.</p>

    <div class="footer-base">
      <p>&copy; 2026 ACDC Air Conditioning &middot; Innaloo, Western Australia</p>
      {'<p class="footer-demo">Demonstration mock-up &ndash; proposed redesign. '
        'Not the official ACDC Air Conditioning website.</p>' if DEMO else ''}
    </div>
  </div>
</footer>

<div class="fixed right-6 bottom-6 z-[55] hidden gap-2 md:grid">
  <a href="tel:{TEL_MOB[0]}" class="fab" aria-label="Call ACDC">
    <svg class="icon" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3h3l1.5 4-2 1.5a8 8 0 0 0 4 4L13 10.5 17 12v3a2 2 0 0 1-2 2A12 12 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>
  </a>
  <a href="contact.html#quote" class="fab fab-blue" aria-label="Request a quote">
    <svg class="icon" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h14v9H8l-5 3z"/></svg>
  </a>
</div>

<a class="callbar" href="tel:{TEL_MOB[0]}">
  <svg class="icon" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3h3l1.5 4-2 1.5a8 8 0 0 0 4 4L13 10.5 17 12v3a2 2 0 0 1-2 2A12 12 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>
  Call now &middot; {TEL_MOB[1]}
</a>

<script src="assets/main.js" defer></script>
</body>
</html>
"""


FOOTER = footer()


def quote_form(anchor=True):
    aid = ' id="quote"' if anchor else ""
    return f"""<form class="grid gap-4 rounded bg-white p-8 sm:grid-cols-2" data-form{aid}
          action="[Formspree endpoint to be supplied]" method="post" novalidate>
      <div class="field">
        <label for="f-name">Name</label>
        <input id="f-name" name="name" required autocomplete="name" placeholder="Full name">
      </div>
      <div class="field">
        <label for="f-email">Email</label>
        <input id="f-email" name="email" type="email" required autocomplete="email" placeholder="you@example.com">
      </div>
      <div class="field">
        <label for="f-phone">Phone</label>
        <input id="f-phone" name="phone" type="tel" required autocomplete="tel" placeholder="0400 000 000">
      </div>
      <div class="field">
        <label for="f-suburb">Suburb</label>
        <input id="f-suburb" name="suburb" required autocomplete="address-level2" placeholder="Innaloo">
      </div>
      <div class="field sm:col-span-2">
        <label for="f-service">Service</label>
        <select id="f-service" name="service" required>
          <option value="">Choose a service</option>
          <option>Installation</option>
          <option>Repair</option>
          <option>Maintenance</option>
          <option>Ventilation</option>
          <option>Commercial</option>
        </select>
      </div>
      <div class="field sm:col-span-2">
        <label for="f-message">Message</label>
        <textarea id="f-message" name="message" rows="4"
                  placeholder="Rooms to cover, current system, anything we should know"></textarea>
      </div>
      <div class="flex flex-wrap items-center gap-4 sm:col-span-2">
        <button class="btn btn-blue" type="submit" data-magnetic>Send enquiry</button>
        <p class="text-[12px] text-graphite" data-note role="status" aria-live="polite"></p>
      </div>
    </form>"""


def cta_band(heading, copy):
    return f"""<section class="section section-dark">
  <div class="lane grid items-start gap-16 lg:grid-cols-2">
    <div class="grid gap-6">
      <p class="eyebrow" data-reveal>Free quote</p>
      <h2 class="heading split" data-split>{heading}</h2>
      <p class="text-fog" data-reveal data-delay="200">{copy}</p>
      <p class="text-fog" data-reveal data-delay="260">
        Or call <a href="tel:{TEL_MOB[0]}" class="font-semibold text-signal-blue hover:text-white">{TEL_MOB[1]}</a>.
      </p>
    </div>
    {quote_form()}
  </div>
</section>"""


def brand_strip():
    logos = ""
    for stem, name, w in BRAND_LOGOS:
        logos += (f'<picture>'
                  f'<source type="image/avif" srcset="img/{stem}-{w}.avif">'
                  f'<img src="img/{stem}-{w}.webp" alt="{name}" width="{w}" height="90" '
                  f'loading="lazy" decoding="async"></picture>')
    for word in BRAND_WORDS:
        logos += f'<span class="marquee-word">{word}</span>'
    return f"""<div class="marquee" aria-label="Brands we install and service">
  <div class="marquee-track">{logos}{logos}</div>
</div>"""


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

SERVICE_TILES = [
    ("Residential", "Domestic",
     "Split systems and ducted air conditioning for homes across the Perth metro area.",
     '<rect x="34" y="52" width="132" height="52" rx="5"/><path d="M100 14 32 52h136z"/>'
     '<path d="M64 104V82h28v22" class="dash"/>'),
    ("Business", "Commercial",
     "Offices, shops and industrial sites. Sized for the load, not for the catalogue.",
     '<rect x="28" y="26" width="58" height="78" rx="4"/><rect x="104" y="50" width="68" height="54" rx="4"/>'
     '<path d="M44 44h26M44 64h26M44 84h26M120 68h36M120 86h36" class="dash"/>'),
    ("Supply &amp; fit", "Installation",
     "Refrigerated units, split systems and ducted air conditioning, installed properly.",
     '<rect x="28" y="32" width="92" height="34" rx="5"/><path d="M138 49h34M156 33v32" class="dash"/>'
     '<path d="M48 82q26 18 52 0" class="dash"/>'),
    ("Winter", "Heating",
     "Reverse-cycle heating that holds temperature through a Perth winter.",
     '<path d="M100 20c16 20 4 30 0 40-6 14 8 24 8 24" class="dash"/>'
     '<path d="M78 38c12 16 3 24 0 32-5 11 6 19 6 19" class="dash"/>'
     '<path d="M122 38c12 16 3 24 0 32-5 11 6 19 6 19" class="dash"/>'
     '<rect x="44" y="92" width="112" height="14" rx="7"/>'),
    ("Summer", "Cooling",
     "Refrigerated cooling, correctly sized and correctly commissioned.",
     '<circle cx="100" cy="62" r="28"/><path d="M100 24v76M62 62h76M76 38l48 48M124 38l-48 48" class="dash"/>'),
    ("Up front", "Design",
     "A complete solution; from consult to design to installation.",
     '<path d="M30 100 100 28l70 72"/><path d="M62 100V72h28v28" class="dash"/><circle cx="100" cy="28" r="4"/>'),
]


def page_home():
    tiles = "\n".join(
        f"""      <article class="card card-outlined" data-reveal data-delay="{(i % 3) * 80}" data-tilt>
        <p class="card-cat">{cat}</p>
        <h3 class="card-name">{name}</h3>
        <p class="card-desc">{desc}</p>
        <div class="card-art"><svg viewBox="0 0 200 120" aria-hidden="true">{art}</svg></div>
        <a href="services.html" class="card-go">Get a quote <span class="chev">&rsaquo;</span></a>
      </article>"""
        for i, (cat, name, desc, art) in enumerate(SERVICE_TILES)
    )

    pillars = [
        ("Fast Reliable Service",
         "When the system stops, the call gets answered and the job gets booked."),
        ("Service and Installation",
         "Highly trained and experts in HVAC service and replacements. We do the job right the first time."),
        ("Honest and Fair",
         "Thorough, informative, and knowledgeable."),
    ]
    pill_html = "\n".join(
        f"""      <article class="grid content-start gap-2" data-reveal data-delay="{i * 90}">
        <span class="mb-4 block h-0.5 w-10 bg-signal-blue" aria-hidden="true"></span>
        <h3 class="text-[24px] font-semibold tracking-[-0.02em] text-iron">{t}</h3>
        <p class="text-[14px]">{d}</p>
      </article>"""
        for i, (t, d) in enumerate(pillars)
    )

    reviews = "\n".join(
        f"""      <blockquote class="review" data-reveal data-delay="{i * 90}" data-tilt>
        {stars(rating.split("/")[0])}
        <p class="review-text">&ldquo;{text}&rdquo;</p>
        <footer class="review-by">
          <b>{who}</b>
          <span>{source} &middot; {when}</span>
        </footer>
      </blockquote>"""
        for i, (who, source, rating, when, text) in enumerate(REVIEWS)
    )

    score_cards = "".join(
        f"""<{'a href="' + url + '" rel="noopener"' if url else 'div'} class="score" data-reveal data-delay="{i * 80}">
          <b class="score-value">{value}</b>
          {stars(value)}
          <span class="score-meta">{name} &middot; {count} reviews</span>
        </{'a' if url else 'div'}>"""
        for i, (name, value, count, url) in enumerate(RATINGS)
    )

    return f"""<section class="hero">
  <div class="hero-media" data-parallax="0.1" aria-hidden="true">
    {img("hero-crane-lift-perth",
         "Crane lifting an air conditioning unit over a house while the ACDC ute waits on site, Perth",
         [480, 720], "100vw", lazy=False)}
  </div>
  <div class="hero-vignette" aria-hidden="true"></div>
  <canvas class="hero-flow" id="flow" aria-hidden="true"></canvas>

  <div class="lane relative py-28 text-center">
    <p class="eyebrow text-ash" data-reveal>Perth Metropolitan Area</p>
    <h1 class="display split mx-auto mt-4 max-w-4xl text-white" data-split>{TAGLINE}</h1>
    <p class="mx-auto mt-6 max-w-2xl text-fog" data-reveal data-delay="240">
      With over 20 years of experience, we&rsquo;re the right choice to take care of your
      air conditioning requirements.
    </p>
    <div class="mt-10 flex flex-wrap justify-center gap-4" data-reveal data-delay="380">
      <a class="btn btn-blue" href="tel:{TEL_MOB[0]}" data-magnetic>Call {TEL_MOB[1]}</a>
      <a class="btn btn-ghost-light" href="contact.html#quote" data-magnetic>Get a free quote <span class="chev">&rsaquo;</span></a>
    </div>
  </div>

  <a class="scrollcue" href="#promise" aria-label="Scroll down"><span></span></a>
</section>

{brand_strip()}

<section class="section" id="promise">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow" data-reveal>Why ACDC</p>
      <h2 class="heading split" data-split>A complete solution; from consult to design to installation.</h2>
      <p class="lede" data-reveal data-delay="180">Getting it right, first time, every time.</p>
    </header>
    <div class="grid gap-12 md:grid-cols-3">
{pill_html}
    </div>
    <div class="mt-16 flex items-baseline gap-4 border-t border-fog pt-8" data-reveal>
      <b class="counter text-[clamp(40px,6vw,64px)] font-light tracking-[-0.03em] text-iron tabular-nums"
         data-to="20" data-suffix="+">0</b>
      <span class="text-[14px] text-slate">years of experience across Perth</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow" data-reveal>What we do</p>
      <h2 class="heading split" data-split>Six ways we keep Perth comfortable.</h2>
    </header>
    <div class="grid gap-12 md:grid-cols-2 lg:grid-cols-3">
{tiles}
    </div>
  </div>
</section>

<section class="relative overflow-hidden bg-onyx">
  <div class="absolute inset-0" data-parallax="0.12" aria-hidden="true">
    {img("daikin-vrv-condensers-commercial-rooftop-perth",
         "Daikin VRV condensers installed on a commercial rooftop in Perth",
         [480, 800], "100vw", cls="h-full w-full object-cover opacity-35")}
  </div>
  <div class="hero-vignette" aria-hidden="true"></div>
  <div class="lane relative grid place-items-center py-32 text-center">
    <p class="eyebrow text-ash" data-reveal>Commercial</p>
    <h2 class="heading split mt-4 max-w-3xl text-white" data-split>Plant that gets commissioned, labelled and handed over.</h2>
    <p class="mt-6 max-w-2xl text-fog" data-reveal data-delay="200">
      Installations, repairs, services and maintenance for residential, commercial and
      industrial clients throughout Perth.
    </p>
    <div class="mt-10 flex flex-wrap justify-center gap-4" data-reveal data-delay="300">
      <a class="btn btn-ghost-light" href="gallery.html" data-magnetic>See the work <span class="chev">&rsaquo;</span></a>
      <a class="btn btn-blue" href="contact.html#quote" data-magnetic>Get a free quote</a>
    </div>
  </div>
</section>

<section class="section section-fog" id="reviews">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow" data-reveal>Reviews</p>
      <h2 class="heading split" data-split>Rated by the people we worked for.</h2>
    </header>

    <div class="scores">{score_cards}</div>

    <div class="grid gap-12 md:grid-cols-3">
{reviews}
    </div>

    <p class="mt-12 flex flex-wrap items-center justify-center gap-6 text-center" data-reveal data-delay="240">
      <a class="btn btn-blue" href="https://www.google.com/search?q=acdc+air+innaloo"
         rel="noopener" data-magnetic>Read all reviews on Google <span class="chev">&rsaquo;</span></a>
      {pending("Live Google reviews widget")}
    </p>
  </div>
</section>

{cta_band("Tell us about the space. We&rsquo;ll size the system.",
          "Installations, repairs, services and maintenance for residential, commercial and "
          "industrial clients throughout Perth.")}
"""


def page_about():
    brands = "".join(
        f'<li class="border-b border-[#dcdcdc] pb-2 text-[20px] font-light tracking-[-0.02em] '
        f'text-iron transition-colors hover:border-signal-blue hover:text-signal-blue">{b}</li>'
        for b in ["Actron Air", "Daikin", "Fujitsu", "LG", "Mitsubishi",
                  "Samsung", "Panasonic", "Hitachi", "Toshiba"]
    )
    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>About</p>
    <h1 class="display split" data-split>ACDC aims to keep you comfortable all year round.</h1>
  </div>
</section>

<section class="section">
  <div class="lane grid max-w-3xl gap-6">
    <p class="lede" data-reveal>
      Tired of those sleepless summer nights and chilly winter mornings?
    </p>
    <p data-reveal data-delay="120">
      ACDC offers its clients the best solutions for all their air conditioning needs,
      ensuring it delivers the most energy efficient results across Perth. Installation,
      repair, service and maintenance for residential, commercial and industrial clients.
    </p>
    <p data-reveal data-delay="200">
      With over 20 years of experience, we&rsquo;re the right choice to take care of your
      air conditioning requirements.
    </p>
  </div>
</section>

<section class="section section-fog">
  <div class="lane grid items-center gap-16 lg:grid-cols-2">
    <figure class="overflow-hidden rounded" data-reveal>
      {img("acdc-service-vans-perth-street",
           "Two ACDC Air Conditioning service vans parked on a Perth street",
           [480, 800], "(min-width: 1024px) 50vw, 100vw", cls="w-full")}
    </figure>
    <div class="grid gap-6">
      <h2 class="heading split" data-split>A team, not a one-man band.</h2>
      <p data-reveal data-delay="160">
        Management, tradesmen, apprentices and administrative staff, all experienced in
        their field. Every enquiry goes to someone who works that discipline, so the advice
        you get is specialist advice.
      </p>
      <p data-reveal data-delay="220">
        <a class="btn btn-blue" href="contact.html#quote" data-magnetic>Get a free quote</a>
      </p>
    </div>
  </div>
</section>

<section class="section">
  <div class="lane grid items-start gap-16 lg:grid-cols-2">
    <div class="grid gap-6">
      <h2 class="heading split" data-split>Aligned with the brands that hold up.</h2>
      <p data-reveal data-delay="160">
        ACDC is aligned with Actron Air, Daikin, Fujitsu, LG, Mitsubishi, Samsung,
        Panasonic, Hitachi and Toshiba, to provide solutions suited to every budget.
        Products are bought directly from the manufacturer.
      </p>
    </div>
    <ul class="grid gap-4 sm:grid-cols-2" data-reveal data-delay="200">{brands}</ul>
  </div>
</section>

<section class="section section-fog">
  <div class="lane grid items-start gap-16 lg:grid-cols-[1fr_1.2fr]">
    <figure class="grid gap-4" data-reveal>
      <div class="grid aspect-4/5 place-items-center rounded bg-white p-6 text-center">
        {pending("Portrait photo")}
      </div>
      <figcaption class="grid gap-0.5 text-[14px]">
        <b class="font-semibold text-iron">Daniel {pending("Surname")}</b>
        <span class="text-[12px] text-ash">Owner &middot; ACDC Air Conditioning</span>
      </figcaption>
    </figure>
    <div class="grid gap-6">
      <h2 class="heading split" data-split>Run by the person who does the work.</h2>
      <p data-reveal data-delay="160">
        Serving Perth and all its surrounding suburbs. Straight answers on what a system
        will cost, what it will do, and what it will not do.
      </p>
      <p data-reveal data-delay="200">
        Based at {ADDRESS[0]}, {ADDRESS[1]} {ADDRESS[2]} {ADDRESS[3]}. &middot;
        {pending("ARC / electrical licence")} {pending("ABN")}
      </p>
      <p data-reveal data-delay="260">
        <a class="btn btn-ghost-dark" href="gallery.html" data-magnetic>See our work <span class="chev">&rsaquo;</span></a>
      </p>
    </div>
  </div>
</section>
"""


def page_services():
    cards = [
        ("air-conditioning.html", "Air Conditioning",
         "Installation, maintenance and repair of refrigerated units, split systems and "
         "ducted air conditioning, across every brand.",
         "daikin-outdoor-units-roof-walkway-perth",
         "Daikin outdoor units installed along a roof walkway, Perth"),
        ("mechanical-ventilation.html", "Mechanical Ventilation",
         "Design, installation, fabrication and commissioning of ventilation systems, "
         "to standard.",
         None, None),
        ("maintenance.html", "Maintenance",
         "Preventative maintenance programs built around your equipment, for air "
         "conditioning and refrigeration.",
         "technician-testing-condenser-electrical-panel-perth",
         "Technician testing the electrical panel of a rooftop condenser during commissioning"),
    ]
    out = ""
    for i, (href, name, desc, stem, alt) in enumerate(cards):
        media = (f'<div class="overflow-hidden rounded">{img(stem, alt, [480, 800], "(min-width: 768px) 33vw, 100vw", cls="w-full transition-transform duration-700 group-hover:scale-105")}</div>'
                 if stem else
                 '<div class="grid aspect-4/3 place-items-center rounded bg-fog p-6 text-center">'
                 '{pending("Ventilation photo")}</div>')
        out += f"""      <article class="group card" data-reveal data-delay="{i * 90}">
        <h2 class="card-name">{name}</h2>
        <p class="card-desc">{desc}</p>
        <div class="my-4">{media}</div>
        <a href="{href}" class="card-go">Read more <span class="chev">&rsaquo;</span></a>
      </article>
"""
    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>Services</p>
    <h1 class="display split" data-split>Air conditioning, ventilation and maintenance across Perth.</h1>
  </div>
</section>

<section class="section section-fog">
  <div class="lane grid gap-12 md:grid-cols-3">
{out}  </div>
</section>

<section class="section">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow" data-reveal>Which one</p>
      <h2 class="heading split" data-split>Start from the symptom, not the catalogue.</h2>
    </header>
    <div class="grid gap-12 md:grid-cols-3">
      <article class="grid content-start gap-3" data-reveal>
        <h3 class="text-[20px] font-semibold tracking-[-0.02em] text-iron">The room is too hot or too cold</h3>
        <p class="text-[14px]">That is an air conditioning question: either there is no system,
          or the one there is was never sized for the space. Either way it starts with a survey
          of the room, its orientation and its glazing.</p>
        <a href="air-conditioning.html" class="text-[14px] font-semibold text-signal-blue">
          Air conditioning <span class="chev">&rsaquo;</span></a>
      </article>
      <article class="grid content-start gap-3" data-reveal data-delay="90">
        <h3 class="text-[20px] font-semibold tracking-[-0.02em] text-iron">The air is stale, damp or full of fumes</h3>
        <p class="text-[14px]">Cooling will not fix that. Air has to be moved out and replaced,
          at the rate the use of the space demands, which is a ventilation design rather than a
          bigger air conditioner.</p>
        <a href="mechanical-ventilation.html" class="text-[14px] font-semibold text-signal-blue">
          Mechanical ventilation <span class="chev">&rsaquo;</span></a>
      </article>
      <article class="grid content-start gap-3" data-reveal data-delay="180">
        <h3 class="text-[20px] font-semibold tracking-[-0.02em] text-iron">It worked better last summer</h3>
        <p class="text-[14px]">Gradual loss of performance is the signature of a dirty coil, a
          slow refrigerant leak or a blocked drain. All three are cheap while they are still
          gradual, and expensive once the compressor goes.</p>
        <a href="maintenance.html" class="text-[14px] font-semibold text-signal-blue">
          Maintenance <span class="chev">&rsaquo;</span></a>
      </article>
    </div>
  </div>
</section>

{cta_band("Describe the problem, not the product.",
          "What the building is used for, what the system is doing wrong, and when it started. "
          "That is enough for us to tell you which of the three it is.")}
"""


def service_page(title, lede, paragraphs, bullets, benefits, stem, alt, faq_note,
                 deep_title, deep_blocks, cta_title, cta_copy):
    paras = "".join(f'<p data-reveal data-delay="{120 + i*60}">{p}</p>'
                    for i, p in enumerate(paragraphs))
    tick = "".join(f"<li>{b}</li>" for b in bullets)
    ben = "".join(
        f'<article class="card" data-reveal data-delay="{i*80}" data-tilt>'
        f'<h3 class="card-name text-[20px]">{t}</h3><p class="card-desc">{d}</p></article>'
        for i, (t, d) in enumerate(benefits))
    deep = "".join(
        f'<article class="grid content-start gap-3" data-reveal data-delay="{i*80}">'
        f'<h3 class="text-[20px] font-semibold tracking-[-0.02em] text-iron">{t}</h3>'
        f'<p class="text-[14px]">{d}</p></article>'
        for i, (t, d) in enumerate(deep_blocks))

    media = (f'<figure class="overflow-hidden rounded" data-reveal data-delay="150">'
             f'{img(stem, alt, [480, 800], "(min-width: 1024px) 50vw, 100vw", cls="w-full")}'
             f'</figure>' if stem else
             '<div class="grid aspect-4/3 place-items-center rounded bg-fog p-8 text-center" '
             'data-reveal data-delay="150">{pending("Photo")}</div>')

    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>Service</p>
    <h1 class="display split" data-split>{title}</h1>
    <p class="mt-6 max-w-2xl text-fog" data-reveal data-delay="240">{lede}</p>
  </div>
</section>

<section class="section">
  <div class="lane grid items-start gap-16 lg:grid-cols-2">
    <div class="grid gap-6">{paras}
      <p data-reveal data-delay="320">
        <a class="btn btn-blue" href="contact.html#quote" data-magnetic>Get a quote</a>
      </p>
    </div>
    {media}
  </div>
</section>

<section class="section section-fog">
  <div class="lane grid items-start gap-16 lg:grid-cols-2">
    <div class="grid gap-6">
      <h2 class="heading split" data-split>What the job covers.</h2>
      <ul class="ticks" data-reveal data-delay="160">{tick}</ul>
    </div>
    <div class="grid gap-6">
      <h2 class="heading split" data-split>Frequently asked</h2>
      <div class="awaiting" data-reveal data-delay="160">
        {pending("FAQ to write")}
        <p>Three to five real questions, in Daniel&rsquo;s words: {faq_note}.
          Answered questions are what Google shows under the result, and what stops
          the phone ringing for things the page could have answered.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow" data-reveal>What you get</p>
      <h2 class="heading split" data-split>Why it matters.</h2>
    </header>
    <div class="grid gap-12 md:grid-cols-2 lg:grid-cols-4">{ben}</div>
  </div>
</section>

<section class="section section-fog">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow" data-reveal>Detail</p>
      <h2 class="heading split" data-split>{deep_title}</h2>
    </header>
    <div class="grid gap-12 md:grid-cols-2">{deep}</div>
  </div>
</section>

{cta_band(cta_title, cta_copy)}
"""


def page_gallery():
    tiles = ""
    for i, (stem, alt, caption) in enumerate(GALLERY):
        tiles += f"""      <figure class="tile" data-reveal data-delay="{(i % 4) * 70}"
              tabindex="0" role="button" aria-label="Open: {alt}">
        {img(stem, alt, [480, 800], "(min-width: 1024px) 25vw, (min-width: 560px) 50vw, 100vw")}
        <figcaption>{caption}</figcaption>
      </figure>
"""
    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>Gallery</p>
    <h1 class="display split" data-split>Work completed across the Perth metro area.</h1>
    <p class="mt-6 max-w-2xl text-fog" data-reveal data-delay="240">
      Every photo below is an ACDC job. Nothing here is stock photography.
    </p>
  </div>
</section>

<section class="section">
  <div class="lane">
    <div class="tiles" id="gallery">
{tiles}    </div>
    <p class="mt-12 text-[14px] text-slate" data-reveal>
      {pending("More recent job photos")} &mdash;
      phone photos from the last few jobs are worth more here than anything from the archive.
    </p>
  </div>
</section>

<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="lb-btn top-4 right-6" id="lbClose" aria-label="Close">&times;</button>
  <button class="lb-btn top-1/2 left-6 -translate-y-1/2" id="lbPrev" aria-label="Previous">&lsaquo;</button>
  <figure class="grid justify-items-center">
    <img id="lbImg" src="" alt="">
    <figcaption id="lbCap"></figcaption>
  </figure>
  <button class="lb-btn top-1/2 right-6 -translate-y-1/2" id="lbNext" aria-label="Next">&rsaquo;</button>
</div>

{cta_band("Want the same done at your place?",
          "Most of these started as a photo and a rough idea of the space. "
          "Send yours and we&rsquo;ll come back with a real number.")}
"""


def page_privacy():
    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>Legal</p>
    <h1 class="display split" data-split>Privacy &amp; terms.</h1>
    <p class="mt-6 max-w-2xl text-fog" data-reveal data-delay="240">
      This page is part of a demonstration mock-up. The wording below is a skeleton
      for the real notice, not legal advice.
    </p>
  </div>
</section>

<section class="section">
  <div class="lane grid max-w-3xl gap-10">
    <div class="grid gap-4" data-reveal>
      <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-iron">Who we are</h2>
      <p>ACDC Air Conditioning, {ADDRESS[0]}, {ADDRESS[1]} {ADDRESS[2]} {ADDRESS[3]},
        serving the Perth Metropolitan Area.</p>
      <p>{pending("Registered entity name and ABN")}</p>
    </div>

    <div class="grid gap-4" data-reveal data-delay="80">
      <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-iron">What the enquiry form collects</h2>
      <p>Name, email, phone, suburb, the service you selected and your message. It is used
        to answer your enquiry and to quote the work, and for nothing else.</p>
      <p>On this mock-up the form is not connected to anything: nothing is transmitted and
        nothing is stored. {pending("Form handler and retention period")}</p>
    </div>

    <div class="grid gap-4" data-reveal data-delay="160">
      <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-iron">Third parties</h2>
      <p>The contact page embeds a Google Maps frame and the pages load Open Sans from
        Google Fonts. Both are requests to Google servers and are subject to Google&rsquo;s
        own privacy terms.</p>
      <p>No analytics, no advertising pixel and no tracking cookie is set by this site.</p>
    </div>

    <div class="grid gap-4" data-reveal data-delay="240">
      <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-iron">Your rights</h2>
      <p>You can ask what we hold about you, ask for it to be corrected, or ask for it to be
        deleted. Write to <a href="mailto:{EMAIL}" class="font-semibold text-signal-blue">{EMAIL}</a>.</p>
      <p>{pending("Complaints process and OAIC reference")}</p>
    </div>

    <div class="grid gap-4" data-reveal data-delay="320">
      <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-iron">Quotes and work</h2>
      <p>{pending("Quote validity, deposit terms, warranty and cancellation")}</p>
    </div>

    <div class="grid gap-4" data-reveal data-delay="400">
      <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-iron">Photography</h2>
      <p>The photographs on this site are of work carried out by ACDC. Manufacturer
        trade marks belong to their respective owners and appear because the equipment
        shown is theirs.</p>
    </div>
  </div>
</section>
"""


def page_404():
    return f"""<section class="pagehead" style="min-height:60svh;display:grid;align-content:center">
  <div class="lane">
    <p class="eyebrow" data-reveal>404</p>
    <h1 class="display split" data-split>That page isn&rsquo;t here.</h1>
    <p class="mt-6 max-w-xl text-fog" data-reveal data-delay="240">
      The link may be old, or the page may have moved. The system still needs fixing,
      so here is the quick way through.
    </p>
    <div class="mt-10 flex flex-wrap gap-4" data-reveal data-delay="340">
      <a class="btn btn-blue" href="tel:{TEL_MOB[0]}" data-magnetic>Call {TEL_MOB[1]}</a>
      <a class="btn btn-ghost-light" href="index.html" data-magnetic>Back to home <span class="chev">&rsaquo;</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="lane grid gap-12 md:grid-cols-3">
    <a href="services.html" class="card card-outlined" data-tilt data-reveal>
      <h2 class="card-name">Services</h2>
      <p class="card-desc">Air conditioning, mechanical ventilation, maintenance.</p>
      <span class="card-go">Go <span class="chev">&rsaquo;</span></span>
    </a>
    <a href="gallery.html" class="card card-outlined" data-tilt data-reveal data-delay="90">
      <h2 class="card-name">Our work</h2>
      <p class="card-desc">Jobs completed across the Perth metro area.</p>
      <span class="card-go">Go <span class="chev">&rsaquo;</span></span>
    </a>
    <a href="contact.html#quote" class="card card-outlined" data-tilt data-reveal data-delay="180">
      <h2 class="card-name">Free quote</h2>
      <p class="card-desc">Tell us what the job is and we will come back to you.</p>
      <span class="card-go">Go <span class="chev">&rsaquo;</span></span>
    </a>
  </div>
</section>
"""


def page_contact():
    rows = [
        ("Phone", f'<a href="tel:{TEL_LAND[0]}" class="hover:text-signal-blue">{TEL_LAND[1]}</a>'),
        ("Mobile", f'<a href="tel:{TEL_MOB[0]}" class="hover:text-signal-blue">{TEL_MOB[1]}</a>'),
        ("Email", f'<a href="mailto:{EMAIL}" class="hover:text-signal-blue">{EMAIL}</a>'),
        ("Service area", "Perth Metropolitan Area, Western Australia"),
        ("Address", f'{ADDRESS[0]}, {ADDRESS[1]} {ADDRESS[2]} {ADDRESS[3]}'),
        ("Trading hours", pending("Opening hours")),
        ("Licence / ABN", pending("ARC licence and ABN")),
    ]
    dl = "".join(
        f'<div data-reveal data-delay="{i*70}">'
        f'<dt class="mb-1 text-[12px] font-semibold uppercase tracking-[0.12em] text-slate">{k}</dt>'
        f'<dd class="text-[20px] font-light tracking-[-0.02em] text-iron">{v}</dd></div>'
        for i, (k, v) in enumerate(rows)
    )
    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>Contact</p>
    <h1 class="display split" data-split>Call, or tell us what the job is.</h1>
  </div>
</section>

<section class="section">
  <div class="lane grid items-start gap-16 lg:grid-cols-2">
    <div class="grid gap-12">
      <dl class="contactinfo grid gap-6">{dl}</dl>
      <figure class="overflow-hidden rounded" data-reveal data-delay="300">
        {img("hero-acdc-van-perth",
             "Rear of an ACDC Air Conditioning van showing the logo and phone number 0432 230 757",
             [480, 720], "(min-width: 1024px) 50vw, 100vw", cls="w-full")}
      </figure>
    </div>
    <div class="overflow-hidden rounded bg-fog" data-reveal data-delay="150">
      <iframe title="ACDC Air Conditioning, 57A Boronia St, Innaloo WA"
              src="https://www.google.com/maps?q=57A%20Boronia%20St%2C%20Innaloo%20WA%206018&amp;hl=en&amp;z=14&amp;output=embed"
              class="h-[420px] w-full border-0" loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>

{cta_band("Every enquiry gets a real answer.",
          "Installation, repair, maintenance, ventilation or a commercial site &mdash; "
          "tell us which, and we will come back to you.")}
"""


PAGES = [
    ("index.html",
     "Air Conditioning Perth | ACDC Air Conditioning",
     "Split system installation, ducted air conditioning, repairs and maintenance across "
     "the Perth Metropolitan Area. Over 20 years of experience.",
     page_home, "Home"),
    ("about.html",
     "About ACDC Air Conditioning | Perth HVAC Specialists",
     "Energy efficient air conditioning for residential, commercial and industrial clients "
     "across Perth. Installation, repair, service and maintenance.",
     page_about, "About"),
    ("services.html",
     "Air Conditioning Services Perth | Install, Ventilation, Service",
     "Air conditioning, mechanical ventilation and preventative maintenance for homes and "
     "businesses across the Perth Metropolitan Area.",
     page_services, "Services"),
    ("air-conditioning.html",
     "Split System &amp; Ducted Air Conditioning Perth | ACDC",
     "Split system installation Perth and ducted air conditioning, plus maintenance and repair "
     "of refrigerated units across every major brand.",
     lambda: service_page(
         "A renowned air con specialist serving Perth and all its surrounding suburbs.",
         "Installation, maintenance and repair of refrigerated units, split systems and "
         "ducted air conditioning.",
         ["ACDC installs, maintains and repairs air conditioning of every type and every brand: "
          "refrigerated units, split systems and ducted air conditioning.",
          "Products are bought directly from the manufacturer, which keeps the price honest and "
          "the warranty clean.",
          "We also service systems installed by someone else. You do not have to have bought it "
          "from us for us to look after it."],
         ["Refrigerated unit installation", "Split system supply and install",
          "Ducted air conditioning", "Maintenance and repair, all brands",
          "Systems installed by others", "Residential, commercial and industrial"],
         [("Smooth design", "The system is designed before anything is drilled."),
          ("Hassle-free install", "Scheduled, clean, and finished when we said it would be."),
          ("Preventative maintenance", "Small problems found while they are still small."),
          ("A better space", "A building people want to be in is a building that works.")],
         "daikin-outdoor-units-roof-walkway-perth",
         "Daikin outdoor units installed along a roof walkway, Perth",
         "typical questions on sizing, running cost and install time",
         "Choosing between a split, a multi-head and ducted.",
         [("One room, one head",
           "A single split serves one space. It is the cheapest entry point and the quickest "
           "install, and it is the right answer for a bedroom, a home office or an extension "
           "that the rest of the house does not need to cool."),
          ("Several rooms, one condenser",
           "A multi-head runs up to five indoor units off one outdoor unit. You get separate "
           "control per room and only one condenser on the wall, which matters when the side "
           "of the house is tight or the strata rules limit external plant."),
          ("Whole house, hidden",
           "Ducted puts the plant in the roof space and leaves only grilles in the ceiling. "
           "Zoning lets you shut off the bedrooms during the day. It costs more and it needs "
           "roof clearance, so it is decided at the survey, not over the phone."),
          ("Why sizing is the whole job",
           "An oversized unit cools fast, then short-cycles: it never runs long enough to pull "
           "humidity out, it wears the compressor, and it costs more to run than the correctly "
           "sized machine next door. This is why the kilowatt figure comes from the room, "
           "not from the price list."),
          ("Refrigerant lines and drainage",
           "Line length, height difference between indoor and outdoor units, and where the "
           "condensate actually drains to decide where equipment can go. Getting this wrong "
           "is the most common reason a system underperforms from day one."),
          ("Servicing what someone else installed",
           "You do not have to have bought the system from us for us to maintain or repair it. "
           "We work across every brand we install, and several we do not.")],
         "Book a survey, not a phone quote.",
         "Send the rooms, the orientation and what the building already has. "
         "The number that comes back is based on the space, not on a guess."), "Air Conditioning"),
    ("mechanical-ventilation.html",
     "Mechanical Ventilation Perth | Car Park, Kitchen, Warehouse | ACDC",
     "Mechanical ventilation in Perth: car park, wet area, toilet exhaust, kitchen range "
     "hoods, dust and fume extraction and warehouse.",
     lambda: service_page(
         "Ventilation designed for the space it has to clear.",
         "Design, installation, fabrication and commissioning, to standard.",
         ["Some buildings do not need cooling, they need air moved. ACDC designs, fabricates, "
          "installs and commissions mechanical ventilation systems that comply with the "
          "relevant standards.",
          "The work covers everything from a single wet area fan to warehouse-scale extraction."],
         ["Car park ventilation", "Wet area ventilation", "Toilet exhaust",
          "Kitchen range hoods", "Dust and fume extraction", "Warehouse ventilation"],
         [("Designed", "Sized for the volume and the air changes actually required."),
          ("Fabricated", "Ductwork made to fit the building, not the other way round."),
          ("Installed", "By the people who designed it."),
          ("Commissioned", "Measured, adjusted and documented before handover.")],
         None, None,
         "typical questions on compliance, noise and commissioning documents",
         "What each kind of ventilation has to achieve.",
         [("Car park",
           "Exhaust has to clear vehicle emissions at the rate the building code sets for the "
           "volume and the traffic. Undersized fans fail their commissioning test, not their "
           "occupants&rsquo; comfort test."),
          ("Wet areas and toilets",
           "Moisture that is not extracted ends up in the plasterboard. Extraction is sized to "
           "the room volume and the number of air changes required, and it has to discharge "
           "outside, not into the roof space."),
          ("Kitchen range hoods",
           "Commercial kitchen extraction carries grease and heat, so the ductwork, the "
           "filtration and the access panels for cleaning are part of the design, not an "
           "afterthought bolted on at the end."),
          ("Dust and fume extraction",
           "Workshop extraction is designed around the capture point: the closer the hood is "
           "to the source, the smaller the fan you need and the less energy the system burns "
           "for the rest of its life."),
          ("Warehouse",
           "Large volumes move on stack effect and cross-flow as much as on fans. A design "
           "that ignores where the openings already are ends up fighting the building."),
          ("Fabrication and commissioning",
           "Ductwork is fabricated to suit the building rather than the building being cut to "
           "suit stock duct. Once installed, flows are measured and adjusted, and the readings "
           "are what gets handed over.")],
         "Send the drawings, or the problem.",
         "A plan set, a photo of the space, or simply what is not clearing. "
         "Ventilation is sized from the volume and the use, so both are the starting point."), "Mechanical Ventilation"),
    ("maintenance.html",
     "Air Conditioning Service &amp; Maintenance Perth | ACDC",
     "Preventative maintenance for air conditioning and refrigeration across Perth. "
     "An unmaintained system wastes energy, then fails.",
     lambda: service_page(
         "Preventative maintenance beats an emergency call-out.",
         "Programs tailored to your equipment, for air conditioning and refrigeration.",
         ["A system that is not maintained wastes energy and wastes money, and it fails at the "
          "worst possible moment.",
          "ACDC builds a preventative maintenance program around the equipment you actually have, "
          "rather than a generic schedule, covering both air conditioning and refrigeration."],
         ["Programs matched to your equipment", "Air conditioning and refrigeration",
          "Scheduled servicing", "Fewer breakdowns", "Efficiency kept where it should be"],
         [("Lower running cost", "A dirty coil costs money every hour it runs."),
          ("Fewer failures", "Most breakdowns announce themselves first."),
          ("Longer equipment life", "The cheapest system is the one you do not replace."),
          ("Planned, not urgent", "Servicing at a time that suits the site.")],
         "technician-testing-condenser-electrical-panel-perth",
         "Technician testing the electrical panel of a rooftop condenser during commissioning",
         "typical questions on service frequency, cost and what a visit covers",
         "What maintenance actually changes.",
         [("Filters and coils",
           "A blocked filter starves the coil of air. The compressor keeps running, the room "
           "never reaches setpoint, and the power bill climbs without anything looking broken."),
          ("Refrigerant charge",
           "A system slowly losing charge cools less each summer. Caught at a service it is a "
           "leak repair; ignored, it runs the compressor outside its envelope until it fails."),
          ("Electrical connections",
           "Terminals loosen with thermal cycling. Checking and retorquing them during a "
           "service is minutes of work, and it is the difference between a clean run and a "
           "burnt contactor in February."),
          ("Condensate drains",
           "Drains block with biofilm. The first sign is usually a ceiling stain, which costs "
           "more to repair than a decade of servicing."),
          ("Refrigeration too",
           "Cool rooms and display cabinets run continuously and fail expensively, with stock "
           "loss on top. They belong on the same schedule as the air conditioning."),
          ("Scheduled beats urgent",
           "A planned visit happens when the site is quiet. A breakdown happens on the hottest "
           "day of the year, when every contractor in Perth is already booked.")],
         "Put the equipment on a schedule.",
         "Tell us what is on site and how it is used. The program is built around that, "
         "not around a generic annual visit."), "Maintenance"),
    ("gallery.html",
     "Our Work | Air Conditioning Installations Perth | ACDC",
     "Split system, ducted and VRV air conditioning installations completed by ACDC across Perth "
     "and its surrounding suburbs.",
     page_gallery, "Gallery"),
    ("privacy.html",
     "Privacy &amp; Terms | ACDC Air Conditioning Perth",
     "How ACDC Air Conditioning handles enquiry details, and the terms that apply to "
     "quotes and work across the Perth Metropolitan Area.",
     page_privacy, "Privacy"),
    ("404.html",
     "Page not found | ACDC Air Conditioning Perth",
     "That page is not here. Call ACDC Air Conditioning on 0432 230 757 or head back "
     "to the home page.",
     page_404, "Not found"),
    ("contact.html",
     "Contact ACDC Air Conditioning | Free Quote, Perth",
     "Call 0432 230 757 or request a free quote for air conditioning installation, repair "
     "or maintenance across the Perth Metropolitan Area.",
     page_contact, "Contact"),
]


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="#000"/>
  <g stroke="#0070d5" stroke-width="3.2" stroke-linecap="round">
    <path d="M32 12v40M14.7 22l34.6 20M14.7 42l34.6-20"/>
    <path d="M32 12l-5 6M32 12l5 6M32 52l-5-6M32 52l5-6"/>
    <path d="M14.7 22l1-7.8M14.7 22l-7.6 2M49.3 42l-1 7.8M49.3 42l7.6-2"/>
    <path d="M14.7 42l-7.6-2M14.7 42l1 7.8M49.3 22l7.6 2M49.3 22l-1-7.8"/>
  </g>
</svg>"""

def robots_txt():
    if DEMO:
        return "# Maquette de demonstration : rien ne doit etre indexe.\nUser-agent: *\nDisallow: /\n"
    return (f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")


def subset_font():
    """Reduit la fonte aux caracteres reellement employes par les pages generees."""
    import subprocess
    subprocess.run(["python3", str(ROOT / "tools" / "subset_font.py")], check=True)


def check_images():
    """Verifie que chaque image citee par une page existe vraiment dans dist/img."""
    present = {p.name for p in (DIST / "img").iterdir()} if (DIST / "img").is_dir() else set()
    wanted = set()
    for page in DIST.glob("*.html"):
        wanted |= set(re.findall(r"img/([\w.-]+\.(?:avif|webp|png))", page.read_text(encoding="utf-8")))
    return wanted - present


def main():
    global CRITICAL_CSS
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "assets").mkdir(exist_ok=True)

    css_file = DIST / "assets" / "site.css"
    if not css_file.exists():
        raise SystemExit("dist/assets/site.css absent : lancer `npm run css` avant `npm run pages`.")
    CRITICAL_CSS = css_file.read_text(encoding="utf-8").strip()

    too_long = [f for f, _, d, *_ in PAGES if len(d) > 160]
    if too_long:
        raise SystemExit("meta description > 160 caracteres : " + ", ".join(too_long))

    for filename, title, description, builder, label in PAGES:
        page = head(filename, title, description, label) + builder() + FOOTER
        (DIST / filename).write_text(page, encoding="utf-8")
        print("wrote", filename)

    (DIST / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (DIST / "robots.txt").write_text(robots_txt(), encoding="utf-8")

    today = __import__("datetime").date.today().isoformat()
    skip = {"404.html", "privacy.html"}
    priority = {"index.html": "1.0", "contact.html": "0.9", "services.html": "0.8",
                "air-conditioning.html": "0.8", "gallery.html": "0.7"}
    urls = ""
    for f, *_ in PAGES:
        if f in skip:
            continue
        loc = f"{SITE_URL}/" if f == "index.html" else f"{SITE_URL}/{f.replace('.html', '')}"
        urls += (f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod>"
                 f"<priority>{priority.get(f, '0.6')}</priority></url>\n")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n", encoding="utf-8")

    (DIST / "assets" / "open-sans.woff2").write_bytes(
        (ROOT / "src" / "fonts" / "open-sans-latin.woff2").read_bytes())
    print("wrote favicon.svg, robots.txt, sitemap.xml, assets/open-sans.woff2")

    # la feuille a ete injectee dans les pages : plus rien ne la sert
    css_file.unlink()

    subset_font()

    missing = check_images()
    if missing:
        raise SystemExit("images referencees mais absentes : " + ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()
