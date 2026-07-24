document.addEventListener('DOMContentLoaded', function() {
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', function() {
      nav.classList.toggle('active');
    });

    document.addEventListener('click', function(e) {
      if (!nav.contains(e.target) && !menuToggle.contains(e.target)) {
        nav.classList.remove('active');
      }
    });
  }

  const readLinks = document.querySelectorAll('.article-card h3 a');
  readLinks.forEach(function(link) {
    link.addEventListener('mouseenter', function() {
      this.style.color = '#e94560';
    });
    link.addEventListener('mouseleave', function() {
      this.style.color = '';
    });
  });
});
