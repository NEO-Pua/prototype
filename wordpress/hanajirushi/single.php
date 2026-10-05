<?php
/**
 * One news article. The mockup has no article page, so this keeps to its pieces: the plain
 * title band, the news line's date and category, the text, then back to the list.
 */

defined( 'ABSPATH' ) || exit;

get_header();

the_post();
$post  = get_post();
$cat   = get_the_category( $post->ID );
$cname = $cat ? hj_term_name( $cat[0] ) : '';
$body  = hj_is_en() ? (string) hj_raw( 'body_en' ) : apply_filters( 'the_content', get_the_content() );
$news  = (string) get_permalink( (int) get_option( 'page_for_posts' ) );
$prev  = get_previous_post();
$next  = get_next_post();
?>
<nav class="crumb crumb--pdx" aria-label="breadcrumb"><div class="wrap"><a href="<?php echo esc_url( hj_link( '/' ) ); ?>"><?php echo hj_t( 'ホーム', 'Home' ); ?></a><a href="<?php echo esc_url( $news ); ?>"><?php echo hj_t( 'お知らせ', 'News' ); ?></a><span><?php echo esc_html( hj_title( $post ) ); ?></span></div></nav>
<article class="sec sec--t art"><div class="wrap art__w">
<header class="art__h rv"><p class="art__m"><time datetime="<?php echo esc_attr( get_the_date( 'Y-m-d' ) ); ?>"><?php echo esc_html( get_the_date( 'Y.m.d' ) ); ?></time><?php echo $cname ? '<a class="cat" href="' . esc_url( get_category_link( $cat[0] ) ) . '">' . esc_html( $cname ) . '</a>' : ''; ?></p>
<h1 class="art__t"><?php echo esc_html( hj_title( $post ) ); ?></h1></header>
<?php if ( trim( wp_strip_all_tags( $body ) ) || has_post_thumbnail() ) : ?>
<div class="entry rv"><?php echo has_post_thumbnail() ? get_the_post_thumbnail( $post, 'large' ) : ''; ?><?php echo wp_kses_post( $body ); ?></div>
<?php endif; ?>
<nav class="art__nav rv" aria-label="<?php echo esc_attr( hj_t( '前後のお知らせ', 'More news' ) ); ?>">
<?php
foreach ( array( array( $prev, '前のお知らせ', 'Previous' ), array( $next, '次のお知らせ', 'Next' ) ) as $n ) {
	if ( $n[0] && hj_has_lang( $n[0] ) ) {
		echo '<a href="' . esc_url( get_permalink( $n[0] ) ) . '"><small>' . hj_t( $n[1], $n[2] ) . '</small>' . esc_html( hj_title( $n[0] ) ) . '</a>';
	}
}
?>
</nav>
<div class="ctr"><?php echo hj_lnk( $news, 'お知らせ一覧', 'All news' ); ?></div>
</div></article>
<?php
get_footer();
