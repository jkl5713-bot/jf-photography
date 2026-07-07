#!/usr/bin/env python3
"""Portfolio image pipeline: EXIF-safe resize -> AVIF + JPEG + LQIP blur-up.

Usage: imgenv/bin/python process_images.py manifest.json
Manifest: [{"src": "/abs/path.jpg", "category": "sports", "slug": "tennis-serve", "role": "gallery"}]
Outputs into assets/img/<category>/<slug>-<w>.{avif,jpg} and writes assets/img/images.json
with dimensions + base64 LQIP for every image.
"""
import json, os, sys, io, base64
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pillow_avif  # noqa: F401  (registers AVIF codec)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")

SIZES = {"hero": [2400, 1200], "gallery": [1600, 800]}
GRADE = True          # JF signature grade: filmic S-curve, teal shadows, gold highlights
SHARPEN = True        # light unsharp mask on resized outputs


def _lut(points):
    """256-entry LUT from control points [(in, out), ...]."""
    xs, ys = zip(*points)
    return np.clip(np.interp(np.arange(256), xs, ys), 0, 255).astype(np.uint8)


# gentle filmic S-curve with a faded black point and soft highlight rolloff
_MASTER = _lut([(0, 5), (48, 44), (128, 132), (208, 212), (255, 251)])
# split-tone: shadows lean teal (R down / B up), highlights lean true gold
# (R held above G: judge-panel fix for green-cream highlights + skin hue drift)
_R = _lut([(0, 0), (64, 62), (160, 162), (224, 225), (240, 238), (255, 252)])
_G = _lut([(0, 2), (128, 129), (208, 206), (255, 250)])
_B = _lut([(0, 9), (96, 100), (176, 172), (255, 245)])


def grade(im):
    """Apply the JF signature grade to an RGB image."""
    a = np.asarray(im)
    a = _MASTER[a]                                   # tone curve on all channels
    a[..., 0] = _R[a[..., 0]]                        # split-tone per channel
    a[..., 1] = _G[a[..., 1]]
    a[..., 2] = _B[a[..., 2]]
    out = Image.fromarray(a, "RGB")
    return ImageEnhance.Color(out).enhance(1.05)     # vibrance-ish lift (1.08 shifted skin)


def process(entry, meta):
    src, cat, slug = entry["src"], entry["category"], entry["slug"]
    role = entry.get("role", "gallery")
    dest_dir = os.path.join(OUT, cat)
    os.makedirs(dest_dir, exist_ok=True)

    im = Image.open(src)
    im = ImageOps.exif_transpose(im).convert("RGB")
    if GRADE:
        im = grade(im)
    w, h = im.size

    widths = [min(s, w) for s in SIZES[role]]
    widths = sorted(set(widths), reverse=True)
    for tw in widths:
        r = im.resize((tw, round(h * tw / w)), Image.LANCZOS)
        if SHARPEN:
            r = r.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))
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
