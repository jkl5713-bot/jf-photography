# JF — Juan Flores Photo & Film

Static portfolio site: no frameworks, no build step for the pages themselves —
just HTML/CSS/JS plus two small Python tools for the image pipeline.

## Run locally

```
cd ~/Projects/jf-photography
python3 -m http.server 8080
# open http://localhost:8080
```

## Deploy (free)

Drag the whole folder into **Netlify Drop** (app.netlify.com/drop), or push to
GitHub and enable **GitHub Pages** / import into **Vercel**. Everything is
static — no server needed.

## Before you launch — confirm these

1. **Prices** on `investment.html`: the $500 Highlight Film package matches your
   signed contract. The "from $175" portrait price is a **placeholder I made up
   from market norms — set your real number** (search `PRICING NOTE` in the file).
2. **FAA Part 107**: `aerial.html` says "Flights under FAA Part 107 rules".
   If you hold a current Part 107 certificate, change it to
   "FAA Part 107 certified remote pilot" (stronger). If not, get certified before
   selling drone work — it's legally required for commercial flights.
3. **Domain**: replace `https://YOUR-DOMAIN.com` in `robots.txt` and
   `sitemap.xml`, and add `<link rel="canonical">` + absolute `og:image` URLs
   once you know the domain.
4. **Contact form**: wired to FormSubmit → jkl5713@gmail.com. The **first**
   submission emails you an activation link — click it once and the form is live.
   After you have a domain, add `<input type="hidden" name="_next"
   value="https://your-domain/thanks.html">` inside the form for the custom
   thank-you page.
5. **Instagram**: no handle was on the SSD, so no social links are on the site.
   Add them in the footer (`gen`erated into every page) when ready.
6. **Jones College**: the sports page credits your Jones College Athletics work —
   double-check you're OK naming them (research says collegiate credit is your
   strongest local proof, but it's your relationship).

## Swap / add photos later

1. Add entries to a manifest JSON like:
   `[{"src": "/Volumes/T9/...jpg", "category": "seniors", "slug": "my-new-photo", "role": "gallery", "desc": "alt text"}]`
2. Process: `python3 tools/process_images.py manifest.json`
   (needs Pillow: `python3 -m venv venv && venv/bin/pip install pillow pillow-avif-plugin`,
   then use `venv/bin/python`)
3. Add the slug + caption to `tools/galleries.json` in whichever gallery you want.
4. Rebuild: `python3 tools/build_galleries.py`

Images are generated as AVIF + JPEG at two widths with blur-up placeholders —
never hand-edit the `<picture>` blocks between `<!-- GALLERY -->` markers.

## Structure

- `index.html` — hero, collections, film-strip, aerial teaser
- `seniors / couples / weddings / sports / aerial .html` — genre galleries
- `about / investment / inquire / thanks .html`
- `css/main.css` — design system (navy/gold/ivory, Fraunces + Cabinet Grotesk)
- `js/main.js` — nav, cursor, reveals, preloader · `js/gallery.js` — lightbox
- `tools/` — image pipeline + gallery generator
- `assets/` — fonts (self-hosted), brand marks, processed images, drone video loop
