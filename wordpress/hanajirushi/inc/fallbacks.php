<?php
/**
 * If the 花印 HANAJIRUSHI Core plugin is not active, the theme still loads (Japanese only,
 * no products or slides) instead of breaking the site, and tells administrators why.
 */

defined( 'ABSPATH' ) || exit;

if ( ! function_exists( 'hj_t' ) ) {
	function hj_lang(): string { return 'ja'; }
	function hj_is_en(): bool { return false; }
	function hj_t( $ja, $en ) { return $ja; }
	function hj_get( string $name, $post_id = null ) { return get_post_meta( $post_id ?: get_the_ID(), $name, true ); }
	function hj_raw( string $name, $post_id = null ) { return get_post_meta( $post_id ?: get_the_ID(), $name, true ); }
	function hj_title( $post = null ): string { return get_the_title( $post ); }
	function hj_has_lang( $post = null ): bool { return true; }
	function hj_opt( string $name ) { return ''; }
	function hj_opt_raw( string $name ) { return ''; }
	function hj_show_tbc(): bool { return false; }
	function hj_marks( string $html ): string { return preg_replace( '/［[^］]*］/u', '', $html ); }
	function hj_pairs( string $name, string $a, string $b ): array { return array(); }
	function hj_exhibitions( string $which = 'upcoming' ): array { return array(); }
	function hj_file_url( $id ): string { return $id ? (string) wp_get_attachment_url( (int) $id ) : ''; }
	function hj_form_value( string $name ) { return ''; }
	function hj_fname( string $name ): string { return 'k' === $name ? 'k' : 'f_' . $name; }
	function hj_form_opt( string $key ): array { return array(); }
	function hj_form(): array { return array( 'step' => 'input', 'values' => array(), 'errors' => array(), 'form' => '' ); }
	function hj_split_lines( $text ): array { return array_values( array_filter( array_map( 'trim', preg_split( '/\R/u', (string) $text ) ), 'strlen' ) ); }
	function hj_categories(): array { return array(); }
	function hj_label( array $map, $key ): string { return ''; }
	function hj_product_photo( int $id, string $size = 'large' ): string { return (string) get_the_post_thumbnail_url( $id, $size ); }
	function hj_products( array $args = array() ): array { return array(); }
	function hj_slides(): array { return array(); }
	function hj_collabs(): array { return array(); }
	function hj_news( int $n = 5 ): array { return get_posts( array( 'posts_per_page' => $n ) ); }
	function hj_term_name( WP_Term $term ): string { return $term->name; }
	function hj_link( $path ): string { return preg_match( '#^(https?:)?//#', (string) $path ) ? (string) $path : home_url( (string) $path ); }
	function hj_switch_url( string $lang ): string { return home_url( 'en' === $lang ? '/en/' : '/' ); }

	add_action( 'admin_notices', function () {
		if ( current_user_can( 'activate_plugins' ) ) {
			echo '<div class="notice notice-warning"><p><b>花印 HANAJIRUSHI テーマ:</b> プラグイン「花印 HANAJIRUSHI Core」を有効にしてください。製品・スライド・英語ページはこのプラグインで動きます。</p></div>';
		}
	} );
}
if ( ! defined( 'HJ_CATS' ) ) {
	define( 'HJ_CATS', array() );
	define( 'HJ_SERIES', array() );
	define( 'HJ_KINDS', array() );
}
