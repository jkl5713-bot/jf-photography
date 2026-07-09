/* JF — gallery: blur-up loading + <dialog> lightbox with keyboard + swipe nav */
(() => {
  /* blur-up: fade each image in once decoded */
  document.querySelectorAll('.masonry img, .strip img, .blurup img').forEach(img => {
    if (img.complete && img.naturalWidth) { img.classList.add('is-loaded'); return; }
    img.addEventListener('load', () => img.classList.add('is-loaded'), { once: true });
    img.addEventListener('error', () => img.classList.add('is-loaded'), { once: true });
  });

  /* lightbox */
  const figures = [...document.querySelectorAll('[data-lightbox] figure[data-full]')];
  if (!figures.length) return;

  const dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.setAttribute('aria-label', 'Image viewer');
  dlg.innerHTML = `
    <img alt="">
    <p class="lightbox__cap" hidden></p>
    <div class="lightbox__bar">
      <button type="button" data-act="prev" aria-label="Previous image">&larr; Prev</button>
      <span class="lightbox__count"></span>
      <button type="button" data-act="next" aria-label="Next image">Next &rarr;</button>
      <button type="button" data-act="close" aria-label="Close">Close</button>
    </div>`;
  document.body.append(dlg);
  const pic = dlg.querySelector('img');
  const count = dlg.querySelector('.lightbox__count');
  const cap = dlg.querySelector('.lightbox__cap');
  let idx = 0;

  const show = i => {
    idx = (i + figures.length) % figures.length;
    const fig = figures[idx];
    pic.src = fig.dataset.full;
    pic.alt = fig.querySelector('img')?.alt || '';
    count.textContent = `${idx + 1} / ${figures.length}`;
    const text = fig.querySelector('figcaption')?.textContent?.trim() || '';
    if (text) {
      cap.hidden = false;
      cap.textContent = text;
    } else {
      cap.hidden = true;
      cap.textContent = '';
    }
    /* preload neighbors */
    [idx + 1, idx - 1].forEach(n => {
      const f = figures[(n + figures.length) % figures.length];
      new Image().src = f.dataset.full;
    });
  };

  figures.forEach((fig, i) => {
    fig.setAttribute('tabindex', '0');
    fig.setAttribute('role', 'button');
    fig.setAttribute('aria-label', fig.querySelector('img')?.alt || fig.querySelector('figcaption')?.textContent?.trim() || 'View image');
    const open = () => {
      const go = () => { show(i); dlg.showModal(); };
      (document.startViewTransition ? document.startViewTransition(go) : (go(), null));
    };
    fig.addEventListener('click', open);
    fig.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
  });

  dlg.addEventListener('click', e => {
    const act = e.target.closest('[data-act]')?.dataset.act;
    if (act === 'prev') show(idx - 1);
    else if (act === 'next') show(idx + 1);
    else if (act === 'close' || e.target === dlg) dlg.close();
  });
  dlg.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });

  /* touch swipe (mobile) */
  let tx = 0, ty = 0;
  dlg.addEventListener('touchstart', e => {
    if (!e.changedTouches[0]) return;
    tx = e.changedTouches[0].clientX;
    ty = e.changedTouches[0].clientY;
  }, { passive: true });
  dlg.addEventListener('touchend', e => {
    if (!e.changedTouches[0]) return;
    const dx = e.changedTouches[0].clientX - tx;
    const dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) < 48 || Math.abs(dx) < Math.abs(dy)) return;
    if (dx < 0) show(idx + 1);
    else show(idx - 1);
  }, { passive: true });
})();
