import os, fitz
from PIL import Image, ImageOps, ImageDraw

BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
DOC = os.path.join(BASE, "Portfolio_Doc")
IMG = os.path.join(BASE, "jorre-portfolio", "assets", "img")
OUT = os.path.join(IMG, "_sheets"); os.makedirs(OUT, exist_ok=True)


def montage(paths, out, cols, tile, labels):
    ims = []
    for p in paths:
        try: ims.append(ImageOps.exif_transpose(Image.open(p)).convert("RGB"))
        except Exception as e: print("skip", p, e); ims.append(Image.new("RGB", (tile, tile), (60, 0, 0)))
    rows = (len(ims) + cols - 1) // cols; pad = 6
    sheet = Image.new("RGB", (cols * (tile + pad) + pad, rows * (tile + pad) + pad), (22, 22, 22))
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims):
        r, c = divmod(i, cols); x = pad + c * (tile + pad); y = pad + r * (tile + pad)
        t = ImageOps.contain(im, (tile, tile)); sheet.paste(t, (x + (tile - t.width) // 2, y + (tile - t.height) // 2))
        lab = labels[i]; d.rectangle([x, y, x + len(lab) * 7 + 6, y + 15], fill=(0, 0, 0)); d.text((x + 3, y + 3), lab, fill=(255, 235, 0))
    sheet.save(out, quality=85); print("wrote", os.path.basename(out))


bi = ["biyou_hero", "biyou_hand", "biyou_blue", "biyou_family", "biyou_c1", "biyou_c2", "biyou_c3"]
montage([os.path.join(IMG, b + ".jpg") for b in bi], os.path.join(OUT, "rev_biyou.jpg"), 4, 300, bi)

for name, pdf in [("biyou_POSTER", "biyou_POSTER.pdf"), ("CALCITE_JORRE", "CALCITE_JORRE.pdf")]:
    d = fitz.open(os.path.join(DOC, "01_BIYOU", pdf)); pg = d[0]; z = 760 / pg.rect.width
    pix = pg.get_pixmap(matrix=fitz.Matrix(z, z))
    Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(os.path.join(OUT, "rev_" + name + ".jpg"), quality=85)
    print(name, "pages", d.page_count, "size", (round(pg.rect.width), round(pg.rect.height)))

rp = ["archtiectuyur.png", "stramien poster MP Illustrator.ai (1).png", "stramien poster MP Illustrator.ai.png"]
montage([os.path.join(DOC, "04_REPAIRAID", r) for r in rp], os.path.join(OUT, "rev_repair.jpg"), 3, 340, ["arch", "stramien_1", "stramien_2"])
print("DONE")
