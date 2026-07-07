# JF — Juan Flores Photo & Film

Static portfolio site: no frameworks — HTML/CSS/JS plus small Python tools
for the image pipeline and page generation.

**Live:** https://jkl5713-bot.github.io/jf-photography/

## Run locally

```
cd ~/Projects/jf-photography
python3 -m http.server 8080
# open http://localhost:8080
```

## Deploy

Pushing to `main` republishes GitHub Pages automatically (takes ~1 minute).

```
git add -A && git commit -m "update" && git push
```

## Owner-maintained lines (keep these true)

- **Availability line** (pricing + inquire pages): edit the `AVAILABILITY`
  constant at the top of `js/main.js` whenever dates book up.
- **Watch-the-film**: upload your best highlight film to YouTube (unlisted is
  fine), then in `tools/gen_pages.py` search for `WATCH-THE-FILM`, uncomment
  the block, set `data-yt` to the video id, and regenerate. The player only
  loads when clicked — the page stays fast.
- **Testimonials**: the `.pullquote` component is built and styled. When a
  client sends a quote, add a `<blockquote class="pullquote">` on pricing/
  weddings/inquire. The form auto-reply already plants the seed.
- **Sports ledger** (sports.html): add a row per new shoot — 60 seconds of
  maintenance for a living résumé.
- **Collection numbers are canon**: Seniors N° 01 · Couples N° 02 ·
  Weddings N° 03 · Sports N° 04 · Aerial N° 05. Don't renumber.

## One thing left to activate

The inquiry form posts to FormSubmit → **jkl81694@gmail.com**. The FIRST
submission emails that address an activation link — submit the form once and
click it. After that, every inquiry lands in your inbox and the visitor is
redirected to the thank-you page.

## Pricing (2026 market research floors, owner-adjusted; see pricing.html)

- Wedding Highlight Film $700 (research floor was $500 — owner raised)
- Wedding photography from $1,100 / photo+film bundle $1,600 (film add-on $500)
- Portrait sessions (seniors/couples/grads) from $250
- Athlete sessions from $150 · game coverage from $125/game
- Real-estate aerials from $125 · land/farm from $150 · events from $200

Research positioning note: these are launch floors. After the first ~5–10
booked jobs and reviews, local comps support raising seniors/couples to ~$350
and weddings to $1,500–1,800 base. `investment.html` redirects to
`pricing.html` (page was renamed).

## Photo & video look

All portfolio images and the drone loop carry the "JF signature grade"
(filmic S-curve, teal shadows, gold highlights, +5% vibrance, light unsharp)
baked into `tools/process_images.py` — new photos get it automatically. It was
tuned by a 3-judge review panel (skin tones, brand, technical QC). To disable:
set `GRADE = False` in that file and rerun.

## Editing the site

- **Page copy / structure:** edit `tools/gen_pages.py`, run
  `python3 tools/gen_pages.py && python3 tools/build_galleries.py`.
  (index.html is standalone — edit it directly.)
- **Add/swap photos:**
  1. Manifest entry: `[{"src": "/Volumes/T9/...jpg", "category": "seniors",
     "slug": "my-photo", "role": "gallery", "desc": "alt text"}]`
  2. `venv/bin/python tools/process_images.py manifest.json`
     (venv: `python3 -m venv venv && venv/bin/pip install pillow pillow-avif-plugin`)
  3. Add slug + caption to `tools/galleries.json`
  4. `python3 tools/build_galleries.py`
- Never hand-edit between `<!-- GALLERY -->` markers — the generator owns those.

## Structure

- `index.html` — hero, collections, film-strip, aerial teaser
- `seniors / couples / weddings / sports / aerial .html` — genre galleries
- `about / investment / inquire / thanks .html`
- `css/main.css` — design system (navy/gold/ivory, Fraunces + Cabinet Grotesk)
- `js/main.js` — nav, cursor, reveals, preloader · `js/gallery.js` — lightbox
- `tools/` — image pipeline, gallery generator, page generator
- `assets/` — fonts (self-hosted), brand marks, processed images, drone loop
