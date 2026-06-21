"""Render the curated Repair Aid deck pages; trim unused Firma candidates; shrink biyou hero."""
import os
import fitz
from PIL import Image, ImageOps

BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
REP = os.path.join(BASE, "Portfolio_Doc", "04_REPAIRAID", "VRAMBOUT_Jorre_MPpresentatie_2026_FINAL.pdf")
IMG = os.path.join(BASE, "jorre-portfolio", "assets", "img")


def render_page(pdf, pageno, dst, target_w=1600, q=85):
    doc = fitz.open(pdf); page = doc[pageno]
    zoom = target_w / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    doc.close(); return f"{os.path.getsize(dst)//1024}KB"


repair = {"repair_hero": 1, "repair_decision": 43, "repair_diagnose": 41,
          "repair_dashboard": 39, "repair_phone": 56, "repair_base": 65, "repair_eco": 47}
for name, pno in repair.items():
    print(name, "p" + str(pno), render_page(REP, pno, os.path.join(IMG, name + ".jpg")))

# Trim unused Firma candidates (keep the chosen 6)
keep = {"ff_C0176T01", "ff_C0212T01", "ff_IMG_3712", "ff_IMG_7331", "ff_IMG_7408", "ff_IMG_7451"}
for f in os.listdir(IMG):
    if f.startswith("ff_") and os.path.splitext(f)[0] not in keep:
        os.remove(os.path.join(IMG, f)); print("removed", f)

# Shrink biyou hero a touch
bh = os.path.join(IMG, "biyou_hero.jpg")
im = ImageOps.exif_transpose(Image.open(bh)).convert("RGB")
im.thumbnail((1400, 1400), Image.LANCZOS)
im.save(bh, "JPEG", quality=80, optimize=True, progressive=True)
print("biyou_hero ->", os.path.getsize(bh) // 1024, "KB")
print("DONE")
