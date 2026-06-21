"""Produce final, web-optimized images + emit two pick-sheets (Firma, Repair Aid)."""
import os, glob, shutil
import fitz
from PIL import Image, ImageDraw, ImageOps

BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
DOC = os.path.join(BASE, "Portfolio_Doc")
OLD = os.path.join(BASE, "Portfolio claude", "website", "assets", "img")
IMG = os.path.join(BASE, "jorre-portfolio", "assets", "img")
SHEETS = os.path.join(IMG, "_sheets")
os.makedirs(IMG, exist_ok=True); os.makedirs(SHEETS, exist_ok=True)


def save_opt(src, dst, maxedge=1600, q=82):
    im = Image.open(src); im = ImageOps.exif_transpose(im).convert("RGB")
    im.thumbnail((maxedge, maxedge), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    return os.path.getsize(dst) // 1024


def render_page(pdf, pageno, dst, target_w=1500, q=85):
    doc = fitz.open(pdf); page = doc[pageno]
    zoom = target_w / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    doc.close(); return f"{pix.width}x{pix.height} {os.path.getsize(dst)//1024}KB"


def labeled_sheet(items, out, cols, tile):
    # items: list of (PIL image, label)
    n = len(items); rows = (n + cols - 1) // cols; pad = 6
    W = cols * (tile + pad) + pad; H = rows * (tile + pad) + pad
    sheet = Image.new("RGB", (W, H), (24, 24, 24)); draw = ImageDraw.Draw(sheet)
    for i, (im, lbl) in enumerate(items):
        r, c = divmod(i, cols); x = pad + c * (tile + pad); y = pad + r * (tile + pad)
        t = ImageOps.contain(im.convert("RGB"), (tile, tile))
        sheet.paste(t, (x + (tile - t.width) // 2, y + (tile - t.height) // 2))
        draw.rectangle([x, y, x + len(lbl) * 8 + 8, y + 18], fill=(0, 0, 0))
        draw.text((x + 3, y + 4), lbl, fill=(255, 235, 0))
    sheet.save(out, quality=85); print("sheet:", os.path.basename(out), sheet.size)


# ---- BIYOU (reuse optimized old-site images) ----
biyou = {"biyou_hero": "p07_3.jpeg", "biyou_family": "p09_4.jpeg", "biyou_hand": "p08_2.jpeg",
         "biyou_blue": "p05_1.jpeg", "biyou_c1": "p06_1.jpeg", "biyou_c2": "p06_2.jpeg", "biyou_c3": "p06_3.jpeg"}
for k, v in biyou.items():
    print("biyou", k, save_opt(os.path.join(OLD, v), os.path.join(IMG, k + ".jpg")), "KB")

# ---- BILOO ----
biloo = {"biloo_hero": "p16_1.jpeg", "biloo_field": "p18_3.jpeg", "biloo_config": "p17_1.jpeg",
         "biloo_top": "p18_1.jpeg", "biloo_test": "p18_2.jpeg", "biloo_cad": "p18_4.jpeg"}
for k, v in biloo.items():
    print("biloo", k, save_opt(os.path.join(OLD, v), os.path.join(IMG, k + ".jpg")), "KB")

# ---- JORRE portraits / candids ----
J = os.path.join(DOC, "00_JORRE")
jorre = {"jorre_portrait": "IMG_8803.jpg", "jorre_portrait_alt": "IMG_8804.jpg", "jorre_make": "IMG_8726.JPG",
         "jorre_studio": "430084966_686994293438381_5589453982498765943_n.jpg",
         "jorre_workshop": "image0.jpeg",
         "jorre_brainstorm": "434164572_1101170627775168_5007276277711808105_n.jpg",
         "jorre_outdoor": "426135415_1107468060670253_4134781738504463043_n.jpg"}
for k, v in jorre.items():
    p = os.path.join(J, v)
    if os.path.exists(p):
        print("jorre", k, save_opt(p, os.path.join(IMG, k + ".jpg"), maxedge=1500), "KB")
    else:
        print("!! missing", v)

# ---- AMI app screens ----
AMI = os.path.join(DOC, "03_AMI", "afdrukken")
alle = os.path.join(AMI, "alle schermen.pdf")
for pno, name in [(0, "ami_join"), (1, "ami_map"), (2, "ami_customize"), (3, "ami_agenda"), (4, "ami_character")]:
    print("ami", name, render_page(alle, pno, os.path.join(IMG, name + ".jpg"), target_w=1500))
print("ami ami_chat", render_page(os.path.join(AMI, "CHATROOM interface (1).pdf"), 0, os.path.join(IMG, "ami_chat.jpg"), target_w=1500))

# ---- FIRMA candidates -> optimized + labeled pick sheet ----
FF = os.path.join(DOC, "05_FIRMA FUNK", "BEELDMATERIAAL")
ff_cands = ["C0175T01.JPG", "C0176T01.JPG", "C0204T01.JPG", "C0205T01.JPG", "C0212T01.JPG",
            "IMG_3674.JPG", "IMG_3712.JPG", "IMG_7331.JPG", "IMG_7408.JPG", "IMG_7451.JPG",
            "IMG_7455.JPG", "IMG_7459.JPG", "IMG_7462.JPG", "IMG_7470.JPG"]
ff_items = []
for v in ff_cands:
    p = os.path.join(FF, v)
    if not os.path.exists(p): print("!! missing", v); continue
    dst = os.path.join(IMG, "ff_" + os.path.splitext(v)[0] + ".jpg")
    save_opt(p, dst, maxedge=1600, q=80)
    ff_items.append((Image.open(dst), os.path.splitext(v)[0]))
labeled_sheet(ff_items, os.path.join(SHEETS, "firma_final.jpg"), cols=4, tile=360)

# ---- REPAIR AID: pick-sheet of candidate deck pages ----
REP = os.path.join(DOC, "04_REPAIRAID")
pres = os.path.join(REP, "VRAMBOUT_Jorre_MPpresentatie_2026_FINAL.pdf")
pick_pages = [0, 1, 33, 35, 37, 39, 41, 43, 47, 56, 58, 65]
rep_items = []
doc = fitz.open(pres)
for pno in pick_pages:
    if pno >= doc.page_count: continue
    page = doc[pno]; zoom = 700 / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    rep_items.append((Image.frombytes("RGB", [pix.width, pix.height], pix.samples), f"p{pno}"))
doc.close()
labeled_sheet(rep_items, os.path.join(SHEETS, "repair_pick.jpg"), cols=3, tile=460)
# also copy the architecture diagram
arch = os.path.join(REP, "archtiectuyur.png")
if os.path.exists(arch):
    print("repair arch", save_opt(arch, os.path.join(IMG, "repair_arch.jpg"), maxedge=1600))

print("\nDONE finals")
