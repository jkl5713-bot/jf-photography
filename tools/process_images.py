#!/usr/bin/env python3
"""Portfolio image pipeline: EXIF-safe resize -> AVIF + JPEG + LQIP blur-up.

Usage: imgenv/bin/python process_images.py manifest.json
Manifest: [{"src": "/abs/path.jpg", "category": "sports", "slug": "tennis-serve", "role": "gallery"}]
Outputs into assets/img/<category>/<slug>-<w>.{avif,jpg} and writes assets/img/images.json
with dimensions + base64 LQIP for every image.
"""
import json, os, sys, io, base64
from PIL import Image, ImageOps, ImageFilter
import pillow_avif  # noqa: F401  (registers AVIF codec)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")

SIZES = {"hero": [2400, 1200], "gallery": [1600, 800]}


def process(entry, meta):
    src, cat, slug = entry["src"], entry["category"], entry["slug"]
    role = entry.get("role", "gallery")
    dest_dir = os.path.join(OUT, cat)
    os.makedirs(dest_dir, exist_ok=True)

    im = Image.open(src)
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size

    widths = [min(s, w) for s in SIZES[role]]
    widths = sorted(set(widths), reverse=True)
    for tw in widths:
        r = im.resize((tw, round(h * tw / w)), Image.LANCZOS)
        r.save(os.path.join(dest_dir, f"{slug}-{tw}.avif"), quality=62)
        r.save(os.path.join(dest_dir, f"{slug}-{tw}.jpg"), quality=80,
               progressive=True, optimize=True)

    tiny = im.resize((24, max(1, round(h * 24 / w))), Image.LANCZOS)
    tiny = tiny.filter(ImageFilter.GaussianBlur(1))
    buf = io.BytesIO()
    tiny.save(buf, "JPEG", quality=55)
    lqip = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

    px = im.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    meta[slug] = {
        "category": cat, "w": w, "h": h, "widths": widths,
        "lqip": lqip, "avg": "#%02x%02x%02x" % px,
        "desc": entry.get("desc", ""),
    }
    print(f"  ok {cat}/{slug} ({w}x{h}) -> {widths}")


def main(manifest_path):
    entries = json.load(open(manifest_path))
    meta_path = os.path.join(OUT, "images.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    fails = []
    for e in entries:
        try:
            process(e, meta)
        except Exception as ex:
            fails.append((e["src"], str(ex)))
            print(f"  FAIL {e['src']}: {ex}", file=sys.stderr)
    os.makedirs(OUT, exist_ok=True)
    json.dump(meta, open(meta_path, "w"), indent=1)
    print(f"done: {len(entries) - len(fails)}/{len(entries)} processed")


if __name__ == "__main__":
    main(sys.argv[1])
