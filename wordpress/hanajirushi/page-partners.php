<?php
/**
 * 海外代理店・パートナー募集 /partners/ (mockup: p_partners() with global_sections()): why us,
 * global network, China, models, trade terms (サイト設定), export support, how to start,
 * FAQ (サイト設定).
 */

defined( 'ABSPATH' ) || exit;

get_header();

echo hj_phero( 'For Partners', '海外代理店・<br>パートナー募集', 'Partnership Programme',
	hj_t( '市場と規模に合わせた協業モデルをご用意しています。', 'Cooperation models to fit your market and scale.' ),
	hj_img( 'world_map_brand.png' ), '協業', array(),
	array( 'pos' => '30% center', 'variant' => 'map', 'anchors' => array( array( 'why', hj_t( '選ばれる理由', 'Why us' ) ), array( 'network', hj_t( '海外展開・実績', 'Global network' ) ), array( 'models', hj_t( '協業モデル', 'Models' ) ),
		array( 'terms', hj_t( '取引条件', 'Trade terms' ) ), array( 'support', hj_t( '輸出書類・登録支援', 'Export support' ) ), array( 'flow', hj_t( 'お取引の流れ', 'How to start' ) ), array( 'faq', hj_t( 'よくあるご質問', 'FAQ' ) ) ) ) );

$reasons = array();
for ( $i = 1; $i <= 3; $i++ ) {
	$reasons[] = array( hj_c( "PARTNER_REASON{$i}_T" ), hj_c( "PARTNER_REASON{$i}_D" ) );
}
?>
<section class="sec why" id="why"><div class="wrap why__g">
<div class="why__h rv"><?php echo hj_seal( '募集中', 'seal--txt seal--m' ) . hj_shd( '01', 'Now recruiting', '海外代理店・<br>パートナー募集中', 'Now recruiting<br><em>partners</em>', '代理店募集' ); ?>
<p class="pd__cp"><?php echo hj_c( 'PARTNER_LEAD' ); ?></p><p class="lead"><?php echo hj_c( 'PARTNER_TEXT' ); ?></p>
<div class="ctas"><?php echo hj_cta_btn( 'partner', 'btn--fill' ); ?></div></div>
<?php echo hj_numbered( $reasons ); ?>
</div></section>
<?php
// ------------------------------------------------------------------ 02 network, 03 China
$regs = '';
foreach ( hj_c( 'REGIONS' ) as $r ) {
	$regs .= '<li class="rv"><small>' . $r[1] . '</small><h3>' . $r[0] . '</h3><p>' . $r[2] . '</p><ul class="tags tags--ink">' . implode( '', array_map( fn( $c ) => '<li>' . $c . '</li>', $r[3] ) ) . '</ul></li>';
}
$china = '';
for ( $i = 1; $i <= 4; $i++ ) {
	$china .= '<li class="rv"><small>' . hj_c( "CHINA{$i}_S" ) . '</small><h3>' . hj_c( "CHINA{$i}_T" ) . '</h3><p>' . hj_c( "CHINA{$i}_B" ) . '</p></li>';
}
?>
<section class="sec sec--t blush" id="network"><div class="wrap">
<?php echo hj_shd( '02', 'Global network', '世界12ヵ国で販売', 'Sold in<br><em>12 countries</em>', '海外展開', hj_t( '日本ならではの上質で誠実なものづくりが認められ、国内はもとより世界12ヵ国で販売されています。', 'Recognised for the quality and honesty of Japanese manufacturing, HANAJIRUSHI is sold in Japan and 12 countries worldwide.' ), 'shd--c' ); ?>
<ul class="gstats rv">
<li><small><?php echo hj_t( '販売国', 'Countries' ); ?></small><b>12<u><?php echo hj_t( 'ヵ国', '' ); ?></u></b></li>
<li><small><?php echo hj_t( '展開地域', 'Regions' ); ?></small><b>3<u><?php echo hj_t( '地域', '' ); ?></u></b></li>
<li><small><?php echo hj_t( '創業', 'Since' ); ?></small><b>2015<u><?php echo hj_t( '年', '' ); ?></u></b></li></ul>
<?php if ( hj_show_tbc() ) : ?><p class="note ctr-t"><?php echo hj_t( '※ 販売国の一覧は確認のうえ掲載します', 'Country list to be confirmed' ) . ' ' . hj_tbd( '12ヵ国リスト', '12-country list' ); ?></p><?php endif; ?>
<ul class="cells cells--3"><?php echo $regs; ?></ul></div></section>
<section class="sec sec--t" id="china"><div class="wrap">
<?php echo hj_shd( '03', 'Market proven', '中国市場での実績', 'Proven in<br><em>China</em>', '中国市場での実績', hj_t( 'アジア最大で、最も競争の激しい美容市場で、ECから実店舗まで複数のチャネルを築いてきました。', 'Asia\'s largest and most demanding beauty market — where we have built channels from e-commerce to physical retail.' ) ); ?>
<ul class="cells cells--4"><?php echo $china; ?></ul></div></section>
<?php
// ------------------------------------------------------------------ 04 models, 05 terms, 06 support
$rows = '';
foreach ( hj_c( 'MODES' ) as $m ) {
	$rows .= '<tr><th>' . $m[0] . '<small>' . $m[1] . '</small></th><td>' . $m[2] . '</td><td>' . $m[3] . '</td></tr>';
}
$terms = '';
foreach ( hj_pairs( 'terms', 'label', 'value' ) as $t ) {
	$terms .= '<tr><th>' . esc_html( $t[0] ) . '</th><td>' . hj_text( $t[1] ) . '</td></tr>';
}
?>
<section class="sec sec--t blush" id="models"><div class="wrap">
<?php echo hj_shd( '04', 'Models', '協業モデル', 'Cooperation models', '協業モデル' ); ?>
<div class="sx rv"><table class="mtbl"><thead><tr><th><?php echo hj_t( '協業モデル', 'Model' ); ?></th><th><?php echo hj_t( '対象', 'For' ); ?></th><th><?php echo hj_t( 'ご提示する主な条件', 'What we define together' ); ?></th></tr></thead><tbody><?php echo $rows; ?></tbody></table></div></div></section>
<section class="sec sec--t" id="terms"><div class="wrap prof__g">
<div><?php echo hj_shd( '05', 'Trade terms', '取引条件', 'Trade terms', '取引条件', hj_show_tbc() ? hj_t( '数値は確認のうえ掲載します。', 'Figures to be confirmed before publishing.' ) : null ); ?></div>
<table class="ptbl rv"><?php echo $terms; ?></table></div></section>
<section class="sec dark" id="support"><div class="wrap docs__g">
<div><?php echo hj_shd( '06', 'Export support', '輸出書類・<br>各国登録の支援', 'Export documents<br><em>&amp; registration</em>', '輸出書類・登録支援' ); ?></div>
<?php echo hj_docs_list(); ?></div>
<div class="wrap"><div class="mtbl--dark rv"><?php echo hj_reg_table(); ?></div></div></section>
<section class="sec sec--t blush" id="flow"><div class="wrap">
<?php echo hj_shd( '07', 'How to start', 'お取引開始までの流れ', 'How to<br><em>get started</em>', 'お取引の流れ', null, 'shd--c' ) . hj_flow( hj_c( 'PARTNER_STEPS' ) ); ?>
<div class="ctr ctr--2"><?php echo hj_cta_btn( 'partner', 'btn--fill', null, array( '代理店申込フォームへ', 'Apply to become a partner' ) ); ?></div></div></section>
<?php
// ------------------------------------------------------------------ 08 FAQ
$qa = '';
foreach ( hj_pairs( 'faq', 'q', 'a' ) as $i => $f ) {
	$qa .= '<details class="faq__i"' . ( 0 === $i ? ' open' : '' ) . '><summary><span class="faq__q">Q</span><span>' . esc_html( $f[0] ) . '</span></summary><div class="faq__a"><span class="faq__q">A</span><p>' . hj_text( $f[1] ) . '</p></div></details>';
}
?>
<section class="sec" id="faq"><div class="wrap prof__g">
<div><?php echo hj_shd( '08', 'FAQ', 'よくあるご質問', 'Frequently asked<br><em>questions</em>', 'よくあるご質問' ); ?>
<div class="ctas"><?php echo hj_cta_lnk( 'business' ); ?></div></div>
<div class="faq rv"><?php echo $qa; ?></div></div></section>
<?php
get_footer();
