# -*- coding: utf-8 -*-
"""
Copy what the WordPress theme and plugin share with the mockup, so the mockup stays the
source of truth for the design and the starter content.

Run:  python wordpress/dev/sync.py

  theme   hanajirushi/assets/css, js, img   <- mockup/assets (premium v1.3 stack only)
  plugin  hanajirushi-core/seed/seed.json   <- mockup/_build/catalog.py + build.py data
          hanajirushi-core/seed/img/        <- photos the starter content uses
          hanajirushi-core/inc/budoux-ja.json <- the BudouX Japanese model (Apache-2.0)

The seed is plain data (no HTML except the catch-line breaks, written as new lines), in
both languages. The plugin's 初期データ tool imports it (Tools → 花印 初期データ).
"""
import html, json, os, re, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WP = os.path.dirname(HERE)
ROOT = os.path.dirname(WP)
MOCK = os.path.join(ROOT, "mockup")
THEME = os.path.join(WP, "hanajirushi")
PLUGIN = os.path.join(WP, "hanajirushi-core")

sys.path.insert(0, os.path.join(MOCK, "_build"))
import build as b          # noqa: E402  (mockup copy and data; t() follows b.L)
import catalog as cat      # noqa: E402

CSS = ["premium.css", "premium-v11.css", "premium-v12.css", "premium-v13.css", "premium-lp.css"]
JS = ["premium.js", "premium-v11.js", "premium-v12.js", "premium-v13.js", "premium-lp.js"]
THEME_IMG = ["logo.svg", "rakuten.svg", "amazon.png", "yahoo.svg", "qoo10.png", "world_map_brand.png",
             "h_brand_top_p.jpg", "h_campany_bldg.jpg", "h_campany_lab.jpg", "h_campany_top_p.jpg",
             "h_campany_sr.jpg", "h_campany_dr.jpg", "h_campany_ent.jpg", "h_hanajirushi_top-1.jpg",
             "hanajirushi_hsc.jpg"]


def copy_assets():
    for sub, names in (("css", CSS), ("js", JS), ("img", THEME_IMG)):
        dst = os.path.join(THEME, "assets", sub)
        os.makedirs(dst, exist_ok=True)
        for n in names:
            shutil.copy2(os.path.join(MOCK, "assets", sub, n), os.path.join(dst, n))
    import budoux
    src = os.path.join(os.path.dirname(budoux.__file__), "models", "ja.json")
    shutil.copy2(src, os.path.join(PLUGIN, "inc", "budoux-ja.json"))


# ------------------------------------------------------------------ text clean-up
def plain(x):
    """Mockup HTML -> plain text for a field: <br> becomes a new line, tags go, entities decode."""
    if x is None:
        return ""
    x = re.sub(r"<br\s*/?>", "\n", x)
    x = re.sub(r"<[^>]+>", "", x)
    return html.unescape(x).strip()


def both(fn):
    """Call fn() once per language; returns (ja, en)."""
    out = []
    for lang in ("ja", "en"):
        b.L = lang
        out.append(fn())
    b.L = "ja"
    return out


# ------------------------------------------------------------------ products
def products():
    ja, en = both(cat.PRODUCTS13)
    out = []
    for i, (p, e) in enumerate(zip(ja, en)):
        img = p["img"]
        out.append({
            "slug": p["slug"], "order": i + 1, "category": p["cat"], "series": p["series"] or "",
            "size": p["size"] or "", "kind": "quasi" if p["kind"] == "医薬部外品" else ("cosmetic" if p["kind"] else ""),
            "is_new": bool(p["new"]), "coming_soon": bool(p["soon"]),
            "show_on_home": p["slug"] in cat.FEATURED, "home_order": cat.FEATURED.index(p["slug"]) + 1 if p["slug"] in cat.FEATURED else 0,
            "rakuten_code": p["rk"] or "", "image": img or "", "image_temp": "" if img else (p["rimg"] or ""),
            "ja": {"title": plain(p["name"]), "sub": plain(p["sub"]), "short": plain(p["short"]), "catch": plain(p["catch"]),
                   "desc": plain(p["desc"]), "usage": plain(p["usage"]), "inci": plain(p["inci"]),
                   "badges": "\n".join(plain(x) for x in p["badges"]), "free": "\n".join(plain(x) for x in p["free"]),
                   "points": [{"title": plain(h), "text": plain(d)} for h, d, _ in p["points"]]},
            "en": {"title": plain(e["name"]), "sub": plain(e["sub"]), "short": plain(e["short"]), "catch": plain(e["catch"]),
                   "desc": plain(e["desc"]), "usage": plain(e["usage"]), "inci": "",
                   "badges": "\n".join(plain(x) for x in e["badges"]), "free": "\n".join(plain(x) for x in e["free"]),
                   "points": [{"title": plain(h), "text": plain(d)} for h, d, _ in e["points"]]},
        })
    return out


# ------------------------------------------------------------------ home slides (premium v1.3 SLIDES13)
def slides():
    """Field for field the kv_slide post type. Links are site paths; the plugin adds /en."""
    return [
        {"order": 1, "visual": "none", "eyebrow": "Hanajirushi · Ginza, Tokyo", "bg": "h_hanajirushi_top-1.jpg", "bg_pos": "70% center",
         "btn1_link": "/products/", "btn2_link": "/brand/",
         "ja": {"tab": "花印について", "label": "", "heading": "ひとりに、ひとつの、\nキレイを咲かせる。", "accent": False,
                "text": "東京・銀座の自社研究室で開発する、\n無香料・無着色の日本製スキンケア。", "btn1": "製品を見る", "btn2": "ブランドについて"},
         "en": {"tab": "Hanajirushi", "label": "", "heading": "Clean formula.\nGentle by design.\nMade in Japan.", "accent": True,
                "text": "Skincare formulated in our own laboratory in Ginza, Tokyo — sold in Japan and 12 countries.",
                "btn1": "View products", "btn2": "About the brand"}},
        {"order": 2, "visual": "kanji", "kanji": "出展", "kanji_caption": "Hong Kong 2026", "bg": "h_campany_top_p.jpg", "bg_pos": "center 40%",
         "btn1_link": "/cosmoprof-asia/", "btn2_link": "",
         "ja": {"tab": "展示会", "label": "展示会", "heading": "Cosmoprof Asia 2026に\n出展します。", "accent": True,
                "text": "2026年11月、香港コンベンション＆エキシビションセンター。ブースでの商談のご予約を受け付けています。",
                "btn1": "展示会専用ページへ", "btn2": ""},
         "en": {"tab": "Exhibition", "label": "Exhibition", "heading": "Meet us at\nCosmoprof Asia 2026", "accent": True,
                "text": "November 2026, Hong Kong Convention & Exhibition Centre. Meetings at our booth can be booked now.",
                "btn1": "Open the event page", "btn2": ""}},
        {"order": 3, "visual": "products", "products": ["hatomugi-skin-conditioner", "hatomugi-essence", "hatomugi-cream"], "bg": "",
         "btn1_link": "/products/hatomugi-essence/", "btn2_link": "/products/hatomugi-cream/",
         "ja": {"tab": "ハトムギシリーズ", "label": "新商品", "heading": "ハトムギシリーズに、\n美容液とクリーム。", "accent": True,
                "text": "ハトムギ化粧水と一緒に使える、ハトムギ豊潤美容液（200mL）とハトムギクリーム（100g）。",
                "btn1": "美容液を見る", "btn2": "クリームを見る"},
         "en": {"tab": "Hatomugi series", "label": "New", "heading": "The Hatomugi series\nadds a serum and a cream.", "accent": True,
                "text": "Hatomugi Rich Essence (200mL) and Hatomugi Cream (100g), made to go with the Hatomugi lotion.",
                "btn1": "See the essence", "btn2": "See the cream"}},
        {"order": 4, "visual": "product", "product": "cleansing-lotion-ma", "seal": "特許", "bg": "h_brand_top_p.jpg", "bg_pos": "center",
         "btn1_link": "/products/cleansing-lotion-ma/", "btn2_link": "",
         "ja": {"tab": "特許", "label": "特許", "heading": "特許技術を採用した、\nクレンジングローション。", "accent": True,
                "text": "うるおい残してしっかり落ちる、拭き取りタイプのクレンジングローション。", "btn1": "製品を見る", "btn2": ""},
         "en": {"tab": "Patent", "label": "Patent", "heading": "A cleansing lotion\nwith patented technology.", "accent": True,
                "text": "A wipe-off cleansing lotion that removes make-up and leaves moisture behind.", "btn1": "View the product", "btn2": ""}},
    ]


# ------------------------------------------------------------------ IP collaborations, news, settings
def collabs():
    ja, en = both(b.IPS)
    return [{"order": i + 1, "image": j[0], "ja": {"title": plain(j[1]), "product": plain(j[2]), "label": plain(j[3]), "channel": plain(j[5])},
             "en": {"title": plain(e[1]), "product": plain(e[2]), "label": plain(e[3]), "channel": plain(e[5])}}
            for i, (j, e) in enumerate(zip(ja, en))]


NEWS_CATS = [("exh", "展示会", "Exhibition"), ("info", "お知らせ", "Notice"), ("biz", "企業情報", "Business"), ("prod", "製品情報", "Product")]


def news():
    ja, en = both(b.NEWS)
    return [{"date": j[0].replace(".", "-"), "cat": j[1], "ja": {"title": plain(j[4])}, "en": {"title": plain(e[4])}}
            for j, e in zip(ja, en)]


def settings():
    b.L = "ja"
    ja = dict(company=plain("花印粧業研究所株式会社"), tel=b.TEL(), fax=b.FAX(), hours=plain(b.HOURS()), address=plain(b.ADDR(True)),
              founded="2015年1月28日")
    b.L = "en"
    en = dict(company="Hanajirushi Institute of Cosmetics, Inc.", tel=b.TEL(), fax=b.FAX(), hours=plain(b.HOURS()),
              address=plain(b.ADDR(True)), founded="28 January 2015")
    b.L = "ja"
    return {"ja": ja, "en": en, "show_tbc": True}


# ------------------------------------------------------------------ fixed page copy (theme)
# The mockup's shared copy, in both languages, for the theme's fixed page text. 要確認 chips
# become ［…］ markers, which the site shows as the mark or leaves out (サイト設定 → 表示).
COPY = ["BIZ_TYPES", "BOOKING_TOPICS", "BUSINESS", "COLLAB_CATCH", "COLLAB_P1", "COLLAB_P2", "COLLAB_VALUES",
        "EXH_INTRO", "EXH_ONSHOW", "EXPORT_DOCS", "JAPAN4", "KINDS_V22", "MODELS_MINI", "MODES", "OFFICE_PHOTOS",
        "PARTNER_LEAD", "PARTNER_TEXT", "PARTNER_STEPS", "RD_CATCH", "RD_P1", "RD_P2", "RD_TAGS", "RD_STEPS",
        "REGIONS", "REGS", "REG_SUPPORT", "STRUCTURE_EN", "VOLUMES", "REASONS", "FREE_FROM", "PRODUCT_LINES"]
COPY += [f"CHINA{i}_{x}" for i in range(1, 5) for x in "TSB"] + [f"QUALITY{i}_{x}" for i in range(1, 4) for x in "TSB"]
COPY += [f"RD_POINT{i}_{x}" for i in range(1, 4) for x in "TD"] + [f"PARTNER_REASON{i}_{x}" for i in range(1, 4) for x in "TD"]

TBD = re.compile(r'<span class="tbd(?: tbd--w)?">(.*?)</span>')


def marks(x):
    """Mockup 要確認 chips -> ［…］ markers, recursively."""
    if isinstance(x, str):
        return TBD.sub(lambda m: "［" + m.group(1) + "］", x)
    if isinstance(x, (list, tuple)):
        return [marks(v) for v in x]
    return x


def copy_data():
    out = {}
    for lang in ("ja", "en"):
        b.L = lang
        out[lang] = {n: marks(getattr(b, n)()) for n in COPY}
    b.L = "ja"
    return out


def text(x):
    """A field value: plain text with ［…］ markers, <br> as new lines."""
    return plain(marks(x))


def settings_more():
    """Editable parts of サイト設定 (company table, message, history, trade terms, FAQ, show contacts)."""
    out = {}
    for lang in ("ja", "en"):
        b.L = lang
        rows = re.findall(r"<tr><th>(.*?)</th><td>(.*?)</td></tr>", b.company_rows(full=True))
        out[lang] = {"rows": [(text(a), text(v)) for a, v in rows], "history": [(text(a), text(v)) for a, v in b.HISTORY()],
                     "terms": [(text(a), text(v)) for a, v in b.TERMS()], "faq": [(text(q), text(a)) for q, a in b.FAQ()],
                     "message": text(b.MESSAGE_PH()), "stations": text(b.STATIONS())}
    b.L = "ja"
    ja, en = out["ja"], out["en"]
    # the company table: capital and banks are Japanese only (EN_ONLY), so rows are matched by label
    en_rows = dict(en["rows"])
    match = {"社名": "Company name", "創業": "Founded", "本社所在地": "Head office", "TEL / FAX": "TEL / FAX", "代表者": "Representative",
             "資本金": None, "事業内容": "Business", "販売地域": "Markets", "取引銀行": None, "法人番号": "Corporate number"}
    rows = []
    for a, v in ja["rows"]:
        e = match.get(a)
        rows.append({"label": a, "value": v, "label_en": e or "", "value_en": en_rows.get(e, "") if e else ""})
    return {
        "profile_rows": rows,
        "history": [{"date": a, "text": v, "date_en": c, "text_en": d} for (a, v), (c, d) in zip(ja["history"], en["history"])],
        "terms": [{"label": a, "value": v, "label_en": c, "value_en": d} for (a, v), (c, d) in zip(ja["terms"], en["terms"])],
        "faq": [{"q": a, "a": v, "q_en": c, "a_en": d} for (a, v), (c, d) in zip(ja["faq"], en["faq"])],
        "message": ja["message"], "message_en": en["message"],
        "rep_title": "代表取締役", "rep_title_en": "Representative Director", "rep_name": "［氏名］", "rep_name_en": "［Name TBC］",
        "stations": ja["stations"] + "［分数］", "stations_en": en["stations"] + "［min TBC］",
        "show_contact": "［氏名］", "show_whatsapp": "［番号］", "show_wechat": "［ID］", "show_email": "export@hanajirushi.co.jp ［要確認］",
    }


def exhibitions():
    b.L = "ja"
    ja_on = plain(b.EXH_ONSHOW())
    b.L = "en"
    en_on = plain(b.EXH_ONSHOW())
    b.L = "ja"
    return [{"slug": "cosmoprof-asia-2026", "title": "Cosmoprof Asia 2026", "year": "2026", "month": "11月", "month_en": "Nov",
             "dates": "2026年11月 ［日程確定待ち］", "dates_en": "November 2026 ［TBC］",
             "venue": "香港コンベンション＆エキシビションセンター（香港・湾仔）", "venue_en": "Hong Kong Convention & Exhibition Centre, Wan Chai",
             "booth": "［確定待ち］", "booth_en": "［TBC］", "onshow": ja_on, "onshow_en": en_on,
             "languages": "日本語・英語・中国語 ［要確認］", "languages_en": "Japanese, English, Chinese ［TBC］",
             "status": "商談予約受付中", "status_en": "Booking meetings now", "page": "/cosmoprof-asia/", "end": "20261130"}]


def form_options():
    """Choices of the contact and booking forms (the plugin checks and mails them; the theme shows them)."""
    out = {"topics": list(b.CTA_TOPICS)}
    for lang in ("ja", "en"):
        b.L = lang
        out[lang] = {"kinds": [plain(x) for x in b.KINDS_V22()], "biz": [plain(x) for x in b.BIZ_TYPES()],
                     "volumes": [plain(x) for x in b.VOLUMES()], "lines": [plain(x) for x in b.PRODUCT_LINES()[3:5]],
                     "days": ["会期1日目", "会期2日目", "会期3日目", "会期外・オンラインを希望"] if lang == "ja" else ["Day 1", "Day 2", "Day 3", "After the show / online"]}
    b.L = "ja"
    return out


# Pages the theme has templates for (page-<slug>.php): slug, Japanese title, English title, parent slug
PAGES = [("home", "トップ", "Top", ""), ("brand", "ブランド", "Brand", ""), ("collaboration", "IPコラボレーション", "IP collaborations", "brand"),
         ("company", "会社概要", "Company", ""), ("rd", "研究開発・品質", "R&D & quality", "company"),
         ("news", "お知らせ", "News", ""), ("partners", "海外代理店・パートナー募集", "Partnership programme", ""),
         ("exhibition", "展示会情報", "Exhibitions", ""), ("contact", "お問い合わせ", "Contact", ""),
         ("cosmoprof-asia", "Cosmoprof Asia 2026 商談ページ", "Cosmoprof Asia 2026 — Buyer page", "")]


def main():
    copy_assets()
    with open(os.path.join(THEME, "inc", "copy.json"), "w", encoding="utf-8") as fh:
        json.dump(copy_data(), fh, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(PLUGIN, "inc", "form-options.json"), "w", encoding="utf-8") as fh:
        json.dump(form_options(), fh, ensure_ascii=False, indent=1)
    seed_img = os.path.join(PLUGIN, "seed", "img")
    os.makedirs(seed_img, exist_ok=True)
    data = {"products": products(), "slides": slides(), "collabs": collabs(), "news_cats": NEWS_CATS,
            "news": news(), "settings": settings(), "settings_more": settings_more(), "exhibitions": exhibitions(),
            "pages": PAGES}
    files = {p["image"] for p in data["products"] if p["image"]} | {s["bg"] for s in data["slides"] if s["bg"]} | {c["image"] for c in data["collabs"]}
    for f in sorted(files):   # resized, so the plugin zip stays under common 2 MB upload limits
        im = Image.open(os.path.join(MOCK, "assets", "img", f)).convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(os.path.join(seed_img, f), quality=80, optimize=True, progressive=True)
    with open(os.path.join(PLUGIN, "seed", "seed.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print(f"seed: {len(data['pages'])} pages, {len(data['exhibitions'])} exhibitions, {len(data['products'])} products, {len(data['slides'])} slides, {len(data['collabs'])} collabs, "
          f"{len(data['news'])} news; {len(files)} images")


if __name__ == "__main__":
    main()
