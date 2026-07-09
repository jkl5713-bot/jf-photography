/* JF — shared interactions: nav, cursor, reveals, preloader, magnetic buttons */
(() => {
  document.documentElement.classList.add('js');

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = navigator.connection && navigator.connection.saveData === true;
  const fine = matchMedia('(pointer: fine)').matches;

  /* owner-maintained: keep this line TRUE — edit as dates book up */
  const AVAILABILITY = 'Now booking fall ’26 seniors & 2027 weddings';
  document.querySelectorAll('[data-avail]').forEach(el => { el.textContent = AVAILABILITY; });

  /* ----- preloader (first visit per session only) ----- */
  const pre = document.querySelector('.preloader');
  if (pre) {
    if (sessionStorage.getItem('jf-seen') || reduced) {
      pre.remove();
    } else {
      sessionStorage.setItem('jf-seen', '1');
      addEventListener('load', () => {
        setTimeout(() => pre.classList.add('is-done'), 900);
        setTimeout(() => pre.remove(), 1700);
      });
      /* hard fallback so the page can never stay covered */
      setTimeout(() => { pre.classList.add('is-done'); setTimeout(() => pre.remove(), 700); }, 3500);
    }
  }

  /* ----- grain off for save-data / reduced motion ----- */
  const grain = document.querySelector('.grain');
  if (grain && (saveData || reduced)) grain.classList.add('is-off');

  /* ----- nav: blur bar + hide on scroll down ----- */
  const nav = document.querySelector('.nav');
  let lastY = scrollY;
  const onScroll = () => {
    if (!nav) return;
    nav.classList.toggle('is-scrolled', scrollY > 40);
    if (!nav.classList.contains('is-open')) {
      nav.classList.toggle('is-hidden', scrollY > lastY && scrollY > 300);
    }
    lastY = scrollY;
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ----- mobile menu ----- */
  const toggle = document.querySelector('.nav__toggle');
  const closeMenu = () => {
    if (!nav || !toggle) return;
    nav.classList.remove('is-open');
    toggle.textContent = 'Menu';
    toggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-open');
  };
  if (toggle && nav) {
    toggle.setAttribute('aria-controls', 'primary-nav');
    toggle.setAttribute('aria-label', 'Open menu');
    const links = nav.querySelector('.nav__links');
    if (links) links.id = 'primary-nav';

    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      toggle.textContent = open ? 'Close' : 'Menu';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('nav-open', open);
      if (open) {
        const first = nav.querySelector('.nav__links a');
        if (first) first.focus({ preventScroll: true });
      }
    });
    nav.querySelectorAll('.nav__links a').forEach(a => a.addEventListener('click', closeMenu));
    addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        closeMenu();
        toggle.focus();
      }
    });
  }

  /* ----- reveal fallback for browsers without scroll-driven animations ----- */
  if (!CSS.supports('animation-timeline: view()')) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  }

  /* ----- custom cursor ----- */
  if (fine && !reduced) {
    const dot = Object.assign(document.createElement('div'), { className: 'cursor-dot' });
    const ring = Object.assign(document.createElement('div'), { className: 'cursor-ring' });
    document.body.append(dot, ring);
    let x = innerWidth / 2, y = innerHeight / 2, rx = x, ry = y;
    addEventListener('pointermove', e => { x = e.clientX; y = e.clientY; dot.style.translate = `${x}px ${y}px`; });
    (function raf() {
      rx += (x - rx) * 0.16; ry += (y - ry) * 0.16;
      ring.style.translate = `${rx}px ${ry}px`;
      requestAnimationFrame(raf);
    })();
    document.addEventListener('pointerover', e => {
      ring.classList.toggle('is-view', !!e.target.closest('.masonry figure, .strip figure, .col-card__media'));
      ring.classList.toggle('is-hover', !!e.target.closest('a, button, input, select, textarea, label'));
    });
  }

  /* ----- magnetic buttons ----- */
  if (fine && !reduced) {
    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('pointermove', e => {
        const r = btn.getBoundingClientRect();
        const mx = (e.clientX - r.left - r.width / 2) * 0.18;
        const my = (e.clientY - r.top - r.height / 2) * 0.3;
        btn.style.translate = `${mx}px ${my}px`;
      });
      btn.addEventListener('pointerleave', () => { btn.style.translate = ''; });
    });
  }

  /* ----- hero title line stagger ----- */
  document.querySelectorAll('.hero__title .line > span').forEach((s, i) =>
    s.style.setProperty('--d', `${0.12 + i * 0.14}s`));

  /* ----- ticker: duplicate track for seamless loop ----- */
  document.querySelectorAll('.ticker').forEach(t => {
    const track = t.querySelector('.ticker__track');
    if (track) t.append(track.cloneNode(true));
  });

  /* ----- film strip: drag-to-scroll + arrow buttons ----- */
  document.querySelectorAll('.strip').forEach(strip => {
    /* wrap with shell + prev/next if not already */
    if (!strip.parentElement.classList.contains('strip-shell')) {
      const shell = document.createElement('div');
      shell.className = 'strip-shell';
      strip.parentNode.insertBefore(shell, strip);
      shell.append(strip);
      const prev = Object.assign(document.createElement('button'), {
        className: 'strip__btn strip__btn--prev', type: 'button',
        innerHTML: '&#8592;',
      });
      prev.setAttribute('aria-label', 'Scroll gallery left');
      const next = Object.assign(document.createElement('button'), {
        className: 'strip__btn strip__btn--next', type: 'button',
        innerHTML: '&#8594;',
      });
      next.setAttribute('aria-label', 'Scroll gallery right');
      shell.prepend(prev);
      shell.append(next);

      const step = () => Math.min(strip.clientWidth * 0.78, 560);
      const sync = () => {
        const max = strip.scrollWidth - strip.clientWidth - 2;
        prev.disabled = strip.scrollLeft <= 2;
        next.disabled = strip.scrollLeft >= max;
      };
      prev.addEventListener('click', () => strip.scrollBy({ left: -step(), behavior: reduced ? 'auto' : 'smooth' }));
      next.addEventListener('click', () => strip.scrollBy({ left: step(), behavior: reduced ? 'auto' : 'smooth' }));
      strip.addEventListener('scroll', sync, { passive: true });
      addEventListener('resize', sync, { passive: true });
      sync();
    }

    /* pointer drag (desktop "drag or scroll") */
    if (!fine) return;
    let down = false, startX = 0, startScroll = 0, moved = 0;
    strip.addEventListener('pointerdown', e => {
      if (e.pointerType === 'touch') return;
      if (e.button !== 0) return;
      down = true; moved = 0;
      startX = e.clientX; startScroll = strip.scrollLeft;
      strip.classList.add('is-dragging');
      strip.setPointerCapture?.(e.pointerId);
    });
    strip.addEventListener('pointermove', e => {
      if (!down) return;
      const dx = e.clientX - startX;
      moved = Math.max(moved, Math.abs(dx));
      strip.scrollLeft = startScroll - dx;
    });
    const endDrag = e => {
      if (!down) return;
      down = false;
      strip.classList.remove('is-dragging');
      /* suppress click if user actually dragged */
      if (moved > 6) {
        const block = ev => { ev.preventDefault(); ev.stopPropagation(); };
        strip.addEventListener('click', block, { capture: true, once: true });
      }
    };
    strip.addEventListener('pointerup', endDrag);
    strip.addEventListener('pointercancel', endDrag);
  });

  /* ----- lazy background videos: fetch on approach, pause offscreen ----- */
  const vids = [...document.querySelectorAll('video[data-lazy]')];
  if (vids.length) {
    const vh = () => Math.max(innerHeight, document.documentElement.clientHeight, 800);
    const checkVids = () => vids.forEach(v => {
      const r = v.getBoundingClientRect();
      const near = r.top < vh() + 240 && r.bottom > -240;
      if (near) {
        if (!v.src && !saveData) v.src = v.dataset.lazy;
        if (!reduced && v.src && v.paused) v.play().catch(() => {});
      } else if (!v.paused) {
        v.pause();
      }
    });
    addEventListener('scroll', checkVids, { passive: true });
    addEventListener('resize', checkVids, { passive: true });
    checkVids();
  }

  /* ----- sticky mobile booking bar ----- */
  const page = (location.pathname.split('/').pop() || 'index.html');
  if (!['inquire.html', 'thanks.html'].includes(page)) {
    const bar = document.createElement('div');
    bar.className = 'bookbar';
    bar.innerHTML = '<a class="btn btn--solid" href="inquire.html">Check my date <span class="arrow">&rarr;</span></a>' +
      '<a class="btn" href="mailto:jkl81694@gmail.com">Email</a>';
    document.body.append(bar);
    const sentinel = document.querySelector('.hero, .video-hero, .banner, .page-hero');
    const showBar = () => {
      if (!sentinel) return;
      const r = sentinel.getBoundingClientRect();
      bar.classList.toggle('is-on', r.bottom < 0);
    };
    if (sentinel) {
      addEventListener('scroll', showBar, { passive: true });
      showBar();
    }
  }

  /* ----- back to top ----- */
  const topBtn = Object.assign(document.createElement('button'), {
    className: 'to-top', type: 'button', innerHTML: '&#8593;',
  });
  topBtn.setAttribute('aria-label', 'Back to top');
  document.body.append(topBtn);
  const syncTop = () => topBtn.classList.toggle('is-on', scrollY > innerHeight * 1.2);
  addEventListener('scroll', syncTop, { passive: true });
  syncTop();
  topBtn.addEventListener('click', () => {
    scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
  });

  /* ----- hover video preview on collection cards ----- */
  if (fine && !reduced && !saveData) {
    document.querySelectorAll('.card-vid').forEach(v => {
      const host = v.closest('.col-card__media');
      if (!host) return;
      const start = () => {
        if (!v.src) v.src = v.dataset.hoverSrc;
        v.play().then(() => v.classList.add('is-playing')).catch(() => {});
      };
      const stop = () => { v.pause(); v.classList.remove('is-playing'); };
      host.addEventListener('pointerenter', start);
      host.addEventListener('pointerleave', stop);
      host.addEventListener('focusin', start);
      host.addEventListener('focusout', stop);
    });
  }

  /* ----- film embed facade (activates when data-yt is set) ----- */
  document.querySelectorAll('.film-embed[data-yt]').forEach(f => {
    if (!f.dataset.yt || f.dataset.yt === 'VIDEO_ID') return;
    const play = () => {
      f.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${f.dataset.yt}?autoplay=1&rel=0"
        allow="autoplay; fullscreen" allowfullscreen title="Wedding highlight film"
        style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>`;
    };
    f.addEventListener('click', play, { once: true });
    f.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); play(); } });
  });

  /* ----- inquire form busy state ----- */
  document.querySelectorAll('form.form').forEach(form => {
    form.addEventListener('submit', () => {
      form.classList.add('is-sending');
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.setAttribute('aria-busy', 'true');
        if (!btn.dataset.label) btn.dataset.label = btn.innerHTML;
        btn.innerHTML = 'Sending…';
      }
    });
  });

  /* ----- idle prefetch of high-intent pages ----- */
  const prefetch = href => {
    if (document.querySelector(`link[rel="prefetch"][href="${href}"]`)) return;
    const l = document.createElement('link');
    l.rel = 'prefetch';
    l.href = href;
    document.head.append(l);
  };
  const idle = window.requestIdleCallback || (cb => setTimeout(cb, 1200));
  idle(() => {
    if (page !== 'inquire.html') prefetch('inquire.html');
    if (page === 'index.html' || page === '' || page === '/') {
      prefetch('seniors.html');
      prefetch('weddings.html');
      prefetch('pricing.html');
    }
  });

  /* ----- current year ----- */
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
