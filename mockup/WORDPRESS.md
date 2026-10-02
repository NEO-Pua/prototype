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

The mockup's `slide()` function in `_build/build.py` **is** the template. Each
argument becomes a field. Staff never touch layout; the theme decides the
desktop layout (text left, image right) and the phone layout (tall card,
text on top).

| Field | Type | Example (JA) | Notes |
|---|---|---|---|
| `label` | Text (short) | ロングセラー | Rose pill at top. Keep ≤ 12 characters. |
| `headline_1` | Text | 花印 | First headline line (dark). |
| `headline_2` | Text | ハトムギ化粧水 | Second line, shown in rose. Replaces the `<em>` in the mockup. |
| `headline_event` | Text, optional | Cosmoprof Asia 2026 | Optional Latin line above the headline (event slides). Set in Montserrat. |
| `description` | Textarea, ≤ 60 chars JA | 北海道産ハトムギ種子エキス高配合… | Hidden on phones if too long; enforce a character limit. |
| `tags` | Repeater (text) | 500mL / 無香料 / 無着色 | Max 4. Desktop only. |
| `media_type` | Select | `photo` / `trio` / `grid` | photo = 1 image fading in from the right; trio = 3 product shots; grid = 4 square images (2×2 on phones). |
| `images` | Gallery | | 1, 3 or 4 images depending on `media_type`; validate the count. |
| `stamp` | Text, optional | 日本製 | Round sticker top-right. Two short lines max. EN: kanji + small English (`出展` / `EXHIBITING`). |
| `button_label` | Text | 詳しく見る | Default “詳しく見る / Learn more” if empty. |
| `link` | Link (ACF) | /brand/#p3 | Whole slide is clickable. |
| `theme` | Select | `light` / `rose` | Use `rose` sparingly (events only), as in the mockup. |
| `start_date` / `end_date` | Date, optional | | Auto-show/hide campaign slides. |
| Order | Post `menu_order` | | Drag-and-drop order (e.g. *Simple Custom Post Order*). |

Rules:

- Show 3–6 slides. Warn in the admin if more than 6 are published.
- Images: upload at least 1600 px wide; the theme generates sizes with `srcset`.
- `#kv=N` review link and autoplay/pause/swipe all come from `main.js`, so no
  per-slide settings are needed.

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
| 展示会情報 | `page-exhibition.php` | current exhibition (Options), products (`show_at_exhibition`), booking form | outline text |
| お知らせ | `home.php` / `archive.php` / `single.php` | posts | — |
| お問い合わせ | `page-contact.php` | contact channels (Options), form | — |

Page-level layout pieces shared by all lower pages (title band, breadcrumb,
jump-to-section links, left/centred section headings) are theme partials in
`template-parts/`, mirroring `lower()`, `st()`, `stl()` in `_build/build.py`.

### 5.7 Meeting booking (Exhibition page)

The mockup's slot picker (3 days × 12 slots, booked slots struck through) needs
real state in production. Two options:

- **Simple (recommended for the first show):** slot list and “booked” slots
  are an ACF repeater staff update by hand; the form emails the request and
  staff confirm by email. Low risk, no double-booking logic.
- **Full:** a booking plugin with availability. Only worth it if they exhibit
  often.

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
| `slide(...)` calls in `kv()` | `kv_slide` posts; `template-parts/kv-slide.php` |
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
