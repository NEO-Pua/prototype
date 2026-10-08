/* 花印 HANAJIRUSHI — premium v1.5 (home page): the brand film. The video shows one frame until
   the visitor presses play; then it starts from the beginning, with sound and the player's own
   controls. When it ends, the play button comes back. */
(function () {
  document.querySelectorAll('[data-film]').forEach(function (fig) {
    var v = fig.querySelector('video'), btn = fig.querySelector('.film__play');
    if (!v || !btn) return;
    var poster = parseFloat((v.getAttribute('src').split('#t=')[1]) || '0');
    var len = fig.querySelector('[data-film-len]');
    v.addEventListener('loadedmetadata', function () {   // the running time, e.g. 0:50
      if (!len || !isFinite(v.duration)) return;
      var s = Math.round(v.duration);
      len.textContent = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
    });
    btn.addEventListener('click', function () {
      fig.classList.add('is-playing');
      v.controls = true;
      try { v.currentTime = 0; } catch (e) {}
      var p = v.play();
      if (p && p.catch) p.catch(function () {});
      v.focus();
    });
    v.addEventListener('ended', function () {
      fig.classList.remove('is-playing');
      v.controls = false;
      try { v.currentTime = poster; } catch (e) {}
      btn.focus();
    });
  });
})();
