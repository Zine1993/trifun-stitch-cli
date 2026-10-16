"""Generic conversion; no website, pet optimization, model, or network imports."""

import json
import math
import warnings
from collections import Counter
from pathlib import Path

from PIL import Image, ImageOps

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
MAX_CELLS = 200_000
Image.MAX_IMAGE_PIXELS = 25_000_000


def load_palette(path: Path) -> tuple[str, list[dict]]:
    """Read a user-supplied JSON palette, including the XStitchLab schema."""
    if path.stat().st_size > 2_000_000:
        raise ValueError("Palette file exceeds 2 MB.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("colors"), list):
        raise ValueError("Palette must contain a colors array.")
    brand = data.get("brand", "Custom")
    if not isinstance(brand, str) or not brand.strip() or len(brand) > 80:
        raise ValueError("Palette brand must be 1-80 characters.")
    colors = data["colors"]
    if not 1 <= len(colors) <= 1024:
        raise ValueError("Palette must contain 1-1024 colors.")
    seen = set()
    clean = []
    for entry in colors:
        if not isinstance(entry, dict):
            raise ValueError("Each palette entry must be an object.")
        code, name, rgb = entry.get("code"), entry.get("name"), entry.get("rgb")
        if not isinstance(code, str) or not code.strip() or len(code) > 40 or code in seen:
            raise ValueError("Palette codes must be unique, nonempty strings up to 40 characters.")
        if not isinstance(name, str) or not name.strip() or len(name) > 120:
            raise ValueError("Palette names must be nonempty strings up to 120 characters.")
        if not isinstance(rgb, list) or len(rgb) != 3 or any(type(c) is not int or not 0 <= c <= 255 for c in rgb):
            raise ValueError("RGB must contain three integer values between 0 and 255.")
        seen.add(code)
        clean.append({"code": code, "name": name, "rgb": rgb})
    return brand, clean


def lab(rgb):
    """sRGB/D65 to CIELAB for basic CIE76 palette matching."""
    linear = [v / 3294.6 if v <= 10.31475 else ((v / 255 + .055) / 1.055) ** 2.4 for v in rgb]
    r, g, b = linear
    xyz = ((.4124564*r + .3575761*g + .1804375*b)/.95047,
           .2126729*r + .7151522*g + .0721750*b,
           (.0193339*r + .1191920*g + .9503041*b)/1.08883)
    x, y, z = [v ** (1/3) if v > 216/24389 else (24389/27*v + 16)/116 for v in xyz]
    return 116*y-16, 500*(x-y), 200*(y-z)


def convert(image_path: Path, width=40, colors=8, fabric=14, palette_path=None, title="Cross-stitch pattern"):
    if not 1 <= width <= 300 or not 1 <= colors <= len(SYMBOLS) or not 6 <= fabric <= 40:
        raise ValueError("Use width 1-300, colors 1-62, and fabric count 6-40.")
    brand, supplied = load_palette(palette_path) if palette_path else ("RGB reference only", None)
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(image_path) as source:
            oriented = ImageOps.exif_transpose(source)
            height = max(1, round(width * oriented.height / oriented.width))
            if width * height > MAX_CELLS:
                raise ValueError("Target grid exceeds 200,000 cells; use a smaller width.")
            rgba = oriented.convert("RGBA")
            # Alpha is explicit: fully transparent cells have no stitch.
            alpha = rgba.getchannel("A").resize((width, height), Image.Resampling.BOX)
            rgb = Image.new("RGBA", rgba.size, "white")
            rgb.alpha_composite(rgba)
            small = rgb.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
    mask = [a >= 128 for a in alpha.get_flattened_data()]
    visible = [pixel for pixel, keep in zip(small.get_flattened_data(), mask) if keep]
    if not visible:
        raise ValueError("Image contains no visible stitches.")
    # Quantize visible cells only, so transparency consumes no thread colors.
    strip = Image.new("RGB", (len(visible), 1))
    strip.putdata(visible)
    quantized = strip.quantize(colors=min(colors, len(visible)), method=Image.Quantize.MEDIANCUT,
                               dither=Image.Dither.NONE).convert("RGB")
    selected = sorted(set(quantized.get_flattened_data()))
    target_labs = [lab(c["rgb"]) for c in supplied] if supplied else []
    mapping = {}
    legend = []
    codes = {}
    for rgb_value in selected:
        if supplied:
            value_lab = lab(rgb_value)
            nearest = min(range(len(supplied)), key=lambda i: sum((a-b)**2 for a,b in zip(value_lab, target_labs[i])))
            entry = supplied[nearest].copy()
        else:
            hex_value = "#%02X%02X%02X" % rgb_value
            entry = {"code": hex_value, "name": "RGB " + hex_value, "rgb": list(rgb_value)}
        if entry["code"] not in codes:
            codes[entry["code"]] = len(legend)
            legend.append({**entry, "symbol": SYMBOLS[len(legend)], "stitches": 0})
        mapping[rgb_value] = codes[entry["code"]]
    visible_iter = iter(quantized.get_flattened_data())
    flat = [mapping[next(visible_iter)] if keep else -1 for keep in mask]
    counts = Counter(flat)
    for i, entry in enumerate(legend):
        entry["stitches"] = counts[i]
        # 2 strands, full crosses, explicit rough model; not a purchase guarantee.
        entry["estimated_meters"] = round(counts[i] * (2*math.sqrt(2)*.0254/fabric + .002) * 2 * 1.2, 3)
    return {"schema_version": 1, "title": title[:160], "brand": brand,
            "width": width, "height": height, "fabric_count": fabric,
            "total_stitches": sum(mask), "empty_cells": counts[-1],
            "stitched_size_cm": [round(width/fabric*2.54, 2), round(height/fabric*2.54, 2)],
            "thread_estimate": "Rough strand-meters: 2 strands, 20% allowance; excludes travel and fabric margins.",
            "legend": legend, "grid": [flat[y*width:(y+1)*width] for y in range(height)]}


def validate(pattern):
    width, height, legend = pattern["width"], pattern["height"], pattern["legend"]
    if len(pattern["grid"]) != height or any(len(row) != width for row in pattern["grid"]):
        raise ValueError("Grid dimensions do not match metadata.")
    counts = Counter(v for row in pattern["grid"] for v in row)
    if any(type(v) is not int or v < -1 or v >= len(legend) for v in counts):
        raise ValueError("Invalid grid index.")
    if len({c["code"] for c in legend}) != len(legend) or len({c["symbol"] for c in legend}) != len(legend):
        raise ValueError("Thread codes and symbols must be unique.")
    if any(c["stitches"] != counts[i] for i, c in enumerate(legend)):
        raise ValueError("Legend stitch counts do not match grid.")
    if pattern["total_stitches"] != width*height-counts[-1] or pattern["empty_cells"] != counts[-1]:
        raise ValueError("Total stitch counts do not match grid.")

