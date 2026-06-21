"""Finish revision assets: re-render AMI fully, Repair PNGs, Firma videos, Biloo montage.
(Does NOT touch Biyou rotation — already applied.)"""
import os, glob, subprocess
import fitz
from PIL import Image, ImageOps, ImageDraw
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = r"C:\Users\jorre\OneDrive - Universiteit Antwerpen\Documenten\0-PO 2025-2026\00_Portfolio"
DOC = os.path.join(BASE, "Portfolio_Doc")
IMG = os.path.join(BASE, "jorre-portfolio", "assets", "img")
VID = os.path.join(BASE, "jorre-portfolio", "assets", "video"); os.makedirs(VID, exist_ok=True)


def opt(src, dst, maxedge=1600, q=82):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((maxedge, maxedge), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    return os.path.getsize(dst) // 1024


print("== AMI report strip (full) ==")
for old in glob.glob(os.path.join(IMG, "ami_p*.jpg")): os.remove(old)
d = fitz.open(os.path.join(DOC, "03_AMI", "Group18_Endterm_Report.pdf"))
n = d.page_count
print("  page_count =", n, "first size", (round(d[0].rect.width), round(d[0].rect.height)))
for i in range(n):
    p = d[i]; z = 1200 / max(p.rect.width, p.rect.height)
    pix = p.get_pixmap(matrix=fitz.Matrix(z, z))
    Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(
        os.path.join(IMG, f"ami_p{i+1:02d}.jpg"), "JPEG", quality=80, optimize=True, progressive=True)
d.close(); print(f"  -> ami_p01..{n:02d}")

print("== REPAIR 3 PNGs ==")
for nm in ["repair_hero", "repair_decision", "repair_diagnose", "repair_dashboard", "repair_phone", "repair_base", "repair_eco", "repair_arch", "repair_ui"]:
    p = os.path.join(IMG, nm + ".jpg")
    if os.path.exists(p): os.remove(p)
R = os.path.join(DOC, "04_REPAIRAID")
print("  arch", opt(os.path.join(R, "archtiectuyur.png"), os.path.join(IMG, "repair_arch.jpg"), 1700, 85))
print("  ui", opt(os.path.join(R, "stramien poster MP Illustrator.ai (1).png"), os.path.join(IMG, "repair_ui.jpg"), 1700, 85))
print("  phone", opt(os.path.join(R, "stramien poster MP Illustrator.ai.png"), os.path.join(IMG, "repair_phone.jpg"), 1700, 85))

print("== FIRMA video loops ==")
ffsrc = os.path.join(DOC, "05_FIRMA FUNK", "BEELDMATERIAAL")
for i, c in enumerate(["C0176.MP4", "C0204.MP4", "C0212.MP4", "C0230.MP4"], 1):
    src = os.path.join(ffsrc, c); dst = os.path.join(VID, f"ff_vid_{i}.mp4"); poster = os.path.join(IMG, f"ff_vid_{i}.jpg")
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "0", "-t", "8", "-i", src, "-vf", "scale=-2:720",
                    "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "30", "-movflags", "+faststart", dst], check=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "1", "-i", src, "-frames:v", "1", "-vf", "scale=-2:720", poster], check=True)
    print(f"  ff_vid_{i}.mp4 {os.path.getsize(dst)//1024}KB  poster {os.path.getsize(poster)//1024}KB")

print("== BILOO montage ==")
bl = ["biloo_hero", "biloo_field", "biloo_config", "biloo_top", "biloo_test", "biloo_cad"]
ims = [ImageOps.contain(Image.open(os.path.join(IMG, b + ".jpg")).convert("RGB"), (300, 300)) for b in bl]
sh = Image.new("RGB", (3 * 306 + 6, 2 * 306 + 6), (22, 22, 22)); dr = ImageDraw.Draw(sh)
for i, im in enumerate(ims):
    r, c = divmod(i, 3); x = 6 + c * 306; y = 6 + r * 306; sh.paste(im, (x, y))
    dr.rectangle([x, y, x + len(bl[i]) * 7 + 6, y + 15], fill=(0, 0, 0)); dr.text((x + 3, y + 3), bl[i], fill=(255, 235, 0))
sh.save(os.path.join(IMG, "_sheets", "rev_biloo.jpg"), quality=85)
print("DONE")
