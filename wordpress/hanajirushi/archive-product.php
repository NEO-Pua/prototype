<?php
/**
 * 製品一覧 /products/ (mockup: p_products13()): every product, filtered by category in the
 * page (premium-v13.js; ?cat=<key> opens it filtered). A new product is one new 製品 post.
 */

defined( 'ABSPATH' ) || exit;

get_header();

$all    = array_values( array_filter( $GLOBALS['wp_query']->posts, 'hj_has_lang' ) );
$counts = array();
foreach ( $all as $p ) {
	$c            = (string) hj_raw( 'category', $p->ID );
	$counts[ $c ] = ( $counts[ $c ] ?? 0 ) + 1;
}
$tabs = '<button type="button" data-cat="all" class="on">' . hj_t( 'すべて', 'All' ) . '<small>' . count( $all ) . '</small></button>';
foreach ( hj_categories() as $k => $label ) {
	if ( ! empty( $counts[ $k ] ) ) {
		$tabs .= '<button type="button" data-cat="' . esc_attr( $k ) . '">' . esc_html( $label ) . '<small>' . (int) $counts[ $k ] . '</small></button>';
	}
}
$cards = '';
foreach ( $all as $i => $p ) {
	$cards .= hj_pcard( $p, $i + 1 );
}
$temp = (bool) array_filter( $all, fn( $p ) => ! has_post_thumbnail( $p ) && hj_raw( 'image_temp', $p->ID ) );

echo hj_phero( 'Products', '製品', 'Products',
	hj_t( 'クレンジングから保湿、UVケアまで。毎日の肌に寄り添う、日本製のスキンケア。', 'From cleansing to moisturising and UV care — Japanese skincare for every day.' ),
	'', '製品' );
?>
<section class="sec sec--t plist13" id="list"><div class="wrap">
<div class="pfilter rv" role="group" aria-label="<?php echo esc_attr( hj_t( 'カテゴリーで絞り込む', 'Filter by category' ) ); ?>"><?php echo $tabs; ?></div>
<ul class="pgrid pgrid--all"><?php echo $cards; ?></ul>
<?php if ( $temp ) : ?>
<p class="note"><?php echo hj_t( '※ 製品画像の一部は、楽天市場 花印公式ショップの商品画像を仮に表示しています。正式な製品写真に差し替えます。', 'Some product images are temporary, taken from our Japanese online store, and will be replaced with final photography.' ); ?></p>
<?php endif; ?>
<?php if ( hj_is_en() ) : ?>
<p class="note">Trade specifications (INCI, shelf life, JAN codes, case packs) and price lists are available on request. <?php echo hj_cta_lnk( 'product', 'lnk--s' ); ?></p>
<?php endif; ?>
</div></section>
<?php
echo hj_brand_collab( '01', 'collab' );   // moved here from the brand page (client, 2026-10-07)
get_template_part( 'template-parts/stores' );
get_footer();
