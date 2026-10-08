<?php
/**
 * Home page (mockup: p_home() for v1.3): slider → figures → news → products → brand →
 * 日本製 → collaborations → partnership → company → online stores.
 */

defined( 'ABSPATH' ) || exit;

get_header();
get_template_part( 'template-parts/home-hero' );

// ------------------------------------------------------------------ figures
$figs = array(
	array( hj_t( '創業', 'Since' ), '2015' . hj_t( '<u>年</u>', '' ), hj_t( '東京・銀座で創業。研究開発型のスキンケアメーカー', 'Founded in Ginza, Tokyo as an R&amp;D-led skincare maker' ) ),
	array( hj_t( '本社', 'Tokyo HQ' ), hj_t( '銀座', 'Ginza' ), hj_t( '東京・銀座二丁目に本社・研究室・ショールーム', 'Head office, lab and showroom in Ginza 2-chome' ) ),
	array( hj_t( '世界', 'Sold in' ), '12' . hj_t( '<u>ヵ国</u>', '<u>countries</u>' ), hj_t( '日本国内のほか世界12ヵ国で販売', 'Sold in Japan and 12 countries worldwide' ) ),
	array( hj_t( '処方開発', 'Formulation' ), hj_t( '自社研究室', 'Own lab' ), hj_t( '原料レベルから自社で処方を開発', 'Formulated in-house from the raw-material level' ) ),
);
echo '<section class="nums nums--4"><div class="wrap"><ul class="nums__l">';
foreach ( $figs as $f ) {
	echo '<li class="rv"><small>' . $f[0] . '</small><b class="' . ( ctype_digit( substr( $f[1], 0, 1 ) ) ? 'num' : 'word' ) . '">' . $f[1] . '</b><p>' . $f[2] . '</p></li>';
}
echo '</ul></div></section>';

// ------------------------------------------------------------------ 01 news
$rows = '';
foreach ( hj_news( 5 ) as $np ) {
	$rows .= hj_news_row( $np );
}
?>
<section class="sec news" id="exhibition"><div class="wrap news__g news__g--wide">
<div class="rv"><?php echo hj_shd( '01', 'News', 'お知らせ', 'News', 'お知らせ' ); ?>
<ul class="nl"><?php echo $rows; ?></ul>
<?php echo hj_lnk( hj_link( '/news/' ), 'お知らせ一覧', 'All news' ); ?></div>
</div></section>
<?php
// ------------------------------------------------------------------ 02 products
$cards = '';
foreach ( hj_home_products() as $i => $p ) {
	$cards .= hj_pcard( $p, $i + 1 );
}
$chips = '';
foreach ( hj_categories() as $k => $label ) {
	$chips .= '<a href="' . esc_url( hj_link( '/products/?cat=' . $k . '#list' ) ) . '">' . esc_html( $label ) . '</a>';
}
?>
<section class="sec col13" id="collection"><div class="wrap">
<div class="col13__h"><?php echo hj_shd( '02', 'Our skincare', '花印のスキンケア', 'Our skincare', '製品', hj_t( 'クレンジングから保湿、UVケアまで。毎日の肌に寄り添う、日本製のスキンケアです。', 'From cleansing to moisturising and UV care — Japanese skincare for every day.' ) ); ?>
<?php echo hj_btn( hj_link( '/products/' ), 'すべての製品を見る', 'All products' ); ?></div>
<nav class="col13__cats rv" aria-label="<?php echo esc_attr( hj_t( 'カテゴリー', 'Categories' ) ); ?>"><?php echo $chips; ?></nav>
<ul class="pgrid"><?php echo $cards; ?></ul>
</div></section>

<?php // ------------------------------------------------------------------ 03 brand ?>
<section class="sec blush br13" id="brand"><div class="wrap br13__g">
<div class="br13__mark rv"><?php echo hj_seal( '花印', 'seal--xl' ); ?><p class="br13__tate" aria-hidden="true">ひとりに、ひとつの、<br>キレイを咲かせる。</p><?php echo hj_slogan_en( 'slogan-en--mark' ); ?></div>
<div class="br13__txt rv"><?php echo hj_shd( '03', 'Brand', '肌に咲く、<br>花の印。', 'Hana-jirushi —<br><em>a flower\'s seal.</em>', 'ブランド' ); ?>
<p><?php echo hj_t( '人の肌を想い、ひとりの悩みを見つめ、ひとつしかないキレイを、メイド・イン・ジャパンのスキンケアの力で届けていく。', 'We look closely at each person\'s skin and each individual concern, and deliver a beauty that is theirs alone — with the power of Japanese-made skincare.' ); ?></p>
<p><?php echo hj_t( '「花印」の名には、ひとりひとりの肌に咲く花の印という想いを込めています。日本ならではの上質で誠実なものづくりが認められ、花印は国内はもとより世界12ヵ国で販売されています。', 'The name HANAJIRUSHI, “flower seal”, stands for the mark of a flower blooming on each person\'s skin. Recognised for the quality and honesty of Japanese manufacturing, our products are sold in Japan and 12 countries worldwide.' ); ?></p>
<div class="ctas"><?php echo hj_btn( hj_link( '/brand/' ), 'ブランドについて', 'About the brand', 'btn--fill' ) . hj_lnk( hj_link( '/rd/' ), '研究開発・品質管理', 'R&amp;D and quality' ); ?></div></div>
</div><?php echo hj_brand_film(); ?></section>
<?php
// ------------------------------------------------------------------ 04 made in Japan
$j4  = array(
	array( '研', hj_t( '日本で開発', 'Developed in Japan' ), hj_t( '日本市場で培った商品開発力', 'Product development honed in the Japanese market' ), '' ),
	array( '造', hj_t( '日本で製造', 'Made in Japan' ), hj_t( '日本国内での確かなものづくり', 'Reliable manufacturing in Japan' ), hj_tbd( '製造地 要確認', 'Site TBC' ) ),
	array( '質', hj_t( '日本で品質管理', 'Quality-checked in Japan' ), hj_t( '日本基準での品質管理・検品', 'Quality control and inspection to Japanese standards' ), hj_tbd() ),
	array( '績', hj_t( '世界での実績', 'Proven worldwide' ), hj_t( '海外市場で積み重ねてきた取引・パートナー実績', 'A track record of trade and partnerships in overseas markets' ), '' ),
);
$li4 = '';
foreach ( $j4 as $i => $j ) {
	$li4 .= '<li class="rv">' . hj_j4_mark( $i, $j[0] ) . '<p class="j4__n">' . sprintf( '%02d', $i + 1 ) . '</p><h3>' . $j[1] . '</h3><p>' . $j[2] . '</p>' . $j[3] . '</li>';
}
?>
<section class="sec dark j4" id="japan"><div class="wrap">
<?php echo hj_shd( '04', 'Made in Japan', '「日本製」4つの強み', 'Made in Japan —<br><em>four strengths</em>', '日本製の強み', hj_t( '「日本製」というラベルだけでなく、その中身をお伝えします。', 'Not just a label — what “Made in Japan” means for your business.' ), 'shd--c' ); ?>
<ol class="j4__l"><?php echo $li4; ?></ol>
<div class="ctr"><?php echo hj_lnk( hj_link( '/rd/' ), '研究開発・品質管理を見る', 'R&amp;D and quality' ); ?></div>
</div></section>
<?php
// ------------------------------------------------------------------ 05 collaborations
$ips = '';
foreach ( hj_collabs() as $c ) {
	$ips .= '<li class="rv"><figure><img src="' . esc_url( (string) get_the_post_thumbnail_url( $c, 'large' ) ) . '" alt="' . esc_attr( hj_title( $c ) ) . '" loading="lazy"></figure><p><b>' . esc_html( hj_title( $c ) ) . '</b><small>'
		. esc_html( (string) hj_get( 'product', $c->ID ) ) . '</small></p><span class="tag">' . esc_html( (string) hj_get( 'label', $c->ID ) ) . '</span></li>';
}
?>
<section class="sec collab"><div class="wrap collab__g">
<div class="collab__txt rv"><?php echo hj_shd( '05', 'Collaboration', '人気IPと、<br>正規ライセンスで。', 'Beloved Japanese IP,<br><em>officially licensed.</em>', 'IPコラボレーション' ); ?>
<p><?php echo hj_t( '日本の人気IPと正規ライセンスを結び、処方からパッケージ、ギフトセットまで一貫して企画・開発しています。', 'Official licences with leading Japanese IP — with full co-development from formula to packaging and gift sets.' ); ?></p>
<p class="note"><?php echo hj_t( 'すべてのコラボレーション商品は正規ライセンス品です。ライセンス証明書類はお取引先にご提示できます。', 'All collaboration products are officially licensed. Proof of licence is available to trade partners.' ); ?></p>
<div class="lnks"><?php echo hj_lnk( hj_link( '/collaboration/' ), 'コラボレーション一覧', 'All collaborations' ) . hj_cta_lnk( 'oem' ); ?></div></div>
<ul class="collab__l"><?php echo $ips; ?></ul>
</div></section>
<?php
// ------------------------------------------------------------------ 06 partnership
$chans = '';
foreach ( hj_t( array( '独占代理店', '販売代理店', 'モダントレード供給', '越境EC' ), array( 'Exclusive distributor', 'Authorised reseller', 'Modern trade supply', 'Cross-border e-commerce' ) ) as $i => $c ) {
	$chans .= '<li><i>' . sprintf( '%02d', $i + 1 ) . '</i>' . $c . '</li>';
}
?>
<section class="sec gp13" id="partners"><div class="wrap gp13__g">
<div class="rv"><?php echo hj_shd( '06', 'Partnership', '海外のパートナーの<br>皆さまへ', 'For partners<br><em>around the world</em>', 'パートナーシップ' ); ?>
<p class="gp13__lead"><?php echo hj_t( '日本ならではの上質で誠実なものづくりを、世界のお客様へ。それぞれの市場をよく知るパートナーの皆さまと、花印の新しい可能性を育てていきます。', 'Japanese quality and honest manufacturing, for customers around the world. We grow Hanajirushi together with partners who know their markets.' ); ?></p>
<div class="ctas"><?php echo hj_btn( hj_link( '/partners/' ), 'パートナーシップについて', 'Partnership programme', 'btn--fill' ) . hj_cta_lnk( 'partner' ); ?></div></div>
<div class="gp13__fig rv"><img src="<?php echo esc_url( hj_img( 'world_map_v15.png' ) ); ?>" alt="<?php echo esc_attr( hj_t( '販売地域の地図', 'Map of our markets' ) ); ?>" loading="lazy">
<p class="gp13__big"><b>12</b><span><?php echo hj_t( 'ヵ国で販売', 'countries' ); ?></span></p>
<ol class="gp13__ch"><?php echo $chans; ?></ol></div>
</div></section>
<?php // ------------------------------------------------------------------ 07 company ?>
<section class="sec dark cosplit"><div class="wrap split__g">
<div class="split__img rv"><div class="arch"><img src="<?php echo esc_url( hj_img( 'h_campany_bldg.jpg' ) ); ?>" alt="<?php echo esc_attr( hj_t( '銀座二丁目の本社ビル', 'Head office building, Ginza 2-chome' ) ); ?>" loading="lazy"></div></div>
<div class="split__txt rv"><?php echo hj_shd( '07', 'Company', '銀座から、世界へ。', 'From Ginza,<br><em>to the world.</em>', '会社情報' ); ?>
<dl class="dl">
<div><dt><?php echo hj_t( '社名', 'Company' ); ?></dt><dd><?php echo esc_html( (string) hj_opt( 'company' ) ); ?></dd></div>
<div><dt><?php echo hj_t( '創業', 'Founded' ); ?></dt><dd><?php echo esc_html( (string) hj_opt( 'founded' ) ); ?></dd></div>
<div><dt><?php echo hj_t( '本社', 'Head office' ); ?></dt><dd><?php echo hj_text( hj_opt( 'address' ) ); ?></dd></div>
</dl>
<div class="ctas"><?php echo hj_btn( hj_link( '/company/' ), '会社概要', 'Company profile', 'btn--light' ) . hj_lnk( hj_link( '/company/#access' ), 'アクセス', 'Access' ); ?></div></div>
</div></section>
<?php
get_template_part( 'template-parts/stores' );
get_footer();
