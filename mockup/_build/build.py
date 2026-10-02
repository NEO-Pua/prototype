# -*- coding: utf-8 -*-
"""
花印 HANAJIRUSHI — bilingual static mockup generator ("local Japanese corporate" style).

Run:  python build.py
Writes ../ja/*.html, ../en/*.html, ../v2.1/ and the review hub ../index.html,
then runs build_premium.py for the Direction B pages in ../premium/.
Uses assets/css/style.css + assets/js/main.js.

Copy sits side by side as t("日本語", "English"). The English edition applies
the content brief's EN-only rules (see EN_ONLY markers): no registered capital
or bank list, no consumer store links, non-literal brand line, +81 phone format,
corporate-structure note.
"""
import os, re, sys, math
import budoux  # pip install budoux
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
L = "ja"  # current language while rendering
VERSION = "2"  # "2" = current design (ja/, en/); "2.1" = soft skin (v2.1/); "2.2" = soft skin + buyer-conversion content (v2.2/)

def V22():
    return VERSION == "2.2"
ASSETS = "../assets/"
IMG = ASSETS + "img/"

FONTS = {
    "2": "family=Noto+Sans+JP:wght@400;500;700;900&family=Shippori+Mincho:wght@500;700&family=Montserrat:wght@500;600;700;800",
    "2.2": "family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Shippori+Mincho:wght@500;600&family=Cormorant+Garamond:wght@500;600&family=Jost:wght@400;500",
    "2.1": "family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Shippori+Mincho:wght@500;600&family=Cormorant+Garamond:wght@500;600&family=Jost:wght@400;500",
}

def t(ja, en):
    return ja if L == "ja" else en

def EN():
    return L == "en"

# ------------------------------------------------------------ icons
BASE_ICONS = {
 "arr": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
 "dl": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v12M7 11l5 5 5-5M4 20h16"/></svg>',
 "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
 "qr": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><path d="M14 14h2v2h-2zM18 14h2v2h-2zM14 18h2v2h-2zM18 18h2v2h-2z"/></svg>',
 "in": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 11v6M8 7v.5M12 17v-6M12 13.5a2.5 2.5 0 0 1 5 0V17"/></svg>',
}

I = dict(BASE_ICONS)
I.update({
 "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6L4.5 18.5A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.5-2.5L14 9V3"/><path d="M7.5 14h9"/></svg>',
 "factory": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21V10l6 3.5V10l6 3.5V6h3l1 15H3z"/><path d="M7 17h2M11 17h2M15 17h2"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6l7-3z"/><path d="M8.8 12.2l2.2 2.2 4.4-4.6"/></svg>',
})

# ---- v2.2: topic-based contact CTAs. contact.html?topic=…(&item=pN) pre-selects the form (see main.js).
CTA_TOPICS = ("partner", "product", "oem", "business")

def cta(topic, ja, en, cls="", item=None):
    q = f"topic={topic}" + (f"&amp;item={item}" if item else "")
    return f'<a class="btn {cls}" href="contact.html?{q}#form">{t(ja, en)}</a>'
I.update({
 "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
 "prev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>',
 "next": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>',
 "pause": '<svg viewBox="0 0 10 10" fill="currentColor"><rect x="1.5" y="1" width="2.4" height="8"/><rect x="6.1" y="1" width="2.4" height="8"/></svg>',
 "play": '<svg viewBox="0 0 10 10" fill="currentColor"><path d="M2 1l7 4-7 4z"/></svg>',
 "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12l4-4 4 2 3-2 4 1 5 4"/><path d="M7 14l3 3c.8.8 2 .8 2.8 0L18 12"/><path d="M2 12l5 5"/></svg>',
 "medal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="14" r="6"/><path d="M8.5 9.5L6 3h4l2 4 2-4h4l-2.5 6.5"/></svg>',
})

def flower(cls=""):
    """5-petal blossom mark used as the section-heading ornament."""
    petals = "".join(f'<ellipse cx="12" cy="6.2" rx="3.4" ry="5" transform="rotate({a} 12 12)"/>' for a in range(0, 360, 72))
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{petals}<circle cx="12" cy="12" r="2.2" fill="#fff"/></svg>'

def laurel():
    """Gold laurel wreath drawn programmatically (two mirrored branches)."""
    cx, cy, r = 75, 66, 56
    out = []
    for side in (1, -1):
        pts = []
        for k in range(0, 41):
            th = math.radians(100 + k * 3.0)
            x = cx + r * math.cos(th)
            if side == -1:
                x = 2 * cx - x
            pts.append((x, cy + r * math.sin(th)))
        for k in range(8):
            th = math.radians(108 + k * 14.5)
            x = cx + r * math.cos(th)
            y = cy + r * math.sin(th)
            if side == -1:
                x = 2 * cx - x
            tang = math.degrees(th) + 90
            rot = (tang + 28) if side == 1 else (180 - tang - 28)
            size = 7.6 - k * 0.35
            out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{size:.1f}" ry="{size*0.42:.1f}" transform="rotate({rot:.1f} {x:.1f} {y:.1f})"/>')
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        out.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    out.append(f'<path d="M{cx-12} {cy+56} Q{cx} {cy+48} {cx+12} {cy+56}" fill="none" stroke="currentColor" stroke-width="2"/>')
    return f'<svg class="laurel" viewBox="0 0 150 130" fill="currentColor" aria-hidden="true">{"".join(out)}</svg>'

def st(big, ja, en, sub_ja=None, sub_en=None):
    """Centred section heading. JA: big EN word + JA title. EN: big EN word + EN title + small kanji."""
    kj = f'<span class="kj">{ja}</span>' if EN() else ''
    sub = t(sub_ja, sub_en)
    p = f'<p>{sub}</p>' if sub else ''
    return f'<div class="st">{flower()}<span class="en">{big}</span><h2>{t(ja, en)}</h2>{kj}{p}</div>'

def stl(big, ja, en, sub_ja=None, sub_en=None):
    """Left-aligned section heading (title left, lead text right). Alternates with st() to vary page rhythm."""
    kj = f'<span class="kj">{ja}</span>' if EN() else ''
    sub = t(sub_ja, sub_en)
    p = f'<p>{sub}</p>' if sub else ''
    return f'<div class="st st--l"><div class="st__hd">{flower()}<span class="en">{big}</span><h2>{t(ja, en)}</h2>{kj}</div>{p}</div>'

def sth(ja, en, more_href=None):
    small = en.upper() if not EN() else ja
    m = f'<a class="more" href="{more_href}">{t("一覧を見る", "View all")}</a>' if more_href else ''
    return f'<div class="sth"><h2>{flower()}{t(ja, en)}<small>{small}</small></h2>{m}</div>'

def hd3(ja, en):
    return f'<h3 class="hd3">{t(ja, en)}<small>{en.upper() if not EN() else ja}</small></h3>'

def tbd(ja="要確認", en="TBC"):
    return f'<span class="tbd">{t(ja, en)}</span>'

def tbdw(ja="要確認", en="TBC"):
    return f'<span class="tbd tbd--w">{t(ja, en)}</span>'

def TEL():   # EN_ONLY: international format
    return t("03-6264-2154", "+81-3-6264-2154")

def FAX():
    return t("03-6264-2354", "+81-3-6264-2354")

def HOURS():
    return t("受付時間 平日10:00〜18:00（土日祝除く）", "Mon–Fri 10:00–18:00 (JST)")

def ADDR(br=False):  # EN_ONLY: Ginza first
    sep = "<br>" if br else " "
    return t(f"〒104-0061{sep}東京都中央区銀座2-12-12 深山ビル2F", f"2-12-12 Ginza, Chuo-ku,{sep}Tokyo 104-0061, Japan (Miyama Bldg. 2F)")

# ------------------------------------------------------------ shared data (built at render time)
def PRODUCTS():
    return [
     dict(id="p1", img="hanajirushi_cl.jpg", cat=t("クレンジング","Cleansing"), sub=t("Deep Cleansing Lotion","花印クレンジングローション"),
          name=t("花印クレンジングローション","Deep Cleansing Lotion"),
          lbls=[(t("特許取得技術","Patented"),"lbl--gold"),(t("ダブル洗顔不要","No double cleanse"),"")],
          short=t("うるおい残してしっかり落ちる、拭き取りタイプのクレンジングウォーター。","Wipe-off cleansing water that removes makeup thoroughly while keeping skin moist."),
          catch=t("うるおい残してしっかり落ちる、拭き取りタイプのクレンジングウォーター","Removes thoroughly, leaves moisture behind — a wipe-off cleansing water"),
          desc=t("特許取得技術の高いクレンジング力で、メイク汚れはもちろん、汗・皮脂・古い角質などコットンで拭き取るだけできれいに落とします。保湿成分ヒアルロン酸・加水分解コラーゲン・アロエベラ葉エキス・ベタイン配合。無香料・無着色・オイルフリー・アルコールフリーなので肌にやさしく低刺激。ダブル洗顔不要です。",
                 "Patented cleansing technology lifts away makeup, sweat, sebum and dead skin cells with just a cotton pad. With moisturising hyaluronic acid, hydrolysed collagen, aloe vera leaf extract and betaine. Fragrance-free, colorant-free, oil-free and alcohol-free — gentle and low-irritation, with no double cleansing needed."),
          tags=t(["無香料","無着色","オイルフリー","アルコールフリー","低刺激"],["Fragrance-free","Colorant-free","Oil-free","Alcohol-free","Low-irritation"]),
          spec=t(["380mL","無香料","無着色","オイルフリー","アルコールフリー"],["380mL","Fragrance-free","Colorant-free","Oil-free","Alcohol-free"]),
          rows=[(t("内容量","Volume"),"380mL"),
                (t("主な保湿成分","Key moisturisers"),t("ヒアルロン酸、加水分解コラーゲン、アロエベラ葉エキス、ベタイン","Hyaluronic acid, hydrolysed collagen, aloe vera leaf extract, betaine")),
                (t("特許","Patent"),t("特許取得技術 ","Patented technology ")+tbd("特許番号","Patent no. TBC"))]),
     dict(id="p2", img="hanajirushi_smfm.jpg", cat=t("フェイスマスク","Face mask"), sub=t("Amino Acid Super Moisture Face Mask","花印スーパーモイスチュアフェイスマスク"),
          name=t("花印スーパーモイスチュアフェイスマスク","Super Moisture Face Mask"),
          lbls=[("6in1","lbl--o"),(t("オールインワン","All-in-one"),"")],
          short=t("肌になじませると美容液に変化する、6つの機能のフェイスマスク。","Six functions in one: a mask that turns into a serum as it melts into skin."),
          catch=t("肌になじませると美容液に変化する、不思議なフェイスマスク","A face mask that transforms into a serum as it melts into skin"),
          desc=t("6つの機能（化粧水・乳液・美容液・クリーム・化粧下地・パック）のフェイスマスクです。保湿成分11種類のアミノ酸、ヒアルロン酸Na、水溶性コラーゲン配合、柔らかなすべすべの肌へ導きます。お手入れの最後に洗い流さないオールインワンジェルとしても使えます。",
                 "Six functions in one — lotion, emulsion, serum, cream, primer and pack. With 11 amino acids, sodium hyaluronate and soluble collagen for soft, smooth skin. Also works as a leave-on all-in-one gel at the end of the routine."),
          tags=t(["6つの機能","洗い流さない","オールインワンジェル"],["6 functions","Leave-on","All-in-one gel"]),
          spec=t(["11種のアミノ酸","ヒアルロン酸Na","水溶性コラーゲン"],["11 amino acids","Sodium hyaluronate","Soluble collagen"]),
          rows=[(t("内容量","Volume"),tbd()),
                (t("主な保湿成分","Key moisturisers"),t("11種類のアミノ酸、ヒアルロン酸Na、水溶性コラーゲン","11 amino acids, sodium hyaluronate, soluble collagen")),
                (t("機能","Functions"),t("化粧水・乳液・美容液・クリーム・化粧下地・パック","Lotion, emulsion, serum, cream, primer, pack"))]),
     dict(id="p3", img="hanajirushi_hsc.jpg", cat=t("化粧水","Lotion"), sub=t("Hatomugi Skin Conditioner","花印ハトムギ化粧水"),
          name=t("花印ハトムギ化粧水","Hatomugi Skin Conditioner"),
          lbls=[(t("大容量","500mL"),""),(t("北海道産ハトムギ","Hokkaido coix seed"),"lbl--o")],
          short=t("北海道産ハトムギ種子エキス高配合。顔にも全身にも使える500mLの大容量。","Rich in Hokkaido coix seed extract. A generous 500mL for face and body."),
          catch=t("厳選された北海道産ハトムギ種子エキス（保湿成分）高配合！500mLの大容量化粧水","Rich in carefully selected coix seed extract from Hokkaido — a generous 500mL lotion"),
          desc=t("大容量なので毎日たっぷり惜しみなく使えます。肌なじみがよく浸透力の高い、みずみずしい使用感の化粧水。保湿成分ハトムギ種子エキス・ヨモギ葉エキス・ヒキオコシ葉/茎エキス・ユズ果実エキス配合。お肌を乾燥から守り、なめらかで明るく透明感のある肌へ導きます。お顔はもちろん、日焼け後のお肌のケアや全身ローションとしても使えます。",
                 "Generous enough to use liberally every day, with a fresh, fast-absorbing feel. With moisturising coix seed, mugwort leaf, isodon and yuzu fruit extracts to protect skin from dryness for a smooth, bright, clear complexion. For the face, after-sun care and as a body lotion."),
          tags=t(["北海道産ハトムギ","無香料","無着色","顔・全身"],["Hokkaido coix seed","Fragrance-free","Colorant-free","Face & body"]),
          spec=t(["500mL","無香料","無着色"],["500mL","Fragrance-free","Colorant-free"]),
          rows=[(t("内容量","Volume"),"500mL"),
                (t("主な保湿成分","Key moisturisers"),t("ハトムギ種子エキス、ヨモギ葉エキス、ヒキオコシ葉/茎エキス、ユズ果実エキス","Coix seed, mugwort leaf, isodon leaf/stem and yuzu fruit extracts")),
                (t("原料産地","Ingredient origin"),t("ハトムギ種子エキス：北海道産","Coix seed extract: Hokkaido, Japan"))]),
     dict(id="p4", img=None, cat=t("クレンジング","Cleansing"), sub=t("Cleansing Oil","花印クレンジングオイル"),
          name=t("花印クレンジングオイル","Cleansing Oil"),
          lbls=[(t("近日掲載","Coming soon"),"lbl--gray")],
          short=t("中国市場の看板アイテム。日本公式サイトへの掲載準備中です。","Our signature item in the China market. Details coming soon."),
          catch=t("中国市場の看板アイテム。日本公式サイトへの掲載を準備中です","Our signature item in the China market — details coming soon"),
          desc=t("製品説明・成分・仕様は確認のうえ掲載します。","Description, ingredients and specifications will be added once confirmed."),
          tags=[], spec=[],
          rows=[(t("製品情報","Product details"),tbd())]),
    ]

def prod_cards(compact=False):
    cards = ''
    for p in PRODUCTS():
        im = f'<img src="{IMG}{p["img"]}" alt="{p["name"]}">' if p["img"] else f'<div class="ph-img">{t("製品画像<br>準備中","Image<br>coming soon")}</div>'
        lb = ''.join(f'<span class="lbl {c}">{x}</span>' for x, c in p["lbls"])
        sp = ''.join(f'<span>{s}</span>' for s in p["spec"]) if p["spec"] else tbd("仕様確認中", "Specs TBC")
        if compact:
            price = ''
        elif EN():   # EN_ONLY: trade buyers see trade pricing, not retail
            price = '<div class="pc-card__p"><b>Trade price</b><span style="font-size:11.5px;font-weight:700;color:var(--rose)">On request</span></div>'
        else:
            price = f'<div class="pc-card__p"><b>希望小売価格</b>{tbd()}</div>'
        b2 = (t("取扱い相談", "Enquire"), f'contact.html?topic=product&amp;item={p["id"]}#form' if V22() else "contact.html") if (compact or EN()) else ("購入する", "#stores")
        cards += f'''<li class="pc-card"><div class="pc-card__img"><div class="pc-card__lbls">{lb}</div>{im}</div>
<div class="pc-card__b"><p class="pc-card__c">{p["cat"]}</p><h3 class="pc-card__n">{p["name"]}</h3><p class="pc-card__d">{p["short"]}</p><div class="pc-card__spec">{sp}</div>
{price}<div class="pc-card__btns"><a href="brand.html#{p["id"]}">{t("詳しく見る","Details")}</a><a href="{b2[1]}">{b2[0]}</a></div></div></li>'''
    return f'<ul class="plist">{cards}</ul>'

def IPS():
    return [
     ("hanajirushi_col_sm.jpg", t("美少女戦士セーラームーン","Sailor Moon"), t("クレンジングローション","Cleansing lotion"), t("中国限定","China only"), "", t("中国市場限定販売","China-exclusive edition")),
     ("hanajirushi_col_lts.jpg", t("リトルツインスターズ","Little Twin Stars"), t("フェイシャルマスク・クレンジング・シャンプー等","Facial masks, cleansing, shampoo, etc."), t("専売品","Exclusive"), "", t("TOKYO LIFESTYLE（東京生活館）専売品","Exclusive to TOKYO LIFESTYLE")),
     ("hanajirushi_col_fb.jpg", t("フルーツバスケット","Fruits Basket"), t("ネイルコレクション","Nail collection"), t("コラボ","Collab"), "lbl--o", None),
     ("hanajirushi_col_yr.jpg", t("ユーリ!!! on ICE","Yuri!!! on ICE"), t("洗顔クリーム","Face wash cream"), t("販売終了","Ended"), "lbl--gray", t("販売終了","Sales ended")),
    ]

def NEWS():
    return [
     ("2026.10.01","exh",t("展示会","Exhibition"),"",t("Cosmoprof Asia 2026（香港）に出展いたします","HANAJIRUSHI to exhibit at Cosmoprof Asia 2026, Hong Kong"), True),
     ("2026.09.25","info",t("お知らせ","Notice"),"lbl--gray",t("コーポレートサイトをリニューアルし、英語版を公開しました","Corporate website renewed — English edition now live"), True),
     ("2026.09.18","biz",t("企業情報","Business"),"lbl--ink",t("海外代理店・パートナー募集ページを公開しました","Partnership programme for overseas distributors launched"), False),
     ("2026.09.10","prod",t("製品情報","Product"),"lbl--o",t("花印クレンジングオイル 日本公式サイト掲載のお知らせ（予定）","Cleansing Oil to join the official product line-up (planned)"), False),
     ("2026.09.01","prod",t("製品情報","Product"),"lbl--o",t("ハトムギ化粧水 製品情報ページを更新しました","Hatomugi Skin Conditioner product information updated"), False),
     ("2022.07.01","info",t("お知らせ","Notice"),"lbl--gray",t("ホームページがリニューアルしました。","Website renewed."), False),
    ]

def news_rows(n=None):
    return ''.join(f'<li data-cat="{c}"><a href="news.html"><span class="d">{d}</span><span class="lbl {cls}">{cl}</span><span class="t">{x}{"<span class=new>NEW</span>" if new else ""}</span></a></li>' for d, c, cl, cls, x, new in NEWS()[:n])

def news_tabs():
    tabs = [("all",t("すべて","All")),("exh",t("展示会","Exhibition")),("prod",t("製品情報","Product")),("biz",t("企業情報","Business")),("info",t("お知らせ","Notice"))]
    return '<div class="tabs">' + ''.join(f'<button class="{"on" if k == "all" else ""}" data-cat="{k}">{v}</button>' for k, v in tabs) + '</div>'

def NEWS_NOTE():
    return f'<p style="font-size:11px;color:var(--ink-3);margin-top:8px">{t("※ 記事タイトルはモックアップ用の仮テキストです。","Headlines are placeholder copy for design review.")}</p>'

def export_list():
    docs = EXPORT_DOCS()
    return '<ul class="models">' + ''.join(f'<li><span><b>{a}</b>{b}</span></li>' for a, b in docs) + '</ul>'

def reg_table():
    regs = REGS()
    sup = REG_SUPPORT()
    rows = ''.join(f'<tr><th>{a}<small>{"" if EN() else e}</small></th><td>{b}</td>' + (f'<td rowspan="{len(regs)}" class="merge">{sup}</td>' if i == 0 else '') + '</tr>' for i, (a, e, b) in enumerate(regs))
    return f'<div class="sx"><table class="dtbl"><thead><tr><th>{t("対象市場","Market")}</th><th>{t("主な手続き・必要資料","Typical requirement")}</th><th>{t("花印の対応","Our support")}</th></tr></thead><tbody>{rows}</tbody></table></div>'

# ------------------------------------------------------------ chrome
def GNAV():
    return [
     ("brand.html", t("ブランド・製品","Brand"), t("Brand","ブランド・製品")),
     ("company.html", t("会社概要","Company"), t("Company","会社概要")),
     ("rd.html", t("研究開発・品質","R&amp;D"), t("R&amp;D","研究開発・品質")),
     ("collaboration.html", t("IPコラボ","Collaboration"), t("Collaboration","IPコラボ")),
     ("global.html", t("海外展開","Global"), t("Global","海外展開")),
     ("partners.html", t("代理店募集","Partners"), t("Partners","代理店募集")),
     ("exhibition.html", t("展示会情報","Exhibition"), t("Exhibition","展示会情報")),
     ("news.html", t("お知らせ","News"), t("News","お知らせ")),
    ]

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS[VERSION]}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ASSETS}css/style.css">{f'<link rel="stylesheet" href="{ASSETS}css/soft.css">' if VERSION in ("2.1", "2.2") else ''}
</head>
<body>'''

def header(fn):
    gn = ''.join(f'<li><a href="{h}" class="{"on" if h == fn else ""}"><b>{j}</b><small>{e}</small></a></li>' for h, j, e in GNAV())
    sp = ''.join(f'<li><a href="{h}"' + (' class="on" aria-current="page"' if h == fn else '') + f'><b>{j}</b><small>{e}</small></a></li>' for h, j, e in GNAV())
    home_on = "on" if fn == "index.html" else ""
    tg = "h1" if fn == "index.html" and not V22() else "p"
    ja_on, en_on = ("on", "") if not EN() else ("", "on")
    tagline = t("化粧品原料・化粧品の研究開発、製造、販売及び輸出入｜花印粧業研究所株式会社（東京・銀座）",
                "Japanese skincare — R&amp;D, manufacturing &amp; export | Hanajirushi Institute of Cosmetics, Inc. (Ginza, Tokyo)")
    # EN_ONLY: no consumer online-store link in the utility bar
    util = t('<li><a href="brand.html#stores">国内オンラインストア</a></li><li><a href="partners.html#faq">よくあるご質問</a></li><li><a href="#">サイトマップ</a></li>',
             '<li><a href="partners.html">Become a distributor</a></li><li><a href="partners.html#faq">FAQ</a></li><li><a href="#">Sitemap</a></li>')
    return f'''<div class="topbar"><div class="wrap">
<{tg} class="tagline">{tagline}</{tg}>
<ul>{util}
<li><span class="lng"><a href="../ja/{fn}" class="{ja_on}">日本語</a><a href="../en/{fn}" class="{en_on}">English</a></span></li></ul></div></div>
<header class="hdr">
<div class="hdr__main"><div class="wrap">
<a class="logo" href="index.html"><img class="logo__img" src="{IMG}logo.svg" alt="花印 HANAJIRUSHI" width="150" height="40"><span class="logo__co">{t("花印粧業研究所株式会社","Hanajirushi Institute of Cosmetics, Inc.")}</span></a>
<div class="hdr__r">
<form class="srch" role="search"><input type="search" placeholder="{t("サイト内検索","Search this site")}"><button type="submit">{t("検索","Search")}</button></form>
<div class="tel"><b>{I["tel"]}{TEL()}</b><small>{HOURS()}</small></div>
<a class="hbtn hbtn--o" href="partners.html">{I["hand"]}{t("代理店募集","Distributors")}</a>
<a class="hbtn hbtn--f" href="contact.html">{I["mail"]}{t("お問い合わせ","Contact")}</a>
<button class="burger" aria-label="{t("メニュー","Menu")}" aria-expanded="false" aria-controls="spnav"><i></i><i></i><i></i><span class="m">MENU</span><span class="c">CLOSE</span></button>
</div></div></div>
<nav class="gnav"><div class="wrap"><ul><li class="home"><a class="home {home_on}" href="index.html" aria-label="{t("ホーム","Home")}">{I["home"]}</a></li>{gn}</ul></div></nav>
<div class="spnav" id="spnav" aria-hidden="true"><div class="spnav__in">
<p class="spnav__lbl">{t("メニュー","Menu")}<span>MENU</span></p>
<ul class="spnav__grid">{sp}</ul>
<div class="spnav__cta"><a class="btn btn--s" href="partners.html">{I["hand"]}{t("代理店募集","Distributors")}</a><a class="btn btn--s btn--o" href="contact.html">{I["mail"]}{t("お問い合わせ","Contact us")}</a></div>
<a class="spnav__tel" href="tel:+81362642154"><span class="ic">{I["tel"]}</span><span><small>{t("お電話でのお問い合わせ","Call our Tokyo office")}</small><b>{TEL()}</b><small>{HOURS()}</small></span></a>
<div class="spnav__lang" role="group" aria-label="Language"><a class="{ja_on}" href="../ja/{fn}">日本語</a><a class="{en_on}" href="../en/{fn}">English</a></div>
</div></div>
</header>
<main>'''

def footer(fn):
    cols = [
     (t("ブランド・製品","Brand &amp; products"), [("brand.html",t("ブランドについて","About the brand")),("brand.html#p1",t("クレンジングローション","Deep Cleansing Lotion")),("brand.html#p2",t("フェイスマスク","Super Moisture Face Mask")),("brand.html#p3",t("ハトムギ化粧水","Hatomugi Skin Conditioner")),("collaboration.html",t("IPコラボレーション","IP collaborations"))]),
     (t("企業情報","Company"), [("company.html",t("会社概要","Company profile")),("company.html#history",t("沿革","History")),("rd.html",t("研究開発・品質管理","R&amp;D and quality")),("company.html#access",t("アクセス","Access")),("news.html",t("お知らせ","News"))]),
     (t("お取引について","Business"), [("partners.html",t("海外代理店・パートナー募集","Partnership programme")),("partners.html#terms",t("取引条件・輸出書類","Trade terms &amp; export documents")),("exhibition.html",t("展示会情報","Exhibitions")),("contact.html",t("お問い合わせ","Contact")),("#",t("プライバシーポリシー","Privacy policy"))]),
    ]
    cg = ''.join(f'<div><h4>{h}</h4><ul>' + ''.join(f'<li><a href="{u}">{x}</a></li>' for u, x in items) + '</ul></div>' for h, items in cols)
    cband = '' if fn == "contact.html" else f'''<section class="cband"><div class="wrap">
<h2>{t("お取引・代理店に関するご相談はお気軽にどうぞ","Interested in distributing HANAJIRUSHI?")}<small>{t("製品・OEM/ODM・海外展開のご相談も承ります。3営業日以内にご返信します。","Product, OEM/ODM and market-entry enquiries welcome. We reply within 3 business days.")}</small></h2>
<div class="t"><small>{t("お電話でのお問い合わせ","Call our Tokyo office")}</small><b>{I["tel"]}{TEL()}</b><small>{t("受付時間 平日10:00〜18:00","Mon–Fri 10:00–18:00 (JST)")}</small></div>
<div class="bt">{(cta("business","ビジネスについて相談する","Discuss your business","btn--w") + cta("partner","販売パートナーについて相談する","Become a sales partner","btn--ol")) if V22() else f'<a class="btn btn--w" href="contact.html">{t("メールでのお問い合わせ","Send an enquiry")}</a><a class="btn btn--ol" href="contact.html">{t("代理店申込フォーム","Apply as a distributor")}</a>'}</div>
</div></section>'''
    other = "en" if not EN() else "ja"
    spbar = t(f'<a href="tel:0362642154">{I["tel"]}電話する</a><a href="partners.html">{I["hand"]}代理店募集</a><a href="contact.html">{I["mail"]}お問い合わせ</a>',
              f'<a href="contact.html#form">{I["chat"]}WhatsApp</a><a href="partners.html">{I["hand"]}Distributors</a><a href="contact.html">{I["mail"]}Contact</a>')
    return f'''</main>
{cband}
<footer class="ftr"><div class="wrap ftr__g">
<div class="ftr__co"><a class="logo" href="index.html"><img class="logo__img" src="{IMG}logo.svg" alt="花印 HANAJIRUSHI" width="150" height="40"><span class="logo__co">{t("花印粧業研究所株式会社","Hanajirushi Institute of Cosmetics, Inc.")}</span></a>
<p>{ADDR(True)}</p><p class="tl">TEL {TEL()}</p><p style="margin-top:0">FAX {FAX()}</p></div>
{cg}
</div>
<div class="ftr__btm"><div class="wrap"><p>© 2026 Hanajirushi Institute of Cosmetics, Inc. All rights reserved.</p><div class="links"><a href="#">{t("プライバシーポリシー","Privacy policy")}</a><a href="#">{t("サイトマップ","Sitemap")}</a><a href="../{other}/{fn}">{t("English","日本語")}</a></div></div></div>
</footer>
<div class="sidetab"><a href="partners.html">{I["hand"]}{t("代理店募集","Distributors")}</a><a class="ink" href="exhibition.html#booking">{I["cal"]}{t("商談予約","Book a meeting")}</a></div>
<button class="totop" aria-label="{t("ページトップへ","Back to top")}">{I["up"]}TOP</button>
<div class="spbar">{spbar}</div>
<script src="{ASSETS}js/main.js"></script>
</body></html>'''

def page(fn, title, desc, body):
    if fn == "index.html":
        full = t("花印 HANAJIRUSHI 公式サイト｜花印粧業研究所株式会社", "HANAJIRUSHI | Japanese Skincare from Ginza, Tokyo")
    else:
        full = t(f"{title}｜花印 HANAJIRUSHI 公式サイト", f"{title} | HANAJIRUSHI — Japanese Skincare, Ginza Tokyo")
    return head(full, desc) + header(fn) + body + footer(fn)

def lower(label, ja, en, sub_ja=None, sub_en=None, bg=None, anchors=None):
    """Lower-page header band + breadcrumb (+ optional in-page anchor links).
    JA: EN label over JA title. EN: kanji label over EN title."""
    style = f' style="--bg:url(../img/{bg})"' if bg else ''  # resolved relative to style.css
    cls = "phd" if bg else "phd phd--plain"
    sub = t(sub_ja, sub_en)
    p = f'<p>{sub}</p>' if sub else ''
    title = t(ja, en)
    anc = ''
    if anchors:
        anc = '<div class="wrap"><nav class="anc" aria-label="' + t("ページ内リンク", "On this page") + '">' + ''.join(f'<a href="#{i}">{x}</a>' for i, x in anchors) + '</nav></div>'
    return f'''<section class="{cls}"{style}><div class="wrap"><p class="en">{flower()}{t(label, ja)}</p><h1>{title}</h1>{p}</div></section>
<nav class="bc" aria-label="breadcrumb"><div class="wrap"><a href="index.html">{I["home"]}{t("ホーム","Home")}</a><span>{title}</span></div></nav>{anc}'''

def A(i, ja, en):
    return (i, t(ja, en))

# ============================================================ TOP
def slide(href, label, head, sub, media, tags=(), stamp=None, go=None, theme="light"):
    """One carousel slide. Every slide shares this layout: label, headline, sub line, tags and button on
    the left; media (photo | trio | grid) on the right; optional stamp top-right. Only content differs."""
    kind, imgs = media
    tg = f'<ul class="sl__tags">{"".join(f"<li>{x}</li>" for x in tags)}</ul>' if tags else ''
    st_ = f'<span class="sl__stamp">{stamp}</span>' if stamp else ''
    btn = f'<span class="sl__go">{go or t("詳しく見る","Learn more")}<i></i></span>'
    pics = ''.join(f'<img src="{IMG}{im}" alt="">' for im in imgs)
    return (f'<div class="slide"><a href="{href}" class="sl sl--{theme}">'
            f'<div class="sl__txt"><span class="sl__pill">{label}</span><p class="sl__h">{head}</p>'
            f'<p class="sl__s">{sub}</p>{tg}{btn}</div>'
            f'<div class="sl__media sl__media--{kind}">{pics}</div>{st_}</a></div>')

def kv():
    slides = [
     slide("exhibition.html", "INFORMATION",
           t('<span class="en">Cosmoprof Asia 2026</span>に出展します', '<span class="en">Cosmoprof Asia 2026</span>See you in Hong Kong'),
           t("2026年11月　香港コンベンション＆エキシビションセンター", "November 2026 · Hong Kong Convention &amp; Exhibition Centre"),
           ("trio", ["hanajirushi_cl.jpg", "hanajirushi_hsc.jpg", "hanajirushi_smfm.jpg"]),
           tags=[t("ブース番号 ", "Booth ") + t("確定待ち", "TBC")],
           stamp=t("出展<br>決定", "出展<small>EXHIBITING</small>"),
           go=t("商談を予約する", "Book a meeting"), theme="rose"),
     slide("brand.html#p3", t("ロングセラー", "LONG-SELLER"),
           t("花印<br><em>ハトムギ化粧水</em>", "Hatomugi<br><em>Skin Conditioner</em>"),
           t("北海道産ハトムギ種子エキス高配合。顔にも全身にも使える500mLの大容量。", "Rich in Hokkaido coix seed extract. A generous 500mL for face and body."),
           ("photo", ["hanajirushi_hsc.jpg"]),
           tags=t(["500mL", "無香料", "無着色", "顔・全身"], ["500mL", "Fragrance-free", "Colorant-free", "Face &amp; body"]),
           stamp=t("日本製", "日本製<small>MADE IN JAPAN</small>")),
     slide("brand.html#p1", t("クレンジング", "CLEANSING"),
           t("うるおい残して、<br><em>しっかり落ちる。</em>", "Removes makeup.<br><em>Keeps moisture.</em>"),
           t("花印クレンジングローション 380mL。拭き取るだけ、ダブル洗顔不要。", "Deep Cleansing Lotion 380mL. Wipe off — no double cleansing."),
           ("photo", ["hanajirushi_cl.jpg"]),
           tags=t(["無香料", "無着色", "オイルフリー", "アルコールフリー"], ["Fragrance-free", "Colorant-free", "Oil-free", "Alcohol-free"]),
           stamp=t("特許<br>取得技術", "特許<small>PATENTED</small>")),
     slide("collaboration.html", "COLLABORATION",
           t("人気IPとの<br><em>正規ライセンス</em>商品", "<em>Officially licensed</em><br>Japanese IP"),
           t("美少女戦士セーラームーン／リトルツインスターズ／フルーツバスケット／ユーリ!!! on ICE", "Sailor Moon / Little Twin Stars / Fruits Basket / Yuri!!! on ICE"),
           ("grid", ["hanajirushi_col_sm.jpg", "hanajirushi_col_lts.jpg", "hanajirushi_col_fb.jpg", "hanajirushi_col_yr.jpg"]),
           stamp=t("正規<br>ライセンス", "正規<small>LICENSED</small>"),
           go=t("コラボを見る", "See collaborations")),
     slide("partners.html", "FOR PARTNERS",
           t("海外代理店・<br><em>パートナー募集中</em>", "Now recruiting<br><em>distributors</em>"),
           t("世界12ヵ国で販売実績。輸出書類・各国登録も技術支援します。", "Sold in 12 countries. Full export documents and registration support."),
           ("photo", ["h_campany_lab.jpg"]),
           tags=t(["独占代理店", "販売代理店", "越境EC", "OEM/ODM"], ["Exclusive", "Reseller", "Cross-border EC", "OEM/ODM"]),
           stamp=t("募集中", "募集中<small>NOW OPEN</small>"),
           go=t("募集要項を見る", "Programme details")),
    ]
    return f'''<section class="kv" aria-label="{t("ピックアップ","Highlights")}">
<div class="kv__track">{"".join(slides)}</div>
<button class="kv__btn kv__btn--p" aria-label="{t("前へ","Previous")}">{I["prev"]}</button><button class="kv__btn kv__btn--n" aria-label="{t("次へ","Next")}">{I["next"]}</button>
<div class="kv__ui"><div class="kv__dots"></div><button class="kv__pause" aria-label="{t("一時停止","Pause")}" data-p='{I["pause"]}' data-r='{I["play"]}'>{I["pause"]}</button></div>
</section>'''

def bnrs():
    items = [
     ("company.html","h_campany_bldg.jpg","Company",t("銀座本社・会社概要","Our Ginza head office"),t("2015年創業","Founded 2015")),
     ("exhibition.html","hanajirushi_cl.jpg","Exhibition","Cosmoprof Asia 2026",t("ブースでの商談予約受付中","Book a meeting at our booth")),
     ("rd.html","h_campany_ent.jpg","R&amp;D",t("研究開発・品質への取り組み","R&amp;D and quality"),t("銀座の自社研究室","Our own lab in Ginza")),
     ("global.html","world_map_brand.png","Global",t("世界12ヵ国で販売","Sold in 12 countries"),t("海外展開・主要市場","Markets &amp; channels")),
    ]
    li = ''.join(f'<li><a href="{h}"><img src="{IMG}{im}" alt=""><span><span class="k">{k}</span><b>{x}</b><small>{s}</small></span></a></li>' for h, im, k, x, s in items)
    return f'<section class="bnrs"><div class="wrap"><ul>{li}</ul></div></section>'

def news_pick():
    return f'''<section class="sec--s"><div class="wrap np">
<div>{sth("お知らせ","News","news.html")}
{news_tabs()}
<ul class="nlist">{news_rows(5)}</ul>
{NEWS_NOTE()}</div>
<aside class="pick"><div class="pick__h">{t("展示会出展のお知らせ","Meet us in Hong Kong")}<span class="en">EXHIBITION</span></div>
<div class="pick__b"><h3>Cosmoprof Asia 2026<small>{t("アジア最大級の美容見本市に出展します","Asia's leading beauty trade show")}</small></h3>
<dl><dt>{t("会期","Dates")}</dt><dd>{t("2026年11月","November 2026")} {tbd("日程確定待ち","TBC")}</dd><dt>{t("会場","Venue")}</dt><dd>{t("香港コンベンション＆エキシビションセンター","Hong Kong Convention &amp; Exhibition Centre")}</dd><dt>{t("ブース","Booth")}</dt><dd>{tbd("確定待ち","TBC")}</dd></dl>
<a class="btn btn--s" href="exhibition.html#booking">{t("商談を予約する","Book a meeting")}</a></div>
</aside>
</div></section>'''

def REASONS():
    return [
     (t("創業","Since"),"2015" + t("<u>年</u>",""),"",t("東京・銀座で創業。研究開発型のスキンケアメーカー","Founded in Ginza, Tokyo as an R&amp;D-led skincare maker")),
     (t("本社","Tokyo HQ"),t("銀座","Ginza"),"s",t("東京・銀座二丁目に本社・研究室・ショールーム","Head office, lab and showroom in Ginza 2-chome")),
     (t("世界","Sold in"),"12" + t("<u>ヵ国</u>","<u>countries</u>"),"",t("日本国内のほか世界12ヵ国で販売","Sold in Japan and 12 countries worldwide")),
     (t("クレンジング","Cleansing"),t("特許技術","Patented"),"s",t("クレンジングローションに特許取得技術を採用","Patented technology in our Deep Cleansing Lotion")),
     (t("処方開発","Formulation"),t("自社研究室","Own lab"),"s",t("原料レベルから自社で処方を開発","Formulated in-house from the raw-material level")),
     (t("IPコラボ","Japanese IP"),t("正規<u>ライセンス</u>","Licensed"),"s",t("日本の人気IPと正規ライセンス契約","Official licences with leading Japanese IP")),
    ]

def reasons():
    lau = laurel()
    li = ''.join(f'<li class="badge"><div class="badge__m">{lau}<div class="c"><small>{a}</small><b class="{c}">{b}</b></div></div><p>{p}</p></li>' for a, b, c, p in REASONS())
    return f'''<section class="sec sec--rose"><div class="wrap">
{st("REASONS","花印が選ばれる理由","Why partners choose HANAJIRUSHI")}
<ul class="badges">{li}</ul>
<p class="badge-note">{t("※ 特許番号・販売国一覧は確認のうえ掲載します","Patent number and country list to be published once confirmed")} {tbd()}</p>
</div></section>'''

def products():
    return f'''<section class="sec"><div class="wrap">
{stl("PRODUCTS","製品ラインナップ","Product line-up","無香料・無着色・オイルフリー・アルコールフリー。敏感な肌にもやさしい、日本製のスキンケア。","Fragrance-free, colorant-free, oil-free, alcohol-free. Gentle skincare, made in Japan.")}
<div class="ptabs"><a class="on" href="brand.html">{t("すべて","All")}</a><a href="brand.html#p1">{t("クレンジング","Cleansing")}</a><a href="brand.html#p3">{t("化粧水","Lotion")}</a><a href="brand.html#p2">{t("フェイスマスク","Face mask")}</a><a href="collaboration.html">{t("IPコラボ商品","Licensed IP")}</a></div>
{prod_cards()}
<div class="btn-row"><a class="btn" href="brand.html">{t("製品一覧を見る","All products")}</a>{cta("product","商品について相談する","Ask about our products","btn--o") if V22() else ""}</div>
</div></section>'''


def cmt_cards(items, tag="POINT"):
    li = ''.join(f'''<li><div class="cmt__img"><img src="{IMG}{im}" alt=""><span class="cmt__n">{tag}<b>{n}</b></span></div>
<div class="cmt__b"><h3>{h}</h3><p>{p}</p><div class="chk">{"".join(f"<span>{c}</span>" for c in cs)}</div>{f'<a class="more" href="{u}">{t("詳しく見る","Learn more")}</a>' if u else ''}</div></li>''' for im, n, h, p, cs, u in items)
    return f'<ul class="cmt">{li}</ul>'

def COMMIT():
    return [
     ("h_campany_lab.jpg","01",t("銀座の<em>自社研究室</em>で処方開発","Formulated in <em>our own lab</em> in Ginza"),
      t("原料の選定から処方開発まで、東京・銀座本社の研究室で行っています。自社で研究開発・製造・輸出入を担うため、仕様変更やOEM/ODMにも柔軟に対応します。","From ingredient selection to formulation, everything is developed in the laboratory at our Ginza head office. With R&amp;D, manufacturing and export in-house, we can adapt specifications and support OEM/ODM."),
      t(["研究開発","製造","輸出入"],["R&amp;D","Manufacturing","Export"]),"rd.html"),
     ("hanajirushi_hsc.jpg","02",t("<em>日本製</em>・国産原料へのこだわり","<em>Made in Japan</em>, with Japanese ingredients"),
      t("北海道産ハトムギ種子エキスなど、国産原料を積極的に採用。日本ならではの上質で誠実なものづくりが、海外でも評価されています。","We actively use Japanese ingredients such as coix seed extract from Hokkaido. The quality and honesty of Japanese manufacturing is recognised worldwide."),
      t(["メイド・イン・ジャパン","北海道産"],["Made in Japan","Hokkaido"]),"rd.html"),
     ("hanajirushi_cl.jpg","03",t("肌にやさしい<em>低刺激処方</em>","<em>Gentle</em>, low-irritation formulas"),
      t("無香料・無着色・オイルフリー・アルコールフリーを基本に、敏感な肌の方にも使いやすい処方を追求しています。","Fragrance-free, colorant-free, oil-free and alcohol-free as standard — formulas designed to suit sensitive skin."),
      t(["無香料","無着色","オイルフリー","アルコールフリー"],["Fragrance-free","Colorant-free","Oil-free","Alcohol-free"]),"brand.html"),
    ]

def commitment():
    return f'''<section class="sec sec--gray"><div class="wrap">{st("COMMITMENT","花印のこだわり","Our commitment")}{cmt_cards(COMMIT())}</div></section>'''

def ip_grid():
    li = ''.join(f'<li><a href="collaboration.html"><div class="i"><img src="{IMG}{im}" alt="{n}"><span class="lbl {c}">{l}</span></div><div class="b"><b>{n}</b><small>{s}</small></div></a></li>' for im, n, s, l, c, _ in IPS())
    return f'<ul class="ipg">{li}</ul>'

def IPNOTE():
    return f'<p class="ipnote">{I["medal"]}{t("すべてのコラボレーション商品は正規ライセンス品です。ライセンス証明書類はお取引先にご提示できます。","All collaboration products are officially licensed. Proof of licence is available to trade partners.")}</p>'

def ip():
    return f'''<section class="sec{"" if V22() else " sec--rose"}"><div class="wrap">
{stl("COLLABORATION","IPコラボレーション","Licensed IP collaborations","日本の人気IPと正規ライセンスを結び、処方からパッケージ、ギフトセットまで一貫して企画・開発しています。","Official licences with leading Japanese IP — with full co-development from formula to packaging and gift sets.")}
{ip_grid()}
{IPNOTE()}
<div class="btn-row"><a class="btn" href="collaboration.html">{t("コラボレーション一覧","All collaborations")}</a>{cta("oem","OEM・共同開発について相談する","Discuss OEM &amp; co-development","btn--o") if V22() else f'<a class="btn btn--o" href="contact.html">{t("コラボのご相談","Discuss a collaboration")}</a>'}</div>
</div></section>'''

def MODELS_MINI():
    return t('<li><span><b>独占代理店</b>国・地域ごとの総代理店</span></li><li><span><b>販売代理店</b>中小規模の輸入業者様</span></li><li><span><b>モダントレード</b>ドラッグストア・専門店</span></li><li><span><b>越境EC・OEM/ODM</b>EC事業者・自社ブランド</span></li>',
             '<li><span><b>Exclusive distributor</b>One partner per country / region</span></li><li><span><b>Authorised reseller</b>Small &amp; mid-size importers</span></li><li><span><b>Modern trade</b>Drugstores &amp; beauty retailers</span></li><li><span><b>Cross-border EC · OEM/ODM</b>Online sellers &amp; private label</span></li>')

def global_partners():
    docs = t(["INCI成分表","COA","MSDS/SDS","自由販売証明書","原産地証明書","多言語ラベル"],["INCI list","COA","MSDS/SDS","Free Sale Certificate","Certificate of Origin","Multilingual labels"])
    steps = t(["フォーム<br>申込","オンライン<br>面談","サンプル<br>評価","契約・<br>初回発注"],["Apply<br>online","Online<br>meeting","Sample<br>review","Contract &amp;<br>first order"])
    stats = f'''<ul class="gstats">
<li><small>{t("販売国","Countries")}</small><b>12<u>{t("ヵ国","")}</u></b></li>
<li><small>{t("取引実績","Trade deals")}</small><b class="na">—<u>{t("件","")}</u></b>{tbd()}</li>
<li><small>{t("海外パートナー","Overseas partners")}</small><b class="na">—<u>{t("社","")}</u></b>{tbd()}</li>
<li><small>{t("創業","Since")}</small><b>2015<u>{t("年","")}</u></b></li></ul>
<p class="gstats__lead">{t("海外市場での実績をもとに、<em>新しい販売代理店・ビジネスパートナー</em>を募集しています。","Building on our track record overseas, we are now recruiting <em>new distributors and business partners</em>.")}</p>''' if V22() else ""
    return f'''<section class="sec{" sec--gray" if V22() else ""}"><div class="wrap">
{st("GLOBAL &amp; PARTNERS","海外展開と代理店募集","Global network &amp; partnerships")}
{stats}<div class="gp">
<div class="box"><div class="box__h"><h3>{I["globe"]}{t("海外展開","Global network")}</h3><span class="en">{t("GLOBAL NETWORK","海外展開")}</span></div>
<div class="box__b"><div class="gmap"><img src="{IMG}world_map_brand.png" alt=""><div class="big"><small>{t("世界","Sold in")}</small><b>12<u>{t("ヵ国","")}</u></b><small>{t("で販売","countries")}</small></div></div>
<div class="rg"><div><b>{t("東アジア","East Asia")}</b>{t("日本・中国を中心にEC・ドラッグストア","Japan &amp; China: e-commerce, drugstores")}</div><div><b>{t("東南アジア","SE Asia")}</b>{t("越境EC・モダントレード","Cross-border EC, modern trade")}</div><div><b>{t("北米","North America")}</b>{t("ECを中心に展開","E-commerce led")}</div></div>
<p style="font-size:12px;color:var(--ink-2)">{t("中国では天猫・抖音・屈臣氏（Watsons）等で展開。販売国一覧","In China via Tmall, Douyin and Watsons. Country list")} {tbd()}</p>
<div class="btn-row"><a class="btn btn--s btn--ink" href="global.html">{t("海外展開を見る","Global network")}</a></div></div></div>
<div class="box recruit"><div class="box__h box__h--rose"><h3>{I["hand"]}{t("海外代理店・パートナー募集","Partnership programme")}</h3><span class="en">{t("FOR PARTNERS","代理店募集")}</span></div>
<span class="stamp2">{t("募集中","募集中<small>NOW OPEN</small>")}</span>
<div class="box__b"><p class="lead">{t("市場と規模に合わせた<em>5つの協業モデル</em>をご用意しています。","<em>Five cooperation models</em> to fit your market and scale.")}</p>
<ul class="models">{MODELS_MINI()}</ul>
<p class="docs-h">{t("対応可能な輸出書類","Export documents we provide")}</p>
<div class="docs">{"".join(f"<span>{d}</span>" for d in docs)}</div>
<p class="docs-h">{t("お取引開始までの流れ","How to start")}</p>
<ol class="flowm">{"".join(f"<li>{s}</li>" for s in steps)}</ol>
<div class="btn-row{" btn-row--stack" if V22() else ""}"><a class="btn btn--s" href="partners.html">{t("募集要項を見る","Programme details")}</a>{cta("partner","販売パートナーについて相談する","Become a sales partner","btn--s btn--o") if V22() else f'<a class="btn btn--s btn--o" href="contact.html">{t("申込フォーム","Apply now")}</a>'}</div></div></div>
</div></div></section>'''

def company_rows(full=False):
    """Company profile rows. EN_ONLY: capital and banks are not shown in English."""
    rows = [(t("社名","Company name"), t("花印粧業研究所株式会社","Hanajirushi Institute of Cosmetics, Inc.") + (f'<br><small style="color:var(--ink-3)">{t("Hanajirushi Institute of Cosmetics, Inc.","花印粧業研究所株式会社")}</small>' if full else ''))]
    rows += [(t("創業","Founded"), t("2015年1月28日","28 January 2015")),
             (t("本社所在地" if full else "本社","Head office"), ADDR(True))]
    if full:
        rows.append(("TEL / FAX", f"TEL {TEL()} ／ FAX {FAX()}"))
    rows.append((t("代表者","Representative"), t("代表取締役 ","Representative Director ") + tbd("氏名","Name TBC")))
    if not EN():
        rows.append(("資本金", "1,000万円"))
    rows.append((t("事業内容","Business"), t("化粧品の原料、化粧品、健康食品の研究開発、製造、販売及び輸出入","R&amp;D, manufacturing, sales, import and export of cosmetic raw materials, cosmetics and health foods")))
    if full:
        rows.append((t("販売地域","Markets"), t("日本国内および世界12ヵ国 ","Japan and 12 countries across East Asia, Southeast Asia and North America ") + tbd("国名一覧","Country list TBC")))
    if not EN():
        rows.append(("取引銀行", "三井住友銀行、三菱UFJ銀行、みずほ銀行"))
    if full:
        rows.append((t("法人番号","Corporate number"), tbd()))
    return ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in rows)

def OFFICE_PHOTOS():
    return [("h_campany_ent.jpg",t("エントランス","Entrance")),("h_campany_lab.jpg",t("研究室","Laboratory")),("h_campany_sr.jpg",t("ショールーム","Showroom")),("h_campany_dr.jpg",t("応接室","Meeting room"))]

def company_mini():
    pin = I["pin"].replace("<svg", '<svg style="width:14px;height:14px;display:inline;vertical-align:-2px;color:var(--rose)"')
    return f'''<section class="sec{"" if V22() else " sec--gray"}"><div class="wrap">
{stl("COMPANY","会社情報","Company profile")}
<div class="co">
<div class="co__ph"><img src="{IMG}h_campany_bldg.jpg" alt=""></div>
<div><table class="otbl">{company_rows()}</table>
<div class="btn-row"><a class="btn btn--s" href="company.html">{t("会社概要","Company profile")}</a><a class="btn btn--s btn--o" href="company.html#access">{t("アクセス","Access")}</a></div></div>
<div><ul class="thumbs">{"".join(f'<li><img src="{IMG}{im}" alt=""><span>{x}</span></li>' for im, x in OFFICE_PHOTOS())}</ul>
<p style="font-size:12px;color:var(--ink-2);margin-top:10px">{pin} {t("東京メトロ 銀座一丁目駅・銀座駅より徒歩圏","Walking distance from Ginza-itchome and Ginza stations")}</p></div>
</div></div></section>'''

def stores():
    """JA: domestic store logos. EN_ONLY: no consumer store links — a 'find a distributor' panel instead."""
    if EN():
        return f'''<section class="sec--s" id="stores"><div class="wrap"><div class="wtb"><span class="ic">{I["globe"]}</span>
<div><h3>Looking for HANAJIRUSHI in your country?</h3><p>We are building our distributor network. Contact us to find a local partner — or to become one.</p></div>
<a class="btn btn--s" href="partners.html">Find / become a distributor</a></div></div></section>'''
    s = [("rakuten.svg","楽天市場 公式ショップ"),("amazon.png","Amazon 公式ストア"),("yahoo.svg","Yahoo!ショッピング"),("qoo10.png","Qoo10 公式ショップ")]
    li = ''.join(f'<a href="#"><img src="{IMG}{im}" alt="{x}"><small>{x}</small></a>' for im, x in s)
    return f'''<section class="sec--s" id="stores"><div class="wrap"><p class="stores-h">国内公式オンラインストア</p><div class="stores">{li}</div></div></section>'''

def fv():
    """v2.2 first view: who we are and how to do business with us, before any product."""
    trust = FV_TRUST()
    return f'''<section class="fv" style="--bg:url(../img/h_brand_top_p.jpg)"><div class="wrap fv__in">
<p class="fv__lbl">JAPANESE SKINCARE MAKER · GINZA, TOKYO</p>
<h1 class="fv__h">{FV_HEAD()}</h1>
<p class="fv__p">{FV_LEAD1()}{tbd("製造地 要確認","Manufacturing site TBC")}<br>{FV_LEAD2()}</p>
<div class="fv__cta"><a class="btn" href="partners.html">{t("代理店・パートナー募集","Become a partner")}</a><a class="btn btn--o" href="brand.html">{t("製品を見る","View products")}</a></div>
<ul class="fv__trust">{"".join(f"<li><small>{a}</small><b>{v}</b></li>" for a, v in trust)}</ul>
</div></section>'''

def japan4():
    items = JAPAN4()
    li = "".join(f'<li><span class="j4__n" aria-hidden="true">{i+1:02d}</span><span class="j4__ic">{I[ic]}</span><h3>{h}</h3><p>{p}</p>{note}</li>' for i, (ic, h, p, note) in enumerate(items))
    return f'''<section class="sec sec--gray"><div class="wrap">
{st("MADE IN JAPAN","「日本製」4つの強み","Made in Japan — four strengths","「日本製」というラベルだけでなく、その中身をお伝えします。","Not just a label — what “Made in Japan” means for your business.")}
<ol class="j4">{li}</ol>
<div class="btn-row"><a class="btn btn--o" href="rd.html">{t("研究開発・品質管理を見る","R&amp;D and quality")}</a></div>
</div></section>'''

def why_partners():
    models = WHY_MODELS()
    items = WHY()
    li = "".join(f'<li><span class="why__n">{i+1:02d}</span><div><h3>{h}</h3>{f"<p>{p}</p>" if p else ""}{x}</div></li>' for i, (h, p, x) in enumerate(items))
    return f'''<section class="sec sec--rose"><div class="wrap">
{stl("WHY HANAJIRUSHI","ビジネスパートナーに選ばれる理由","Why business partners choose us","良い商品であることに加えて、花印と取引する理由をお伝えします。","Beyond good products — why companies choose to do business with us.")}
<ul class="why">{li}</ul>
<div class="btn-row">{cta("partner","販売パートナーについて相談する","Become a sales partner")}{cta("business","ビジネスについて相談する","Discuss your business","btn--o")}</div>
</div></section>'''

def p_home():
    if V22():
        body = fv() + kv() + news_pick() + japan4() + products() + why_partners() + ip() + global_partners() + company_mini() + stores()
    else:
        body = kv() + bnrs() + news_pick() + reasons() + products() + commitment() + ip() + global_partners() + company_mini() + stores()
    return page("index.html", "", t("花印粧業研究所株式会社の公式サイト。東京・銀座の自社研究室で開発する、無香料・無着色の日本製スキンケア。世界12ヵ国で販売。海外代理店・パートナー募集中。",
                                    "HANAJIRUSHI: clean, gentle Japanese skincare formulated in our own laboratory in Ginza, Tokyo. Sold in 12 countries. Distributor enquiries welcome."), body)

# ============================================================ BRAND
def BRAND_TEXT():
    """Brand story, two paragraphs (shared with the premium build)."""
    return (t("人の肌を想い、ひとりの悩みを見つめ、ひとつしかないキレイを、メイド・イン・ジャパンのスキンケアの力で届けていく。",
              "We look closely at each person's skin and each individual concern, and deliver a beauty that is theirs alone — with the power of Japanese-made skincare."),
            t("「花印」の名には、ひとりひとりの肌に咲く花の印という想いを込めています。日本ならではの上質で誠実なものづくりが認められ、花印は国内はもとより世界12ヵ国で販売されています。",
              "The name HANAJIRUSHI, “flower seal”, stands for the mark of a flower blooming on each person's skin. Recognised for the quality and honesty of Japanese manufacturing, our products are sold in Japan and 12 countries worldwide."))

def FREE_FROM():
    return t([("無香料","FRAGRANCE FREE"),("無着色","COLORANT FREE"),("オイル<br>フリー","OIL FREE"),("アルコール<br>フリー","ALCOHOL FREE"),("日本製","MADE IN JAPAN")],
             [("Fragrance<br>free","無香料"),("Colorant<br>free","無着色"),("Oil<br>free","オイルフリー"),("Alcohol<br>free","アルコールフリー"),("Made in<br>Japan","日本製")])

def p_brand():
    hd = lower("BRAND","ブランド・製品","Brand &amp; Products","人の肌を想い、ひとりの悩みを見つめる、日本製のスキンケア。","Gentle, honest skincare — formulated and made in Japan.","h_brand_top_p.jpg",
               [A("philosophy","ブランド理念","Philosophy"),A("lineup","製品ラインナップ","Line-up"),A("p1","クレンジング","Cleansing"),A("p2","フェイスマスク","Face Mask"),A("p3","ハトムギ化粧水","Hatomugi"),A("stores","国内でのご購入","Where to buy")])
    # EN_ONLY: brand line is re-written for English, not translated; the Japanese slogan stays as a small accent.
    catch = t('<p class="catch mincho">ひとりに、ひとつの、<br><em>キレイ</em>を咲かせる。</p>',
              '<p class="catch">Clean formula.<br><em>Gentle by design.</em><br>Made in Japan.</p><p class="mincho" style="color:var(--rose);font-size:15px;margin-top:6px">ひとりに、ひとつの、キレイを咲かせる。</p>')
    p1, p2 = BRAND_TEXT()
    body1 = f'<p class="mt2">{p1}</p><p>{p2}</p>'
    free = FREE_FROM()
    phil = f'''<section class="sec" id="philosophy"><div class="wrap">
{st("PHILOSOPHY","ブランド理念","Brand philosophy")}
<div class="md"><img class="ph" src="{IMG}h_hanajirushi_top-1.jpg" alt="">
<div class="txt">{catch}{body1}</div></div>
<ul class="freec mt3">{"".join(f"<li>{a}<small>{b}</small></li>" for a, b in free)}</ul>
</div></section>'''
    lineup = f'''<section class="sec sec--gray" id="lineup"><div class="wrap">
{stl("LINE UP","製品ラインナップ","Product line-up","お取引に必要な仕様情報（全成分・使用期限・JANコード・入数）は各製品欄に掲載します。","Trade specifications — INCI, shelf life, JAN codes and case packs — are listed for each product.")}
{prod_cards()}</div></section>'''
    det = ''
    common = [(t("全成分（INCI）","Full INCI list"), tbd("掲載予定","To be listed")),
              (t("使用期限","Shelf life"), t("未開封 ","Unopened ") + tbd() + t("　開封後 "," · After opening ") + tbd()),
              (t("JANコード","JAN / EAN"), tbd()),
              (t("入数・ケースサイズ","Case pack"), tbd())]
    # EN_ONLY: no "buy" button pointing to Japanese consumer stores
    btns = t('<a class="btn btn--s" href="#stores">購入する</a><a class="btn btn--s btn--o" href="contact.html">お取引・卸のご相談</a>',
             '<a class="btn btn--s" href="contact.html">Trade enquiry</a><a class="btn btn--s btn--o" href="partners.html">Become a distributor</a>')
    for i, p in enumerate(PRODUCTS()):
        if V22():
            btns = t('<a class="btn btn--s" href="#stores">購入する</a>', "") + cta("product", "この商品について相談する", "Ask about this product", "btn--s" + t(" btn--o", ""), p["id"]) + t("", '<a class="btn btn--s btn--o" href="partners.html">Become a distributor</a>')
        im = f'<img src="{IMG}{p["img"]}" alt="{p["name"]}">' if p["img"] else f'<div class="ph-img">{t("製品画像<br>準備中","Image<br>coming soon")}</div>'
        lb = ''.join(f'<span class="lbl {c}">{x}</span>' for x, c in p["lbls"])
        tg = ''.join(f'<span>{x}</span>' for x in p["tags"])
        rows = ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in p["rows"] + common)
        bg = "" if i % 2 == 0 else " sec--gray"
        det += f'''<section class="sec{bg}" id="{p["id"]}"><div class="wrap">
<h3 class="hd3">{p["name"]}<small>{p["sub"] if EN() else p["sub"].upper()}</small></h3>
<div class="pdt"><div class="pdt__img"><div class="pc-card__lbls">{lb}</div>{im}</div>
<div><span class="pdt__c">{p["cat"]}</span><h3>{p["name"]}<small>{p["sub"]}</small></h3>
<p class="cp">{p["catch"]}</p><p class="ds">{p["desc"]}</p>
{f'<div class="tg">{tg}</div>' if tg else ''}
<table class="otbl otbl--w">{rows}</table>
<div class="btn-row">{btns}</div></div></div>
</div></section>'''
    collab = f'''<section class="sec sec--rose"><div class="wrap">{st("COLLABORATION","IPコラボレーション商品","Licensed IP collaborations")}{ip_grid()}
<div class="btn-row"><a class="btn" href="collaboration.html">{t("コラボレーションについて","About our collaborations")}</a></div></div></section>'''
    return page("brand.html", t("ブランド・製品","Brand &amp; Products"),
                t("花印のブランド理念と製品ラインナップ。クレンジングローション、フェイスマスク、ハトムギ化粧水。無香料・無着色・オイルフリー・アルコールフリーの日本製スキンケア。",
                  "HANAJIRUSHI brand philosophy and product line-up: Deep Cleansing Lotion, Super Moisture Face Mask, Hatomugi Skin Conditioner. Clean formulas, made in Japan."),
                hd + phil + lineup + det + collab + stores())

# ============================================================ COMPANY
def p_company():
    hd = lower("COMPANY","会社概要","Company","東京・銀座から、日本のスキンケアを世界へ。","Japanese skincare, from Ginza, Tokyo to the world.","h_campany_top_p.jpg",
               [A("message","代表挨拶","Message"),A("profile","会社概要","Profile"),A("business","事業内容","Business"),A("history","沿革","History"),A("office","オフィス紹介","Office"),A("access","アクセス","Access")])
    msg = f'''<section class="sec" id="message"><div class="wrap">
{st("MESSAGE","代表挨拶","Message from the Representative")}
<div class="md md--top"><img class="ph" src="{IMG}h_campany_ent.jpg" alt="">
<div class="txt"><p class="catch">{t('<span class="mincho">銀座から、<em>世界</em>へ。</span>','From Ginza <em>to the world.</em>')}</p>
<p class="mt2">{MESSAGE_PH()}</p>
<p style="text-align:right;margin-top:24px">{t("花印粧業研究所株式会社<br>代表取締役 ","Hanajirushi Institute of Cosmetics, Inc.<br>Representative Director ")}{tbd("氏名","Name TBC")}</p></div></div></div></section>'''
    prof = f'''<section class="sec sec--gray" id="profile"><div class="wrap">
{stl("PROFILE","会社概要","Company profile")}
<table class="otbl otbl--w" style="background:#fff">{company_rows(full=True)}</table></div></section>'''
    # EN_ONLY: corporate structure note
    struct = '' if not EN() else f'''<section class="sec--s"><div class="wrap"><div class="ibox ibox--rose"><h4>Corporate structure<small>企業体制</small></h4>
<p>{STRUCTURE_EN()}</p></div></div></section>'''
    business = f'''<section class="sec" id="business"><div class="wrap">
{st("BUSINESS","事業内容","Our business","化粧品の原料、化粧品、健康食品の研究開発、製造、販売及び輸出入","R&amp;D, manufacturing, sales, import and export of cosmetic raw materials, cosmetics and health foods")}
{cmt_cards(BUSINESS(), "BUSINESS")}</div></section>'''
    history = f'''<section class="sec sec--gray" id="history"><div class="wrap">
{stl("HISTORY","沿革","History")}
<table class="otbl otbl--w" style="background:#fff">{"".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in HISTORY())}</table>
<p style="font-size:12px;color:var(--ink-3);margin-top:10px">{t("※ 年月は確認のうえ掲載します。","Dates to be confirmed.")}</p></div></section>'''
    office = f'''<section class="sec" id="office"><div class="wrap">
{st("OFFICE","オフィス紹介","Our Ginza office","銀座二丁目の本社に、研究室・ショールーム・応接室を備えています。","Our head office in Ginza 2-chome houses our laboratory, showroom and meeting rooms.")}
<div class="md md--top md--300"><img class="ph" src="{IMG}h_campany_bldg.jpg" alt="" style="aspect-ratio:3/4">
<ul class="thumbs">{"".join(f'<li><img src="{IMG}{im}" alt=""><span>{x}</span></li>' for im, x in OFFICE_PHOTOS())}</ul></div></div></section>'''
    access = f'''<section class="sec sec--gray" id="access"><div class="wrap">
{stl("ACCESS","アクセス","Access")}
<div class="md md--top"><div class="mapframe"><iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%B8%AD%E5%A4%AE%E5%8C%BA%E9%8A%80%E5%BA%A72-12-12&output=embed&hl={L}"></iframe></div>
<div><table class="otbl" style="background:#fff">
<tr><th>{t("所在地","Address")}</th><td>{ADDR(True)}</td></tr>
<tr><th>{t("最寄駅","Stations")}</th><td>{STATIONS()}{tbd("分数","min TBC")}</td></tr>
<tr><th>TEL</th><td>{TEL()}</td></tr><tr><th>FAX</th><td>{FAX()}</td></tr>
<tr><th>{t("受付時間","Hours")}</th><td>{t("平日 10:00〜18:00（土日祝除く）","Mon–Fri 10:00–18:00 (JST)")}</td></tr></table>
<div class="btn-row" style="justify-content:flex-start"><a class="btn btn--s btn--o" href="https://maps.google.com/?q=2-12-12+Ginza+Chuo-ku+Tokyo">{t("Googleマップで見る","Open in Google Maps")}</a></div></div></div></div></section>'''
    return page("company.html", t("会社概要","Company"),
                t("花印粧業研究所株式会社の会社概要。代表挨拶、事業内容、沿革、オフィス紹介、アクセス。2015年創業、東京・銀座本社。",
                  "Company profile of Hanajirushi Institute of Cosmetics, Inc. Founded 2015, headquartered in Ginza, Tokyo, with in-house R&D, manufacturing and export."),
                hd + msg + prof + struct + business + history + office + access)

def STATIONS():
    return t("東京メトロ有楽町線「銀座一丁目駅」<br>東京メトロ銀座線・丸ノ内線・日比谷線「銀座駅」<br>徒歩 ","Ginza-itchome Station (Yurakucho Line)<br>Ginza Station (Ginza, Marunouchi, Hibiya Lines)<br>Walk ")

def MESSAGE_PH():
    return t("（代表挨拶の原稿をご提供いただき掲載します。創業の想い、ものづくりへの姿勢、海外展開への展望などを400〜600字程度で想定しています。）","(Message from the Representative Director to be supplied — around 150–250 words on the company's founding, approach to product-making and global ambitions.)")

def STRUCTURE_EN():  # EN_ONLY
    return f'<b>HANAJIRUSHI is a Japanese skincare brand headquartered in Ginza, Tokyo, with R&amp;D and product development based in Japan.</b> Our China market operations are managed through {tbd("","[China operating company] TBC")}, covering Tmall, Douyin and offline retail including Watsons. Global distribution enquiries are handled directly by our Tokyo head office.'

def BUSINESS():
    return [
     ("h_campany_lab.jpg","01",t("<em>研究開発</em>","<em>Research &amp; development</em>"),t("自社研究室で、化粧品原料レベルから処方を開発。肌へのやさしさと実感を両立する処方を追求しています。","Formulation from the raw-material level in our own laboratory — balancing gentleness and results."),t(["原料研究","処方開発","評価試験"],["Ingredients","Formulation","Testing"]),"rd.html"),
     ("hanajirushi_hsc.jpg","02",t("<em>製造</em>","<em>Manufacturing</em>"),t("日本国内での化粧品製造。メイド・イン・ジャパンの品質を、国内外のお客様へお届けします。","Cosmetics manufacturing in Japan, delivering made-in-Japan quality to customers at home and abroad."),t(["日本製","品質管理"],["Made in Japan","Quality control"]),"rd.html#quality"),
     ("h_campany_sr.jpg","03",t("<em>販売・輸出入</em>","<em>Sales &amp; trade</em>"),t("国内オンラインストアでの販売に加え、自社で輸出入を行い、世界12ヵ国のパートナーへ製品を供給しています。","We handle import and export ourselves, supplying partners in 12 countries."),t(["国内販売","輸出入","代理店"],["Domestic sales","Import/export","Distributors"]),"partners.html"),
    ]

def HISTORY():
    return [
     (t("2015年1月","Jan 2015"), t("花印粧業研究所株式会社を東京都中央区銀座に設立","Hanajirushi Institute of Cosmetics founded in Ginza, Tokyo")),
     (tbd("年月","Date TBC"), t("花印クレンジングローション、ハトムギ化粧水などを発売","Deep Cleansing Lotion, Hatomugi Skin Conditioner and other core products launched")),
     (tbd("年月","Date TBC"), t("中国市場へ進出（天猫・抖音・屈臣氏等）","Entered the China market (Tmall, Douyin, Watsons)")),
     (tbd("年月","Date TBC"), t("日本の人気IPとの正規ライセンス商品の開発を開始","First officially licensed Japanese IP collaboration")),
     (t("2022年7月","Jul 2022"), t("コーポレートサイトをリニューアル","Corporate website renewed")),
     (t("2026年9月","Sep 2026"), t("コーポレートサイト英語版を公開、海外代理店の募集を開始","English website launched; overseas partnership programme opened")),
     (t("2026年11月","Nov 2026"), t("Cosmoprof Asia 2026（香港）に出展","Exhibiting at Cosmoprof Asia 2026, Hong Kong")),
    ]

# ============================================================ R&D
def flow_steps(steps):
    return '<ol class="flow2">' + ''.join(f'<li><span class="s">STEP<b>{i+1:02d}</b></span><h4>{a}</h4><p>{b}</p></li>' for i, (a, b) in enumerate(steps)) + '</ol>'

def p_rd():
    hd = lower("R&amp;D / QUALITY","研究開発・品質","R&amp;D &amp; Quality","銀座の自社研究室から、確かな処方を。","Reliable formulas, from our own laboratory in Ginza.","h_campany_lab.jpg",
               [A("lab","自社研究室","Laboratory"),A("process","開発から出荷まで","Process"),A("quality","品質管理体制","Quality"),A("docs","輸出書類","Export documents"),A("regist","各国登録の支援","Registration")])
    lab = f'''<section class="sec" id="lab"><div class="wrap">
{st("LABORATORY","銀座の自社研究室","Our laboratory in Ginza")}
<div class="md"><img class="ph" src="{IMG}h_campany_lab.jpg" alt="">
<div class="txt"><p class="catch">{RD_CATCH()}</p>
<p class="mt2">{RD_P1()}</p>
<p>{RD_P2()}</p>
<div class="tg">{"".join(f"<span>{x}</span>" for x in RD_TAGS())}</div></div></div>
<ul class="pts mt3">
<li><p class="n">POINT<b>01</b></p><h4>{RD_POINT1_T()}</h4><p>{RD_POINT1_D()}</p></li>
<li><p class="n">POINT<b>02</b></p><h4>{RD_POINT2_T()}</h4><p>{RD_POINT2_D()}</p></li>
<li><p class="n">POINT<b>03</b></p><h4>{RD_POINT3_T()}</h4><p>{RD_POINT3_D()}</p></li></ul>
</div></section>'''
    steps = RD_STEPS()
    process = f'''<section class="sec sec--gray" id="process"><div class="wrap">
{stl("PROCESS","開発から出荷まで","From formulation to shipment")}{flow_steps(steps)}</div></section>'''
    quality = f'''<section class="sec" id="quality"><div class="wrap">
{st("QUALITY","品質管理体制","Quality management","工場情報・認証・生産能力は確認のうえ掲載します。","Factory details, certifications and capacity will be published once confirmed.")}
<div class="g3">
<div class="ibox"><h4>{QUALITY1_T()}<small>{QUALITY1_S()}</small></h4><p>{QUALITY1_B()}</p></div>
<div class="ibox"><h4>{QUALITY2_T()}<small>{QUALITY2_S()}</small></h4><p>{QUALITY2_B()}</p></div>
<div class="ibox"><h4>{QUALITY3_T()}<small>{QUALITY3_S()}</small></h4><p>{QUALITY3_B()}</p></div>
</div></div></section>'''
    docs = f'''<section class="sec sec--gray" id="docs"><div class="wrap">
{stl("EXPORT DOCUMENTS","輸出書類への対応","Export documentation","海外のお取引先の輸入・登録手続きに必要な書類を、製品ごとにご用意します。","The documents your importer and regulator will ask for — prepared for each product.")}
{export_list()}</div></section>'''
    reg = f'''<section class="sec" id="regist"><div class="wrap">
{st("REGISTRATION","各国登録の技術支援","Registration support by market","登録実績の有無にかかわらず、現地登録に必要な技術資料の提供でパートナー様の手続きを支援します。","Whether or not we have registered in your market before, we support your local registration with the technical documentation it requires.")}
{reg_table()}</div></section>'''
    return page("rd.html", t("研究開発・品質","R&amp;D &amp; Quality"),
                t("花印の研究開発と品質管理。銀座の自社研究室での処方開発、日本国内での製造、輸出書類、各国登録の技術支援。",
                  "HANAJIRUSHI R&D and quality: in-house formulation in Ginza, manufacturing in Japan, export documentation and registration support."),
                hd + lab + process + quality + docs + reg)

# ============================================================ COLLABORATION
def p_collaboration():
    hd = lower("COLLABORATION","IPコラボレーション","Licensed IP Collaborations","日本の人気IPとの正規ライセンス商品。","Officially licensed products with leading Japanese IP.","hanajirushi_col_lts.jpg",
               [A("about","コラボレーションについて","About"),A("works","コラボレーション実績","Portfolio"),A("value","パートナー様へのメリット","Value for partners")])
    about = f'''<section class="sec" id="about"><div class="wrap">
<div class="md"><div class="txt">{sth("コラボレーションについて","About")}
<p class="catch mt2">{COLLAB_CATCH()}</p>
<p class="mt1">{COLLAB_P1()}</p>
<p>{COLLAB_P2()}</p></div>
<img class="ph" src="{IMG}hanajirushi_col_sm.jpg" alt=""></div></div></section>'''
    li = ''.join(f'''<li><img src="{IMG}{im}" alt="{n}"><div class="b"><span class="lbl {c}">{l}</span><h4>{n}</h4>
<dl><dt>{t("商品","Product")}</dt><dd>{s}</dd><dt>{t("販売","Channel")}</dt><dd>{ch or tbd()}</dd><dt>{t("区分","Type")}</dt><dd>{t("正規ライセンス商品","Officially licensed")}</dd></dl></div></li>''' for im, n, s, l, c, ch in IPS())
    works = f'''<section class="sec sec--rose" id="works"><div class="wrap">
{st("WORKS","コラボレーション実績","Collaboration portfolio")}<ul class="ipd">{li}</ul>
<div class="mt2">{IPNOTE()}</div>
<p style="font-size:12px;color:var(--ink-3);margin-top:8px;text-align:center">{t("※ IP名称・画像の公開範囲は各ライセンス契約を確認のうえ掲載します","IP names and images will be published within the scope of each licence agreement")} {tbd()}</p></div></section>'''
    vals = COLLAB_VALUES()
    value = f'''<section class="sec" id="value"><div class="wrap">
{stl("MERIT","パートナー様へのメリット","What this means for distributors")}
<ul class="pts">{"".join(f'<li><p class="n">MERIT<b>{i+1:02d}</b></p><h4>{a}</h4><p>{b}</p></li>' for i, (a, b) in enumerate(vals))}</ul>
<div class="btn-row">{cta("oem","OEM・共同開発について相談する","Discuss OEM &amp; co-development") if V22() else f'<a class="btn" href="contact.html">{t("コラボのご相談","Discuss a collaboration")}</a>'}<a class="btn btn--o" href="partners.html">{t("代理店募集について","Partnership programme")}</a></div></div></section>'''
    return page("collaboration.html", t("IPコラボレーション","Licensed IP Collaborations"),
                t("花印のIPコラボレーション。美少女戦士セーラームーン、リトルツインスターズ、フルーツバスケット、ユーリ!!! on ICE との正規ライセンス商品。",
                  "HANAJIRUSHI licensed IP collaborations: Sailor Moon, Little Twin Stars, Fruits Basket, Yuri!!! on ICE. Full co-development capability for distributors."),
                hd + about + works + value)

# ============================================================ GLOBAL
def p_global():
    hd = lower("GLOBAL","海外展開","Global Network","日本ならではの上質で誠実なものづくりを、世界へ。","Japanese quality and honesty, trusted in 12 countries.",None,
               [A("network","販売ネットワーク","Network"),A("markets","主要市場","Key markets"),A("china","中国市場での実績","Proven in China")])
    net = f'''<section class="sec" id="network"><div class="wrap">
{st("GLOBAL NETWORK","世界12ヵ国で販売","Sold in 12 countries","日本ならではの上質で誠実なものづくりが認められ、国内はもとより世界12ヵ国で販売されています。","Recognised for the quality and honesty of Japanese manufacturing, HANAJIRUSHI is sold in Japan and 12 countries worldwide.")}
<div class="g3" style="max-width:780px;margin:0 auto 24px"><div class="stat"><small>{t("販売国","Countries")}</small><b>12<u>{t("ヵ国","")}</u></b></div><div class="stat"><small>{t("展開地域","Regions")}</small><b>3<u>{t("地域","")}</u></b></div><div class="stat"><small>{t("創業","Since")}</small><b>2015<u>{t("年","")}</u></b></div></div>
<div class="gmap"><img src="{IMG}world_map_brand.png" alt=""><div class="big"><small>{t("世界","Sold in")}</small><b>12<u>{t("ヵ国","")}</u></b><small>{t("で販売","countries")}</small></div></div>
<p class="center" style="font-size:12px;color:var(--ink-3);margin-top:10px">{t("※ 販売国の一覧は確認のうえ掲載します","Country list to be confirmed")} {tbd("12ヵ国リスト","12-country list")}</p></div></section>'''
    regs = REGIONS()
    markets = f'''<section class="sec sec--gray" id="markets"><div class="wrap">
{stl("MARKETS","主要市場","Key markets")}
<div class="g3">{"".join(f'<div class="ibox"><h4>{a}<small>{e}</small></h4><p>{d}</p><div class="docs mt1">{"".join(f"<span>{c}</span>" for c in cs)}</div></div>' for a, e, d, cs in regs)}</div></div></section>'''
    china = f'''<section class="sec" id="china"><div class="wrap">
{st("MARKET PROVEN","中国市場での実績","Proven in China","アジア最大で、最も競争の激しい美容市場で、ECから実店舗まで複数のチャネルを築いてきました。","Asia's largest and most demanding beauty market — where we have built channels from e-commerce to physical retail.")}
<div class="g4">
<div class="ibox ibox--rose"><h4>{CHINA1_T()}<small>{CHINA1_S()}</small></h4><p>{CHINA1_B()}</p></div>
<div class="ibox ibox--rose"><h4>{CHINA2_T()}<small>{CHINA2_S()}</small></h4><p>{CHINA2_B()}</p></div>
<div class="ibox ibox--rose"><h4>{CHINA3_T()}<small>{CHINA3_S()}</small></h4><p>{CHINA3_B()}</p></div>
<div class="ibox ibox--rose"><h4>{CHINA4_T()}<small>{CHINA4_S()}</small></h4><p>{CHINA4_B()}</p></div>
</div>
<div class="btn-row"><a class="btn" href="partners.html">{t("代理店募集について","Partnership programme")}</a></div></div></section>'''
    return page("global.html", t("海外展開","Global Network"),
                t("花印の海外展開。世界12ヵ国で販売。東アジア・東南アジア・北米の主要市場と、中国市場での実績。",
                  "HANAJIRUSHI global network: sold in 12 countries across East Asia, Southeast Asia and North America, with a proven multi-channel presence in China."),
                hd + net + markets + china)

# ============================================================ PARTNERS
def p_partners():
    hd = lower("FOR PARTNERS","海外代理店・パートナー募集","Partnership Programme","市場と規模に合わせた協業モデルをご用意しています。","Cooperation models to fit your market and scale.","h_campany_lab.jpg",
               [A("why","選ばれる理由","Why us"),A("models","協業モデル","Models"),A("terms","取引条件","Trade terms"),A("support","輸出書類・登録支援","Export support"),A("flow","お取引の流れ","How to start"),A("faq","よくあるご質問","FAQ")])
    why = f'''<section class="sec" id="why"><div class="wrap">
<div class="box recruit"><div class="box__h box__h--rose"><h3>{I["hand"]}{t("海外代理店・パートナー募集中","Now recruiting partners")}</h3><span class="en">{t("NOW RECRUITING","募集中")}</span></div><span class="stamp2">{t("募集中","募集中<small>NOW OPEN</small>")}</span>
<div class="box__b"><p class="lead">{PARTNER_LEAD()}</p>
<p style="font-size:13.5px;color:var(--ink-2)">{PARTNER_TEXT()}</p></div></div>
<ul class="pts mt3">
<li><p class="n">REASON<b>01</b></p><h4>{PARTNER_REASON1_T()}</h4><p>{PARTNER_REASON1_D()}</p></li>
<li><p class="n">REASON<b>02</b></p><h4>{PARTNER_REASON2_T()}</h4><p>{PARTNER_REASON2_D()}</p></li>
<li><p class="n">REASON<b>03</b></p><h4>{PARTNER_REASON3_T()}</h4><p>{PARTNER_REASON3_D()}</p></li></ul></div></section>'''
    modes = MODES()
    models = f'''<section class="sec sec--gray" id="models"><div class="wrap">
{stl("MODELS","協業モデル","Cooperation models")}
<div class="sx"><table class="dtbl" style="background:#fff"><thead><tr><th>{t("協業モデル","Model")}</th><th>{t("対象","For")}</th><th>{t("ご提示する主な条件","What we define together")}</th></tr></thead><tbody>
{"".join(f"<tr><th>{a}<small>{b}</small></th><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in modes)}</tbody></table></div></div></section>'''
    terms_rows = TERMS()
    terms = f'''<section class="sec" id="terms"><div class="wrap">
{st("TERMS","取引条件","Trade terms","数値は確認のうえ掲載します。","Figures to be confirmed before publishing.")}
<table class="otbl otbl--w">{"".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in terms_rows)}</table></div></section>'''
    support = f'''<section class="sec sec--gray" id="support"><div class="wrap">
{stl("SUPPORT","輸出書類・各国登録の支援","Export documents &amp; registration support")}
{hd3("対応可能な輸出書類","Export documents")}{export_list()}
<div class="mt3">{hd3("各国登録の技術支援","Registration support")}{reg_table()}</div></div></section>'''
    steps = PARTNER_STEPS()
    flow = f'''<section class="sec" id="flow"><div class="wrap">
{st("FLOW","お取引開始までの流れ","How to get started")}{flow_steps(steps)}
<div class="btn-row mt3"><a class="btn" href="{"contact.html?topic=partner#form" if V22() else "contact.html"}" style="min-width:min(320px,100%);height:58px;font-size:16px">{t("代理店申込フォームへ","Apply to become a partner")}</a></div></div></section>'''
    qa = FAQ()
    faq = f'''<section class="sec sec--gray" id="faq"><div class="wrap">
{stl("FAQ","よくあるご質問","Frequently asked questions")}
<div class="faq">{"".join(f'<details{" open" if i == 0 else ""}><summary><span class="q">Q</span>{q}</summary><div class="ans"><span class="a">A</span><p>{a}</p></div></details>' for i, (q, a) in enumerate(qa))}</div></div></section>'''
    return page("partners.html", t("海外代理店・パートナー募集","Partnership Programme"),
                t("花印の海外代理店・パートナー募集。協業モデル、取引条件、輸出書類、各国登録の技術支援、お取引開始までの流れ、よくあるご質問。",
                  "Become a HANAJIRUSHI distributor: cooperation models, trade terms, export documentation, registration support, how to start and FAQ."),
                hd + why + models + terms + support + flow + faq)

# ============================================================ EXHIBITION
def p_exhibition():
    hd = lower("EXHIBITION","展示会情報","Exhibitions","展示会への出展情報と、商談のご予約。","Where to meet us — and how to book a meeting.",None,
               [A("outline","出展概要","Outline"),A("products","出展製品","Products"),A("booking","商談のご予約","Book a meeting")])
    outline = f'''<section class="sec" id="outline"><div class="wrap">
<div class="exh"><span class="stamp3">{t("出展<br>決定！","出展<small>EXHIBITING</small>")}</span>
<div><span class="pill">INFORMATION</span><h2>Cosmoprof Asia 2026<small>{t("に出展します！","See you in Hong Kong!")}</small></h2>
<p style="margin-top:12px;font-size:14px">{EXH_INTRO()}</p></div>
<dl><dt>{t("会期","Dates")}</dt><dd>{t("2026年11月","November 2026")} {tbdw("日程確定待ち","TBC")}</dd><dt>{t("会場","Venue")}</dt><dd>{t("香港コンベンション＆<br>エキシビションセンター","Hong Kong Convention &amp;<br>Exhibition Centre")}</dd><dt>{t("ブース","Booth")}</dt><dd>{tbdw("確定待ち","TBC")}</dd></dl></div>
<div class="mt3">{hd3("出展概要","Outline")}
<table class="otbl otbl--w"><tr><th>{t("展示会名","Event")}</th><td>Cosmoprof Asia 2026</td></tr><tr><th>{t("会期","Dates")}</th><td>{t("2026年11月","November 2026")} {tbd("日程確定待ち","TBC")}</td></tr>
<tr><th>{t("会場","Venue")}</th><td>{t("香港コンベンション＆エキシビションセンター（香港・湾仔）","Hong Kong Convention &amp; Exhibition Centre, Wan Chai")}</td></tr><tr><th>{t("ホール・ブース番号","Hall / booth")}</th><td>{tbd("確定待ち","TBC")}</td></tr>
<tr><th>{t("出展内容","On show")}</th><td>{EXH_ONSHOW()}</td></tr>
<tr><th>{t("対応言語","Languages")}</th><td>{t("日本語・英語・中国語 ","Japanese, English, Chinese ")}{tbd()}</td></tr></table></div></div></section>'''
    prods = f'''<section class="sec sec--gray" id="products"><div class="wrap">{stl("PRODUCTS","出展製品","Products on display")}{prod_cards(compact=True)}</div></section>'''
    days = t(["1日目","2日目","3日目"], ["Day 1","Day 2","Day 3"])
    times = SLOT_TIMES()
    slots = ''.join(f'<p class="slotday">{d} {tbd("日付","Date TBC")}</p><div class="slots">' + ''.join(f'<button type="button" data-day="{d}" class="{"off" if (i + j) % 7 == 3 else ""}">{tm}</button>' for j, tm in enumerate(times)) + '</div>' for i, d in enumerate(days))
    req, opt = f'<span class="r">{t("必須","Required")}</span>', f'<span class="o">{t("任意","Optional")}</span>'
    topics = BOOKING_TOPICS()
    booking = f'''<section class="sec" id="booking"><div class="wrap">
{st("BOOKING","商談のご予約","Book a meeting","30分単位でご予約いただけます。ご希望の日時を選択し、必要事項をご記入ください。","30-minute slots. Pick a time, fill in your details and we will confirm by email.")}
<div class="np np--320">
<form class="ibox">
<p class="hd4" style="margin-top:0">{t("ご希望の日時を選択","Choose a time")}</p>{slots}
<p class="legend"><span><i></i>{t("予約可","Available")}</span><span><i class="on"></i>{t("選択中","Selected")}</span><span><i class="off"></i>{t("予約済","Booked")}</span></p>
<p style="margin:14px 0 18px;padding:10px 14px;background:var(--rose-ll);border-radius:4px;font-size:13px">{t("選択中の日時：","Selected: ")}<b data-slot-out>{t("未選択","none")}</b></p>
<table class="ftbl">
<tr><th>{t("会社名","Company")}{req}</th><td><input type="text"></td></tr>
<tr><th>{t("お名前","Name")}{req}</th><td><input type="text"></td></tr>
<tr><th>{t("メールアドレス","Business email")}{req}</th><td><input type="email"></td></tr>
<tr><th>WhatsApp / WeChat{opt}</th><td><input type="text"></td></tr>
<tr><th>{t("ご相談内容","Topics")}{opt}</th><td><div class="cks">{"".join(f'<label><input type="checkbox">{x}</label>' for x in topics)}</div></td></tr>
</table>
<div class="fsub"><button class="btn" type="submit">{t("予約をリクエストする","Request this slot")}</button></div></form>
<aside><p class="hd4" style="margin-top:0">{t("展示会担当者","Your contact at the show")}</p>
<ul class="chn"><li><span class="ic">{I["pin"]}</span><div><small>{t("担当者","Contact person")}</small><b>{tbd("氏名","Name TBC")}</b></div></li>
<li><span class="ic">{I["chat"]}</span><div><small>WhatsApp</small><b>{tbd("番号","Number TBC")}</b></div></li>
<li><span class="ic">{I["qr"]}</span><div><small>WeChat</small><b>{tbd("ID","ID TBC")}</b></div></li>
<li><span class="ic">{I["mail"]}</span><div><small>{t("メール","Email")}</small><b>export@hanajirushi.co.jp</b> {tbd()}</div></li></ul>
<div class="qrs"><div><div class="q">QR</div>WeChat</div><div><div class="q">QR</div>WhatsApp</div></div>
<p class="hd4">{t("資料ダウンロード","Downloads")}</p>
<div style="display:flex;flex-direction:column;gap:8px"><a class="dl" href="#"><span><span class="f">PDF</span>{t("会社案内","Company profile")}</span>{I["dl"]}</a><a class="dl" href="#"><span><span class="f">PDF</span>{t("製品カタログ","Product catalogue")}</span>{I["dl"]}</a></div></aside>
</div></div></section>'''
    return page("exhibition.html", t("展示会情報","Exhibitions"),
                t("花印は Cosmoprof Asia 2026（香港）に出展します。出展概要、出展製品、ブースでの商談のご予約。",
                  "HANAJIRUSHI exhibits at Cosmoprof Asia 2026, Hong Kong. Outline, products on display and meeting booking."),
                hd + outline + prods + booking)

# ============================================================ NEWS
def p_news():
    hd = lower("NEWS","お知らせ","News","花印粧業研究所からのお知らせ・展示会・製品情報。","Announcements, exhibitions and product news.")
    cats = [(t("展示会","Exhibition"),1),(t("製品情報","Product"),2),(t("企業情報","Business"),1),(t("お知らせ","Notice"),2)]
    body = f'''<section class="sec"><div class="wrap nwrap">
<div>{news_tabs()}<ul class="nlist">{news_rows()}</ul>
{NEWS_NOTE()}
<div class="pager"><span class="on">1</span><a href="#">2</a><a href="#">3</a><a href="#">{t("次へ ›","Next ›")}</a></div></div>
<aside class="side"><h4>{t("カテゴリー","Categories")}</h4><ul>{"".join(f'<li><a href="#">{c}<span>({n})</span></a></li>' for c, n in cats)}</ul>
<h4>{t("アーカイブ","Archive")}</h4><ul><li><a href="#">2026<span>(5)</span></a></li><li><a href="#">2022<span>(1)</span></a></li></ul>
<a class="pick__s" href="exhibition.html" style="border:2px solid var(--rose);border-radius:6px;background:#fff"><img src="{IMG}hanajirushi_cl.jpg" alt=""><span><b>Cosmoprof Asia 2026</b>{t("商談予約受付中","Book a meeting")}</span></a></aside>
</div></section>'''
    return page("news.html", t("お知らせ","News"),
                t("花印粧業研究所株式会社からのお知らせ。展示会、製品情報、企業情報。", "News from Hanajirushi Institute of Cosmetics, Inc.: exhibitions, products and business updates."),
                hd + body)

# ============================================================ CONTACT
ITEM_MAP = ["p1 p4", "p3", "p2", "ip", "oem"]   # contact form product checkboxes ← ?item=pN

def p_contact():
    hd = lower("CONTACT","お問い合わせ","Contact","お取引・代理店・製品に関するご相談はこちらから。","Distribution, trade, product and OEM enquiries.")
    biz = BIZ_TYPES()
    lines = PRODUCT_LINES()
    kinds = KINDS()
    kind_vals = [""] * len(kinds)
    if V22():   # topics match the cta() buttons across the site
        kinds = KINDS_V22()
        kind_vals = list(CTA_TOPICS)
    vols = VOLUMES()
    req, opt = f'<span class="r">{t("必須","Required")}</span>', f'<span class="o">{t("任意","Optional")}</span>'
    sel = t("選択してください", "Please select")
    sm = (lambda en: f'<small>{en}</small>') if not EN() else (lambda en: '')
    # EN: WhatsApp/WeChat, target market and volume are required to qualify overseas leads
    req_en = req if EN() else opt
    top = f'''<ul class="ctop">
<li><h4>{I["tel"]}{t("お電話でのお問い合わせ","Call our Tokyo office")}</h4><p class="big">{TEL()}</p><p>{HOURS()}</p></li>
<li><h4>{I["mail"]}{t("メールでのお問い合わせ","Email enquiry")}</h4><p>{t("下記フォームより送信ください。<br>3営業日以内にご返信します。","Use the form below.<br>We reply within 3 business days.")}</p><a class="btn btn--s" href="#form">{t("フォームへ進む","Go to the form")}</a></li>
<li><h4>{I["chat"]}WhatsApp / WeChat</h4><p>{t("海外のお客様はこちらからもご連絡いただけます。","Overseas partners can also message us directly.")}<br>ID {tbd()}</p><a class="btn btn--s btn--o" href="#form">{t("QRコードを表示","Show QR codes")}</a></li></ul>'''
    form = f'''<form id="form">
<ol class="fstep"><li class="on"><span>01</span>{t("入力","Enter")}</li><li><span>02</span>{t("確認","Confirm")}</li><li><span>03</span>{t("完了","Done")}</li></ol>
<table class="ftbl">
<tr><th>{t("お問い合わせ種別","Enquiry type")}{req}</th><td><div class="cks">{"".join(f'<label><input type="radio" name="k"' + (f' value="{kind_vals[i]}"' if kind_vals[i] else "") + f'{" checked" if i == 0 else ""}>{k}</label>' for i, k in enumerate(kinds))}</div></td></tr>
<tr><th>{t("会社名","Company name")}{req}{sm("COMPANY")}</th><td><input type="text" placeholder="{t("例）花印粧業研究所株式会社","e.g. ABC Trading Co., Ltd.")}"></td></tr>
<tr><th>{t("国・地域","Country / region")}{req}{sm("COUNTRY")}</th><td><input type="text" placeholder="{t("例）日本、ベトナム","e.g. Vietnam")}"></td></tr>
<tr><th>{t("お名前","Contact person")}{req}{sm("NAME")}</th><td><input type="text" placeholder="{t("例）山田 花子","e.g. Jane Tan")}"></td></tr>
<tr><th>{t("役職","Position")}{req_en}</th><td><input type="text"></td></tr>
<tr><th>{t("メールアドレス","Business email")}{req}{sm("EMAIL")}</th><td><input type="email" placeholder="{t("例）info@example.com","e.g. jane@company.com")}"><span class="hint">{t("フリーメールではなく、会社ドメインのアドレスをご記入ください。","Please use your company domain rather than a free webmail address.")}</span></td></tr>
<tr><th>{t("電話番号","Phone")}{opt}</th><td><input type="tel" placeholder="{t("例）03-1234-5678","e.g. +84 28 1234 5678")}"></td></tr>
<tr><th>WhatsApp / WeChat{req_en}</th><td><input type="text"><span class="hint">{t("海外のお客様はいずれかをご記入ください。","Either one is fine.")}</span></td></tr>
<tr><th>{t("事業形態","Business type")}{req}</th><td><select><option>{sel}</option>{"".join(f"<option>{b}</option>" for b in biz)}</select></td></tr>
<tr><th>{t("対象市場","Target market")}{req_en}</th><td><input type="text" placeholder="{t("例）タイ、マレーシア","e.g. Thailand, Malaysia")}"></td></tr>
<tr><th>{t("ご関心の製品","Products of interest")}{opt}</th><td><div class="cks">{"".join(f'<label><input type="checkbox"' + (f' data-items="{ITEM_MAP[i]}"' if V22() else "") + f'>{x}</label>' for i, x in enumerate(lines))}</div></td></tr>
<tr><th>{t("年間予定仕入数量","Estimated annual volume")}{req_en}</th><td><select><option>{sel}</option>{"".join(f"<option>{v}</option>" for v in vols)}</select></td></tr>
<tr><th>{t("会社ウェブサイト","Company website")}{opt}</th><td><input type="url" placeholder="https://"></td></tr>
<tr><th>{t("現在の販売チャネル","Current channels")}{opt}</th><td><input type="text"></td></tr>
<tr><th>{t("お問い合わせ内容","Message")}{req}</th><td><textarea></textarea></td></tr>
<tr><th>{t("展示会","Exhibition")}{opt}</th><td><div class="cks"><label><input type="checkbox">{t("展示会会場からのお問い合わせです","I am contacting you from the exhibition floor")}</label></div></td></tr>
</table>
<div class="pp"><b>{t("個人情報の取り扱いについて","Handling of personal information")}</b><br>{t("花印粧業研究所株式会社は、お問い合わせいただいた個人情報を、お問い合わせへの回答およびご連絡のためにのみ利用し、法令に基づく場合を除き、ご本人の同意なく第三者に提供することはありません。（プライバシーポリシー全文は確認のうえ掲載します。）","Hanajirushi Institute of Cosmetics, Inc. uses the personal information you provide only to respond to your enquiry, and does not share it with third parties without your consent except where required by law. (Full privacy policy to be published.)")}</div>
<label class="agree"><input type="checkbox">{t("個人情報の取り扱いに同意する","I agree to the handling of my personal information")}</label>
<div class="fsub"><button class="btn" type="submit">{t("入力内容を確認する","Review my enquiry")}</button></div>
<p class="center" style="font-size:12px;color:var(--ink-3);margin-top:12px">{t("送信後、自動返信メールにて会社案内PDFのダウンロードリンクをお送りします。","After sending, you will receive an automatic confirmation with a link to our company profile (PDF).")}</p></form>'''
    body = f'''<section class="sec"><div class="wrap">{top}{st("FORM","お問い合わせフォーム","Enquiry form")}{form}</div></section>'''
    return page("contact.html", t("お問い合わせ","Contact"),
                t("花印粧業研究所株式会社へのお問い合わせ。海外代理店のお申込み、お取引・製品・OEM/ODMのご相談。",
                  "Contact Hanajirushi Institute of Cosmetics: distributor applications, trade, product and OEM/ODM enquiries. Email, WhatsApp, WeChat."),
                hd + body)

# ============================================================ shared copy
# Lifted verbatim from the page functions so v2.x and the premium build print the same words.

def EXPORT_DOCS():
    return [
     (t("INCI成分表","INCI ingredient list"), t("国際化粧品原料標準命名法による全成分表示","Full ingredient declaration in INCI nomenclature")),
     (t("COA（出荷検査成績書）","Certificate of Analysis (COA)"), t("ロットごとの出荷検査報告書","Batch-level test report for every shipment")),
     ("MSDS / SDS", t("安全データシート","Safety data sheet")),
     (t("自由販売証明書","Free Sale Certificate"), t("Free Sale Certificate（輸出国での販売証明）","Issued for export registration")),
     (t("原産地証明書","Certificate of Origin"), t("Certificate of Origin（関税優遇の申請用）","For preferential tariff treatment")),
     (t("製造日・ロット番号の表示ルール","Production date & lot code rules"), t("表示ルールの説明資料","Explanation of date and batch coding")),
     (t("ラベル法規対応","Labelling compliance"), t("多言語ラベル・成分表翻訳のサポート","Multilingual labels and ingredient translations")),
    ]

def REGS():
    return [
     (t("中国本土","Mainland China"),"China",t("NMPA 備案・登録資料","NMPA notification / registration dossier")),
     (t("東南アジア","Southeast Asia"),"ASEAN",t("ASEAN化粧品指令に基づく資料、各国への届出","ASEAN Cosmetic Directive dossier, national notifications")),
     ("EU","European Union",t("CPNP 届出、責任者（RP）、製品情報ファイル（PIF）","CPNP notification, Responsible Person, Product Information File")),
     (t("米国","United States"),"USA",t("MoCRA 対応、施設登録、製品リスティング","MoCRA compliance, facility registration, product listing")),
     (t("中東","Middle East"),"GCC",t("SFDA（サウジアラビア）、ESMA（UAE）登録","SFDA (Saudi Arabia), ESMA (UAE) registration")),
    ]

def REG_SUPPORT():
    return t("技術資料の提供により、現地での登録手続きを支援します", "Technical documentation provided to support your local registration")

def FV_TRUST():
    return t([("創業","2015"),("本社","東京・銀座"),("販売","世界12ヵ国"),("開発","自社研究室")],
              [("Since","2015"),("Head office","Ginza, Tokyo"),("Sold in","12 countries"),("R&amp;D","In-house lab")])

def FV_HEAD():
    return t("世界へ届ける、<br>日本品質のスキンケア製品。","Japanese-quality skincare,<br>delivered to the world.")

def FV_LEAD1():
    return t("日本で開発・製造。","Developed and made in Japan.")

def FV_LEAD2():
    return t("世界の販売代理店・ビジネスパートナーに、<br>独自性のあるスキンケア製品を提供しています。","We supply distinctive skincare products<br>to distributors and business partners worldwide.")

def JAPAN4():
    return [
     ("flask", t("日本で開発","Developed in Japan"), t("日本市場で培った商品開発力","Product development honed in the Japanese market"), ""),
     ("factory", t("日本で製造","Made in Japan"), t("日本国内での確かなものづくり","Reliable manufacturing in Japan"), tbd("製造地 要確認","Site TBC")),
     ("shield", t("日本で品質管理","Quality-checked in Japan"), t("日本基準での品質管理・検品","Quality control and inspection to Japanese standards"), tbd("要確認","TBC")),
     ("globe", t("世界での実績","Proven worldwide"), t("海外市場で積み重ねてきた取引・パートナー実績","A track record of trade and partnerships in overseas markets"), ""),
    ]

def WHY_MODELS():
    return t(["販売代理","卸売","OEM","共同開発"], ["Distribution","Wholesale","OEM","Co-development"])

def WHY():
    return [
     (t("市場実績のある商品","Products with a proven sales record"), t("実際の市場で販売実績を積み重ねてきた商品","Products with an established track record in real markets"), tbd("販売実績データ 要確認","Sales data TBC")),
     (t("独自の商品開発力","Original product development"), t("市場ニーズを捉えた商品企画・開発","Product planning and development that captures market needs"), ""),
     (t("柔軟なパートナーシップ","Flexible partnerships"), "", '<div class="why__tags">' + "".join(f"<span>{m}</span>" for m in WHY_MODELS()) + "</div>"),
     (t("海外ビジネスへの対応","Ready for overseas business"), t("各国・地域のパートナーとの取引・サポート実績","Experience trading with and supporting partners across countries and regions"), ""),
    ]

def RD_CATCH():
    return t("処方は、<em>原料レベル</em>から<br>自社で開発しています。","Every formula starts at the <em>raw-material level</em> — in-house.")

def RD_P1():
    return t("花印の処方は、東京・銀座本社の研究室で原料レベルから開発しています。肌へのやさしさと確かな実感を両立させるため、無香料・無着色・オイルフリー・アルコールフリーを基本設計としています。","HANAJIRUSHI formulas are developed from the raw-material level in the laboratory at our Ginza head office. Our baseline design is fragrance-free, colorant-free, oil-free and alcohol-free — gentle on skin, with results you can feel.")

def RD_P2():
    return t("自社で研究開発・製造・輸出入を担うことで、お取引先のご要望に応じた仕様変更やOEM/ODMにも柔軟に対応します。","Because R&amp;D, manufacturing and export are all in-house, we can respond flexibly to specification changes and OEM/ODM requests.")

def RD_TAGS():
    return t(["原料研究","処方開発","評価試験","OEM/ODM対応"],["Ingredient research","Formulation","Testing","OEM/ODM"])

def RD_POINT1_T():
    return t("研究開発 R&amp;D","R&amp;D")

def RD_POINT1_D():
    return t("自社研究室で、原料レベルから処方を開発。","In-house laboratory, formulation from raw-material level.")

def RD_POINT2_T():
    return t("製造 MAKE","Make")

def RD_POINT2_D():
    return t("日本国内での化粧品製造（メイド・イン・ジャパン）。","Cosmetics manufacturing in Japan.")

def RD_POINT3_T():
    return t("輸出入 TRADE","Trade")

def RD_POINT3_D():
    return t("自社による輸出入。短く確かな取引チェーンを実現。","Direct import &amp; export by our own company — a short, reliable trading chain.")

def RD_STEPS():
    return [(t("原料研究","Ingredient research"),t("国産原料を中心に、安全性と機能性を評価します。","Safety and function evaluated, with a focus on Japanese ingredients.")),
             (t("処方開発","Formulation"),t("低刺激設計を基本に、使用感と効果を設計します。","Low-irritation design balancing texture and efficacy.")),
             (t("試作・評価","Prototyping &amp; testing"),t("安定性・使用感・パッチテスト等で評価します。","Stability, sensory and patch testing.")),
             (t("製造","Manufacturing"),t("日本国内で化粧品を製造します。","Cosmetics manufactured in Japan.")),
             (t("品質検査・出荷","Inspection &amp; shipment"),t("ロットごとに出荷検査を行い、COAを発行します。","Batch inspection with a COA for every lot."))]

def QUALITY1_T():
    return t("生産工場","Factory")

def QUALITY1_S():
    return t("FACTORY","生産工場")

def QUALITY1_B():
    return f'''{t("名称・所在地・自社／委託の別 ","Name, location, owned or contracted ")}{tbd()}<br>{t("GMP / ISO 22716 取得状況 ","GMP / ISO 22716 status ")}{tbd()}'''

def QUALITY2_T():
    return t("生産能力","Capacity")

def QUALITY2_S():
    return t("CAPACITY","生産能力")

def QUALITY2_B():
    return f'''{t("月間生産能力 ","Monthly capacity ")}{tbd()}<br>{t("大口受注への対応可否を明記します。","To show readiness for large orders.")}'''

def QUALITY3_T():
    return t("品質管理","QC system")

def QUALITY3_S():
    return t("QC SYSTEM","品質管理")

def QUALITY3_B():
    return f'''{t("検査フロー、ロット管理、保存サンプル制度 ","Inspection flow, lot management, retained samples ")}{tbd()}'''

def COLLAB_CATCH():
    return t("人気IPと、<em>正規ライセンス</em>で。","Beloved Japanese IP, <em>officially licensed.</em>")

def COLLAB_P1():
    return t("花印は、日本の著名IPの公式ライセンスを複数取得し、処方からパッケージ、ギフトセットまで一貫したコラボレーション商品の企画・開発力を備えています。","HANAJIRUSHI holds official licences for several of Japan's best-known IP, with end-to-end capability to develop collaboration products — from formula to packaging and gift sets.")

def COLLAB_P2():
    return t("IPライセンサーの審査は、品質管理・財務・コンプライアンスにわたり厳格です。これらのライセンスを取得していること自体が、私たちの信頼の証です。","Licensors audit their partners rigorously on quality, finance and compliance. Holding these licences is itself a third-party endorsement of how we work.")

def COLLAB_VALUES():
    return [(t("高い価格プレミアム","Premium pricing"),t("限定コラボギフトセットは、通常品を上回る価格設定が可能です。","Limited collaboration gift sets retail well above regular items.")),
            (t("売場への参入","Channel access"),t("IPライセンス商品は、百貨店・専門店などの売場参入の重要な条件となります。","Licensed IP is a key condition for entering department-store and specialty counters.")),
            (t("ファンによる集客","Built-in audience"),t("IPファンによる自発的な拡散と、検索からの流入が期待できます。","Organic word-of-mouth and search traffic from fan communities.")),
            (t("市場限定の企画","Market-exclusive editions"),t("特定の国・地域向けに、専用のコラボレーション商品を企画できます。","Collaborations can be developed exclusively for your market."))]

def REGIONS():
    return [(t("東アジア","East Asia"),t("EAST ASIA","東アジア"),t("日本・中国を中心に、ドラッグストア・EC・免税チャネルで展開。","Japan and China at the core — drugstores, e-commerce and duty-free."),t(["ドラッグストア","EC","免税店"],["Drugstores","E-commerce","Duty free"])),
            (t("東南アジア","Southeast Asia"),t("SOUTHEAST ASIA","東南アジア"),t("越境ECとモダントレードを軸に拡大中。","Growing through cross-border e-commerce and modern trade."),t(["越境EC","モダントレード"],["Cross-border EC","Modern trade"])),
            (t("北米","North America"),t("NORTH AMERICA","北米"),t("ECを中心とした展開。","E-commerce-led distribution."),[t("EC","E-commerce")])]

def CHINA1_T():
    return t("天猫 公式旗艦店","Tmall flagship store")

def CHINA1_S():
    return 'E-COMMERCE'

def CHINA1_B():
    return f'''{t("開店年・実績 ","Opened / results ")}{tbd()}'''

def CHINA2_T():
    return t("抖音 インフルエンサー連携","Douyin creator network")

def CHINA2_S():
    return 'SOCIAL'

def CHINA2_B():
    return f'''{t("連携規模 ","Scale ")}{tbd()}'''

def CHINA3_T():
    return t("屈臣氏（Watsons）等","Watsons and other chains")

def CHINA3_S():
    return 'RETAIL'

def CHINA3_B():
    return f'''{t("導入店舗数 ","Store count ")}{tbd()}'''

def CHINA4_T():
    return t("中国限定IPコラボ","China-exclusive IP")

def CHINA4_S():
    return 'LICENSED IP'

def CHINA4_B():
    return f'''{t("美少女戦士セーラームーン 限定版","Sailor Moon limited edition")}'''

def PARTNER_LEAD():
    return t("独占代理店から越境EC、OEM/ODMまで。<br><em>市場と規模に合わせた協業</em>をご提案します。","From exclusive distribution to cross-border e-commerce and OEM/ODM —<br><em>a partnership that fits your market.</em>")

def PARTNER_TEXT():
    return t("東京・銀座の自社研究室で開発する日本製スキンケアを、あなたの市場へ。輸出書類のご用意から各国登録の技術支援まで、お取引に必要なサポートを行います。","Bring Japanese skincare, developed in our own Ginza laboratory, to your market. We support you from export documentation to local registration.")

def PARTNER_REASON1_T():
    return t("自社研究室を持つ日本ブランド","A Japanese brand with its own lab")

def PARTNER_REASON1_D():
    return t("銀座本社で処方開発。研究開発・製造・輸出入を自社で担います。","Formulated at our Ginza head office. R&amp;D, manufacturing and export in-house.")

def PARTNER_REASON2_T():
    return t("12ヵ国・中国市場での実績","Proven in 12 countries, including China")

def PARTNER_REASON2_D():
    return t("アジア最大の美容市場で、EC・実店舗の双方に展開しています。","Multi-channel presence in Asia's largest beauty market.")

def PARTNER_REASON3_T():
    return t("正規IPライセンス商品","Licensed IP capability")

def PARTNER_REASON3_D():
    return t("市場限定のコラボレーション商品を企画できます。","Market-exclusive collaborations can be developed.")

def MODES():
    return [(t("独占代理店","Exclusive distributor"),t("Exclusive Distributor","独占代理店"),t("単一国・地域の有力企業様","Leading importer for one country / region"),t("年間仕入額の目安、地域保護、販売目標","Annual purchase threshold, territory protection, sales targets")),
             (t("販売代理店","Authorised reseller"),t("Authorized Reseller","販売代理店"),t("中小規模の輸入業者様","Small and mid-size importers"),t("最小ロット、価格体系、オンライン販売の可否","MOQ, pricing structure, online sales permission")),
             (t("モダントレード供給","Modern trade supply"),t("Modern Trade","モダントレード"),t("ドラッグストアチェーン、コスメ専門店","Drugstore chains, beauty retailers"),t("安定供給、バーコード・ラベル対応、支払条件","Supply stability, barcode / label compliance, payment terms")),
             (t("越境EC","Cross-border e-commerce"),t("Cross-border EC","越境EC"),t("天猫国際、Shopee、Lazada、Amazon 出店者様","Tmall Global, Shopee, Lazada, Amazon sellers"),t("小ロット・直送対応、登録書類の支援","Small lots / drop-shipping, registration documents")),
             ("OEM / ODM","OEM / ODM",t("自社ブランドをお持ちの事業者様","Private-label brand owners"),t("最小ロット、開発期間、処方対応、工場資格","MOQ, development lead time, formulation, factory credentials"))]

def TERMS():
    return [(t("最小発注数量（MOQ）","Minimum order (MOQ)"), t("初回 ","First order ") + tbd() + t("　リピート "," · Repeat ") + tbd()),
                  (t("納期","Lead time"), t("在庫品 ","In stock ") + tbd() + t("　受注生産 "," · Made to order ") + tbd()),
                  (t("貿易条件","Incoterms"), t("EXW 東京 ／ FOB 東京・横浜 ／ CIF","EXW Tokyo / FOB Tokyo or Yokohama / CIF")),
                  (t("お支払条件","Payment"), t("T/T 前払い ","T/T advance ") + tbd("比率","% TBC") + t("、L/C は応相談",", L/C negotiable")),
                  (t("地域保護","Territory protection"), t("独占代理店契約に基づき設定","Defined under the exclusive distribution agreement")),
                  (t("価格体系","Pricing"), t("数量に応じた段階価格（価格表は個別にご案内します）","Tiered by volume; price lists are provided on request")),
                  (t("サンプル","Samples"), t("無償提供の範囲・送料負担 ","Free sample allowance / freight ") + tbd()),
                  (t("販促支援","Marketing support"), t("販促物、商品研修、展示会への協力、販促費の補助","POS material, training, exhibition support, promotion subsidies")),
                  (t("価格・流通管理","Price &amp; channel control"), t("並行輸入・過度な値引きへの対策により、代理店様の利益を保護","Measures against parallel imports and under-pricing to protect partner margins"))]

def PARTNER_STEPS():
    return [(t("申込フォーム送信","Submit the application"),t("会社情報、対象市場、販売チャネル、年間予定数量をご記入ください。","Company details, target market, channel type and estimated annual volume.")),
             (t("3営業日以内にご返信","Reply within 3 business days"),t("担当者よりご連絡し、オンライン面談を設定します。","We contact you and schedule an online meeting.")),
             (t("サンプル評価・条件協議","Samples &amp; terms"),t("サンプルをお送りし、取引条件をすり合わせます。","We send samples and align on commercial terms.")),
             (t("契約・初回発注","Agreement &amp; first order"),t("代理店契約を締結し、初回のご発注をいただきます。","Distribution agreement signed; first order placed.")),
             (t("出荷・販売開始","Shipment &amp; launch"),t("販促物や商品研修で、市場での立ち上げを支援します。","Launch support with marketing materials and training."))]

def FAQ():
    return [(t("最小発注数量（MOQ）はどのくらいですか？","What is the minimum order quantity (MOQ)?"),
           t("初回・リピートそれぞれの最小発注数量を設定しています。具体的な数量は ","We set separate MOQs for first and repeat orders. Exact quantities: ") + tbd() + t("。協業モデルにより異なりますので、お気軽にご相談ください。",". They vary by cooperation model — please ask.")),
          (t("サンプルを取り寄せることはできますか？","Can we request samples?"),
           t("サンプルのご提供が可能です。無償提供の範囲や送料のご負担については ","Yes, samples are available. Free allowance and freight terms: ") + tbd() + t("。",".")),
          (t("自国での化粧品登録に必要な書類は用意してもらえますか？","Can you provide documents for registration in our country?"),
           t("INCI成分表、COA、MSDS/SDS、自由販売証明書、原産地証明書などをご用意し、現地での登録手続きを技術資料の提供で支援します。","We provide the INCI list, COA, MSDS/SDS, Free Sale Certificate, Certificate of Origin and other technical documents to support your local registration.")),
          (t("独占代理店になることはできますか？","Can we become the exclusive distributor for our market?"),
           t("国・地域ごとに独占代理店契約が可能です。年間仕入額の目安や販売目標などの条件をご提示のうえ、協議させていただきます。","Yes, exclusive agreements are available by country or region, based on annual purchase thresholds and sales targets agreed together.")),
          (t("自社ブランド（OEM/ODM）での製造は可能ですか？","Do you offer OEM/ODM for private labels?"),
           t("自社研究室での処方開発を活かし、OEM/ODMにも対応しています。最小ロット・開発期間は ","Yes — using our in-house formulation capability. MOQ and development lead time: ") + tbd() + t("。","."))]

def EXH_INTRO():
    return t("アジア最大級の美容見本市に出展します。ブースでは製品をお試しいただけるほか、代理店・お取引のご相談を承ります。","We are exhibiting at Asia's leading beauty trade show. Try our products at the booth and talk to us about distribution.")

def EXH_ONSHOW():
    return t("スキンケア製品（クレンジング・化粧水・フェイスマスク）、IPコラボレーション商品、OEM/ODMのご案内","Skincare (cleansing, lotion, face mask), licensed IP products, OEM/ODM services")

def SLOT_TIMES():
    return ["10:00","10:30","11:00","11:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30"]

def BOOKING_TOPICS():
    return t(["代理店","モダントレード","越境EC","OEM/ODM","IPコラボ"], ["Distribution","Modern trade","Cross-border EC","OEM/ODM","Licensed IP"])

def BIZ_TYPES():
    return t(["輸入業者","販売代理店","小売チェーン","ECプラットフォーム・EC事業者","自社ブランド（OEM/ODM）","メディア","その他"],
            ["Importer","Distributor","Retail chain","E-commerce platform / seller","Private label (OEM/ODM)","Media","Other"])

def PRODUCT_LINES():
    return t(["クレンジング","化粧水","フェイスマスク","IPコラボ商品","OEM/ODM"], ["Cleansing","Lotion","Face mask","Licensed IP products","OEM/ODM"])

def KINDS():
    return t(["代理店・お取引のご相談","製品について","OEM/ODM","IPコラボ","その他"], ["Distribution / trade","Products","OEM/ODM","IP collaboration","Other"])

def KINDS_V22():
    return t(["販売パートナー（代理店・卸）について","商品について","OEM・共同開発について","ビジネス全般・その他"],
                  ["Sales partnership (distribution / wholesale)","Products","OEM &amp; co-development","General business / other"])

def VOLUMES():
    return t(["〜1,000個","1,000〜10,000個","10,000〜50,000個","50,000個以上"], ["Up to 1,000 units","1,000–10,000","10,000–50,000","50,000+"])

PAGES = {
 "index.html": p_home, "brand.html": p_brand, "company.html": p_company, "rd.html": p_rd,
 "collaboration.html": p_collaboration, "global.html": p_global, "partners.html": p_partners,
 "exhibition.html": p_exhibition, "news.html": p_news, "contact.html": p_contact,
}

# ============================================================ Japanese line breaking
# BudouX splits Japanese text into phrases; <wbr> between phrases + CSS word-break:keep-all
# makes every browser (incl. Safari on iPhone) wrap between phrases instead of mid-word.
_BX = budoux.load_default_japanese_parser()
_JP = re.compile(r"[぀-ヿ一-鿿]")
_SKIP = {"script", "style", "title", "textarea", "select", "option"}

def add_wbr(html):
    head, sep, body = html.partition("<body")
    out, skip = [], 0
    for tok in re.split(r"(<[^>]+>)", body):
        if tok.startswith("<"):
            m = re.match(r"</?([a-zA-Z0-9]+)", tok)
            if m and m.group(1).lower() in _SKIP:
                skip += -1 if tok.startswith("</") else 1
            out.append(tok)
        elif tok and not skip and _JP.search(tok):
            joined = "<wbr>".join(_BX.parse(tok))
            out.append(re.sub(r"(&[#a-zA-Z0-9]*)<wbr>([#a-zA-Z0-9]*;)", r"", joined))
        else:
            out.append(tok)
    return head + sep + "".join(out)

# ============================================================ review hub
def hub():
    names = [("index.html", "Top", "トップ")] + [(f, en, ja) for f, ja, en in
             [("brand.html","ブランド・製品","Brand &amp; Products"),("company.html","会社概要","Company"),("rd.html","研究開発・品質","R&amp;D &amp; Quality"),
              ("collaboration.html","IPコラボレーション","Collaboration"),("global.html","海外展開","Global"),("partners.html","代理店募集","For Partners"),
              ("exhibition.html","展示会情報","Exhibition"),("news.html","お知らせ","News"),("contact.html","お問い合わせ","Contact")]]
    def col(prefix, lang, label, tag, only=None):
        return f'<div class="hub__col"><h2>{label}<b>{tag}</b></h2><ul>' + ''.join(
            f'<li><a href="{prefix}{lang}/{f}">{en}<span>{ja}</span></a></li>' for f, en, ja in names if not only or f in only) + '</ul></div>'
    prem = tuple(f for f, _, _ in names if f != "global.html")  # premium: 海外展開 is part of 代理店募集
    return f'''<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>花印 HANAJIRUSHI — Website Design Mockup</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Montserrat:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css"></head><body class="hubpage">
<div class="hub"><div class="hub__in">
<div class="hub__hd"><img class="hub__logo" src="assets/img/logo.svg" alt="花印 HANAJIRUSHI"><div><h1>Website <span>Mockup</span></h1><p>花印 公式サイト デザインモックアップ ／ 日本語版・英語版</p></div></div>
<h2 class="hub__ver">Premium <span>採用案 — 生成り×葡萄色・円窓・明朝縦組み＋商談獲得型の構成（全9ページ）</span></h2>
<div class="hub__g">{col("premium/","ja","日本語版 Japanese","JA · Premium",prem)}{col("premium/","en","英語版 English","EN · Premium",prem)}</div>
<h2 class="hub__ver">v2.2 <span>v2.1＋商談獲得型の構成（FV刷新・日本製4つの強み・選ばれる理由・相談CTA）</span></h2>
<div class="hub__g">{col("v2.2/","ja","日本語版 Japanese","JA · v2.2")}{col("v2.2/","en","英語版 English","EN · v2.2")}</div>
<h2 class="hub__ver">v2.1 <span>ソフト版 — やわらかく上品な配色・書体（社内レビュー用）</span></h2>
<div class="hub__g">{col("v2.1/","ja","日本語版 Japanese","JA · v2.1")}{col("v2.1/","en","英語版 English","EN · v2.1")}</div>
<h2 class="hub__ver">v2 <span>現行版 — ローズ・ゴシック体</span></h2>
<div class="hub__g">{col("","ja","日本語版 Japanese","JA · v2")}{col("","en","英語版 English","EN · v2")}</div>
<p class="hub__meta">Static HTML/CSS mockup for design sign-off. Items marked <span class="tbd">要確認 / TBC</span> are placeholders awaiting client input (MOQ, lead times, country list, booth number, factory details, etc.). The English edition follows the brief's EN-only rules: no registered capital or bank list, no consumer store links, non-literal brand line, international phone format.</p>
</div></div></body></html>'''

def build():
    global L, VERSION, ASSETS, IMG
    for VERSION, base, ASSETS in (("2", ROOT, "../assets/"), ("2.1", os.path.join(ROOT, "v2.1"), "../../assets/"), ("2.2", os.path.join(ROOT, "v2.2"), "../../assets/")):
        IMG = ASSETS + "img/"
        for lang in ("ja", "en"):
            L = lang
            d = os.path.join(base, lang); os.makedirs(d, exist_ok=True)
            for fn, fn_ in PAGES.items():
                html = fn_()
                if lang == "ja":
                    html = add_wbr(html)
                with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"v{VERSION} {lang}/{fn:20} {len(html):>7} bytes")
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(hub())
    print("index.html (review hub)")
    import build_premium  # Direction B: reuses this module's data under its own name
    build_premium.build()

if __name__ == "__main__":
    build()
