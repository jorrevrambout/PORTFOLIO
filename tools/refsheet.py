"""Render the reference deck + a sheet of unused Firma stills for curation."""
import os
import fitz
from PIL import Image, ImageOps, ImageDraw

BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
SH = os.path.join(BASE, "jorre-portfolio", "assets", "img", "_sheets"); os.makedirs(SH, exist_ok=True)
FF = os.path.join(BASE, "Portfolio_Doc", "05_FIRMA FUNK", "BEELDMATERIAAL")


def sheet(items, out, cols, tile):
    rows = (len(items) + cols - 1) // cols
    s = Image.new("RGB", (cols * (tile + 6) + 6, rows * (tile + 6) + 6), (24, 24, 24))
    d = ImageDraw.Draw(s)
    for i, (im, lbl) in enumerate(items):
        t = ImageOps.contain(im.convert("RGB"), (tile, tile))
        r, c = divmod(i, cols); x = 6 + c * (tile + 6); y = 6 + r * (tile + 6)
        s.paste(t, (x + (tile - t.width) // 2, y + (tile - t.height) // 2))
        d.rectangle([x, y, x + len(lbl) * 7 + 6, y + 15], fill=(0, 0, 0))
        d.text((x + 3, y + 3), lbl, fill=(255, 235, 0))
    s.save(out, quality=85); print("->", os.path.basename(out), s.size)


# reference deck
doc = fitz.open(os.path.join(BASE, "Design", "Black and Gray Minimalist Creative Portfolio Presentation.pdf"))
pages = [0, 1, 2, 3, 4, 6, 9, 12, 18, 30, 55, 90]
items = []
for p in pages:
    if p < doc.page_count:
        pix = doc[p].get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
        items.append((Image.frombytes("RGB", [pix.width, pix.height], pix.samples), "p" + str(p)))
doc.close()
sheet(items, os.path.join(SH, "ref_deck.jpg"), 4, 330)

# unused Firma candidates
cands = ["C0204T01.JPG", "C0209T01.JPG", "C0230T01.JPG", "IMG_3654.JPG", "IMG_3669.JPG",
         "IMG_3692.JPG", "IMG_7327.JPG", "IMG_7421.JPG", "IMG_7452.JPG", "IMG_7455.JPG",
         "IMG_7463.JPG", "IMG_7467.JPG", "IMG_7470.JPG", "C0175T01.JPG"]
fit = []
for v in cands:
    p = os.path.join(FF, v)
    if os.path.exists(p):
        im = ImageOps.exif_transpose(Image.open(p)); im.thumbnail((500, 500))
        fit.append((im, v.replace(".JPG", "")))
sheet(fit, os.path.join(SH, "firma_unused.jpg"), 4, 330)
print("done")
