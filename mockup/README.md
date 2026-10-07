# 花印 HANAJIRUSHI — Website Design Mockup

Static HTML/CSS mockup of the renewed corporate site, in Japanese and English,
built from `花印官网重点信息清单.docx` (content brief dated 2026-09-18).
Purpose: lock down the design before production build.

## How to view

Open `index.html` (review hub listing every page in both languages), or go
straight to `premium/ja/index.html` / `premium/en/index.html` (the chosen design). The 日本語 / English switch in the
header jumps to the same page in the other language.

Pages work from the file system, but Google Fonts and the embedded map need an
internet connection. For a local server:

```bash
python -m http.server 8765 --directory mockup
```

then open http://localhost:8765/

Tip: `ja/index.html#kv=3` (or `en/…`) opens the top carousel on slide 3 with autoplay off.

## Versions

| Version | Folder | Look |
|---|---|---|
| **Premium v1.5** | `premium-1.5/ja/`, `premium-1.5/en/`, `premium-1.5/cosmoprof-asia/` | Premium v1.4 with the client's second round (2026-10-07): the logo's magenta #D92070 in place of the crimson, and English pages without Japanese labels (see *Premium v1.5* below). |
| **Premium v1.4** | `premium-1.4/ja/`, `premium-1.4/en/`, `premium-1.4/cosmoprof-asia/` | Premium v1.3 with the client's change proposal (2026-10-07): the official logo, the client's brand-page text and message, one button per slide, a store chooser on product pages, fewer product spec rows, no history for now (see *Premium v1.4* below). |
| **Premium v1.3** | `premium-1.3/ja/`, `premium-1.3/en/`, `premium-1.3/cosmoprof-asia/` | Premium v1.2 with the reviewer's changes (意見まとめ.xlsx, 2026-10): brighter (white, V1 crimson), new menu order, separate Brand and Products pages, a products list plus one page per product from the Rakuten store, a large-image home slider, a short partnership section (see *Premium v1.3* below). |
| **Premium v1.2** | `premium-1.2/ja/`, `premium-1.2/en/`, `premium-1.2/cosmoprof-asia/` | Premium v1.1 plus a standalone Cosmoprof Asia buyer page for the booth QR code, and a home slider for news (see *Premium v1.2* below). |
| **Premium v1.1** | `premium-1.1/ja/`, `premium-1.1/en/` | Premium v1 plus the fixes and motion from the 2026-10 review (see *Premium v1.1* below). |
| **Premium v1** (chosen, 2026-10) | `premium/ja/`, `premium/en/` | 9 pages (海外展開 is a section of 代理店募集) and a short 5-item menu. Premium look (see below) with the v2.2 business content: business-first hero, 「日本製」4つの強み, ビジネスパートナーに選ばれる理由, figures, topic-based contact buttons. |
| **v2.2** (soft + business) | `v2.2/ja/`, `v2.2/en/` | v2.1 look plus buyer-conversion content (internal feedback 2026-10): new first view (who we are / how to do business, trust strip), 「日本製」4つの強み, ビジネスパートナーに選ばれる理由, numbers in Global & Partners, and topic-based contact buttons (`contact.html?topic=partner|product|oem|business&item=pN` pre-selects the form). Unconfirmed claims (manufacturing site, QC, sales results, deal and partner counts) are marked 要確認. |
| **v2.1** (soft) | `v2.1/ja/`, `v2.1/en/` | Softer, calmer, more refined: dusty rose `#A24A63`, Shippori Mincho headings at medium weight, Zen Kaku Gothic New body, Cormorant Garamond for Latin display words, tints and thin rules instead of solid rose blocks. Built from internal feedback (2026-10) asking for something closer to the current official site / V1 demo. |
| **v2** (current) | `ja/`, `en/` | Rose `#C8235F`, bold Noto Sans JP / Montserrat, solid rose accents. |

### Premium — the chosen direction

Started as "Direction B", a 3-page stretch proposal; the client team chose it
in 2026-10 and it is now built out to 9 pages in both languages.
Same copy, data and EN-only rules as v2.x (it imports them from `build.py`,
whose shared copy functions such as `JAPAN4()`, `WHY()`, `MODES()`, `TERMS()`,
`FAQ()` are defined once); only the markup and skin differ:
`_build/build_premium.py`, `assets/css/premium.css`, `assets/js/premium.js`.
`python _build/build.py` builds it too.

Business content (internal feedback 2026-10):

- **Hero:** 「世界へ届ける、日本品質のスキンケア製品。」 / "Japanese-quality
  skincare, delivered to the world." with 「日本で開発・製造。」 and a 製造地 要確認 chip.
- **Menu (feedback 「菜单不要太多」, matched to the V1 demo):** ブランド・製品 /
  代理店募集 / 企業情報 / お知らせ, a highlighted *Cosmoprof Asia* link (remove
  after the show) and the お問い合わせ button. Secondary pages sit under a parent:
  IPコラボ under ブランド・製品, 研究開発・品質 under 企業情報. They are reached from
  the parent page's section bar (→ link), the breadcrumb, indented sub-links in
  the phone menu, and the footer. The former 海外展開 page is now the
  `#network` and `#china` sections of 代理店募集.
- **Home order:** hero → figures → 「日本製」4つの強み (plum band, kanji in gold
  rings: 研・造・質・績) → collection → 選ばれる理由 → IP collaborations →
  partnership (with figures) → news & exhibition → company → stores.
- **Topic buttons:** `contact.html?topic=partner|product|oem|business`, plus
  `&item=p1…p4` from product pages. The contact form pre-selects the enquiry
  type and product (`premium.js`). The same set of four sits in the contact
  band on every page.
- Unconfirmed claims (manufacturing site, QC, sales data, deal and partner
  counts) stay marked 要確認 (景品表示法).

Premium here comes from craft rather than empty space:

- **Colour:** warm kinari paper `#F7F2EC` with a faint washi grain, one deep plum
  band per page `#2D2226`, and the brand pink kept as a softened 薄紅 accent
  (`#B4677C` decorative, `#94485E` for text). Text colours pass WCAG AA.
- **Type:** Zen Old Mincho for Japanese display (vertical 縦組み headings),
  Bodoni Moda for Latin display, Noto Sans JP light body, Jost spaced capitals.
- **Motifs:** 円窓 round-window product frames with a gold ring, arch-topped
  photographs, and the 花印 seal (落款) as the recurring brand mark (the name
  itself means "flower seal").
- **Motion:** slow zoom on heroes, fade-up reveals, line-wipe buttons; all off
  under `prefers-reduced-motion`.
- **Photos:** the existing site photos, colour-graded in CSS to sit together.
  They are small (440px product shots), so a real shoot is the biggest
  remaining upgrade for this direction.

### Premium v1.1

Same pages and copy as v1; every difference is gated by `V11()` in
`_build/build_premium.py` (v1 output does not change), and v1.1 pages load
`assets/css/premium-v11.css` + `assets/js/premium-v11.js` after the v1 files.

Fixes from the review:

- English hero headline in three balanced lines (was five).
- No empty product slot: products without a photo get one line under the grid.
- Home partnership: the map column stays in view while the text scrolls.
- Home company: a plum band with the head office in an arch, instead of the
  grey full-width street photo.
- Each photo used once: R&D, collaboration and partners no longer reuse
  other pages' header photos (R&D and collaboration use the plain header,
  partners uses the world map); the lab photo sits in a 円窓 sized to its
  resolution; the company page shows a portrait placeholder (代表者写真 要確認)
  and the office gallery no longer repeats the lab and showroom.
- Footer: 海外展開・販売実績 listed under お取引について.

Motion (restrained; all of it off under `prefers-reduced-motion`):

1. **Opening, home only, once per visit** (`html.intro`, set in `<head>` with
   `sessionStorage`): the gold ring draws round, the 円窓 opens like an iris,
   the vertical headline is brushed in column by column (English: lines rise),
   the 花印 seal stamps in, then the text, header and exhibition note. ~2.5 s.
   Repeat visits get a short fade.
2. **Images:** 円窓 open as an expanding circle with the ring drawn in; arch
   photos rise like a curtain; square photos and the map wipe in; list items
   follow the existing stagger. Lower-page headers: the photo wipes in and the
   large kanji is brushed in.
3. **Headings** are revealed line by line (`.ln` spans; the generator splits
   headings on `<br>`).
4. **Figures** (12ヵ国, 2015年) count up once.
5. **Page changes** cross-fade with the View Transitions API (Chrome, Edge,
   Safari; other browsers load pages as before).

### Premium v1.2 — Cosmoprof Asia buyer page

Coworker feedback (2026-10): the show page should be a standalone page, like the
V1 demo's `cosmoprof-asia/`, because visitors open it by scanning a QR code at the
booth. v1.2 = v1.1 plus that page; gated by `V12()` (v1 and v1.1 output unchanged).

- **Address:** `premium-1.2/cosmoprof-asia/` — `index.html` is English (the address
  the QR code opens), `ja.html` is Japanese; `?lang=ja` / `?lang=en` also work, as in V1.
- **Phone first:** slim sticky header (logo, show name, JA/EN, booking button), no
  site menu, a booking bar fixed to the bottom on phones, no large background photo.
- **Content:** show facts (dates, venue, booth, languages — 要確認), the three
  products with *Discuss this product* (ticks it in the form below), 「日本製」4つの強み,
  cooperation models and trade terms at a glance, export documents, next steps, one
  booking-and-enquiry form (preferred day and time as free input, confirmed by staff
  by reply; no slot grid to maintain), show contacts and downloads, and a
  share block: the page address, copy link and a QR code drawn in the browser from
  the page's own address (qrcode.js from cdnjs), so it works wherever the mockup is
  hosted. The QR printed for the booth must be generated from the final public URL.
- **Site links (v1.2):** the header's *Cosmoprof Asia* item, the home hero note and the
  show cards open the buyer page. 展示会情報 is a list of exhibitions: each upcoming
  show links to its own buyer page (one form, not two), and past exhibitions are listed
  once confirmed (要確認 for now). The home news section has no separate show card;
  the slider carries the show.
- Files: `assets/css/premium-lp.css`, `assets/js/premium-lp.js` (plus the v1 and v1.1 files).

**Home slider (v1.2, feedback 2026-10: keep the home slides for 展会・产品发布・专利获得):**

- The first view is a slider. Slide 1 is the brand/business hero, unchanged (with the
  first-visit opening); then 展示会 (Cosmoprof Asia → the buyer page), 新製品 (Cleansing
  Oil, launch date 要確認) and 特許 (Deep Cleansing Lotion, patent number 要確認).
  Announcement slides use a product 円窓 or a plum 円窓 holding a kanji (出展, 新), as
  there are no photos for them yet.
- Slides cross-fade; on entry the window opens, the ring is drawn and the lines rise.
  Desktop: one row of labelled tabs with a 2px progress line, plus a pause button (tabs
  and arrow keys change slides; no arrows, count or scroll cue, so the strip has one
  job). Phones: 01 / 04 count and bars under the header, pause, swipe. Slide 1 stays 8 s, the others 7 s; nothing moves on by itself under
  reduced motion. The small exhibition note under the v1.1 hero is replaced by the
  exhibition slide.
- Files: `assets/css/premium-v12.css` (every v1.2 site page), `assets/js/premium-v12.js` (home page only).

### Premium v1.5 — the client's second round (2026-10-07)

v1.4 plus three requests (in Chinese, relayed by the user). Gated by `V15()` in
`_build/build_premium.py`; v1–v1.4 output does not change. Files: `assets/css/premium-v15.css`,
`assets/img/world_map_v15.png` (the sales map in the new colour, converted from Adobe RGB to sRGB).

- **The logo's red** (「用logo的红色，替换现有的红色」, LOGO－2020版 06): magenta `#D92070` replaces the
  crimson `#A51D34` for buttons, bands, the seal, lines and the map. Text uses `#CC1E69`, a hair
  darker, so it keeps WCAG AA on the grey bands (4.9:1); white on `#D92070` is 4.8:1.
- **English pages in English** (「英语页面里存在的日语部分，试试用英语替代」) and **no repeats**
  (「重复的话，可以不显示」): no small Japanese line under page titles, section headings, menu items,
  region, model and quality labels. The faint word behind each page title is English and differs from
  the title (Bloom, Skincare, Ginza, Lab, Co-create, Grow, Meet us, Updates, Hello). Word stamps are
  English (Patent, Expo, Join us); 一二三 are I II III; the 日本製 circles carry icons; the exhibition
  slide's circle says Hong Kong.
- **Kept in Japanese on English pages** (agreed with the user): the 日本語 switch, the logo, product
  names and ingredient lists as printed on the pack, the legal company name, and the slogan
  ひとりに、ひとつの、キレイを咲かせる。 with an English line under it (*Helping every person's own
  beauty bloom.* — our draft for the client to check).
- Japanese pages change colour only.

### Premium v1.4 — the client's change proposal (2026-10-07)

v1.3 plus the changes the client marked on screenshots of v1.3 and the text in
ブランドページ文字案.docx (`~/Downloads/LOGO－2020版/change proposal/`). Gated by `V14()` in
`_build/build_premium.py`; v1–v1.3 output does not change. Files: `assets/css/premium-v14.css`,
`assets/js/premium-v14.js` (store chooser), `assets/img/logo_mark.png` / `logo_mark_w.png` (cropped
from the client's LOGO－2020版 files).

- **Official logo only** (「LOGOは正式のものしか使えないです」): the drawn 花印 seal is now the official
  square mark (magenta; the white-square version on the crimson contact band of the home page). Word
  stamps (特許, 出展, 募集中) are not the logo and stay — to confirm with the client.
- **Home:** one button per slide (the first); no 無香料・無着色… line under the products.
- **Brand** (`brand.html`): the client's text — header lead, BRAND CONCEPT, **OUR VALUES** (five values,
  in place of the five free-from circles: 「用以下内容代替」), BRAND STORY (fills the three placeholders);
  the IP collaborations block moved to the products page. English is our draft for the client to check.
- **Products:** no free-from line; the IP collaborations block is at the foot of the list.
- **Product page:** 「この製品を購入する」 opens a choice of stores (楽天市場 = the product's Rakuten page;
  Amazon, Yahoo!ショッピング, Qoo10 marked URL 要確認 until the client sends the addresses). The details
  table keeps 製品名, 内容量, 原産国, 全成分, JANコード (区分, 使用期限, 入数・ケースサイズ, 製造販売元 removed).
- **Company:** the client's representative message (English is our draft), no portrait; 沿革 is on hold
  (「保留」) — hidden from the page, the in-page links and the footer.
- **To confirm:** the representative's name; whether the magenta logo should change the site's crimson;
  the Amazon / Yahoo / Qoo10 store addresses; the English drafts.

### Premium v1.3 — reviewer feedback (意見まとめ.xlsx)

v1.2 plus the reviewer's changes; gated by `V13()` in `_build/build_premium.py`, so v1–v1.2
output does not change. Files: `assets/css/premium-v13.css` (loaded last),
`assets/js/premium-v13.js` (products filter), `_build/catalog.py` (product data).

- **Brighter, closer to V1:** white paper (no washi grain), V1's light grey `#F6F5F3` for
  bands, V1's crimson `#A51D34` for the seal, accents and filled buttons. The former plum
  bands are light; the contact band at the foot of every page is crimson (as in V1); the
  footer is light. Photos are no longer graded down.
- **Menu:** TOP／ブランド／製品／会社情報／お知らせ／パートナーシップ／Cosmoprof Asia／お問い合わせ.
  IPコラボ sits under ブランド, 研究開発・品質 under 会社情報.
- **Brand** (`brand.html`) is brand only: philosophy, a ブランドストーリー section holding three
  places for the client's text (due 5 Oct 2026, marked 要確認), research, IP collaborations.
- **Products** (`products.html`): every product as a card, filtered by category (with
  counts; `?cat=` opens it filtered). **One page per product**
  (`product-<slug>.html`), in the order of V1's product page: photo and buttons, features,
  how to use, research, details (accordion: product information, full ingredients,
  cautions, export documents), more products. JA has 楽天市場で購入する (the item's
  Rakuten page); EN has trade enquiry buttons only (EN_ONLY rule).
- **Product data** comes from the official Rakuten store (13 products + the Cleansing Oil,
  coming soon), condensed: no rankings or sale wording, no absorption claims; the
  quasi-drug eye cream keeps to its approved claims. Adding a product = one entry in
  `catalog.PRODUCTS13()`. Photos: our own packshots where we have them, otherwise the
  Rakuten image is **linked** (not copied; some show shop banners) — a note on the
  products page says they are temporary.
- **Home:** a slider of large images (brand, Cosmoprof Asia, Hatomugi series, patent) —
  existing site photos stand in until the client sends brand / new-product images; figures
  strip; news; featured products with category chips; brand; 日本製の強み; collaborations;
  a short partnership section (no trade-deal or partner counts, as asked); company.
  選ばれる理由 is no longer on the home page (it stays on パートナーシップ).
- **Partnership figures** no longer show trade-deal or partner counts (countries, regions
  and founding year only).
- **Home slider height:** about three quarters of the screen on desktop (620–720px, close to
  V1's 650/760px) and on phones (smaller visual, kanji circle and type, tighter spacing);
  tablets held sideways keep text and visual side by side.
- **Review fixes (2 Oct):** product cards put the 新商品／近日公開 tag on the photo and 花印 on a
  small line above the name; the how-to-use row on product pages is compact; the contact band
  has its seal above the heading; the brand philosophy arch uses the flower-wall photo; the home
  company photo is smaller on phones; the products page links to the IP collaborations instead
  of repeating them. Fixed: some English product pages showed Japanese tags and how-to-use text.
- **To confirm:** every Rakuten listing names a third-party 製造販売元 (manufacturer), while
  the site copy says HANAJIRUSHI does its own manufacturing — check before publishing. The
  manufacturer row on each product page is 要確認. Ingredient lists were copied from Rakuten
  with obvious typos corrected; check them against the packs.

**Also in v1.2 (all pages):** the two flower photographs (home background, brand header)
are graded down to the palette; the phone menu keeps a solid header while open (the list
used to scroll under the logo), JA / EN sits in the phone header, the drawer keeps only
the phone number and the show card (address and company name are in the footer), and
its links fade up in turn. Very small phones (320 px) no longer overflow.


v2 and v2.1 have identical pages and content; v2.1 only adds `assets/css/soft.css`
(type and colour overrides, loaded after `style.css`) and a different font set.
`python _build/build.py` builds all three. v2.2 content changes are gated by `V22()` in the generator; v2.2 also uses `soft.css`. Once one is chosen, either delete the other
folder, or fold `soft.css` into `style.css` and drop the version switch in the generator.

## Design

Both editions use a **local Japanese corporate** style: dense layout, bold
Gothic headings, banner carousel with stamps/medals, laurel badges, tinted
section bands, table-style forms, fixed side tabs and a mobile bottom bar.

The English edition keeps the Japanese look (kanji labels under English
headings, kanji-plus-English stamps such as 出展 EXHIBITING) and follows the
brief's English-only rules:

| Rule | JA | EN |
|---|---|---|
| Registered capital, bank list | shown | removed |
| Consumer store links (Rakuten, Amazon, Yahoo!, Qoo10) | shown | replaced by "Find / become a distributor" |
| Product price line | 希望小売価格 (TBC) | Trade price: on request |
| Product buttons | 購入する | Enquire / Trade enquiry |
| Brand line | ひとりに、ひとつの、キレイを咲かせる。 | "Clean formula. Gentle by design. Made in Japan." (rewritten, original kept as a small accent) |
| Phone / address | 03-6264-2154, 〒 first | +81-3-6264-2154, Ginza first |
| Corporate structure note | — | on Company page |
| Contact form | WhatsApp/WeChat, market, volume optional | required (qualifies overseas leads) |

## Structure

```
mockup/
├── index.html            review hub
├── ja/                   Japanese edition (10 pages)
├── en/                   English edition (10 pages, same file names)
├── assets/
│   ├── css/style.css     shared stylesheet
│   ├── js/main.js        carousel, news tabs, slot picker, sp menu, page top
│   └── img/              photos & product shots pulled from hanajirushi.co.jp
│                         + world_map_brand.png (existing map recoloured)
├── premium/              chosen design (9 pages × JA/EN), premium.css + premium.js
└── _build/build.py       generator for all pages + review hub
    _build/build_premium.py  premium generator (reuses build.py copy & data)
    _build/catalog.py        v1.3 product catalogue (from the Rakuten store)
```

Pages: Top · Brand/Products · Company · R&D & Quality · Collaboration ·
Global · For Partners · Exhibition · News · Contact.

## Editing copy

Edit `_build/build.py`, then run `python _build/build.py` to regenerate
everything (21 HTML files). Requires BudouX (`pip install budoux`): the build
inserts `<wbr>` between Japanese phrases so every browser, including Safari on
iPhone, wraps lines between phrases instead of mid-word.

The logo (`assets/img/logo.svg`) is the client's own HANAJIRUSHI / 花印 wordmark
from hanajirushi.co.jp, recoloured from white to dark grey for light backgrounds. Copy sits side by side as `t("日本語", "English")`. Shared data
(products, IP collaborations, news, export documents, registration markets) is
defined once near the top and reused across pages. English-only rules are
marked with `EN_ONLY` comments.

## Moving to WordPress

See [WORDPRESS.md](WORDPRESS.md) for the production plan: content types,
fields, which parts staff can edit, language rules and the mapping from this
mockup's generator to WordPress templates.

## Placeholders

Anything the client has not yet confirmed is shown as a dashed chip
(`要確認` / `TBC`): MOQ, lead times, 12-country list, booth number, show dates,
factory & certifications, patent numbers, INCI lists, shelf life, JAN codes,
case packs, retail prices, representative's name and message, history dates,
China operating company, contact names/WhatsApp/WeChat, and the Cleansing Oil
product details/image. News headlines are sample copy. Forms are disabled
(v2.x: alert on submit; premium: a short notice).
