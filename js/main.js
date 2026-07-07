/* JF — shared interactions: nav, cursor, reveals, preloader, magnetic buttons */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = navigator.connection && navigator.connection.saveData === true;

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

  /* ----- nav: blur bar + hide on scroll down ----- */
  const nav = document.querySelector('.nav');
  let lastY = scrollY;
  const onScroll = () => {
    nav.classList.toggle('is-scrolled', scrollY > 40);
    if (!nav.classList.contains('is-open')) {
      nav.classList.toggle('is-hidden', scrollY > lastY && scrollY > 300);
    }
    lastY = scrollY;
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const toggle = document.querySelector('.nav__toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      toggle.textContent = open ? 'Close' : 'Menu';
      toggle.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.querySelectorAll('.nav__links a').forEach(a =>
      a.addEventListener('click', () => {
        nav.classList.remove('is-open');
        toggle.textContent = 'Menu';
        document.body.style.overflow = '';
      }));
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
  if (matchMedia('(pointer: fine)').matches && !reduced) {
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
  if (matchMedia('(pointer: fine)').matches && !reduced) {
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
  const page = location.pathname.split('/').pop();
  if (!['inquire.html', 'thanks.html'].includes(page)) {
    const bar = document.createElement('div');
    bar.className = 'bookbar';
    bar.innerHTML = '<a class="btn btn--solid" href="inquire.html">Check my date <span class="arrow">&rarr;</span></a>' +
      '<a class="btn" href="mailto:jkl81694@gmail.com">Email</a>';
    document.body.append(bar);
    const sentinel = document.querySelector('.hero, .video-hero, .banner, .page-hero');
    const showBar = () => {
      const r = sentinel.getBoundingClientRect();
      bar.classList.toggle('is-on', r.bottom < 0);
    };
    if (sentinel) {
      addEventListener('scroll', showBar, { passive: true });
      showBar();
    }
  }

  /* ----- hover video preview on collection cards ----- */
  if (matchMedia('(pointer: fine)').matches && !reduced && !saveData) {
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

  /* ----- current year ----- */
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
