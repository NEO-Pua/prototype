/* 花印 HANAJIRUSHI — premium v1.4: the store chooser behind 「この製品を購入する」 on product
   pages (a <dialog>). Stores whose address is not known yet are marked and do nothing. */
(function(){
  var d=document.getElementById('buy');
  if(!d)return;
  [].forEach.call(document.querySelectorAll('[data-buy]'),function(b){
    b.addEventListener('click',function(){
      if(d.showModal)d.showModal();else d.setAttribute('open','');
    });
  });
  function close(){if(d.close)d.close();else d.removeAttribute('open')}
  d.addEventListener('click',function(e){
    if(e.target===d||(e.target.closest&&e.target.closest('[data-close]')))close();   // backdrop or ×
  });
  [].forEach.call(d.querySelectorAll('a[aria-disabled="true"]'),function(a){
    a.addEventListener('click',function(e){e.preventDefault()});
  });
})();
