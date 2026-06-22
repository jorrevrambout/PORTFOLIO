"""Add Firma IMG_3731 + two new intro-loop photos (jorre_18/19). Verify sheet."""
import os
from PIL import Image, ImageOps, ImageDraw

BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
DOC = os.path.join(BASE, "Portfolio_Doc")
IMG = os.path.join(BASE, "jorre-portfolio", "assets", "img")
SH = os.path.join(IMG, "_sheets"); os.makedirs(SH, exist_ok=True)


def opt(src, dst, maxedge=1600, q=82):
    if not os.path.exists(src):
        print("!! MISSING", src); return None
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((maxedge, maxedge), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    return os.path.getsize(dst) // 1024


jobs = {
    "ff_IMG_3731.jpg": os.path.join(DOC, "05_FIRMA FUNK", "BEELDMATERIAAL", "IMG_3731.JPG"),
    "jorre_18.jpg": os.path.join(DOC, "00_JORRE", "IMG_3720.JPG"),
    "jorre_19.jpg": os.path.join(DOC, "00_JORRE", "IMG_3675.JPG"),
}
for dst, src in jobs.items():
    print(dst, opt(src, os.path.join(IMG, dst)), "KB")

checks = ["ff_C0176T01.jpg", "ff_IMG_3731.jpg", "jorre_18.jpg", "jorre_19.jpg"]
tile, cols = 380, 2
rows = (len(checks) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tile + 6) + 6, rows * (tile + 6) + 6), (24, 24, 24))
d = ImageDraw.Draw(sheet)
for i, name in enumerate(checks):
    p = os.path.join(IMG, name)
    if not os.path.exists(p): continue
    im = ImageOps.contain(Image.open(p).convert("RGB"), (tile, tile))
    r, c = divmod(i, cols); x = 6 + c * (tile + 6); y = 6 + r * (tile + 6)
    sheet.paste(im, (x + (tile - im.width) // 2, y + (tile - im.height) // 2))
    d.rectangle([x, y, x + len(name) * 8 + 6, y + 17], fill=(0, 0, 0))
    d.text((x + 3, y + 4), name, fill=(255, 235, 0))
sheet.save(os.path.join(SH, "verify3.jpg"), quality=86)
print("sheet ->", os.path.join(SH, "verify3.jpg"))
