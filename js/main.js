/* Prime Hotel Picks. No dependencies. */
document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Mobile navigation ---------- */
  var menuToggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.nav');

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', function (e) {
      e.stopPropagation();
      nav.classList.toggle('active');
      menuToggle.setAttribute('aria-expanded', nav.classList.contains('active'));
    });

    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target) && !menuToggle.contains(e.target)) {
        nav.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('active')) {
        nav.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.focus();
      }
    });

    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- "How we research" accordion ---------- */
  document.querySelectorAll('.methodology-box__header').forEach(function (header) {
    header.setAttribute('role', 'button');
    header.setAttribute('tabindex', '0');
    header.setAttribute('aria-expanded', 'false');

    function toggle() {
      var content = header.nextElementSibling;
      var caret = header.querySelector('.methodology-box__toggle');
      var open = content && content.classList.toggle('open');
      if (caret) caret.classList.toggle('open');
      header.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    header.addEventListener('click', toggle);
    header.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });

  /* ---------- Cookie consent, gating ad loading ----------
     Ads are only loaded once the visitor has actively accepted. Declining
     leaves the page ad-free rather than storing a preference nothing reads. */
  var CONSENT_KEY = 'cookieConsent';
  var banner = document.querySelector('.cookie-consent');

  function loadAds() {
    var slots = document.querySelectorAll('.ad-slot[data-ad-client]');
    if (!slots.length) return;
    if (!document.getElementById('adsense-loader')) {
      var client = slots[0].getAttribute('data-ad-client');
      if (!client || client.indexOf('ca-pub-') !== 0) return; // not configured yet
      var s = document.createElement('script');
      s.id = 'adsense-loader';
      s.async = true;
      s.crossOrigin = 'anonymous';
      s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + client;
      document.head.appendChild(s);
    }
    slots.forEach(function (slot) {
      if (slot.dataset.filled) return;
      slot.dataset.filled = '1';
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
  }

  var stored = null;
  try { stored = localStorage.getItem(CONSENT_KEY); } catch (e) { /* storage blocked */ }

  if (stored === 'accepted') {
    loadAds();
  } else if (!stored && banner) {
    setTimeout(function () { banner.classList.add('show'); }, 800);
  }

  document.addEventListener('click', function (e) {
    var accept = e.target.closest('.cookie-consent__btn--accept');
    var decline = e.target.closest('.cookie-consent__btn--decline');
    if (!accept && !decline) return;

    try { localStorage.setItem(CONSENT_KEY, accept ? 'accepted' : 'declined'); } catch (err) {}
    if (banner) banner.classList.remove('show');
    if (accept) loadAds();
  });
});
