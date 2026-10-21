# 花印 HANAJIRUSHI — WordPress theme and plugin

The premium v1.7 mockup (`../mockup/premium-1.7/`) as an installable WordPress theme and
plugin. **Status (v0.6.0): every page is built, with the client's changes up to 2026-10-21**
(v1.4–1.5: official logo, brand text, store chooser, 代表メッセージ, the logo's magenta, English
pages without Japanese labels; v1.6: the cleansing-oil slide, the client's 14 products, order and
photos, OEM quality cards, company table, office photos, access and hours, no 化粧品 label or INCI
row; v1.7: the brand header slideshow, the 全成分 section kept) — home, brand, IP collaborations,
products and each product page, company, R&D, news (list, categories, years, article),
partnership, exhibitions, contact (with a working form) and the Cosmoprof Asia buyer page
(booth QR code, booking form) — in Japanese and English.

| Folder | What it is | Installed via |
|---|---|---|
| `hanajirushi/` | Theme: templates, the design's CSS/JS (the mockup's own files), fixed page copy | 外観 → テーマ → 新規追加 → テーマのアップロード |
| `hanajirushi-core/` | Plugin: content structure (製品・トップスライド・IPコラボ・展示会・サイト設定), the two forms, JA/EN, Japanese line breaking, 初期データ | プラグイン → 新規追加 → プラグインのアップロード |
| `dev/` | Tools: `sync.py`, `package.py`, local test site (`blueprint.json`) | — |

Content lives in the plugin, design in the theme, so a later redesign keeps the content.

## Requirements

- WordPress 6.6 or later, PHP 8.1 or later. Tested on WordPress 7.1.2 with PHP 8.4 (our server: 7.1.2 / PHP 8.4.26 / MySQL 8.4 / nginx) and PHP 8.5.
- One free plugin from WordPress.org: **Secure Custom Fields** (maintained by WordPress.org;
  the free continuation of ACF, including repeaters and settings pages). The 花印 plugin
  declares it, so WordPress offers to install it.
- No paid plugins. No language plugin (see *Japanese and English*).

## Install (WordPress admin)

1. `python wordpress/dev/package.py` → `wordpress/dist/hanajirushi.zip` and `hanajirushi-core.zip`.
2. プラグイン → 新規追加: search **Secure Custom Fields**, install, activate.
3. プラグイン → 新規追加 → プラグインのアップロード: `hanajirushi-core.zip`, activate.
4. 外観 → テーマ → 新規追加 → テーマのアップロード: `hanajirushi.zip`, activate.
5. 設定 → パーマリンク: 「投稿名」 (`/%postname%/`), save. **Required**: without it `/products/` and
   `/en/` do not exist. On **nginx**, WordPress cannot check that the server passes these
   addresses to WordPress (Site Health always says yes); if `/products/` gives the server's own
   404 page rather than the site's, the nginx site needs `try_files $uri $uri/ /index.php?$args;`.
6. ツール → 花印 初期データ → 「初期データを取り込む」: the mockup's products (from the
   Rakuten store), home slides, IP collaborations, exhibitions, news, company details,
   history, trade terms and FAQ. It also creates the pages the theme has templates for
   (ブランド, 会社概要, お問い合わせ … with these exact slugs) and sets トップ as the home page and
   お知らせ as the news page. Running it again updates the same items (it never duplicates);
   **it overwrites starter items that staff have since edited**, so on a live site run it
   only once.
   Updating from an earlier version: upload the new zips (WordPress asks to replace the
   installed version), then run 初期データ once to add the new pages and settings.
7. サイト設定 → お問い合わせ: the address enquiries go to (empty = the site admin's email).
   Check that the server can send email (a test enquiry); every enquiry is also kept in
   お問い合わせ履歴, so nothing is lost if mail fails. If mail does not arrive, an SMTP
   plugin (e.g. the free *WP Mail SMTP*) connects WordPress to the company's mail server.
8. サイト設定 → 表示: turn **要確認マーク** off before the site goes public.

Upload size: the theme zip is about 1.8 MB and the plugin about 0.6 MB, under the common
2 MB upload limit (サイトヘルス → 情報 → サーバー → アップロードの上限ファイルサイズ). If a
later version is larger, upload by FTP or raise `upload_max_filesize`. The 初期データ import
adds 10 photos; if a slow server stops it at its PHP time limit, press the button again (it
continues where it stopped).

By FTP instead: copy the two folders to `wp-content/themes/` and `wp-content/plugins/`,
then do steps 2 and 4–7 in the admin.

**Moving to the client's server** (build on ours first, then move): everything is either
files (theme, plugin, `wp-content/uploads`) or database content, so any normal WordPress
move works — the free *Duplicator* plugin, or by hand: FTP the files, export/import the
database, then replace the old site address (e.g. *Better Search Replace*).

## Japanese and English

- Japanese at `/…`, English at the same address under `/en/…` (`/products/hatomugi-cream/`
  ↔ `/en/products/hatomugi-cream/`). The plugin handles the prefix; every link WordPress
  builds on an English page gets `/en/` automatically.
- One post per item, both languages on it: 日本語 / English tabs on the edit screen. The
  Japanese name is the post title; the English one is the `title_en` field.
- **An item with no English title is left out of the English site** (lists skip it, its
  page is 404), so JA-only news or products are simply left without an English title.
- English pages follow the mockup's EN_ONLY rules: no Rakuten buttons or Japanese store
  links; the trade buttons instead.

## What staff edit

| Menu | Content |
|---|---|
| 製品 | One post per product: 基本情報 (category, series, size, new / coming soon, on the home page, store pages for 「この製品を購入する」: Rakuten code, Amazon, Yahoo!ショッピング, Qoo10), 日本語, English, 取引情報 (JAN, cautions). Photo = アイキャッチ画像. Order = 属性 → 順序. A store without its address is marked 要確認 on the review site and left out of the chooser on the live site. |
| トップスライド | One post per slide: texts per language (with character limits), one button and its link, visual (none / product / 3 products / kanji — with an English word for the English site, e.g. Hong Kong), seal, background photo, optional start and end dates. |
| IPコラボ | Name, product, label, sales channel per language; photo = アイキャッチ画像. |
| 投稿 (お知らせ) | Japanese title and text as usual; English title and text in the *English* box. Categories: 展示会, お知らせ, 企業情報, 製品情報. |
| 展示会 | One post per show: dates, venue, booth, on show, languages, status, its buyer page, last day (after it, the show moves to 過去の出展). The next show also fills the buyer page and the news sidebar. |
| サイト設定 | Tabs: company details (JA / EN), 会社概要の表, 代表メッセージ (heading, text with a blank line between paragraphs, title — the representative stays anonymous, no portrait), 写真 (the three photo shapes — 16:9, 4:5, 1:1 — explained at the top; a photo for each page header — brand, IP collaborations, products, company, R&D, news, partnership, exhibitions, contact — shown whole in a 16:9 frame on every screen; 16:9, 2400×1350 px recommended, with the part to keep if a photo of another shape is cropped; then the photos inside the pages — home company, brand concept and research, the three business photos, the office photos with their captions, the R&D and product-page lab photo — each labelled with its shape and size; empty keeps the theme's photo, or no photo), ブランドムービー (the home page film: an MP4 from メディア, or a URL; the frame shown before play; title — empty means no film section), 沿革 (on hold: a 表示 switch puts it back on the page and in the footer), 取引条件, よくあるご質問, アクセス (stations), 展示会担当 (contact, WhatsApp, WeChat, QR images, PDFs), お問い合わせ (notification address, auto-reply), 表示 (要確認 marks). |
| お問い合わせ履歴 | Every contact enquiry and booth booking, as sent (read only). |
| 固定ページ | The pages exist so their addresses work; their layout and text are the theme's (the brand text is the client's, from the mockup). |

**要確認 marks:** in any field, text in full-width square brackets — ［要確認］, ［氏名］,
［TBC］ — shows as the dashed 要確認 mark while サイト設定 → 表示 is on, and disappears when it is
off. The starter data uses this for every fact still to confirm.

The menu, the fixed page copy (headings, brand text, figures…) and the layout are in the
theme. Japanese line breaks are automatic (BudouX, see below); staff never type `<br>` or
`<wbr>`.

## For developers

- **Forms** (`hanajirushi-core/inc/forms.php`): お問い合わせ is 入力 → 確認 → 完了, the booth
  booking is one step; both check required fields (English asks a little more, as the
  mockup does), block bots (nonce, hidden trap field, a 3-second minimum), keep a copy in
  お問い合わせ履歴, mail the staff and auto-reply. Field names are `f_<name>`: plain names
  such as `name` or `day` are WordPress's own address variables and make the page 404.
  Choices come from `inc/form-options.json` (made by `sync.py` from the mockup).
- **Fixed page copy** comes from the mockup too: `sync.py` writes `hanajirushi/inc/copy.json`
  from `mockup/_build/build.py` (both languages) and the templates read it with `hj_c()`.
  Change copy in the mockup and run `sync.py`.
- **Live-site switch:** the design's `premium.js` blocks form sending and store links in the
  mockup; the theme marks `<html data-live>` so they work on the real site.

- **Design files are the mockup's.** `dev/sync.py` copies `premium*.css/js` and the images
  from `mockup/assets/` into the theme, regenerates the plugin's `seed/seed.json` from
  `mockup/_build/catalog.py` and `build.py`, and copies the BudouX model. Change the design
  in the mockup, run `sync.py`, never edit the theme's `assets/` by hand.
- **Templates follow the mockup's functions** (`mockup/_build/build_premium.py`):
  `front-page.php` = `p_home()`, `archive-product.php` = `p_products13()`,
  `single-product.php` = `p_product13()`, `header.php` / `footer.php` = `header()` /
  `footer()`; small helpers in `inc/helpers.php` mirror `eb()`, `shd()`, `lines()`, `lnk()`,
  `btn()`, `seal()`, `win()`.
- **Field names** are in `hanajirushi-core/inc/fields.php`; keys are
  `field_hj_<group>_<name>`. Read them only through `hj_get()` (current language),
  `hj_raw()` (shared), `hj_title()`, `hj_opt()` (`inc/data.php`).
- **Japanese line breaking**: `inc/budoux.php` is a PHP port of Google's BudouX parser
  (Apache-2.0) with its Japanese model; Japanese pages get `<wbr>` between phrases as they
  are sent, as the mockup's `add_wbr()` does.
- **Local test site** (no server needed; WordPress Playground): `npx @wp-playground/cli@latest
  server --php=8.5 --wp=latest --blueprint=wordpress/dev/blueprint.json --mount-dir
  wordpress/hanajirushi /wordpress/wp-content/themes/hanajirushi --mount-dir
  wordpress/hanajirushi-core /wordpress/wp-content/plugins/hanajirushi-core`
  → http://127.0.0.1:9400 (admin logged in). It starts fresh each time: installs Secure
  Custom Fields, activates both, imports the 初期データ. Edits to the theme and plugin
  folders show on reload. `dist/blueprint-zip.json` (made by `package.py`) instead installs the two zips,
  the way the admin upload does. (In this repo: the `wordpress` and
  `wordpress-zip` entries of `.claude/launch.json`.)

## Updating a site from 0.4.x to 0.5.0 (premium v1.6)

Upload both zips (plugin first), then run ツール → 花印 初期データ once. It:
- adds the new products (ピュアメルトクレンジングオイル, クレンジングバーム, モイスチュア洗顔クリーム) with the
  client's photos, renames クレンジングローションMa to ディープクレンジングローション, sets the new order and
  the home-page products;
- sets クレーパック and the 80g AMINO face mask to 下書き (draft, not deleted);
- replaces the third home slide with the cleansing-oil slide (visual バナー画像) and updates slide 1;
- updates the company table (no 代表者, 販売地域, 法人番号), stations and reception hours (10:00〜17:00);
- puts the client's lab photos into サイト設定 → 写真 (research windows, business 一, office photos).

Re-running 初期データ overwrites these items again, including photos chosen in サイト設定 → 写真 for
those slots. The office section now has six photo slots (three 4:5 above three 16:9).

## Updating a site from 0.5.0 to 0.6.0 (premium v1.7)

Upload both zips (plugin first), then run ツール → 花印 初期データ once: it fills サイト設定 → 写真 →
ブランドのヘッダー（スライドショー） with the client's three photos and copy. With two or more slides
there, the brand page header becomes a slideshow (the copy is text, typed in each slide's fields, in
Japanese and English). Product pages show the 全成分 section again.

