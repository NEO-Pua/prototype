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
| **Premium** (chosen, 2026-10) | `premium/ja/`, `premium/en/` | All 10 pages. Premium look (see below) with the v2.2 business content: business-first hero, 「日本製」4つの強み, ビジネスパートナーに選ばれる理由, figures in Global & Partners, topic-based contact buttons. |
| **v2.2** (soft + business) | `v2.2/ja/`, `v2.2/en/` | v2.1 look plus buyer-conversion content (internal feedback 2026-10): new first view (who we are / how to do business, trust strip), 「日本製」4つの強み, ビジネスパートナーに選ばれる理由, numbers in Global & Partners, and topic-based contact buttons (`contact.html?topic=partner|product|oem|business&item=pN` pre-selects the form). Unconfirmed claims (manufacturing site, QC, sales results, deal and partner counts) are marked 要確認. |
| **v2.1** (soft) | `v2.1/ja/`, `v2.1/en/` | Softer, calmer, more refined: dusty rose `#A24A63`, Shippori Mincho headings at medium weight, Zen Kaku Gothic New body, Cormorant Garamond for Latin display words, tints and thin rules instead of solid rose blocks. Built from internal feedback (2026-10) asking for something closer to the current official site / V1 demo. |
| **v2** (current) | `ja/`, `en/` | Rose `#C8235F`, bold Noto Sans JP / Montserrat, solid rose accents. |

### Premium — the chosen direction

Started as "Direction B", a 3-page stretch proposal; the client team chose it
in 2026-10 and it is now built out to all 10 pages in both languages.
Same copy, data and EN-only rules as v2.x (it imports them from `build.py`,
whose shared copy functions such as `JAPAN4()`, `WHY()`, `MODES()`, `TERMS()`,
`FAQ()` are defined once); only the markup and skin differ:
`_build/build_premium.py`, `assets/css/premium.css`, `assets/js/premium.js`.
`python _build/build.py` builds it too.

Business content (internal feedback 2026-10):

- **Hero:** 「世界へ届ける、日本品質のスキンケア製品。」 / "Japanese-quality
  skincare, delivered to the world." with 「日本で開発・製造。」 and a 製造地 要確認 chip.
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
├── premium/              chosen design (10 pages × JA/EN), premium.css + premium.js
└── _build/build.py       generator for all pages + review hub
    _build/build_premium.py  premium generator (reuses build.py copy & data)
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
