document.addEventListener('DOMContentLoaded', function() {
  var menuToggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.nav');

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      nav.classList.toggle('active');
      menuToggle.setAttribute('aria-expanded', nav.classList.contains('active'));
    });

    document.addEventListener('click', function(e) {
      if (!nav.contains(e.target) && !menuToggle.contains(e.target)) {
        nav.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
      }
    });

    var navLinks = nav.querySelectorAll('a');
    navLinks.forEach(function(link) {
      link.addEventListener('click', function() {
        nav.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // E-E-A-T: Methodology box toggle
  document.addEventListener('click', function(e) {
    var header = e.target.closest('.methodology-box__header');
    if (!header) return;
    var content = header.nextElementSibling;
    var toggle = header.querySelector('.methodology-box__toggle');
    if (content) content.classList.toggle('open');
    if (toggle) toggle.classList.toggle('open');
  });

  // Cookie Consent Banner
  var cookieBanner = document.querySelector('.cookie-consent');
  if (cookieBanner && !localStorage.getItem('cookieConsent')) {
    setTimeout(function() { cookieBanner.classList.add('show'); }, 1000);
  }
  document.addEventListener('click', function(e) {
    if (e.target.closest('.cookie-consent__btn--accept')) {
      localStorage.setItem('cookieConsent', 'accepted');
      if (cookieBanner) cookieBanner.classList.remove('show');
    }
    if (e.target.closest('.cookie-consent__btn--decline')) {
      localStorage.setItem('cookieConsent', 'declined');
      if (cookieBanner) cookieBanner.classList.remove('show');
    }
  });
});
