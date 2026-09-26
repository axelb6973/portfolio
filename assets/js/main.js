/* =============================================================
   AXAIR — interactions
   Everything degrades to a static page if JS is off, and every
   loop bails out under prefers-reduced-motion.
   ============================================================= */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var raf = window.requestAnimationFrame.bind(window);

  /* ---------- promo bar ---------- */
  var promo = document.getElementById('promo');
  var promoClose = document.getElementById('promoClose');
  if (promo && promoClose) {
    promoClose.addEventListener('click', function () { promo.classList.add('is-closed'); });
  }

  /* ---------- sticky nav shadow ---------- */
  var nav = document.getElementById('nav');

  /* ---------- mobile menu ---------- */
  var burger = document.getElementById('burger');
  var navLinks = document.getElementById('navLinks');
  if (burger && navLinks) {
    burger.addEventListener('click', function () {
      burger.classList.toggle('is-open');
      navLinks.classList.toggle('is-open');
    });
    navLinks.addEventListener('click', function (e) {
      if (e.target.classList.contains('nav__link')) {
        burger.classList.remove('is-open');
        navLinks.classList.remove('is-open');
      }
    });
  }

  /* ---------- nav underline that follows the hovered link ---------- */
  var ink = document.getElementById('navInk');
  if (ink && navLinks) {
    var links = navLinks.querySelectorAll('.nav__link');
    var moveInk = function (el) {
      if (!el) { ink.style.opacity = 0; return; }
      ink.style.opacity = 1;
      ink.style.width = el.offsetWidth + 'px';
      ink.style.transform = 'translateX(' + el.offsetLeft + 'px)';
    };
    links.forEach(function (l) { l.addEventListener('mouseenter', function () { moveInk(l); }); });
    navLinks.addEventListener('mouseleave', function () {
      moveInk(navLinks.querySelector('.nav__link.is-current'));
    });
  }

  /* ---------- split headlines into per-word masked lines ---------- */
  document.querySelectorAll('[data-split]').forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach(function (w, i) {
      var span = document.createElement('span');
      span.className = 'w';
      var inner = document.createElement('i');
      inner.textContent = w;
      inner.style.transitionDelay = (i * 55) + 'ms';
      span.appendChild(inner);
      el.appendChild(span);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
  });

  /* ---------- reveal on scroll (split + generic + counters) ---------- */
  var counters = [];

  function animateCounter(el) {
    var to = parseFloat(el.dataset.to);
    var dec = parseInt(el.dataset.dec || '0', 10);
    var suffix = el.dataset.suffix || '';
    if (reduced) { el.textContent = to.toFixed(dec) + suffix; return; }
    var start = performance.now(), dur = 1400;
    (function tick(now) {
      var t = Math.min(1, (now - start) / dur);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = (to * eased).toFixed(dec) + suffix;
      if (t < 1) raf(tick);
    })(start);
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        var delay = parseInt(el.dataset.delay || '0', 10);
        setTimeout(function () {
          el.classList.add('is-in');
          el.querySelectorAll('.counter').forEach(animateCounter);
          if (el.classList.contains('counter')) animateCounter(el);
        }, reduced ? 0 : delay);
        io.unobserve(el);
      });
    }, { threshold: 0.18, rootMargin: '0px 0px -8% 0px' });

    document.querySelectorAll('[data-reveal],[data-split]').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('[data-reveal],[data-split]').forEach(function (el) { el.classList.add('is-in'); });
    document.querySelectorAll('.counter').forEach(animateCounter);
  }

  /* ---------- single scroll loop: progress bar, parallax, nav, steps ---------- */
  var bar = document.getElementById('scrollBar');
  var parallaxEls = [].slice.call(document.querySelectorAll('[data-parallax]'));
  var steps = document.getElementById('steps');
  var stepsLine = document.getElementById('stepsLine');
  var sections = [].slice.call(document.querySelectorAll('section[id]'));
  var navLinkEls = [].slice.call(document.querySelectorAll('.nav__link'));
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
        var centerOffset = (r.top + r.height / 2 - vh / 2) / vh;
        var amount = parseFloat(el.dataset.parallax) * r.height * centerOffset;
        el.style.transform = 'translate3d(0,' + amount.toFixed(2) + 'px,0)';
      });
    }

    if (steps && stepsLine) {
      var sr = steps.getBoundingClientRect();
      var p = (vh * 0.85 - sr.top) / sr.height;
      stepsLine.style.width = Math.max(0, Math.min(1, p)) * 100 + '%';
    }

    // active nav link
    var current = null;
    sections.forEach(function (s) {
      var r = s.getBoundingClientRect();
      if (r.top <= vh * 0.35 && r.bottom > vh * 0.35) current = s.id;
    });
    navLinkEls.forEach(function (l) {
      l.classList.toggle('is-current', current !== null && l.getAttribute('href') === '#' + current);
    });

    ticking = false;
  }

  function requestScroll() { if (!ticking) { ticking = true; raf(onScroll); } }
  window.addEventListener('scroll', requestScroll, { passive: true });
  window.addEventListener('resize', requestScroll);
  onScroll();

  /* ---------- carousel ---------- */
  (function () {
    var vp = document.getElementById('carViewport');
    if (!vp) return;
    var slides = [].slice.call(vp.querySelectorAll('.slide'));
    var dotsWrap = document.getElementById('carDots');
    var index = 0, timer = null;

    var dots = slides.map(function (_, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-label', 'Vue ' + (i + 1));
      b.addEventListener('click', function () { go(i, true); });
      dotsWrap.appendChild(b);
      return b;
    });

    function go(i, manual) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        s.classList.toggle('is-active', n === index);
        s.setAttribute('aria-hidden', n === index ? 'false' : 'true');
      });
      dots.forEach(function (d, n) { d.classList.toggle('is-active', n === index); });
      if (manual) restart();
    }

    function restart() {
      if (timer) clearInterval(timer);
      if (reduced) return;
      timer = setInterval(function () { go(index + 1); }, 6500);
    }

    document.getElementById('carPrev').addEventListener('click', function () { go(index - 1, true); });
    document.getElementById('carNext').addEventListener('click', function () { go(index + 1, true); });

    // swipe
    var x0 = null;
    vp.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    vp.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) go(index + (dx < 0 ? 1 : -1), true);
      x0 = null;
    });

    // pause when off screen
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { e.isIntersecting ? restart() : (timer && clearInterval(timer)); });
      }, { threshold: 0.25 }).observe(vp);
    } else { restart(); }

    go(0);
  })();

  /* ---------- pointer-driven effects (desktop only) ---------- */
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  if (finePointer && !reduced) {
    /* custom cursor ring, lerped toward the pointer */
    var cursor = document.getElementById('cursor');
    var mx = 0, my = 0, cx = 0, cy = 0;
    document.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY; cursor.classList.add('is-on');
    });
    (function loop() {
      cx += (mx - cx) * 0.18;
      cy += (my - cy) * 0.18;
      cursor.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0)';
      raf(loop);
    })();
    document.querySelectorAll('a,button,[data-tilt]').forEach(function (el) {
      el.addEventListener('mouseenter', function () { cursor.classList.add('is-hot'); });
      el.addEventListener('mouseleave', function () { cursor.classList.remove('is-hot'); });
    });

    /* magnetic buttons */
    document.querySelectorAll('[data-magnetic]').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / r.width;
        var dy = (e.clientY - (r.top + r.height / 2)) / r.height;
        el.style.transform = 'translate(' + (dx * 8).toFixed(2) + 'px,' + (dy * 6).toFixed(2) + 'px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });

    /* card tilt */
    document.querySelectorAll('[data-tilt]').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
        var dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
        el.style.transform =
          'perspective(900px) rotateY(' + (dx * 4).toFixed(2) + 'deg) rotateX(' +
          (-dy * 4).toFixed(2) + 'deg) translateY(-6px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- hero airflow canvas ---------- */
  (function () {
    var cv = document.getElementById('flow');
    if (!cv || reduced) { if (cv) cv.style.display = 'none'; return; }
    var ctx = cv.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = 0, h = 0, parts = [];
    var pointer = { x: -9999, y: -9999 };

    function resize() {
      var r = cv.getBoundingClientRect();
      w = r.width; h = r.height;
      cv.width = w * dpr; cv.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var count = Math.min(140, Math.round(w * h / 12000));
      parts = [];
      for (var i = 0; i < count; i++) {
        parts.push({
          x: Math.random() * w,
          y: Math.random() * h,
          vx: 0.25 + Math.random() * 0.75,
          len: 20 + Math.random() * 70,
          a: 0.08 + Math.random() * 0.3
        });
      }
    }

    cv.addEventListener('mousemove', function (e) {
      var r = cv.getBoundingClientRect();
      pointer.x = e.clientX - r.left; pointer.y = e.clientY - r.top;
    });
    cv.addEventListener('mouseleave', function () { pointer.x = pointer.y = -9999; });

    var visible = true;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { threshold: 0 }).observe(cv);
    }

    function frame() {
      raf(frame);
      if (!visible || !w) return;
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        // pointer pushes the stream aside, like a hand in front of a vent
        var dx = p.x - pointer.x, dy = p.y - pointer.y;
        var d2 = dx * dx + dy * dy;
        if (d2 < 22500) {
          var f = (1 - Math.sqrt(d2) / 150) * 2.2;
          p.y += (dy > 0 ? f : -f);
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
    }

    window.addEventListener('resize', resize);
    resize(); frame();
  })();

  /* ---------- form: client-side validation only, no backend wired ---------- */
  var form = document.getElementById('form');
  var note = document.getElementById('formNote');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = 0;
      form.querySelectorAll('input[required]').forEach(function (i) {
        var empty = !i.value.trim();
        i.closest('.field').classList.toggle('is-bad', empty);
        if (empty) bad++;
      });
      if (bad) {
        note.textContent = 'Merci de compléter les champs requis.';
        note.classList.remove('is-ok');
        return;
      }
      note.textContent = 'Demande enregistrée. Nous rappelons sous 2 h ouvrées.';
      note.classList.add('is-ok');
      form.reset();
    });
  }
})();
