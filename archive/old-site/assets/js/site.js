(function () {
  'use strict';

  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ============ Header scroll class ============ */
  var header = document.getElementById('siteHeader');
  if (header) {
    window.addEventListener('scroll', function () {
      header.classList.toggle('scrolled', window.scrollY > 12);
    }, { passive: true });
  }

  /* ============ Mobile menu ============ */
  var menuBtn = document.getElementById('menuBtn');
  var mobileMenu = document.getElementById('mobileMenu');
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', function () {
      mobileMenu.classList.toggle('open');
    });
    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileMenu.classList.remove('open');
      });
    });
  }

  /* ============ Scroll reveal with sibling stagger ============ */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          if (!prefersReduced) {
            var siblings = Array.from(
              entry.target.parentElement.querySelectorAll('.reveal:not(.is-visible)')
            );
            var idx = siblings.indexOf(entry.target);
            if (idx > 0) {
              entry.target.style.transitionDelay = (idx * 0.12) + 's';
            }
          }
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    reveals.forEach(function (el) { revealObserver.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ============ Active nav section tracking ============ */
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav-links .nav-link[href^="#"]');

  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var activeHref = '#' + entry.target.id;
          navLinks.forEach(function (link) {
            link.classList.toggle('active', link.getAttribute('href') === activeHref);
          });
        }
      });
    }, { threshold: 0.35, rootMargin: '-80px 0px -30% 0px' });

    sections.forEach(function (sec) { sectionObserver.observe(sec); });
  }

  /* Hero parallax is handled by GSAP ScrollTrigger in motion.js */

  /* ============ Stat-card 3D tilt ============ */
  if (!prefersReduced && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.stat-card').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var dx = (e.clientX - (rect.left + rect.width / 2)) / (rect.width / 2);
        var dy = (e.clientY - (rect.top + rect.height / 2)) / (rect.height / 2);
        card.style.transform = 'translateY(-5px) rotateY(' + (dx * 4) + 'deg) rotateX(' + (-dy * 4) + 'deg)';
      });
      card.addEventListener('mouseleave', function () {
        card.style.transform = '';
      });
    });
  }

  /* ============ Cursor glow follower ============ */
  if (!prefersReduced && window.matchMedia('(hover: hover)').matches) {
    var glow = document.getElementById('cursorGlow');
    if (glow) {
      var glowX = 0, glowY = 0, targetX = 0, targetY = 0;

      document.addEventListener('mousemove', function (e) {
        targetX = e.clientX;
        targetY = e.clientY;
        glow.style.opacity = '1';
      }, { passive: true });

      document.addEventListener('mouseleave', function () {
        glow.style.opacity = '0';
      });

      (function tick() {
        glowX += (targetX - glowX) * 0.1;
        glowY += (targetY - glowY) * 0.1;
        glow.style.left = glowX + 'px';
        glow.style.top = glowY + 'px';
        requestAnimationFrame(tick);
      })();
    }
  }

}());
