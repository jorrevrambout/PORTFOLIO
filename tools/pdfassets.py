"""Process 4 distinct Firma photos for the PDF + a sheet of the intro photos to assign."""
import os
from PIL import Image, ImageOps, ImageDraw

BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
FF = os.path.join(BASE, "Portfolio_Doc", "05_FIRMA FUNK", "BEELDMATERIAAL")
IMG = os.path.join(BASE, "jorre-portfolio", "assets", "img")
SH = os.path.join(IMG, "_sheets"); os.makedirs(SH, exist_ok=True)


def opt(src, dst, maxedge=1500, q=82):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((maxedge, maxedge), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    return os.path.getsize(dst) // 1024


# 4 distinct unused Firma photos for the PDF
ff = {"ff_pdf_1.jpg": "IMG_3654.JPG", "ff_pdf_2.jpg": "C0230T01.JPG",
      "ff_pdf_3.jpg": "IMG_7327.JPG", "ff_pdf_4.jpg": "IMG_7467.JPG"}
for dst, src in ff.items():
    print(dst, opt(os.path.join(FF, src), os.path.join(IMG, dst)), "KB")


def sheet(names, out, cols, tile, folder=IMG):
    rows = (len(names) + cols - 1) // cols
    s = Image.new("RGB", (cols * (tile + 6) + 6, rows * (tile + 6) + 6), (24, 24, 24))
    d = ImageDraw.Draw(s)
    for i, name in enumerate(names):
        p = os.path.join(folder, name)
        if not os.path.exists(p): continue
        im = ImageOps.contain(Image.open(p).convert("RGB"), (tile, tile))
        r, c = divmod(i, cols); x = 6 + c * (tile + 6); y = 6 + r * (tile + 6)
        s.paste(im, (x + (tile - im.width) // 2, y + (tile - im.height) // 2))
        d.rectangle([x, y, x + len(name) * 7 + 6, y + 15], fill=(0, 0, 0))
        d.text((x + 3, y + 3), name, fill=(255, 235, 0))
    s.save(out, quality=85); print("->", os.path.basename(out), s.size)


sheet(["jorre_%02d.jpg" % i for i in range(1, 20)], os.path.join(SH, "jorre_all.jpg"), 5, 300)
sheet(["ff_pdf_1.jpg", "ff_pdf_2.jpg", "ff_pdf_3.jpg", "ff_pdf_4.jpg"], os.path.join(SH, "ff_pdf.jpg"), 4, 320)
print("done")
