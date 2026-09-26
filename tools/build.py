#!/usr/bin/env python3
"""Assemble les pages statiques du site ACDC.

Le header, le footer et les blocs communs vivent ici pour eviter la derive
entre les cinq pages. Sortie : des fichiers .html autonomes a la racine,
sans etape de build cote hebergeur.

    python3 tools/build.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

TEL_LAND_HREF = "tel:+61894466146"
TEL_LAND_TEXT = "9446 6146"
TEL_MOB_HREF = "tel:+61432230757"
TEL_MOB_TEXT = "0432 230 757"
EMAIL = "daniel@acdcair.com.au"

JSONLD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HVACBusiness",
  "name": "ACDC Air Conditioning",
  "slogan": "Fast & reliable heating and air conditioning service in Perth Metropolitan area",
  "email": "daniel@acdcair.com.au",
  "telephone": ["+61894466146", "+61432230757"],
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Innaloo",
    "addressRegion": "WA",
    "addressCountry": "AU"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": -31.962367, "longitude": 115.900795 },
  "areaServed": { "@type": "City", "name": "Perth Metropolitan Area, Western Australia" },
  "knowsAbout": ["Split system installation", "Ducted air conditioning", "Mechanical ventilation", "Preventative maintenance"]
}
</script>"""

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("gallery.html", "Gallery"),
    ("contact.html", "Contact"),
]


def head(page, title, description):
    links = "\n".join(
        '      <a href="{href}" class="nav__link{cur}">{label}</a>'.format(
            href=href, label=label, cur=" is-current" if href == page else ""
        )
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
<link rel="icon" href="public/images/acdc-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{JSONLD}
</head>
<body>

<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span id="scrollBar"></span></div>
<div class="cursor" id="cursor" aria-hidden="true"></div>

<div class="topbar">
  <p>Perth Metropolitan Area &middot; based in Innaloo</p>
  <p class="topbar__tels">
    <a href="{TEL_LAND_HREF}">{TEL_LAND_TEXT}</a>
    <span aria-hidden="true">/</span>
    <a href="{TEL_MOB_HREF}">{TEL_MOB_TEXT}</a>
  </p>
</div>

<header class="nav" id="nav">
  <div class="nav__inner">
    <a class="brand" href="index.html" data-magnetic>
      <img src="public/images/acdc-logo.png" alt="ACDC Air Conditioning" width="150" height="40"
           onerror="this.replaceWith(Object.assign(document.createElement('span'),{{className:'brand__fallback',textContent:'ACDC'}}))">
    </a>

    <nav class="nav__links" id="navLinks" aria-label="Main">
{links}
      <span class="nav__ink" id="navInk" aria-hidden="true"></span>
    </nav>

    <div class="nav__utils">
      <a class="nav__tel" href="{TEL_MOB_HREF}">
        <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3h3l1.5 4-2 1.5a8 8 0 0 0 4 4L13 10.5 17 12v3a2 2 0 0 1-2 2A12 12 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>
        {TEL_MOB_TEXT}
      </a>
      <a class="btn btn--blue" href="contact.html#quote" data-magnetic>Get a free quote</a>
      <button class="burger" id="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
    </div>
  </div>
</header>

<main id="main">
"""


FOOTER = f"""</main>

<footer class="footer">
  <div class="lane footer__grid">
    <div class="footer__brand">
      <p class="brand__fallback brand__fallback--light">ACDC</p>
      <p>Fast &amp; reliable heating and air conditioning service in Perth Metropolitan area.</p>
      <p>
        <a href="{TEL_LAND_HREF}">{TEL_LAND_TEXT}</a> &middot;
        <a href="{TEL_MOB_HREF}">{TEL_MOB_TEXT}</a><br>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
      </p>
    </div>
    <div>
      <h2>Services</h2>
      <a href="services.html#air-conditioning">Air conditioning</a>
      <a href="services.html#ventilation">Mechanical ventilation</a>
      <a href="services.html#maintenance">Maintenance</a>
      <a href="services.html#systems">System types</a>
    </div>
    <div>
      <h2>Company</h2>
      <a href="about.html">About ACDC</a>
      <a href="gallery.html">Our work</a>
      <a href="contact.html">Contact</a>
      <a href="contact.html#quote">Free quote</a>
    </div>
    <div>
      <h2>Details</h2>
      <p class="todo">Trading hours [to be supplied]</p>
      <p class="todo">AU / ARC licence [to be supplied]</p>
      <p class="todo">ABN [to be supplied]</p>
      <p class="todo">Social links [to be supplied]</p>
    </div>
  </div>
  <div class="lane footer__base">
    <p>&copy; 2026 ACDC Air Conditioning &middot; Perth Metropolitan Area, Western Australia</p>
    <p class="demo-note">Demonstration mock-up &ndash; proposed redesign. Not an official ACDC website.</p>
  </div>
</footer>

<a class="callbar" href="{TEL_MOB_HREF}">
  <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3h3l1.5 4-2 1.5a8 8 0 0 0 4 4L13 10.5 17 12v3a2 2 0 0 1-2 2A12 12 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>
  Call now &middot; {TEL_MOB_TEXT}
</a>

<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def quote_form(compact=False):
    """Le formulaire de devis. Aucun endpoint reel n'est cable."""
    wide = "" if compact else ' id="quote"'
    return f"""<form class="form" data-form{wide} action="[Formspree endpoint to be supplied]" method="post" novalidate>
      <div class="field">
        <label for="q-name">Name</label>
        <input id="q-name" name="name" required autocomplete="name" placeholder="Full name">
      </div>
      <div class="field">
        <label for="q-email">Email</label>
        <input id="q-email" name="email" type="email" required autocomplete="email" placeholder="you@example.com">
      </div>
      <div class="field">
        <label for="q-phone">Phone</label>
        <input id="q-phone" name="phone" type="tel" required autocomplete="tel" placeholder="0400 000 000">
      </div>
      <div class="field">
        <label for="q-address">Address</label>
        <input id="q-address" name="address" autocomplete="street-address" placeholder="Street, suburb">
      </div>
      <div class="field field--full">
        <label for="q-service">Service needed</label>
        <select id="q-service" name="service" required>
          <option value="">Choose a service</option>
          <option>Installation</option>
          <option>Repair</option>
          <option>Maintenance</option>
          <option>Ventilation</option>
          <option>Commercial</option>
        </select>
      </div>
      <div class="field field--full">
        <label for="q-message">Message</label>
        <textarea id="q-message" name="message" rows="4" placeholder="Rooms to cover, current system, anything we should know"></textarea>
      </div>
      <div class="field--full form__foot">
        <button class="btn btn--blue" type="submit" data-magnetic>Send enquiry</button>
        <p class="form__note" data-note role="status"></p>
      </div>
    </form>"""


SERVICE_TILES = [
    ("Domestic", "Homes across the Perth metro area, from a single bedroom split to a whole-house ducted system.",
     '<rect x="34" y="52" width="132" height="54" rx="6"/><path d="M100 14 32 52h136z"/><path d="M62 106v-24h30v24" class="dash"/>'),
    ("Commercial", "Offices, shops and industrial sites. Systems sized for the load, not for the catalogue.",
     '<rect x="28" y="28" width="60" height="78" rx="4"/><rect x="104" y="52" width="68" height="54" rx="4"/><path d="M44 46h28M44 66h28M44 86h28M120 70h36M120 88h36" class="dash"/>'),
    ("Installation", "Supply and install of refrigerated units, split systems and ducted air conditioning.",
     '<rect x="30" y="34" width="92" height="34" rx="5"/><path d="M138 51h34M156 35v32" class="dash"/><path d="M50 82q26 18 52 0" class="dash"/>'),
    ("Heating", "Reverse-cycle heating that keeps the place comfortable through a Perth winter.",
     '<path d="M100 22c16 20 4 30 0 40-6 14 8 24 8 24" class="dash"/><path d="M78 40c12 16 3 24 0 32-5 11 6 19 6 19" class="dash"/><path d="M122 40c12 16 3 24 0 32-5 11 6 19 6 19" class="dash"/><rect x="44" y="92" width="112" height="16" rx="8"/>'),
    ("Cooling", "Refrigerated cooling, correctly sized and correctly commissioned so it holds temperature.",
     '<circle cx="100" cy="64" r="30"/><path d="M100 24v80M60 64h80M74 38l52 52M126 38l-52 52" class="dash"/>'),
    ("Design", "A complete solution; from consult to design to installation.",
     '<path d="M32 100 100 28l68 72"/><path d="M60 100v-30h30v30" class="dash"/><circle cx="100" cy="28" r="4"/>'),
]

BRANDS = ["Actron Air", "Daikin", "Fujitsu", "LG", "Mitsubishi", "Samsung", "Hitachi", "Toshiba", "Panasonic"]

GALLERY_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

GALLERY_ALTS = [
    "split system installation perth",
    "ducted air conditioning northern suburbs perth",
    "air conditioning maintenance perth",
    "wall mounted split system install innaloo",
    "outdoor condenser unit installation perth",
    "ducted air conditioning ceiling grille perth",
    "commercial air conditioning perth",
    "split system service and repair perth",
    "refrigerated air conditioning installation perth",
    "mechanical ventilation ducting perth",
    "roof mounted air conditioning unit perth",
    "evaporative to refrigerated changeover perth",
    "air conditioning installation western suburbs perth",
    "ducted system return air grille perth",
    "split system condenser bracket install perth",
    "air conditioning electrical connection perth",
    "ceiling cassette air conditioning perth",
    "warehouse ventilation extraction perth",
    "air conditioning filter clean and service perth",
    "multi head split system installation perth",
    "air conditioning pipework and insulation perth",
]


def gallery_tiles():
    out = []
    for i, n in enumerate(GALLERY_NUMBERS):
        alt = GALLERY_ALTS[i]
        out.append(
            f"""      <figure class="tile" data-reveal data-delay="{(i % 4) * 70}">
        <img src="public/images/gallery/{n}.jpg" alt="{alt}" loading="lazy" width="533" height="400"
             onerror="this.closest('.tile').classList.add('is-missing')">
        <figcaption class="tile__missing">[Image {n}-533x400.jpg to be added]</figcaption>
      </figure>"""
        )
    return "\n".join(out)


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def page_home():
    tiles = "\n".join(
        f"""      <article class="card" data-reveal data-delay="{(i % 3) * 80}" data-tilt>
        <h3 class="card__name">{name}</h3>
        <p class="card__desc">{desc}</p>
        <div class="card__art"><svg viewBox="0 0 200 120" aria-hidden="true">{art}</svg></div>
        <a class="card__go" href="services.html">Get a quote <span class="chev">&rsaquo;</span></a>
      </article>"""
        for i, (name, desc, art) in enumerate(SERVICE_TILES)
    )
    brands = "".join(f"<span>{b}</span><i aria-hidden=\"true\">&middot;</i>" for b in BRANDS)

    return f"""<section class="hero">
  <canvas class="hero__flow" id="flow" aria-hidden="true"></canvas>
  <div class="hero__halo" aria-hidden="true"></div>

  <div class="hero__content">
    <p class="eyebrow" data-reveal>Perth Metropolitan Area &middot; Innaloo</p>
    <h1 class="display split" data-split>Fast &amp; reliable heating and air conditioning service in Perth Metropolitan area</h1>
    <p class="hero__sub" data-reveal data-delay="240">
      With over 20 years of experience, we&rsquo;re the right choice to take care of your air conditioning requirements.
    </p>
    <div class="hero__cta" data-reveal data-delay="380">
      <a class="btn btn--blue" href="{TEL_MOB_HREF}" data-magnetic>Call {TEL_MOB_TEXT}</a>
      <a class="btn btn--ghost-light" href="contact.html#quote" data-magnetic>Get a free quote <span class="chev">&rsaquo;</span></a>
    </div>

    <div class="hero__unit" data-parallax="-0.08" aria-hidden="true">
      <svg viewBox="0 0 520 190" class="unit">
        <rect class="unit__body" x="20" y="20" width="480" height="120" rx="8"/>
        <path class="unit__lip" d="M20 132 H500 L470 168 H50 Z"/>
        <g class="unit__vents"><path d="M60 150 H455"/><path d="M66 158 H448"/></g>
        <g class="unit__led"><circle cx="452" cy="52" r="4"/></g>
        <g class="unit__edge"><path d="M20 28 H500"/></g>
      </svg>
      <div class="unit__air"><span></span><span></span><span></span><span></span><span></span></div>
    </div>
  </div>

  <a class="scrollcue" href="#promise" aria-label="Scroll down"><span></span></a>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee__track">{brands}{brands}</div>
</div>

<section class="section" id="promise">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow eyebrow--dark" data-reveal>Why ACDC</p>
      <h2 class="heading split" data-split>A complete solution; from consult to design to installation.</h2>
    </header>

    <div class="grid grid--3">
      <article class="pillar" data-reveal data-tilt>
        <span class="pillar__mark" aria-hidden="true"></span>
        <h3>Fast Reliable Service</h3>
        <p>When the system stops, the call gets answered and the job gets booked.</p>
      </article>
      <article class="pillar" data-reveal data-delay="90" data-tilt>
        <span class="pillar__mark pillar__mark--warm" aria-hidden="true"></span>
        <h3>Service and Installation</h3>
        <p>Highly trained and experts in HVAC service and replacements.</p>
      </article>
      <article class="pillar" data-reveal data-delay="180" data-tilt>
        <span class="pillar__mark" aria-hidden="true"></span>
        <h3>Honest and Fair</h3>
        <p>Thorough, informative, and knowledgeable.</p>
      </article>
    </div>

    <div class="counterline" data-reveal>
      <b class="counter" data-to="20" data-suffix="+">0</b>
      <span>years of experience across Perth</span>
    </div>
  </div>
</section>

<section class="section section--fog">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow eyebrow--dark" data-reveal>What we do</p>
      <h2 class="heading split" data-split>Six ways we keep Perth comfortable.</h2>
    </header>
    <div class="grid grid--3">
{tiles}
    </div>
  </div>
</section>

<section class="section">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow eyebrow--dark" data-reveal>Reviews</p>
      <h2 class="heading split" data-split>What our customers say.</h2>
    </header>
    <div class="grid grid--3">
      <blockquote class="quote quote--empty" data-reveal data-tilt><p class="todo">[Google review to be added]</p></blockquote>
      <blockquote class="quote quote--empty" data-reveal data-delay="90" data-tilt><p class="todo">[Google review to be added]</p></blockquote>
      <blockquote class="quote quote--empty" data-reveal data-delay="180" data-tilt><p class="todo">[Google review to be added]</p></blockquote>
    </div>
    <p class="centered" data-reveal data-delay="240">
      <a class="btn btn--ghost-dark" href="[Google reviews URL to be supplied]" data-magnetic>See our Google reviews <span class="chev">&rsaquo;</span></a>
    </p>
  </div>
</section>

<section class="cta" id="quote-band">
  <div class="lane cta__inner">
    <div class="cta__copy">
      <p class="eyebrow" data-reveal>Free quote</p>
      <h2 class="heading split" data-split>Tell us about the space. We&rsquo;ll size the system.</h2>
      <p data-reveal data-delay="200">
        Installations, repairs, services and maintenance for residential, commercial and industrial
        clients throughout Perth. Call <a href="{TEL_MOB_HREF}">{TEL_MOB_TEXT}</a> or send the form.
      </p>
    </div>
    {quote_form()}
  </div>
</section>
"""


def page_about():
    brands = "".join(f"<li>{b}</li>" for b in BRANDS[:6])
    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>About</p>
    <h1 class="display split" data-split>ACDC aims to keep you comfortable all year round.</h1>
  </div>
</section>

<section class="section">
  <div class="lane prose">
    <p class="lede" data-reveal>
      ACDC offers its clients the best solutions for all their air conditioning needs, ensuring it
      delivers the most energy efficient results across Perth.
    </p>
    <p data-reveal data-delay="120">
      Installations, repairs, services and maintenance for residential, commercial and industrial
      clients throughout Perth.
    </p>
    <p data-reveal data-delay="200">
      With over 20 years of experience, we&rsquo;re the right choice to take care of your air
      conditioning requirements &mdash; a complete solution; from consult to design to installation.
    </p>
  </div>
</section>

<section class="section section--fog">
  <div class="lane split-cols">
    <div>
      <h2 class="heading split" data-split>Aligned with the brands that hold up.</h2>
      <p data-reveal data-delay="160">
        ACDC is aligned with Actron Air, Daikin, Fujitsu, LG, Mitsubishi and Samsung to provide
        solutions suited to every budget.
      </p>
    </div>
    <ul class="brandlist" data-reveal data-delay="200">{brands}</ul>
  </div>
</section>

<section class="section">
  <div class="lane split-cols split-cols--tight">
    <figure class="owner" data-reveal>
      <div class="owner__photo todo">[Photo of Daniel to be supplied]</div>
      <figcaption>
        <b>Daniel [surname to be confirmed]</b>
        <span>Owner &middot; ACDC Air Conditioning</span>
      </figcaption>
    </figure>
    <div>
      <h2 class="heading split" data-split>Run by the person who does the work.</h2>
      <p data-reveal data-delay="160">
        Based in Innaloo, serving the Perth Metropolitan Area. Straight answers on what a system
        will cost, what it will do, and what it will not do.
      </p>
      <p class="todo" data-reveal data-delay="220">[AU / ARC licence number to be supplied] &middot; [ABN to be supplied]</p>
      <p data-reveal data-delay="280"><a class="btn btn--blue" href="contact.html#quote" data-magnetic>Get a free quote</a></p>
    </div>
  </div>
</section>
"""


def page_services():
    systems = [
        ("Split systems", "One outdoor unit to one or more indoor heads. The common choice for a room, an extension or a unit."),
        ("Ducted", "Conditioned air distributed through the ceiling to every room, with zoning where it makes sense."),
        ("Refrigerated", "Refrigerated cooling and reverse-cycle heating that holds temperature through a Perth summer."),
    ]
    sys_html = "\n".join(
        f"""      <article class="card" data-reveal data-delay="{i * 90}" data-tilt>
        <h3 class="card__name">{n}</h3>
        <p class="card__desc">{d}</p>
      </article>"""
        for i, (n, d) in enumerate(systems)
    )

    def service(anchor, eyebrow, title, lead, bullets, icon, warm=False):
        items = "".join(f"<li>{b}</li>" for b in bullets)
        return f"""<section class="section{' section--fog' if warm else ''}" id="{anchor}">
  <div class="lane split-cols">
    <div>
      <svg class="serviceicon" viewBox="0 0 64 64" aria-hidden="true" data-reveal>{icon}</svg>
      <p class="eyebrow eyebrow--dark" data-reveal>{eyebrow}</p>
      <h2 class="heading split" data-split>{title}</h2>
      <p data-reveal data-delay="160">{lead}</p>
      <p data-reveal data-delay="240"><a class="btn btn--blue" href="contact.html#quote" data-magnetic>Get a quote</a></p>
    </div>
    <ul class="ticks" data-reveal data-delay="200">{items}</ul>
  </div>
</section>"""

    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>Services</p>
    <h1 class="display split" data-split>Air conditioning, ventilation and maintenance across Perth.</h1>
  </div>
</section>

{service(
    "air-conditioning", "Air conditioning",
    "A renowned air con specialist serving Perth and all its surrounding suburbs.",
    "ACDC is a renowned air con specialist serving Perth and all its surrounding suburbs. "
    "Installation, maintenance and repair of refrigerated units, split systems and ducted air conditioning.",
    ["Installation of refrigerated units", "Split system supply and install",
     "Ducted air conditioning", "Maintenance and repair", "Residential, commercial and industrial"],
    '<rect x="8" y="16" width="34" height="16" rx="3"/><path d="M50 24h8M54 18v12" class="dash"/>'
    '<path d="M14 40q10 8 20 0" class="dash"/>',
)}

{service(
    "ventilation", "Mechanical ventilation",
    "Ventilation designed for the space it has to clear.",
    "Design and installation of mechanical ventilation systems for buildings that need air moved, "
    "not just cooled.",
    ["Car park ventilation", "Wet area ventilation", "Toilet exhaust",
     "Kitchen range hood", "Dust and fume extraction", "Warehouse ventilation"],
    '<circle cx="32" cy="32" r="16"/><path d="M32 16v32M16 32h32" class="dash"/>'
    '<circle cx="32" cy="32" r="4"/>',
    warm=True,
)}

{service(
    "maintenance", "Maintenance",
    "Preventative maintenance beats an emergency call-out.",
    "Preventative maintenance programs tailored to your equipment, to avoid breakdowns and "
    "optimise efficiency.",
    ["Programs matched to your equipment", "Scheduled servicing",
     "Fewer breakdowns", "Efficiency kept where it should be"],
    '<path d="M40 14a10 10 0 0 0-13 13L14 40a4 4 0 0 0 6 6l13-13a10 10 0 0 0 13-13l-7 7-6-6z"/>'
    '<path d="M18 44h2" class="dash"/>',
)}

<section class="section section--fog" id="systems">
  <div class="lane">
    <header class="sechead">
      <p class="eyebrow eyebrow--dark" data-reveal>System types</p>
      <h2 class="heading split" data-split>Three ways to condition a building.</h2>
    </header>
    <div class="grid grid--3">
{sys_html}
    </div>
  </div>
</section>
"""


def page_gallery():
    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>Gallery</p>
    <h1 class="display split" data-split>Work completed across the Perth metro area.</h1>
  </div>
</section>

<section class="section">
  <div class="lane">
    <div class="tiles" id="gallery">
{gallery_tiles()}
    </div>
    <p class="note" data-reveal>
      Images are pulled from the existing ACDC site. Run
      <code>bash public/images/fetch-assets.sh</code> to download them into <code>public/images/</code>.
    </p>
  </div>
</section>

<div class="lightbox" id="lightbox" hidden>
  <button class="lightbox__close" id="lbClose" aria-label="Close">&times;</button>
  <button class="lightbox__nav lightbox__nav--prev" id="lbPrev" aria-label="Previous">&lsaquo;</button>
  <img id="lbImg" src="" alt="">
  <button class="lightbox__nav lightbox__nav--next" id="lbNext" aria-label="Next">&rsaquo;</button>
</div>
"""


def page_contact():
    return f"""<section class="pagehead">
  <div class="lane">
    <p class="eyebrow" data-reveal>Contact</p>
    <h1 class="display split" data-split>Call, or tell us what the job is.</h1>
  </div>
</section>

<section class="section">
  <div class="lane split-cols">
    <div class="contactinfo">
      <dl>
        <div data-reveal><dt>Phone</dt><dd><a href="{TEL_LAND_HREF}">{TEL_LAND_TEXT}</a></dd></div>
        <div data-reveal data-delay="70"><dt>Mobile</dt><dd><a href="{TEL_MOB_HREF}">{TEL_MOB_TEXT}</a></dd></div>
        <div data-reveal data-delay="140"><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div data-reveal data-delay="210"><dt>Service area</dt><dd>Perth Metropolitan Area, WA &mdash; based in Innaloo</dd></div>
        <div data-reveal data-delay="280"><dt>Trading hours</dt><dd class="todo">[to be supplied]</dd></div>
        <div data-reveal data-delay="350"><dt>Licence / ABN</dt><dd class="todo">[AU / ARC licence and ABN to be supplied]</dd></div>
      </dl>
    </div>

    <div class="mapwrap" data-reveal data-delay="150">
      <iframe
        title="ACDC Air Conditioning service area, Perth"
        src="https://www.google.com/maps?q=-31.962367,115.900795&hl=en&z=12&output=embed"
        loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>

<section class="cta">
  <div class="lane cta__inner">
    <div class="cta__copy">
      <p class="eyebrow" data-reveal>Free quote</p>
      <h2 class="heading split" data-split>Every enquiry gets a real answer.</h2>
      <p data-reveal data-delay="200">
        Installation, repair, maintenance, ventilation or a commercial site &mdash; tell us which,
        and we will come back to you.
      </p>
    </div>
    {quote_form()}
  </div>
</section>
"""


PAGES = [
    ("index.html",
     "Air Conditioning Perth | ACDC Air Conditioning, Innaloo",
     "Fast and reliable heating and air conditioning service across the Perth Metropolitan Area. Split system installation, ducted air conditioning, repairs and maintenance. Over 20 years of experience.",
     page_home),
    ("about.html",
     "About ACDC Air Conditioning | Perth HVAC Specialists",
     "ACDC aims to keep you comfortable all year round, delivering the most energy efficient air conditioning results across Perth for residential, commercial and industrial clients.",
     page_about),
    ("services.html",
     "Split System &amp; Ducted Air Conditioning Perth | ACDC Services",
     "Split system installation Perth, ducted air conditioning, mechanical ventilation and preventative maintenance for homes and businesses across the Perth Metropolitan Area.",
     page_services),
    ("gallery.html",
     "Our Work | Air Conditioning Installations Perth | ACDC",
     "Split system and ducted air conditioning installations completed by ACDC across Perth and its surrounding suburbs.",
     page_gallery),
    ("contact.html",
     "Contact ACDC Air Conditioning | Free Quote, Perth &amp; Innaloo",
     "Call ACDC Air Conditioning on 0432 230 757 or request a free quote for air conditioning installation, repair or maintenance anywhere in the Perth Metropolitan Area.",
     page_contact),
]


def main():
    for filename, title, description, builder in PAGES:
        html = head(filename, title, description) + builder() + FOOTER
        (ROOT / filename).write_text(html, encoding="utf-8")
        print("wrote", filename)


if __name__ == "__main__":
    main()
