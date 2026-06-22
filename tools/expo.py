"""Optimize the Expo images for Repair Aid + build a verify sheet."""
import os
from PIL import Image, ImageOps, ImageDraw

BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
EXPO = os.path.join(BASE, "00_Inleveren", "VRAMBOUT_Jorre_Website_Expo_2026")
IMG = os.path.join(BASE, "jorre-portfolio", "assets", "img")
SH = os.path.join(IMG, "_sheets"); os.makedirs(SH, exist_ok=True)


def opt(src, dst, maxedge=1700, q=85):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((maxedge, maxedge), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    return os.path.getsize(dst) // 1024


jobs = {
    "repair_expo_01.jpg": "VRAMBOUT_Jorre_Website_Expo_01.jpg",
    "repair_diagram.jpg": "VRAMBOUT_Jorre_Website_Expo_02_2026.jpg",
    "repair_expo_03.jpg": "VRAMBOUT_jorre_Website_Expo_03.jpg",
    "repair_expo_04.jpg": "VRAMBOUT_jorre_Website_Expo_04.jpg",
}
for dst, src in jobs.items():
    p = os.path.join(EXPO, src)
    print(dst, opt(p, os.path.join(IMG, dst)), "KB" if os.path.exists(os.path.join(IMG, dst)) else "FAIL")

# verify sheet
checks = ["repair_expo_01.jpg", "repair_diagram.jpg", "repair_expo_03.jpg", "repair_expo_04.jpg",
          "ff_IMG_7408.jpg", "ff_C0176T01.jpg", "biyou_c1.jpg", "biyou_c2.jpg", "biyou_c3.jpg",
          "biyou_poster.jpg", "biyou_calcite.jpg"]
tile, cols = 360, 4
rows = (len(checks) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tile + 6) + 6, rows * (tile + 6) + 6), (24, 24, 24))
d = ImageDraw.Draw(sheet)
for i, name in enumerate(checks):
    p = os.path.join(IMG, name)
    if not os.path.exists(p):
        continue
    im = ImageOps.contain(Image.open(p).convert("RGB"), (tile, tile))
    r, c = divmod(i, cols); x = 6 + c * (tile + 6); y = 6 + r * (tile + 6)
    sheet.paste(im, (x + (tile - im.width) // 2, y + (tile - im.height) // 2))
    d.rectangle([x, y, x + len(name) * 7 + 6, y + 16], fill=(0, 0, 0))
    d.text((x + 3, y + 4), name, fill=(255, 235, 0))
sheet.save(os.path.join(SH, "verify2.jpg"), quality=85)
print("sheet ->", os.path.join(SH, "verify2.jpg"))
