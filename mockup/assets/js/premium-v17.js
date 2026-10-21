/* 花印 HANAJIRUSHI — premium v1.7 (brand page): the header photos as a slideshow. One photo every
   6 seconds; the dots choose a photo; hovering or focusing pauses it; off screen it waits. With
   reduced motion it does not move on by itself (the dots still work). */
(function () {
  document.querySelectorAll('[data-pslides]').forEach(function (box) {
    var slides = [].slice.call(box.querySelectorAll('.pslide'));
    var dots = [].slice.call(box.querySelectorAll('[data-ps]'));
    if (slides.length < 2) return;
    var cur = 0, timer = null, held = false, seen = true;
    var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

    function show(n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle('is-on', i === cur); s.setAttribute('aria-hidden', i === cur ? 'false' : 'true'); });
      dots.forEach(function (d, i) { if (i === cur) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
    }
    function run() {
      clearInterval(timer);
      if (!still && !held && seen) timer = setInterval(function () { show(cur + 1); }, 6000);
    }
    dots.forEach(function (d, i) { d.addEventListener('click', function () { show(i); run(); }); });
    ['mouseenter', 'focusin'].forEach(function (e) { box.addEventListener(e, function () { held = true; run(); }); });
    ['mouseleave', 'focusout'].forEach(function (e) { box.addEventListener(e, function () { held = false; run(); }); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { seen = es[0].isIntersecting; run(); }).observe(box);
    }
    show(0);
    run();
  });
})();
