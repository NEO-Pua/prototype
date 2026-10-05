<?php
/**
 * Fallback for pages without their own template yet (the remaining lower pages are built
 * after the proof): title band, then the content.
 */

defined( 'ABSPATH' ) || exit;

get_header();

if ( is_404() ) {
	echo hj_phero( 'Not found', 'ページが見つかりません', 'Page not found', hj_t( 'お探しのページは移動または削除された可能性があります。', 'The page may have moved or been removed.' ), '', '404' );
	echo '<section class="sec sec--t"><div class="wrap">' . hj_btn( hj_link( '/' ), 'トップページへ', 'Back to the home page', 'btn--fill' ) . '</div></section>';
} else {
	while ( have_posts() ) {
		the_post();
		$title = esc_html( hj_title() );
		echo hj_phero( strtoupper( (string) get_post_field( 'post_name' ) ), $title, $title, '', '', '' );
		$body = hj_is_en() && 'post' === get_post_type() ? (string) hj_raw( 'body_en' ) : apply_filters( 'the_content', get_the_content() );
		echo '<section class="sec sec--t"><div class="wrap"><div class="entry">' . wp_kses_post( $body ) . '</div></div></section>';
	}
}

get_footer();
