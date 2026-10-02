# 花印 HANAJIRUSHI — WordPress Implementation Plan

How to turn this static mockup into the production WordPress site so that
**Hanajirushi staff can update news, products, the home slider and other
everyday content themselves**, without touching code or layout.

The promise made to the client (2026-10):

> 公開後は、お知らせ・商品情報・トップページのスライド・展示会情報・会社概要などを
> 貴社側で管理画面から追加・編集できます。日本語版・英語版も同じ管理画面から編集できます。
> ページ構成の変更や新しいコーナーの追加は制作側で対応します。

Everything below exists to keep that promise. If a design change would force
staff to edit HTML, it breaks the promise. Find another way.

---

## 1. Principles

1. **Staff fill in forms, the theme does the design.** Every repeating element
   (news item, product, slide, IP card, FAQ…) is a set of fields. The theme
   renders it with one shared template, exactly as `_build/build.py` does now.
2. **No page builders** (Elementor, etc.). They let staff break the layout and
   produce heavy markup. Use a custom theme with plain PHP templates.
3. **Reuse the mockup's CSS and JS as-is.** `assets/css/style.css` and
   `assets/js/main.js` are production-quality. The theme should output the
   same HTML structure and class names the mockup uses.
4. **One field = one fact.** No free-text fields that staff must format
   (no "type `<br>` here"). Line breaks, colours and layout come from the theme.
5. **Language rules are code, not editor discipline.** The English-only rules
   (§7) are enforced in templates so staff can't accidentally publish the
   capital or bank list in English.

---

## 2. Stack

| Need | Recommendation | Notes |
|---|---|---|
| Base | Fresh custom theme (`hanajirushi`) | Current site uses the LIQUID MAGAZINE theme; replace it, don't extend it. |
| Custom fields | **Advanced Custom Fields (ACF) Pro** | Repeater, Options Page, Flexible Content. Field groups exported to JSON in the theme (`acf-json/`) so they're version-controlled. |
| Custom post types | Register in theme code (`functions.php` / `inc/cpt.php`) | Not via a plugin UI, so the structure lives in git. |
| Bilingual JA/EN | **Polylang** (or Polylang Pro) | One post per language, linked as translations. URLs `/` (JA) and `/en/` (EN). Must support translating ACF Options pages (Polylang Pro + ACF, or store options per language, see §6). |
| Forms | **MW WP Form** or **Contact Form 7 + confirm add-on** | The design has a 入力 → 確認 → 完了 step bar, which MW WP Form supports natively and is the common choice in Japan. |
| Meeting booking | Custom form (MW WP Form) + slot field, or a booking plugin | See §5.7. |
| SEO | Yoast SEO (already used on the current site) | Per-language titles and descriptions. |
| Japanese line breaking | BudouX | See §8. |

Keep plugins to this list. Every extra plugin is something staff can
misconfigure and something that needs updating.

---

## 3. Content model overview

| Type | WordPress object | Edited by staff | Used on |
|---|---|---|---|
| お知らせ News | Built-in **Post** + category | ✅ often | Home news list, News page |
| 製品 Products | CPT `product` | ✅ sometimes | Home product cards, Brand page, Exhibition page |
| スライド Home slides | CPT `kv_slide` | ✅ often | Home carousel |
| IPコラボ Collaborations | CPT `collab` | ✅ occasionally | Home, Brand, Collaboration page |
| よくあるご質問 FAQ | CPT `faq` | ✅ occasionally | Partners page |
| 沿革 History | ACF repeater on Options | ✅ rarely | Company page |
| 会社情報・取引条件・展示会 etc. | **ACF Options pages** | ✅ when facts change | Many pages (see §6) |
| Page structure & static copy | Page templates + ACF fields on each Page | ⚠️ text only | All lower pages |

---

## 4. Custom post types in detail

Field names below are suggestions; keep them consistent with the mockup data
in `_build/build.py` (`PRODUCTS()`, `IPS()`, `NEWS()`, `slide()` calls) so the
migration is mechanical.

### 4.1 Home slides — `kv_slide`

The home page's first view is a slider (premium v1.2). **Slide 1** is the fixed
brand/business hero, edited on an Options page and always first. **Announcement slides**
(exhibitions, product launches, patents, campaigns) are `kv_slide` posts. Staff fill in
fields only; there is no HTML and no layout to touch, and the theme does the motion,
vertical text, colours and phone layout. In the mockup, `SLIDES()` in
`_build/build_premium.py` holds the same fields and `kv_slide()` prints them the way
`template-parts/kv-slide.php` will.

| Field | Type | Example (JA / EN) | Rules |
|---|---|---|---|
| `label` | Select (+ "Other" text) | 展示会 / Exhibition · 新製品 · 特許 · お知らせ · キャンペーン | Shown as the pill on the slide and as the tab name under the slider. |
| `line1` | Text | 特許技術を採用した、 / A cleansing lotion | Headline line 1. **Max 14 JA / 32 EN** (half-width characters count half; the admin shows a counter). |
| `line2` | Text | クレンジングローション。 / with patented technology. | Headline line 2, printed in the accent colour (JA: pink; EN: pink italic). Same limit. |
| `text` | Text (one line) | うるおい残してしっかり落ちる… | **Max 60 JA / 130 EN.** No line breaks. |
| `button_label` | Text | 製品を見る / View the product | Short; ≤ 12 JA / 24 EN. |
| `link` | Link (page picker or URL) | /brand/#p1, /cosmoprof-asia/ | Internal pages are picked, not typed. |
| `visual` | Radio | `product` / `kanji` / `photo` | Decides which of the next fields are shown. |
| `product` | Post object → `product` | Deep Cleansing Lotion | *visual = product*: its packshot is used automatically, inside the 円窓. |
| `kanji` + `caption` | Text (1–2 characters) + text | 出展 + Hong Kong 2026 | *visual = kanji*: the characters in a plum 円窓, set vertically, with a small Latin caption. |
| `photo` | Image (square crop) | | *visual = photo*: WordPress crops it square; at least 900 px. For photos that are not product shots. |
| `seal` | Text, optional (1–2 characters) | 特許 | A stamped 落款 on the visual. |
| `start_date` / `end_date` | Date, optional | 2026-09-15 / 2026-11-30 | The slide appears and disappears by itself (e.g. the exhibition slide after the show). |
| Order | `menu_order` | | Drag-and-drop order (e.g. *Simple Custom Post Order*). |

Theme rules (staff never see these):

- Headlines are printed as two lines, each in a masked span for the line reveal; long
  lines wrap inside their span, which is why the fields have limits.
- In Japanese headlines, runs of Latin letters (e.g. *Cosmoprof Asia 2026*) are set in
  Bodoni automatically and kept together with the following character.
- Polylang: each slide exists in JA and EN as linked translations; show a warning when
  one language is missing.
- Warn in the admin when more than 5 slides are live; visitors rarely see beyond the third.
- Timing (slide 1: 8 s, others: 7 s), pause, swipe and reduced-motion behaviour come from
  `premium-v12.js` and need no settings.
- The mockup's dashed 要確認 / TBC chips are not a field; they disappear in production.

v1 / v1.1 (no slider) and the earlier v2 banner carousel are superseded by this.

### 4.2 Products — `product`

| Field | Type | Example |
|---|---|---|
| Title | Post title | 花印ハトムギ化粧水 |
| `subtitle_en` | Text | Hatomugi Skin Conditioner (shown small under the title) |
| `category` | Taxonomy `product_cat` | 化粧水 / クレンジング / フェイスマスク |
| `labels` | Repeater: text + style (`rose`, `gold`, `gray`, `outline`, `ink`) | 大容量 (rose), 北海道産ハトムギ (outline) |
| `short_desc` | Textarea | Card text on Home/Brand |
| `catch` | Text | Rose lead line on the detail block |
| `description` | Textarea | Main body |
| `feature_tags` | Repeater (text) | 無香料 / 無着色 / 顔・全身 |
| `spec_chips` | Repeater (text) | 500mL / 無香料 (small grey chips on cards) |
| `volume` | Text | 500mL |
| `key_ingredients` | Text | ハトムギ種子エキス、ヨモギ葉エキス… |
| `ingredient_origin` | Text, optional | ハトムギ種子エキス：北海道産 |
| `patent` | Text, optional | 特許番号 |
| `inci` | Textarea | Full INCI list (B2B requirement) |
| `shelf_life_unopened` / `shelf_life_opened` | Text | |
| `jan` | Text | JAN / EAN code |
| `case_pack` | Text | 入数・ケースサイズ |
| `retail_price` | Text, **JA only** | 希望小売価格 (see §7) |
| `image` | Image | Square, ≥ 1000 px |
| `status` | Select | `published` / `coming_soon` (shows 近日掲載 label and placeholder image) |
| `show_on_home` / `show_at_exhibition` | True/False | Controls Home cards and Exhibition “出展製品” |

Empty B2B fields render as nothing, never as “undefined”. Before launch they
show the `要確認 / TBC` chip only on a staging site, never in production.

### 4.3 News — built-in Post

- Categories (slug → label JA / EN):
  `exh` 展示会 / Exhibition · `prod` 製品情報 / Product ·
  `biz` 企業情報 / Business · `info` お知らせ / Notice.
  The slugs drive the label colour and the home-page filter tabs (`data-cat`).
- The **NEW** mark is automatic: posts newer than 14 days (make the number an option).
- Home shows the latest 5; News page paginates by 10 with category and
  year-archive sidebar.
- Featured image optional (not shown in the current list design).

### 4.4 IP collaborations — `collab`

| Field | Type | Example |
|---|---|---|
| Title | Post title | 美少女戦士セーラームーン |
| `product` | Text | クレンジングローション |
| `label` + `label_style` | Text + select | 中国限定 (rose) / 専売品 / 販売終了 (gray) |
| `channel` | Text | 中国市場限定販売 |
| `image` | Image (square) | |
| `published_ok` | True/False | **Licence check**: only show if the licence allows public display (open question from the brief). |

### 4.5 FAQ — `faq`

Question (title), answer (WYSIWYG, limited toolbar), `page` (select: partners
/ contact…), order. First item renders open.

---

## 5. Pages and templates

Each page is a WordPress **Page** with its own template file. Static copy on
the page (intro paragraphs, catchphrases) is an ACF field on that page, not
hard-coded, so staff can reword it.

| Page | Template | Dynamic sources | Editable static copy |
|---|---|---|---|
| Top | `front-page.php` | slides, 4 banner links (Options), news ×5, reasons badges (Options), products (`show_on_home`), commitment ×3 (fields), collabs, global + partners box (Options), company mini (Options), store logos (JA only) | section intros |
| ブランド・製品 | `page-brand.php` | products (all, with detail blocks `#p1…`), collabs, stores | philosophy text, slogan, free-from circles |
| 会社概要 | `page-company.php` | company profile rows, history, office photos, access (Options) | representative message, business cards |
| 研究開発・品質 | `page-rd.php` | export documents, registration table (Options) | lab text, process steps, quality boxes |
| IPコラボ | `page-collaboration.php` | collabs | about text, merits ×4 |
| 海外展開 | `page-global.php` | stats, regions, China results (Options) | intro |
| 代理店募集 | `page-partners.php` | models, trade terms, export docs, registration, flow, FAQ | intro, reasons |
| 展示会情報 | `page-exhibition.php` | v1.2: list of `exhibition` posts (name, dates, venue, booth, status, link to its buyer page), upcoming first, past below; v1/v1.1: current exhibition (Options), products, booking form | intro |
| お知らせ | `home.php` / `archive.php` / `single.php` | posts | — |
| お問い合わせ | `page-contact.php` | contact channels (Options), form | — |

Page-level layout pieces shared by all lower pages (title band, breadcrumb,
jump-to-section links, left/centred section headings) are theme partials in
`template-parts/`, mirroring `lower()`, `st()`, `stl()` in `_build/build.py`.

### 5.7 Meeting booking (Exhibition page)

**Premium v1.2 (chosen, feedback 2026-10):** no slot picker. Meetings at a show are
few, and a slot grid would need staff to keep booked slots up to date. The form asks
for a **preferred day** (select: 会期1日目 / 2日目 / 3日目 / 会期外・オンライン — the day
labels can show the real dates from the Exhibition Options) and a **preferred time**
(free text, e.g. 「14:00頃」「午後」). The request arrives by email like any enquiry and
staff confirm the time by reply. Nothing to maintain, no booking plugin.

v1 / v1.1 mockups still show the earlier slot picker (3 days × 12 slots). If a slot
system is ever wanted, the two options were: an ACF repeater of booked slots updated
by hand, or a booking plugin with availability.

---

## 6. Site-wide settings (ACF Options pages)

Facts that appear on many pages are entered **once**:

| Options page | Fields |
|---|---|
| 会社情報 Company | company name JA/EN, founded, address JA, address EN (Ginza-first), tel (stored once; theme formats `03-…` for JA and `+81-3-…` for EN), fax, hours, representative name & title, capital (**JA only**), banks (**JA only**), corporate number, business description, markets, China operating company (EN corporate-structure note), office photos, map query |
| 沿革 History | repeater: date + text |
| 取引条件 Trade terms | MOQ first / repeat, lead time stock / made-to-order, Incoterms, payment, territory, pricing note, samples, marketing support, price control |
| 協業モデル Models | repeater: model, audience, conditions |
| 輸出書類・各国登録 | repeater documents (name + note); repeater markets (market + requirement) |
| 展示会 Exhibition | event name, dates, venue, hall/booth, on-show text, languages, contact person, WhatsApp, WeChat, email, QR images, PDF downloads, show-announcement toggle (drives the home side box and the 商談予約 side tab) |
| 海外展開 Global | number of countries, regions, country list, China channel results |
| 選ばれる理由 Reasons | 6 badges: small label + big value + caption |
| 連絡先 Contact channels | email, WhatsApp, WeChat, LINE (JA only), LinkedIn |
| 国内ストア Stores (JA only) | Rakuten / Amazon / Yahoo! / Qoo10 URLs |

With Polylang, either use Polylang Pro's ACF integration to translate options,
or register each options page twice (`_ja` / `_en`) and read by current
language. Language-neutral facts (phone number, founded date, counts) should
live in one place only.

---

## 6b. v2.2 additions (if v2.2 is chosen)

- **First view** (`fv()`): label, headline, lead, two CTAs and a 4-item trust strip.
  Options page fields; the headline and lead are per language.
- **「日本製」4つの強み** (`japan4()`) and **選ばれる理由** (`why_partners()`): 4 items each
  (icon/number, title, one line). ACF repeater on an Options page, max 4.
- **Global stats** (`gstats`): countries, trade deals, overseas partners, founded.
  Options fields; an empty number renders as "—" plus nothing else in production.
- **Topic CTAs**: buttons link to `/contact/?topic=partner|product|oem|business`
  (`&item=<product slug>` from product pages). The contact form must accept these
  query parameters and pre-select the enquiry type and product. With MW WP Form,
  read them via the form's default-value filter; keep topic slugs stable because
  they are used in links across the site.
- Claims marked 要確認 in the mockup (made in Japan, QC in Japan, sales results, counts)
  must be confirmed by the client before launch: legal exposure under 景品表示法.

## 6c. Premium (the chosen design, 2026-10)

The client team chose the premium direction (`premium/`, generator
`_build/build_premium.py`). Content model and pages are the same as above,
with these differences:

- **Short menu (4 sections + the show + contact).** Build the header from a WordPress
  menu with one level of children: ブランド・製品 (child: IPコラボ), 代理店募集,
  企業情報 (children: 会社概要, 研究開発・品質), お知らせ. The desktop header shows the
  top level only; the phone menu shows children as indented sub-links; a parent is
  marked current on its child pages. The *Cosmoprof Asia* item is a menu entry staff
  remove after the show. Breadcrumbs follow the page parent (set the WordPress page
  parent to match).
- **No 海外展開 page.** Its content (figures, regions, China results) is two sections
  of the 代理店募集 page (`#network`, `#china`); skip `page-global.php` and add a
  redirect from `/global/` to `/partners/#network` if the old URL was ever shared.
- **Home slider (v1.2).** Slide 1 is the fixed brand/business hero (Options page);
  announcement slides are `kv_slide` posts with fixed fields and character limits — see §4.1.
- **No home carousel (v1, v1.1).** The top page has one fixed hero instead of `kv_slide`
  posts: label, headline, lead, two buttons and the featured product image as
  Options fields (per language). Skip the `kv_slide` CPT unless the client asks
  for rotating slides later. The exhibition note in the hero reads the
  Exhibition Options (show-announcement toggle).
- **v2.2 content is included** (§6b): 「日本製」4つの強み, 選ばれる理由, global
  figures and the topic buttons. In premium each 強み item also has a single
  kanji (研・造・質・績), so the repeater gets a `kanji` field (1 character).
- **Contact band** (above the footer on every page except Contact) shows the four
  topic buttons; it is a theme partial, labels from the language files.
- **Lower-page title band** has two variants: with a photo (`phero()` with an
  image: Brand, Company, R&D, Collaboration, Global, Partners) and plain
  (Exhibition, News, Contact). Each takes a short decorative kanji (e.g. 研究,
  協業) as a page field.
- Assets: enqueue `assets/css/premium.css` and `assets/js/premium.js` instead of
  `style.css` / `main.js`. `premium.js` holds the topic pre-select, slot picker
  and news filter.

| Premium mockup (`_build/build_premium.py`) | WordPress |
|---|---|
| `h_hero()` | Hero Options + `template-parts/hero.php` |
| `h_japan4()`, `h_why()`, `gstats()` | Options repeaters (§6b) |
| `contact_band()`, `cta_btn()`, `topic_href()` | `template-parts/contact-band.php`, helper `hj_topic_url()` |
| `phero()` | `template-parts/page-header.php` (photo / plain variants) |
| `p_rd()` … `p_contact()` | the page templates in §5 |

### Premium v1.1 motion layer

If v1.1 is chosen, enqueue `premium-v11.css` and `premium-v11.js` after the v1
files (or merge them). Things the theme must keep producing:

- **Heading lines:** every display heading is printed as one
  `<span class="ln" style="--i:N"><span>…</span></span>` per line. Staff type
  headings with line breaks (ACF textarea, *new lines → `<br>`*); a helper such as
  `hj_lines( $text )` splits on `<br>` / new lines. Without it headings still
  show, just without the line reveal.
- **Opening sequence:** front page only. The small inline script that adds
  `html.intro` (first view per browser tab, skipped for reduced motion) must sit
  in `<head>` before the stylesheets.
- **Images** need no extra markup: the reveal hooks onto the existing `.rv`,
  `.win`, `.arch` and figure classes.
- **Page fades** come from one CSS rule (`@view-transition`), so no plugin.

### Premium v1.2: Cosmoprof Asia buyer page

- A WordPress Page with its own template (`page-cosmoprof-asia.php`) and a slim
  header/footer partial; no global menu. Keep a short, stable slug such as
  `/cosmoprof-asia/` (English) and `/ja/cosmoprof-asia/` — the QR code printed for the
  booth points at the English address and must not change after printing.
- Content comes from the Exhibition Options (§6): dates, venue, booth, languages,
  show contact, WhatsApp, WeChat, QR images, PDF downloads; products from `product`
  posts flagged `show_at_exhibition`; trade terms and export documents from their
  Options pages.
- The form is the exhibition booking form (§5.7): preferred day (select) and preferred
  time (free text), both optional, then the visitor's details; product
  checkboxes use the same `data-items` keys as the contact form.
- Generate the booth QR code once from the final URL (any QR tool, high error
  correction, SVG for print). The in-page QR (qrcode.js) is a convenience for sharing.
- When the show is over, unpublish the page or redirect it to the 展示会情報 page,
  and remove the *Cosmoprof Asia* header item. On 展示会情報 the show then moves from
  "upcoming" to "past" by its end date, so the list keeps itself up to date.
- Exhibitions are an `exhibition` post type (name, year/month, dates, venue, booth, on-show
  text, languages, status label, link to the buyer page). A new show is a new post plus,
  if wanted, a new buyer page from the same template.

### Premium v1.3: separate Brand and Products, one page per product

Reviewer feedback 2026-10 (意見まとめ.xlsx). If v1.3 is the version built:

- **Menu** (Appearance → Menus): TOP／ブランド／製品／会社情報／お知らせ／パートナーシップ,
  then the *Cosmoprof Asia* item and the お問い合わせ button. IP コラボ stays a child of
  ブランド, 研究開発・品質 a child of 会社情報.
- **Products become real pages.** `product` is a public post type with an archive
  (`archive-product.php` → 製品一覧, `/products/`) and a single template
  (`single-product.php` → `/products/<slug>/`). The home page, the archive and the
  "その他の製品" block on each product page all query `product` posts, so a new product
  is one new post — nothing else to edit (the client has 10+ products and more coming).
- **Product fields added for v1.3** (on top of §4.2): `series` (taxonomy:
  ハトムギシリーズ / アミノ酸保湿シリーズ), `is_new` (true/false → 新商品 tag),
  `kind` (化粧品 / 医薬部外品), `features` (repeater, 3 rows: title + text), `free_from`
  (repeater), `usage` (textarea), `cautions` (textarea), `rakuten_url` (URL, **JA only** —
  the 楽天市場で購入する button; never output on English pages, §7), `gallery` (images).
  `product_cat` terms: クレンジング / 化粧水・美容液 / クリーム・ジェル / マスク・パック /
  UV・化粧下地 / メンズ.
- **Archive filter**: category buttons with counts; `?cat=<term slug>` opens the list
  filtered (links from the home chips and the product breadcrumb use it).
- **Contact form**: the product checkboxes are the `product_cat` terms (+ IP コラボ, OEM);
  `?item=<product slug>` ticks the product's category.
- **Home first view**: `kv_slide` gains `visual = background` — a full-width photo behind
  the text (the client supplies brand / new-product images). Slide 1 (brand) is an
  Options-page slide. Products on the home page: `show_on_home`, in menu order.
- **Initial data**: the mockup's `_build/catalog.py` holds 13 products taken from the
  Rakuten store (names, sizes, descriptions, ingredients, usage) — import it as the first
  `product` posts. Photos: replace the Rakuten images (some carry shop banners) with
  clean packshots before launch.

## 7. Language rules (enforced in templates)

From the content brief. Do not rely on staff to remember these.

| Rule | JA | EN |
|---|---|---|
| Registered capital, bank list | shown | **never rendered** |
| Domestic store links (Rakuten, Amazon, Yahoo!, Qoo10) | shown | replaced by “Find / become a distributor” panel |
| Product price line | 希望小売価格 | “Trade price: On request” |
| Product buttons | 購入する | Enquire / Trade enquiry |
| Brand line | ひとりに、ひとつの、キレイを咲かせる。 | “Clean formula. Gentle by design. Made in Japan.” + JA slogan small |
| Phone / address | domestic format, 〒 first | +81 format, Ginza first |
| Corporate structure note | — | shown on Company page |
| Contact form | WhatsApp/WeChat, market, volume optional | required |
| Section headings | big EN word + JA title | big EN word + EN title + small kanji |

The EN site keeps Japanese accents on purpose (kanji sub-labels, kanji+English
stamps). Don't “clean them up”.

---

## 8. Japanese line breaking

The mockup inserts `<wbr>` between Japanese phrases at build time (BudouX) and
sets `word-break: keep-all`, so every browser, including Safari on iPhone,
wraps between phrases instead of mid-word.

In WordPress, apply the same on output, for headings, card text and slide
text at minimum:

- **Server side:** run BudouX on the rendered text (a PHP port, or pre-process
  via a small filter on `the_title` / ACF `format_value`). Check that any
  port you pick is maintained.
- **Client side alternative:** Google's official BudouX JavaScript package
  (`<budoux-ja>` web component or the parser) on page load. Simpler, but
  text reflows once after load.

Keep `html[lang="ja"] body{word-break:keep-all;overflow-wrap:anywhere}` from
`style.css` either way.

---

## 9. Editor experience checklist

What makes this usable for non-technical staff:

- [ ] Admin menu in Japanese, grouped: お知らせ / 製品 / スライド / IPコラボ / FAQ / サイト設定
- [ ] Every field has a short Japanese help text and, where length matters, a character counter
- [ ] Image fields state the recommended size and crop
- [ ] Required fields enforced (slide image count matches `media_type`, etc.)
- [ ] Preview works for slides and products before publishing
- [ ] Editor role (`編集者`) can edit content but not themes, plugins or settings
- [ ] A one-page Japanese manual with screenshots: “お知らせを追加する”, “スライドを入れ替える”, “商品を追加する”

---

## 10. What stays with the developers

Per the client agreement, these are **not** staff-editable:

- Page structure, section order, adding new sections or page types
- Colours, fonts, spacing (`--rose` and other tokens in `style.css`)
- Navigation menus beyond relabelling (can use WP Menus if they want limited control)
- Form fields and email routing

---

## 11. Open items before build

Carried over from the mockup (`要確認 / TBC` chips):

- Official brand colour (HEX/CMYK): the mockup's rose `#C8235F` is matched by
  eye to the Rakuten store logo (≈ `#C01050`). A confirmed value is a
  one-line change in `style.css`; re-run the contrast check if it gets lighter.
- MOQ, lead times, payment terms, sample policy
- 12-country list; China channel figures; IP licence publication scope
- Booth number and show dates; exhibition contact person, WhatsApp, WeChat
- Factory, GMP/ISO, capacity; patent number; INCI, shelf life, JAN, case pack per product
- Representative's name and message; history dates; China operating company name
- Which products the site lists (the Rakuten store also sells Fine Washing,
  Lavender Oil mask and others not in the mockup); Cleansing Oil details and image
- New product / lifestyle photography (the biggest visual upgrade available)

---

## 12. Mapping from the mockup

| Mockup (`_build/build.py`) | WordPress |
|---|---|
| `SLIDES()` + `kv_slide()` in `build_premium.py` (v1.2) | `kv_slide` posts; `template-parts/kv-slide.php` |
| `PRODUCTS()` | `product` posts |
| `IPS()` | `collab` posts |
| `NEWS()` | Posts with categories `exh/prod/biz/info` |
| `company_rows()`, `TEL()`, `ADDR()`, `HOURS()` | Company Options + formatting helpers in `inc/format.php` |
| `export_list()`, `reg_table()` | Export/registration Options |
| `lower()`, `st()`, `stl()`, `hd3()` | `template-parts/page-header.php`, `section-heading.php` |
| `t(ja, en)` | Polylang (`pll_current_language()`) + per-language fields |
| `EN_ONLY` comments | Conditionals on `pll_current_language() === 'en'` |
| `add_wbr()` | BudouX filter (§8) |
| `assets/css/style.css`, `assets/js/main.js` | Enqueued unchanged from the theme |
