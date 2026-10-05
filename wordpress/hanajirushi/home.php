<?php
/**
 * お知らせ /news/ (mockup: p_news()), also used for category and year archives
 * (/category/exh/, /2026/). Ten per page; categories, years and the next exhibition aside.
 */

defined( 'ABSPATH' ) || exit;

get_header();

echo hj_phero( 'News', 'お知らせ', 'News',
	hj_t( '花印粧業研究所からのお知らせ・展示会・製品情報。', 'Announcements, exhibitions and product news.' ), '', '便り' );

$news_url = (string) get_permalink( (int) get_option( 'page_for_posts' ) );
$current  = is_category() ? get_queried_object()->slug : 'all';
$tabs     = '<a href="' . esc_url( $news_url ) . '"' . ( 'all' === $current ? ' class="on"' : '' ) . '>' . hj_t( 'すべて', 'All' ) . '</a>';
$cats     = get_categories( array( 'hide_empty' => true, 'exclude' => array( (int) get_option( 'default_category' ) ) ) );
$order    = array_flip( array( 'exh', 'prod', 'biz', 'info' ) );   // the mockup's order; other categories after
usort( $cats, fn( $a, $b ) => ( $order[ $a->slug ] ?? 99 ) <=> ( $order[ $b->slug ] ?? 99 ) ?: strcmp( $a->name, $b->name ) );
foreach ( $cats as $c ) {
	$tabs .= '<a href="' . esc_url( get_category_link( $c ) ) . '"' . ( $c->slug === $current ? ' class="on"' : '' ) . '>' . esc_html( hj_term_name( $c ) ) . '</a>';
}

$rows = '';
while ( have_posts() ) {
	the_post();
	if ( hj_has_lang() ) {
		$rows .= hj_news_row( get_post() );
	}
}

// pages: 1 2 3 次へ
$pager = '';
$total = (int) $GLOBALS['wp_query']->max_num_pages;
if ( $total > 1 ) {
	$cur = max( 1, (int) get_query_var( 'paged' ) );
	for ( $i = 1; $i <= $total; $i++ ) {
		$pager .= $i === $cur ? '<span class="on">' . $i . '</span>' : '<a href="' . esc_url( get_pagenum_link( $i ) ) . '">' . $i . '</a>';
	}
	if ( $cur < $total ) {
		$pager .= '<a href="' . esc_url( get_pagenum_link( $cur + 1 ) ) . '">' . hj_t( '次へ', 'Next' ) . '</a>';
	}
	$pager = '<nav class="pager" aria-label="pagination">' . $pager . '</nav>';
}

$side_cats = '';
foreach ( $cats as $c ) {
	$side_cats .= '<li><a href="' . esc_url( get_category_link( $c ) ) . '">' . esc_html( hj_term_name( $c ) ) . '<small>(' . (int) $c->count . ')</small></a></li>';
}
$years = '';
foreach ( $GLOBALS['wpdb']->get_results( "SELECT YEAR(post_date) AS y, COUNT(*) AS n FROM {$GLOBALS['wpdb']->posts} WHERE post_type = 'post' AND post_status = 'publish' GROUP BY y ORDER BY y DESC" ) as $y ) {
	$years .= '<li><a href="' . esc_url( get_year_link( (int) $y->y ) ) . '">' . (int) $y->y . '<small>(' . (int) $y->n . ')</small></a></li>';
}
?>
<section class="sec sec--t"><div class="wrap news__g">
<div class="rv"><div class="ftabs ftabs--links" role="navigation" aria-label="<?php echo esc_attr( hj_t( 'カテゴリー', 'Categories' ) ); ?>"><?php echo $tabs; ?></div>
<?php if ( $rows ) : ?>
<ul class="nl"><?php echo $rows; ?></ul>
<?php else : ?>
<p class="exl__none"><?php echo hj_t( 'お知らせはまだありません。', 'No news yet.' ); ?></p>
<?php endif; ?>
<?php echo $pager; ?></div>
<aside class="side rv"><p class="pform__h"><?php echo hj_t( 'カテゴリー', 'Categories' ); ?></p><ul class="dlist"><?php echo $side_cats; ?></ul>
<p class="pform__h"><?php echo hj_t( 'アーカイブ', 'Archive' ); ?></p><ul class="dlist"><?php echo $years; ?></ul>
<?php echo hj_exh_card(); ?></aside>
</div></section>
<?php
get_footer();
