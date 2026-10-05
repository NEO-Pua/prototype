<?php
/**
 * Product pieces: photo panel, card, names (the mockup's pimg(), pcard(), pcname(), pname()).
 */

defined( 'ABSPATH' ) || exit;

/** Product photo in a square panel. */
function hj_pimg( WP_Post $p, string $cls = '' ): string {
	$src = hj_product_photo( $p->ID );
	if ( ! $src ) {
		return '<figure class="ppan ppan--soon ' . $cls . '"><span>' . hj_seal() . '<small>' . hj_t( '近日公開', 'Coming soon' ) . '</small></span></figure>';
	}
	$ext = has_post_thumbnail( $p ) ? '' : ' data-src="rakuten"';   // temporary store image: contained on white (premium-v13.css)
	return '<figure class="ppan ' . $cls . '"' . $ext . '><img src="' . esc_url( $src ) . '" alt="' . esc_attr( hj_title( $p ) ) . '" loading="lazy"></figure>';
}

/** Long Japanese product names wrap between words, not mid-word. */
const HJ_NAME_WORDS = array( 'クレンジング', 'ジューシー', 'ハトムギ', '豊潤', 'ブースター', 'モイスチュア', 'フェイス', '薬用', 'リンクル', 'スーパー', 'トーンアップ', 'UV', 'クレー' );

/** Card name: 花印 on its own small line; the rest may wrap only between words. */
function hj_pcname( string $name ): string {
	$name = esc_html( $name );
	if ( ! str_starts_with( $name, '花印' ) ) {
		return $name;
	}
	$rest = trim( mb_substr( $name, 2 ) );
	foreach ( HJ_NAME_WORDS as $w ) {
		$rest = str_replace( $w, $w . '<wbr>', $rest );
	}
	if ( str_ends_with( $rest, '<wbr>' ) ) {
		$rest = substr( $rest, 0, -5 );
	}
	return '<small class="pcard__b">花印</small>' . $rest;
}

/** Page title name: a break opportunity after 花印 and before フェイスマスク. */
function hj_pname( string $name ): string {
	$name = esc_html( $name );
	$name = preg_replace( '/^花印/u', '花印<wbr>', $name );
	return str_replace( 'フェイスマスク', '<wbr>フェイスマスク', $name );
}

/** Category label, and "category · series" for the small line above names. */
function hj_product_cat( WP_Post $p ): string {
	return hj_label( HJ_CATS, hj_raw( 'category', $p->ID ) );
}

function hj_product_series( WP_Post $p ): string {
	return hj_label( HJ_SERIES, hj_raw( 'series', $p->ID ) );
}

/** One product card (products list, home, "more products"). $i is its number in the list. */
function hj_pcard( WP_Post $p, int $i ): string {
	$soon = (bool) hj_raw( 'coming_soon', $p->ID );
	$ser  = hj_product_series( $p );
	$flag = hj_raw( 'is_new', $p->ID ) ? '<span class="pcard__new">' . hj_t( '新商品', 'New' ) . '</span>'
		: ( $soon ? '<span class="pcard__new pcard__new--soon">' . hj_t( '近日公開', 'Coming soon' ) . '</span>' : '' );
	$body = hj_pimg( $p )
		. '<p class="pcard__no">No.' . sprintf( '%02d', $i ) . '<span>' . esc_html( hj_product_cat( $p ) ) . ( $ser ? '<i> · ' . esc_html( $ser ) . '</i>' : '' ) . '</span>' . $flag . '</p>'
		. '<h3 class="pcard__n">' . hj_pcname( hj_title( $p ) ) . '</h3><p class="pcard__d">' . esc_html( hj_get( 'short', $p->ID ) ) . '</p>';
	$cat  = esc_attr( (string) hj_raw( 'category', $p->ID ) );
	if ( $soon ) {
		return '<li class="pcard pcard--soon rv" data-cat="' . $cat . '" id="' . esc_attr( $p->post_name ) . '"><div>' . $body . '</div></li>';
	}
	return '<li class="pcard rv" data-cat="' . $cat . '"><a href="' . esc_url( get_permalink( $p ) ) . '">' . $body . '<span class="pcard__go" aria-hidden="true">' . HJ_ARR . '</span></a></li>';
}

/** Products shown on the home page, in display order. */
function hj_home_products(): array {
	return hj_products( array( 'meta_query' => array_merge( array( array( 'key' => 'show_on_home', 'value' => '1' ) ), function_exists( 'hj_lang_meta_query' ) ? hj_lang_meta_query() : array() ) ) );
}
