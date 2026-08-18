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

  /* ---------- Cookie consent ----------
     The AdSense script itself loads from the <head> on every page, because
     AdSense review has to be able to find it. What the visitor's choice
     controls is personalisation: an inline shim in the <head> reads this same
     localStorage key before the ad script runs and sets
     requestNonPersonalizedAds accordingly.

     A change of mind therefore needs a reload to take effect, which is what
     the reload below is for. Do not reintroduce a gate here that claims to
     stop the script loading -- the previous version of this file did exactly
     that, keyed on an attribute no element ever carried, so it never ran while
     the banner and privacy policy both promised it did. */
  var CONSENT_KEY = 'cookieConsent';
  var banner = document.querySelector('.cookie-consent');

  function readConsent() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }

  if (!readConsent() && banner) {
    setTimeout(function () { banner.classList.add('show'); }, 800);
  }

  document.addEventListener('click', function (e) {
    var accept = e.target.closest('.cookie-consent__btn--accept');
    var decline = e.target.closest('.cookie-consent__btn--decline');
    if (!accept && !decline) return;

    var previous = readConsent();
    var choice = accept ? 'accepted' : 'declined';
    try { localStorage.setItem(CONSENT_KEY, choice); } catch (err) {}
    if (banner) banner.classList.remove('show');

    /* Only reload when the setting actually changed, so a first-time Decline
       (already the default) does not bounce the page for no reason. */
    if (previous === 'accepted' && choice === 'declined') location.reload();
    if (previous !== 'accepted' && choice === 'accepted') location.reload();
  });
});
