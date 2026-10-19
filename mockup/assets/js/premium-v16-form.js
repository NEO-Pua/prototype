/* 花印 HANAJIRUSHI — premium v1.6 mockup only: the contact form's 確認 and 完了 screens, and a
   preview of the two emails the WordPress site sends (to the staff address in サイト設定, and the
   automatic reply to the customer). Nothing is sent. The steps, wording and email layout follow
   the WordPress build (wordpress/hanajirushi/page-contact.php, hanajirushi-core/inc/forms.php).
   An empty form is shown with sample values, so the screens can be reviewed without typing. */
(function () {
  if (document.documentElement.hasAttribute('data-live')) return;
  var form = document.getElementById('form');
  if (!form) return;
  var EN = (document.documentElement.lang || '').indexOf('en') === 0;
  var L = function (ja, en) { return EN ? en : ja; };
  var ARR = '<svg class="arr" viewBox="0 0 40 10" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true"><path d="M0 5h38M33 1l5 4-5 4"/></svg>';
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  // sample values by field position (the form's order), used only when the form is left empty
  var SAMPLE = EN
    ? ['', 'Sample Trading Pte. Ltd.', 'Singapore', 'Jane Tan', 'Purchasing Manager', 'jane.tan@sample-trading.example', '+65 6123 4567', '+65 9123 4567', 1, 'Singapore, Malaysia', 2, 2,
       'https://sample-trading.example', 'Drugstores, e-commerce', 'We are interested in distributing your products in Southeast Asia and would like to know your trade terms and minimum order quantities.', 0]
    : ['', '株式会社サンプル商事', 'シンガポール', '山田 太郎', '購買部長', 'yamada@sample-trading.example', '+65 6123 4567', '+65 9123 4567', 1, 'シンガポール、マレーシア', 2, 2,
       'https://sample-trading.example', 'ドラッグストア、EC', '貴社製品の東南アジアでの販売代理店について、取引条件と最小発注数量を伺いたく、お問い合わせいたしました。', 0];

  var JA = ['お問い合わせ種別', '会社名', '国・地域', 'お名前', '役職', 'メールアドレス', '電話番号', 'WhatsApp / WeChat', '事業形態', '対象市場',
            '年間予定仕入数量', 'ご関心の製品', '会社ウェブサイト', '現在の販売チャネル', 'お問い合わせ内容', '展示会'];

  function label(el) {
    var h = el.querySelector('legend, span');
    if (!h) return '';
    var c = h.cloneNode(true);
    [].forEach.call(c.querySelectorAll('em'), function (e) { e.remove(); });
    return c.textContent.trim();
  }
  function read(el) {
    if (el.tagName === 'FIELDSET') {
      return [].filter.call(el.querySelectorAll('input:checked'), Boolean).map(function (i) { return i.parentNode.textContent.trim(); }).join(L('、', ', '));
    }
    var f = el.querySelector('input, select, textarea');
    if (!f) return '';
    if (f.tagName === 'SELECT') return f.selectedIndex > 0 ? f.options[f.selectedIndex].text : '';
    return f.value.trim();
  }
  function sample(el, i) {
    var v = SAMPLE[i];
    if (typeof v !== 'number') return v || '';
    if (el.tagName === 'FIELDSET') {   // the first n options of a checkbox group
      return [].slice.call(el.querySelectorAll('label'), 0, v).map(function (l) { return l.textContent.trim(); }).join(L('、', ', '));
    }
    var s = el.querySelector('select');
    return s && s.options[v] ? s.options[v].text : '';
  }
  function collect() {
    var flds = [].slice.call(form.querySelectorAll('.fld'));
    var rows = flds.map(function (el) { return [label(el), read(el)]; });
    var typed = rows.slice(1).some(function (r) { return r[1]; });   // the enquiry type is always ticked
    if (!typed) rows = flds.map(function (el, i) { return [rows[i][0], i === 0 ? rows[0][1] : sample(el, i)]; });
    return { rows: rows, sample: !typed };
  }
  function bar(n) {
    var s = [L('入力', 'Enter'), L('確認', 'Confirm'), L('完了', 'Done')];
    return '<ol class="fstep">' + s.map(function (x, i) { return '<li' + (i === n ? ' class="on"' : '') + '><i>0' + (i + 1) + '</i>' + x + '</li>'; }).join('') + '</ol>';
  }
  var box = document.createElement('div');
  box.className = 'pform pform--main mk-step';
  box.hidden = true;
  form.parentNode.insertBefore(box, form.nextSibling);
  var mail = document.createElement('section');
  mail.className = 'mk-mail';
  mail.hidden = true;
  box.parentNode.insertBefore(mail, box.nextSibling);

  function show(el) { form.hidden = el !== form; box.hidden = el !== box; (el === form ? form : box).scrollIntoView({ block: 'start' }); }
  var data;

  function confirmView() {
    data = collect();
    var dl = data.rows.map(function (r) { return '<div><dt>' + esc(r[0]) + '</dt><dd>' + (r[1] ? esc(r[1]).replace(/\n/g, '<br>') : '—') + '</dd></div>'; }).join('');
    box.className = 'pform pform--main mk-step';
    box.innerHTML = bar(1) + '<p class="pform__h">' + L('以下の内容で送信します。よろしければ「送信する」を押してください。', 'Please check your enquiry, then send it.') + '</p>'
      + (data.sample ? '<p class="mk-note">' + L('（入力がないため、サンプルの内容で表示しています）', '(Nothing was entered, so sample values are shown.)') + '</p>' : '')
      + '<dl class="dl cfm">' + dl + '</dl>'
      + '<div class="pform__sub cfm__b"><button class="btn" type="button" data-back><span>' + L('入力画面に戻る', 'Edit') + '</span></button>'
      + '<button class="btn btn--fill" type="button" data-send><span>' + L('送信する', 'Send') + '</span>' + ARR + '</button></div>';
    mail.hidden = true;
    show(box);
  }

  function doneView() {
    box.className = 'pform pform--main pform--done mk-step';
    box.innerHTML = bar(2) + '<p class="pform__h">' + L('お問い合わせを受け付けました。', 'Thank you — your enquiry has been sent.') + '</p>'
      + '<p>' + L('内容を確認のうえ、3営業日以内に担当者よりご連絡いたします。受付確認のメールをお送りしましたので、あわせてご確認ください。', 'We will reply within 3 business days. A confirmation has been sent to your email address.') + '</p>'
      + '<div class="pform__sub"><a class="btn" href="index.html"><span>' + L('トップページへ', 'Back to the home page') + '</span>' + ARR + '</a></div>';
    mailView();
    show(box);
  }

  function mailView() {
    var get = function (i) { return (data.rows[i] || ['', ''])[1]; };
    var kind = get(0) || L('お問い合わせ', 'Enquiry'), company = get(1), name = get(3), email = get(5);
    var block = function (ja) {   // the staff email always uses the Japanese field names (forms.php)
      return data.rows.map(function (r, i) { return r[1] ? '■ ' + (ja ? JA[i] || r[0] : r[0]) + '\n' + r[1] : ''; }).filter(Boolean).join('\n\n');
    };
    var lines = block(false);
    var d = new Date(), p2 = function (n) { return ('0' + n).slice(-2); };
    var when = d.getFullYear() + '-' + p2(d.getMonth() + 1) + '-' + p2(d.getDate()) + ' ' + p2(d.getHours()) + ':' + p2(d.getMinutes());
    var title = '[' + kind + '] ' + company + '／' + name;
    var staff = block(true) + '\n\n---\n言語: ' + (EN ? 'EN' : 'JA') + ' / ページ: ' + location.href.split('#')[0].split('?')[0] + ' / 日時: ' + when;
    var pdf = 'https://…/company-profile.pdf';
    var reply = EN
      ? 'Dear ' + name + ',\n\nThank you for contacting Hanajirushi Institute of Cosmetics. We have received your message below and will reply within 3 business days.\n\nCompany profile (PDF): ' + pdf + '\n\n' + lines
      : name + ' 様\n\n花印粧業研究所株式会社です。お問い合わせありがとうございます。\n以下の内容で承りました。3営業日以内に担当者よりご連絡いたします。\n\n会社案内（PDF）: ' + pdf + '\n\n' + lines;
    var card = function (tag, rows, body, foot) {
      return '<article class="mk-mail__c"><b class="mk-mail__t">' + tag + '</b><dl>' + rows.map(function (r) { return '<dt>' + r[0] + '</dt><dd>' + esc(r[1]) + '</dd>'; }).join('') + '</dl>'
        + '<pre>' + esc(body) + '</pre>' + (foot ? '<p class="mk-mail__f">' + foot + '</p>' : '') + '</article>';
    };
    mail.innerHTML = '<h3 class="mk-mail__h">' + L('送信後に届くメール（イメージ）', 'The emails sent (preview)') + '</h3>'
      + '<p class="mk-mail__n">' + L('モックアップ用の表示です。実際のサイトでは、この画面には表示されません。', 'Shown in the mockup only — not on the real site.') + '</p>'
      + '<div class="mk-mail__g">'
      + card(L('社内への通知メール', 'Notification to your team'),
             [[L('宛先', 'To'), L('サイト設定 → お問い合わせ → 通知先メールアドレス', 'サイト設定 → お問い合わせ → 通知先メールアドレス')], [L('返信先', 'Reply-To'), name + ' <' + email + '>'], [L('件名', 'Subject'), '【花印サイト】' + title]],
             staff, L('送信内容は管理画面の「お問い合わせ履歴」にも保存されます。', 'Every enquiry is also saved under お問い合わせ履歴 in the admin.'))
      + card(L('お客様への自動返信メール', 'Automatic reply to the customer'),
             [[L('宛先', 'To'), email], [L('件名', 'Subject'), L('【花印】お問い合わせを受け付けました', 'Hanajirushi — we have received your message')]],
             reply, L('会社案内（PDF）の行は、サイト設定にPDFを登録したときだけ入ります。', 'The company-profile line appears only once a PDF is uploaded in サイト設定.'))
      + '</div>';
    mail.hidden = false;
  }

  // before premium.js, which stops every mockup form with a toast
  document.addEventListener('submit', function (e) {
    if (e.target !== form) return;
    e.preventDefault();
    e.stopPropagation();
    confirmView();
  }, true);
  box.addEventListener('click', function (e) {
    if (e.target.closest('[data-back]')) { mail.hidden = true; show(form); }
    else if (e.target.closest('[data-send]')) doneView();
  });
})();
