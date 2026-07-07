#!/usr/bin/env python3
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = "https://jkl5713-bot.github.io/jf-photography"

NAV_ITEMS = [("seniors.html", "Seniors"), ("couples.html", "Couples"),
             ("weddings.html", "Weddings"), ("sports.html", "Sports"),
             ("aerial.html", "Aerial"), ("about.html", "About"),
             ("investment.html", "Investment"), ("inquire.html", "Inquire")]


def head(title, desc, fname=""):
    page_url = f"{BASE}/{fname}" if fname else f"{BASE}/"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{page_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{BASE}/assets/img/hero/golden-hour-tennis-serve-ellisville-ms-1200.jpg">
<link rel="icon" href="assets/brand/favicon.png">
<link rel="apple-touch-icon" href="assets/brand/favicon.png">
<link rel="preload" href="assets/fonts/fraunces-3.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/CabinetGrotesk-Variable.woff2" as="font" type="font/woff2" crossorigin>
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
    return f'''<header class="nav">
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
        <a class="link-line" href="investment.html">Investment</a>
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


def gallery_page(fname, title, desc, banner_id, eyebrow, h1, lede, gallery_id, extra=""):
    body = f'''<main id="main">
  <section class="banner parallax">
    <!-- GALLERY:{banner_id} -->
    <!-- /GALLERY:{banner_id} -->
  </section>
  <div class="wrap" style="padding-block:clamp(2.5rem,6vh,4rem)">
    <p class="eyebrow reveal">{eyebrow}</p>
    <h1 class="reveal" style="font-size:var(--text-2xl);max-width:16ch">{h1}</h1>
    <p class="lede dim reveal mt-2" style="--d:.15s;font-size:var(--text-lg);max-width:48ch">{lede}</p>
  </div>
  <section class="wrap" style="padding-bottom:var(--section)">
    <div class="masonry" data-lightbox>
      <!-- GALLERY:{gallery_id} -->
      <!-- /GALLERY:{gallery_id} -->
    </div>
  </section>
{extra}</main>
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
      <p class="mt-2 reveal" style="--d:.2s"><a class="btn" href="investment.html">See wedding collections <span class="arrow">&rarr;</span></a></p>
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
    <video autoplay muted loop playsinline preload="metadata"
      poster="assets/video/aerial-loop-poster.jpg"
      src="assets/video/aerial-loop.mp4" aria-hidden="true"></video>
    <div class="wrap" style="padding-block:clamp(3rem,8vh,6rem)">
      <p class="eyebrow reveal">Aerial — photo &amp; film</p>
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
</main>
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

# ---------------- investment ----------------
investment = head(
    "Investment — Photography &amp; Film Collections | Juan Flores, Hattiesburg MS",
    "Transparent starting prices for senior sessions, couples, weddings, sports and drone work in Hattiesburg, Laurel and Ellisville, Mississippi.",
    "investment.html"
) + "\n" + nav("investment.html") + '''
<main id="main">
  <div class="wrap page-hero">
    <p class="eyebrow reveal">Investment</p>
    <h1 class="reveal">Priced like a person, <em>not a package machine</em>.</h1>
    <p class="lede reveal" style="--d:.15s">Every booking gets the same eye, the same care and the same turnaround promise. Here's where things start — your exact quote comes after we talk, and it never changes after we shake on it.</p>
  </div>

  <section class="section wrap">
    <p class="eyebrow reveal">Collections</p>
    <!-- PRICING: researched 2026 small-market MS rates (local comps: Hattiesburg/Petal
         photographers, Droners.io MS/AL/LA listings). Film package = signed contract terms. -->
    <div class="tiers">
      <div class="tier reveal">
        <h3>The Highlight Film</h3>
        <p class="price">$500 <small>WEDDING FILM</small></p>
        <ul>
          <li>Up to 6 continuous hours of coverage</li>
          <li>Cinematic 16:9 highlight film</li>
          <li>Vertical 9:16 cut for social</li>
          <li>One revision round · delivered in 3–4 weeks</li>
          <li>$250 refundable retainer holds your date</li>
        </ul>
        <a class="btn" href="inquire.html">Check my date</a>
      </div>
      <div class="tier reveal" style="--d:.1s">
        <h3>Wedding photography</h3>
        <p class="price">from $1,200 <small>PHOTO + FILM $1,600 — BEST VALUE</small></p>
        <ul>
          <li>Six hours of wedding-day photography</li>
          <li>Fully edited online gallery with print rights</li>
          <li>Add the Highlight Film for $400 — one storyteller, both crafts</li>
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
</main>
''' + FOOTER
open(os.path.join(ROOT, "investment.html"), "w").write(investment)
print("wrote investment.html")

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
  </div>
  <section class="wrap" style="padding-bottom:var(--section)">
    <form class="form reveal" action="https://formsubmit.co/jkl81694@gmail.com" method="POST">
      <input type="hidden" name="_subject" value="New inquiry — jf photo &amp; film website">
      <input type="hidden" name="_next" value="https://jkl5713-bot.github.io/jf-photography/thanks.html">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <div class="row">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" required autocomplete="name"></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="row">
        <div class="field"><label for="f-phone">Phone <span class="dim">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="f-type">What are we making?</label>
          <select id="f-type" name="session_type" required>
            <option value="" selected disabled>Choose one</option>
            <option>Senior session</option>
            <option>Couples / engagement</option>
            <option>Wedding — photo</option>
            <option>Wedding — film</option>
            <option>Wedding — photo + film</option>
            <option>Sports — athlete or program</option>
            <option>Drone / aerial</option>
            <option>Something else</option>
          </select>
        </div>
      </div>
      <div class="row">
        <div class="field"><label for="f-date">Date (or best guess)</label><input id="f-date" name="preferred_date" type="text" placeholder="e.g. Oct 17, 2026"></div>
        <div class="field"><label for="f-hear">How'd you find me? <span class="dim">(optional)</span></label><input id="f-hear" name="heard_from" type="text"></div>
      </div>
      <div class="field"><label for="f-msg">Your story</label><textarea id="f-msg" name="message" placeholder="Venue, team, vision, questions — everything helps." required></textarea></div>
      <div>
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

print("all pages generated")
