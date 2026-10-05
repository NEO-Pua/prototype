/* 花印 HANAJIRUSHI — premium v1.3: the products list filter.
   Buttons filter the cards by category; ?cat=<key> (from the home page chips and the
   product-page breadcrumb) opens the list already filtered. */
(function(){
  var f=document.querySelector('.pfilter');
  if(!f)return;
  var btns=[].slice.call(f.querySelectorAll('button')),
      cards=[].slice.call(document.querySelectorAll('.pgrid--all .pcard'));
  function set(c){
    if(!btns.some(function(b){return b.getAttribute('data-cat')===c}))c='all';
    btns.forEach(function(b){
      var on=b.getAttribute('data-cat')===c;
      b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false');
    });
    cards.forEach(function(li){
      li.hidden=!(c==='all'||li.getAttribute('data-cat')===c);
      if(!li.hidden)li.classList.add('in');
    });
  }
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      var c=b.getAttribute('data-cat');set(c);
      try{history.replaceState(null,'',c==='all'?location.pathname+'#list':'?cat='+c+'#list')}catch(e){}
    });
  });
  var m=location.search.match(/[?&]cat=([a-z]+)/);
  set(m?m[1]:'all');
})();
