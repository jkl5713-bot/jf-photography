#!/usr/bin/env python3
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = "https://jkl5713-bot.github.io/jf-photography"

IMG_META = json.load(open(os.path.join(ROOT, "assets", "img", "images.json")))

# collection numbering is canon — keep stable (matches tools/galleries.json)
PAGE_META = {
    "seniors.html":  {"num": "N° 01", "banner": "senior-portrait-golden-hour-backlit",
                      "next": ("couples.html", "N° 02 · Couples", "couple-park-portrait-petal-ms")},
    "couples.html":  {"num": "N° 02", "banner": "couple-park-portrait-petal-ms",
                      "next": ("weddings.html", "N° 03 · Weddings", "bride-groom-portrait-petal-ms")},
    "weddings.html": {"num": "N° 03", "banner": "bride-groom-portrait-petal-ms",
                      "next": ("sports.html", "N° 04 · Sports", "college-football-quarterback-friday-night")},
    "sports.html":   {"num": "N° 04", "banner": "college-tennis-forehand-jones-college",
                      "next": ("aerial.html", "N° 05 · Aerial", "aerial-st-moritz-dawn-alps")},
    "aerial.html":   {"num": "N° 05", "banner": None,
                      "next": ("seniors.html", "N° 01 · Seniors", "senior-session-strawberry-farm-laugh")},
    "about.html":    {"banner": "marching-band-golden-hour"},
}


def _srcsets(slug):
    m = IMG_META[slug]
    base = f"assets/img/{m['category']}/{slug}"
    avif = ", ".join(f"{base}-{tw}.avif {tw}w" for tw in m["widths"])
    jpg = ", ".join(f"{base}-{tw}.jpg {tw}w" for tw in m["widths"])
    return m, base, avif, jpg


def preload_link(slug):
    """LCP preload for the page's banner image (AVIF branch always matches)."""
    _, _, avif, _ = _srcsets(slug)
    return f'<link rel="preload" as="image" type="image/avif" imagesrcset="{avif}" imagesizes="100vw">'


def next_col(href, label, slug):
    m, base, avif, jpg = _srcsets(slug)
    big = m["widths"][0]
    sizes = "100vw"
    return f'''  <a class="next-col" href="{href}">
    <picture>
      <source type="image/avif" srcset="{avif}" sizes="{sizes}">
      <img src="{base}-{big}.jpg" srcset="{jpg}" sizes="{sizes}"
        width="{m['w']}" height="{m['h']}" loading="lazy" decoding="async" alt="">
    </picture>
    <div class="next-col__text">
      <p class="eyebrow">Next collection</p>
      <h2>{label} <span class="arrow">&rarr;</span></h2>
    </div>
  </a>
'''

NAV_ITEMS = [("seniors.html", "Seniors"), ("couples.html", "Couples"),
             ("weddings.html", "Weddings"), ("sports.html", "Sports"),
             ("aerial.html", "Aerial"), ("about.html", "About"),
             ("pricing.html", "Pricing"), ("inquire.html", "Inquire")]


def head(title, desc, fname=""):
    page_url = f"{BASE}/{fname}" if fname else f"{BASE}/"
    pm = PAGE_META.get(fname, {})
    extra_preload = f"\n{preload_link(pm['banner'])}" if pm.get("banner") else ""
    if fname == "aerial.html":
        extra_preload = '\n<link rel="preload" as="image" href="assets/video/aerial-loop-poster.jpg">'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#060f1b">
<link rel="canonical" href="{page_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{BASE}/assets/img/hero/golden-hour-tennis-serve-ellisville-ms-1200.jpg">
<link rel="icon" href="assets/brand/favicon.png">
<link rel="apple-touch-icon" href="assets/brand/favicon.png">
<link rel="preload" href="assets/fonts/fraunces-3.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/CabinetGrotesk-Variable.woff2" as="font" type="font/woff2" crossorigin>{extra_preload}
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/main.css">
<script src="js/main.js" defer></script>
<script src="js/gallery.js" defer></script>
</head>
<body>
'''


def nav(current):
    CUR = ' aria-current="page"'
    lis = "\n".join(
        f'      <li><a href="{href}"{CUR if href == current else ""}>{label}</a></li>'
        for href, label in NAV_ITEMS)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <a class="nav__logo" href="index.html" aria-label="JF — home">
    <img src="assets/brand/jf-white.png" alt="JF monogram — Juan Flores Photo &amp; Film">
  </a>
  <nav aria-label="Primary">
    <ul class="nav__links">
{lis}
    </ul>
  </nav>
  <button class="nav__toggle" aria-expanded="false">Menu</button>
</header>
'''


FOOTER = '''<footer class="footer">
  <div class="wrap">
    <div class="footer__cta">
      <p class="eyebrow" style="justify-content:center">Ready when you are</p>
      <h2 class="reveal">Let's make something <em>worth keeping</em>.</h2>
      <p class="mt-2"><a class="btn btn--solid" href="inquire.html">Check my date <span class="arrow">&rarr;</span></a></p>
    </div>
    <div class="footer__grid">
      <img src="assets/brand/jf-white.png" alt="JF monogram">
      <p>Serving Hattiesburg · Laurel · Ellisville<br>the Gulf South &amp; anywhere the story goes</p>
      <div class="footer__links">
        <a class="link-line" href="https://www.instagram.com/j.f.official" target="_blank" rel="noopener">Instagram</a>
        <a class="link-line" href="mailto:jkl81694@gmail.com">Email</a>
        <a class="link-line" href="pricing.html">Pricing</a>
        <a class="link-line" href="inquire.html">Inquire</a>
      </div>
      <p>© <span data-year>2026</span> Juan Flores Photo &amp; Film</p>
    </div>
  </div>
</footer>

<div class="grain" aria-hidden="true"></div>
</body>
</html>
'''


def gallery_page(fname, title, desc, banner_id, eyebrow, h1, lede, gallery_id, extra="", pre_gallery=""):
    pm = PAGE_META.get(fname, {})
    num = f'<span class="num">{pm["num"]}</span> ' if pm.get("num") else ""
    ramp = next_col(*pm["next"]) if pm.get("next") else ""
    body = f'''<main id="main">
  <section class="banner parallax">
    <!-- GALLERY:{banner_id} -->
    <!-- /GALLERY:{banner_id} -->
  </section>
  <div class="wrap" style="padding-block:clamp(2.5rem,6vh,4rem)">
    <p class="eyebrow reveal">{num}{eyebrow}</p>
    <h1 class="reveal" style="font-size:var(--text-2xl);max-width:16ch">{h1}</h1>
    <p class="lede dim reveal mt-2" style="--d:.15s;font-size:var(--text-lg);max-width:48ch">{lede}</p>
  </div>
{pre_gallery}  <section id="frames" class="wrap" style="padding-bottom:var(--section)">
    <div class="masonry" data-lightbox>
      <!-- GALLERY:{gallery_id} -->
      <!-- /GALLERY:{gallery_id} -->
    </div>
  </section>
{extra}{ramp}</main>
'''
    html = head(title, desc, fname) + "\n" + nav(fname) + "\n" + body + "\n" + FOOTER
    open(os.path.join(ROOT, fname), "w").write(html)
    print("wrote", fname)


# ---------------- gallery pages ----------------
gallery_page(
    "seniors.html",
    "Senior Portraits in Hattiesburg &amp; Laurel, MS | Juan Flores Photo &amp; Film",
    "Editorial senior portrait sessions across Hattiesburg, Laurel and Ellisville, Mississippi — golden-hour light, real locations, gallery in weeks.",
    "banner-seniors", "Seniors &amp; grads",
    "Your year. <em>Your light.</em>",
    "This is the year everything changes — your session should feel like it. We plan looks and locations around you, chase the best hour of light, and build a gallery that looks like a magazine, not a yearbook.",
    "seniors",
    extra='''  <section class="section wrap">
    <p class="eyebrow reveal">How it works</p>
    <div class="process">
      <div class="step reveal"><span class="n">01</span><h3>Plan the look</h3><p>We talk outfits, locations and the vibe you want — campus, farm, downtown, water. You bring you; I bring the plan.</p></div>
      <div class="step reveal" style="--d:.1s"><span class="n">02</span><h3>Chase the light</h3><p>Sessions are scheduled around golden hour. Relaxed direction the whole way — nobody's a model until suddenly you are.</p></div>
      <div class="step reveal" style="--d:.2s"><span class="n">03</span><h3>Your gallery</h3><p>Fully edited images delivered in an online gallery, ready for prints, announcements and the group chat.</p></div>
    </div>
  </section>
''')

gallery_page(
    "couples.html",
    "Couples &amp; Engagement Photographer — Hattiesburg, MS | Juan Flores",
    "Couples and engagement photography in Hattiesburg, Laurel and Ellisville, Mississippi — honest, golden-hour storytelling for two.",
    "banner-couples", "Couples",
    "Two people, <em>zero posing</em>.",
    "Engagements, anniversaries, or no reason at all. I'll put you somewhere beautiful at the right hour and keep you moving, laughing and close — the frames take care of themselves.",
    "couples",
    extra='''  <section class="section wrap center">
    <p class="dim reveal" style="margin-inline:auto">This collection is growing fast — more sessions land here after every weekend.<br>Want yours in it?</p>
    <p class="mt-2 reveal"><a class="btn" href="inquire.html">Book a couples session <span class="arrow">&rarr;</span></a></p>
  </section>
''')

gallery_page(
    "weddings.html",
    "Wedding Photographer &amp; Videographer in Hattiesburg, MS | Juan Flores",
    "Wedding photography and cinematic highlight films across Hattiesburg, Laurel, Ellisville and Petal, Mississippi — one shooter, photo and film.",
    "banner-weddings", "Weddings &amp; films",
    "Told honestly, <em>kept forever</em>.",
    "One storyteller for photo and film means nobody misses the moment — the shoe game, the ugly-cry toast, your grandmother's hands during the prayer. Highlight film in 16:9 plus a vertical cut ready for the group chat.",
    "weddings",
    extra='''  <section class="section ivory">
    <div class="wrap">
      <p class="eyebrow reveal">The film</p>
      <h2 class="reveal" style="font-size:var(--text-xl);max-width:26ch">Every collection includes a cinematic <em>highlight film</em> — and a vertical cut for the feed.</h2>
      <p class="mt-2 reveal" style="--d:.1s">Up to six continuous hours of coverage, one round of revisions, delivered digitally in three to four weeks. Add-ons: extended coverage, a full start-to-finish ceremony film, or the raw footage.</p>
      <!-- WATCH-THE-FILM: upload your best highlight film to YouTube (unlisted is fine),
           then uncomment and set data-yt to the video id. The player only loads on click.
      <div class="film-embed reveal mt-4" data-yt="VIDEO_ID" role="button" tabindex="0" aria-label="Play the highlight film">
        <img src="assets/video/aerial-loop-poster.jpg" alt="" loading="lazy" decoding="async">
        <span class="film-embed__play">Play the film</span>
      </div>
      -->
      <p class="mt-2 reveal" style="--d:.2s"><a class="btn" href="pricing.html">See wedding collections <span class="arrow">&rarr;</span></a></p>
    </div>
  </section>
''')

gallery_page(
    "sports.html",
    "Sports Photographer — Ellisville &amp; Hattiesburg, MS | Juan Flores",
    "College and individual sports photography in Ellisville and Hattiesburg, Mississippi — game coverage, athlete sessions and season media for programs and families.",
    "banner-sports", "Sports",
    "Peak action, <em>every time</em>.",
    "I shoot media for Jones College Athletics — football under the lights, soccer at dusk, tennis at golden hour. Programs get season coverage; athletes and parents get the frame that makes the season real.",
    "sports",
    pre_gallery='''  <section class="wrap" style="padding-bottom:clamp(2rem,5vh,3.5rem)">
    <p class="eyebrow reveal">Recent coverage</p>
    <ol class="ledger">
      <li class="reveal"><span class="ledger__date">Spring ’26</span><span class="ledger__event">Jones College Tennis — six match days, championship banners up</span><a class="link-line" href="#frames">View frames</a></li>
      <li class="reveal" style="--d:.05s"><span class="ledger__date">Oct ’24</span><span class="ledger__event">Jones College Homecoming — parade &amp; stadium aerials</span><a class="link-line" href="aerial.html">Aerial set</a></li>
      <li class="reveal" style="--d:.1s"><span class="ledger__date">Fall ’24</span><span class="ledger__event">Bobcats Football — three game days under the lights</span><a class="link-line" href="#frames">View frames</a></li>
      <li class="reveal" style="--d:.15s"><span class="ledger__date">Fall ’24</span><span class="ledger__event">Bobcats Women’s Soccer — five match days</span><a class="link-line" href="#frames">View frames</a></li>
    </ol>
  </section>
''',
    extra='''  <section class="section wrap">
    <p class="eyebrow reveal">For athletes &amp; programs</p>
    <div class="tiers">
      <div class="tier reveal"><h3>Game coverage</h3><p class="price">from $125 <small>PER GAME</small></p><ul><li>Full-game shooting, peak action + sidelines</li><li>Fast social-ready selects</li><li>Team gallery delivery</li></ul><a class="btn" href="inquire.html">Inquire</a></div>
      <div class="tier reveal" style="--d:.1s"><h3>Athlete sessions</h3><p class="price">from $150 <small>PER ATHLETE</small></p><ul><li>Individual portraits in uniform, stadium or court</li><li>Banner &amp; signing-day graphics ready</li><li>Recruiting-profile friendly</li></ul><a class="btn" href="inquire.html">Inquire</a></div>
      <div class="tier reveal" style="--d:.2s"><h3>Season media</h3><p class="price">custom <small>MULTI-GAME</small></p><ul><li>Multi-game packages for programs</li><li>Photo + video + drone in one crew</li><li>Consistent look all season</li></ul><a class="btn" href="inquire.html">Inquire</a></div>
    </div>
  </section>
''')

# ---------------- aerial (custom hero) ----------------
aerial = head(
    "Drone Photography &amp; Video — Hattiesburg &amp; Laurel, MS | Juan Flores",
    "FAA Part 107 certified drone photography and cinematic 4K aerial video in Hattiesburg, Laurel and Ellisville, Mississippi — venues, land, events, sports facilities and real estate.",
    "aerial.html"
) + "\n" + nav("aerial.html") + '''
<main id="main">
  <section class="video-hero">
    <video muted loop playsinline preload="none"
      poster="assets/video/aerial-loop-poster.jpg"
      data-lazy="assets/video/aerial-loop.mp4" aria-hidden="true"></video>
    <div class="wrap" style="padding-block:clamp(3rem,8vh,6rem)">
      <p class="eyebrow reveal"><span class="num">N° 05</span> Aerial — photo &amp; film</p>
      <h1 class="reveal" style="font-size:var(--text-2xl);max-width:14ch">Above <em>everything</em>.</h1>
      <p class="lede dim reveal mt-2" style="--d:.15s;font-size:var(--text-lg);max-width:46ch">Cinematic aerials for venues, land and farms, events, sports facilities and real estate — from Mississippi main streets to the Swiss Alps.</p>
      <div class="badges mt-2 reveal" style="--d:.25s">
        <span class="badge gold">FAA Part 107 certified remote pilot</span>
        <span class="badge">DJI Mini 4 Pro · 4K HDR</span>
        <span class="badge">Controlled airspace via LAANC</span>
      </div>
    </div>
  </section>
  <section class="section wrap">
    <div class="masonry" data-lightbox>
      <!-- GALLERY:aerial -->
      <!-- /GALLERY:aerial -->
    </div>
  </section>
  <section class="wrap" style="padding-bottom:var(--section)">
    <p class="eyebrow reveal">Where a drone earns its keep</p>
    <div class="tiers">
      <div class="tier reveal"><h3>Venues &amp; events</h3><p class="price">from $200 <small>PER EVENT</small></p><ul><li>Wedding venues at dusk — add-on from $200</li><li>Festivals, parades, game days</li><li>Establishing shots for films</li></ul><a class="btn" href="inquire.html">Inquire</a></div>
      <div class="tier reveal" style="--d:.1s"><h3>Land &amp; property</h3><p class="price">from $125 <small>PER LISTING</small></p><ul><li>Real-estate listings from $125</li><li>Farms, acreage and timberland from $150</li><li>Construction progress</li></ul><a class="btn" href="inquire.html">Inquire</a></div>
      <div class="tier reveal" style="--d:.2s"><h3>Sports facilities</h3><p class="price">custom <small>PROGRAMS</small></p><ul><li>Stadium and complex flyovers</li><li>Hype-video aerials</li><li>Program media add-on</li></ul><a class="btn" href="inquire.html">Inquire</a></div>
    </div>
  </section>
''' + next_col(*PAGE_META["aerial.html"]["next"]) + '''</main>
''' + FOOTER
open(os.path.join(ROOT, "aerial.html"), "w").write(aerial)
print("wrote aerial.html")

# ---------------- about ----------------
about = head(
    "About Juan Flores — Photographer &amp; Videographer, Hattiesburg MS",
    "Juan Flores is a South Mississippi photographer and videographer shooting seniors, couples, weddings, sports and aerial — raised on a farm, at home everywhere.",
    "about.html"
) + "\n" + nav("about.html") + '''
<main id="main">
  <section class="banner parallax">
    <!-- GALLERY:banner-about -->
    <!-- /GALLERY:banner-about -->
  </section>
  <div class="wrap" style="padding-block:clamp(2.5rem,6vh,4rem)">
    <p class="eyebrow reveal">About</p>
    <h1 class="reveal" style="font-size:var(--text-2xl);max-width:16ch">Farm-raised. <em>Light-obsessed.</em></h1>
  </div>
  <section class="wrap" style="max-width:900px;margin-inline:auto;padding-bottom:var(--section)">
    <p class="reveal" style="font-size:var(--text-lg)">I'm Juan — a photographer and videographer from South Mississippi, raised on a working farm, studying at Southern Miss, and shooting media for Jones College Athletics.</p>
    <p class="dim mt-2 reveal">Since 2021 the camera has taken me from Friday-night sidelines in Ellisville to rooftops in Rome, strawberry fields in California and frozen mornings over the Alps. What I brought home is one conviction: the best photos happen when people forget the camera is there.</p>
    <p class="dim mt-2 reveal">So that's the job. I show up early, find the light, keep it easy, and stay on the moment — whether that's a bride's grandfather tearing up, a match point at golden hour, or your dog refusing to look at the lens. Photo and video, ground and air, one person who cares how your story is kept.</p>
    <div class="badges mt-4 reveal">
      <span class="badge gold">Jones College Athletics media</span>
      <span class="badge">FAA Part 107 certified pilot</span>
      <span class="badge">Weekends — booked by retainer</span>
      <span class="badge">Gulf South &amp; travel</span>
    </div>
    <p class="eyebrow reveal" style="margin-top:4rem">The kit</p>
    <p class="dim reveal">Sony A7 III full-frame for stills and film · DJI RS 4 Pro gimbal for cinema-smooth movement · DJI Mini 4 Pro for 4K HDR aerials. Small enough to move fast, sharp enough for a billboard.</p>
  </section>
  <section class="section strip-stage">
    <div class="wrap"><p class="eyebrow reveal">Off the clock, still shooting</p></div>
    <div class="strip" data-lightbox>
      <div class="strip__track">
        <!-- GALLERY:about-strip -->
        <!-- /GALLERY:about-strip -->
      </div>
    </div>
  </section>
</main>
''' + FOOTER
open(os.path.join(ROOT, "about.html"), "w").write(about)
print("wrote about.html")

# ---------------- pricing ----------------
pricing = head(
    "Pricing — Photography &amp; Film Collections | Juan Flores, Hattiesburg MS",
    "Transparent starting prices for senior sessions, couples, weddings, sports and drone work in Hattiesburg, Laurel and Ellisville, Mississippi.",
    "pricing.html"
) + "\n" + nav("pricing.html") + '''
<main id="main">
  <div class="wrap page-hero">
    <p class="eyebrow reveal">Pricing</p>
    <h1 class="reveal">Priced like a person, <em>not a package machine</em>.</h1>
    <p class="lede reveal" style="--d:.15s">Every booking gets the same eye, the same care and the same turnaround promise. Here's where things start — your exact quote comes after we talk, and it never changes after we shake on it.</p>
    <p class="avail reveal" style="--d:.25s"><span class="avail__dot" aria-hidden="true"></span><span data-avail></span></p>
    <span class="assure reveal" style="--d:.3s">Retainer fully refundable until 3 days out · one free date change</span>
  </div>

  <section class="section wrap">
    <p class="eyebrow reveal">Collections</p>
    <!-- PRICING: researched 2026 small-market MS rates (local comps: Hattiesburg/Petal
         photographers, Droners.io MS/AL/LA listings). Film package = signed contract terms. -->
    <div class="tiers">
      <div class="tier reveal">
        <h3>The Highlight Film</h3>
        <p class="price">$700 <small>WEDDING FILM</small></p>
        <p class="reframe">Hold your date for $250 — refundable</p>
        <ul>
          <li>Up to 6 continuous hours of coverage</li>
          <li>Cinematic 16:9 highlight film</li>
          <li>Vertical 9:16 cut for social</li>
          <li>One revision round · delivered in 3–4 weeks</li>
        </ul>
        <a class="btn" href="inquire.html">Check my date</a>
      </div>
      <div class="tier tier--featured reveal" style="--d:.1s">
        <span class="tier__badge">Most booked</span>
        <h3>Wedding photography</h3>
        <p class="price">from $1,100 <small>PHOTO + FILM $1,600 — BEST VALUE</small></p>
        <p class="reframe">Hold your date for $250 — refundable</p>
        <ul>
          <li>Six hours of wedding-day photography</li>
          <li>Fully edited online gallery with print rights</li>
          <li>Add the Highlight Film for $500 — one storyteller, both crafts</li>
          <li>Aerial coverage add-on from $200</li>
        </ul>
        <a class="btn btn--solid" href="inquire.html">Check my date</a>
      </div>
      <div class="tier reveal" style="--d:.2s">
        <h3>Portrait sessions</h3>
        <p class="price">from $250 <small>SENIORS · COUPLES · GRADS</small></p>
        <ul>
          <li>60–90 minute golden-hour session</li>
          <li>Locations planned together — no stiff posing</li>
          <li>Fully edited online gallery</li>
          <li>Print &amp; share rights included</li>
        </ul>
        <a class="btn" href="inquire.html">Inquire</a>
      </div>
      <div class="tier reveal" style="--d:.3s">
        <h3>Sports &amp; aerial</h3>
        <p class="price">from $125 <small>GAMES · ATHLETES · FLIGHTS</small></p>
        <ul>
          <li>Athlete banner sessions from $150</li>
          <li>Program game coverage from $125 per game</li>
          <li>Real-estate aerials from $125 · land &amp; farms from $150</li>
          <li>Event &amp; venue flyovers from $200</li>
        </ul>
        <a class="btn" href="inquire.html">Inquire</a>
      </div>
    </div>
  </section>

  <section class="section ivory">
    <div class="wrap">
      <p class="eyebrow reveal">How booking works</p>
      <div class="process">
        <div class="step reveal"><span class="n">01</span><h3>Inquire</h3><p>Tell me your date and your story. I answer within 24 hours — weekends fill first, so earlier is better.</p></div>
        <div class="step reveal" style="--d:.1s"><span class="n">02</span><h3>Reserve</h3><p>A $250 refundable retainer locks weddings; sessions hold with a simple agreement. One free date change with 14+ days notice.</p></div>
        <div class="step reveal" style="--d:.2s"><span class="n">03</span><h3>Shoot &amp; deliver</h3><p>We make the thing. Your edited gallery or film lands in 3–4 weeks, delivered digitally, ready to keep forever.</p></div>
      </div>
    </div>
  </section>

  <section class="section wrap">
    <p class="eyebrow reveal">Fair questions</p>
    <div class="faq">
      <details class="reveal"><summary>Do you travel?</summary><p class="dim">Yes. Hattiesburg, Laurel and Ellisville are home turf with no travel fee. Beyond that, we'll sort simple mileage — and for the right story, I'll go anywhere. I've shot three countries and counting.</p></details>
      <details class="reveal"><summary>How far out should I book?</summary><p class="dim">Weddings: as soon as you have a date — I only take weekend bookings, so Saturdays go fast. Senior sessions: 3–4 weeks ahead usually works.</p></details>
      <details class="reveal"><summary>When do we get everything?</summary><p class="dim">Three to four weeks after your date, delivered digitally through an online gallery or download. Sneak selects usually land sooner.</p></details>
      <details class="reveal"><summary>What if we need to change the date?</summary><p class="dim">One free date change with at least 14 days written notice. The retainer is refundable except for cancellations within 3 days of the event.</p></details>
      <details class="reveal"><summary>Can you do photo AND video?</summary><p class="dim">That's the whole point of hiring one storyteller — photo, film and drone in a single booking, one consistent look, nobody tripping over each other at the ceremony.</p></details>
      <details class="reveal"><summary>How do we pay?</summary><p class="dim">Cash, check, Venmo, Zelle, Cash App, PayPal or Apple Pay. Retainer up front, balance due by the day of the event.</p></details>
    </div>
  </section>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type": "Question", "name": "Do you travel?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Hattiesburg, Laurel and Ellisville are home turf with no travel fee. Beyond that, simple mileage — and for the right story, anywhere."}},
      {"@type": "Question", "name": "How far out should I book?", "acceptedAnswer": {"@type": "Answer", "text": "Weddings: as soon as you have a date — weekend bookings only, so Saturdays go fast. Senior sessions: 3-4 weeks ahead usually works."}},
      {"@type": "Question", "name": "When do we get everything?", "acceptedAnswer": {"@type": "Answer", "text": "Three to four weeks after your date, delivered digitally through an online gallery or download. Sneak selects usually land sooner."}},
      {"@type": "Question", "name": "What if we need to change the date?", "acceptedAnswer": {"@type": "Answer", "text": "One free date change with at least 14 days written notice. The retainer is refundable except for cancellations within 3 days of the event."}},
      {"@type": "Question", "name": "Can you do photo AND video?", "acceptedAnswer": {"@type": "Answer", "text": "Yes — photo, film and drone in a single booking, one consistent look, one storyteller."}},
      {"@type": "Question", "name": "How do we pay?", "acceptedAnswer": {"@type": "Answer", "text": "Cash, check, Venmo, Zelle, Cash App, PayPal or Apple Pay. Retainer up front, balance due by the day of the event."}}
    ]
  }
  </script>
</main>
''' + FOOTER
open(os.path.join(ROOT, "pricing.html"), "w").write(pricing)
print("wrote pricing.html")

# old URL redirect: investment.html -> pricing.html
redirect = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pricing | Juan Flores Photo &amp; Film</title>
<meta http-equiv="refresh" content="0; url=pricing.html">
<link rel="canonical" href="''' + BASE + '''/pricing.html">
</head>
<body><p>This page moved to <a href="pricing.html">pricing.html</a>.</p></body>
</html>
'''
open(os.path.join(ROOT, "investment.html"), "w").write(redirect)
print("wrote investment.html (redirect)")

# ---------------- inquire ----------------
inquire = head(
    "Inquire — Check Your Date | Juan Flores Photo &amp; Film, Hattiesburg MS",
    "Check availability for senior sessions, couples, weddings, sports coverage and drone work in Hattiesburg, Laurel and Ellisville, Mississippi.",
    "inquire.html"
) + "\n" + nav("inquire.html") + '''
<main id="main">
  <div class="wrap page-hero">
    <p class="eyebrow reveal">Inquire</p>
    <h1 class="reveal">Tell me <em>your story</em>.</h1>
    <p class="lede reveal" style="--d:.15s">A few details and you're done — I read every one of these myself and answer within 24 hours.</p>
    <p class="avail reveal" style="--d:.25s"><span class="avail__dot" aria-hidden="true"></span><span data-avail></span></p>
  </div>
  <section class="wrap" style="padding-bottom:var(--section)">
    <form class="form reveal" action="https://formsubmit.co/jkl81694@gmail.com" method="POST">
      <input type="hidden" name="_subject" value="New inquiry — jf photo &amp; film website">
      <input type="hidden" name="_next" value="https://jkl5713-bot.github.io/jf-photography/thanks.html">
      <input type="hidden" name="_autoresponse" value="Got it — your inquiry is in my inbox. I read every one of these myself and I'll reply within 24 hours, usually much faster. If your date is flexible, say so in your reply and I'll send options. — Juan, JF Photo &amp; Film">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <div class="row">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" required autocomplete="name"></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="row">
        <div class="field"><label for="f-phone">Phone <span class="dim">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <fieldset class="field" style="border:0">
        <legend style="font-size:var(--text-xs);font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--paper-dim);margin-bottom:.6rem">What are we making?</legend>
        <div class="pills">
          <label><input type="radio" name="session_type" value="Senior session" required><span>Senior session</span></label>
          <label><input type="radio" name="session_type" value="Couples / engagement"><span>Couples</span></label>
          <label><input type="radio" name="session_type" value="Wedding — photo"><span>Wedding photo</span></label>
          <label><input type="radio" name="session_type" value="Wedding — film"><span>Wedding film</span></label>
          <label><input type="radio" name="session_type" value="Wedding — photo + film"><span>Photo + film</span></label>
          <label><input type="radio" name="session_type" value="Sports"><span>Sports</span></label>
          <label><input type="radio" name="session_type" value="Drone / aerial"><span>Aerial</span></label>
          <label><input type="radio" name="session_type" value="Something else"><span>Something else</span></label>
        </div>
      </fieldset>
      <div class="row">
        <div class="field"><label for="f-date">Date (or best guess)</label><input id="f-date" name="preferred_date" type="text" placeholder="e.g. Oct 17, 2026"></div>
        <div class="field"><label for="f-hear">How'd you find me? <span class="dim">(optional)</span></label><input id="f-hear" name="heard_from" type="text"></div>
      </div>
      <div class="field"><label for="f-msg">Your story</label><textarea id="f-msg" name="message" placeholder="Venue, team, vision, questions — everything helps." required></textarea></div>
      <div>
        <span class="assure" style="margin-bottom:1rem">Retainer fully refundable until 3 days out · one free date change</span>
        <button class="btn btn--solid" type="submit">Send it <span class="arrow">&rarr;</span></button>
        <p class="dim mt-2" style="font-size:var(--text-sm)">Replies within 24 hours — usually much faster. Prefer email? <a class="link-line" href="mailto:jkl81694@gmail.com">jkl81694@gmail.com</a> · or DM <a class="link-line" href="https://www.instagram.com/j.f.official" target="_blank" rel="noopener">@j.f.official</a></p>
      </div>
    </form>
  </section>
</main>
''' + FOOTER
open(os.path.join(ROOT, "inquire.html"), "w").write(inquire)
print("wrote inquire.html")

# ---------------- thanks ----------------
thanks = head(
    "Thank You | Juan Flores Photo &amp; Film",
    "Your inquiry is in — expect a reply within 24 hours.",
    "thanks.html"
) + "\n" + nav("") + '''
<main id="main">
  <div class="wrap page-hero" style="min-height:60svh">
    <p class="eyebrow reveal">Received</p>
    <h1 class="reveal">Got it. <em>Talk soon.</em></h1>
    <p class="lede reveal" style="--d:.15s">Your inquiry is in my inbox — expect a reply within 24 hours. In the meantime, the work is right this way.</p>
    <p class="mt-2 reveal" style="--d:.25s"><a class="btn" href="index.html#collections">Back to the collections <span class="arrow">&rarr;</span></a></p>
  </div>
</main>
''' + FOOTER
open(os.path.join(ROOT, "thanks.html"), "w").write(thanks)
print("wrote thanks.html")

# ---------------- 404 ----------------
notfound = head(
    "Page Not Found | Juan Flores Photo &amp; Film",
    "That page wandered out of frame.",
    "404.html"
) + "\n" + nav("") + '''
<main id="main">
  <div class="wrap page-hero" style="min-height:60svh">
    <p class="eyebrow reveal">404</p>
    <h1 class="reveal">Out of <em>frame</em>.</h1>
    <p class="lede reveal" style="--d:.15s">That page doesn't exist — but the good stuff is one click away.</p>
    <p class="mt-2 reveal" style="--d:.25s"><a class="btn btn--solid" href="index.html">Back to the work <span class="arrow">&rarr;</span></a></p>
  </div>
</main>
''' + FOOTER
open(os.path.join(ROOT, "404.html"), "w").write(notfound)
print("wrote 404.html")

print("all pages generated")
