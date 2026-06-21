/* =========================================================
   Jorre Vrambout — Portfolio 2026  ·  interactions
   ========================================================= */
(() => {
  'use strict';
  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------- Theme ---------- */
  const saved = localStorage.getItem('jv-theme');
  if (saved) root.setAttribute('data-theme', saved);
  $('#themeToggle')?.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('jv-theme', next);
  });

  /* ---------- Loader ---------- */
  const loader = $('#loader'), bar = $('#loaderBar'), pct = $('#loaderPct');
  let p = 0;
  const finish = () => {
    p = 100;
    if (bar) bar.style.width = '100%';
    if (pct) pct.textContent = '100';
    loader?.classList.add('done');
    document.body.classList.add('loaded');
    startReveal();
  };
  if (reduce || !loader) {
    finish();
  } else {
    const tick = setInterval(() => {
      p += Math.random() * 16 + 6;
      if (p >= 100) { clearInterval(tick); finish(); }
      else { if (bar) bar.style.width = p + '%'; if (pct) pct.textContent = Math.floor(p); }
    }, 110);
    setTimeout(() => { clearInterval(tick); finish(); }, 1700);
  }

  /* ---------- Per-project accent (apply locally on load) ---------- */
  const projects = $$('.project');
  projects.forEach(s => {
    const a = s.dataset.accent, on = s.dataset.on;
    if (a) s.style.setProperty('--accent', a);
    if (on) s.style.setProperty('--on-accent', on);
  });

  /* ---------- Reveal on scroll ---------- */
  function startReveal() {
    const items = $$('.reveal, .reveal-lines, .hl');
    if (!('IntersectionObserver' in window)) { items.forEach(i => i.classList.add('in')); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    items.forEach(i => io.observe(i));
  }
  // failsafe: if something blocks the loader, reveal anyway
  setTimeout(() => { if (!document.body.classList.contains('loaded')) finish(); }, 2600);

  /* ---------- Global accent theming + rail/nav active ---------- */
  const railLinks = $$('.rail a');
  const navLinks = $$('.nav__links a');
  const sections = $$('main section[id], footer[id]');
  const setGlobalAccent = (el) => {
    if (el && el.classList.contains('project')) {
      root.style.setProperty('--accent', el.dataset.accent);
      root.style.setProperty('--on-accent', el.dataset.on || '#fff');
    } else {
      root.style.removeProperty('--accent');
      root.style.removeProperty('--on-accent');
    }
  };
  const secObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const id = e.target.id;
      setGlobalAccent(e.target);
      railLinks.forEach(a => a.classList.toggle('active', a.dataset.rail === id));
      // nav active mapping
      const map = { about: 'about', work: 'work', contact: 'contact' };
      let navId = map[id] || (e.target.classList.contains('project') ? 'work' : null);
      navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + navId));
    });
  }, { threshold: 0.001, rootMargin: '-45% 0px -45% 0px' });
  sections.forEach(s => secObserver.observe(s));

  /* ---------- Scroll progress ---------- */
  const prog = $('#progress');
  const onScroll = () => {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    if (prog) prog.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  };
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Custom cursor (asterisk) ---------- */
  const cursor = $('#cursor');
  const fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  if (cursor && fine && !reduce) {
    document.body.classList.add('cursor-on');
    let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y, rot = 0;
    addEventListener('mousemove', (e) => { x = e.clientX; y = e.clientY; }, { passive: true });
    const loop = () => {
      cx += (x - cx) * 0.18; cy += (y - cy) * 0.18;
      rot += 0.4 + Math.hypot(x - cx, y - cy) * 0.25;
      cursor.style.transform = `translate(${cx}px,${cy}px) rotate(${rot}deg)`;
      requestAnimationFrame(loop);
    };
    loop();
    const hoverEls = 'a, button, .shot, .video, .nav__theme';
    $$(hoverEls).forEach(el => {
      el.addEventListener('mouseenter', () => cursor.classList.add('is-hover'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('is-hover'));
    });
    addEventListener('mouseleave', () => cursor.style.opacity = '0');
    addEventListener('mouseenter', () => cursor.style.opacity = '1');
  }

  /* ---------- Count-up stats ---------- */
  const stats = $$('.stat b[data-count]');
  if (stats.length) {
    const co = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target, target = +el.dataset.count, dur = 1400, t0 = performance.now();
        const step = (t) => {
          const k = Math.min((t - t0) / dur, 1);
          const eased = 1 - Math.pow(1 - k, 3);
          el.textContent = Math.round(target * eased);
          if (k < 1) requestAnimationFrame(step);
        };
        if (reduce) el.textContent = target; else requestAnimationFrame(step);
        co.unobserve(el);
      });
    }, { threshold: 0.6 });
    stats.forEach(s => co.observe(s));
  }

  /* ---------- YouTube facade ---------- */
  $$('.video[data-yt]').forEach(v => {
    v.addEventListener('click', () => {
      const id = v.dataset.yt;
      const f = document.createElement('iframe');
      f.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
      f.allow = 'accelerated-sensors; autoplay; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      f.title = 'AMI concept video';
      v.innerHTML = '';
      v.appendChild(f);
    }, { once: true });
  });

  /* ---------- Lightbox ---------- */
  const imgs = $$('.gallery .shot img');
  const lb = $('#lightbox'), lbImg = $('#lbImg'), lbCap = $('#lbCap'), lbCount = $('#lbCount');
  let idx = 0;
  const show = (i) => {
    idx = (i + imgs.length) % imgs.length;
    const im = imgs[idx];
    lbImg.src = im.src; lbImg.alt = im.alt;
    lbCap.textContent = im.alt || '';
    lbCount.textContent = `${idx + 1} / ${imgs.length}`;
  };
  const open = (i) => { show(i); lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false'); };
  const close = () => { lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); };
  imgs.forEach((im, i) => im.addEventListener('click', () => open(i)));
  $('#lbClose')?.addEventListener('click', close);
  $('#lbNext')?.addEventListener('click', () => show(idx + 1));
  $('#lbPrev')?.addEventListener('click', () => show(idx - 1));
  lb?.addEventListener('click', (e) => { if (e.target === lb) close(); });
  addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') show(idx + 1);
    if (e.key === 'ArrowLeft') show(idx - 1);
  });

  /* ---------- Back to top ---------- */
  $('#toTop')?.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));
})();
