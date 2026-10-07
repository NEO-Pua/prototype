<?php
/**
 * Menu, contact band and footer content (the mockup's NAV(), header(), contact_band(),
 * footer()). The menu is fixed in code so the Japanese and English menus always match;
 * labels sit side by side here.
 */

defined( 'ABSPATH' ) || exit;

/**
 * Main menu: [key, path, Japanese, English, children[path, Japanese, English]].
 * The key matches hj_page_key() (or a parent's), which marks the current item.
 */
function hj_nav(): array {
	return array(
		array( 'home', '/', 'TOP', 'Top', array() ),
		array( 'brand', '/brand/', 'ブランド', 'Brand', array( array( '/collaboration/', 'IPコラボレーション', 'IP collaborations' ) ) ),
		array( 'products', '/products/', '製品', 'Products', array() ),
		array( 'company', '/company/', '会社情報', 'Company', array( array( '/rd/', '研究開発・品質', 'R&amp;D &amp; quality' ) ) ),
		array( 'news', '/news/', 'お知らせ', 'News', array() ),
		array( 'partners', '/partners/', 'パートナーシップ', 'Partnership', array() ),
	);
}

/** Current menu section: product pages belong to 製品, collaboration to ブランド, R&D to 会社情報. */
function hj_nav_current(): string {
	$k = hj_page_key();
	return array( 'product' => 'products', 'collaboration' => 'brand', 'rd' => 'company', 'exhibition' => 'partners' )[ $k ] ?? $k;
}

function hj_tel(): string {
	return (string) ( hj_opt( 'tel' ) ?: hj_t( '03-6264-2154', '+81-3-6264-2154' ) );
}

function hj_tel_href(): string {
	$tel = preg_replace( '/[^0-9]/', '', (string) hj_opt_raw( 'tel' ) );
	return 'tel:+81' . ltrim( $tel ?: '362642154', '0' );
}

function hj_hours(): string {
	return (string) hj_opt( 'hours' );
}

/** Exhibition shown in the menu drawer (fixed for the proof; becomes an exhibition post later). */
function hj_menu_exh(): string {
	return '<a class="menu__exh" href="' . esc_url( hj_link( '/cosmoprof-asia/' ) ) . '"><small>Exhibition</small><b>Cosmoprof Asia 2026</b><span>'
		. hj_t( '2026年11月・香港 — 商談予約受付中', 'Hong Kong, November 2026 — book a meeting' ) . '</span></a>';
}

/** The contact band above the footer (every page except Contact). */
function hj_contact_band(): string {
	return '<section class="cta">
<div class="wrap cta__in rv">
' . hj_seal( '花印', 'seal--m' ) . '
<div class="cta__h">' . hj_eb( 'Contact' ) . '<h2 class="h2">' . hj_lines( hj_t( 'お取引・代理店に関する<br>ご相談を承ります。', 'Interested in distributing<br><em>HANAJIRUSHI?</em>' ) ) . '</h2>
<p>' . hj_t( '製品・OEM/ODM・海外展開のご相談も承ります。3営業日以内にご返信します。', 'Product, OEM/ODM and market-entry enquiries welcome. We reply within 3 business days.' ) . '</p></div>
<div class="cta__r"><p class="cta__tel"><small>' . hj_t( 'お電話でのお問い合わせ', 'Call our Tokyo office' ) . '</small><a href="' . esc_attr( hj_tel_href() ) . '">' . esc_html( hj_tel() ) . '</a><small>' . esc_html( hj_hours() ) . '</small></p>
<div class="cta__b">' . hj_cta_btn( 'partner', 'btn--fill' ) . hj_cta_btn( 'business' ) . '</div>
<p class="cta__more">' . hj_cta_lnk( 'product', 'lnk--s' ) . hj_cta_lnk( 'oem', 'lnk--s' ) . '</p></div>
</div></section>';
}

/** Footer link columns: [heading, [[path, label]…]]. The product column lists the home-page products. */
function hj_footer_cols(): array {
	$prods = array( array( '/products/', hj_t( '製品一覧', 'All products' ) ) );
	foreach ( array_slice( hj_home_products(), 0, 4 ) as $p ) {
		$prods[] = array( get_permalink( $p ), esc_html( hj_title( $p ) ) );
	}
	return array(
		array( hj_t( 'ブランド', 'Brand' ), array( array( '/brand/', hj_t( 'ブランドについて', 'About the brand' ) ), array( '/collaboration/', hj_t( 'IPコラボレーション', 'IP collaborations' ) ), array( '/rd/', hj_t( '研究開発・品質管理', 'R&amp;D and quality' ) ) ) ),
		array( hj_t( '製品', 'Products' ), $prods ),
		array( hj_t( '会社情報', 'Company' ), array( array( '/company/', hj_t( '会社概要', 'Company profile' ) ), ...( hj_opt_raw( 'show_history' ) ? array( array( '/company/#history', hj_t( '沿革', 'History' ) ) ) : array() ), array( '/company/#access', hj_t( 'アクセス', 'Access' ) ), array( '/news/', hj_t( 'お知らせ', 'News' ) ) ) ),
		array( hj_t( 'パートナーシップ', 'Partnership' ), array( array( '/partners/', hj_t( '海外代理店・パートナー募集', 'Partnership programme' ) ), array( '/partners/#network', hj_t( '海外展開・販売実績', 'Global network' ) ), array( '/exhibition/', hj_t( '展示会情報', 'Exhibitions' ) ), array( '/contact/', hj_t( 'お問い合わせ', 'Contact' ) ) ) ),
	);
}

/** Page titles and descriptions by page slug: [Japanese title, English title, JA description, EN description]. */
function hj_pages(): array {
	return array(
		'brand'          => array( 'ブランド', 'Brand', '花印のブランドコンセプト、5つの価値観、ブランドストーリー。ひとりに、ひとつの、キレイを咲かせる。東京・銀座の日本製スキンケア。', 'The HANAJIRUSHI brand: our concept, our five values and our story — Japanese skincare from Ginza, Tokyo.' ),
		'collaboration'  => array( 'IPコラボレーション', 'Licensed IP Collaborations', '花印のIPコラボレーション。美少女戦士セーラームーン、リトルツインスターズ、フルーツバスケット、ユーリ!!! on ICE との正規ライセンス商品。', 'HANAJIRUSHI licensed IP collaborations: Sailor Moon, Little Twin Stars, Fruits Basket, Yuri!!! on ICE. Full co-development capability for distributors.' ),
		'company'        => array( '会社概要', 'Company', '花印粧業研究所株式会社の会社概要。代表メッセージ、事業内容、オフィス紹介、アクセス。2015年創業、東京・銀座本社。', 'Company profile of Hanajirushi Institute of Cosmetics, Inc. Founded 2015, headquartered in Ginza, Tokyo, with in-house R&D, manufacturing and export.' ),
		'rd'             => array( '研究開発・品質', 'R&D & Quality', '花印の研究開発と品質管理。銀座の自社研究室での処方開発、日本国内での製造、輸出書類、各国登録の技術支援。', 'HANAJIRUSHI R&D and quality: in-house formulation in Ginza, manufacturing in Japan, export documentation and registration support.' ),
		'news'           => array( 'お知らせ', 'News', '花印粧業研究所株式会社からのお知らせ。展示会、製品情報、企業情報。', 'News from Hanajirushi Institute of Cosmetics, Inc.: exhibitions, products and business updates.' ),
		'partners'       => array( '海外代理店・パートナー募集', 'Partnership Programme', '花印の海外代理店・パートナー募集。世界12ヵ国での販売実績、中国市場での実績、協業モデル、取引条件、輸出書類、各国登録の技術支援、お取引開始までの流れ、よくあるご質問。', 'Become a HANAJIRUSHI distributor: sold in 12 countries, proven in China; cooperation models, trade terms, export documentation, registration support, how to start and FAQ.' ),
		'exhibition'     => array( '展示会情報', 'Exhibitions', '花印の展示会情報。出展予定の展示会と専用の商談ページ、過去の出展実績。', 'HANAJIRUSHI exhibitions: upcoming shows with their own meeting pages, and past exhibitions.' ),
		'contact'        => array( 'お問い合わせ', 'Contact', '花印粧業研究所株式会社へのお問い合わせ。海外代理店のお申込み、お取引・製品・OEM/ODMのご相談。', 'Contact Hanajirushi Institute of Cosmetics: distributor applications, trade, product and OEM/ODM enquiries. Email, WhatsApp, WeChat.' ),
		'cosmoprof-asia' => array( 'Cosmoprof Asia 2026 商談ページ', 'Cosmoprof Asia 2026 — Buyer page', 'Cosmoprof Asia 2026（香港）に出展する花印の商談ページ。出展製品、取引条件、商談のご予約、展示会担当者の連絡先。', 'HANAJIRUSHI at Cosmoprof Asia 2026, Hong Kong: products, trade terms at a glance, meeting booking and show contacts.' ),
	);
}
