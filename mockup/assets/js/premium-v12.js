/* 花印 HANAJIRUSHI — premium v1.2 home slider (first view).
   Autoplay is the CSS progress line on the current tab: when its animation ends, the next
   slide comes in. Pausing pauses the line; reduced motion removes the line's animation, so
   the slider then only moves when asked. Tabs, arrow keys (on the tabs) and swipe. */
(function(){
  var hero=document.querySelector('.hero--slides');
  if(!hero)return;
  var slides=[].slice.call(hero.querySelectorAll('.hs__s')),
      tabs=[].slice.call(hero.querySelectorAll('[data-go]')),
      num=hero.querySelector('.hs__n b'), play=hero.querySelector('.hs__play'),
      n=slides.length, cur=0;

  function show(el,on){
    el.classList.toggle('is-on',on);
    if(on){el.removeAttribute('aria-hidden')}else{el.setAttribute('aria-hidden','true')}
    el.inert=!on;
  }
  slides.forEach(function(el,i){show(el,i===0)});

  function go(i){
    i=(i+n)%n;
    if(i===cur)return;
    show(slides[cur],false);tabs[cur].removeAttribute('aria-current');
    cur=i;
    show(slides[cur],true);tabs[cur].setAttribute('aria-current','true');
    num.textContent=('0'+(cur+1)).slice(-2);
    hero.removeAttribute('data-first');
  }

  tabs.forEach(function(b,i){b.addEventListener('click',function(){go(i)})});
  hero.addEventListener('animationend',function(e){if(e.animationName==='hs-fill')go(cur+1)});

  function pause(p){
    hero.classList.toggle('is-paused',p);
    play.setAttribute('aria-label',p?play.getAttribute('data-play'):play.getAttribute('data-pause'));
  }
  play.addEventListener('click',function(){pause(!hero.classList.contains('is-paused'))});

  hero.querySelector('.hs__ui').addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'){go(cur+1);e.preventDefault()}
    if(e.key==='ArrowLeft'){go(cur-1);e.preventDefault()}
  });

  var x0=null,y0=null;
  hero.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
  hero.addEventListener('touchend',function(e){
    if(x0===null)return;
    var dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0;
    if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)go(cur+(dx<0?1:-1));
    x0=y0=null;
  },{passive:true});
})();
