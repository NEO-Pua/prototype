<?php
/**
 * 花印 HANAJIRUSHI theme.
 *
 * Presentation only: templates, the design's CSS/JS (assets/, the same files as the mockup)
 * and the fixed copy of the page layouts. Content and its structure come from the
 * 花印 HANAJIRUSHI Core plugin (products, slides, collaborations, settings, JA/EN).
 */

defined( 'ABSPATH' ) || exit;

define( 'HJ_THEME_VERSION', '0.4.0' );

require get_template_directory() . '/inc/fallbacks.php';
require get_template_directory() . '/inc/helpers.php';
require get_template_directory() . '/inc/products.php';
require get_template_directory() . '/inc/chrome.php';

add_action( 'after_setup_theme', function () {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
} );

const HJ_FONTS = 'https://fonts.googleapis.com/css2?family=Zen+Old+Mincho:wght@400;500;600&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400;1,6..96,500&family=Noto+Sans+JP:wght@300;400;500&family=Jost:wght@300;400;500&display=swap';

add_action( 'wp_enqueue_scripts', function () {
	$u = get_template_directory_uri() . '/assets/';
	$v = HJ_THEME_VERSION;
	wp_enqueue_style( 'hj-fonts', HJ_FONTS, array(), null );
	wp_enqueue_style( 'hj-premium', $u . 'css/premium.css', array( 'hj-fonts' ), $v );
	wp_enqueue_style( 'hj-premium-v11', $u . 'css/premium-v11.css', array( 'hj-premium' ), $v );
	$lp = is_page( 'cosmoprof-asia' );   // the buyer page: the mockup's buyer-page stack (no slider CSS)
	if ( $lp ) {
		wp_enqueue_style( 'hj-premium-lp', $u . 'css/premium-lp.css', array( 'hj-premium-v11' ), $v );
		wp_enqueue_style( 'hj-premium-v13', $u . 'css/premium-v13.css', array( 'hj-premium-lp' ), $v );
	} else {
		wp_enqueue_style( 'hj-premium-v12', $u . 'css/premium-v12.css', array( 'hj-premium-v11' ), $v );
		wp_enqueue_style( 'hj-premium-v13', $u . 'css/premium-v13.css', array( 'hj-premium-v12' ), $v );
	}
	wp_enqueue_style( 'hj-premium-v14', $u . 'css/premium-v14.css', array( 'hj-premium-v13' ), $v );
	wp_enqueue_style( 'hj-premium-v15', $u . 'css/premium-v15.css', array( 'hj-premium-v14' ), $v );
	wp_enqueue_style( 'hj-wp', $u . 'css/wp.css', array( 'hj-premium-v15' ), $v );

	wp_enqueue_script( 'hj-premium', $u . 'js/premium.js', array(), $v, true );
	wp_enqueue_script( 'hj-premium-v11', $u . 'js/premium-v11.js', array( 'hj-premium' ), $v, true );
	if ( is_front_page() ) {
		wp_enqueue_script( 'hj-premium-v12', $u . 'js/premium-v12.js', array( 'hj-premium' ), $v, true );
		wp_enqueue_script( 'hj-premium-v15', $u . 'js/premium-v15.js', array(), $v, true );   // the brand film
	}
	if ( $lp ) {
		wp_enqueue_script( 'hj-qrcode', 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js', array(), null, true );
		wp_enqueue_script( 'hj-premium-lp', $u . 'js/premium-lp.js', array( 'hj-premium-v11', 'hj-qrcode' ), $v, true );
	} else {
		wp_enqueue_script( 'hj-premium-v13', $u . 'js/premium-v13.js', array( 'hj-premium' ), $v, true );
	}
	if ( is_singular( 'product' ) ) {   // the store chooser behind 「この製品を購入する」
		wp_enqueue_script( 'hj-premium-v14', $u . 'js/premium-v14.js', array(), $v, true );
	}

	// Logged-in staff: keep the fixed header below the WordPress toolbar.
	if ( is_admin_bar_showing() ) {
		wp_add_inline_style( 'hj-wp', '@media (min-width:601px){.admin-bar .hd,.admin-bar .lp-hd{top:var(--wp-admin--admin-bar--height,32px)}}' );
	}

	// No block styles on a theme that does not use blocks on the front end.
	wp_dequeue_style( 'wp-block-library' );
	wp_dequeue_style( 'classic-theme-styles' );
	wp_dequeue_style( 'global-styles' );
} );

// The design's scripts expect html.js before the stylesheets load; fonts connect early.
add_action( 'wp_head', function () {
	echo "<script>document.documentElement.classList.add('js')</script>\n";
	echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
}, 0 );

// The live site: the design's scripts let forms send and store links open (premium.js).
add_filter( 'language_attributes', function ( $out ) {
	return is_admin() ? $out : $out . ' data-live';
}, 20 );

// Page titles as in the mockup.
add_filter( 'pre_get_document_title', function () {
	$site = hj_t( '花印 HANAJIRUSHI 公式サイト', 'HANAJIRUSHI — Japanese Skincare, Ginza Tokyo' );
	if ( is_front_page() ) {
		return hj_t( '花印 HANAJIRUSHI 公式サイト｜花印粧業研究所株式会社', 'HANAJIRUSHI | Japanese Skincare from Ginza, Tokyo' );
	}
	if ( is_post_type_archive( 'product' ) ) {
		$title = hj_t( '製品', 'Products' );
	} elseif ( is_page() && isset( hj_pages()[ get_post_field( 'post_name', get_queried_object_id() ) ] ) ) {
		$pg = hj_pages()[ get_post_field( 'post_name', get_queried_object_id() ) ];
		if ( 'cosmoprof-asia' === get_post_field( 'post_name', get_queried_object_id() ) ) {
			return hj_t( $pg[0], $pg[1] ) . hj_t( '｜花印 HANAJIRUSHI', ' | HANAJIRUSHI' );
		}
		$title = hj_t( $pg[0], $pg[1] );
	} elseif ( is_home() ) {
		$title = hj_t( 'お知らせ', 'News' );
	} elseif ( is_category() ) {
		$title = hj_term_name( get_queried_object() ) . hj_t( '｜お知らせ', ' | News' );
	} elseif ( is_year() ) {
		$title = get_query_var( 'year' ) . hj_t( '年｜お知らせ', ' | News' );
	} elseif ( is_singular() ) {
		$title = hj_title( get_queried_object() );
	} elseif ( is_404() ) {
		$title = hj_t( 'ページが見つかりません', 'Page not found' );
	} else {
		$title = wp_strip_all_tags( get_the_archive_title() );
	}
	return $title . hj_t( '｜', ' | ' ) . $site;
} );

// Meta description: the product's one-line text on product pages, else the page's own.
add_action( 'wp_head', function () {
	$d = hj_t( '花印（HANAJIRUSHI）の公式サイト。東京・銀座の自社研究室で開発する日本製スキンケア。クレンジング、ハトムギ化粧水、美容液、クリーム、UV化粧下地など。',
		'HANAJIRUSHI: Japanese skincare formulated in our own laboratory in Ginza, Tokyo — cleansing, Hatomugi lotion, serums, creams and UV primer.' );
	if ( is_singular( 'product' ) ) {
		$id = get_queried_object_id();
		$d  = hj_title( $id ) . hj_t( '（', ' (' ) . hj_raw( 'size', $id ) . hj_t( '）｜', ') — ' ) . hj_get( 'short', $id );
	} elseif ( is_page() && isset( hj_pages()[ get_post_field( 'post_name', get_queried_object_id() ) ] ) ) {
		$pg = hj_pages()[ get_post_field( 'post_name', get_queried_object_id() ) ];
		$d  = hj_t( $pg[2], $pg[3] ) ?: $d;
	} elseif ( is_home() ) {
		$d = hj_pages()['news'][ hj_is_en() ? 3 : 2 ];
	} elseif ( is_post_type_archive( 'product' ) ) {
		$d = hj_t( '花印の製品一覧。クレンジング、化粧水・美容液、クリーム・ジェル、マスク・パック、UV化粧下地、メンズ。日本製のスキンケア。',
			"HANAJIRUSHI products: cleansing, lotions and serums, creams and gels, masks, UV primer and men's care. Made in Japan." );
	}
	printf( '<meta name="description" content="%s">' . "\n", esc_attr( $d ) );
}, 1 );

// The design's page classes (pg-home, pg-products, pg-product …).
add_filter( 'body_class', function ( $classes ) {
	$classes[] = 'pg-' . hj_page_key();
	return $classes;
} );
