/* =========================================================
   Jorre Vrambout — Portfolio 2026 · interactions
   ========================================================= */
(() => {
  'use strict';
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* theme */
  const saved = localStorage.getItem('jv-theme');
  if (saved) root.setAttribute('data-theme', saved);
  $('#themeToggle')?.addEventListener('click', () => {
    const n = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', n); localStorage.setItem('jv-theme', n);
  });

  /* loader */
  const loader = $('#loader'), bar = $('#loaderBar'), pct = $('#loaderPct');
  let p = 0;
  const finish = () => {
    if (bar) bar.style.width = '100%'; if (pct) pct.textContent = '100';
    loader?.classList.add('done'); document.body.classList.add('loaded'); startReveal();
  };
  if (reduce || !loader) finish();
  else {
    const t = setInterval(() => {
      p += Math.random() * 16 + 7;
      if (p >= 100) { clearInterval(t); finish(); }
      else { if (bar) bar.style.width = p + '%'; if (pct) pct.textContent = Math.floor(p); }
    }, 105);
    setTimeout(() => { clearInterval(t); finish(); }, 1700);
  }
  setTimeout(() => { if (!document.body.classList.contains('loaded')) finish(); }, 2600);

  /* reveal */
  function startReveal() {
    const items = $$('.reveal, .reveal-lines, .hl');
    if (!('IntersectionObserver' in window)) { items.forEach(i => i.classList.add('in')); return; }
    const io = new IntersectionObserver((es) => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    items.forEach(i => io.observe(i));
  }

  /* skill dots */
  $$('.dots').forEach(d => {
    const n = +d.dataset.level || 0; let h = '';
    for (let i = 0; i < 5; i++) h += `<i class="${i < n ? 'on' : ''}"></i>`;
    d.innerHTML = h;
  });

  /* photo loop */
  (() => {
    const box = $('#photoLoop'); if (!box) return;
    const total = 19;
    const srcs = Array.from({ length: total }, (_, i) => `assets/img/jorre_${String(i + 1).padStart(2, '0')}.jpg`);
    const layers = $$('.loop__img', box); const idxEl = $('#loopIndex'); $('#loopTotal').textContent = total;
    let i = 0, front = 0;
    layers[0].src = srcs[0];
    const step = () => {
      const next = (i + 1) % total; const back = 1 - front;
      layers[back].src = srcs[next];
      layers[back].onload = () => {
        layers[back].classList.add('is-on'); layers[front].classList.remove('is-on');
        front = back; i = next; if (idxEl) idxEl.textContent = String(i + 1).padStart(2, '0');
      };
    };
    if (!reduce) setInterval(step, 3000);
  })();

  /* lazy media loader */
  function loadMedia(scope) {
    $$('img[data-src]', scope).forEach(im => { im.src = im.dataset.src; im.removeAttribute('data-src'); });
    $$('video[data-src]', scope).forEach(v => {
      const s = document.createElement('source'); s.src = v.dataset.src; s.type = 'video/mp4';
      v.appendChild(s); v.removeAttribute('data-src'); v.load();
    });
  }
  const playVids = (scope, on) => $$('video', scope).forEach(v => { on ? v.play().catch(() => {}) : v.pause(); });

  /* count-up */
  function countUp(scope) {
    $$('.stat b[data-count]', scope).forEach(el => {
      if (el.dataset.done) return; el.dataset.done = '1';
      const target = +el.dataset.count, dur = 1300, t0 = performance.now();
      if (reduce) { el.textContent = target; return; }
      const s = (t) => { const k = Math.min((t - t0) / dur, 1); el.textContent = Math.round(target * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(s); };
      requestAnimationFrame(s);
    });
  }

  /* project expand / collapse */
  const projects = $$('.proj');
  const setAccent = (el) => {
    if (el) { root.style.setProperty('--accent', el.dataset.accent); root.style.setProperty('--on-accent', el.dataset.on || '#fff'); }
    else { root.style.removeProperty('--accent'); root.style.removeProperty('--on-accent'); }
  };
  projects.forEach(pr => {
    const btn = $('.proj__bar', pr), detail = $('.proj__detail', pr);
    btn.addEventListener('click', () => {
      const open = pr.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) { loadMedia(detail); countUp(detail); setAccent(pr); setTimeout(() => playVids(detail, true), 400); }
      else playVids(detail, false);
    });
  });

  /* Firma videos: play when in view, pause when out (and once a source exists) */
  if (!reduce) {
    const vio = new IntersectionObserver((es) => es.forEach(e => {
      const v = e.target;
      if (e.isIntersecting && v.children.length) v.play().catch(() => {});
      else v.pause();
    }), { threshold: 0.25 });
    $$('.vid video').forEach(v => vio.observe(v));
  }

  /* global accent theming by section / project in view */
  const secs = [...projects, ...$$('main > section:not(.work), footer')];
  const io2 = new IntersectionObserver((es) => es.forEach(e => {
    if (!e.isIntersecting) return;
    setAccent(e.target.classList.contains('proj') ? e.target : null);
    const id = e.target.id;
    $$('.nav__links a').forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + id));
  }), { rootMargin: '-45% 0px -45% 0px' });
  secs.forEach(s => io2.observe(s));

  /* scroll progress */
  const prog = $('#progress');
  addEventListener('scroll', () => {
    const h = document.documentElement, max = h.scrollHeight - h.clientHeight;
    if (prog) prog.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  }, { passive: true });

  /* AMI horizontal strip: vertical wheel -> horizontal */
  const strip = $('#amiStrip');
  strip?.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) { strip.scrollLeft += e.deltaY; e.preventDefault(); }
  }, { passive: false });

  /* embedded YouTube facade (plays inside the page, works on static hosting) */
  $$('.ytembed').forEach(yt => {
    yt.addEventListener('click', () => {
      const f = document.createElement('iframe');
      f.src = `https://www.youtube-nocookie.com/embed/${yt.dataset.yt}?autoplay=1&rel=0`;
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true; f.title = 'AMI concept film';
      yt.innerHTML = ''; yt.appendChild(f);
    }, { once: true });
  });

  /* custom cursor */
  const cursor = $('#cursor');
  if (cursor && matchMedia('(hover:hover) and (pointer:fine)').matches && !reduce) {
    document.body.classList.add('cursor-on');
    let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y, rot = 0;
    addEventListener('mousemove', (e) => { x = e.clientX; y = e.clientY; }, { passive: true });
    (function loop() {
      cx += (x - cx) * 0.18; cy += (y - cy) * 0.18;
      rot += 0.4 + Math.hypot(x - cx, y - cy) * 0.25;
      cursor.style.transform = `translate(${cx}px,${cy}px) rotate(${rot}deg)`;
      requestAnimationFrame(loop);
    })();
    const mark = () => $$('a,button,.shot,.vid,.hstrip img,.nav__theme').forEach(el => {
      el.addEventListener('mouseenter', () => cursor.classList.add('is-hover'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('is-hover'));
    });
    mark();
    addEventListener('mouseleave', () => cursor.style.opacity = '0');
    addEventListener('mouseenter', () => cursor.style.opacity = '1');
  }

  /* lightbox (gallery + strip images) */
  const lb = $('#lightbox'), lbImg = $('#lbImg'), lbCap = $('#lbCap'), lbCount = $('#lbCount');
  let imgs = [], idx = 0;
  const collect = () => { imgs = $$('.shot img, .hstrip img'); };
  const show = (i) => {
    idx = (i + imgs.length) % imgs.length; const im = imgs[idx];
    lbImg.src = im.currentSrc || im.src; lbImg.alt = im.alt; lbCap.textContent = im.alt || '';
    lbCount.textContent = `${idx + 1} / ${imgs.length}`;
  };
  document.addEventListener('click', (e) => {
    const im = e.target.closest('.shot img, .hstrip img');
    if (!im || !im.src) return;
    collect(); const i = imgs.indexOf(im); if (i < 0) return;
    show(i); lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false');
  });
  const close = () => { lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); };
  $('#lbClose')?.addEventListener('click', close);
  $('#lbNext')?.addEventListener('click', () => show(idx + 1));
  $('#lbPrev')?.addEventListener('click', () => show(idx - 1));
  lbImg?.addEventListener('click', (e) => { e.stopPropagation(); show(idx + 1); });
  lb?.addEventListener('click', (e) => { if (e.target === lb) close(); });
  addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show(idx + 1); if (e.key === 'ArrowLeft') show(idx - 1);
  });

  $('#toTop')?.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));

  /* contact word cycle: Design / build / create in accent colours */
  const ws = $('#wordSwap');
  if (ws && !reduce) {
    const words = ['Design', 'build', 'create'];
    const cols = ['--c1', '--c2', '--c3', '--c5'];
    let k = 0;
    setInterval(() => {
      k++; ws.style.opacity = '0';
      setTimeout(() => {
        ws.textContent = words[k % words.length];
        ws.style.color = `var(${cols[k % cols.length]})`;
        ws.style.opacity = '1';
      }, 220);
    }, 2200);
  }
})();
