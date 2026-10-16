"""Portable PNG/JSON/PDF exports with no external fonts or website imports."""

import io
import json
from pathlib import Path

from fpdf import FPDF
from PIL import Image

from .core import validate


def printable(value):
    # Built-in PDF fonts are ASCII; preserve original Unicode in JSON.
    return " ".join(str(value).encode("ascii", "replace").decode().split())


def preview_image(pattern):
    image = Image.new("RGBA", (pattern["width"], pattern["height"]))
    image.putdata([(*pattern["legend"][v]["rgb"], 255) if v >= 0 else (0,0,0,0)
                   for row in pattern["grid"] for v in row])
    return image


def export_pdf(pattern, path: Path):
    pdf = FPDF()
    pdf.set_title(printable(pattern["title"]))
    pdf.set_author("trifun")
    pdf.set_auto_page_break(True, margin=16)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 9, "trifun | Basic cross-stitch")
    pdf.set_font("Helvetica", "", 11)
    for text in [printable(pattern["title"]),
                 f'{pattern["width"]} x {pattern["height"]} cells | {pattern["total_stitches"]} stitches | {len(pattern["legend"])} colors',
                 f'{pattern["fabric_count"]}-count fabric | stitched area {pattern["stitched_size_cm"][0]} x {pattern["stitched_size_cm"][1]} cm',
                 "Palette: " + printable(pattern["brand"]),
                 "Blank cells have no stitch. White cells WITH symbols are stitched.",
                 "Print chart pages at 100% scale. Cell size: 4 mm. No page overlap.",
                 "RGB-only output is not a thread shopping list. Supply a licensed thread palette for thread codes.",
                 "PDF labels use ASCII (? replaces unsupported characters); JSON retains original text."]:
        pdf.set_x(10)
        pdf.multi_cell(0, 6, text)
    img = preview_image(pattern)
    buffer = io.BytesIO()
    img.resize((img.width*4, img.height*4), Image.Resampling.NEAREST).save(buffer, format="PNG")
    w = min(110, 95*img.width/img.height)
    pdf.image(buffer, x=10, y=pdf.get_y()+5, w=w)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, "Legend and rough thread estimates", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 5, pattern["thread_estimate"] + "\nStrand-meters count individual strands, not six-strand skeins. Add fabric margins separately.")
    for entry in pattern["legend"]:
        if pdf.get_y() > 263:
            pdf.add_page()
        pdf.set_x(10)
        pdf.set_fill_color(*entry["rgb"])
        pdf.cell(8, 7, "", border=1, fill=True)
        pdf.cell(8, 7, entry["symbol"], align="C")
        label = printable(f'{entry["code"]} | {entry["name"]}')[:65]
        pdf.cell(128, 7, label)
        pdf.cell(36, 7, f'{entry["stitches"]} sts / {entry["estimated_meters"]:.2f} m', new_x="LMARGIN", new_y="NEXT")
    # A4: 40 columns x 55 rows at 4 mm leaves room for coordinates.
    for top in range(0, pattern["height"], 55):
        for left in range(0, pattern["width"], 40):
            right, bottom = min(left+40, pattern["width"]), min(top+55, pattern["height"])
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 9, f'Chart | columns {left+1}-{right}, rows {top+1}-{bottom}', new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(0, 6, "Coordinates are 1-based. Continue at the next numbered column/row.")
            pdf.set_font("Courier", "", 7)
            for x in range(left, right):
                pdf.set_xy(22+(x-left)*4, 31)
                pdf.cell(4, 4, str(x+1) if x==left or (x+1)%5==0 else "", align="C")
            for y in range(top, bottom):
                pdf.set_xy(10, 36+(y-top)*4)
                pdf.cell(11, 4, str(y+1) if y==top or (y+1)%5==0 else "", align="R")
                for x in range(left, right):
                    v = pattern["grid"][y][x]
                    pdf.set_xy(22+(x-left)*4, 36+(y-top)*4)
                    pdf.set_draw_color(70 if x%10==0 or y%10==0 else 190)
                    pdf.cell(4, 4, pattern["legend"][v]["symbol"] if v>=0 else "", border=1, align="C")
            pdf.set_xy(10, 275)
            pdf.set_font("Helvetica", "", 8)
            pdf.cell(0, 5, f"trifun | page {pdf.page_no()} | basic symbol chart")
    pdf.output(path)


def export(pattern, output: Path):
    validate(pattern)
    # Never silently overwrite an earlier project or write a partial output into it.
    output.mkdir(parents=True, exist_ok=False)
    (output / "pattern.json").write_text(json.dumps(pattern, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    image = preview_image(pattern)
    image.save(output / "grid.png")
    image.resize((image.width*8, image.height*8), Image.Resampling.NEAREST).save(output / "preview.png")
    export_pdf(pattern, output / "pattern.pdf")
