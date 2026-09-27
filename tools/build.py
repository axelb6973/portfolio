#!/usr/bin/env python3
"""Assemble les pages statiques du site ACDC dans dist/.

Header, footer, formulaire et grille de galerie vivent ici : c'est la source
unique, les huit pages en decoulent. Sortie = HTML autonome, l'hebergeur
n'execute rien.

    python3 tools/build.py
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

# --------------------------------------------------------------------------
# Donnees reelles. Rien ici n'est invente : ce qui manque est un [placeholder].
# --------------------------------------------------------------------------
TEL_LAND = ("+61894466146", "9446 6146")
TEL_MOB = ("+61432230757", "0432 230 757")
EMAIL = "daniel@acdcair.com.au"
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


def img(stem, alt, widths, sizes, *, lazy=True, cls="", extra=""):
    """Un <img> WebP avec srcset. width/height fixes : pas de saut de mise en page."""
    srcset = ", ".join(f"img/{stem}-{w}.webp {w}w" for w in widths)
    biggest = max(widths)
    ratio = 549 / 720 if stem.startswith("hero-") else 600 / 800
    loading = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    return (f'<img src="img/{stem}-{biggest}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{alt}" width="{biggest}" height="{round(biggest * ratio)}" '
            f'{loading} class="{cls}"{extra}>')


def jsonld(page_name):
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HVACBusiness",
  "name": "ACDC Air Conditioning",
  "slogan": "Fast & reliable heating and air conditioning service in Perth Metropolitan area",
  "email": "{EMAIL}",
  "telephone": ["{TEL_LAND[0]}", "{TEL_MOB[0]}"],
  "areaServed": {{ "@type": "City", "name": "Perth Metropolitan Area, Western Australia" }},
  "address": {{ "@type": "PostalAddress", "addressRegion": "WA", "addressCountry": "AU" }},
  "knowsAbout": ["Split system installation", "Ducted air conditioning",
                 "Refrigerated air conditioning", "Mechanical ventilation",
                 "Preventative maintenance"],
  "brand": ["Actron Air", "Daikin", "Fujitsu", "LG", "Mitsubishi", "Samsung",
            "Panasonic", "Hitachi", "Toshiba"]
}}
</script>"""


def head(page, title, description):
    links = "\n".join(
        f'        <a href="{href}" class="nav-link{" is-current" if href == page else ""}">{label}</a>'
        for href, label in NAV
    )
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#000000">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
{jsonld(page)}
</head>
<body>

<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span id="scrollBar"></span></div>
<div class="cursor" id="cursor" aria-hidden="true"></div>

<div class="bg-carbon text-fog text-[12px] tracking-wider">
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
      <img src="img/acdc-logo.png" alt="ACDC Air Conditioning" width="313" height="147"
           class="h-9 w-auto object-contain">
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
    nav_cols = ""
    for title, items in [
        ("Services", [("air-conditioning.html", "Air conditioning"),
                      ("mechanical-ventilation.html", "Mechanical ventilation"),
                      ("maintenance.html", "Maintenance"),
                      ("services.html", "All services")]),
        ("Company", [("about.html", "About ACDC"), ("gallery.html", "Our work"),
                     ("contact.html", "Contact"), ("contact.html#quote", "Free quote")]),
    ]:
        rows = "".join(f'<a href="{h}">{t}</a>' for h, t in items)
        nav_cols += f'<div><h2>{title}</h2><nav>{rows}</nav></div>'

    return f"""</main>

<footer class="footer">
  <div class="lane grid gap-12 text-[14px] md:grid-cols-[1.6fr_1fr_1fr_1fr]">
    <div class="grid content-start gap-4">
      <img src="img/acdc-logo.png" alt="ACDC Air Conditioning" width="313" height="147"
           class="h-10 w-auto object-contain">
      <p class="text-fog">{TAGLINE}.</p>
      <p>
        <a href="tel:{TEL_LAND[0]}" class="font-semibold hover:text-signal-blue">{TEL_LAND[1]}</a> &middot;
        <a href="tel:{TEL_MOB[0]}" class="font-semibold hover:text-signal-blue">{TEL_MOB[1]}</a><br>
        <a href="mailto:{EMAIL}" class="font-semibold hover:text-signal-blue">{EMAIL}</a>
      </p>
    </div>
    {nav_cols}
    <div>
      <h2>Details</h2>
      <p class="py-1"><span class="todo">Trading hours [to be supplied]</span></p>
      <p class="py-1"><span class="todo">ARC / electrical licence [to be supplied]</span></p>
      <p class="py-1"><span class="todo">ABN [to be supplied]</span></p>
      <p class="py-1"><span class="todo">Google listing &amp; socials [to be supplied]</span></p>
    </div>
  </div>
  <div class="lane mt-12 flex flex-wrap justify-between gap-4 border-t border-[#3f3f3f] pt-6 text-[12px]">
    <p>&copy; 2026 ACDC Air Conditioning &middot; Perth Metropolitan Area, Western Australia</p>
    <p class="text-ash">Demonstration mock-up &ndash; proposed redesign. Not an official ACDC website.</p>
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
        logos += (f'<img src="img/{stem}-{w}.webp" alt="{name}" width="{w}" height="90" '
                  f'loading="lazy" decoding="async">')
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
        f"""      <article class="card" data-reveal data-delay="{(i % 3) * 80}" data-tilt>
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
        f"""      <blockquote class="grid min-h-40 place-content-center rounded bg-fog p-6 text-center"
                  data-reveal data-delay="{i * 90}" data-tilt>
        <p class="todo">[Google review to be added]</p>
      </blockquote>"""
        for i in range(3)
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

<section class="section section-fog">
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

<section class="section">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow" data-reveal>Reviews</p>
      <h2 class="heading split" data-split>What our customers say.</h2>
    </header>
    <div class="grid gap-12 md:grid-cols-3">
{reviews}
    </div>
    <p class="mt-12 text-center" data-reveal data-delay="240">
      <a class="btn btn-ghost-dark" href="[Google reviews URL to be supplied]" data-magnetic>
        See our Google reviews <span class="chev">&rsaquo;</span></a>
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
        <span class="todo">[Photo of Daniel to be supplied]</span>
      </div>
      <figcaption class="grid gap-0.5 text-[14px]">
        <b class="font-semibold text-iron">Daniel <span class="todo">[surname to be confirmed]</span></b>
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
        <span class="todo">Exact address [to be confirmed]</span> &middot;
        <span class="todo">ARC / electrical licence [to be supplied]</span> &middot;
        <span class="todo">ABN [to be supplied]</span>
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
                 '<span class="todo">[Ventilation photo to be supplied]</span></div>')
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

{cta_band("Not sure which one you need? Describe the problem.",
          "Tell us what the building does and what the system is doing wrong. "
          "We&rsquo;ll tell you which of the three it is.")}
"""


def service_page(title, lede, paragraphs, bullets, benefits, stem, alt, faq_note):
    paras = "".join(f'<p data-reveal data-delay="{120 + i*60}">{p}</p>'
                    for i, p in enumerate(paragraphs))
    tick = "".join(f"<li>{b}</li>" for b in bullets)
    ben = "".join(
        f'<article class="card" data-reveal data-delay="{i*80}" data-tilt>'
        f'<h3 class="card-name text-[20px]">{t}</h3><p class="card-desc">{d}</p></article>'
        for i, (t, d) in enumerate(benefits))
    media = (f'<figure class="overflow-hidden rounded" data-reveal data-delay="150">'
             f'{img(stem, alt, [480, 800], "(min-width: 1024px) 50vw, 100vw", cls="w-full")}'
             f'</figure>' if stem else
             '<div class="grid aspect-4/3 place-items-center rounded bg-fog p-8 text-center" '
             'data-reveal data-delay="150"><span class="todo">[Photo to be supplied]</span></div>')

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
      <p data-reveal data-delay="160"><span class="todo">[FAQ to be supplied &mdash; {faq_note}]</span></p>
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

{cta_band("Ready when you are.",
          "Every enquiry gets a real answer from someone who works this discipline.")}
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
      <span class="todo">[More recent job photos to be supplied]</span> &mdash;
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
          "Send the details and we&rsquo;ll come back with a real number.")}
"""


def page_contact():
    rows = [
        ("Phone", f'<a href="tel:{TEL_LAND[0]}" class="hover:text-signal-blue">{TEL_LAND[1]}</a>'),
        ("Mobile", f'<a href="tel:{TEL_MOB[0]}" class="hover:text-signal-blue">{TEL_MOB[1]}</a>'),
        ("Email", f'<a href="mailto:{EMAIL}" class="hover:text-signal-blue">{EMAIL}</a>'),
        ("Service area", "Perth Metropolitan Area, Western Australia"),
        ("Address", '<span class="todo">[to be confirmed]</span>'),
        ("Trading hours", '<span class="todo">[to be supplied]</span>'),
        ("Licence / ABN", '<span class="todo">[ARC licence and ABN to be supplied]</span>'),
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
    <dl class="grid gap-6">{dl}</dl>
    <div class="overflow-hidden rounded bg-fog" data-reveal data-delay="150">
      <iframe title="ACDC Air Conditioning service area, Perth"
              src="https://www.google.com/maps?q=Perth%2C%20Western%20Australia&amp;hl=en&amp;z=11&amp;output=embed"
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
     "Fast and reliable heating and air conditioning service across the Perth Metropolitan Area. "
     "Split system installation, ducted air conditioning, repairs and maintenance. Over 20 years of experience.",
     page_home),
    ("about.html",
     "About ACDC Air Conditioning | Perth HVAC Specialists",
     "ACDC aims to keep you comfortable all year round, delivering the most energy efficient "
     "air conditioning results across Perth for residential, commercial and industrial clients.",
     page_about),
    ("services.html",
     "Air Conditioning Services Perth | Install, Ventilation, Service",
     "Air conditioning, mechanical ventilation and preventative maintenance for homes and "
     "businesses across the Perth Metropolitan Area.",
     page_services),
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
         "typical questions on sizing, running cost and install time")),
    ("mechanical-ventilation.html",
     "Mechanical Ventilation Perth | Car Park, Kitchen, Warehouse | ACDC",
     "Design, installation, fabrication and commissioning of mechanical ventilation in Perth: "
     "car park, wet area, toilet exhaust, kitchen range hoods, dust and fume extraction, warehouse.",
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
         "typical questions on compliance, noise and commissioning documents")),
    ("maintenance.html",
     "Air Conditioning Service &amp; Maintenance Perth | ACDC",
     "Preventative maintenance programs for air conditioning and refrigeration across Perth. "
     "An unmaintained system wastes energy and money, and eventually breaks down.",
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
         "typical questions on service frequency, cost and what a visit covers")),
    ("gallery.html",
     "Our Work | Air Conditioning Installations Perth | ACDC",
     "Split system, ducted and VRV air conditioning installations completed by ACDC across Perth "
     "and its surrounding suburbs.",
     page_gallery),
    ("contact.html",
     "Contact ACDC Air Conditioning | Free Quote, Perth",
     "Call ACDC Air Conditioning on 0432 230 757 or request a free quote for air conditioning "
     "installation, repair or maintenance anywhere in the Perth Metropolitan Area.",
     page_contact),
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

ROBOTS = """# Maquette de demonstration : rien ne doit etre indexe.
User-agent: *
Disallow: /
"""


def main():
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "assets").mkdir(exist_ok=True)

    for filename, title, description, builder in PAGES:
        page = head(filename, title, description) + builder() + FOOTER
        (DIST / filename).write_text(page, encoding="utf-8")
        print("wrote", filename)

    (DIST / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (DIST / "robots.txt").write_text(ROBOTS, encoding="utf-8")

    urls = "".join(f"  <url><loc>https://example.invalid/{f}</loc></url>\n"
                   for f, *_ in PAGES)
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- Domaine a remplacer au deploiement. La demo est en noindex. -->\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n", encoding="utf-8")

    (DIST / "assets" / "main.js").write_bytes((ROOT / "src" / "js" / "main.js").read_bytes())
    print("wrote favicon.svg, robots.txt, sitemap.xml, assets/main.js")


if __name__ == "__main__":
    main()
