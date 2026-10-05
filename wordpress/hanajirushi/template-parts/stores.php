<?php
/**
 * Online stores (mockup: store_section()). Japanese: the domestic stores. English: no
 * consumer store links (EN_ONLY rule) — a distributor line instead.
 */

defined( 'ABSPATH' ) || exit;

if ( hj_is_en() ) : ?>
<section class="stores" id="stores"><div class="wrap stores__en rv">
<p class="eb"><span>Where to buy</span></p><h2>Looking for Hanajirushi in your country?</h2>
<p>We are building our distributor network. Contact us to find a local partner — or to become one.</p>
<?php echo hj_lnk( hj_link( '/partners/' ), '', 'Find / become a distributor' ); ?></div></section>
<?php
	return;
endif;

$stores = array(
	array( 'rakuten.svg', '楽天市場 公式ショップ', 'https://www.rakuten.co.jp/hanajirushi/' ),
	array( 'amazon.png', 'Amazon 公式ストア', '#' ),
	array( 'yahoo.svg', 'Yahoo!ショッピング', '#' ),
	array( 'qoo10.png', 'Qoo10 公式ショップ', '#' ),
);
$li = '';
foreach ( $stores as $s ) {
	$ext = '#' !== $s[2] ? ' target="_blank" rel="noopener"' : '';
	$li .= '<li><a href="' . esc_url( $s[2] ) . '"' . $ext . '><img src="' . esc_url( hj_img( $s[0] ) ) . '" alt="' . esc_attr( $s[1] ) . '"><small>' . esc_html( $s[1] ) . '</small></a></li>';
}
?>
<section class="stores" id="stores"><div class="wrap rv">
<p class="eb"><span>Online store</span></p><h2>国内公式オンラインストア</h2><ul class="stores__l"><?php echo $li; ?></ul></div></section>
