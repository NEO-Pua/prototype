/* 花印 HANAJIRUSHI — carousel, news tabs, slot picker, sp menu, page top */
(function(){
  var EN=document.documentElement.lang==='en';
  // ---------- KV carousel (infinite, centred, with peeking side slides) ----------
  var kv=document.querySelector('.kv');
  if(kv){
    var track=kv.querySelector('.kv__track');
    var orig=[].slice.call(track.children);
    var n=orig.length, CL=2;
    // clone CL slides at each end for seamless looping
    for(var i=0;i<CL;i++){
      track.appendChild(orig[i].cloneNode(true));
      track.insertBefore(orig[n-1-i].cloneNode(true),track.firstChild);
    }
    var slides=[].slice.call(track.children);
    var idx=CL, timer=null, playing=true;
    var dots=kv.querySelector('.kv__dots');
    orig.forEach(function(_,k){
      var b=document.createElement('button');b.setAttribute('aria-label','slide '+(k+1));
      b.addEventListener('click',function(){go(k+CL);restart()});dots.appendChild(b);
    });
    function sw(){
      var w=kv.clientWidth;
      return w<=768 ? Math.round(w*0.88) : Math.min(820,Math.round(w*0.62));
    }
    function layout(anim){
      var s=sw(), gap=parseFloat(getComputedStyle(track).columnGap)||16;
      kv.style.setProperty('--sw',s+'px');
      var x=(kv.clientWidth-s)/2-idx*(s+gap);
      track.classList.toggle('nt',!anim);
      track.style.transform='translateX('+x+'px)';
      slides.forEach(function(el,j){el.classList.toggle('cur',j===idx)});
      var real=((idx-CL)%n+n)%n;
      [].forEach.call(dots.children,function(d,j){d.classList.toggle('on',j===real)});
    }
    function go(k){idx=k;layout(true)}
    track.addEventListener('transitionend',function(e){
      if(e.target!==track)return;
      if(idx>=n+CL){idx-=n;layout(false)}
      else if(idx<CL){idx+=n;layout(false)}
    });
    kv.querySelector('.kv__btn--n').addEventListener('click',function(){go(idx+1);restart()});
    kv.querySelector('.kv__btn--p').addEventListener('click',function(){go(idx-1);restart()});
    var pause=kv.querySelector('.kv__pause');
    function restart(){clearInterval(timer);if(playing)timer=setInterval(function(){go(idx+1)},5000)}
    pause.addEventListener('click',function(){
      playing=!playing;pause.innerHTML=playing?pause.dataset.p:pause.dataset.r;restart();
    });
    window.addEventListener('resize',function(){layout(false)});
    // touch swipe
    var sx=null;
    track.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
    track.addEventListener('touchend',function(e){
      if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;sx=null;
      if(Math.abs(dx)>40){go(idx+(dx<0?1:-1));restart()}
    });
    // #kv=N opens slide N (1-based) with autoplay off — handy for reviews
    var m=location.hash.match(/kv=(\d+)/);
    if(m){idx=CL+Math.min(n,Math.max(1,+m[1]))-1;playing=false;pause.innerHTML=pause.dataset.r}
    layout(false);restart();
  }

  // ---------- news tabs ----------
  var tabs=document.querySelectorAll('.tabs button');
  tabs.forEach(function(b){
    b.addEventListener('click',function(){
      tabs.forEach(function(x){x.classList.remove('on')});b.classList.add('on');
      var c=b.dataset.cat;
      document.querySelectorAll('.nlist li').forEach(function(li){
        li.classList.toggle('hide',c!=='all'&&li.dataset.cat!==c);
      });
    });
  });

  // ---------- meeting slot picker ----------
  var slotBtns=document.querySelectorAll('.slots button');
  slotBtns.forEach(function(b){
    b.addEventListener('click',function(){
      slotBtns.forEach(function(x){x.classList.remove('on')});b.classList.add('on');
      var out=document.querySelector('[data-slot-out]');
      if(out)out.textContent=b.dataset.day+'　'+b.textContent+(EN?' (30 min)':'〜（30分）');
    });
  });

  // ---------- sp menu ----------
  var burger=document.querySelector('.burger'), spnav=document.querySelector('.spnav'), root=document.documentElement;
  function setMenu(open){
    root.classList.toggle('menu-open',open);
    burger.setAttribute('aria-expanded',open);
    spnav.setAttribute('aria-hidden',!open);
  }
  if(burger&&spnav){
    burger.addEventListener('click',function(){setMenu(!root.classList.contains('menu-open'))});
    spnav.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&root.classList.contains('menu-open')){setMenu(false);burger.focus()}});
  }

  // ---------- page top ----------
  var tt=document.querySelector('.totop');
  if(tt){
    window.addEventListener('scroll',function(){tt.classList.toggle('show',scrollY>500)},{passive:true});
    tt.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'})});
  }

  // ---------- contact form: pre-select from ?topic=…&item=pN (v2.2 CTA buttons) ----------
  var qs=new URLSearchParams(location.search), topic=qs.get('topic'), item=qs.get('item');
  if(topic){var r=document.querySelector('input[name="k"][value="'+topic+'"]');if(r)r.checked=true}
  if(item){document.querySelectorAll('input[data-items]').forEach(function(c){
    if((' '+c.getAttribute('data-items')+' ').indexOf(' '+item+' ')>-1)c.checked=true})}

  // ---------- mockup: disable forms ----------
  document.querySelectorAll('form').forEach(function(f){
    f.addEventListener('submit',function(e){e.preventDefault();alert(EN?'Design mockup: search and form submission are disabled.':'モックアップのため検索・送信は無効です。')});
  });
})();
