#!/usr/bin/env python3
"""Inject static <picture> markup into pages between markers.

Reads assets/img/images.json (written by process_images.py) and
tools/galleries.json, then replaces everything between
<!-- GALLERY:<id> --> and <!-- /GALLERY:<id> --> in every top-level .html.

galleries.json entry modes:
  {"mode": "figures", "items": [{"slug": ..., "caption": ...}, ...]}   masonry/strip figures
  {"mode": "pic", "slug": ..., "sizes": "100vw", "eager": true}        bare <picture> (heroes, cards)

Rerun after adding or swapping photos: python3 tools/build_galleries.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = json.load(open(os.path.join(ROOT, "assets", "img", "images.json")))
SPEC = json.load(open(os.path.join(ROOT, "tools", "galleries.json")))
DEFAULT_SIZES = "(max-width: 700px) 96vw, (max-width: 1100px) 46vw, 31vw"


def srcsets(slug):
    m = META[slug]
    base = f"assets/img/{m['category']}/{slug}"
    avif = ", ".join(f"{base}-{tw}.avif {tw}w" for tw in m["widths"])
    jpg = ", ".join(f"{base}-{tw}.jpg {tw}w" for tw in m["widths"])
    return m, base, avif, jpg


def picture(slug, sizes=DEFAULT_SIZES, eager=False, alt=None):
    m, base, avif, jpg = srcsets(slug)
    big = m["widths"][0]
    load = ('fetchpriority="high"' if eager else 'loading="lazy" decoding="async"')
    return f'''<picture>
  <source type="image/avif" srcset="{avif}" sizes="{sizes}">
  <img src="{base}-{big}.jpg" srcset="{jpg}" sizes="{sizes}"
    width="{m['w']}" height="{m['h']}" {load} alt="{alt or m.get('desc', '')}">
</picture>'''


def figure(item):
    slug, caption = item["slug"], item["caption"]
    m, base, avif, jpg = srcsets(slug)
    big = m["widths"][0]
    sizes = item.get("sizes", DEFAULT_SIZES)
    return f'''<figure class="reveal" data-full="{base}-{big}.jpg"
  style="aspect-ratio:{m['w']}/{m['h']};background-image:url('{m['lqip']}')">
  <picture>
    <source type="image/avif" srcset="{avif}" sizes="{sizes}">
    <img src="{base}-{big}.jpg" srcset="{jpg}" sizes="{sizes}"
      width="{m['w']}" height="{m['h']}" loading="lazy" decoding="async"
      alt="{m.get('desc') or caption}">
  </picture>
  <figcaption>{caption}</figcaption>
</figure>'''


def build(gid):
    entry = SPEC[gid]
    if entry.get("mode") == "pic":
        return picture(entry["slug"], entry.get("sizes", "100vw"),
                       entry.get("eager", False), entry.get("alt"))
    parts = [figure(i) for i in entry["items"]]
    inter = entry.get("interlude")
    if inter:
        block = ('<aside class="interlude"><div class="wrap">'
                 f'<p class="eyebrow">{inter["eyebrow"]}</p>'
                 f'<p class="interlude__line">{inter["line"]}</p>'
                 '</div></aside>')
        parts.insert(min(inter.get("after", 8), len(parts)), block)
    return "\n".join(parts)


def main():
    changed = 0
    for fn in sorted(os.listdir(ROOT)):
        if not fn.endswith(".html"):
            continue
        path = os.path.join(ROOT, fn)
        html = orig = open(path).read()
        for gid in SPEC:
            pat = re.compile(rf"(<!-- GALLERY:{gid} -->).*?(<!-- /GALLERY:{gid} -->)", re.S)
            html = pat.sub(lambda mm: mm.group(1) + "\n" + build(gid) + "\n" + mm.group(2), html)
        if html != orig:
            open(path, "w").write(html)
            changed += 1
            print(f"  updated {fn}")
    print(f"done: {changed} pages updated")


if __name__ == "__main__":
    main()
