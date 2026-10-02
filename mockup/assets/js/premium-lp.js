/* 花印 HANAJIRUSHI — premium v1.2 buyer page (cosmoprof-asia/), loaded after premium.js and
   premium-v11.js (which already handle the slot picker, the form notice and the reveals).
   - "Discuss this product" ticks that product in the form below
   - the page address is shown, can be copied, and is drawn as a QR code (qrcode.js from
     cdnjs; without it the box keeps its "QR" placeholder) */
(function(){
  var EN=document.documentElement.lang==='en';
  var toast=document.querySelector('.toast'), tt=null;
  function say(msg){
    if(!toast)return;
    toast.textContent=msg;toast.classList.add('show');
    clearTimeout(tt);tt=setTimeout(function(){toast.classList.remove('show')},3200);
  }

  [].forEach.call(document.querySelectorAll('[data-pick]'),function(a){
    a.addEventListener('click',function(){
      var id=a.getAttribute('data-pick');
      [].forEach.call(document.querySelectorAll('input[data-items]'),function(c){
        if((' '+c.getAttribute('data-items')+' ').indexOf(' '+id+' ')>-1)c.checked=true;
      });
      say(EN?'Added to your request below.':'下のフォームに製品を追加しました。');
    });
  });

  // the QR code always opens the English page (the address printed at the booth);
  // "copy link" copies the page in the language being read
  var base=location.href.split('#')[0].split('?')[0];
  var qrUrl=base.replace(/(index|ja)\.html$/,'');
  var pageUrl=EN?qrUrl:base;
  var out=document.querySelector('[data-share-url]');
  if(out)out.textContent=pageUrl;

  var box=document.getElementById('lp-qr');
  if(box&&window.QRCode){
    try{
      new QRCode(box,{text:qrUrl,width:176,height:176,colorDark:'#2d2226',colorLight:'#fcfaf7',correctLevel:QRCode.CorrectLevel.M});
      box.classList.add('on');
    }catch(e){}
  }

  var copy=document.querySelector('[data-copy]');
  if(copy)copy.addEventListener('click',function(){
    function done(){say(EN?'Link copied.':'リンクをコピーしました。')}
    if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(pageUrl).then(done,function(){say(pageUrl)})}
    else{
      var ta=document.createElement('textarea');ta.value=pageUrl;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';
      document.body.appendChild(ta);ta.select();
      try{document.execCommand('copy');done()}catch(e){say(pageUrl)}
      ta.remove();
    }
  });

  var dl=document.querySelector('[data-qr-dl]');
  if(dl)dl.addEventListener('click',function(){
    var c=box&&box.querySelector('canvas');
    if(!c){say(EN?'The QR code is not available offline.':'オフラインのため QR コードを表示できません。');return}
    var a=document.createElement('a');
    a.href=c.toDataURL('image/png');a.download='hanajirushi-cosmoprof-asia-qr.png';
    document.body.appendChild(a);a.click();a.remove();
  });
})();
