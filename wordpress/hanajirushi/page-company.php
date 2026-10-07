<?php
/**
 * 会社概要 /company/ (mockup: p_company() for v1.4): message, profile, business, office,
 * access. The message, the profile table and the history are edited in サイト設定. The history is
 * on hold (client, 2026-10-07): shown only when サイト設定 → 沿革 → 表示 is switched on. The
 * representative stays anonymous: the message is signed with the title only, without a portrait.
 */

defined( 'ABSPATH' ) || exit;

get_header();

$history_on = (bool) hj_opt_raw( 'show_history' );
$n          = $history_on ? array( '04', '05', '06' ) : array( '', '04', '05' );   // section numbers: history, office, access

echo hj_phero( 'Company', '会社概要', 'Company',
	hj_t( '東京・銀座から、日本のスキンケアを世界へ。', 'Japanese skincare, from Ginza, Tokyo to the world.' ),
	hj_img( 'h_campany_top_p.jpg' ), '銀座', array(),
	array( 'pos' => '30% center', 'anchors' => array( array( 'message', hj_t( '代表メッセージ', 'Message' ) ), array( 'profile', hj_t( '会社概要', 'Profile' ) ), array( 'business', hj_t( '事業内容', 'Business' ) ),
		...( $history_on ? array( array( 'history', hj_t( '沿革', 'History' ) ) ) : array() ), array( 'office', hj_t( 'オフィス紹介', 'Office' ) ), array( 'access', hj_t( 'アクセス', 'Access' ) ), array( '/rd/', hj_t( '研究開発・品質', 'R&amp;D &amp; quality' ) ) ) ) );

// ------------------------------------------------------------------ 01 message
$head  = hj_is_en() ? '<h2 class="msg__h">' . hj_lines( 'From Ginza,<br><em>to the world.</em>' ) . '</h2>' : '<h2 class="msg__tate">' . hj_lines( '銀座から、<br>世界へ。' ) . '</h2>';
$paras = '';
foreach ( preg_split( '/\R\s*\R/u', trim( (string) hj_opt( 'message' ) ) ) as $para ) {   // paragraphs: a blank line between
	if ( '' !== trim( $para ) ) {
		$paras .= '<p>' . hj_text( $para ) . '</p>';
	}
}
$lead    = (string) hj_opt( 'message_lead' );
$company = esc_html( (string) hj_opt( 'company' ) );
?>
<section class="sec msg msg--noimg" id="message"><div class="wrap msg__g">
<div class="msg__s rv"><?php echo hj_eb( 'Message', '01' ) . $head; ?></div>
<div class="msg__txt rv"><?php echo $lead ? '<p class="msg__lead">' . esc_html( $lead ) . '</p>' : ''; ?><?php echo $paras; ?>
<p class="msg__end" lang="ja">ひとりに、ひとつの、キレイを咲かせる。</p><?php echo hj_slogan_en( 'slogan-en--msg' ); ?>
<p class="msg__sig"><?php echo $company; ?><br><?php echo esc_html( (string) hj_opt( 'rep_title' ) ); ?></p></div>
</div></section>
<?php
// ------------------------------------------------------------------ 02 profile
$rows = '';
foreach ( hj_pairs( 'profile_rows', 'label', 'value' ) as $r ) {
	$rows .= '<tr><th>' . esc_html( $r[0] ) . '</th><td>' . hj_text( $r[1] ) . '</td></tr>';
}
?>
<section class="sec sec--t blush" id="profile"><div class="wrap prof__g">
<?php echo hj_shd( '02', 'Profile', '会社概要', 'Company profile', '会社概要' ); ?>
<table class="ptbl rv"><?php echo $rows; ?></table></div></section>
<?php if ( hj_is_en() ) : ?>
<section class="sec--s"><div class="wrap"><div class="note-box rv"><?php echo hj_eb( 'Corporate structure' ); ?><p><?php echo hj_c( 'STRUCTURE_EN' ); ?></p></div></div></section>
<?php endif; ?>
<?php
// ------------------------------------------------------------------ 03 business
$biz = '';
foreach ( hj_c( 'BUSINESS' ) as $i => $b ) {
	$tags = implode( '', array_map( fn( $c ) => '<li>' . $c . '</li>', $b[4] ) );
	$biz .= '<li class="rv"><div class="arch"><img src="' . esc_url( hj_img( $b[0] ) ) . '" alt="" loading="lazy"></div>
<p class="craft__n"><span>' . hj_kan( $i ) . '</span>' . $b[1] . '</p><h3>' . $b[2] . '</h3><p>' . $b[3] . '</p><ul class="tags tags--ink">' . $tags . '</ul></li>';
}
?>
<section class="sec biz" id="business"><div class="wrap">
<?php echo hj_shd( '03', 'Business', '事業内容', 'Our business', '事業内容', hj_t( '化粧品の原料、化粧品、健康食品の研究開発、製造、販売及び輸出入', 'R&amp;D, manufacturing, sales, import and export of cosmetic raw materials, cosmetics and health foods' ), 'shd--c' ); ?>
<ol class="craft__l"><?php echo $biz; ?></ol></div></section>
<?php
// ------------------------------------------------------------------ 04 history (on hold)
if ( $history_on ) :
	$hist = '';
	foreach ( hj_pairs( 'history', 'date', 'text' ) as $h ) {
		$hist .= '<li class="rv"><p class="tl__d">' . hj_text( $h[0] ) . '</p><p class="tl__t">' . hj_text( $h[1] ) . '</p></li>';
	}
	?>
<section class="sec dark hist" id="history"><div class="wrap hist__g">
<div><?php echo hj_shd( $n[0], 'History', '沿革', 'History', '沿革' ); ?><?php echo hj_show_tbc() ? '<p class="note">' . hj_t( '※ 年月は確認のうえ掲載します。', 'Dates to be confirmed.' ) . '</p>' : ''; ?></div>
<ol class="tl"><?php echo $hist; ?></ol></div></section>
	<?php
endif;
// ------------------------------------------------------------------ 05 office (photos not already shown under 事業内容)
$shown = array_map( fn( $b ) => $b[0], hj_c( 'BUSINESS' ) );
$ph    = '';
foreach ( hj_c( 'OFFICE_PHOTOS' ) as $o ) {
	if ( ! in_array( $o[0], $shown, true ) ) {
		$ph .= '<li class="rv"><figure><img src="' . esc_url( hj_img( $o[0] ) ) . '" alt="" loading="lazy"><figcaption>' . $o[1] . '</figcaption></figure></li>';
	}
}
?>
<section class="sec office" id="office"><div class="wrap">
<?php echo hj_shd( $n[1], 'Office', 'オフィス紹介', 'Our Ginza office', 'オフィス紹介', hj_t( '銀座二丁目の本社に、研究室・ショールーム・応接室を備えています。', 'Our head office in Ginza 2-chome houses our laboratory, showroom and meeting rooms.' ), 'shd--c' ); ?>
<div class="office__g"><figure class="office__main rv"><img src="<?php echo esc_url( hj_img( 'h_campany_bldg.jpg' ) ); ?>" alt="" loading="lazy"><figcaption><?php echo hj_t( '本社ビル（銀座二丁目）', 'Head office, Ginza 2-chome' ); ?></figcaption></figure>
<ul class="office__l"><?php echo $ph; ?></ul></div></div></section>
<?php
// ------------------------------------------------------------------ 06 access
$acc = array(
	array( hj_t( '所在地', 'Address' ), hj_text( hj_opt( 'address' ) ) ),
	array( hj_t( '最寄駅', 'Stations' ), hj_text( hj_opt( 'stations' ) ) ),
	array( 'TEL', esc_html( hj_tel() ) ),
	array( 'FAX', esc_html( (string) hj_opt( 'fax' ) ) ),
	array( hj_t( '受付時間', 'Hours' ), esc_html( (string) hj_opt( 'hours' ) ) ),
);
$dl = '';
foreach ( $acc as $a ) {
	$dl .= '<div><dt>' . $a[0] . '</dt><dd>' . $a[1] . '</dd></div>';
}
$map = 'https://www.google.com/maps?q=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%B8%AD%E5%A4%AE%E5%8C%BA%E9%8A%80%E5%BA%A72-12-12&output=embed&hl=' . hj_lang();
?>
<section class="sec sec--t blush" id="access"><div class="wrap acc__g">
<div class="acc__map rv"><iframe loading="lazy" title="<?php echo esc_attr( hj_t( '地図', 'Map' ) ); ?>" referrerpolicy="no-referrer-when-downgrade" src="<?php echo esc_url( $map ); ?>"></iframe></div>
<div class="rv"><?php echo hj_shd( $n[2], 'Access', 'アクセス', 'Access', 'アクセス' ); ?>
<dl class="dl"><?php echo $dl; ?></dl>
<?php echo hj_lnk( 'https://maps.google.com/?q=2-12-12+Ginza+Chuo-ku+Tokyo', 'Googleマップで見る', 'Open in Google Maps' ); ?></div>
</div></section>
<?php
get_footer();
