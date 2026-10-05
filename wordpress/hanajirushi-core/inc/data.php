<?php
/**
 * Reading content in the language being shown. The theme only calls these, so it never
 * needs to know how a field is stored.
 */

defined( 'ABSPATH' ) || exit;

/** A field in the language being shown (name on Japanese pages, name_en on English ones). */
function hj_get( string $name, $post_id = null ) {
	return hj_raw( hj_is_en() ? $name . '_en' : $name, $post_id );
}

/** A field that is the same in both languages. */
function hj_raw( string $name, $post_id = null ) {
	$post_id = $post_id ?: get_the_ID();
	if ( function_exists( 'get_field' ) ) {
		return get_field( $name, $post_id );
	}
	return get_post_meta( $post_id, $name, true );
}

/** Title in the language being shown (English titles are the title_en field). */
function hj_title( $post = null ): string {
	$post = get_post( $post );
	if ( ! $post ) {
		return '';
	}
	return hj_is_en() ? (string) get_post_meta( $post->ID, 'title_en', true ) : get_the_title( $post );
}

/** Whether a post has the language being shown (English needs an English title). */
function hj_has_lang( $post = null ): bool {
	return '' !== trim( hj_title( $post ) );
}

/** A サイト設定 field in the language being shown. */
function hj_opt( string $name ) {
	return hj_opt_raw( hj_is_en() ? $name . '_en' : $name );
}

function hj_opt_raw( string $name ) {
	return function_exists( 'get_field' ) ? get_field( $name, 'option' ) : get_option( 'options_' . $name );
}

/** 要確認 marks are shown only while the サイト設定 switch is on (review site, before launch). */
function hj_show_tbc(): bool {
	return (bool) hj_opt_raw( 'show_tbc' );
}

/**
 * ［…］ in any text marks a fact still to confirm: shown as the 要確認 mark while サイト設定 →
 * 表示 is on (review site), removed when it is off (live site). Works on escaped text or HTML.
 */
function hj_marks( string $html ): string {
	return preg_replace_callback( '/［([^］]*)］/u', function ( $m ) {
		return hj_show_tbc() ? '<span class="tbd">' . $m[1] . '</span>' : '';
	}, $html );
}

/**
 * Rows of a サイト設定 table (profile_rows, history, terms, faq) in the language being shown:
 * [[first, second]…]. English pages skip rows whose English first column is empty.
 */
function hj_pairs( string $name, string $a, string $b ): array {
	$out = array();
	foreach ( (array) hj_opt_raw( $name ) as $row ) {
		$x = hj_is_en() ? (string) ( $row[ $a . '_en' ] ?? '' ) : (string) ( $row[ $a ] ?? '' );
		$y = hj_is_en() ? (string) ( $row[ $b . '_en' ] ?? '' ) : (string) ( $row[ $b ] ?? '' );
		if ( '' !== trim( $x ) ) {
			$out[] = array( $x, $y );
		}
	}
	return $out;
}

/** Exhibitions: 'upcoming' (last day today or later, soonest first) or 'past' (latest first). */
function hj_exhibitions( string $which = 'upcoming' ): array {
	$today = wp_date( 'Ymd' );
	$all   = get_posts( array(
		'post_type'      => 'exhibition',
		'posts_per_page' => -1,
		'meta_key'       => 'end',
		'orderby'        => 'meta_value',
		'order'          => 'upcoming' === $which ? 'ASC' : 'DESC',
		'meta_query'     => hj_lang_meta_query(),
	) );
	return array_values( array_filter( $all, function ( $p ) use ( $which, $today ) {
		$end = (string) hj_raw( 'end', $p->ID );
		return 'upcoming' === $which ? ( '' === $end || $end >= $today ) : ( '' !== $end && $end < $today );
	} ) );
}

/** URL of a media library file (PDF, QR image), or ''. */
function hj_file_url( $id ): string {
	return $id ? (string) wp_get_attachment_url( (int) $id ) : '';
}

/** Non-empty lines of a text area. */
function hj_split_lines( $text ): array {
	return array_values( array_filter( array_map( 'trim', preg_split( '/\R/u', (string) $text ) ), 'strlen' ) );
}

function hj_label( array $map, $key ): string {
	return isset( $map[ $key ] ) ? hj_t( $map[ $key ][0], $map[ $key ][1] ) : '';
}

/** Product categories in display order: key => label. */
function hj_categories(): array {
	$out = array();
	foreach ( HJ_CATS as $k => $v ) {
		$out[ $k ] = hj_t( $v[0], $v[1] );
	}
	return $out;
}

/** Photo of a product: the featured image, else the temporary image address. */
function hj_product_photo( int $id, string $size = 'large' ): string {
	$url = get_the_post_thumbnail_url( $id, $size );
	return $url ?: (string) hj_raw( 'image_temp', $id );
}

/** A meta query that keeps only posts with an English title, on English pages. */
function hj_lang_meta_query(): array {
	return hj_is_en() ? array( array( 'key' => 'title_en', 'value' => '', 'compare' => '!=' ) ) : array();
}

/** Products in display order. */
function hj_products( array $args = array() ): array {
	$q = new WP_Query( array_merge( array(
		'post_type'      => 'product',
		'posts_per_page' => -1,
		'orderby'        => array( 'menu_order' => 'ASC', 'title' => 'ASC' ),
		'meta_query'     => hj_lang_meta_query(),
		'no_found_rows'  => true,
	), $args ) );
	return $q->posts;
}

/** Slides showing today, in order. */
function hj_slides(): array {
	$today = wp_date( 'Ymd' );
	$out   = array();
	$q     = new WP_Query( array(
		'post_type'      => 'kv_slide',
		'posts_per_page' => -1,
		'orderby'        => array( 'menu_order' => 'ASC', 'date' => 'ASC' ),
		'meta_query'     => hj_lang_meta_query(),
		'no_found_rows'  => true,
	) );
	foreach ( $q->posts as $p ) {
		$start = (string) hj_raw( 'start', $p->ID );
		$end   = (string) hj_raw( 'end', $p->ID );
		if ( ( $start && $start > $today ) || ( $end && $end < $today ) ) {
			continue;
		}
		$out[] = $p;
	}
	return $out;
}

function hj_collabs(): array {
	return get_posts( array(
		'post_type'      => 'collab',
		'posts_per_page' => -1,
		'orderby'        => array( 'menu_order' => 'ASC', 'title' => 'ASC' ),
		'meta_query'     => hj_lang_meta_query(),
	) );
}

/** Latest news posts in the language being shown. */
function hj_news( int $n = 5 ): array {
	return get_posts( array(
		'post_type'      => 'post',
		'posts_per_page' => $n,
		'meta_query'     => hj_lang_meta_query(),
	) );
}

/** A news category's label in the language being shown (English name in the term description's first line, or name_en). */
function hj_term_name( WP_Term $term ): string {
	if ( hj_is_en() ) {
		$en = (string) get_term_meta( $term->term_id, 'name_en', true );
		return $en ?: $term->name;
	}
	return $term->name;
}

/** A site link: /path/ gets the site address (and /en on English pages); full URLs stay. */
function hj_link( $path ): string {
	$path = trim( (string) $path );
	if ( '' === $path ) {
		return '';
	}
	if ( preg_match( '#^(https?:)?//#', $path ) || str_starts_with( $path, '#' ) || str_starts_with( $path, 'mailto:' ) || str_starts_with( $path, 'tel:' ) ) {
		return $path;
	}
	return home_url( $path );
}

// English news lists only count news that has English (so paging stays at ten per page).
add_action( 'pre_get_posts', function ( WP_Query $q ) {
	if ( ! is_admin() && $q->is_main_query() && hj_is_en() && ( $q->is_home() || $q->is_category() || $q->is_date() ) ) {
		$q->set( 'meta_query', hj_lang_meta_query() );
	}
} );

// English pages of posts that have no English: not found.
add_action( 'template_redirect', function () {
	if ( hj_is_en() && is_singular( array( 'product', 'post' ) ) && ! hj_has_lang( get_queried_object() ) ) {
		global $wp_query;
		$wp_query->set_404();
		status_header( 404 );
	}
	// Coming-soon products have no page yet.
	if ( is_singular( 'product' ) && hj_raw( 'coming_soon', get_queried_object_id() ) ) {
		wp_safe_redirect( home_url( '/products/' ), 302 );
		exit;
	}
}, 5 );
