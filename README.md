# Jorre Vrambout — Portfolio 2026

A bold-but-minimalist, single-page portfolio. Black / white / grey, with one accent colour per project. Vanilla HTML, CSS and JavaScript — **no build step**.

```
jorre-portfolio/
├── index.html          # all content & structure
├── css/styles.css      # design system + layout
├── js/main.js          # interactions (cursor, reveals, accent theming, lightbox…)
├── assets/img/         # optimized images (final, web-ready)
├── tools/              # Python scripts that produced the images (fitz + Pillow)
├── vercel.json         # static hosting config (clean URLs + asset caching)
└── README.md
```

## Run it locally
No tooling needed — it's static.

- **VS Code:** install the **Live Server** extension → right-click `index.html` → *Open with Live Server*.
- **Or any static server:** `npx serve .`  (or `python -m http.server 8080`) then open the printed URL.

## Edit the content
Everything is in `index.html`. Each project is a `<section class="project" data-accent="#xxxxxx">` — change the text inside, and the `data-accent` controls that project's colour. Images live in `assets/img/`; swap a file (keep the name) or point the `<img src>` at a new one.

## Re-generate images (optional)
The originals live in `../Portfolio_Doc/`. The scripts in `tools/` render the source PDFs and compress the photos:

```bash
python tools/build_assets.py     # produces the final optimized images
python tools/finalize_repair.py  # renders the Repair Aid slides
```
(Requires `pymupdf` and `Pillow`: `pip install pymupdf Pillow`.)

## Put it online — GitHub → Vercel
1. **Create the repo & push** (in VS Code: *Source Control → Publish to GitHub*), or:
   ```bash
   git init && git add . && git commit -m "Portfolio 2026"
   git branch -M main
   git remote add origin https://github.com/<you>/jorre-portfolio.git
   git push -u origin main
   ```
2. **Deploy:** go to [vercel.com](https://vercel.com) → *Add New… → Project* → import the repo.
   Framework preset: **Other**. Build command: *none*. Output directory: `.` (root). Click **Deploy**.
3. Every `git push` afterwards redeploys automatically.

> Note: this folder lives in OneDrive. Git works fine here, but if a push ever feels stuck, pause OneDrive sync for a moment.
