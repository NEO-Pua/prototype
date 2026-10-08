# -*- coding: utf-8 -*-
"""
花印 HANAJIRUSHI — "Direction B" premium site (chosen direction, 2026-10).

Run:  python build_premium.py      (build.py also runs it)
Writes ../premium/ja/ and ../premium/en/: 9 pages each (海外展開 is a section of 代理店募集),
the same pages as premium v1.1 in ../premium-1.1/ (see V11 below), and premium v1.2 in
../premium-1.2/: v1.1 plus a standalone Cosmoprof Asia buyer page (cosmoprof-asia/).

Copy and data come from build.py (t(), PRODUCTS(), NEWS(), MODES(), TERMS(), FAQ(),
JAPAN4(), WHY() ...), so every direction says exactly the same thing and follows the
same EN_ONLY rules. Only the markup and the skin differ: assets/css/premium.css +
assets/js/premium.js.

Visual language: warm kinari paper and deep plum, a softened 薄紅 pink as the accent,
円窓 round-window product frames, the 花印 seal as a recurring mark, vertical Mincho
headings in Japanese and Bodoni display type in English.

Business focus (feedback 2026-10): the home page opens with who we are and how to do
business with us; 「日本製」4つの強み and ビジネスパートナーに選ばれる理由 sit on the home
page; topic-based enquiry buttons (contact.html?topic=partner|product|oem|business
&item=pN) pre-select the contact form. Unconfirmed claims stay marked 要確認.

Premium v1.1 (review 2026-10): v1 plus layout fixes, each photo used once per page set,
and a restrained motion layer (assets/css/premium-v11.css + assets/js/premium-v11.js):
a once-per-visit opening on the home first view, headings revealed line by line, images
opened with wipes (円窓: an expanding circle, its gold ring drawn), count-up figures and
cross-page fades. Every v1.1 difference is gated by V11(); v1 output does not change.

Premium v1.3 (reviewer feedback 2026-10, 意見まとめ.xlsx): v1.2 made brighter and closer to the
V1 demo — white paper, V1 crimson #A51D34, light bands instead of plum, a crimson contact
band, light footer (assets/css/premium-v13.css); menu TOP／ブランド／製品／会社情報／お知らせ／
パートナーシップ／Cosmoprof Asia／お問い合わせ; Brand and Products as separate pages, with a
products list and one page per product (catalog.py, from the Rakuten store); a home slider
of large images; a short partnership section without figures. Gated by V13().
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as b
from build import t, EN, tbd, tbdw, TEL, FAX, HOURS, ADDR, I
import catalog as cat

OUT = os.path.join(b.ROOT, "premium")
OUT11 = os.path.join(b.ROOT, "premium-1.1")
OUT12 = os.path.join(b.ROOT, "premium-1.2")
OUT13 = os.path.join(b.ROOT, "premium-1.3")
OUT14 = os.path.join(b.ROOT, "premium-1.4")
OUT15 = os.path.join(b.ROOT, "premium-1.5")
_VER = 1.0

def V11():
    """True while building premium v1.1 or later (set by build())."""
    return _VER >= 1.1

def V12():
    """True while building premium v1.2: v1.1 plus the standalone Cosmoprof Asia buyer page."""
    return _VER >= 1.2

def V13():
    """True while building premium v1.3: v1.2 brightened, with separate Brand and Products pages."""
    return _VER >= 1.3

def V14():
    """True while building premium v1.4: the client's change proposal (2026-10-07) on v1.3 —
    official logo, the client's brand text and message, one button per slide, store chooser."""
    return _VER >= 1.4

def V15():
    """True while building premium v1.5: the client's second round (2026-10-07) — the logo's
    magenta #D92070 replaces the crimson, and the English pages carry no Japanese except the
    language switch, the logo, product names and ingredients as printed, the legal company name
    and the slogan (with its translation)."""
    return _VER >= 1.5

def EN15():
    """An English page of v1.5 or later: Japanese labels are left out or put into English."""
    return V15() and EN()

# v1.5 EN: the large faint word behind each page title, in place of the kanji. A word of its
# own rather than the title again (the client: 「重复的话，可以不显示」).
KJ_EN = {"花印": "Bloom", "製品": "Skincare", "銀座": "Ginza", "研究": "Lab", "協創": "Co-create",
         "協業": "Grow", "出展": "Meet us", "便り": "Updates", "相談": "Hello"}
# v1.5 EN: word stamps in English
SEAL_EN = {"特許": "Patent", "出展": "Expo", "募集中": "Join<br>us"}
SLOGAN_EN = "Helping every person’s own beauty bloom."

def LOGO():
    """The HANAJIRUSHI 花印 wordmark; v1.5 uses the official magenta version (LOGO－2020版 06)."""
    return "logo_v15.svg" if V15() else "logo.svg"

# v1.5: the brand film from the client's current site (2022, 0:50). The mockup plays it from
# there; the WordPress build takes it from サイト設定 (uploaded to the new site's media).
FILM_URL = "https://hanajirushi.co.jp/wp/wp-content/uploads/2022/06/hanajirushi.mp4"
FILM_POSTER_T = 12   # seconds: the logo on flowers, shown before play

def brand_film():
    """v1.5 home: the brand film under the brand text. It loads only its first frames until the
    visitor presses play (no autoplay, sound allowed); premium-v15.js starts it."""
    if not V15():
        return ""
    play = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>'
    return f'''<figure class="film rv" data-film>
<div class="film__v"><video src="{FILM_URL}#t={FILM_POSTER_T}" preload="metadata" playsinline controlslist="nodownload" aria-label="{t("花印 ブランドムービー","Hanajirushi brand film")}"></video>
<button class="film__play" type="button" aria-label="{t("ブランドムービーを再生（0:50・音声あり）","Play the brand film (0:50, with sound)")}"><span class="film__ic">{play}</span></button></div>
<figcaption class="film__cap"><b>{t("花印 ブランドムービー","Hanajirushi brand film")}</b><i data-film-len>0:50</i>{tbd("映像内の製品 要確認","Products shown TBC")}</figcaption>
</figure>'''

def MAP():
    """The sales map; v1.5 recolours the markets to the logo magenta."""
    return "world_map_v15.png" if V15() else "world_map_brand.png"

def slogan_en(cls=""):
    """v1.5 EN: the slogan stays in Japanese, with this English line under it."""
    return f'<p class="slogan-en {cls}">{SLOGAN_EN}</p>' if EN15() else ''
ASSETS = "../../assets/"
IMG = ASSETS + "img/"
FONTS = ("family=Zen+Old+Mincho:wght@400;500;600&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400;1,6..96,500"
         "&family=Noto+Sans+JP:wght@300;400;500&family=Jost:wght@300;400;500")

ARR = '<svg class="arr" viewBox="0 0 40 10" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true"><path d="M0 5h38M33 1l5 4-5 4"/></svg>'

# ------------------------------------------------------------ primitives
def seal(txt="花印", cls=""):
    """The 花印 seal (落款). Square, filled, characters set vertically.
    v1.4: the client allows only the official logo (change proposal 2026-10-07), so the 花印 seal
    is the official square mark; the white-square version shows on the crimson contact band.
    Word stamps (特許, 出展, 募集中) are not the logo and stay."""
    if EN15() and txt in SEAL_EN:
        return f'<span class="seal seal--en {cls}" aria-hidden="true"><span>{SEAL_EN[txt]}</span></span>'
    if V14() and txt == "花印":
        return (f'<span class="seal seal--logo {cls}" aria-hidden="true"><img class="lm" src="{IMG}logo_mark.png" alt="">'
                f'<img class="lm-w" src="{IMG}logo_mark_w.png" alt=""></span>')
    return f'<span class="seal {cls}" aria-hidden="true"><span>{txt}</span></span>'

def eb(word, num=""):
    n = f'<i>{num}</i>' if num else ''
    return f'<p class="eb">{n}<span>{word}</span></p>'

def lines(html):
    """v1.1: one masked span per heading line (split on <br>), so lines can be revealed in
    turn. An <em> that runs across a break is closed and reopened. v1: unchanged."""
    if not V11():
        return html
    # Bodoni italic capitals space "HANAJIRUSHI" unevenly (it reads "HAN AJIRUSHI"); title case in italic headings
    html = html.replace("<em>HANAJIRUSHI", "<em>Hanajirushi")
    out, carry = [], False
    for i, seg in enumerate(html.split("<br>")):
        if carry:
            seg = "<em>" + seg
        carry = seg.count("<em>") > seg.count("</em>")
        if carry:
            seg += "</em>"
        out.append(f'<span class="ln" style="--i:{i}"><span>{seg}</span></span>')
    return "".join(out)

def shd(num, word, ja, en, kj=None, lead=None, cls=""):
    """Section heading. JA: Mincho title. EN: Bodoni title + small kanji accent."""
    k = f'<p class="kj">{kj}</p>' if (EN() and kj and not V15()) else ''
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="shd {cls}">{eb(word, num)}<h2 class="h2">{lines(t(ja, en))}</h2>{k}{l}</div>'

def lnk(href, ja, en, cls=""):
    return f'<a class="lnk {cls}" href="{href}"><span>{t(ja, en)}</span>{ARR}</a>'

def btn(href, ja, en, cls=""):
    return f'<a class="btn {cls}" href="{href}"><span>{t(ja, en)}</span>{ARR}</a>'

def win(img, alt="", cls=""):
    """円窓 — round window frame with an offset gold ring."""
    if img:
        inner = f'<img src="{IMG}{img}" alt="{alt}" loading="lazy">'
    else:
        inner = f'<span class="win__ph">{seal()}<small>{t("近日公開","Coming soon")}</small></span>'
    return f'<figure class="win {cls}"><div class="win__c">{inner}</div></figure>'

def pname(s):
    """Product names: let long katakana names wrap between words, not mid-word."""
    return s.replace("花印", "花印<wbr>", 1).replace("フェイスマスク", "<wbr>フェイスマスク")

def nobr(s):
    return s.replace("<br>", "" if not EN() else " ")

# ------------------------------------------------------------ enquiry entry points
# Topic slugs match build.CTA_TOPICS and the contact form's radio values.
TOPIC = {
    "partner":  ("販売パートナーについて相談する", "Become a sales partner"),
    "product":  ("商品について相談する", "Ask about our products"),
    "oem":      ("OEM・共同開発について相談する", "Discuss OEM &amp; co-development"),
    "business": ("ビジネスについて相談する", "Discuss your business"),
}

def topic_href(topic, item=None):
    return f"contact.html?topic={topic}" + (f"&amp;item={item}" if item else "") + "#form"

def cta_btn(topic, cls="", item=None, label=None):
    ja, en = label or TOPIC[topic]
    return btn(topic_href(topic, item), ja, en, cls)

def cta_lnk(topic, cls="", item=None, label=None):
    ja, en = label or TOPIC[topic]
    return lnk(topic_href(topic, item), ja, en, cls)

# ------------------------------------------------------------ chrome
def head(title, desc, pg):
    return f'''<!DOCTYPE html>
<html lang="{b.L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<script>document.documentElement.classList.add('js')</script>{intro_js(pg)}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ASSETS}css/premium.css">{v11_css()}{v12_css(pg)}{v13_css()}
</head>
<body class="pg-{pg}">
<a class="skip" href="#main">{t("本文へスキップ","Skip to content")}</a>'''

def intro_js(pg):
    """v1.1 home: play the opening sequence once per visit (per browser tab), never when the
    visitor asked for reduced motion."""
    if not (V11() and pg == "home") or V13():   # v1.3: the first view is a photo slider, no 円窓 opening
        return ""
    return ("\n<script>try{if(!sessionStorage.getItem('hj-intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches)"
            "{document.documentElement.classList.add('intro');sessionStorage.setItem('hj-intro','1')}}catch(e){}</script>")

def v12_css(pg):
    return f'\n<link rel="stylesheet" href="{ASSETS}css/premium-v12.css">' if V12() else ''

def v11_css():
    return f'\n<link rel="stylesheet" href="{ASSETS}css/premium-v11.css">' if V11() else ''

def v13_css():
    return (f'\n<link rel="stylesheet" href="{ASSETS}css/premium-v13.css">' if V13() else '') + (f'\n<link rel="stylesheet" href="{ASSETS}css/premium-v14.css">' if V14() else '') + (f'\n<link rel="stylesheet" href="{ASSETS}css/premium-v15.css">' if V15() else '')

# Global menu kept short (feedback 2026-10: 「菜单不要太多」): four sections plus the show and
# the contact button. Secondary pages sit under a parent: reached from the parent page's
# section bar, the breadcrumb, the phone menu's sub-links and the footer.
def NAV():
    if V13():   # reviewer 2026-10: TOP／ブランド／製品／会社情報／お知らせ／パートナーシップ (then Cosmoprof Asia, お問い合わせ)
        return [("index.html", "TOP", t("Top","トップ"), []),
                ("brand.html", t("ブランド","Brand"), t("Brand","ブランド"),
                 [("collaboration.html", t("IPコラボレーション","IP collaborations"))]),
                ("products.html", t("製品","Products"), t("Products","製品"), []),
                ("company.html", t("会社情報","Company"), t("Company","会社情報"),
                 [("rd.html", t("研究開発・品質","R&amp;D &amp; quality"))]),
                ("news.html", t("お知らせ","News"), t("News","お知らせ"), []),
                ("partners.html", t("パートナーシップ","Partnership"), t("Partnership","パートナーシップ"), [])]
    return [("brand.html", t("ブランド・製品","Brand &amp; Products"), t("Brand","ブランド・製品"),
             [("collaboration.html", t("IPコラボレーション","IP collaborations"))]),
            ("partners.html", t("代理店募集","Partnership"), t("Partnership","代理店募集"), []),
            ("company.html", t("企業情報","Company"), t("Company","企業情報"),
             [("rd.html", t("研究開発・品質","R&amp;D &amp; quality"))]),
            ("news.html", t("お知らせ","News"), t("News","お知らせ"), [])]

PARENT = {"collaboration.html": "brand.html", "rd.html": "company.html"}

def parent_of(fn):
    if V13() and fn.startswith("product-"):
        return "products.html"
    return PARENT.get(fn)

def header(fn):
    cur = lambda h: " aria-current=page" if h == fn else (" aria-current=true" if h == parent_of(fn) else "")
    nav = ''.join(f'<li><a href="{h}"{cur(h)}>{j}</a></li>' for h, j, e, kids in NAV())
    nav += f'<li class="hd__ev"><a href="{lp_href() if V12() else "exhibition.html"}"{cur("exhibition.html")}>Cosmoprof Asia</a></li>'
    top = [] if V13() else [("index.html", t("トップ","Top"), t("Top","トップ"), [])]   # v1.3: TOP is already in the menu
    pages = top + NAV() + [("contact.html", t("お問い合わせ","Contact"), t("Contact","お問い合わせ"), [])]
    def sub(kids):
        return ('<ul class="menu__sub">' + ''.join(f'<li><a href="{h}"{" aria-current=page" if h == fn else ""}>{x}</a></li>' for h, x in kids) + '</ul>') if kids else ''
    mlist = ''.join(f'<li><a href="{h}"{" aria-current=page" if h == fn else ""}><i>{i:02d}</i><b>{j}</b>{"" if EN15() else f"<small>{e}</small>"}</a>{sub(kids)}</li>' for i, (h, j, e, kids) in enumerate(pages))
    ja_on, en_on = ("on", "") if not EN() else ("", "on")
    lng = f'<span class="lng" role="group" aria-label="Language"><a href="../ja/{fn}" class="{ja_on}" lang="ja">JA</a><a href="../en/{fn}" class="{en_on}" lang="en">EN</a></span>'
    return f'''<header class="hd" data-hd>
<div class="hd__in">
<a class="hd__logo" href="index.html"><img src="{IMG}{LOGO()}" alt="花印 HANAJIRUSHI" width="132" height="35"></a>
<nav class="hd__nav" aria-label="{t("メインメニュー","Main menu")}"><ul>{nav}</ul></nav>
<div class="hd__r">{lng}
<a class="hd__cta" href="contact.html">{t("お問い合わせ","Contact")}</a>
<button class="hd__menu" type="button" aria-expanded="false" aria-controls="menu"><span class="bars"><i></i><i></i></span><span class="m">Menu</span><span class="c">Close</span></button>
</div></div>
</header>
<div class="menu" id="menu" aria-hidden="true"><div class="menu__in">
<ul class="menu__l">{mlist}</ul>
<div class="menu__side">{"" if V12() else seal(cls="seal--m")}
{"" if V12() else f'<p class="menu__co">{t("花印粧業研究所株式会社","Hanajirushi Institute of Cosmetics, Inc.")}</p>'}
{"" if V12() else f'<p>{ADDR(True)}</p>'}
<p class="menu__tel"><a href="tel:+81362642154">{TEL()}</a><small>{HOURS()}</small></p>
<a class="menu__exh" href="{lp_href() if V12() else "exhibition.html"}"><small>Exhibition</small><b>Cosmoprof Asia 2026</b><span>{t("2026年11月・香港 — 商談予約受付中","Hong Kong, November 2026 — book a meeting")}</span></a>
{"" if V12() else lng}</div>
</div></div>
<main id="main">'''

def contact_band():
    return f'''<section class="cta">
<div class="wrap cta__in rv">
{seal(cls="seal--m")}
<div class="cta__h">{eb("Contact")}<h2 class="h2">{lines(t("お取引・代理店に関する<br>ご相談を承ります。","Interested in distributing<br><em>HANAJIRUSHI?</em>"))}</h2>
<p>{t("製品・OEM/ODM・海外展開のご相談も承ります。3営業日以内にご返信します。","Product, OEM/ODM and market-entry enquiries welcome. We reply within 3 business days.")}</p></div>
<div class="cta__r"><p class="cta__tel"><small>{t("お電話でのお問い合わせ","Call our Tokyo office")}</small><a href="tel:+81362642154">{TEL()}</a><small>{HOURS()}</small></p>
<div class="cta__b">{cta_btn("partner","btn--fill")}{cta_btn("business")}</div>
<p class="cta__more">{cta_lnk("product","lnk--s")}{cta_lnk("oem","lnk--s")}</p></div>
</div></section>'''

def footer(fn):
    glob = ("partners.html#network", t("海外展開・販売実績","Global network"))
    cols = [
     (t("ブランド・製品","Brand &amp; products"), [("brand.html",t("ブランドについて","About the brand")),("brand.html#p1",t("クレンジングローション","Deep Cleansing Lotion")),("brand.html#p2",t("フェイスマスク","Super Moisture Face Mask")),("brand.html#p3",t("ハトムギ化粧水","Hatomugi Skin Conditioner")),("collaboration.html",t("IPコラボレーション","IP collaborations"))]),
     (t("企業情報","Company"), [("company.html",t("会社概要","Company profile")),("company.html#history",t("沿革","History")),("rd.html",t("研究開発・品質管理","R&amp;D and quality"))] + ([] if V11() else [glob]) + [("news.html",t("お知らせ","News"))]),
     (t("お取引について","Business"), [("partners.html",t("海外代理店・パートナー募集","Partnership programme"))] + ([glob] if V11() else []) + [("partners.html#terms",t("取引条件・輸出書類","Trade terms &amp; export documents")),("exhibition.html",t("展示会情報","Exhibitions")),("contact.html",t("お問い合わせ","Contact"))]),
    ]
    if V13():
        by = cat.BY_SLUG()
        cols = [
         (t("ブランド","Brand"), [("brand.html",t("ブランドについて","About the brand")),("collaboration.html",t("IPコラボレーション","IP collaborations")),("rd.html",t("研究開発・品質管理","R&amp;D and quality"))]),
         (t("製品","Products"), [("products.html",t("製品一覧","All products"))] + [(cat.page_of(by[s]), by[s]["name"]) for s in cat.FEATURED[:4]]),
         (t("会社情報","Company"), [("company.html",t("会社概要","Company profile"))] + ([] if V14() else [("company.html#history",t("沿革","History"))]) + [("company.html#access",t("アクセス","Access")),("news.html",t("お知らせ","News"))]),
         (t("パートナーシップ","Partnership"), [("partners.html",t("海外代理店・パートナー募集","Partnership programme")),glob,("exhibition.html",t("展示会情報","Exhibitions")),("contact.html",t("お問い合わせ","Contact"))]),
        ]
    cg = ''.join(f'<div><h3>{h}</h3><ul>' + ''.join(f'<li><a href="{u}">{x}</a></li>' for u, x in items) + '</ul></div>' for h, items in cols)
    other = "en" if not EN() else "ja"
    band = '' if fn == "contact.html" else contact_band()
    return f'''</main>
{band}
<footer class="ft"><div class="wrap">
<div class="ft__top">
<div class="ft__co"><a class="ft__logo" href="index.html"><img src="{IMG}{LOGO()}" alt="花印 HANAJIRUSHI" width="150" height="40"></a>{seal(cls="seal--s")}
<p class="ft__name">{t("花印粧業研究所株式会社","Hanajirushi Institute of Cosmetics, Inc.")}</p>
<p>{ADDR(True)}</p><p class="ft__tel">TEL {TEL()}<br>FAX {FAX()}</p></div>
<nav class="ft__nav" aria-label="{t("フッターメニュー","Footer menu")}">{cg}</nav>
</div>
<div class="ft__btm"><p>© 2026 Hanajirushi Institute of Cosmetics, Inc.</p>
<div><a href="#">{t("プライバシーポリシー","Privacy policy")}</a><a href="../{other}/{fn}">{t("English","日本語")}</a></div></div>
</div></footer>
<button class="totop" type="button" aria-label="{t("ページトップへ","Back to top")}">{I["up"]}</button>
<div class="toast" role="status" aria-live="polite"></div>
<script src="{ASSETS}js/premium.js"></script>{f'\n<script src="{ASSETS}js/premium-v11.js"></script>' if V11() else ''}{f'\n<script src="{ASSETS}js/premium-v12.js"></script>' if V12() and fn == "index.html" else ''}{f'\n<script src="{ASSETS}js/premium-v13.js"></script>' if V13() else ''}{f'\n<script src="{ASSETS}js/premium-v14.js"></script>' if V14() else ''}{f'<script src="{ASSETS}js/premium-v15.js"></script>' if V15() and fn == "index.html" else ''}
</body></html>'''

def page(fn, pg, title, desc, body):
    if fn == "index.html":
        full = t("花印 HANAJIRUSHI 公式サイト｜花印粧業研究所株式会社", "HANAJIRUSHI | Japanese Skincare from Ginza, Tokyo")
    else:
        full = t(f"{title}｜花印 HANAJIRUSHI 公式サイト", f"{title} | HANAJIRUSHI — Japanese Skincare, Ginza Tokyo")
    return head(full, desc, pg) + header(fn) + body + footer(fn)

def phero(label, ja, en, sub, img, kanji, anchors, pos="center", parent=None, variant=""):
    """Lower-page hero: title on paper, full-height photograph (right), large vertical kanji.
    img=None gives the plain variant (paper only) for utility pages."""
    title = t(ja, en)
    # an entry ending in .html links to a child page (last, with an arrow)
    anc = ''.join(f'<a class="anc__pg" href="{i}">{x}</a>' if i.endswith(".html") else f'<a href="#{i}">{x}</a>' for i, x in anchors)
    up = f'<a href="{parent[0]}">{parent[1]}</a>' if parent else ""
    pic = f'<div class="phero__img"><img src="{IMG}{img}" alt="" style="object-position:{pos}"></div>' if img else ''
    navs = f'<nav class="anc" aria-label="{t("ページ内リンク","On this page")}"><div class="wrap">{anc}</div></nav>' if anchors else ''
    cls = ("" if img else " phero--plain") + (f" phero--{variant}" if variant else "")
    return f'''<section class="phero{cls}">
<div class="phero__txt"><div class="phero__t rv">{eb(label)}<h1>{lines(title)}</h1>{f'<p class="kj">{ja.replace("<br>", "")}</p>' if EN() and not V15() else ''}<p class="phero__sub">{sub}</p></div>
{f'<p class="phero__kj phero__kj--en" aria-hidden="true">{KJ_EN[kanji]}</p>' if EN15() else f'<p class="phero__kj" aria-hidden="true">{kanji}</p>'}</div>
{pic}
</section>
<nav class="crumb" aria-label="breadcrumb"><div class="wrap"><a href="index.html">{t("ホーム","Home")}</a>{up}<span>{title.replace("<br>", "")}</span></div></nav>
{navs}'''

def store_section():
    """JA: domestic store logos. EN_ONLY: no consumer store links — a distributor line instead."""
    if EN():
        return f'''<section class="stores" id="stores"><div class="wrap stores__en rv">
<p class="eb"><span>Where to buy</span></p><h2>Looking for {"Hanajirushi" if V12() else "HANAJIRUSHI"} in your country?</h2>
<p>We are building our distributor network. Contact us to find a local partner — or to become one.</p>
{lnk("partners.html","","Find / become a distributor")}</div></section>'''
    s = [("rakuten.svg","楽天市場 公式ショップ"),("amazon.png","Amazon 公式ストア"),("yahoo.svg","Yahoo!ショッピング"),("qoo10.png","Qoo10 公式ショップ")]
    li = ''.join(f'<li><a href="#"><img src="{IMG}{im}" alt="{x}"><small>{x}</small></a></li>' for im, x in s)
    return f'''<section class="stores" id="stores"><div class="wrap rv">
<p class="eb"><span>Online store</span></p><h2>国内公式オンラインストア</h2><ul class="stores__l">{li}</ul></div></section>'''

# ------------------------------------------------------------ shared blocks
def flow(steps):
    return '<ol class="flow">' + ''.join(f'<li class="rv"><i>{i+1:02d}</i><h3>{a}</h3><p>{d}</p></li>' for i, (a, d) in enumerate(steps)) + '</ol>'

def numbered(items, cls=""):
    """Numbered pairs (title, text[, extra html]) — 選ばれる理由, merits, reasons."""
    out = ''
    for i, it in enumerate(items):
        h, p = it[0], it[1]
        x = it[2] if len(it) > 2 else ''
        out += f'<li class="rv"><span class="nums2__n">{i+1:02d}</span><div><h3>{h}</h3>{f"<p>{p}</p>" if p else ""}{x}</div></li>'
    return f'<ol class="nums2 {cls}">{out}</ol>'

def docs_list():
    return '<ul class="docl">' + ''.join(f'<li class="rv"><b>{a}</b><span>{d}</span></li>' for a, d in b.EXPORT_DOCS()) + '</ul>'

def reg_table():
    regs = b.REGS()
    rows = ''.join(f'<tr><th>{a}{"" if EN() else f"<small>{e}</small>"}</th><td>{d}</td>' + (f'<td rowspan="{len(regs)}" class="mtbl__m">{b.REG_SUPPORT()}</td>' if i == 0 else '') + '</tr>' for i, (a, e, d) in enumerate(regs))
    return f'<div class="sx"><table class="mtbl"><thead><tr><th>{t("対象市場","Market")}</th><th>{t("主な手続き・必要資料","Typical requirement")}</th><th>{t("花印の対応","Our support")}</th></tr></thead><tbody>{rows}</tbody></table></div>'

def ip_cards(detail=False):
    out = ''
    for im, n, s, l, c, ch in b.IPS():
        dl = (f'<dl><div><dt>{t("商品","Product")}</dt><dd>{s}</dd></div><div><dt>{t("販売","Channel")}</dt><dd>{ch or tbd()}</dd></div>'
              f'<div><dt>{t("区分","Type")}</dt><dd>{t("正規ライセンス商品","Officially licensed")}</dd></div></dl>') if detail else f'<small>{s}</small>'
        out += f'<li class="rv"><figure><img src="{IMG}{im}" alt="{n}" loading="lazy"></figure><p><b>{n}</b>{dl}</p><span class="tag">{l}</span></li>'
    return out

def IPNOTE():
    return t("すべてのコラボレーション商品は正規ライセンス品です。ライセンス証明書類はお取引先にご提示できます。","All collaboration products are officially licensed. Proof of licence is available to trade partners.")

# ============================================================ TOP
def h_hero():
    p = b.PRODUCTS()[2]  # Hatomugi: the long-seller, and the calmest packshot
    made = tbd("製造地 要確認", "Manufacturing site TBC")
    ctas = f'{btn("partners.html","代理店・パートナー募集","Become a partner","btn--fill")}{lnk("brand.html","製品を見る","View products")}'
    if EN():
        head_ = b.FV_HEAD().replace("<br>", "<br><em>") + "</em>"
        if V11():
            # three balanced lines instead of five: "Japanese-quality / skincare, delivered / to the world."
            a1, a2 = b.FV_HEAD().split("<br>")[0].split(" ", 1)
            d1, d2 = b.FV_HEAD().split("<br>")[1].split(" ", 1)
            head_ = lines(f'<span class="nw">{a1}</span><br>{a2} <em>{d1}</em><br><em>{d2}</em>')
        txt = f'''<div class="hero__txt{rv()}">
{eb("Japanese Skincare Maker — Ginza, Tokyo")}
<h1 class="hero__h">{head_}</h1>
<p class="hero__lead">{b.FV_LEAD1()} {made}<br>{nobr(b.FV_LEAD2())}</p>
<div class="hero__ctas">{ctas}</div>
</div>'''
    else:
        head_ = lines(b.FV_HEAD().replace("日本品質の", "日本品質の<br>"))  # three short vertical columns
        txt = f'''<div class="hero__txt{rv()}">
<h1 class="hero__tate">{head_}</h1>
<div class="hero__side">{eb("Japanese Skincare Maker — Ginza, Tokyo")}
<p class="hero__lead">{b.FV_LEAD1()}{made}<br>{nobr(b.FV_LEAD2())}</p>
<div class="hero__ctas">{ctas}</div></div>
</div>'''
    vis = f'''<div class="hero__vis{rv()}">{win(p["img"], p["name"], "win--xl")}{seal(cls="seal--l")}
<p class="hero__cap"><span>No.03</span>{p["name"]}　500mL</p>
<p class="hero__jp" aria-hidden="true">ひとりに、ひとつの、キレイを咲かせる。</p></div>'''
    if V12():
        return hero_slides(txt, vis)
    return f'''<section class="hero">
<div class="hero__bg" aria-hidden="true"><img src="{IMG}h_hanajirushi_top-1.jpg" alt=""></div>
<div class="wrap hero__in">
{txt}
{vis}
</div>
<a class="hero__note" href="{lp_href() if V12() else "#exhibition"}"><span class="hero__note-k">{t("出展","Exhibiting")}</span><b>Cosmoprof Asia 2026</b><span>{t("2026年11月・香港 — 商談予約受付中","Hong Kong, November 2026 — book a meeting")}</span>{ARR}</a>
<p class="hero__scroll" aria-hidden="true">Scroll</p>
</section>'''

# ------------------------------------------------------------ home slider (v1.2)
# The announcement slides as data, field for field the kv_slide post type in WORDPRESS.md
# §4.1, so the WordPress build is a one-to-one copy. No HTML in any field: the theme does the
# layout (line reveal, accent colour, Latin in Bodoni, 円窓). Order = menu order.
MOCK_TODAY = "2026-10-02"   # the mockup's "today" for start / end dates

def SLIDES():
    return [
        dict(label=t("展示会", "Exhibition"),
             line1=t("Cosmoprof Asia 2026に", "Meet us at"), line2=t("出展します。", "Cosmoprof Asia 2026"),
             text=t("2026年11月、香港コンベンション＆エキシビションセンター。ブースでの商談のご予約を受け付けています。",
                    "November 2026, Hong Kong Convention & Exhibition Centre. Meetings at our booth can be booked now."),
             button=t("展示会専用ページへ", "Open the event page"), link=lp_href(),
             visual="kanji", kanji="出展", caption="Hong Kong 2026", seal="",
             start="2026-09-15", end="2026-11-30",
             tbc=t("日程確定待ち", "Dates TBC")),
        dict(label=t("新製品", "New product"),
             line1=t("中国市場の看板アイテムを、", "Our signature item in China —"), line2=t("日本でも。", "coming to Japan."),
             text=t("花印クレンジングオイルの、日本公式サイトでのご紹介を準備しています。",
                    "We are preparing to introduce HANAJIRUSHI Cleansing Oil in Japan."),
             button=t("詳しく見る", "Details"), link="brand.html#p4",
             visual="kanji", kanji="新", caption="Coming soon", seal="",
             start="2026-09-01", end="",
             tbc=t("発売時期 要確認", "Launch date TBC")),
        dict(label=t("特許", "Patent"),
             line1=t("特許技術を採用した、", "A cleansing lotion"), line2=t("クレンジングローション。", "with patented technology."),
             text=t("うるおい残してしっかり落ちる、拭き取りタイプのクレンジングウォーター。",
                    "Wipe-off cleansing water that removes makeup thoroughly while keeping skin moist."),
             button=t("製品を見る", "View the product"), link="brand.html#p1",
             visual="product", product="p1", seal="特許",
             start="", end="",
             tbc=t("特許番号 要確認", "Patent no. TBC")),
    ]

# Character limits the admin enforces (full-width = 1, half-width = 0.5)
LIMITS = {"ja": dict(line=14, text=60), "en": dict(line=32, text=130)}

def _width(x):
    return sum(.5 if ord(c) < 0x2E80 else 1 for c in x)

def kv_slide(sl, i, n):
    """One announcement slide from its fields: what template-parts/kv-slide.php will print."""
    lim = LIMITS[b.L]
    for f in ("line1", "line2"):
        assert _width(sl[f]) <= lim["line"], f"slide {i + 2}: {f} is over {lim['line']}: {sl[f]}"
    assert _width(sl["text"]) <= lim["text"], f"slide {i + 2}: text is over {lim['text']}"
    esc = lambda x: html.escape(x, quote=False)
    def latin(x):  # Japanese headlines: Latin words in Bodoni, kept together with the next character
        x = esc(x)
        return x if EN() else re.sub(r"([A-Za-z0-9][A-Za-z0-9 .\-]*[A-Za-z0-9])(\S?)",
                                     r'<span class="nw"><span class="lat">\1</span>\2</span>', x)
    head = lines(f"{latin(sl['line1'])}<br><em>{latin(sl['line2'])}</em>")
    if sl["visual"] == "product":
        pr = {x["id"]: x for x in b.PRODUCTS()}[sl["product"]]
        vis = win(pr["img"], pr["name"], "win--xl")
    elif sl["visual"] == "photo":
        vis = win(sl["photo"], "", "win--xl")
    else:  # kanji: 1-2 characters in a plum 円窓, with a small caption
        vis = (f'<figure class="win win--xl win--kj"><div class="win__c"><span class="win__kj">{esc(sl["kanji"])}</span>'
               f'<small>{esc(sl["caption"])}</small></div></figure>')
    if sl["seal"]:
        vis += seal(esc(sl["seal"]), "seal--l seal--txt")
    chip = tbd(sl["tbc"], sl["tbc"]) if sl.get("tbc") else ""   # mockup only: facts awaiting confirmation
    return f'''
<div class="hs__s" role="group" aria-roledescription="slide" aria-label="{i + 2} / {n}" aria-hidden="true">
<div class="wrap hero__in"><div class="hs__txt"><p class="hs__k">{esc(sl["label"])}</p><h2 class="hs__h">{head}</h2>
<p class="hero__lead">{esc(sl["text"])}{chip}</p><div class="hero__ctas">{btn(sl["link"], sl["button"], sl["button"], "btn--fill")}</div></div>
<div class="hs__vis">{vis}</div></div></div>'''

def live(sl):
    return (not sl["start"] or sl["start"] <= MOCK_TODAY) and (not sl["end"] or MOCK_TODAY <= sl["end"])

def hero_slides(txt, vis):
    """v1.2 home: important news rotates in the first view (feedback 2026-10: 展会・产品发布・
    专利获得). Slide 1 is the brand/business hero, unchanged (an Options page in WordPress);
    the announcement slides come from SLIDES()."""
    slides = [x for x in SLIDES() if live(x)]
    labels = [t("花印について", "HANAJIRUSHI")] + [x["label"] for x in slides]
    n = len(labels)
    first = (f'<div class="hs__s is-on" role="group" aria-roledescription="slide" aria-label="1 / {n}">'
             f'<div class="wrap hero__in">\n{txt}\n{vis}\n</div></div>')
    rest = "".join(kv_slide(x, i, n) for i, x in enumerate(slides))
    tabs = "".join(f'<li><button type="button" data-go="{i}"{" aria-current=true" if i == 0 else ""}><span>{html.escape(lab, quote=False)}</span><i></i></button></li>'
                   for i, lab in enumerate(labels))
    return f'''<section class="hero hero--slides" data-first aria-roledescription="carousel" aria-label="{t("注目のお知らせ","Highlights")}">
<div class="hero__bg" aria-hidden="true"><img src="{IMG}h_hanajirushi_top-1.jpg" alt=""></div>
<div class="hs"><div class="hs__track">{first}{rest}</div></div>
<div class="hs__ui"><p class="hs__n"><b>01</b><span>/ {n:02d}</span></p>
<ol class="hs__tabs">{tabs}</ol>
<div class="hs__btns"><button type="button" class="hs__play" aria-label="{t("一時停止","Pause")}" data-pause="{t("一時停止","Pause")}" data-play="{t("再生","Play")}"><i></i></button></div></div>
</section>'''

# v1.3 home order: news → products → brand → 日本製 → collaboration → partnership → company
HOME13 = {"news": "01", "products": "02", "brand": "03", "japan": "04", "collab": "05", "partners": "06", "company": "07"}

def hn(key, default):
    return HOME13[key] if V13() else default

def rv():
    """v1: the home first view fades in like every other block. v1.1: it has its own
    entrance (premium-v11.css), so it must not wait for the scroll reveal."""
    return "" if V11() else " rv"

def h_numbers():
    items = b.REASONS()
    order = [0, 2, 1, 3, 4, 5]
    li = ''.join(f'<li class="rv"><small>{items[i][0]}</small><b class="{"num" if items[i][1][:1].isdigit() else "word"}">{items[i][1]}</b><p>{items[i][3]}</p></li>' for i in order)
    return f'''<section class="nums"><div class="wrap">
<ul class="nums__l">{li}</ul>
<p class="note">{t("※ 特許番号・販売国一覧は確認のうえ掲載します","Patent number and country list to be published once confirmed")} {tbd()}</p>
</div></section>'''

def h_japan4():
    kan = ["研", "造", "質", "績"]
    li = ''.join(f'<li class="rv"><span class="j4__k{" j4__k--ic" if EN15() else ""}" aria-hidden="true">{I[ic] if EN15() else kan[i]}</span><p class="j4__n">{i+1:02d}</p><h3>{h}</h3><p>{d}</p>{note}</li>'
                 for i, (ic, h, d, note) in enumerate(b.JAPAN4()))
    return f'''<section class="sec dark j4" id="japan"><div class="wrap">
{shd(hn("japan","01"),"Made in Japan","「日本製」4つの強み","Made in Japan —<br><em>four strengths</em>", kj="日本製の強み", cls="shd--c",
     lead=t("「日本製」というラベルだけでなく、その中身をお伝えします。","Not just a label — what “Made in Japan” means for your business."))}
<ol class="j4__l">{li}</ol>
<div class="ctr">{lnk("rd.html","研究開発・品質管理を見る","R&amp;D and quality")}</div>
</div></section>'''

def soon_note(prods):
    """v1.1: products without a photo get one quiet line under the grid, not an empty slot."""
    return ''.join(f'<p class="col__soon rv"><i>No.{i+1:02d}</i>{p["name"]} — {p["short"]} <a href="brand.html#{p["id"]}">{t("詳しく見る","Details")}</a></p>'
                   for i, p in prods if not p["img"])

def h_collection():
    cards = ''
    for i, p in enumerate(b.PRODUCTS()):
        if V11() and not p["img"]:
            continue
        cards += f'''<li class="rv"><a href="brand.html#{p["id"]}">{win(p["img"], p["name"])}
<p class="col__no">No.{i+1:02d}<span>{p["cat"]}</span></p><h3>{pname(p["name"])}</h3><p class="col__d">{p["short"]}</p>
<span class="lnk lnk--s"><span>{t("詳しく見る","Details")}</span>{ARR}</span></a></li>'''
    free = ''.join(f'<li>{nobr(a)}</li>' for a, _ in b.FREE_FROM())
    return f'''<section class="sec col" id="collection"><div class="wrap">
{shd("02","Collection","製品ラインナップ","The collection", kj="製品ラインナップ",
     lead=t("無香料・無着色・オイルフリー・アルコールフリー。敏感な肌にもやさしい、日本製のスキンケア。","Fragrance-free, colorant-free, oil-free, alcohol-free. Gentle skincare, made in Japan."), cls="shd--c")}
<ul class="col__l{" col__l--3" if V11() else ""}">{cards}</ul>
{soon_note(enumerate(b.PRODUCTS())) if V11() else ""}<ul class="free rv">{free}</ul>
<div class="ctr ctr--2">{btn("brand.html#lineup","製品一覧を見る","All products")}{cta_btn("product","btn--fill")}</div>
</div></section>'''

def h_why():
    return f'''<section class="sec blush why" id="why"><div class="wrap why__g">
<div class="why__h rv">{shd("03","Why Hanajirushi","ビジネスパートナーに<br>選ばれる理由","Why partners<br><em>choose us</em>", kj="選ばれる理由",
     lead=t("良い商品であることに加えて、花印と取引する理由をお伝えします。","Beyond good products — why companies choose to do business with us."))}
<div class="ctas">{cta_btn("partner","btn--fill")}{cta_lnk("business")}</div></div>
{numbered(b.WHY())}
</div></section>'''

def h_collab():
    return f'''<section class="sec collab"><div class="wrap collab__g">
<div class="collab__txt rv">{shd(hn("collab","04"),"Collaboration","人気IPと、<br>正規ライセンスで。","Beloved Japanese IP,<br><em>officially licensed.</em>", kj="IPコラボレーション")}
<p>{t("日本の人気IPと正規ライセンスを結び、処方からパッケージ、ギフトセットまで一貫して企画・開発しています。","Official licences with leading Japanese IP — with full co-development from formula to packaging and gift sets.")}</p>
<p class="note">{IPNOTE()}</p>
<div class="lnks">{lnk("collaboration.html","コラボレーション一覧","All collaborations")}{cta_lnk("oem")}</div></div>
<ul class="collab__l">{ip_cards()}</ul>
</div></section>'''

def gstats():
    if V13():   # reviewer 2026-10: trade results and partner counts cannot be published
        return f'''<ul class="gstats rv">
<li><small>{t("販売国","Countries")}</small><b>12<u>{t("ヵ国","")}</u></b></li>
<li><small>{t("展開地域","Regions")}</small><b>3<u>{t("地域","")}</u></b></li>
<li><small>{t("創業","Since")}</small><b>2015<u>{t("年","")}</u></b></li></ul>'''
    return f'''<ul class="gstats rv">
<li><small>{t("販売国","Countries")}</small><b>12<u>{t("ヵ国","")}</u></b></li>
<li><small>{t("取引実績","Trade deals")}</small><b class="na">—<u>{t("件","")}</u></b>{tbd()}</li>
<li><small>{t("海外パートナー","Overseas partners")}</small><b class="na">—<u>{t("社","")}</u></b>{tbd()}</li>
<li><small>{t("創業","Since")}</small><b>2015<u>{t("年","")}</u></b></li></ul>'''

def h_partners():
    rg = [(t("東アジア","East Asia"), t("日本・中国を中心にEC・ドラッグストア","Japan &amp; China: e-commerce, drugstores")),
          (t("東南アジア","Southeast Asia"), t("越境EC・モダントレード","Cross-border EC, modern trade")),
          (t("北米","North America"), t("ECを中心に展開","E-commerce led"))]
    steps = t(["フォーム申込","オンライン面談","サンプル評価","契約・初回発注"], ["Apply online","Online meeting","Sample review","Contract &amp; first order"])
    return f'''<section class="sec blush gp" id="partners"><div class="wrap gp__g">
<div class="gp__map rv"><img src="{IMG}world_map_brand.png" alt="{t("販売地域の地図","Map of our markets")}" loading="lazy">
{gstats()}
<ul class="gp__rg">{"".join(f"<li><b>{a}</b>{d}</li>" for a, d in rg)}</ul>
<p class="note">{t("中国では天猫・抖音・屈臣氏（Watsons）等で展開。販売国一覧","In China via Tmall, Douyin and Watsons. Country list")} {tbd()}</p></div>
<div class="gp__txt rv">{shd("05","Partnership","海外代理店・<br>パートナー募集","Become a<br><em>HANAJIRUSHI partner</em>", kj="代理店募集")}
<p class="gp__lead">{t("海外市場での実績をもとに、<em>新しい販売代理店・ビジネスパートナー</em>を募集しています。","Building on our track record overseas, we are now recruiting <em>new distributors and business partners</em>.")}</p>
<p>{t("独占代理店から越境EC、OEM/ODMまで。市場と規模に合わせた協業をご提案します。輸出書類のご用意から各国登録の技術支援まで、お取引に必要なサポートを行います。","From exclusive distribution to cross-border e-commerce and OEM/ODM — a partnership that fits your market. We support you from export documentation to local registration.")}</p>
<ul class="models">{b.MODELS_MINI()}</ul>
<ol class="steps">{"".join(f"<li><i>{i+1:02d}</i>{s}</li>" for i, s in enumerate(steps))}</ol>
<div class="ctas">{cta_btn("partner","btn--fill")}{lnk("partners.html","募集要項を見る","Programme details")}</div></div>
</div></section>'''

def h_news():
    rows = ''.join(f'<li><a href="news.html"><time>{d}</time><span class="cat">{cl}</span><span class="tt">{x}{"<span class=new>New</span>" if new else ""}</span></a></li>' for d, c, cl, cls, x, new in b.NEWS()[:5])
    return f'''<section class="sec news" id="exhibition"><div class="wrap news__g{" news__g--wide" if V12() else ""}">
<div class="rv">{shd(hn("news","06"),"News","お知らせ","News", kj="お知らせ")}
<ul class="nl">{rows}</ul>
<p class="note">{t("※ 記事タイトルはモックアップ用の仮テキストです。","Headlines are placeholder copy for design review.")}</p>
{lnk("news.html","お知らせ一覧","All news")}</div>
{"" if V12() else exh_card(compact=True)}
</div></section>'''

def exh_card(compact=False):
    return f'''<aside class="exh rv">{seal("出展", "seal--txt")}
{eb("Exhibition")}<h3>Cosmoprof Asia 2026</h3><p>{b.EXH_INTRO()}</p>
<dl><div><dt>{t("会期","Dates")}</dt><dd>{t("2026年11月","November 2026")} {tbdw("日程確定待ち","TBC")}</dd></div>
<div><dt>{t("会場","Venue")}</dt><dd>{t("香港コンベンション＆エキシビションセンター","Hong Kong Convention &amp; Exhibition Centre")}</dd></div>
<div><dt>{t("ブース","Booth")}</dt><dd>{tbdw("確定待ち","TBC")}</dd></div></dl>
{btn(lp_href("#booking") if V12() else ("exhibition.html#booking" if compact else "#booking"),"商談を予約する","Book a meeting","btn--light")}</aside>'''

def h_company():
    if V11():
        return h_company11()
    rows = [(t("社名","Company"), t("花印粧業研究所株式会社","Hanajirushi Institute of Cosmetics, Inc.")),
            (t("創業","Founded"), t("2015年1月28日","28 January 2015")),
            (t("本社","Head office"), ADDR(True))]
    return f'''<section class="coband"><div class="coband__bg" aria-hidden="true"><img src="{IMG}h_campany_top_p.jpg" alt="" loading="lazy"></div>
<div class="wrap coband__in"><div class="coband__card rv">{shd("07","Company","銀座から、世界へ。","From Ginza,<br><em>to the world.</em>", kj="会社情報")}
<dl class="dl">{"".join(f"<div><dt>{a}</dt><dd>{v}</dd></div>" for a, v in rows)}</dl>
<div class="ctas">{btn("company.html","会社概要","Company profile")}{lnk("company.html#access","アクセス","Access")}</div></div></div></section>'''

def h_company11():
    """v1.1: plum band with the head-office building in an arch (the street photo is kept
    for the company page header only)."""
    rows = [(t("社名","Company"), t("花印粧業研究所株式会社","Hanajirushi Institute of Cosmetics, Inc.")),
            (t("創業","Founded"), t("2015年1月28日","28 January 2015")),
            (t("本社","Head office"), ADDR(True))]
    return f'''<section class="sec dark cosplit"><div class="wrap split__g">
<div class="split__img rv"><div class="arch"><img src="{IMG}h_campany_bldg.jpg" alt="{t("銀座二丁目の本社ビル","Head office building, Ginza 2-chome")}" loading="lazy"></div></div>
<div class="split__txt rv">{shd(hn("company","07"),"Company","銀座から、世界へ。","From Ginza,<br><em>to the world.</em>", kj="会社情報")}
<dl class="dl">{"".join(f"<div><dt>{a}</dt><dd>{v}</dd></div>" for a, v in rows)}</dl>
<div class="ctas">{btn("company.html","会社概要","Company profile","btn--light")}{lnk("company.html#access","アクセス","Access")}</div></div>
</div></section>'''

# ============================================================ v1.3: products (catalog.py)
def prod_href(pid):
    """A product link: its own page in v1.3, the brand-page anchor before."""
    if V13():
        p = cat.BY_LEGACY().get(pid)
        if p and not p["soon"]:
            return cat.page_of(p)
        return "products.html#" + (p["slug"] if p else "list")
    return f"brand.html#{pid}"

def product_lines():
    """Contact and booking forms: (label, data-items) for the product checkboxes. v1.3 lists the
    catalogue categories; ?item=<slug> (or a legacy pN) ticks the matching box."""
    if V13():
        allp = cat.PRODUCTS13()
        rows = [(v, " ".join([p["slug"] for p in allp if p["cat"] == k] + [p["legacy"] for p in allp if p["cat"] == k and p["legacy"]]))
                for k, v in cat.CATS()]
        return rows + [(b.PRODUCT_LINES()[3], b.ITEM_MAP[3]), (b.PRODUCT_LINES()[4], b.ITEM_MAP[4])]
    return list(zip(b.PRODUCT_LINES(), b.ITEM_MAP))

def pimg(p, cls=""):
    """Product photo in a square panel. Rakuten images are linked, not copied (see catalog.py)."""
    src = cat.photo(p, IMG)
    if not src:
        return f'<figure class="ppan ppan--soon {cls}"><span>{seal()}<small>{t("近日公開","Coming soon")}</small></span></figure>'
    ext = "" if p["img"] else ' data-src="rakuten"'
    return f'<figure class="ppan {cls}"{ext}><img src="{src}" alt="{p["name"]}" loading="lazy"></figure>'

_PC_WORDS = ("クレンジング", "ジューシー", "ハトムギ", "豊潤", "ブースター", "モイスチュア", "フェイス", "薬用",
             "リンクル", "スーパー", "トーンアップ", "UV", "クレー")

def pcname(name):
    """v1.3 card names: 花印 on its own small line; the rest may wrap only between words."""
    if not name.startswith("花印"):
        return name
    rest = name[2:].strip()
    for w in _PC_WORDS:
        rest = rest.replace(w, w + "<wbr>")
    return f'<small class="pcard__b">花印</small>{rest.removesuffix("<wbr>")}'

def pcard(p, i):
    """One product card (products list, home, 'more products')."""
    cats = dict(cat.CATS())
    ser = cat.SERIES().get(p["series"]) if p["series"] else None
    flag = (f'<span class="pcard__new">{t("新商品","New")}</span>' if p["new"] else
            f'<span class="pcard__new pcard__new--soon">{t("近日公開","Coming soon")}</span>' if p["soon"] else '')
    body = (f'{pimg(p)}<p class="pcard__no">No.{i:02d}<span>{cats[p["cat"]]}{"<i> · " + ser + "</i>" if ser else ""}</span>{flag}</p>'
            f'<h3 class="pcard__n">{pcname(p["name"])}</h3><p class="pcard__d">{p["short"]}</p>')
    if p["soon"]:
        return f'<li class="pcard pcard--soon rv" data-cat="{p["cat"]}" id="{p["slug"]}"><div>{body}</div></li>'
    return f'<li class="pcard rv" data-cat="{p["cat"]}"><a href="{cat.page_of(p)}">{body}<span class="pcard__go" aria-hidden="true">{ARR}</span></a></li>'

# ============================================================ v1.3: home
def SLIDES13():
    """The first view: large images that change (reviewer 2026-10: 「第1案のように、大きな画像が
    切り替わるスライド形式」). The client will supply brand and new-product images; until then
    the existing site photographs stand in. Order: brand, exhibition, new product, patent."""
    by = cat.BY_SLUG()
    return [
     dict(kind="brand", tab=t("花印について", "Hanajirushi"), k=None, eyebrow="Hanajirushi · Ginza, Tokyo",
          head=t("ひとりに、ひとつの、<br>キレイを咲かせる。", "Clean formula.<br><em>Gentle by design.</em><br>Made in Japan."),
          text=t("東京・銀座の自社研究室で開発する、<br>無香料・無着色の日本製スキンケア。", "Skincare formulated in our own laboratory in Ginza, Tokyo — sold in Japan and 12 countries."),
          bg="h_hanajirushi_top-1.jpg", pos="70% center", vis=None,
          ctas=[("products.html", ("製品を見る", "View products"), "fill"), ("brand.html", ("ブランドについて", "About the brand"), "lnk")]),
     dict(kind="exh", tab=t("展示会", "Exhibition"), k=t("展示会", "Exhibition"),
          head=t('<span class="nw"><span class="lat">Cosmoprof Asia 2026</span>に</span><br><em>出展します。</em>', "Meet us at<br><em>Cosmoprof Asia 2026</em>"),
          text=t("2026年11月、香港コンベンション＆エキシビションセンター。ブースでの商談のご予約を受け付けています。", "November 2026, Hong Kong Convention &amp; Exhibition Centre. Meetings at our booth can be booked now."),
          tbc=t("日程確定待ち", "Dates TBC"), bg="h_campany_top_p.jpg", pos="center 40%", vis=("kanji", "出展", "Hong Kong 2026"),
          ctas=[(lp_href(), ("展示会専用ページへ", "Open the event page"), "fill")]),
     dict(kind="new", tab=t("ハトムギシリーズ", "Hatomugi series"), k=t("新商品", "New"),
          head=t("ハトムギシリーズに、<br><em>美容液とクリーム。</em>", "The Hatomugi series<br><em>adds a serum and a cream.</em>"),
          text=t("ハトムギ化粧水と一緒に使える、ハトムギ豊潤美容液（200mL）とハトムギクリーム（100g）。", "Hatomugi Rich Essence (200mL) and Hatomugi Cream (100g), made to go with the Hatomugi lotion."),
          bg=None, vis=("panels", [by["hatomugi-skin-conditioner"], by["hatomugi-essence"], by["hatomugi-cream"]]),
          ctas=[(cat.page_of(by["hatomugi-essence"]), ("美容液を見る", "See the essence"), "fill"), (cat.page_of(by["hatomugi-cream"]), ("クリームを見る", "See the cream"), "lnk")]),
     dict(kind="patent", tab=t("特許", "Patent"), k=t("特許", "Patent"),
          head=t("特許技術を採用した、<br><em>クレンジングローション。</em>", "A cleansing lotion<br><em>with patented technology.</em>"),
          text=t("うるおい残してしっかり落ちる、拭き取りタイプのクレンジングローション。", "A wipe-off cleansing lotion that removes make-up and leaves moisture behind."),
          tbc=t("特許番号 要確認", "Patent no. TBC"), bg="h_brand_top_p.jpg", pos="center", vis=("win", by["cleansing-lotion-ma"]),
          ctas=[(cat.page_of(by["cleansing-lotion-ma"]), ("製品を見る", "View the product"), "fill")]),
    ]

def hero13():
    sl = SLIDES13()
    n = len(sl)
    out = ''
    for i, s in enumerate(sl):
        on = i == 0
        tag = "h1" if on else "h2"
        bg = (f'<div class="hs13__bg" aria-hidden="true"><img src="{IMG}{s["bg"]}" alt="" style="object-position:{s.get("pos", "center")}"></div>'
              if s["bg"] else '<div class="hs13__bg hs13__bg--plain" aria-hidden="true"></div>')
        k = f'<p class="hs__k">{s["k"]}</p>' if s["k"] else eb(s["eyebrow"])
        chip = tbd(s["tbc"], s["tbc"]) if s.get("tbc") else ""
        ctas = ''.join(btn(h, lab[0], lab[1], "btn--fill") if kind == "fill" else lnk(h, lab[0], lab[1])
                       for h, lab, kind in (s["ctas"][:1] if V14() else s["ctas"]))   # v1.4: one button per slide
        v = s["vis"]
        vis = ''
        if v and v[0] == "kanji":
            kj, cap = ("Hong Kong", v[2].replace("Hong Kong ", "")) if EN15() else (v[1], v[2])
            vis = f'<figure class="win win--xl win--kj"><div class="win__c"><span class="win__kj{" win__kj--en" if EN15() else ""}">{kj}</span><small>{cap}</small></div></figure>'
        elif v and v[0] == "win":
            vis = win(v[1]["img"], v[1]["name"], "win--xl") + seal("特許", "seal--l seal--txt")
        elif v and v[0] == "panels":
            vis = '<ul class="hs13__panels">' + ''.join(f'<li>{pimg(p)}<p>{p["name"]}<small>{p["size"]}</small></p></li>' for p in v[1]) + '</ul>'
        vis = f'<div class="hs13__vis">{vis}</div>' if vis else ''
        hide = '' if on else ' aria-hidden="true"'
        out += f'''
<div class="hs__s hs13 hs13--{s["kind"]}{" is-on" if on else ""}" role="group" aria-roledescription="slide" aria-label="{i + 1} / {n}"{hide}>{bg}
<div class="wrap hs13__in"><div class="hs__txt">{k}<{tag} class="hs__h">{lines(s["head"])}</{tag}>
<p class="hero__lead">{s["text"]}{chip}</p><div class="hero__ctas">{ctas}</div></div>{vis}</div></div>'''
    tabs = ''.join(f'<li><button type="button" data-go="{i}"{" aria-current=true" if i == 0 else ""}><span>{s["tab"]}</span><i></i></button></li>' for i, s in enumerate(sl))
    return f'''<section class="hero hero--slides hero13" data-first aria-roledescription="carousel" aria-label="{t("メインビジュアル","Highlights")}">
<div class="hs"><div class="hs__track">{out}</div></div>
<div class="hs__ui"><p class="hs__n"><b>01</b><span>/ {n:02d}</span></p>
<ol class="hs__tabs">{tabs}</ol>
<div class="hs__btns"><button type="button" class="hs__play" aria-label="{t("一時停止","Pause")}" data-pause="{t("一時停止","Pause")}" data-play="{t("再生","Play")}"><i></i></button></div></div>
</section>'''

def h_numbers13():
    rs = b.REASONS()
    li = ''.join(f'<li class="rv"><small>{rs[i][0]}</small><b class="{"num" if rs[i][1][:1].isdigit() else "word"}">{rs[i][1]}</b><p>{rs[i][3]}</p></li>' for i in (0, 1, 2, 4))
    return f'<section class="nums nums--4"><div class="wrap"><ul class="nums__l">{li}</ul></div></section>'

def h_products13():
    """Home: the products at the front (reviewer 2026-10: the home page is mainly for consumers)."""
    by = cat.BY_SLUG()
    cards = ''.join(pcard(by[s], i + 1) for i, s in enumerate(cat.FEATURED))   # numbered by position in the list
    chips = ''.join(f'<a href="products.html?cat={k}#list">{v}</a>' for k, v in cat.CATS())
    free = ''.join(f'<li>{nobr(a)}</li>' for a, _ in b.FREE_FROM())
    return f'''<section class="sec col13" id="collection"><div class="wrap">
<div class="col13__h">{shd(hn("products","02"),"Our skincare","花印のスキンケア","Our skincare", kj="製品",
     lead=t("クレンジングから保湿、UVケアまで。毎日の肌に寄り添う、日本製のスキンケアです。","From cleansing to moisturising and UV care — Japanese skincare for every day."))}
{btn("products.html","すべての製品を見る","All products")}</div>
<nav class="col13__cats rv" aria-label="{t("カテゴリー","Categories")}">{chips}</nav>
<ul class="pgrid">{cards}</ul>
{"" if V14() else f'<ul class="free rv">{free}</ul>'}
</div></section>'''

def h_brand13():
    p1, p2 = b.BRAND_TEXT()
    return f'''<section class="sec blush br13" id="brand"><div class="wrap br13__g">
<div class="br13__mark rv">{seal(cls="seal--xl")}<p class="br13__tate" aria-hidden="true">ひとりに、ひとつの、<br>キレイを咲かせる。</p>{slogan_en("slogan-en--mark")}</div>
<div class="br13__txt rv">{shd(hn("brand","03"),"Brand","肌に咲く、<br>花の印。","Hana-jirushi —<br><em>a flower's seal.</em>", kj="ブランド")}
<p>{p1}</p><p>{p2}</p>
<div class="ctas">{btn("brand.html","ブランドについて","About the brand","btn--fill")}{lnk("rd.html","研究開発・品質管理","R&amp;D and quality")}</div></div>
</div>{f'<div class="wrap">{brand_film()}</div>' if V15() else ""}</section>'''

def h_partners13():
    """Home partnership, kept short and without figures that cannot be published yet
    (reviewer 2026-10: 取引実績や海外パートナー数などの具体的な数値を公開しにくい)."""
    chans = ''.join(f'<li><i>{i+1:02d}</i>{m[0]}</li>' for i, m in enumerate(b.MODES()[:4]))
    return f'''<section class="sec gp13" id="partners"><div class="wrap gp13__g">
<div class="rv">{shd(hn("partners","06"),"Partnership","海外のパートナーの<br>皆さまへ","For partners<br><em>around the world</em>", kj="パートナーシップ")}
<p class="gp13__lead">{t("日本ならではの上質で誠実なものづくりを、世界のお客様へ。それぞれの市場をよく知るパートナーの皆さまと、花印の新しい可能性を育てていきます。","Japanese quality and honest manufacturing, for customers around the world. We grow Hanajirushi together with partners who know their markets.")}</p>
<div class="ctas">{btn("partners.html","パートナーシップについて","Partnership programme","btn--fill")}{cta_lnk("partner")}</div></div>
<div class="gp13__fig rv"><img src="{IMG}{MAP()}" alt="{t("販売地域の地図","Map of our markets")}" loading="lazy">
<p class="gp13__big"><b>12</b><span>{t("ヵ国で販売","countries")}</span></p>
<ol class="gp13__ch">{chans}</ol></div>
</div></section>'''

def p_home():
    if V13():
        body = hero13() + h_numbers13() + h_news() + h_products13() + h_brand13() + h_japan4() + h_collab() + h_partners13() + h_company() + store_section()
        return page("index.html", "home", "", t("花印（HANAJIRUSHI）の公式サイト。東京・銀座の自社研究室で開発する日本製スキンケア。クレンジング、ハトムギ化粧水、美容液、クリーム、UV化粧下地など。",
                                                 "HANAJIRUSHI: Japanese skincare formulated in our own laboratory in Ginza, Tokyo — cleansing, Hatomugi lotion, serums, creams and UV primer."), body)
    body = h_hero() + h_numbers() + h_japan4() + h_collection() + h_why() + h_collab() + h_partners() + h_news() + h_company() + store_section()
    return page("index.html", "home", "", t("花印粧業研究所株式会社の公式サイト。東京・銀座の自社研究室で開発する、無香料・無着色の日本製スキンケア。世界12ヵ国で販売。海外代理店・パートナー募集中。",
                                             "HANAJIRUSHI: clean, gentle Japanese skincare formulated in our own laboratory in Ginza, Tokyo. Sold in 12 countries. Distributor enquiries welcome."), body)

# ============================================================ BRAND
def brand_phil():
    p1, p2 = b.BRAND_TEXT()
    # EN_ONLY: brand line is re-written for English, not translated; the Japanese slogan stays as a vertical accent.
    slogan = t(f'<h2 class="phil__tate">{lines("ひとりに、ひとつの、<br>キレイを咲かせる。")}</h2>',
               f'<h2 class="phil__h">{lines("Clean formula.<br><em>Gentle by design.</em><br>Made in Japan.")}</h2><p class="phil__jp" aria-hidden="true">ひとりに、ひとつの、キレイを咲かせる。</p>{slogan_en()}')
    return f'''<section class="sec phil" id="philosophy"><div class="wrap phil__g">
<div class="phil__s rv">{eb("Philosophy","01")}{slogan}</div>
<div class="phil__txt rv"><p class="phil__lead">{p1}</p><p>{p2}</p>
<div class="name">{seal(cls="seal--l")}<p><b>{t("花印 — 肌に咲く、花の印。","Hana-jirushi — “flower seal”.")}</b>{t("ひとりひとりの肌に咲く花の印という想いを、名前に込めています。","The mark of a flower blooming on each person's skin.")}</p></div></div>
<div class="phil__img rv"><div class="arch"><img src="{IMG}{"h_brand_top_p.jpg" if V13() else "h_hanajirushi_top-1.jpg"}" alt="" loading="lazy"{' style="object-position:0% center"' if V13() else ""}></div></div>
</div>
<div class="wrap"><ul class="rings rv">{"".join(f"<li><span>{a}</span><small>{s}</small></li>" for a, s in b.FREE_FROM())}</ul></div>
</section>'''

def brand_collab(num="03", idattr=""):
    return f'''<section class="sec blush collab collab--row"{idattr}><div class="wrap">
{shd(num,"Collaboration","IPコラボレーション商品","Licensed IP collaborations", kj="IPコラボレーション", cls="shd--c")}
<ul class="collab__l collab__l--4">{ip_cards()}</ul>
<div class="ctr ctr--2">{lnk("collaboration.html","コラボレーションについて","About our collaborations")}{cta_lnk("oem")}</div></div></section>'''

def VALUES14():
    """OUR VALUES (client text, change proposal 2026-10-07): in place of the five free-from circles.
    (number, English word, Japanese title, English title, Japanese text, English text)"""
    return [
     ("INDIVIDUALITY", "一人ひとりを尊重する", "Respect for each person",
      "肌も悩みも、美しさのかたちも人それぞれ。画一的な美しさを押しつけず、一人ひとりに合った選択肢を考えます。",
      "Skin, concerns and ideas of beauty differ from person to person. We never impose one standard of beauty, and think about the choice that suits each individual."),
     ("INTEGRITY", "誠実であること", "Honesty",
      "商品の品質、原料、使用方法、情報発信に誠実に向き合い、お客様との信頼関係を大切にします。",
      "We are honest about quality, ingredients, how our products are used and what we say about them, and we value our customers' trust."),
     ("QUALITY", "品質を追求する", "The pursuit of quality",
      "原料選定、処方設計、製造、品質管理の各段階で改善を重ね、日々のケアにふさわしい品質を追求します。",
      "We keep improving every stage — ingredients, formulation, manufacturing and quality control — for a quality worthy of daily care."),
     ("ACCESSIBILITY", "美しさを身近に", "Beauty within reach",
      "品質と価格のバランスを大切にし、毎日のスキンケアを無理なく続けられる選択肢を届けます。",
      "We balance quality and price, offering choices that make daily skincare easy to keep up."),
     ("GROWTH", "ともに成長する", "Growing together",
      "お客様の声に耳を傾け、時代や生活の変化に合わせて商品とサービスを進化させます。国や文化の違いも理解し、世界の人々に寄り添います。",
      "We listen to our customers and evolve our products and services as times and lifestyles change — understanding different countries and cultures, and staying close to people around the world."),
    ]

def STORY14():
    """BRAND STORY (client text): label, headline, text — Japanese, then our English draft."""
    return [
     (t("花印が大切にしている想い", "What we care about"), t("一人ひとりの美しさに、寄り添う。", "Close to every person's beauty."),
      t("肌質も、年齢も、理想の美しさも、人それぞれ。花印は、一人ひとりの肌に向き合い、毎日のスキンケアを通じて、自分らしい美しさを育むことを大切にしています。",
        "Skin type, age and the beauty people hope for all differ. Hanajirushi meets each person's skin and helps them nurture a beauty of their own through everyday skincare.")),
     (t("花印のものづくり", "How we make our products"), t("毎日の肌に、確かな品質と心地よさを。", "Reliable quality and comfort, every day."),
      t("原料選びから処方、使い心地まで。毎日無理なく続けられる、身近で心地よいスキンケアを目指して、商品づくりに取り組んでいます。",
        "From the choice of ingredients to the formula and the feel on the skin, we make skincare that is easy to live with and pleasant to use every day.")),
     (t("銀座から、世界へ", "From Ginza to the world"), t("日本の美しさを、世界の一人ひとりへ。", "Japanese beauty, for every person worldwide."),
      t("銀座を起点に、日本で培ってきたスキンケアへの想いを世界へ。国や文化を越えて、一人ひとりの「キレイ」に寄り添うブランドを目指します。",
        "From Ginza, we take the care for skin we have built in Japan to the world — a brand that stays close to every person's beauty, across countries and cultures.")),
    ]

def p_brand14():
    """v1.4 brand page: the client's text (ブランドページ文字案, change proposal 2026-10-07) —
    header, brand concept, OUR VALUES in place of the free-from circles, brand story in place of
    the placeholders, research. The IP collaborations block moved to the products page."""
    A = b.A
    hd = phero("Brand", "ブランド", "Brand",
               t("一人ひとりの肌に寄り添い、その人らしい美しさを育む。<br>花印は、毎日のスキンケアを通じて、一人ひとりが自分らしい美しさを楽しめる毎日を届けるブランドです。",
                 "Close to every skin, nurturing a beauty that is truly one's own. Through everyday skincare, Hanajirushi helps each person enjoy a beauty of their own, every day."),
               "h_brand_top_p.jpg", "花印",
               [A("concept","ブランドコンセプト","Concept"),A("values","5つの価値観","Our values"),A("story","ブランドストーリー","Our story"),A("research","研究への取り組み","Research"),("products.html",t("製品一覧","All products"))])
    # EN_ONLY: the English slogan is re-written, not translated; the Japanese line stays as an accent
    slogan = t(f'<h2 class="phil__tate">{lines("ひとりに、ひとつの、<br>キレイを咲かせる。")}</h2>',
               f'<h2 class="phil__h">{lines("Clean formula.<br><em>Gentle by design.</em><br>Made in Japan.")}</h2><p class="phil__jp" aria-hidden="true">ひとりに、ひとつの、キレイを咲かせる。</p>{slogan_en()}')
    concept = f'''<section class="sec phil" id="concept"><div class="wrap phil__g">
<div class="phil__s rv">{eb("Brand concept","01")}{slogan}</div>
<div class="phil__txt rv"><p class="phil__lead">{t("美しさのかたちは、人それぞれ。","Beauty takes as many forms as there are people.")}</p>
<p>{t("肌質も、年齢も、ライフスタイルも、理想とする美しさも、一人ひとり違います。だから花印は、誰かの美しさをそのまま当てはめるのではなく、一人ひとりの肌と向き合い、その人に合った美しさを育むことを大切にしています。",
     "Skin type, age, lifestyle, the beauty you hope for — no two people are alike. So rather than fitting anyone to someone else's idea of beauty, Hanajirushi starts from each person's skin and helps the beauty that suits them grow.")}</p>
<p>{t("毎日使うものだからこそ、品質にこだわり、使いやすく、無理なく続けられること。特別な日のためだけではなく、何気ない毎日の中で、自分の肌を大切にする時間を届けること。それが、花印が考えるスキンケアです。",
     "Because it is something you use every day, it should be well made, easy to use and easy to keep up — not only for special days, but as everyday time to look after your skin. That is what skincare means to Hanajirushi.")}</p></div>
<div class="phil__img rv"><div class="arch"><img src="{IMG}h_brand_top_p.jpg" alt="" loading="lazy" style="object-position:0% center"></div></div>
</div></section>'''
    vals = ''.join(f'<li class="rv"><span class="vals__n">{i+1:02d}</span><span class="vals__w">{w}</span><h3>{t(ja, en)}</h3><p>{t(dja, den)}</p></li>'
                   for i, (w, ja, en, dja, den) in enumerate(VALUES14()))
    values = f'''<section class="sec sec--t vals-sec" id="values"><div class="wrap">
{shd("02","Our values","花印が大切にする、<br>5つの価値観。","Five values<br><em>we hold to</em>", kj="5つの価値観", cls="shd--c")}
<ol class="vals">{vals}</ol></div></section>'''
    items = ''.join(f'<li class="rv"><span class="story13__n">{i+1:02d}</span><p class="story13__k">{k}</p><h3>{h}</h3><p>{x}</p></li>'
                    for i, (k, h, x) in enumerate(STORY14()))
    story = f'''<section class="sec sec--t blush" id="story"><div class="wrap">
{shd("03","Brand story","美しさは、<br>一人ひとり違う。","Every beauty<br><em>is different.</em>", kj="ブランドストーリー", cls="shd--c",
     lead=t("だからこそ、私たちは一人ひとりの肌と向き合い、その人らしい美しさを育むスキンケアを届けたい。それが、花印のものづくりの原点です。",
            "That is why we want to offer skincare that meets each person's skin and nurtures a beauty of their own — the starting point of everything Hanajirushi makes."))}
<ol class="story13 story13--full">{items}</ol></div></section>'''
    research = f'''<section class="sec" id="research"><div class="wrap split__g">
<div class="split__img split__img--win rv">{win("h_campany_lab.jpg", t("銀座本社の研究室","Our laboratory in Ginza"), "win--m")}</div>
<div class="split__txt rv">{shd("04","Research","銀座の研究室から、<br>確かな処方を。","Reliable formulas<br><em>from our Ginza lab.</em>", kj="研究への取り組み")}
<p class="pd__cp">{b.RD_CATCH()}</p><p>{b.RD_P1()}</p>
<div class="ctas">{btn("rd.html","研究開発・品質管理","R&amp;D and quality")}{lnk("products.html","製品一覧","All products")}</div></div></div></section>'''
    return page("brand.html", "brand", t("ブランド","Brand"),
                t("花印のブランドコンセプト、5つの価値観、ブランドストーリー。ひとりに、ひとつの、キレイを咲かせる。東京・銀座の日本製スキンケア。",
                  "The HANAJIRUSHI brand: our concept, our five values and our story — Japanese skincare from Ginza, Tokyo."),
                hd + concept + values + story + research + store_section())


def p_brand13():
    """v1.3: the brand page on its own (products moved to products.html). The fuller brand text
    arrives from the client on 2026-10-05; its place is held below."""
    A = b.A
    hd = phero("Brand", "ブランド", "Brand",
               t("人の肌を想い、ひとりの悩みを見つめる、日本製のスキンケア。","Gentle, honest skincare — formulated and made in Japan."),
               "h_brand_top_p.jpg", "花印",
               [A("philosophy","ブランド理念","Philosophy"),A("story","ブランドストーリー","Our story"),A("research","研究への取り組み","Research"),A("collab","IPコラボレーション","Collaborations"),("products.html",t("製品一覧","All products"))])
    slots = [(t("ブランドの背景","Background"), t("花印が生まれた背景と、名前に込めた想い。","How Hanajirushi began, and what the name stands for.")),
             (t("大切にしていること","What we value"), t("肌へのやさしさと、日本ならではのものづくり。","Gentleness, and Japanese craftsmanship.")),
             (t("花印の魅力","What sets us apart"), t("製品づくりへのこだわりと、お客様に選ばれている理由。","How we make our products, and why customers choose them."))]
    due = tbd("原稿受領後に掲載（10月5日予定）", "Text due 5 Oct")
    story = f'''<section class="sec sec--t blush" id="story"><div class="wrap">
{shd("02","Our story","ブランドストーリー","Our story", kj="ブランドストーリー", cls="shd--c",
     lead=t("ブランドの背景や魅力をお伝えする本文は、ご提供いただく原稿を掲載します。","The full brand story will be added from the text being supplied."))}
<ol class="story13">{"".join(f'<li class="rv"><span class="story13__n">{i+1:02d}</span><h3>{h}</h3><p>{d}</p>{due}</li>' for i, (h, d) in enumerate(slots))}</ol></div></section>'''
    research = f'''<section class="sec" id="research"><div class="wrap split__g">
<div class="split__img split__img--win rv">{win("h_campany_lab.jpg", t("銀座本社の研究室","Our laboratory in Ginza"), "win--m")}</div>
<div class="split__txt rv">{shd("03","Research","銀座の研究室から、<br>確かな処方を。","Reliable formulas<br><em>from our Ginza lab.</em>", kj="研究への取り組み")}
<p class="pd__cp">{b.RD_CATCH()}</p><p>{b.RD_P1()}</p>
<div class="ctas">{btn("rd.html","研究開発・品質管理","R&amp;D and quality")}{lnk("products.html","製品一覧","All products")}</div></div></div></section>'''
    if V14():
        return p_brand14()
    return page("brand.html", "brand", t("ブランド","Brand"),
                t("花印のブランド理念とブランドストーリー。ひとりに、ひとつの、キレイを咲かせる。東京・銀座の自社研究室で開発する日本製スキンケア。",
                  "The HANAJIRUSHI brand: our philosophy and story, research in our own Ginza laboratory, and licensed IP collaborations."),
                hd + brand_phil() + story + research + brand_collab("04", ' id="collab"') + store_section())

def p_products13():
    """v1.3: every product on one list page, filtered by category; each card opens its own page.
    Built to grow: a new product is one more entry in catalog.PRODUCTS13()."""
    allp = cat.PRODUCTS13()
    hd = phero("Products", "製品", "Products",
               t("クレンジングから保湿、UVケアまで。毎日の肌に寄り添う、日本製のスキンケア。","From cleansing to moisturising and UV care — Japanese skincare for every day."),
               None, "製品", [])
    counts = {k: sum(1 for p in allp if p["cat"] == k) for k, _ in cat.CATS()}
    tabs = (f'<button type="button" data-cat="all" class="on">{t("すべて","All")}<small>{len(allp)}</small></button>' +
            ''.join(f'<button type="button" data-cat="{k}">{v}<small>{counts[k]}</small></button>' for k, v in cat.CATS()))
    cards = ''.join(pcard(p, i + 1) for i, p in enumerate(allp))
    note = t("※ 製品画像の一部は、楽天市場 花印公式ショップの商品画像を仮に表示しています。正式な製品写真に差し替えます。",
             "Some product images are temporary, taken from our Japanese online store, and will be replaced with final photography.")
    trade = f'<p class="note">Trade specifications (INCI, shelf life, JAN codes, case packs) and price lists are available on request. {cta_lnk("product","lnk--s")}</p>' if EN() else ''
    free = ''.join(f'<li>{nobr(a)}</li>' for a, _ in b.FREE_FROM())
    body = f'''<section class="sec sec--t plist13" id="list"><div class="wrap">
<div class="pfilter rv" role="group" aria-label="{t("カテゴリーで絞り込む","Filter by category")}">{tabs}</div>
<ul class="pgrid pgrid--all">{cards}</ul>
<p class="note">{note}</p>{trade}
{"" if V14() else f'<ul class="free rv">{free}</ul>'}
{"" if V14() else f'<p class="plist13__ip rv">{t("人気IPとの正規ライセンス商品は","Officially licensed collaborations with popular characters: ")}{lnk("collaboration.html","IPコラボレーション商品へ","See IP collaborations")}</p>'}
</div></section>'''
    if V14():   # the IP collaborations block moves here from the brand page (change proposal)
        body += brand_collab("01", ' id="collab"')
    return page("products.html", "products", t("製品","Products"),
                t("花印の製品一覧。クレンジング、化粧水・美容液、クリーム・ジェル、マスク・パック、UV化粧下地、メンズ。日本製のスキンケア。",
                  "HANAJIRUSHI products: cleansing, lotions and serums, creams and gels, masks, UV primer and men's care. Made in Japan."),
                hd + body + store_section())

def p_product13(p):
    """v1.3: one page per product, in the order of the V1 demo's product page (reviewer 2026-10):
    product and buttons, features, how to use, research, details (accordion), more products."""
    allp = cat.PRODUCTS13()
    cats = dict(cat.CATS())
    ser = cat.SERIES().get(p["series"]) if p["series"] else None
    fn = cat.page_of(p)
    badges = ''.join(f'<li>{x}</li>' for x in p["badges"])
    free = ''.join(f'<li>{x}</li>' for x in p["free"])
    ask = cta_btn("product", "" if not EN() else "btn--fill", p["slug"], ("この製品について相談する", "Ask about this product"))
    buy = f'<a class="btn btn--fill" href="{cat.RAKUTEN}{p["rk"]}/" target="_blank" rel="noopener"><span>楽天市場で購入する</span>{ARR}</a>'
    if V14():   # change proposal: one 「この製品を購入する」 button opening a choice of stores
        buy = f'<button class="btn btn--fill" type="button" data-buy aria-haspopup="dialog" aria-controls="buy"><span>この製品を購入する</span>{ARR}</button>'
    ctas = t(buy + ask, ask + btn("partners.html", "", "Become a distributor"))   # EN_ONLY: no consumer store link
    crumb = (f'<nav class="crumb crumb--pdx" aria-label="breadcrumb"><div class="wrap"><a href="index.html">{t("ホーム","Home")}</a>'
             f'<a href="products.html">{t("製品","Products")}</a><a href="products.html?cat={p["cat"]}#list">{cats[p["cat"]]}</a><span>{p["name"]}</span></div></nav>')
    top = f'''<section class="pdx"><div class="wrap pdx__g">
<div class="pdx__vis rv">{pimg(p, "ppan--l")}<p class="pdx__lbl">Hanajirushi / {cats[p["cat"]]}</p><p class="pdx__size">{p["size"]}</p></div>
<div class="pdx__info rv">{eb(cats[p["cat"]] + (" · " + ser if ser else ""))}
<h1 class="pdx__n">{pname(p["name"])}</h1><p class="pdx__sub">{p["sub"]}</p>
<ul class="pdx__badges">{badges}</ul>
<p class="pdx__d">{p["desc"]}</p>
{f'<ul class="pdx__free">{free}</ul>' if free else ''}
<p class="pdx__spec"><b>{p["size"]}</b><span>{p["kind"]}</span><span>{t("日本製","Made in Japan")}</span></p>
<div class="ctas">{ctas}</div>
<p class="pdx__trade">{lnk("partners.html","販売代理店・輸入商・小売企業の皆さまへ","For distributors, importers and retailers","lnk--s")}</p></div>
</div></section>
<nav class="anc anc--pdx" aria-label="{t("ページ内リンク","On this page")}"><div class="wrap"><a href="#features">{t("製品の特長","Features")}</a><a href="#usage">{t("使い方","How to use")}</a><a href="#details">{t("製品情報","Details")}</a><a class="anc__pg" href="{topic_href("product", p["slug"])}">{t("お問い合わせ","Enquire")}</a></div></nav>'''
    pts = ''.join(f'<li class="rv"><span class="pdf__n">{k+1:02d}</span><h3>{h}</h3><p>{d}{(" " + tbd("特許番号 要確認","Patent no. TBC")) if flag == "patent" else ""}</p></li>'
                  for k, (h, d, flag) in enumerate(p["points"]))
    feat = f'''<section class="sec pdf" id="features"><div class="wrap">
<div class="shd shd--c">{eb("Features","01")}<h2 class="h2">{lines(p["catch"])}</h2></div>
<ol class="pdf__l">{pts}</ol></div></section>'''
    use = p["usage"] or tbd("使用方法 要確認", "How to use: TBC")
    usage = f'''<section class="sec sec--t blush" id="usage"><div class="wrap pdu__g">
<div class="rv">{shd("02","How to use","使い方","How to use", kj="使い方")}</div><p class="pdu__t rv">{use}</p></div></section>'''
    research = f'''<section class="sec sec--t"><div class="wrap split__g">
<div class="split__img split__img--win rv">{win("h_campany_lab.jpg", t("銀座本社の研究室","Our laboratory in Ginza"), "win--m")}</div>
<div class="split__txt rv">{shd("03","Research","銀座の研究室から、<br>確かな処方を。","Reliable formulas<br><em>from our Ginza lab.</em>", kj="研究への取り組み")}<p>{b.RD_P1()}</p>
<div class="ctas">{lnk("rd.html","研究開発・品質管理","R&amp;D and quality")}</div></div></div></section>'''
    info = [(t("製品名","Product"), p["name"]), (t("内容量","Size"), p["size"]), (t("区分","Category"), p["kind"]), (t("原産国","Made in"), t("日本","Japan"))] + cat.TBC(p)
    if V14():   # change proposal: no 区分, 使用期限, 入数・ケースサイズ or 製造販売元 rows
        tbc = cat.TBC(p)
        info = [(t("製品名","Product"), p["name"]), (t("内容量","Size"), p["size"]), (t("原産国","Made in"), t("日本","Japan")), tbc[0], tbc[2]]
    dl = ''.join(f'<div><dt>{a}</dt><dd>{v}</dd></div>' for a, v in info)
    inci = p["inci"] if not EN() else (f'{tbd("英文表記 要確認", "English INCI list TBC")}<span class="pdd__ja" lang="ja">{p["inci"]}</span>')
    docs = ''.join(f'<li>{a}</li>' for a, d in b.EXPORT_DOCS())
    acc = [(t("製品情報","Product information"), f'<dl class="dl">{dl}</dl>', True),
           (t("全成分","Ingredients"), f'<p class="pdd__inci">{inci}</p>', False),
           (t("使用上の注意","Cautions"), f'<p>{t("パッケージ記載の使用上の注意を掲載します。","The cautions printed on the pack will be listed here.")} {tbd()}</p>', False),
           (t("輸出関連資料（お取引先向け）","Export documents (for trade partners)"), f'<ul class="tags tags--ink">{docs}</ul><p class="note">{t("製品ごとにご用意します。","Prepared for each product.")} {tbd()}</p>', False)]
    det = ''.join(f'<details class="pdd__i"{" open" if o else ""}><summary><span>{h}</span></summary><div class="pdd__b">{c}</div></details>' for h, c, o in acc)
    details = f'''<section class="sec sec--t blush" id="details"><div class="wrap prof__g">
<div>{shd("04","Product details","製品情報","Product details", kj="製品情報")}</div>
<div class="pdd rv">{det}</div></div></section>'''
    others = [x for x in allp if x["slug"] != p["slug"] and not x["soon"]]
    more_l = ([x for x in others if x["cat"] == p["cat"]] + [x for x in others if x["cat"] != p["cat"] and x["slug"] in cat.FEATURED])[:3]
    more = f'''<section class="sec sec--t" id="more"><div class="wrap">
<div class="col13__h">{shd("05","More","その他の製品","More products", kj="その他の製品")}{lnk("products.html","製品一覧へ","All products")}</div>
<ul class="pgrid">{"".join(pcard(x, k + 1) for k, x in enumerate(more_l))}</ul></div></section>'''
    dlg = buy_dialog(p) if (V14() and not EN()) else ''
    return page(fn, "product", p["name"], f'{p["name"]}（{p["size"]}）｜{p["short"]}' if not EN() else f'{p["name"]} ({p["size"]}) — {p["short"]}',
                crumb + top + feat + usage + research + details + more + dlg)

def buy_dialog(p):
    """v1.4: the store chooser behind 「この製品を購入する」 (premium-v14.js opens it). Rakuten opens
    this product's page; the other stores' addresses are still to come from the client."""
    rk = f'{cat.RAKUTEN}{p["rk"]}/'
    stores = [("rakuten.svg", "楽天市場", "花印 公式ショップ", rk), ("amazon.png", "Amazon", "公式ストア", None),
              ("yahoo.svg", "Yahoo!ショッピング", "公式ストア", None), ("qoo10.png", "Qoo10", "公式ショップ", None)]
    li = ''.join((f'<li><a href="{u}" target="_blank" rel="noopener">' if u else '<li><a href="#" aria-disabled="true">')
                 + f'<img src="{IMG}{im}" alt=""><b>{n}</b><small>{x}</small>{"" if u else tbd("URL 要確認","URL TBC")}</a></li>'
                 for im, n, x, u in stores)
    return f'''
<dialog class="buy" id="buy" aria-labelledby="buy-h"><div class="buy__in">
{eb("Online store")}<h2 id="buy-h">購入するストアを選ぶ</h2><p class="buy__p">{p["name"]}（{p["size"]}）</p>
<ul class="buy__l">{li}</ul>
<button class="buy__x" type="button" data-close aria-label="閉じる">×</button></div></dialog>'''

def p_brand():
    if V13():
        return p_brand13()
    A = b.A
    hd = phero("Brand", "ブランド・製品", "Brand &amp; Products",
               t("人の肌を想い、ひとりの悩みを見つめる、日本製のスキンケア。","Gentle, honest skincare — formulated and made in Japan."),
               "h_brand_top_p.jpg", "花印",
               [A("philosophy","ブランド理念","Philosophy"),A("lineup","製品ラインナップ","Line-up"),A("p1","クレンジング","Cleansing"),A("p2","フェイスマスク","Face Mask"),A("p3","ハトムギ化粧水","Hatomugi"),A("stores","国内でのご購入","Where to buy"),("collaboration.html",t("IPコラボレーション","IP collaborations"))])
    phil = brand_phil()
    idx = ''.join(f'<li><a href="#{p["id"]}"><i>No.{i+1:02d}</i><b>{pname(p["name"])}</b><small>{p["cat"]}</small></a></li>' for i, p in enumerate(b.PRODUCTS()))
    lineup = f'''<section class="sec sec--t blush" id="lineup"><div class="wrap">
{shd("02","Line-up","製品ラインナップ","The line-up", kj="製品ラインナップ", cls="shd--c",
     lead=t("お取引に必要な仕様情報（全成分・使用期限・JANコード・入数）は各製品欄に掲載します。","Trade specifications — INCI, shelf life, JAN codes and case packs — are listed for each product."))}
<ol class="pidx rv">{idx}</ol></div></section>'''
    common = [(t("全成分（INCI）","Full INCI list"), tbd("掲載予定","To be listed")),
              (t("使用期限","Shelf life"), t("未開封 ","Unopened ") + tbd() + t("　開封後 "," · After opening ") + tbd()),
              (t("JANコード","JAN / EAN"), tbd()),
              (t("入数・ケースサイズ","Case pack"), tbd())]
    det = ''
    for i, p in enumerate(b.PRODUCTS()):
        # EN_ONLY: no "buy" button pointing to Japanese consumer stores
        ask = cta_btn("product", "" if not EN() else "btn--fill", p["id"], ("この商品について相談する", "Ask about this product"))
        btns = t(f'{btn("#stores","購入する","","btn--fill")}{ask}', f'{ask}{btn("partners.html","","Become a distributor")}')
        rows = ''.join(f'<div><dt>{a}</dt><dd>{v}</dd></div>' for a, v in p["rows"] + common)
        tg = ''.join(f'<li>{x}</li>' for x in p["tags"])
        lb = ''.join(f'<li>{x}</li>' for x, c in p["lbls"])
        det += f'''<section class="sec pd{" pd--r" if i % 2 else ""}" id="{p["id"]}"><div class="wrap pd__g">
<div class="pd__vis rv">{win(p["img"], p["name"], "win--l")}<p class="pd__no">No.{i+1:02d}</p></div>
<div class="pd__txt rv"><p class="pd__cat">{p["cat"]}</p><h2 class="pd__n">{pname(p["name"])}</h2><p class="pd__sub">{p["sub"]}</p>
<ul class="pd__lb">{lb}</ul>
<p class="pd__cp">{p["catch"]}</p><p class="pd__ds">{p["desc"]}</p>
{f'<ul class="tags tags--ink">{tg}</ul>' if tg else ''}
<dl class="dl dl--spec">{rows}</dl>
<div class="ctas">{btns}</div></div>
</div></section>'''
    collab = brand_collab()
    return page("brand.html", "brand", t("ブランド・製品","Brand &amp; Products"),
                t("花印のブランド理念と製品ラインナップ。クレンジングローション、フェイスマスク、ハトムギ化粧水。無香料・無着色・オイルフリー・アルコールフリーの日本製スキンケア。",
                  "HANAJIRUSHI brand philosophy and product line-up: Deep Cleansing Lotion, Super Moisture Face Mask, Hatomugi Skin Conditioner. Clean formulas, made in Japan."),
                hd + phil + lineup + det + collab + store_section())

# ============================================================ COMPANY
def msg_img():
    if V11():
        return (f'<figure class="msg__img msg__ph rv"><div>{seal(cls="seal--m")}<small>{t("代表者写真","Portrait")}</small>'
                f'{tbd("撮影・ご提供待ち","To be supplied")}</div></figure>')
    return f'<figure class="msg__img rv"><img src="{IMG}h_campany_ent.jpg" alt="" loading="lazy"><figcaption>{t("銀座本社 エントランス","Ginza head office, entrance")}</figcaption></figure>'

def MESSAGE14():
    """The representative's message (client text, change proposal 2026-10-07; English is our draft)."""
    return t(["私たち花印は、銀座を出発点に、一人ひとりが自分らしい美しさと出会えるスキンケアを追求してきました。",
              "肌質も、年齢も、求める美しさも、人それぞれです。だからこそ、私たちは一人ひとりの肌と真摯に向き合い、毎日の暮らしの中で無理なく続けられる、身近で心地よいスキンケアを届けたいと考えています。",
              "私たちが目指すのは、日本のお客様だけでなく、世界中の人々に、花印のスキンケアを通じて自分らしい美しさを育んでいただくことです。",
              "品質と使い心地にこだわり、お客様の声に耳を傾けながら、国や文化を越えて、一人ひとりに寄り添う商品づくりに取り組んでまいります。",
              "銀座から世界へ。これからも花印は、毎日のスキンケアを通じて、一人ひとりの「キレイ」を応援し続けます。"],
             ["Starting from Ginza, Hanajirushi has pursued skincare that helps each person discover a beauty of their own.",
              "Skin type, age and the beauty people seek all differ. That is why we meet each person's skin sincerely, and want to offer skincare that is approachable, comfortable and easy to keep up in daily life.",
              "Our aim is for people not only in Japan but all over the world to nurture their own beauty through Hanajirushi skincare.",
              "Committed to quality and comfort, and listening to our customers, we will keep making products that stay close to each person, across countries and cultures.",
              "From Ginza to the world: through everyday skincare, Hanajirushi will keep supporting the beauty of every person."])

def p_company():
    A = b.A
    hd = phero("Company", "会社概要", "Company",
               t("東京・銀座から、日本のスキンケアを世界へ。","Japanese skincare, from Ginza, Tokyo to the world."),
               "h_campany_top_p.jpg", "銀座",
               [A("message","代表メッセージ" if V14() else "代表挨拶","Message"),A("profile","会社概要","Profile"),A("business","事業内容","Business")] + ([] if V14() else [A("history","沿革","History")]) + [A("office","オフィス紹介","Office"),A("access","アクセス","Access"),("rd.html",t("研究開発・品質","R&amp;D &amp; quality"))], pos="30% center")
    head_ = t(f'<h2 class="msg__tate">{lines("銀座から、<br>世界へ。")}</h2>', f'<h2 class="msg__h">{lines("From Ginza,<br><em>to the world.</em>")}</h2>')
    msg = f'''<section class="sec msg" id="message"><div class="wrap msg__g">
<div class="msg__s rv">{eb("Message","01")}{head_}</div>
<div class="msg__txt rv"><p>{b.MESSAGE_PH()}</p>
<p class="msg__sig">{t("花印粧業研究所株式会社<br>代表取締役 ","Hanajirushi Institute of Cosmetics, Inc.<br>Representative Director ")}{tbd("氏名","Name TBC")}</p></div>
{msg_img()}
</div></section>'''
    if V14():   # change proposal: the client's message, no portrait
        paras = ''.join(f'<p>{x}</p>' for x in MESSAGE14())
        msg = f'''<section class="sec msg msg--noimg" id="message"><div class="wrap msg__g">
<div class="msg__s rv">{eb("Message","01")}{head_}</div>
<div class="msg__txt rv"><p class="msg__lead">{t("一人ひとりの美しさに、寄り添い続ける。","Staying close to the beauty of every person.")}</p>{paras}
<p class="msg__end" lang="ja">ひとりに、ひとつの、キレイを咲かせる。</p>{slogan_en("slogan-en--msg")}
<p class="msg__sig">{t("花印粧業研究所株式会社<br>代表取締役","Hanajirushi Institute of Cosmetics, Inc.<br>Representative Director")}</p></div>
</div></section>'''
    prof = f'''<section class="sec sec--t blush" id="profile"><div class="wrap prof__g">
{shd("02","Profile","会社概要","Company profile", kj="会社概要")}
<table class="ptbl rv">{b.company_rows(full=True).replace(" " + tbd("氏名","Name TBC"), "") if V14() else b.company_rows(full=True)}</table></div></section>'''
    # EN_ONLY: corporate structure note
    struct = '' if not EN() else f'''<section class="sec--s"><div class="wrap"><div class="note-box rv">{eb("Corporate structure")}<p>{b.STRUCTURE_EN()}</p></div></div></section>'''
    kan = ["I", "II", "III"] if EN15() else ["一", "二", "三"]
    biz = ''.join(f'''<li class="rv"><div class="arch"><img src="{IMG}{im}" alt="" loading="lazy"></div>
<p class="craft__n"><span>{kan[i]}</span>{n}</p><h3>{h}</h3><p>{p}</p><ul class="tags tags--ink">{"".join(f"<li>{c}</li>" for c in cs)}</ul></li>''' for i, (im, n, h, p, cs, u) in enumerate(b.BUSINESS()))
    business = f'''<section class="sec biz" id="business"><div class="wrap">
{shd("03","Business","事業内容","Our business", kj="事業内容", cls="shd--c",
     lead=t("化粧品の原料、化粧品、健康食品の研究開発、製造、販売及び輸出入","R&amp;D, manufacturing, sales, import and export of cosmetic raw materials, cosmetics and health foods"))}
<ol class="craft__l">{biz}</ol></div></section>'''
    hist = ''.join(f'<li class="rv"><p class="tl__d">{a}</p><p class="tl__t">{v}</p></li>' for a, v in b.HISTORY())
    history = f'''<section class="sec dark hist" id="history"><div class="wrap hist__g">
<div>{shd("04","History","沿革","History", kj="沿革")}<p class="note">{t("※ 年月は確認のうえ掲載します。","Dates to be confirmed.")}</p></div>
<ol class="tl">{hist}</ol></div></section>'''
    shown = {im for im, *_ in b.BUSINESS()} if V11() else set()
    ph = ''.join(f'<li class="rv"><figure><img src="{IMG}{im}" alt="" loading="lazy"><figcaption>{x}</figcaption></figure></li>' for im, x in b.OFFICE_PHOTOS() if im not in shown)
    office = f'''<section class="sec office" id="office"><div class="wrap">
{shd("04" if V14() else "05","Office","オフィス紹介","Our Ginza office", kj="オフィス紹介", cls="shd--c",
     lead=t("銀座二丁目の本社に、研究室・ショールーム・応接室を備えています。","Our head office in Ginza 2-chome houses our laboratory, showroom and meeting rooms."))}
<div class="office__g"><figure class="office__main rv"><img src="{IMG}h_campany_bldg.jpg" alt="" loading="lazy"><figcaption>{t("本社ビル（銀座二丁目）","Head office, Ginza 2-chome")}</figcaption></figure>
<ul class="office__l">{ph}</ul></div></div></section>'''
    rows = [(t("所在地","Address"), ADDR(True)), (t("最寄駅","Stations"), b.STATIONS() + tbd("分数","min TBC")),
            ("TEL", TEL()), ("FAX", FAX()), (t("受付時間","Hours"), t("平日 10:00〜18:00（土日祝除く）","Mon–Fri 10:00–18:00 (JST)"))]
    access = f'''<section class="sec sec--t blush" id="access"><div class="wrap acc__g">
<div class="acc__map rv"><iframe loading="lazy" title="{t("地図","Map")}" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%B8%AD%E5%A4%AE%E5%8C%BA%E9%8A%80%E5%BA%A72-12-12&output=embed&hl={b.L}"></iframe></div>
<div class="rv">{shd("05" if V14() else "06","Access","アクセス","Access", kj="アクセス")}
<dl class="dl">{"".join(f"<div><dt>{a}</dt><dd>{v}</dd></div>" for a, v in rows)}</dl>
{lnk("https://maps.google.com/?q=2-12-12+Ginza+Chuo-ku+Tokyo","Googleマップで見る","Open in Google Maps")}</div>
</div></section>'''
    return page("company.html", "company", t("会社概要","Company"),
                t("花印粧業研究所株式会社の会社概要。代表メッセージ、事業内容、オフィス紹介、アクセス。2015年創業、東京・銀座本社。" if V14() else "花印粧業研究所株式会社の会社概要。代表挨拶、事業内容、沿革、オフィス紹介、アクセス。2015年創業、東京・銀座本社。",
                  "Company profile of Hanajirushi Institute of Cosmetics, Inc. Founded 2015, headquartered in Ginza, Tokyo, with in-house R&D, manufacturing and export."),
                hd + msg + prof + struct + business + ("" if V14() else history) + office + access)

# ============================================================ R&D
def p_rd():
    A = b.A
    hd = phero("R&amp;D / Quality", "研究開発・<br>品質管理", "R&amp;D &amp; Quality",
               t("銀座の自社研究室から、確かな処方を。","Reliable formulas, from our own laboratory in Ginza."),
               None if V11() else "h_campany_lab.jpg", "研究",
               [A("lab","自社研究室","Laboratory"),A("process","開発から出荷まで","Process"),A("quality","品質管理体制","Quality"),A("docs","輸出書類","Export documents"),A("regist","各国登録の支援","Registration")],
               parent=("company.html", t("会社情報","Company") if V13() else t("企業情報","Company")))
    pts = [(b.RD_POINT1_T(), b.RD_POINT1_D()), (b.RD_POINT2_T(), b.RD_POINT2_D()), (b.RD_POINT3_T(), b.RD_POINT3_D())]
    kan = ["I", "II", "III"] if EN15() else ["一", "二", "三"]
    trio = ''.join(f'<li class="rv"><p class="craft__n"><span>{kan[i]}</span></p><h3>{h}</h3><p>{d}</p></li>' for i, (h, d) in enumerate(pts))
    lab = f'''<section class="sec split" id="lab"><div class="wrap split__g">
{f'<div class="split__img split__img--win rv">{win("h_campany_lab.jpg", t("銀座本社の研究室","Our laboratory in Ginza"), "win--m")}</div>' if V11() else f'<div class="split__img rv"><div class="arch"><img src="{IMG}h_campany_lab.jpg" alt="" loading="lazy"></div></div>'}
<div class="split__txt rv">{shd("01","Laboratory","銀座の自社研究室","Our laboratory in Ginza", kj="自社研究室")}
<p class="pd__cp">{b.RD_CATCH()}</p><p>{b.RD_P1()}</p><p>{b.RD_P2()}</p>
<ul class="tags tags--ink">{"".join(f"<li>{x}</li>" for x in b.RD_TAGS())}</ul>
<div class="ctas">{cta_btn("oem","btn--fill")}</div></div>
</div>
<div class="wrap"><ol class="trio">{trio}</ol></div></section>'''
    process = f'''<section class="sec sec--t blush" id="process"><div class="wrap">
{shd("02","Process","開発から出荷まで","From formulation<br><em>to shipment</em>", kj="開発プロセス", cls="shd--c")}
{flow(b.RD_STEPS())}</div></section>'''
    q = [(b.QUALITY1_T(), b.QUALITY1_S(), b.QUALITY1_B()), (b.QUALITY2_T(), b.QUALITY2_S(), b.QUALITY2_B()), (b.QUALITY3_T(), b.QUALITY3_S(), b.QUALITY3_B())]
    quality = f'''<section class="sec" id="quality"><div class="wrap">
{shd("03","Quality","品質管理体制","Quality management", kj="品質管理",
     lead=t("工場情報・認証・生産能力は確認のうえ掲載します。","Factory details, certifications and capacity will be published once confirmed."))}
<ul class="cells cells--3">{"".join(f'<li class="rv">{"" if EN15() else f"<small>{s}</small>"}<h3>{h}</h3><p>{d}</p></li>' for h, s, d in q)}</ul></div></section>'''
    docs = f'''<section class="sec dark" id="docs"><div class="wrap docs__g">
<div>{shd("04","Export documents","輸出書類への対応","Export<br><em>documentation</em>", kj="輸出書類",
     lead=t("海外のお取引先の輸入・登録手続きに必要な書類を、製品ごとにご用意します。","The documents your importer and regulator will ask for — prepared for each product."))}</div>
{docs_list()}</div></section>'''
    reg = f'''<section class="sec sec--t" id="regist"><div class="wrap">
{shd("05","Registration","各国登録の技術支援","Registration support<br><em>by market</em>", kj="各国登録",
     lead=t("登録実績の有無にかかわらず、現地登録に必要な技術資料の提供でパートナー様の手続きを支援します。","Whether or not we have registered in your market before, we support your local registration with the technical documentation it requires."))}
<div class="rv">{reg_table()}</div>
<div class="ctr ctr--2">{cta_btn("product","btn--fill")}{lnk("partners.html","代理店募集について","Partnership programme")}</div></div></section>'''
    return page("rd.html", "rd", t("研究開発・品質","R&amp;D &amp; Quality"),
                t("花印の研究開発と品質管理。銀座の自社研究室での処方開発、日本国内での製造、輸出書類、各国登録の技術支援。",
                  "HANAJIRUSHI R&D and quality: in-house formulation in Ginza, manufacturing in Japan, export documentation and registration support."),
                hd + lab + process + quality + docs + reg)

# ============================================================ COLLABORATION
def p_collaboration():
    A = b.A
    hd = phero("Collaboration", "IP<br>コラボレーション", "Licensed IP Collaborations",
               t("日本の人気IPとの正規ライセンス商品。","Officially licensed products with leading Japanese IP."),
               None if V11() else "h_hanajirushi_top-1.jpg", "協創",
               [A("about","コラボレーションについて","About"),A("works","コラボレーション実績","Portfolio"),A("value","パートナー様へのメリット","Value for partners")],
               parent=("brand.html", t("ブランド","Brand") if V13() else t("ブランド・製品","Brand &amp; Products")))
    about = f'''<section class="sec" id="about"><div class="wrap about__g">
<div class="rv">{shd("01","About","コラボレーションについて","About our collaborations", kj="コラボレーション")}<p class="pd__cp">{b.COLLAB_CATCH()}</p></div>
<div class="about__txt rv"><p>{b.COLLAB_P1()}</p><p>{b.COLLAB_P2()}</p></div>
</div></section>''' if V11() else f'''<section class="sec split" id="about"><div class="wrap split__g split__g--r">
<div class="split__txt rv">{shd("01","About","コラボレーションについて","About our collaborations", kj="コラボレーション")}
<p class="pd__cp">{b.COLLAB_CATCH()}</p><p>{b.COLLAB_P1()}</p><p>{b.COLLAB_P2()}</p></div>
<div class="split__img rv"><figure class="sq"><img src="{IMG}hanajirushi_col_sm.jpg" alt="" loading="lazy"></figure></div>
</div></section>'''
    works = f'''<section class="sec sec--t blush collab" id="works"><div class="wrap">
{shd("02","Portfolio","コラボレーション実績","Collaboration portfolio", kj="コラボレーション実績", cls="shd--c")}
<ul class="ipcards">{ip_cards(detail=True)}</ul>
<p class="note ctr-t">{IPNOTE()}<br>{t("※ IP名称・画像の公開範囲は各ライセンス契約を確認のうえ掲載します","IP names and images will be published within the scope of each licence agreement")} {tbd()}</p>
</div></section>'''
    value = f'''<section class="sec" id="value"><div class="wrap why__g">
<div class="why__h rv">{shd("03","Merit","パートナー様への<br>メリット","What this means<br><em>for distributors</em>", kj="パートナー様へのメリット")}
<div class="ctas">{cta_btn("oem","btn--fill")}{lnk("partners.html","代理店募集について","Partnership programme")}</div></div>
{numbered(b.COLLAB_VALUES())}
</div></section>'''
    return page("collaboration.html", "collaboration", t("IPコラボレーション","Licensed IP Collaborations"),
                t("花印のIPコラボレーション。美少女戦士セーラームーン、リトルツインスターズ、フルーツバスケット、ユーリ!!! on ICE との正規ライセンス商品。",
                  "HANAJIRUSHI licensed IP collaborations: Sailor Moon, Little Twin Stars, Fruits Basket, Yuri!!! on ICE. Full co-development capability for distributors."),
                hd + about + works + value)

# ============================================================ GLOBAL
def global_sections():
    """海外展開 (formerly global.html), merged into the partners page: network + markets, then China."""
    regs = ''.join(f'<li class="rv">{"" if EN15() else f"<small>{e}</small>"}<h3>{a}</h3><p>{d}</p><ul class="tags tags--ink">{"".join(f"<li>{c}</li>" for c in cs)}</ul></li>' for a, e, d, cs in b.REGIONS())
    net = f'''<section class="sec sec--t blush" id="network"><div class="wrap">
{shd("02","Global network","世界12ヵ国で販売","Sold in<br><em>12 countries</em>", kj="海外展開", cls="shd--c",
     lead=t("日本ならではの上質で誠実なものづくりが認められ、国内はもとより世界12ヵ国で販売されています。","Recognised for the quality and honesty of Japanese manufacturing, HANAJIRUSHI is sold in Japan and 12 countries worldwide."))}
{"" if V11() else f'<div class="gnet rv"><img src="{IMG}world_map_brand.png" alt="{t("販売地域の地図","Map of our markets")}" loading="lazy"></div>'}
{gstats()}
<p class="note ctr-t">{t("※ 販売国の一覧は確認のうえ掲載します","Country list to be confirmed")} {tbd("12ヵ国リスト","12-country list")}</p>
<ul class="cells cells--3">{regs}</ul></div></section>'''
    ch = [(b.CHINA1_T(), b.CHINA1_S(), b.CHINA1_B()), (b.CHINA2_T(), b.CHINA2_S(), b.CHINA2_B()), (b.CHINA3_T(), b.CHINA3_S(), b.CHINA3_B()), (b.CHINA4_T(), b.CHINA4_S(), b.CHINA4_B())]
    china = f'''<section class="sec sec--t" id="china"><div class="wrap">
{shd("03","Market proven","中国市場での実績","Proven in<br><em>China</em>", kj="中国市場での実績",
     lead=t("アジア最大で、最も競争の激しい美容市場で、ECから実店舗まで複数のチャネルを築いてきました。","Asia's largest and most demanding beauty market — where we have built channels from e-commerce to physical retail."))}
<ul class="cells cells--4">{"".join(f'<li class="rv"><small>{s}</small><h3>{h}</h3><p>{d}</p></li>' for h, s, d in ch)}</ul></div></section>'''
    return net + china

# ============================================================ PARTNERS
def p_partners():
    A = b.A
    hd = phero("For Partners", "海外代理店・<br>パートナー募集", "Partnership Programme",
               t("市場と規模に合わせた協業モデルをご用意しています。","Cooperation models to fit your market and scale."),
               MAP() if V11() else "h_brand_top_p.jpg", "協業",
               [A("why","選ばれる理由","Why us"),A("network","海外展開・実績","Global network"),A("models","協業モデル","Models"),A("terms","取引条件","Trade terms"),A("support","輸出書類・登録支援","Export support"),A("flow","お取引の流れ","How to start"),A("faq","よくあるご質問","FAQ")], pos="30% center", variant="map" if V11() else "")
    reasons = [(b.PARTNER_REASON1_T(), b.PARTNER_REASON1_D()), (b.PARTNER_REASON2_T(), b.PARTNER_REASON2_D()), (b.PARTNER_REASON3_T(), b.PARTNER_REASON3_D())]
    why = f'''<section class="sec why" id="why"><div class="wrap why__g">
<div class="why__h rv">{seal("募集中", "seal--txt seal--m")}{shd("01","Now recruiting","海外代理店・<br>パートナー募集中","Now recruiting<br><em>partners</em>", kj="代理店募集")}
<p class="pd__cp">{b.PARTNER_LEAD()}</p><p class="lead">{b.PARTNER_TEXT()}</p>
<div class="ctas">{cta_btn("partner","btn--fill")}</div></div>
{numbered(reasons)}
</div></section>'''
    rows = ''.join(f'<tr><th>{a}{"" if EN15() else f"<small>{e}</small>"}</th><td>{c}</td><td>{d}</td></tr>' for a, e, c, d in b.MODES())
    models = f'''<section class="sec sec--t blush" id="models"><div class="wrap">
{shd("04","Models","協業モデル","Cooperation models", kj="協業モデル")}
<div class="sx rv"><table class="mtbl"><thead><tr><th>{t("協業モデル","Model")}</th><th>{t("対象","For")}</th><th>{t("ご提示する主な条件","What we define together")}</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>'''
    terms = f'''<section class="sec sec--t" id="terms"><div class="wrap prof__g">
<div>{shd("05","Trade terms","取引条件","Trade terms", kj="取引条件",
     lead=t("数値は確認のうえ掲載します。","Figures to be confirmed before publishing."))}</div>
<table class="ptbl rv">{"".join(f"<tr><th>{a}</th><td>{v}</td></tr>" for a, v in b.TERMS())}</table></div></section>'''
    support = f'''<section class="sec dark" id="support"><div class="wrap docs__g">
<div>{shd("06","Export support","輸出書類・<br>各国登録の支援","Export documents<br><em>&amp; registration</em>", kj="輸出書類・登録支援")}</div>
{docs_list()}</div>
<div class="wrap"><div class="mtbl--dark rv">{reg_table()}</div></div></section>'''
    flow_ = f'''<section class="sec sec--t blush" id="flow"><div class="wrap">
{shd("07","How to start","お取引開始までの流れ","How to<br><em>get started</em>", kj="お取引の流れ", cls="shd--c")}
{flow(b.PARTNER_STEPS())}
<div class="ctr ctr--2">{cta_btn("partner","btn--fill", label=("代理店申込フォームへ","Apply to become a partner"))}</div></div></section>'''
    qa = ''.join(f'<details class="faq__i"{" open" if i == 0 else ""}><summary><span class="faq__q">Q</span><span>{q}</span></summary><div class="faq__a"><span class="faq__q">A</span><p>{a}</p></div></details>' for i, (q, a) in enumerate(b.FAQ()))
    faq = f'''<section class="sec" id="faq"><div class="wrap prof__g">
<div>{shd("08","FAQ","よくあるご質問","Frequently asked<br><em>questions</em>", kj="よくあるご質問")}
<div class="ctas">{cta_lnk("business")}</div></div>
<div class="faq rv">{qa}</div></div></section>'''
    return page("partners.html", "partners", t("海外代理店・パートナー募集","Partnership Programme"),
                t("花印の海外代理店・パートナー募集。世界12ヵ国での販売実績、中国市場での実績、協業モデル、取引条件、輸出書類、各国登録の技術支援、お取引開始までの流れ、よくあるご質問。",
                  "Become a HANAJIRUSHI distributor: sold in 12 countries, proven in China; cooperation models, trade terms, export documentation, registration support, how to start and FAQ."),
                hd + why + global_sections() + models + terms + support + flow_ + faq)

# ============================================================ EXHIBITION
def EXHIBITIONS():
    """Upcoming shows, in date order; each has its own buyer page (WordPress: an `exhibition`
    post with a page link). Past shows are not listed until the client confirms them."""
    return [dict(year="2026", month=t("11月", "Nov"), name="Cosmoprof Asia 2026",
                 venue=t("香港コンベンション＆エキシビションセンター（香港・湾仔）", "Hong Kong Convention &amp; Exhibition Centre, Wan Chai"),
                 status=t("商談予約受付中", "Booking meetings now"), page=lp_href())]

def exh_list():
    A = b.A
    hd = phero("Exhibition", "展示会情報", "Exhibitions",
               t("出展予定の展示会と、これまでの出展。","Where to meet us: upcoming and past exhibitions."),
               None, "出展", [A("upcoming","開催予定","Upcoming"),A("past","過去の出展","Past exhibitions")])
    rows = ''
    for e in EXHIBITIONS():
        rows += f'''<article class="exl rv">
<p class="exl__d"><b>{e["year"]}</b><span>{e["month"]}</span>{tbd("日程確定待ち","Dates TBC")}</p>
<div class="exl__b"><p class="exl__st">{e["status"]}</p><h3>{e["name"]}</h3><p class="exl__v">{e["venue"]}</p>
<dl class="dl"><div><dt>{t("ブース","Booth")}</dt><dd>{tbd("確定待ち","TBC")}</dd></div>
<div><dt>{t("出展内容","On show")}</dt><dd>{b.EXH_ONSHOW()}</dd></div>
<div><dt>{t("対応言語","Languages")}</dt><dd>{t("日本語・英語・中国語 ","Japanese, English, Chinese ")}{tbd()}</dd></div></dl></div>
<div class="exl__a">{btn(e["page"],"展示会専用ページへ","Open the event page","btn--fill")}{lnk(e["page"].split("#")[0] + "#booking","商談を予約する","Book a meeting")}</div>
</article>'''
    up = f'''<section class="sec sec--t" id="upcoming"><div class="wrap">
{shd("01","Upcoming","開催予定の展示会","Upcoming exhibitions", kj="開催予定",
     lead=t("会期中の商談は、各展示会の専用ページからご予約いただけます。","Meetings during a show are booked on that show's own page."))}
<div class="exl__l">{rows}</div></div></section>'''
    past = f'''<section class="sec sec--t blush" id="past"><div class="wrap">
{shd("02","Past exhibitions","過去の出展","Past exhibitions", kj="出展実績")}
<p class="exl__none rv">{t("過去の出展実績は、確認のうえ掲載します。","Past exhibitions will be listed once confirmed.")} {tbd()}</p></div></section>'''
    return page("exhibition.html", "exhibition", t("展示会情報","Exhibitions"),
                t("花印の展示会情報。出展予定の展示会と専用の商談ページ、過去の出展実績。",
                  "HANAJIRUSHI exhibitions: upcoming shows with their own meeting pages, and past exhibitions."),
                hd + up + past)

def p_exhibition():
    if V12():
        return exh_list()
    A = b.A
    hd = phero("Exhibition", "展示会情報", "Exhibitions",
               t("展示会への出展情報と、商談のご予約。","Where to meet us — and how to book a meeting."),
               None, "出展",
               [A("outline","出展概要","Outline"),A("products","出展製品","Products"),A("booking","商談のご予約","Book a meeting")])
    rows = [(t("展示会名","Event"), "Cosmoprof Asia 2026"),
            (t("会期","Dates"), t("2026年11月","November 2026") + " " + tbd("日程確定待ち","TBC")),
            (t("会場","Venue"), t("香港コンベンション＆エキシビションセンター（香港・湾仔）","Hong Kong Convention &amp; Exhibition Centre, Wan Chai")),
            (t("ホール・ブース番号","Hall / booth"), tbd("確定待ち","TBC")),
            (t("出展内容","On show"), b.EXH_ONSHOW()),
            (t("対応言語","Languages"), t("日本語・英語・中国語 ","Japanese, English, Chinese ") + tbd())]
    outline = f'''<section class="sec sec--t" id="outline"><div class="wrap exo__g">
{exh_card()}
<div class="rv">{shd("01","Outline","出展概要","Outline", kj="出展概要")}
<table class="ptbl">{"".join(f"<tr><th>{a}</th><td>{v}</td></tr>" for a, v in rows)}</table></div>
</div></section>'''
    cards = ''.join(f'''<li class="rv"><a href="brand.html#{p["id"]}">{win(p["img"], p["name"])}
<p class="col__no">No.{i+1:02d}<span>{p["cat"]}</span></p><h3>{pname(p["name"])}</h3></a>
{cta_lnk("product","lnk--s",p["id"],("取扱い相談","Enquire"))}</li>''' for i, p in enumerate(b.PRODUCTS()) if not (V11() and not p["img"]))
    prods = f'''<section class="sec sec--t blush col" id="products"><div class="wrap">
{shd("02","On display","出展製品","Products on display", kj="出展製品", cls="shd--c")}
<ul class="col__l col__l--exh{" col__l--3" if V11() else ""}">{cards}</ul>{soon_note(enumerate(b.PRODUCTS())) if V11() else ""}</div></section>'''
    days = t(["1日目","2日目","3日目"], ["Day 1","Day 2","Day 3"])
    slots = ''.join(f'<p class="slotday">{d} {tbd("日付","Date TBC")}</p><div class="slots">' + ''.join(f'<button type="button" data-day="{d}"{" disabled class=off" if (i + j) % 7 == 3 else ""}>{tm}</button>' for j, tm in enumerate(b.SLOT_TIMES())) + '</div>' for i, d in enumerate(days))
    req, opt = f'<em class="req">{t("必須","Required")}</em>', f'<em class="opt">{t("任意","Optional")}</em>'
    booking = lp_block() if V12() else f'''<section class="sec" id="booking"><div class="wrap book__g">
<div class="rv">{shd("03","Book a meeting","商談のご予約","Book a meeting", kj="商談のご予約",
     lead=t("30分単位でご予約いただけます。ご希望の日時を選択し、必要事項をご記入ください。","30-minute slots. Pick a time, fill in your details and we will confirm by email."))}
<form class="pform">
<p class="pform__h">{t("ご希望の日時を選択","Choose a time")}</p>{slots}
<p class="legend"><span><i></i>{t("予約可","Available")}</span><span><i class="on"></i>{t("選択中","Selected")}</span><span><i class="off"></i>{t("予約済","Booked")}</span></p>
<p class="slotout">{t("選択中の日時：","Selected: ")}<b data-slot-out>{t("未選択","none")}</b></p>
<div class="fgrid">
<label class="fld"><span>{t("会社名","Company")}{req}</span><input type="text"></label>
<label class="fld"><span>{t("お名前","Name")}{req}</span><input type="text"></label>
<label class="fld"><span>{t("メールアドレス","Business email")}{req}</span><input type="email"></label>
<label class="fld"><span>WhatsApp / WeChat{opt}</span><input type="text"></label>
<fieldset class="fld fld--full"><legend>{t("ご相談内容","Topics")}{opt}</legend><div class="opts">{"".join(f'<label><input type="checkbox">{x}</label>' for x in b.BOOKING_TOPICS())}</div></fieldset>
</div>
<div class="pform__sub"><button class="btn btn--fill" type="submit"><span>{t("予約をリクエストする","Request this slot")}</span>{ARR}</button></div></form></div>
<aside class="book__side rv"><p class="pform__h">{t("展示会担当者","Your contact at the show")}</p>
<dl class="dl">
<div><dt>{t("担当者","Contact")}</dt><dd>{tbd("氏名","Name TBC")}</dd></div>
<div><dt>WhatsApp</dt><dd>{tbd("番号","Number TBC")}</dd></div>
<div><dt>WeChat</dt><dd>{tbd("ID","ID TBC")}</dd></div>
<div><dt>{t("メール","Email")}</dt><dd>export@hanajirushi.co.jp {tbd()}</dd></div></dl>
<div class="qrs"><figure><span>QR</span><figcaption>WeChat</figcaption></figure><figure><span>QR</span><figcaption>WhatsApp</figcaption></figure></div>
<p class="pform__h">{t("資料ダウンロード","Downloads")}</p>
<ul class="dlist"><li><a href="#">{t("会社案内","Company profile")}<small>PDF</small></a></li><li><a href="#">{t("製品カタログ","Product catalogue")}<small>PDF</small></a></li></ul></aside>
</div></section>'''
    return page("exhibition.html", "exhibition", t("展示会情報","Exhibitions"),
                t("花印は Cosmoprof Asia 2026（香港）に出展します。出展概要、出展製品、ブースでの商談のご予約。",
                  "HANAJIRUSHI exhibits at Cosmoprof Asia 2026, Hong Kong. Outline, products on display and meeting booking."),
                hd + outline + prods + booking)

# ============================================================ NEWS
def p_news():
    hd = phero("News", "お知らせ", "News",
               t("花印粧業研究所からのお知らせ・展示会・製品情報。","Announcements, exhibitions and product news."),
               None, "便り", [])
    tabs = [("all", t("すべて","All")), ("exh", t("展示会","Exhibition")), ("prod", t("製品情報","Product")), ("biz", t("企業情報","Business")), ("info", t("お知らせ","Notice"))]
    tb = ''.join(f'<button type="button" data-cat="{k}"{" class=on" if k == "all" else ""}>{v}</button>' for k, v in tabs)
    rows = ''.join(f'<li data-cat="{c}"><a href="news.html"><time>{d}</time><span class="cat">{cl}</span><span class="tt">{x}{"<span class=new>New</span>" if new else ""}</span></a></li>' for d, c, cl, cls, x, new in b.NEWS())
    cats = [(t("展示会","Exhibition"),1),(t("製品情報","Product"),2),(t("企業情報","Business"),1),(t("お知らせ","Notice"),2)]
    body = f'''<section class="sec sec--t"><div class="wrap news__g">
<div class="rv"><div class="ftabs" role="group" aria-label="{t("カテゴリーで絞り込む","Filter by category")}">{tb}</div>
<ul class="nl">{rows}</ul>
<p class="note">{t("※ 記事タイトルはモックアップ用の仮テキストです。","Headlines are placeholder copy for design review.")}</p>
<nav class="pager" aria-label="pagination"><span class="on">1</span><a href="#">2</a><a href="#">3</a><a href="#">{t("次へ","Next")}</a></nav></div>
<aside class="side rv"><p class="pform__h">{t("カテゴリー","Categories")}</p><ul class="dlist">{"".join(f'<li><a href="#">{c}<small>({n})</small></a></li>' for c, n in cats)}</ul>
<p class="pform__h">{t("アーカイブ","Archive")}</p><ul class="dlist"><li><a href="#">2026<small>(5)</small></a></li><li><a href="#">2022<small>(1)</small></a></li></ul>
{exh_card(compact=True)}</aside>
</div></section>'''
    return page("news.html", "news", t("お知らせ","News"),
                t("花印粧業研究所株式会社からのお知らせ。展示会、製品情報、企業情報。", "News from Hanajirushi Institute of Cosmetics, Inc.: exhibitions, products and business updates."),
                hd + body)

# ============================================================ CONTACT
def p_contact():
    hd = phero("Contact", "お問い合わせ", "Contact",
               t("お取引・代理店・製品に関するご相談はこちらから。","Distribution, trade, product and OEM enquiries."),
               None, "相談", [])
    kinds = b.KINDS_V22()
    blurbs = [t("独占代理店・販売代理店・モダントレード・越境ECのご相談。","Exclusive or authorised distribution, modern trade and cross-border e-commerce."),
              t("製品仕様・サンプル・成分・輸出書類についてのお問い合わせ。","Specifications, samples, ingredients and export documents."),
              t("自社ブランド製品の開発、IPコラボレーション商品の企画。","Private-label development and licensed IP collaborations."),
              t("展示会での商談、その他のご相談。","Meetings at exhibitions, and anything else.")]
    topics = ''.join(f'<li class="rv"><a href="{topic_href(k)}"><i>{i+1:02d}</i><b>{kinds[i]}</b><small>{blurbs[i]}</small>{ARR}</a></li>' for i, k in enumerate(b.CTA_TOPICS))
    chan = f'''<ul class="cells cells--3 chan">
<li class="rv"><small>{t("お電話","Telephone")}</small><h3><a href="tel:+81362642154">{TEL()}</a></h3><p>{HOURS()}</p></li>
<li class="rv"><small>{t("フォーム","Enquiry form")}</small><h3>{t("3営業日以内にご返信","Reply within 3 business days")}</h3><p>{t("下記フォームより送信ください。","Use the form below.")}</p></li>
<li class="rv"><small>WhatsApp / WeChat</small><h3>{t("海外のお客様","Overseas partners")}</h3><p>{t("こちらからもご連絡いただけます。","Message us directly.")} ID {tbd()}</p></li></ul>'''
    req, opt = f'<em class="req">{t("必須","Required")}</em>', f'<em class="opt">{t("任意","Optional")}</em>'
    req_en = req if EN() else opt   # EN: WhatsApp/WeChat, position, market and volume qualify overseas leads
    sel = t("選択してください", "Please select")
    def fld(label, inner, mark, full=False, hint=""):
        h = f'<small class="hint">{hint}</small>' if hint else ''
        return f'<label class="fld{" fld--full" if full else ""}"><span>{label}{mark}</span>{inner}{h}</label>'
    kind_opts = ''.join(f'<label><input type="radio" name="k" value="{v}"{" checked" if i == 0 else ""}>{k}</label>' for i, (k, v) in enumerate(zip(kinds, b.CTA_TOPICS)))
    lines = ''.join(f'<label><input type="checkbox" data-items="{it}">{x}</label>' for x, it in product_lines())
    form = f'''<form class="pform pform--main" id="form">
<ol class="fstep"><li class="on"><i>01</i>{t("入力","Enter")}</li><li><i>02</i>{t("確認","Confirm")}</li><li><i>03</i>{t("完了","Done")}</li></ol>
<fieldset class="fld fld--full"><legend>{t("お問い合わせ種別","Enquiry type")}{req}</legend><div class="opts">{kind_opts}</div></fieldset>
<div class="fgrid">
{fld(t("会社名","Company name"), f'<input type="text" placeholder="{t("例）花印粧業研究所株式会社","e.g. ABC Trading Co., Ltd.")}">', req)}
{fld(t("国・地域","Country / region"), f'<input type="text" placeholder="{t("例）日本、ベトナム","e.g. Vietnam")}">', req)}
{fld(t("お名前","Contact person"), f'<input type="text" placeholder="{t("例）山田 花子","e.g. Jane Tan")}">', req)}
{fld(t("役職","Position"), '<input type="text">', req_en)}
{fld(t("メールアドレス","Business email"), f'<input type="email" placeholder="{t("例）info@example.com","e.g. jane@company.com")}">', req, hint=t("フリーメールではなく、会社ドメインのアドレスをご記入ください。","Please use your company domain rather than a free webmail address."))}
{fld(t("電話番号","Phone"), f'<input type="tel" placeholder="{t("例）03-1234-5678","e.g. +84 28 1234 5678")}">', opt)}
{fld("WhatsApp / WeChat", '<input type="text">', req_en, hint=t("海外のお客様はいずれかをご記入ください。","Either one is fine."))}
{fld(t("事業形態","Business type"), f'<select><option>{sel}</option>{"".join(f"<option>{x}</option>" for x in b.BIZ_TYPES())}</select>', req)}
{fld(t("対象市場","Target market"), f'<input type="text" placeholder="{t("例）タイ、マレーシア","e.g. Thailand, Malaysia")}">', req_en)}
{fld(t("年間予定仕入数量","Estimated annual volume"), f'<select><option>{sel}</option>{"".join(f"<option>{v}</option>" for v in b.VOLUMES())}</select>', req_en)}
<fieldset class="fld fld--full"><legend>{t("ご関心の製品","Products of interest")}{opt}</legend><div class="opts">{lines}</div></fieldset>
{fld(t("会社ウェブサイト","Company website"), '<input type="url" placeholder="https://">', opt)}
{fld(t("現在の販売チャネル","Current channels"), '<input type="text">', opt)}
{fld(t("お問い合わせ内容","Message"), '<textarea rows="6"></textarea>', req, full=True)}
<fieldset class="fld fld--full"><legend>{t("展示会","Exhibition")}{opt}</legend><div class="opts"><label><input type="checkbox">{t("展示会会場からのお問い合わせです","I am contacting you from the exhibition floor")}</label></div></fieldset>
</div>
<div class="pp"><b>{t("個人情報の取り扱いについて","Handling of personal information")}</b>{t("花印粧業研究所株式会社は、お問い合わせいただいた個人情報を、お問い合わせへの回答およびご連絡のためにのみ利用し、法令に基づく場合を除き、ご本人の同意なく第三者に提供することはありません。（プライバシーポリシー全文は確認のうえ掲載します。）","Hanajirushi Institute of Cosmetics, Inc. uses the personal information you provide only to respond to your enquiry, and does not share it with third parties without your consent except where required by law. (Full privacy policy to be published.)")}</div>
<label class="agree"><input type="checkbox">{t("個人情報の取り扱いに同意する","I agree to the handling of my personal information")}</label>
<div class="pform__sub"><button class="btn btn--fill" type="submit"><span>{t("入力内容を確認する","Review my enquiry")}</span>{ARR}</button></div>
<p class="note ctr-t">{t("送信後、自動返信メールにて会社案内PDFのダウンロードリンクをお送りします。","After sending, you will receive an automatic confirmation with a link to our company profile (PDF).")}</p>
</form>'''
    body = f'''<section class="sec sec--t"><div class="wrap">
{shd("01","Topics","ご相談内容から選ぶ","Choose<br><em>a topic</em>", kj="ご相談内容", lead=t("ご相談内容を選ぶと、フォームの種別が選択された状態になります。","Pick a topic and the form below opens with it selected."))}
<ul class="topics">{topics}</ul>
{chan}</div></section>
<section class="sec sec--t blush"><div class="wrap wrap--form">
{shd("02","Enquiry form","お問い合わせフォーム","Enquiry form", kj="お問い合わせフォーム", cls="shd--c")}
{form}</div></section>'''
    return page("contact.html", "contact", t("お問い合わせ","Contact"),
                t("花印粧業研究所株式会社へのお問い合わせ。海外代理店のお申込み、お取引・製品・OEM/ODMのご相談。",
                  "Contact Hanajirushi Institute of Cosmetics: distributor applications, trade, product and OEM/ODM enquiries. Email, WhatsApp, WeChat."),
                hd + body)

# ============================================================ COSMOPROF ASIA BUYER PAGE (v1.2)
# A standalone, phone-first page for visitors who scan the QR code at the booth:
# premium-1.2/cosmoprof-asia/index.html (English, the address the QR code opens) and ja.html.
# Its own slim header and footer, no site menu; links back to the full site.
LP_DIR = "cosmoprof-asia"

def lp_href(anchor=""):
    """Site pages (premium-1.2/<lang>/) → the buyer page in the visitor's language."""
    return f'../{LP_DIR}/{"index.html" if EN() else "ja.html"}{anchor}'

def lp_site(fn):
    """Buyer page → a page of the main site in the same language."""
    return f'../{b.L}/{fn}'

def lp_block():
    """v1.2 exhibition page: booking now happens on the buyer page, so one form only."""
    return f'''<section class="sec dark lp-hand" id="booking"><div class="wrap lp-hand__g">
<div class="rv">{shd("03","Book a meeting","商談のご予約","Book a meeting", kj="商談のご予約",
     lead=t("会期中の商談のご予約・お問い合わせは、展示会専用ページで承ります。会場では QR コードからもご覧いただけます。",
            "Meeting bookings and enquiries for the show are handled on our dedicated event page. At the booth, scan the QR code to open it."))}</div>
<div class="ctas rv">{btn(lp_href("#booking"),"展示会専用ページを開く","Open the event page","btn--light")}</div>
</div></section>'''

def lp_page():
    p_all = b.PRODUCTS()
    hato = p_all[2]
    other = "ja.html" if EN() else "index.html"
    # ?lang=ja / ?lang=en (links in the V1 style) open the matching file
    want = "ja" if EN() else "en"
    redirect = f"<script>if(/[?&]lang={want}\\b/.test(location.search))location.replace('{other}'+location.hash)</script>"
    title = t("Cosmoprof Asia 2026 商談ページ｜花印 HANAJIRUSHI", "Cosmoprof Asia 2026 — Buyer page | HANAJIRUSHI")
    desc = t("Cosmoprof Asia 2026（香港）に出展する花印の商談ページ。出展製品、取引条件、商談のご予約、展示会担当者の連絡先。",
             "HANAJIRUSHI at Cosmoprof Asia 2026, Hong Kong: products, trade terms at a glance, meeting booking and show contacts.")
    on_ja, on_en = ("on", "") if not EN() else ("", "on")
    lng = f'<span class="lng" role="group" aria-label="Language"><a href="ja.html" class="{on_ja}" lang="ja">JA</a><a href="index.html" class="{on_en}" lang="en">EN</a></span>'
    anchors = [("products", t("出展製品","Products")), ("strengths", t("日本製の強み","Strengths")),
               ("business", t("お取引","Business")), ("booking", t("商談予約","Book a meeting")), ("contact", t("展示会担当","Show contacts"))]
    anc = ''.join(f'<a href="#{i}">{x}</a>' for i, x in anchors)

    facts = [(t("会期","Dates"), t("2026年11月","November 2026") + " " + tbd("日程確定待ち","TBC")),
             (t("会場","Venue"), t("香港コンベンション＆エキシビションセンター","Hong Kong Convention &amp; Exhibition Centre")),
             (t("ブース","Booth"), tbd("確定待ち","TBC")),
             (t("対応言語","Languages"), t("日本語・英語・中国語 ","Japanese, English, Chinese ") + tbd())]
    hero = f'''<section class="lp-hero"><div class="wrap lp-hero__g">
<div class="lp-hero__txt rv">{eb("Cosmoprof Asia 2026 · Hong Kong")}
<h1 class="lp-hero__h">{lines(t('<span class="nw"><span class="lat">Cosmoprof Asia 2026</span>で、</span><br>お会いしましょう。',"Meet us at<br><em>Cosmoprof Asia 2026</em>"))}</h1>
<p class="lp-hero__lead">{t("東京・銀座の日本製スキンケアメーカー、花印です。","HANAJIRUSHI — Japanese skincare, developed in our own laboratory in Ginza, Tokyo. ")}{b.EXH_INTRO()}</p>
<dl class="dl">{"".join(f"<div><dt>{a}</dt><dd>{v}</dd></div>" for a, v in facts)}</dl>
<div class="ctas">{btn("#booking","商談を予約する","Book a meeting","btn--fill")}{lnk("#products","出展製品を見る","See the products")}</div></div>
<div class="lp-hero__vis rv">{win(hato["img"], hato["name"], "win--l")}{seal(cls="seal--l")}</div>
</div></section>'''

    rs = b.REASONS()
    nums = ''.join(f'<li class="rv"><small>{rs[i][0]}</small><b class="{"num" if rs[i][1][:1].isdigit() else "word"}">{rs[i][1]}</b><p>{rs[i][3]}</p></li>' for i in (0, 2, 1, 4))
    trust = f'<section class="nums lp-nums"><div class="wrap"><ul class="nums__l">{nums}</ul></div></section>'

    cards = ''
    for i, p in enumerate(p_all):
        if not p["img"]:
            continue
        cards += f'''<li class="rv">{win(p["img"], p["name"])}
<p class="col__no">No.{i+1:02d}<span>{p["cat"]}</span></p><h3>{pname(p["name"])}</h3><p class="col__d">{p["short"]}</p>
<p class="lp-prod__a"><a class="lnk lnk--s" href="#booking" data-pick="{p["id"]}"><span>{t("この製品を相談する","Discuss this product")}</span>{ARR}</a>
<a class="lnk lnk--s" href="{lp_site(prod_href(p["id"]))}"><span>{t("製品の詳細","Product details")}</span>{ARR}</a></p></li>'''
    soon = ''.join(f'<p class="col__soon rv"><i>No.{i+1:02d}</i>{p["name"]} — {p["short"]}</p>' for i, p in enumerate(p_all) if not p["img"])
    products = f'''<section class="sec col lp-prod" id="products"><div class="wrap">
{shd("01","On display","出展製品","On display", kj="出展製品", cls="shd--c",
     lead=t("無香料・無着色・オイルフリー・アルコールフリー。ブースでお試しいただけます。","Fragrance-free, colorant-free, oil-free, alcohol-free. Try them at our booth."))}
<ul class="col__l col__l--3">{cards}</ul>{soon}</div></section>'''

    kan = ["研", "造", "質", "績"]
    j4 = ''.join(f'<li class="rv"><span class="j4__k{" j4__k--ic" if EN15() else ""}" aria-hidden="true">{I[ic] if EN15() else kan[i]}</span><p class="j4__n">{i+1:02d}</p><h3>{h}</h3><p>{d}</p>{note}</li>'
                 for i, (ic, h, d, note) in enumerate(b.JAPAN4()))
    strengths = f'''<section class="sec sec--t dark j4" id="strengths"><div class="wrap">
{shd("02","Made in Japan","「日本製」4つの強み","Made in Japan —<br><em>four strengths</em>", kj="日本製の強み", cls="shd--c")}
<ol class="j4__l">{j4}</ol>
<div class="ctr">{lnk(lp_site("rd.html"),"研究開発・品質管理","R&amp;D and quality")}</div></div></section>'''

    terms = b.TERMS()
    rows = ''.join(f'<div><dt>{terms[i][0]}</dt><dd>{terms[i][1]}</dd></div>' for i in (0, 1, 2, 3, 6))
    docs = ''.join(f'<li>{a}</li>' for a, d in b.EXPORT_DOCS())
    business = f'''<section class="sec sec--t blush" id="business"><div class="wrap lp-biz__g">
<div class="rv">{shd("03","Working together","市場に合わせた<br>お取引","A model that<br><em>fits your market</em>", kj="お取引について")}
<ul class="models">{b.MODELS_MINI()}</ul>
{lnk(lp_site("partners.html"),"代理店募集の詳細","Partnership programme")}</div>
<div class="rv"><p class="pform__h">{t("主な取引条件","Trade terms at a glance")}</p>
<dl class="dl">{rows}</dl>
<p class="pform__h lp-biz__h">{t("ご用意できる輸出書類","Export documents we prepare")}</p>
<ul class="tags tags--ink">{docs}</ul>
<p class="note">{t("※ 数値・対応範囲は確認のうえ掲載します。","Figures and scope to be confirmed before publishing.")}</p></div>
</div></section>'''

    steps = f'''<section class="sec sec--t" id="steps"><div class="wrap">
{shd("04","Next steps","お取引開始までの流れ","From first meeting<br><em>to first order</em>", kj="お取引の流れ", cls="shd--c")}
{flow(b.PARTNER_STEPS())}</div></section>'''

    # Preferred day and time are free input (feedback 2026-10): few meetings, and a slot grid would
    # need staff to keep booked slots up to date. Staff confirm each meeting by reply.
    days = t(["会期1日目","会期2日目","会期3日目","会期外・オンラインを希望"], ["Day 1","Day 2","Day 3","After the show / online"])
    req, opt = f'<em class="req">{t("必須","Required")}</em>', f'<em class="opt">{t("任意","Optional")}</em>'
    req_en = req if EN() else opt   # EN_ONLY: WhatsApp/WeChat and market qualify overseas leads (as on the contact page)
    sel = t("選択してください", "Please select")
    plines = ''.join(f'<label><input type="checkbox" data-items="{it}">{x}</label>' for x, it in product_lines())
    def fld(label, inner, mark, full=False):
        return f'<label class="fld{" fld--full" if full else ""}"><span>{label}{mark}</span>{inner}</label>'
    booking = f'''<section class="sec sec--t blush" id="booking"><div class="wrap book__g">
<div class="rv">{shd("05","Book a meeting","商談のご予約・お問い合わせ","Book a meeting<br><em>or send an enquiry</em>", kj="商談のご予約",
     lead=t("ご希望の日時をお知らせください。展示会担当者より日時を確定してご連絡します。お問い合わせだけでも承ります。","Tell us when suits you and our show team will confirm the time. You can also just send an enquiry."))}
<form class="pform pform--main">
<p class="pform__h">{t("ご希望の日時","Preferred day and time")}</p>
<div class="fgrid fgrid--when">
{fld(t("ご希望の日","Preferred day"), f'<select><option>{sel}</option>{"".join(f"<option>{d}</option>" for d in days)}</select>', opt)}
{fld(t("ご希望の時間帯","Preferred time"), f'<input type="text" placeholder="{t("例）14:00頃、午後、いつでも可","e.g. around 14:00, afternoon, any time")}">', opt)}
</div>
<p class="note">{t("会期：2026年11月","Show dates: November 2026")} {tbd("日程確定待ち","TBC")}　{t("担当者より日時を確定してご連絡します。","Our show team will confirm the time by reply.")}</p>
<p class="pform__h lp-who">{t("お客様情報","Your details")}</p>
<div class="fgrid">
{fld(t("会社名","Company"), '<input type="text" autocomplete="organization">', req)}
{fld(t("国・地域","Country / region"), '<input type="text" autocomplete="country-name">', req)}
{fld(t("お名前","Name"), '<input type="text" autocomplete="name">', req)}
{fld(t("メールアドレス","Business email"), '<input type="email" autocomplete="email">', req)}
{fld("WhatsApp / WeChat", '<input type="text">', req_en)}
{fld(t("事業形態","Business type"), f'<select><option>{sel}</option>{"".join(f"<option>{x}</option>" for x in b.BIZ_TYPES())}</select>', req)}
<fieldset class="fld fld--full"><legend>{t("ご関心の製品","Products of interest")}{opt}</legend><div class="opts">{plines}</div></fieldset>
{fld(t("ご相談内容","Message"), '<textarea rows="4"></textarea>', opt, full=True)}
</div>
<label class="agree"><input type="checkbox">{t("個人情報の取り扱いに同意する","I agree to the handling of my personal information")}</label>
<div class="pform__sub"><button class="btn btn--fill" type="submit"><span>{t("予約・お問い合わせを送信","Send my request")}</span>{ARR}</button></div>
<p class="note ctr-t">{t("内容を確認のうえ、展示会担当者よりご連絡します。","Our show team will get back to you.")}</p>
</form></div>
<aside class="book__side rv" id="contact"><p class="pform__h">{t("展示会担当者","Your contact at the show")}</p>
<dl class="dl">
<div><dt>{t("担当者","Contact")}</dt><dd>{tbd("氏名","Name TBC")}</dd></div>
<div><dt>WhatsApp</dt><dd>{tbd("番号","Number TBC")}</dd></div>
<div><dt>WeChat</dt><dd>{tbd("ID","ID TBC")}</dd></div>
<div><dt>{t("メール","Email")}</dt><dd>export@hanajirushi.co.jp {tbd()}</dd></div>
<div><dt>{t("東京本社","Tokyo office")}</dt><dd><a href="tel:+81362642154">{TEL()}</a></dd></div></dl>
<div class="qrs"><figure><span>QR</span><figcaption>WeChat</figcaption></figure><figure><span>QR</span><figcaption>WhatsApp</figcaption></figure></div>
<p class="pform__h">{t("資料ダウンロード","Downloads")}</p>
<ul class="dlist"><li><a href="#">{t("会社案内","Company profile")}<small>PDF</small></a></li><li><a href="#">{t("製品カタログ","Product catalogue")}<small>PDF</small></a></li></ul></aside>
</div></section>'''

    share = f'''<section class="sec sec--t lp-share" id="share"><div class="wrap lp-share__g">
<figure class="lp-qr rv"><div id="lp-qr" aria-label="{t("このページのQRコード","QR code for this page")}"><span>QR</span></div></figure>
<div class="rv">{shd("06","Share","このページを共有","Share<br><em>this page</em>", kj="ページを共有",
     lead=t("同僚の方への共有や、後で見返すときにご利用ください。QRコードを読み取ると英語版が開きます（右上で日本語に切り替えられます）。",
            "Pass it to a colleague, or keep it for after the show. The QR code opens the English page; switch to Japanese at the top."))}
<p class="lp-url" data-share-url></p>
<div class="ctas"><button class="btn" type="button" data-copy><span>{t("リンクをコピー","Copy link")}</span>{ARR}</button>
<button class="lnk" type="button" data-qr-dl><span>{t("QRコードを保存（PNG）","Save QR code (PNG)")}</span>{ARR}</button></div>
<p class="note">{t("※ 会場で配布するQRコードは、公開URLの確定後に本番用を発行します。","The QR code printed for the booth will be issued once the public address is final.")}</p></div>
</div></section>'''

    foot = f'''<footer class="ft lp-ft"><div class="wrap">
<div class="lp-ft__g"><div class="ft__co"><a class="ft__logo" href="{lp_site("index.html")}"><img src="{IMG}{LOGO()}" alt="花印 HANAJIRUSHI" width="150" height="40"></a>{seal(cls="seal--s")}
<p class="ft__name">{t("花印粧業研究所株式会社","Hanajirushi Institute of Cosmetics, Inc.")}</p>
<p>{ADDR(True)}</p><p class="ft__tel">TEL {TEL()}</p></div>
<ul class="lp-ft__l"><li><a href="{lp_site("index.html")}">{t("公式サイト トップ","Main website")}</a></li><li><a href="{lp_site("products.html" if V13() else "brand.html")}">{t("製品","Products") if V13() else t("ブランド・製品","Brand &amp; products")}</a></li>
<li><a href="{lp_site("partners.html")}">{t("代理店募集","Partnership programme")}</a></li><li><a href="{lp_site("company.html")}">{t("会社概要","Company profile")}</a></li></ul></div>
<div class="ft__btm"><p>© 2026 Hanajirushi Institute of Cosmetics, Inc.</p><div><a href="#">{t("プライバシーポリシー","Privacy policy")}</a><a href="{other}">{t("English","日本語")}</a></div></div>
</div></footer>
<div class="lp-bar"><a class="btn btn--fill" href="#booking"><span>{t("商談を予約する","Book a meeting")}</span>{ARR}</a><a class="btn" href="#contact"><span>{t("担当者に連絡","Contact us")}</span></a></div>
<button class="totop" type="button" aria-label="{t("ページトップへ","Back to top")}">{I["up"]}</button>
<div class="toast" role="status" aria-live="polite"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script src="{ASSETS}js/premium.js"></script>
<script src="{ASSETS}js/premium-v11.js"></script>
<script src="{ASSETS}js/premium-lp.js"></script>
</body></html>'''

    return f'''<!DOCTYPE html>
<html lang="{b.L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
{redirect}
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ASSETS}css/premium.css">
<link rel="stylesheet" href="{ASSETS}css/premium-v11.css">
<link rel="stylesheet" href="{ASSETS}css/premium-lp.css">{v13_css()}
</head>
<body class="pg-lp">
<a class="skip" href="#main">{t("本文へスキップ","Skip to content")}</a>
<header class="lp-hd" data-hd><div class="lp-hd__in">
<a class="hd__logo" href="{lp_site("index.html")}"><img src="{IMG}{LOGO()}" alt="花印 HANAJIRUSHI" width="132" height="35"></a>
<p class="lp-hd__ev"><b>Cosmoprof Asia 2026</b><span>{t("香港・2026年11月","Hong Kong · November 2026")}</span></p>
<div class="hd__r">{lng}<a class="hd__cta" href="#booking">{t("商談を予約","Book a meeting")}</a></div>
</div></header>
<main id="main">
{hero}
<nav class="anc" aria-label="{t("ページ内リンク","On this page")}"><div class="wrap">{anc}</div></nav>
{trust}{products}{strengths}{business}{steps}{booking}{share}
</main>
{foot}'''

PAGES = {"index.html": p_home, "brand.html": p_brand, "company.html": p_company, "rd.html": p_rd,
         "collaboration.html": p_collaboration, "partners.html": p_partners,
         "exhibition.html": p_exhibition, "news.html": p_news, "contact.html": p_contact}

def build():
    global _VER
    b.IMG = IMG  # build.py helpers that print image paths resolve from premium/<lang>/
    for out, ver in ((OUT, 1.0), (OUT11, 1.1), (OUT12, 1.2), (OUT13, 1.3), (OUT14, 1.4), (OUT15, 1.5)):
        _VER = ver
        for lang in ("ja", "en"):
            b.L = lang
            d = os.path.join(out, lang); os.makedirs(d, exist_ok=True)
            pages = dict(PAGES)
            if V13():   # products list + one page per product (catalog.py)
                pages["products.html"] = p_products13
                for p in cat.PRODUCTS13():
                    if not p["soon"]:
                        pages[cat.page_of(p)] = (lambda p=p: p_product13(p))
            for fn, fn_ in pages.items():
                html = fn_()
                if lang == "ja":
                    html = b.add_wbr(html)
                with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"{os.path.basename(out)} {lang}/{fn:20} {len(html):>7} bytes")
            if V12():
                # the buyer page: index.html (English, the QR address) and ja.html
                d = os.path.join(out, LP_DIR); os.makedirs(d, exist_ok=True)
                html = lp_page()
                if lang == "ja":
                    html = b.add_wbr(html)
                fn = "ja.html" if lang == "ja" else "index.html"
                with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"{os.path.basename(out)} {LP_DIR}/{fn:14} {len(html):>7} bytes")
    _VER = 1.0

if __name__ == "__main__":
    build()
