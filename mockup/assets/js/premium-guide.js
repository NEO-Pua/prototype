/* 花印 HANAJIRUSHI — premium v1.5 mockup only: image guide tags.
   Every photo that can be replaced gets a small tag with the shape and size to prepare
   (16:9 2400×1350, 4:5 1600×2000, 1:1 1600×1600), so the team knows what to shoot or crop.
   A button at the lower left hides or shows the tags (remembered in this browser).
   The WordPress theme does not load this file. */
(function () {
  var en = (document.documentElement.lang || '').indexOf('en') === 0;
  var L = function (ja, e) { return en ? e : ja; };

  var H = ['16:9', '2400×1350'], P = ['4:5', '1600×2000'], S = ['1:1', '1600×1600'];
  // [selector, where the tag goes (closest), what, shape, note]
  var SPOTS = [
    ['.phero__img--slides', null, L('ヘッダー写真（スライド）', 'Header photos (slideshow)'), H, L('写真に文字は入れない・左1/6はぼかし', 'no text in the photo · left 1/6 fades')],
    ['.phero:not(.phero--plain) .phero__img', null, L('ヘッダー写真', 'Header photo'), H, L('左1/6はぼかし', 'left 1/6 fades')],
    ['.phero--plain .phero__txt', null, L('ヘッダー写真（任意）', 'Header photo (optional)'), H, L('追加すると写真付きの見出しに', 'adds a photo to this header')],
    ['.hs13--oil .hs13__bg', null, L('スライド画像', 'Slide image'), ['12:5', '2880×1200'], L('製品は右寄せ・左側は文字', 'product on the right, text on the left')],
    ['.hs13__banner', null, L('スライド画像（スマートフォン）', 'Slide image (phones)'), ['12:5', '2880×1200'], L('製品部分を切り取って表示', 'cropped to the product')],
    ['.hs13__bg:not(.hs13__bg--plain)', null, L('スライド背景', 'Slide background'), H, L('文字の背景・画面により切り取り', 'behind text, cropped by screen')],
    ['.hs13__bg--plain', null, L('スライド背景（任意）', 'Slide background (optional)'), H, ''],
    ['.ppan:not(.ppan--soon)', null, L('製品写真', 'Product photo'), S, L('白背景・製品は中央', 'white background, centred')],
    ['.split__img--win .win', null, L('写真', 'Photo'), S, L('円形に表示・主役は中央', 'shown as a circle, subject centred')],
    ['.win:not(.win--kj)', null, L('製品写真', 'Product photo'), S, L('円形に表示', 'shown as a circle')],
    ['.arch', null, L('写真', 'Photo'), P, L('上部は丸く切り取り', 'rounded at the top')],
    ['.office__main', null, L('写真', 'Photo'), P, ''],
    ['.ofc16__p figure', null, L('写真', 'Photo'), P, ''],
    ['.ofc16__w figure', null, L('写真', 'Photo'), H, ''],
    ['.office__l figure', null, L('写真', 'Photo'), H, ''],
    [':is(.collab__l, .ipcards) figure', null, L('IPコラボ画像', 'IP collaboration image'), S, ''],
    ['.film__v', null, L('動画', 'Film'), ['MP4', '1920×1080'], L('横長（約2.5:1）で表示', 'shown wide (about 2.5:1)')]
  ];

  var css = '.ig{position:absolute;z-index:6;top:10px;left:10px;display:block;max-width:calc(100% - 20px);padding:5px 9px 6px;border-radius:3px;' +
    'background:rgba(39,38,40,.84);color:#fff;font:500 11px/1.45 Jost,"Noto Sans JP",sans-serif;letter-spacing:.04em;text-align:left;' +
    'pointer-events:none;box-shadow:0 4px 12px -6px rgba(0,0,0,.5);white-space:normal}' +
    '.ig b{display:block;font-weight:500;font-size:12px;letter-spacing:.06em;color:#ffd0e3}' +
    '.ig i{display:block;font-style:normal;opacity:.8;font-size:10.5px}' +
    '.win .ig{top:6%;left:6%}' +
    '.arch .ig{top:auto;bottom:10px}' +
    '.collab__l figure .ig,.ipcards figure .ig{top:auto;bottom:10px}' +
    '.hs13__bg .ig{top:auto;left:auto;right:16px;bottom:96px}' +
    '.phero--plain .phero__txt>.ig{top:16px;left:auto;right:16px}' +
    '.ig-off .ig{display:none}' +
    '.ig-btn{position:fixed;z-index:60;left:14px;bottom:14px;padding:8px 14px;border:0;border-radius:20px;background:rgba(39,38,40,.88);color:#fff;' +
    'font:500 12px/1 Jost,"Noto Sans JP",sans-serif;letter-spacing:.06em;cursor:pointer;box-shadow:0 6px 18px -8px rgba(0,0,0,.5)}' +
    '.ig-btn:focus-visible{outline:2px solid #d92070;outline-offset:2px}' +
    '@media (max-width:760px){.ig{font-size:10px;padding:4px 7px}.ig b{font-size:11px}.hs13__bg .ig{bottom:auto;top:120px}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var done = new Set();
  SPOTS.forEach(function (s) {
    document.querySelectorAll(s[0]).forEach(function (el) {
      if (done.has(el)) return;
      done.add(el);
      if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
      var tag = document.createElement('span');
      tag.className = 'ig';
      tag.setAttribute('aria-hidden', 'true');
      tag.innerHTML = '<b>' + s[2] + '</b>' + s[3][0] + ' ・ ' + s[3][1] + 'px' + (s[4] ? '<i>' + s[4] + '</i>' : '');
      el.appendChild(tag);
    });
  });

  var KEY = 'hj-image-guide';
  var off = false;
  try { off = localStorage.getItem(KEY) === 'off'; } catch (e) {}
  var root = document.documentElement;
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'ig-btn';
  function paint() {
    root.classList.toggle('ig-off', off);
    btn.textContent = off ? L('画像ガイドを表示', 'Show image guide') : L('画像ガイドを隠す', 'Hide image guide');
    btn.setAttribute('aria-pressed', String(!off));
  }
  btn.addEventListener('click', function () {
    off = !off;
    try { localStorage.setItem(KEY, off ? 'off' : 'on'); } catch (e) {}
    paint();
  });
  paint();
  document.body.appendChild(btn);
})();
