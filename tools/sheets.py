"""Build contact sheets so we can curate the best images from the source folders."""
import os, glob
import fitz
from PIL import Image, ImageDraw, ImageOps

BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
DOC = os.path.join(BASE, "Portfolio_Doc")
OUT = os.path.join(BASE, "jorre-portfolio", "assets", "img", "_sheets")
os.makedirs(OUT, exist_ok=True)


def contact_sheet(images, out, cols=5, tile=300):
    n = len(images)
    if n == 0:
        print("!! no images for", out); return
    rows = (n + cols - 1) // cols
    pad = 6
    W = cols * (tile + pad) + pad
    H = rows * (tile + pad) + pad
    sheet = Image.new("RGB", (W, H), (24, 24, 24))
    draw = ImageDraw.Draw(sheet)
    for i, im in enumerate(images):
        r, c = divmod(i, cols)
        x = pad + c * (tile + pad); y = pad + r * (tile + pad)
        t = ImageOps.contain(im, (tile, tile))
        ox = x + (tile - t.width) // 2; oy = y + (tile - t.height) // 2
        sheet.paste(t, (ox, oy))
        lbl = str(i)
        draw.rectangle([x, y, x + len(lbl) * 9 + 8, y + 18], fill=(0, 0, 0))
        draw.text((x + 3, y + 4), lbl, fill=(255, 235, 0))
    sheet.save(out, quality=85)
    print("wrote", os.path.basename(out), sheet.size, "n=", n)


def load_img(p, maxedge=900):
    im = Image.open(p); im = ImageOps.exif_transpose(im); im = im.convert("RGB")
    im.thumbnail((maxedge, maxedge))
    return im


def pdf_pages(path, maxpages=80, zoom=1.0):
    doc = fitz.open(path); out = []
    for i, page in enumerate(doc):
        if i >= maxpages: break
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        out.append(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    doc.close(); return out


def listing(label, files):
    print(f"\n== {label} ==")
    for i, f in enumerate(files):
        print(i, os.path.basename(f))


# 1. JORRE portraits
try:
    d = os.path.join(DOC, "00_JORRE")
    files = sorted(f for f in glob.glob(os.path.join(d, "*")) if f.lower().endswith((".jpg", ".jpeg", ".png")))
    contact_sheet([load_img(f) for f in files], os.path.join(OUT, "jorre.jpg"), cols=5, tile=300)
    listing("JORRE", files)
except Exception as e:
    print("JORRE error", e)

# 2. AMI app screens (afdrukken PDFs)
try:
    d = os.path.join(DOC, "03_AMI", "afdrukken")
    files = sorted(glob.glob(os.path.join(d, "*.pdf")))
    imgs = []; titles = []
    for f in files:
        for j, im in enumerate(pdf_pages(f, maxpages=15, zoom=1.1)):
            imgs.append(im); titles.append(f"{os.path.basename(f)[:14]} p{j}")
    contact_sheet(imgs, os.path.join(OUT, "ami.jpg"), cols=6, tile=300)
    print("\n== AMI tiles =="); [print(i, t) for i, t in enumerate(titles)]
except Exception as e:
    print("AMI error", e)

# 3. Repair Aid - presentation, dossier, poster
try:
    d = os.path.join(DOC, "04_REPAIRAID")
    pres = pdf_pages(os.path.join(d, "VRAMBOUT_Jorre_MPpresentatie_2026_FINAL.pdf"), maxpages=80, zoom=0.7)
    contact_sheet(pres, os.path.join(OUT, "repair_pres.jpg"), cols=7, tile=260)
    doss = pdf_pages(os.path.join(d, "VRAMBOUT_Jorre_MPdossier_2026_FINAL.pdf"), maxpages=90, zoom=0.6)
    contact_sheet(doss, os.path.join(OUT, "repair_dossier.jpg"), cols=8, tile=220)
    poster = pdf_pages(os.path.join(d, "VRAMBOUT_Jorre_poster_2026.pdf"), maxpages=1, zoom=1.6)[0]
    poster.save(os.path.join(OUT, "repair_poster_full.jpg"), quality=88)
    print("\nrepair: pres", len(pres), "dossier", len(doss), "poster", poster.size)
except Exception as e:
    print("REPAIR error", e)

# 4. Firma Funk event stills
try:
    d = os.path.join(DOC, "05_FIRMA FUNK", "BEELDMATERIAAL")
    files = sorted(f for f in glob.glob(os.path.join(d, "*")) if f.lower().endswith((".jpg", ".jpeg")))
    contact_sheet([load_img(f) for f in files], os.path.join(OUT, "firma.jpg"), cols=6, tile=300)
    listing("FIRMA", files)
except Exception as e:
    print("FIRMA error", e)

print("\nDONE")
