/**
 * motion.js — Awwwards-grade motion stack for Poesie Landing Page
 *
 * Systems (in execution order):
 *  1. Lenis      — smooth, frictionless scroll inertia
 *  2. GSAP init  — register ScrollTrigger, sync with Lenis RAF
 *  3. Text split — SplitType word-by-word cinematic reveals
 *  4. Hero       — GSAP-driven depth parallax (replaces site.js version)
 *  5. Pen scene  — fountain pen SVG draws on scroll progress
 *  6. Phone      — feature mockups drift at different parallax depths
 *  7. Stat cards — staggered cascade entrance
 *  8. Sub-lines  — section italic subtitles fade-slide in
 */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────────────────────────
   * GUARDS
   * ──────────────────────────────────────────────────────────────────────── */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (typeof gsap === 'undefined') {
    console.warn('[motion.js] GSAP not loaded — motion system disabled.');
    return;
  }
  if (typeof ScrollTrigger === 'undefined') {
    console.warn('[motion.js] ScrollTrigger not loaded — motion system disabled.');
    return;
  }

  if (typeof MotionPathPlugin !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger, MotionPathPlugin);
  } else {
    gsap.registerPlugin(ScrollTrigger);
    console.warn('[motion.js] MotionPathPlugin not loaded — pen cursor motion disabled.');
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * 1. LENIS — smooth scroll
   * ──────────────────────────────────────────────────────────────────────── */
  var lenis = null;

  function initLenis() {
    if (reduced || typeof Lenis === 'undefined') return;

    lenis = new Lenis({
      duration: 1.35,
      /* Exponential ease-out — feels like ink flowing, decelerates smoothly */
      easing: function (t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); },
      smoothWheel: true,
      smoothTouch: false, /* keep native momentum on iOS */
    });

    /* Tick Lenis inside GSAP's RAF for perfectly synced frame timing */
    gsap.ticker.add(function (time) {
      lenis.raf(time * 1000);
    });
    gsap.ticker.lagSmoothing(0);

    /* Keep ScrollTrigger updated with Lenis's smoothed position */
    lenis.on('scroll', function () {
      ScrollTrigger.update();
    });

    /* Smooth anchor navigation — intercept all #hash links */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        var hash = anchor.getAttribute('href');
        if (!hash || hash === '#') return;
        var target = document.querySelector(hash);
        if (!target) return;
        e.preventDefault();
        lenis.scrollTo(target, { offset: -84, duration: 1.6 }); /* 84px = header height */
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * 2. CINEMATIC TEXT REVEALS — SplitType + GSAP word-by-word clip masks
   *
   *  Elements marked data-split="words" get their words wrapped in
   *  overflow:hidden line clips. Each word slides up from y:105%
   *  with a gentle stagger — the classic Awwwards text-reveal.
   * ──────────────────────────────────────────────────────────────────────── */
  var _splitInstances = [];

  function _revertSplits() {
    _splitInstances.forEach(function (inst) {
      try {
        if (inst && typeof inst.revert === 'function') {
          inst.revert();
        }
      } catch (e) {
        console.warn('Error reverting SplitType instance:', e);
      }
    });
    _splitInstances = [];

    var targets = document.querySelectorAll('[data-split], [data-split-text]');
    targets.forEach(function (el) {
      if (typeof ScrollTrigger !== 'undefined') {
        ScrollTrigger.getAll().forEach(function (st) {
          if (st.vars && st.vars.trigger === el) {
            st.kill();
          }
        });
      }
      el.classList.remove('gsap-split-ready');
      if (typeof gsap !== 'undefined') {
        gsap.set(el, { clearProps: 'all' });
      }
    });
  }

  function _reinitSplits() {
    if (typeof SplitType === 'undefined') return;
    var targets = document.querySelectorAll('[data-split], [data-split-text]');
    targets.forEach(function (el) {
      _animateSplitElement(el);
    });
    if (typeof ScrollTrigger !== 'undefined') {
      ScrollTrigger.refresh();
    }
  }

  function refreshAnimations(updateCallback) {
    _revertSplits();

    if (typeof updateCallback === 'function') {
      try {
        var res = updateCallback();
        if (res && typeof res.then === 'function') {
          return res.then(function () {
            _reinitSplits();
          });
        }
      } catch (err) {
        console.error('Error executing updateCallback in refreshAnimations:', err);
      }
    }

    _reinitSplits();
  }

  // Expose globally so i18n or other scripts can safely trigger animation refresh
  window.refreshAnimations = refreshAnimations;
  window.revertSplitText = _revertSplits;

  function initTextReveals() {
    _reinitSplits();
  }

  function _animateSplitElement(el) {
    var splitType = el.getAttribute('data-split') || el.getAttribute('data-split-text') || 'words';

    var split = new SplitType(el, {
      types: splitType === 'words' ? 'lines,words' : 'lines',
      lineClass: 'st-line',
      wordClass: 'st-word',
    });
    _splitInstances.push(split);
    el.classList.add('gsap-split-ready');

    var animTargets = splitType === 'words' ? split.words : split.lines;
    if (!animTargets || !animTargets.length) return;

    if (reduced) {
      /* Respect user preference — no animation, just ensure visible */
      gsap.set(animTargets, { y: 0, opacity: 1 });
      return;
    }

    /* The clip-mask slide: words start BELOW their container's overflow edge */
    gsap.from(animTargets, {
      y: '108%',
      duration: 0.92,
      stagger: {
        each: 0.052,
        ease: 'power1.in',
      },
      ease: 'power3.out',
      clearProps: 'transform', /* Release GSAP control after animation so CSS can take over */
      scrollTrigger: {
        trigger: el,
        start: 'top 86%',
        toggleActions: 'play none none none',
      },
    });
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * 3. HERO PARALLAX — GSAP replaces the vanilla scroll listener in site.js
   *    (site.js listener was removed to avoid double-animation)
   * ──────────────────────────────────────────────────────────────────────── */
  function initHeroParallax() {
    if (reduced) return;

    var heroPhones = document.querySelector('.hero-phones');
    var heroVisual = document.querySelector('.hero-visual');
    if (!heroPhones) return;

    /* Phone mockup drifts down as user scrolls away from hero */
    gsap.to(heroPhones, {
      y: 90,
      ease: 'none',
      scrollTrigger: {
        trigger: '.hero',
        start: 'top top',
        end: 'bottom top',
        scrub: 1.4,
      },
    });

    /* Hero visual fades gently as hero exits viewport */
    if (heroVisual) {
      gsap.to(heroVisual, {
        opacity: 0.25,
        ease: 'none',
        scrollTrigger: {
          trigger: '.hero',
          start: '50% top',
          end: 'bottom top',
          scrub: 1.0,
        },
      });
    }
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * 4. FOUNTAIN PEN SCENE — SVG path draws on scroll progress with pen cursor
   *
   *    The SVG <path id="penPath"> has its stroke-dasharray set to the
   *    full path length. ScrollTrigger scrubs dashoffset from full → 0,
   *    making the path appear to be drawn by the fountain pen cursor.
   *    GSAP MotionPathPlugin animates the pen along the exact same path
   *    GSAP MotionPathPlugin animates the pen along each path sequentially,
   *    seamlessly jumping from stroke to stroke with fixed natural handwriting tilt.
   * ──────────────────────────────────────────────────────────────────────── */
  var _penTimeline = null;
  var _penYoyoTween = null;
  // 130° positions the barrel at top-right and nib at bottom-left (~50° to paper)
  var PEN_BASE_ROTATION = 130;

  function initFountainPen() {
    var penGroup = document.getElementById('penGroup');
    var svg = document.getElementById('penSvg');
    var pen = document.getElementById('penCursor');

    // Collect all paths inside #penGroup, or directly in #penSvg, or single #penPath
    var pathElements = [];
    if (penGroup) {
      pathElements = Array.prototype.slice.call(penGroup.querySelectorAll('path'));
    }
    if (!pathElements.length && svg) {
      pathElements = Array.prototype.slice.call(svg.querySelectorAll('path'));
    }
    if (!pathElements.length) {
      var singlePath = document.getElementById('penPath');
      if (singlePath) pathElements = [singlePath];
    }

    if (!pathElements.length) return;

    // Dynamically fit SVG viewBox to the actual bounding box of all paths
    function fitViewBox() {
      try {
        if (svg && penGroup && penGroup.getBBox) {
          var bbox = penGroup.getBBox();
          if (bbox && bbox.width > 0 && bbox.height > 0) {
            var padX = 10;
            var padY = 8;
            svg.setAttribute('viewBox', [
              Math.floor(bbox.x - padX),
              Math.floor(bbox.y - padY),
              Math.ceil(bbox.width + padX * 2),
              Math.ceil(bbox.height + padY * 2)
            ].join(' '));
          }
        }
      } catch (e) {}
    }

    function buildAnimation() {
      // Clean up previous timeline, ScrollTrigger, and yoyo tween on rebuild (e.g. resize)
      if (_penTimeline) {
        if (_penTimeline.scrollTrigger) {
          _penTimeline.scrollTrigger.kill();
        }
        _penTimeline.kill();
        _penTimeline = null;
      }
      if (_penYoyoTween) {
        _penYoyoTween.kill();
        _penYoyoTween = null;
      }

      fitViewBox();

      // Measure all paths and compute total path length
      var pathData = [];
      var totalLength = 0;

      pathElements.forEach(function (p) {
        var len = p.getTotalLength();
        if (!len || isNaN(len) || len < 0.5) len = 0.5; // Avoid 0
        totalLength += len;
        pathData.push({ el: p, length: len });

        // Set initial stroke-dash state (stroke is completely hidden and invisible)
        gsap.set(p, {
          strokeDasharray: len,
          strokeDashoffset: len,
          autoAlpha: 0, // Eliminates round linecap dots artifact before drawing starts
        });
      });

      if (!pathData.length || totalLength === 0) return;

      if (reduced) {
        /* Skip animation, reveal all paths immediately and hide pen */
        pathData.forEach(function (d) {
          gsap.set(d.el, { strokeDashoffset: 0, autoAlpha: 1 });
        });
        if (pen) gsap.set(pen, { display: 'none' });
        return;
      }

      if (pen) {
        gsap.set(pen, {
          transformOrigin: '100% 50%',
          rotation: PEN_BASE_ROTATION - 3,
        });

        /* Subtle organic yoyo breathing: +/- 3° to simulate natural finger/hand movement */
        _penYoyoTween = gsap.to(pen, {
          rotation: PEN_BASE_ROTATION + 3,
          duration: 1.3,
          ease: 'sine.inOut',
          repeat: -1,
          yoyo: true,
        });
      }

      /* Autonomous time-based timeline: plays once when pen scene enters viewport */
      _penTimeline = gsap.timeline({
        scrollTrigger: {
          trigger: '#pen-scene',
          start: 'top 70%',
          toggleActions: 'play none none none',
        },
      });

      var TOTAL_STROKE_TIME = 3.5; // Autonomous time-based duration in seconds
      var currentTime = 0;

      pathData.forEach(function (d, idx) {
        // Proportionate duration so drawing speed is uniform across all strokes
        var strokeDuration = (d.length / totalLength) * TOTAL_STROKE_TIME;

        // 1. Reveal stroke at the exact moment its drawing starts (eliminates dots artifact)
        _penTimeline.set(d.el, { autoAlpha: 1 }, currentTime);

        // 2. Draw current stroke
        _penTimeline.to(d.el, {
          strokeDashoffset: 0,
          duration: strokeDuration,
          ease: 'power1.inOut',
        }, currentTime);

        // 3. Animate pen along current stroke, jumping seamlessly to next stroke on completion
        if (pen && typeof MotionPathPlugin !== 'undefined') {
          _penTimeline.to(pen, {
            motionPath: {
              path: d.el,
              align: d.el,
              alignOrigin: [1, 0.5],
              autoRotate: false, // Steady natural handwriting posture
            },
            duration: strokeDuration,
            ease: 'power1.inOut',
            immediateRender: idx === 0, // Only first tween immediately renders at start of first path
          }, currentTime);
        }

        currentTime += strokeDuration;
      });
    }

    buildAnimation();

    /* Rebuild on window resize to ensure responsive SVG path coordinates stay in sync */
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(buildAnimation, 180);
    });

    /* Animate the eyebrow label in as pen scene enters view */
    var eyebrow = document.querySelector('.pen-scene-eyebrow');
    if (eyebrow && !reduced) {
      gsap.from(eyebrow, {
        opacity: 0,
        y: 20,
        duration: 1.1,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: '#pen-scene',
          start: 'top 80%',
          toggleActions: 'play none none none',
        },
      });
    }

    /* Gently reveal the scroll hint */
    var hint = document.querySelector('.pen-scene-hint');
    if (hint && !reduced) {
      gsap.from(hint, {
        opacity: 0,
        duration: 1.4,
        delay: 0.5,
        ease: 'power1.out',
        scrollTrigger: {
          trigger: '#pen-scene',
          start: 'top 75%',
          toggleActions: 'play none none none',
        },
      });
    }
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * 5. FEATURE SECTION PHONE PARALLAX
   *    Primary phone mockups drift at a different rate than the page scroll,
   *    creating a convincing depth separation (foreground vs background).
   * ──────────────────────────────────────────────────────────────────────── */
  function initPhoneParallax() {
    if (reduced) return;
    /* Only on devices that can benefit (pointer:fine = mouse/trackpad) */
    if (!window.matchMedia('(pointer: fine)').matches) return;

    document.querySelectorAll('.phone-window.float-slow').forEach(function (phone) {
      var section = phone.closest('section');
      if (!section) return;

      /* Alternate drift direction based on layout side */
      var isRight = !!phone.closest('.align-right');
      var yDrift  = isRight ? 28 : -28;

      gsap.fromTo(phone,
        { y: -18 },
        {
          y: yDrift,
          ease: 'none',
          scrollTrigger: {
            trigger: section,
            start: 'top bottom',
            end: 'bottom top',
            scrub: 1.6,
          },
        }
      );
    });
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * 6. STAT CARDS — staggered cascade reveal
   * ──────────────────────────────────────────────────────────────────────── */
  function initStatCards() {
    var cards = document.querySelectorAll('.stat-card');
    if (!cards.length || reduced) return;

    gsap.from(cards, {
      y: 52,
      opacity: 0,
      duration: 0.82,
      stagger: 0.13,
      ease: 'power3.out',
      /* Clear GSAP's inline transform after animation so
         the existing mouse-tilt effect in site.js can take over cleanly */
      onComplete: function () {
        gsap.set(cards, { clearProps: 'transform,opacity' });
      },
      scrollTrigger: {
        trigger: '.stat-grid',
        start: 'top 78%',
        toggleActions: 'play none none none',
      },
    });
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * 7. SECTION SUBTITLES — italic gold lines fade & drift up
   * ──────────────────────────────────────────────────────────────────────── */
  function initSubtitleReveals() {
    if (reduced) return;

    document.querySelectorAll('.section-sub').forEach(function (el) {
      gsap.from(el, {
        opacity: 0,
        y: 20,
        duration: 1.0,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          toggleActions: 'play none none none',
        },
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * 8. FAQ ITEM STAGGER
   * ──────────────────────────────────────────────────────────────────────── */
  function initFaqReveal() {
    var items = document.querySelectorAll('.faq-item');
    if (!items.length || reduced) return;

    gsap.from(items, {
      y: 30,
      opacity: 0,
      duration: 0.7,
      stagger: 0.1,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: '.faq-list',
        start: 'top 82%',
        toggleActions: 'play none none none',
      },
    });
  }

  /* ─────────────────────────────────────────────────────────────────────────
   * INIT
   * ──────────────────────────────────────────────────────────────────────── */
  function init() {
    initLenis();
    initTextReveals();
    initHeroParallax();
    initFountainPen();
    initPhoneParallax();
    initStatCards();
    initSubtitleReveals();
    initFaqReveal();

    /* Refresh all ScrollTrigger bounds after all resources load
       (fonts shift layout, images change dimensions) */
    window.addEventListener('load', function () {
      ScrollTrigger.refresh(true);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

}());
