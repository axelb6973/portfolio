/* =============================================================
   ACDC — interactions
   Sans dependance. La page reste lisible et navigable sans JS,
   et chaque boucle s'arrete sous prefers-reduced-motion.
   ============================================================= */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var raf = window.requestAnimationFrame.bind(window);

  /* ---------- menu mobile ---------- */
  var burger = document.getElementById('burger');
  var mobileNav = document.getElementById('mobileNav');
  if (burger && mobileNav) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') !== 'true';
      burger.setAttribute('aria-expanded', String(open));
      mobileNav.style.maxHeight = open ? mobileNav.scrollHeight + 'px' : '0px';
      var bars = burger.children;
      bars[0].style.transform = open ? 'translateY(3px) rotate(45deg)' : '';
      bars[1].style.transform = open ? 'translateY(-3px) rotate(-45deg)' : '';
    });
  }

  /* ---------- soulignement de nav qui suit le survol ---------- */
  var ink = document.getElementById('navInk');
  var navLinks = document.getElementById('navLinks');
  if (ink && navLinks) {
    navLinks.querySelectorAll('.nav-link').forEach(function (l) {
      l.addEventListener('mouseenter', function () {
        ink.style.opacity = 1;
        ink.style.width = l.offsetWidth + 'px';
        ink.style.transform = 'translateX(' + l.offsetLeft + 'px)';
      });
    });
    navLinks.addEventListener('mouseleave', function () { ink.style.opacity = 0; });
  }

  /* ---------- titres decoupes en mots, reveles sous masque ---------- */
  document.querySelectorAll('[data-split]').forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach(function (w, i) {
      var span = document.createElement('span');
      span.className = 'w';
      var inner = document.createElement('i');
      inner.textContent = w;
      inner.style.transitionDelay = Math.min(i * 40, 480) + 'ms';
      span.appendChild(inner);
      el.appendChild(span);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
  });

  /* ---------- compteurs ---------- */
  function animateCounter(el) {
    var to = parseFloat(el.dataset.to);
    var suffix = el.dataset.suffix || '';
    if (reduced) { el.textContent = to + suffix; return; }
    var start = performance.now(), dur = 1400;
    (function tick(now) {
      var t = Math.min(1, (now - start) / dur);
      el.textContent = Math.round(to * (1 - Math.pow(1 - t, 3))) + suffix;
      if (t < 1) raf(tick);
    })(start);
  }

  /* ---------- apparition au scroll ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        setTimeout(function () {
          el.classList.add('is-in');
          if (el.classList.contains('counter')) animateCounter(el);
          el.querySelectorAll('.counter').forEach(animateCounter);
        }, reduced ? 0 : parseInt(el.dataset.delay || '0', 10));
        io.unobserve(el);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('[data-reveal],[data-split]').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('[data-reveal],[data-split]').forEach(function (el) { el.classList.add('is-in'); });
    document.querySelectorAll('.counter').forEach(animateCounter);
  }

  /* ---------- une seule boucle de scroll ---------- */
  var bar = document.getElementById('scrollBar');
  var nav = document.getElementById('nav');
  var parallaxEls = [].slice.call(document.querySelectorAll('[data-parallax]'));
  var ticking = false;

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    var vh = window.innerHeight;
    var max = document.documentElement.scrollHeight - vh;

    if (bar) bar.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
    if (nav) nav.classList.toggle('is-stuck', y > 8);

    if (!reduced) {
      parallaxEls.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var offset = (r.top + r.height / 2 - vh / 2) / vh;
        var amount = parseFloat(el.dataset.parallax) * r.height * offset;
        el.style.transform = 'translate3d(0,' + amount.toFixed(2) + 'px,0)';
      });
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; raf(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- effets au pointeur (souris uniquement) ---------- */
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches && !reduced) {
    var cursor = document.getElementById('cursor');
    if (cursor) {
      var mx = 0, my = 0, cx = 0, cy = 0;
      document.addEventListener('mousemove', function (e) {
        mx = e.clientX; my = e.clientY; cursor.classList.add('is-on');
      });
      (function loop() {
        cx += (mx - cx) * 0.18; cy += (my - cy) * 0.18;
        cursor.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0)';
        raf(loop);
      })();
      document.querySelectorAll('a,button,[data-tilt],.tile').forEach(function (el) {
        el.addEventListener('mouseenter', function () { cursor.classList.add('is-hot'); });
        el.addEventListener('mouseleave', function () { cursor.classList.remove('is-hot'); });
      });
    }

    document.querySelectorAll('[data-magnetic]').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / r.width;
        var dy = (e.clientY - (r.top + r.height / 2)) / r.height;
        el.style.transform = 'translate(' + (dx * 8).toFixed(2) + 'px,' + (dy * 6).toFixed(2) + 'px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });

    document.querySelectorAll('[data-tilt]').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
        var dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
        el.style.transform = 'perspective(900px) rotateY(' + (dx * 4).toFixed(2) +
          'deg) rotateX(' + (-dy * 4).toFixed(2) + 'deg) translateY(-6px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- flux d'air du hero ---------- */
  (function () {
    var cv = document.getElementById('flow');
    if (!cv) return;
    if (reduced) { cv.style.display = 'none'; return; }
    var ctx = cv.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = 0, h = 0, parts = [], visible = true;
    var pointer = { x: -9999, y: -9999 };

    function resize() {
      var r = cv.getBoundingClientRect();
      w = r.width; h = r.height;
      cv.width = w * dpr; cv.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      parts = [];
      var count = Math.min(120, Math.round(w * h / 14000));
      for (var i = 0; i < count; i++) {
        parts.push({
          x: Math.random() * w, y: Math.random() * h,
          vx: 0.25 + Math.random() * 0.75,
          len: 20 + Math.random() * 70,
          a: 0.07 + Math.random() * 0.26
        });
      }
    }

    cv.addEventListener('mousemove', function (e) {
      var r = cv.getBoundingClientRect();
      pointer.x = e.clientX - r.left; pointer.y = e.clientY - r.top;
    });
    cv.addEventListener('mouseleave', function () { pointer.x = pointer.y = -9999; });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { threshold: 0 }).observe(cv);
    }

    (function frame() {
      raf(frame);
      if (!visible || !w) return;
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        // le curseur ecarte le flux, comme une main devant une bouche d'air
        var dx = p.x - pointer.x, dy = p.y - pointer.y;
        var d2 = dx * dx + dy * dy;
        if (d2 < 22500) {
          var f = (1 - Math.sqrt(d2) / 150) * 2.2;
          p.y += dy > 0 ? f : -f;
        }
        p.x += p.vx;
        if (p.x - p.len > w) { p.x = -p.len; p.y = Math.random() * h; }
        ctx.strokeStyle = 'rgba(0,112,213,' + p.a + ')';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(p.x - p.len, p.y);
        ctx.lineTo(p.x, p.y);
        ctx.stroke();
      }
    })();

    window.addEventListener('resize', resize);
    resize();
  })();

  /* ---------- lightbox galerie ---------- */
  (function () {
    var box = document.getElementById('lightbox');
    var gallery = document.getElementById('gallery');
    if (!box || !gallery) return;
    var img = document.getElementById('lbImg');
    var cap = document.getElementById('lbCap');
    var tiles = [].slice.call(gallery.querySelectorAll('.tile'));
    var index = 0, opener = null;

    function show(i) {
      index = (i + tiles.length) % tiles.length;
      var source = tiles[index].querySelector('img');
      img.src = source.currentSrc || source.src;
      img.alt = source.alt;
      cap.textContent = tiles[index].querySelector('figcaption').textContent;
      box.hidden = false;
      document.body.style.overflow = 'hidden';
      document.getElementById('lbClose').focus();
    }
    function close() {
      box.hidden = true;
      img.src = '';
      document.body.style.overflow = '';
      if (opener) opener.focus();
    }

    function openFrom(tile) { opener = tile; show(tiles.indexOf(tile)); }
    gallery.addEventListener('click', function (e) {
      var tile = e.target.closest('.tile');
      if (tile) openFrom(tile);
    });
    gallery.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var tile = e.target.closest('.tile');
      if (!tile) return;
      e.preventDefault();
      openFrom(tile);
    });

    document.getElementById('lbClose').addEventListener('click', close);
    document.getElementById('lbPrev').addEventListener('click', function () { show(index - 1); });
    document.getElementById('lbNext').addEventListener('click', function () { show(index + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (box.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
      if (e.key === 'Tab') {
        // piege a focus : la lightbox est modale
        var btns = box.querySelectorAll('button');
        var first = btns[0], last = btns[btns.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  })();

  /* ---------- formulaires ----------
     Validation cote client uniquement : l'endpoint est un placeholder,
     rien n'est envoye tant qu'il n'est pas renseigne. */
  document.querySelectorAll('[data-form]').forEach(function (form) {
    var note = form.querySelector('[data-note]');

    function markError(field, message) {
      field.closest('.field').classList.add('is-bad');
      field.setAttribute('aria-invalid', 'true');
      return message;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var problems = [];
      form.querySelectorAll('[required]').forEach(function (i) {
        var wrap = i.closest('.field');
        wrap.classList.remove('is-bad');
        i.removeAttribute('aria-invalid');
        if (!i.value.trim()) {
          problems.push(markError(i, 'required'));
        } else if (i.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(i.value)) {
          problems.push(markError(i, 'email'));
        }
      });

      note.classList.remove('text-signal-blue', 'text-iron');
      if (problems.length) {
        note.textContent = 'Please check the highlighted fields.';
        note.classList.add('text-iron');
        form.querySelector('.is-bad input, .is-bad select, .is-bad textarea').focus();
        return;
      }
      note.textContent = 'Demo form — no endpoint is connected yet.';
      note.classList.add('text-signal-blue');
    });
  });
})();
