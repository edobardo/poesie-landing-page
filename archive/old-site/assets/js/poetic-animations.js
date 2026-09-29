/**
 * poetic-animations.js
 * Thematic animation layer for Poesie Landing Page.
 * Systems: Typewriter Hero · Ink-Dry Subtitle · Hand-Drawn SVG Hovers · Journal Scroll Reveals
 */

(function () {
  'use strict';

  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ============================================================
   * 1. TYPEWRITER HERO ENTRANCE
   *    Types out the h1 text character by character,
   *    then fades in the cursor to a gentle blink.
   * ============================================================ */
  function initTypewriter() {
    var el = document.getElementById('heroTitle');
    if (!el) return;

    /* Capture original text — preserve any <br> as a real newline */
    var rawHTML = el.innerHTML; // e.g. "Every feeling,<br>written down."
    /* Build an array of tokens: characters or <br> markers */
    var tokens = [];
    var tmp = document.createElement('div');
    tmp.innerHTML = rawHTML;

    function tokenizeNode(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        node.textContent.split('').forEach(function (ch) {
          tokens.push({ type: 'char', value: ch });
        });
      } else if (node.nodeName === 'BR') {
        tokens.push({ type: 'br' });
      } else {
        node.childNodes.forEach(tokenizeNode);
      }
    }
    tmp.childNodes.forEach(tokenizeNode);

    /* Clear the element and create a container + cursor */
    el.innerHTML = '';
    el.style.opacity = '1'; // ensure visible immediately

    var textSpan = document.createElement('span');
    textSpan.setAttribute('aria-hidden', 'true');
    el.appendChild(textSpan);

    /* Accessible live region so screen-readers still get the full text */
    var srSpan = document.createElement('span');
    srSpan.className = 'sr-only';
    srSpan.style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;';
    srSpan.textContent = el.textContent || rawHTML.replace(/<br\s*\/?>/gi, ' ');
    el.appendChild(srSpan);

    var cursor = document.createElement('span');
    cursor.className = 'typewriter-cursor';
    cursor.setAttribute('aria-hidden', 'true');
    el.appendChild(cursor);

    if (prefersReduced) {
      /* Skip animation — show text immediately */
      textSpan.innerHTML = rawHTML;
      cursor.classList.add('done');
      triggerInkDry();
      return;
    }

    /* Typing speed: slight variation for organic feel */
    var BASE_DELAY = 46;   // ms per character
    var VARIANCE   = 22;   // ± random variance

    var index = 0;

    function typeNext() {
      if (index >= tokens.length) {
        /* Typing complete — fade the cursor to idle blink */
        setTimeout(function () {
          cursor.classList.add('done');
          triggerInkDry();
        }, 320);
        return;
      }

      var token = tokens[index];
      index++;

      if (token.type === 'br') {
        textSpan.appendChild(document.createElement('br'));
        setTimeout(typeNext, BASE_DELAY * 3); // small pause at line break
      } else {
        var ch = token.value;
        var charNode = document.createTextNode(ch);
        textSpan.appendChild(charNode);

        /* Slight pause after punctuation for a natural writing feel */
        var pause = (ch === ',' || ch === '.' || ch === '!' || ch === '?')
          ? BASE_DELAY * 6
          : BASE_DELAY + (Math.random() * VARIANCE * 2 - VARIANCE);

        setTimeout(typeNext, pause);
      }
    }

    /* Start after a short lead-in delay matching eyebrow animation */
    setTimeout(typeNext, 600);
  }

  /* ============================================================
   * 2. INK-DRY SUBTITLE TRIGGER
   *    Called by typewriter once typing finishes.
   * ============================================================ */
  function triggerInkDry() {
    /* The .ink-dry class already has animation-delay set inline;
       we simply ensure the element is in the DOM correctly.
       Nothing extra needed — CSS handles it. */
  }

  /* ============================================================
   * 3. HAND-DRAWN SVG PEN-LINE on .nav-link elements
   *    Injects an absolutely-positioned SVG <line> element into
   *    every nav-link so CSS can animate stroke-dashoffset on hover.
   * ============================================================ */
  function initPenLines() {
    /* Nav links in the desktop nav and mobile menu */
    var navLinks = document.querySelectorAll('.nav-links .nav-link, .mobile-menu .nav-link');

    navLinks.forEach(function (link) {
      if (link.querySelector('.pen-line')) return; // already injected

      /* Make sure position:relative is set */
      var computed = window.getComputedStyle(link);
      if (computed.position === 'static') {
        link.style.position = 'relative';
      }

      /* Build SVG pen-line element */
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'pen-line');
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('focusable', 'false');
      svg.setAttribute('viewBox', '0 0 200 10');
      svg.setAttribute('preserveAspectRatio', 'none');

      var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      /* Slightly wavy: start a touch above center, end a touch below */
      line.setAttribute('x1', '0');
      line.setAttribute('y1', '6');
      line.setAttribute('x2', '200');
      line.setAttribute('y2', '5');

      svg.appendChild(line);
      link.appendChild(svg);
      link.classList.add('has-pen-line');
    });
  }

  /* ============================================================
   * 4. HAND-DRAWN SVG PEN-BORDER on .btn-ghost elements
   *    The SVG rect is already in the HTML (injected at build time
   *    for the hero button). For any other .btn-ghost buttons,
   *    inject programmatically.
   * ============================================================ */
  function initPenBorders() {
    var ghostBtns = document.querySelectorAll('.btn-ghost');

    ghostBtns.forEach(function (btn) {
      if (btn.querySelector('.pen-border')) return; // already has one

      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'pen-border');
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('focusable', 'false');
      svg.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none;';

      var rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('width', '100%');
      rect.setAttribute('height', '100%');
      rect.setAttribute('rx', '11');
      rect.setAttribute('ry', '11');

      svg.appendChild(rect);
      /* Prepend so it sits behind text */
      btn.insertBefore(svg, btn.firstChild);
    });
  }

  /* ============================================================
   * 5. JOURNAL SCROLL REVEAL — enhanced stagger timing
   *    Upgrades the stagger logic to use longer, page-turn delays
   *    that feel like placing a diary page down.
   * ============================================================ */
  function initJournalReveal() {
    /* The main reveal logic is in site.js. Here we enhance the
       stagger timing for sibling .reveal groups to feel more
       like turning a journal page. */
    var reveals = document.querySelectorAll('.reveal:not(.is-visible)');

    if (!('IntersectionObserver' in window)) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;

        var target = entry.target;

        if (!prefersReduced) {
          /* Calculate position among siblings for deeper stagger */
          var parent = target.parentElement;
          var siblings = Array.from(parent.querySelectorAll('.reveal'));
          var idx = siblings.indexOf(target);

          /* Use a longer, poetic delay curve — diary pages settle slowly */
          var delays = [0, 0.18, 0.38, 0.60, 0.84];
          var delay = delays[Math.min(idx, delays.length - 1)];
          target.style.transitionDelay = delay + 's';
        }

        target.classList.add('is-visible');
        observer.unobserve(target);
      });
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -48px 0px'
    });

    reveals.forEach(function (el) { observer.observe(el); });
  }

  /* ============================================================
   * 6. FLOATING INK PARTICLES (ambient, very subtle)
   *    A handful of tiny gold dust motes that drift upward
   *    like ink particles rising from a parchment page.
   * ============================================================ */
  function initInkParticles() {
    if (prefersReduced) return;
    if (!window.matchMedia('(hover: hover)').matches) return; // desktop only

    var PARTICLE_COUNT = 7;
    var container = document.createElement('div');
    container.setAttribute('aria-hidden', 'true');
    container.style.cssText = [
      'position:fixed',
      'inset:0',
      'pointer-events:none',
      'z-index:1',
      'overflow:hidden',
    ].join(';');
    document.body.appendChild(container);

    for (var i = 0; i < PARTICLE_COUNT; i++) {
      createInkMote(container, i);
    }
  }

  function createInkMote(container, index) {
    var mote = document.createElement('span');
    var size = 2 + Math.random() * 2; // 2–4 px
    var startX = 5 + Math.random() * 90; // % across viewport
    var duration = 12 + Math.random() * 16; // 12–28 s
    var delay = index * (duration / 7);

    mote.style.cssText = [
      'position:absolute',
      'bottom:-6px',
      'left:' + startX + '%',
      'width:' + size + 'px',
      'height:' + size + 'px',
      'border-radius:50%',
      'background:rgba(195,174,120,0.35)',
      'filter:blur(0.8px)',
      'animation:inkMoteRise ' + duration + 's cubic-bezier(.16,.84,.18,1) ' + delay + 's infinite',
      'will-change:transform,opacity',
    ].join(';');

    container.appendChild(mote);
  }

  /* Inject the keyframe once */
  (function injectMoteKeyframe() {
    var style = document.createElement('style');
    style.textContent = [
      '@keyframes inkMoteRise{',
      '  0%  {transform:translateY(0)   translateX(0)    scale(1);   opacity:0;}',
      '  8%  {opacity:0.55;}',
      '  50% {transform:translateY(-45vh) translateX(12px) scale(0.85); opacity:0.25;}',
      '  85% {opacity:0.08;}',
      '  100%{transform:translateY(-90vh) translateX(-8px) scale(0.5);  opacity:0;}',
      '}',
    ].join('');
    document.head.appendChild(style);
  }());

  /* ============================================================
   * INIT — run after DOM is ready
   * ============================================================ */
  function init() {
    initTypewriter();
    initPenLines();
    initPenBorders();
    initJournalReveal();
    initInkParticles();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

}());
