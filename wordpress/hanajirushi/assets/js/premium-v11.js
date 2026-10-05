/* 花印 HANAJIRUSHI — premium v1.1 motion layer (loaded after premium.js).
   - heading lines (.ln) are revealed in turn as they enter the viewport
   - figures (12ヵ国, 2015年) count up once
   - the list stagger set by premium.js is handed to child images as --d
   The opening sequence and the image reveals themselves are CSS (premium-v11.css). */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  [].forEach.call(document.querySelectorAll('.rv'),function(el){
    if(el.style.transitionDelay)el.style.setProperty('--d',el.style.transitionDelay);
  });

  var lns=document.querySelectorAll('.ln');
  var nums=document.querySelectorAll('.nums b.num, .gstats b:not(.na)');

  function count(el){
    var tn=el.firstChild;
    if(!tn||tn.nodeType!==3)return;
    var end=parseInt(tn.nodeValue,10);
    if(isNaN(end))return;
    var start=end>=1000?end-30:0, t0=null, dur=1600;   // years roll up from a nearby year
    tn.nodeValue=String(start);
    function step(ts){
      if(t0===null)t0=ts;
      var p=Math.min((ts-t0)/dur,1), e=1-Math.pow(1-p,3);
      tn.nodeValue=String(Math.round(start+(end-start)*e));
      if(p<1)requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  if(reduce||!('IntersectionObserver' in window)){
    [].forEach.call(lns,function(l){l.classList.add('in')});
    return;
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      if(e.target.classList.contains('ln'))e.target.classList.add('in');else count(e.target);
      io.unobserve(e.target);
    });
  },{rootMargin:'0px 0px -6% 0px',threshold:0});
  [].forEach.call(lns,function(l){io.observe(l)});
  [].forEach.call(nums,function(n){io.observe(n)});
})();
