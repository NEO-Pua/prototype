<?php
/**
 * Japanese / English without a language plugin.
 *
 * Japanese is the site's own language at /…; English is the same address under /en/….
 * One post holds both languages (English fields sit on an "English" tab), so a product,
 * slide or news item is edited once and the two addresses always match.
 *
 * How the /en/ prefix works: before WordPress reads the address, the prefix is noted and
 * removed, so every normal WordPress address (pages, products, news, archives) also works
 * under /en/. After that, every link WordPress builds through home_url() gets /en/ back
 * while an English page is being shown, so menus, permalinks and archive links stay in
 * English without any extra work in the theme.
 */

defined( 'ABSPATH' ) || exit;

/** Path of the site root ('' or '/sub'), without a trailing slash. */
function hj_home_path(): string {
	return rtrim( (string) wp_parse_url( get_option( 'home' ), PHP_URL_PATH ), '/' );
}

/** Notes the language of this request and strips /en from the address WordPress parses. */
function hj_detect_lang(): void {
	$GLOBALS['hj_lang'] = 'ja';
	if ( is_admin() || wp_doing_cron() || ( defined( 'WP_CLI' ) && WP_CLI ) || empty( $_SERVER['REQUEST_URI'] ) ) {
		return;
	}
	$uri    = $_SERVER['REQUEST_URI'];
	$prefix = hj_home_path() . '/en';
	if ( $uri === $prefix || str_starts_with( $uri, $prefix . '/' ) || str_starts_with( $uri, $prefix . '?' ) ) {
		$GLOBALS['hj_lang']     = 'en';
		$GLOBALS['hj_orig_uri'] = $uri;
		$rest                   = substr( $uri, strlen( $prefix ) );
		$_SERVER['REQUEST_URI'] = hj_home_path() . ( '' === $rest || '?' === $rest[0] ? '/' . $rest : $rest );
	}
}

/** 'ja' or 'en'. */
function hj_lang(): string {
	return $GLOBALS['hj_lang'] ?? 'ja';
}

function hj_is_en(): bool {
	return 'en' === hj_lang();
}

/** The Japanese or the English text, for the language being shown. */
function hj_t( $ja, $en ) {
	return hj_is_en() ? $en : $ja;
}

/** Inserts /en after the site root in a URL of this site (no change if it is already there). */
function hj_url_en( string $url ): string {
	$home = untrailingslashit( get_option( 'home' ) );
	$home = set_url_scheme( $home, wp_parse_url( $url, PHP_URL_SCHEME ) ?: null );
	if ( ! str_starts_with( $url, $home ) ) {
		return $url;
	}
	$rest = substr( $url, strlen( $home ) );
	if ( '/en' === $rest || str_starts_with( $rest, '/en/' ) || str_starts_with( $rest, '/en?' ) ) {
		return $url;
	}
	return $home . '/en' . ( '' === $rest ? '/' : $rest );
}

/** The address of the page being shown, in the given language. */
function hj_switch_url( string $lang ): string {
	$base = hj_home_path();
	$uri  = $_SERVER['REQUEST_URI'] ?? '/';
	if ( hj_is_en() ) {
		$rest = substr( $uri, strlen( $base . '/en' ) );
		$uri  = $base . ( '' === $rest || '?' === $rest[0] ? '/' . $rest : $rest );
	}
	if ( 'en' === $lang ) {
		$uri = $base . '/en' . substr( $uri, strlen( $base ) );
	}
	$origin = wp_parse_url( get_option( 'home' ) );
	$host   = ( is_ssl() ? 'https' : ( $origin['scheme'] ?? 'http' ) ) . '://' . ( $origin['host'] ?? '' ) . ( isset( $origin['port'] ) ? ':' . $origin['port'] : '' );
	return $host . $uri;
}

// After WordPress has read the address: give the original back (canonical redirects compare
// against it) and from now on build English links.
add_action( 'parse_request', function () {
	if ( isset( $GLOBALS['hj_orig_uri'] ) ) {
		$_SERVER['REQUEST_URI'] = $GLOBALS['hj_orig_uri'];
	}
	if ( hj_is_en() ) {
		add_filter( 'home_url', fn( $url ) => hj_url_en( $url ), 20 );
	}
}, 1 );

// <html lang="en"> and English WordPress strings on English pages.
add_filter( 'language_attributes', function ( $out ) {
	return hj_is_en() ? preg_replace( '/lang="[^"]*"/', 'lang="en"', $out ) : $out;
} );
add_filter( 'locale', function ( $locale ) {
	return ( hj_is_en() && ! is_admin() ) ? 'en_US' : $locale;
} );

// Search engines: the two language versions of each page point at each other.
add_action( 'wp_head', function () {
	if ( is_404() || is_search() ) {
		return;
	}
	printf( "<link rel=\"alternate\" hreflang=\"ja\" href=\"%s\">\n", esc_url( hj_switch_url( 'ja' ) ) );
	printf( "<link rel=\"alternate\" hreflang=\"en\" href=\"%s\">\n", esc_url( hj_switch_url( 'en' ) ) );
	printf( "<link rel=\"alternate\" hreflang=\"x-default\" href=\"%s\">\n", esc_url( hj_switch_url( 'ja' ) ) );
}, 2 );
