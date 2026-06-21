"""Revision asset rebuild: Biyou rotate+poster/calcite, JORRE loop, AMI report strip,
Repair 3 PNGs, Firma video loops. Cleans superseded assets."""
import os, glob, subprocess
import fitz
from PIL import Image, ImageOps
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
DOC = os.path.join(BASE, "Portfolio_Doc")
IMG = os.path.join(BASE, "jorre-portfolio", "assets", "img")
VID = os.path.join(BASE, "jorre-portfolio", "assets", "video")
os.makedirs(VID, exist_ok=True)


def opt(src, dst, maxedge=1600, q=82):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((maxedge, maxedge), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    return os.path.getsize(dst) // 1024


def render(pdf, page, dst, target=1600, q=85):
    d = fitz.open(pdf); p = d[page]; z = target / max(p.rect.width, p.rect.height)
    pix = p.get_pixmap(matrix=fitz.Matrix(z, z))
    Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    d.close(); return os.path.getsize(dst) // 1024


def rm(*names):
    for n in names:
        p = os.path.join(IMG, n)
        if os.path.exists(p): os.remove(p); print("  removed", n)


print("== BIYOU ==")
rm("biyou_hand.jpg")
for n in ["biyou_hero", "biyou_c1", "biyou_c2", "biyou_c3"]:
    p = os.path.join(IMG, n + ".jpg")
    im = ImageOps.exif_transpose(Image.open(p)).transpose(Image.ROTATE_270)  # 90 CW
    im.save(p, "JPEG", quality=82, optimize=True, progressive=True); print("  rotated", n)
print("  poster", render(os.path.join(DOC, "01_BIYOU", "biyou_POSTER.pdf"), 0, os.path.join(IMG, "biyou_poster.jpg"), target=2000), "KB")
print("  calcite", render(os.path.join(DOC, "01_BIYOU", "CALCITE_JORRE.pdf"), 0, os.path.join(IMG, "biyou_calcite.jpg"), target=2000), "KB")

print("== JORRE loop ==")
rm("jorre_portrait.jpg", "jorre_portrait_alt.jpg", "jorre_make.jpg", "jorre_studio.jpg",
   "jorre_workshop.jpg", "jorre_brainstorm.jpg", "jorre_outdoor.jpg")
jfiles = sorted(f for f in glob.glob(os.path.join(DOC, "00_JORRE", "*")) if f.lower().endswith((".jpg", ".jpeg", ".png")))
for i, f in enumerate(jfiles, 1):
    opt(f, os.path.join(IMG, f"jorre_{i:02d}.jpg"), maxedge=1280, q=82)
print(f"  {len(jfiles)} photos -> jorre_01..{len(jfiles):02d}")

print("== AMI report strip ==")
rm("ami_join.jpg", "ami_map.jpg", "ami_customize.jpg", "ami_agenda.jpg", "ami_character.jpg", "ami_chat.jpg")
for old in glob.glob(os.path.join(IMG, "ami_p*.jpg")): os.remove(old)
amipdf = fitz.open(os.path.join(DOC, "03_AMI", "Group18_Endterm_Report.pdf"))
print("  pages", amipdf.page_count, "size", (round(amipdf[0].rect.width), round(amipdf[0].rect.height)))
for i in range(amipdf.page_count):
    p = amipdf[i]; z = 1000 / max(p.rect.width, p.rect.height)
    pix = p.get_pixmap(matrix=fitz.Matrix(z, z))
    Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(os.path.join(IMG, f"ami_p{i+1:02d}.jpg"), "JPEG", quality=80, optimize=True, progressive=True)
amipdf.close(); print(f"  -> ami_p01..{amipdf.page_count:02d}")

print("== REPAIR 3 PNGs ==")
rm("repair_hero.jpg", "repair_decision.jpg", "repair_diagnose.jpg", "repair_dashboard.jpg",
   "repair_phone.jpg", "repair_base.jpg", "repair_eco.jpg", "repair_arch.jpg")
R = os.path.join(DOC, "04_REPAIRAID")
print("  arch", opt(os.path.join(R, "archtiectuyur.png"), os.path.join(IMG, "repair_arch.jpg"), 1700, 85))
print("  ui", opt(os.path.join(R, "stramien poster MP Illustrator.ai (1).png"), os.path.join(IMG, "repair_ui.jpg"), 1700, 85))
print("  phone", opt(os.path.join(R, "stramien poster MP Illustrator.ai.png"), os.path.join(IMG, "repair_phone.jpg"), 1700, 85))

print("== FIRMA video loops ==")
ffsrc = os.path.join(DOC, "05_FIRMA FUNK", "BEELDMATERIAAL")
clips = ["C0176.MP4", "C0204.MP4", "C0212.MP4", "C0230.MP4"]
for i, c in enumerate(clips, 1):
    src = os.path.join(ffsrc, c); dst = os.path.join(VID, f"ff_vid_{i}.mp4")
    poster = os.path.join(IMG, f"ff_vid_{i}.jpg")
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "0", "-t", "8", "-i", src,
                    "-vf", "scale=-2:720", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "30", "-movflags", "+faststart", dst], check=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "1", "-i", src,
                    "-frames:v", "1", "-vf", "scale=-2:720", poster], check=True)
    print(f"  ff_vid_{i}.mp4 {os.path.getsize(dst)//1024}KB  poster {os.path.getsize(poster)//1024}KB")

# Biloo reference montage (to confirm purple vs prototyping grouping)
from PIL import ImageDraw
bl = ["biloo_hero", "biloo_field", "biloo_config", "biloo_top", "biloo_test", "biloo_cad"]
ims = [ImageOps.contain(Image.open(os.path.join(IMG, b + ".jpg")).convert("RGB"), (300, 300)) for b in bl]
sh = Image.new("RGB", (3 * 306 + 6, 2 * 306 + 6), (22, 22, 22)); d = ImageDraw.Draw(sh)
for i, im in enumerate(ims):
    r, c = divmod(i, 3); x = 6 + c * 306; y = 6 + r * 306; sh.paste(im, (x, y))
    d.rectangle([x, y, x + len(bl[i]) * 7 + 6, y + 15], fill=(0, 0, 0)); d.text((x + 3, y + 3), bl[i], fill=(255, 235, 0))
sh.save(os.path.join(IMG, "_sheets", "rev_biloo.jpg"), quality=85)
print("\nDONE")
