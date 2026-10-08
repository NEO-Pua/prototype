/* 花印 HANAJIRUSHI — premium v1.5 (home page): the brand film.

   - Once the film is in view it starts by itself, muted (browsers allow no sound before a click),
     with a pause button and a "sound on" button over it. It pauses when scrolled away and carries
     on when it comes back, unless the visitor paused it.
   - "Sound on" restarts the film from the beginning with sound and the player's own controls.
   - It plays once. At the end it shows the logo frame and the play button again; the play button
     starts it from the beginning with sound.
   - With reduced motion or data saving it does not start by itself: the play button waits.
   - The running time under the film is read from the video. */
(function () {
  var quiet = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var save = navigator.connection && navigator.connection.saveData;

  document.querySelectorAll('[data-film]').forEach(function (fig) {
    var v = fig.querySelector('video'), big = fig.querySelector('.film__play');
    var pz = fig.querySelector('[data-film-pause]'), snd = fig.querySelector('[data-film-sound]');
    var len = fig.querySelector('[data-film-len]');
    if (!v || !big) return;
    var poster = parseFloat((v.getAttribute('src').split('#t=')[1]) || '0');
    var state = 'idle';          // idle (logo frame) | auto (muted, by itself) | watch (with sound)
    var held = false;            // the visitor paused the muted film
    var done = false;            // it has played once

    function set(s) {
      state = s;
      fig.classList.toggle('is-auto', s === 'auto');
      fig.classList.toggle('is-playing', s === 'watch');
      v.controls = s === 'watch';
    }
    function go() { var p = v.play(); if (p && p.catch) p.catch(function () { if (state === 'auto') set('idle'); }); }
    function mark() {
      if (!pz) return;
      var paused = v.paused;
      pz.classList.toggle('is-paused', paused);
      pz.setAttribute('aria-label', pz.getAttribute(paused ? 'data-play' : 'data-pause'));
    }
    function watch() {          // from the beginning, with sound and the player's controls
      set('watch');
      v.muted = false;
      try { v.currentTime = 0; } catch (e) {}
      go();
      v.focus();
    }

    v.addEventListener('loadedmetadata', function () {   // the running time, e.g. 0:50
      if (!len || !isFinite(v.duration)) return;
      var s = Math.round(v.duration);
      len.textContent = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
    });
    v.addEventListener('play', mark);
    v.addEventListener('pause', mark);
    v.addEventListener('ended', function () {
      done = true;
      set('idle');
      v.muted = true;
      try { v.currentTime = poster; } catch (e) {}
      big.focus({ preventScroll: true });
    });

    big.addEventListener('click', watch);
    if (snd) snd.addEventListener('click', watch);
    if (pz) pz.addEventListener('click', function () {
      if (v.paused) { held = false; go(); } else { held = true; v.pause(); }
    });

    if (quiet || save || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          if (state === 'idle' && !done) {          // first time in view: start muted from the beginning
            set('auto');
            v.muted = true;
            try { v.currentTime = 0; } catch (err) {}
            go();
          } else if (state === 'auto' && !held && v.paused) {
            go();
          }
        } else if (state !== 'idle' && !v.paused) {
          v.pause();                                // out of view: pause (sound or not)
        }
      });
    }, { threshold: 0.5 }).observe(v);
  });
})();
