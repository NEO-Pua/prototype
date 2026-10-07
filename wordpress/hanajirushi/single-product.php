<?php
/**
 * One product /products/<slug>/ (mockup: p_product13()): photo and buttons, features,
 * how to use, research, details (accordion), more products.
 */

defined( 'ABSPATH' ) || exit;

get_header();

$p    = get_queried_object();
$id   = $p->ID;
$cats = hj_categories();
$cat  = (string) hj_raw( 'category', $id );
$ser  = hj_product_series( $p );
$name = hj_title( $p );
$size = (string) hj_raw( 'size', $id );
$kind = hj_label( HJ_KINDS, hj_raw( 'kind', $id ) );
$li   = fn( $lines ) => implode( '', array_map( fn( $x ) => '<li>' . esc_html( $x ) . '</li>', $lines ) );

// Buttons. English pages never link to the Japanese consumer store (EN_ONLY rule).
$ask = hj_cta_btn( 'product', hj_is_en() ? 'btn--fill' : '', $p->post_name, array( 'この製品について相談する', 'Ask about this product' ) );
$rk  = (string) hj_raw( 'rakuten_code', $id );
// 「この製品を購入する」 opens a choice of stores (client, 2026-10-07). A store without its address is
// marked 要確認 on the review site and left out on the live site.
$stores = array(
	array( 'rakuten.svg', '楽天市場', '花印 公式ショップ', $rk ? 'https://item.rakuten.co.jp/hanajirushi/' . rawurlencode( $rk ) . '/' : '' ),
	array( 'amazon.png', 'Amazon', '公式ストア', (string) hj_raw( 'amazon_url', $id ) ),
	array( 'yahoo.svg', 'Yahoo!ショッピング', '公式ストア', (string) hj_raw( 'yahoo_url', $id ) ),
	array( 'qoo10.png', 'Qoo10', '公式ショップ', (string) hj_raw( 'qoo10_url', $id ) ),
);
$store_li = '';
foreach ( $stores as $s ) {
	if ( $s[3] ) {
		$store_li .= '<li><a href="' . esc_url( $s[3] ) . '" target="_blank" rel="noopener"><img src="' . esc_url( hj_img( $s[0] ) ) . '" alt=""><b>' . $s[1] . '</b><small>' . $s[2] . '</small></a></li>';
	} elseif ( hj_show_tbc() ) {
		$store_li .= '<li><a href="#" aria-disabled="true"><img src="' . esc_url( hj_img( $s[0] ) ) . '" alt=""><b>' . $s[1] . '</b><small>' . $s[2] . '</small>' . hj_tbd( 'URL 要確認', 'URL TBC' ) . '</a></li>';
	}
}
$buy = ( $store_li && ! hj_is_en() ) ? '<button class="btn btn--fill" type="button" data-buy aria-haspopup="dialog" aria-controls="buy"><span>この製品を購入する</span>' . HJ_ARR . '</button>' : '';
$ctas = hj_is_en() ? $ask . hj_btn( hj_link( '/partners/' ), '', 'Become a distributor' ) : $buy . $ask;

$free = hj_split_lines( hj_get( 'free', $id ) );
?>
<nav class="crumb crumb--pdx" aria-label="breadcrumb"><div class="wrap"><a href="<?php echo esc_url( hj_link( '/' ) ); ?>"><?php echo hj_t( 'ホーム', 'Home' ); ?></a><a href="<?php echo esc_url( hj_link( '/products/' ) ); ?>"><?php echo hj_t( '製品', 'Products' ); ?></a><a href="<?php echo esc_url( hj_link( '/products/?cat=' . $cat . '#list' ) ); ?>"><?php echo esc_html( $cats[ $cat ] ?? '' ); ?></a><span><?php echo esc_html( $name ); ?></span></div></nav>
<section class="pdx"><div class="wrap pdx__g">
<div class="pdx__vis rv"><?php echo hj_pimg( $p, 'ppan--l' ); ?><p class="pdx__lbl">Hanajirushi / <?php echo esc_html( $cats[ $cat ] ?? '' ); ?></p><p class="pdx__size"><?php echo esc_html( $size ); ?></p></div>
<div class="pdx__info rv"><?php echo hj_eb( esc_html( ( $cats[ $cat ] ?? '' ) . ( $ser ? ' · ' . $ser : '' ) ) ); ?>
<h1 class="pdx__n"><?php echo hj_pname( $name ); ?></h1><p class="pdx__sub"><?php echo esc_html( (string) hj_get( 'sub', $id ) ); ?></p>
<ul class="pdx__badges"><?php echo $li( hj_split_lines( hj_get( 'badges', $id ) ) ); ?></ul>
<p class="pdx__d"><?php echo hj_text( hj_get( 'desc', $id ) ); ?></p>
<?php if ( $free ) : ?><ul class="pdx__free"><?php echo $li( $free ); ?></ul><?php endif; ?>
<p class="pdx__spec"><b><?php echo esc_html( $size ); ?></b><span><?php echo esc_html( $kind ); ?></span><span><?php echo hj_t( '日本製', 'Made in Japan' ); ?></span></p>
<div class="ctas"><?php echo $ctas; ?></div>
<p class="pdx__trade"><?php echo hj_lnk( hj_link( '/partners/' ), '販売代理店・輸入商・小売企業の皆さまへ', 'For distributors, importers and retailers', 'lnk--s' ); ?></p></div>
</div></section>
<nav class="anc anc--pdx" aria-label="<?php echo esc_attr( hj_t( 'ページ内リンク', 'On this page' ) ); ?>"><div class="wrap"><a href="#features"><?php echo hj_t( '製品の特長', 'Features' ); ?></a><a href="#usage"><?php echo hj_t( '使い方', 'How to use' ); ?></a><a href="#details"><?php echo hj_t( '製品情報', 'Details' ); ?></a><a class="anc__pg" href="<?php echo esc_url( hj_topic_url( 'product', $p->post_name ) ); ?>"><?php echo hj_t( 'お問い合わせ', 'Enquire' ); ?></a></div></nav>
<?php
// ------------------------------------------------------------------ 01 features
$pts = '';
foreach ( (array) hj_get( 'points', $id ) as $k => $pt ) {
	$pts .= '<li class="rv"><span class="pdf__n">' . sprintf( '%02d', $k + 1 ) . '</span><h3>' . esc_html( $pt['title'] ?? '' ) . '</h3><p>' . esc_html( $pt['text'] ?? '' ) . '</p></li>';
}
?>
<section class="sec pdf" id="features"><div class="wrap">
<div class="shd shd--c"><?php echo hj_eb( 'Features', '01' ); ?><h2 class="h2"><?php echo hj_heading( hj_get( 'catch', $id ), hj_is_en() ); ?></h2></div>
<ol class="pdf__l"><?php echo $pts; ?></ol></div></section>
<?php
// ------------------------------------------------------------------ 02 how to use
$use = (string) hj_get( 'usage', $id );
?>
<section class="sec sec--t blush" id="usage"><div class="wrap pdu__g">
<div class="rv"><?php echo hj_shd( '02', 'How to use', '使い方', 'How to use', '使い方' ); ?></div><p class="pdu__t rv"><?php echo $use ? hj_text( $use ) : hj_tbd( '使用方法 要確認', 'How to use: TBC' ); ?></p></div></section>

<?php // ------------------------------------------------------------------ 03 research ?>
<section class="sec sec--t"><div class="wrap split__g">
<div class="split__img split__img--win rv"><?php echo hj_win( hj_img( 'h_campany_lab.jpg' ), hj_t( '銀座本社の研究室', 'Our laboratory in Ginza' ), 'win--m' ); ?></div>
<div class="split__txt rv"><?php echo hj_shd( '03', 'Research', '銀座の研究室から、<br>確かな処方を。', 'Reliable formulas<br><em>from our Ginza lab.</em>', '研究への取り組み' ); ?><p><?php echo hj_t( '花印の処方は、東京・銀座本社の研究室で原料レベルから開発しています。肌へのやさしさと確かな実感を両立させるため、無香料・無着色・オイルフリー・アルコールフリーを基本設計としています。', 'HANAJIRUSHI formulas are developed from the raw-material level in the laboratory at our Ginza head office. Our baseline design is fragrance-free, colorant-free, oil-free and alcohol-free — gentle on skin, with results you can feel.' ); ?></p>
<div class="ctas"><?php echo hj_lnk( hj_link( '/rd/' ), '研究開発・品質管理', 'R&amp;D and quality' ); ?></div></div></div></section>
<?php
// ------------------------------------------------------------------ 04 details
$row  = function ( string $label, string $value ): string {
	return '<div><dt>' . $label . '</dt><dd>' . $value . '</dd></div>';
};
$trade = function ( string $field ) use ( $id ): string {
	$v = (string) hj_raw( $field, $id );
	return '' !== $v ? esc_html( $v ) : hj_tbd();
};
// The client keeps 製品名, 内容量, 原産国, 全成分（INCI表記）, JANコード (2026-10-07).
$dl = $row( hj_t( '製品名', 'Product' ), esc_html( $name ) ) . $row( hj_t( '内容量', 'Size' ), esc_html( $size ) ) . $row( hj_t( '原産国', 'Made in' ), hj_t( '日本', 'Japan' ) );
foreach ( array(
	// the English INCI list itself sits under 全成分 below; this row says whether it is there
	array( hj_t( '全成分（INCI表記）', 'Full INCI list' ), hj_raw( 'inci_en', $id ) ? hj_t( '下記「全成分」に掲載', 'Under “Ingredients” below' ) : hj_tbd( '掲載予定', 'To be listed' ), (string) hj_raw( 'inci_en', $id ) ),
	array( hj_t( 'JANコード', 'JAN / EAN' ), $trade( 'jan' ), (string) hj_raw( 'jan', $id ) ),
) as $r ) {
	if ( '' !== $r[2] || hj_show_tbc() ) {   // empty facts: hidden on the live site, marked 要確認 on the review site
		$dl .= $row( $r[0], $r[1] );
	}
}
$inci = (string) hj_get( 'inci', $id );
if ( hj_is_en() && '' === $inci && hj_raw( 'inci', $id ) ) {
	$inci_html = hj_tbd( '英文表記 要確認', 'English INCI list TBC' ) . '<span class="pdd__ja" lang="ja">' . esc_html( (string) hj_raw( 'inci', $id ) ) . '</span>';
} else {
	$inci_html = $inci ? esc_html( $inci ) : hj_tbd( '掲載予定', 'To be listed' );
}
$cautions = (string) hj_get( 'cautions', $id );
$acc      = array(
	array( hj_t( '製品情報', 'Product information' ), '<dl class="dl">' . $dl . '</dl>', true ),
	array( hj_t( '全成分', 'Ingredients' ), '<p class="pdd__inci">' . $inci_html . '</p>', false ),
	array( hj_t( '使用上の注意', 'Cautions' ), $cautions ? '<p>' . hj_text( $cautions ) . '</p>' : '<p>' . hj_t( 'パッケージ記載の使用上の注意を掲載します。', 'The cautions printed on the pack will be listed here.' ) . ' ' . hj_tbd() . '</p>', false ),
	array( hj_t( '輸出関連資料（お取引先向け）', 'Export documents (for trade partners)' ), '<ul class="tags tags--ink">' . $li( hj_t( array( 'INCI成分表', 'COA（出荷検査成績書）', 'MSDS / SDS', '自由販売証明書', '原産地証明書', '製造日・ロット番号の表示ルール', 'ラベル法規対応' ), array( 'INCI ingredient list', 'Certificate of Analysis (COA)', 'MSDS / SDS', 'Free Sale Certificate', 'Certificate of Origin', 'Production date & lot code rules', 'Labelling compliance' ) ) ) . '</ul><p class="note">' . hj_t( '製品ごとにご用意します。', 'Prepared for each product.' ) . ' ' . hj_tbd() . '</p>', false ),
);
$det = '';
foreach ( $acc as $a ) {
	if ( ! $cautions && ! hj_show_tbc() && $a[0] === hj_t( '使用上の注意', 'Cautions' ) ) {
		continue;
	}
	$det .= '<details class="pdd__i"' . ( $a[2] ? ' open' : '' ) . '><summary><span>' . $a[0] . '</span></summary><div class="pdd__b">' . $a[1] . '</div></details>';
}
?>
<section class="sec sec--t blush" id="details"><div class="wrap prof__g">
<div><?php echo hj_shd( '04', 'Product details', '製品情報', 'Product details', '製品情報' ); ?></div>
<div class="pdd rv"><?php echo $det; ?></div></div></section>
<?php
// ------------------------------------------------------------------ 05 more products: same category first, then home products
$others = array_filter( hj_products(), fn( $x ) => $x->ID !== $id && ! hj_raw( 'coming_soon', $x->ID ) );
$same   = array_filter( $others, fn( $x ) => hj_raw( 'category', $x->ID ) === $cat );
$home   = array_filter( $others, fn( $x ) => hj_raw( 'category', $x->ID ) !== $cat && hj_raw( 'show_on_home', $x->ID ) );
$more   = '';
foreach ( array_slice( array_merge( $same, $home ), 0, 3 ) as $k => $x ) {
	$more .= hj_pcard( $x, $k + 1 );
}
?>
<section class="sec sec--t" id="more"><div class="wrap">
<div class="col13__h"><?php echo hj_shd( '05', 'More', 'その他の製品', 'More products', 'その他の製品' ) . hj_lnk( hj_link( '/products/' ), '製品一覧へ', 'All products' ); ?></div>
<ul class="pgrid"><?php echo $more; ?></ul></div></section>
<?php if ( $buy ) : ?>
<dialog class="buy" id="buy" aria-labelledby="buy-h"><div class="buy__in">
<?php echo hj_eb( 'Online store' ); ?><h2 id="buy-h">購入するストアを選ぶ</h2><p class="buy__p"><?php echo esc_html( $name . '（' . $size . '）' ); ?></p>
<ul class="buy__l"><?php echo $store_li; ?></ul>
<button class="buy__x" type="button" data-close aria-label="閉じる">×</button></div></dialog>
<?php endif; ?>
<?php
get_footer();
