/* 花印 HANAJIRUSHI — Direction B (premium): header state, menu, reveal on scroll, page-top,
   and a notice for links to pages that this stretch mockup does not include. */
(function(){
  var EN=document.documentElement.lang==='en';
  var root=document.documentElement;

  // ---------- header: transparent at the top, solid once scrolled ----------
  var hd=document.querySelector('[data-hd]'), totop=document.querySelector('.totop');
  function onScroll(){
    var y=window.scrollY;
    if(hd)hd.classList.toggle('is-solid',y>40);
    if(totop)totop.classList.toggle('show',y>700);
  }
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  if(totop)totop.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});

  // ---------- full-screen menu ----------
  var btn=document.querySelector('.hd__menu'), menu=document.getElementById('menu');
  function setMenu(open){
    root.classList.toggle('menu-open',open);
    menu.classList.toggle('open',open);
    menu.setAttribute('aria-hidden',open?'false':'true');
    btn.setAttribute('aria-expanded',open?'true':'false');
  }
  if(btn&&menu){
    btn.addEventListener('click',function(){setMenu(!menu.classList.contains('open'))});
    menu.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&menu.classList.contains('open')){setMenu(false);btn.focus()}});
    window.addEventListener('resize',function(){if(window.innerWidth>1080&&menu.classList.contains('open'))setMenu(false)});
  }

  // ---------- reveal on scroll, staggered within a list ----------
  var rv=[].slice.call(document.querySelectorAll('.rv'));
  rv.forEach(function(el){
    if(el.parentElement){
      var sibs=[].filter.call(el.parentElement.children,function(c){return c.classList.contains('rv')});
      var i=sibs.indexOf(el);
      if(sibs.length>1&&i>0)el.style.transitionDelay=Math.min(i*0.12,0.6)+'s';
    }
  });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}});
    },{rootMargin:'0px 0px -8% 0px',threshold:0.08});
    rv.forEach(function(el){io.observe(el)});
  }else{
    rv.forEach(function(el){el.classList.add('in')});
  }

  // ---------- mockup: forms do not send (the WordPress site marks <html data-live> and sends) ----------
  var LIVE=document.documentElement.hasAttribute('data-live');
  var toast=document.querySelector('.toast'), tt=null;
  function say(msg){
    if(!toast)return;
    toast.textContent=msg;toast.classList.add('show');
    clearTimeout(tt);tt=setTimeout(function(){toast.classList.remove('show')},4200);
  }
  if(!LIVE)[].forEach.call(document.querySelectorAll('form'),function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      say(EN?'This is a design mockup: the form is not sent.':'デザイン確認用のモックアップのため、送信はされません。');
    });
  });

  // ---------- contact: topic buttons pre-select the form (contact.html?topic=partner&item=p1) ----------
  var qs=new URLSearchParams(location.search), topic=qs.get('topic'), item=qs.get('item');
  if(topic){var r=document.querySelector('input[name="k"][value="'+topic+'"]');if(r)r.checked=true}
  if(item){[].forEach.call(document.querySelectorAll('input[data-items]'),function(c){
    if((' '+c.getAttribute('data-items')+' ').indexOf(' '+item+' ')>-1)c.checked=true})}

  // ---------- exhibition: meeting slot picker ----------
  var out=document.querySelector('[data-slot-out]');
  [].forEach.call(document.querySelectorAll('.slots button:not([disabled])'),function(b){
    b.addEventListener('click',function(){
      [].forEach.call(document.querySelectorAll('.slots button.on'),function(x){x.classList.remove('on');x.removeAttribute('aria-pressed')});
      b.classList.add('on');b.setAttribute('aria-pressed','true');
      if(out)out.textContent=b.getAttribute('data-day')+' '+b.textContent;
    });
  });

  // ---------- news: category filter ----------
  [].forEach.call(document.querySelectorAll('.ftabs button'),function(b){
    b.addEventListener('click',function(){
      var c=b.getAttribute('data-cat');
      [].forEach.call(document.querySelectorAll('.ftabs button'),function(x){x.classList.toggle('on',x===b)});
      [].forEach.call(document.querySelectorAll('.nl li[data-cat]'),function(li){li.hidden=!(c==='all'||li.getAttribute('data-cat')===c)});
    });
  });

  // store logos are placeholders in a mockup
  if(!LIVE)[].forEach.call(document.querySelectorAll('.stores__l a'),function(a){a.addEventListener('click',function(e){e.preventDefault()})});
})();
