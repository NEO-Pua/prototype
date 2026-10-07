<?php
/**
 * Site header and phone menu (mockup: header()).
 */

defined( 'ABSPATH' ) || exit;

$current = hj_nav_current();
$nav     = '';
$mlist   = '';
$pages   = array_merge( hj_nav(), array( array( 'contact', '/contact/', 'お問い合わせ', 'Contact', array() ) ) );
foreach ( hj_nav() as $item ) {
	[ $key, $path, $ja, $en ] = $item;
	$nav .= '<li><a href="' . esc_url( hj_link( $path ) ) . '"' . ( $key === $current ? ' aria-current="' . ( hj_page_key() === $key ? 'page' : 'true' ) . '"' : '' ) . '>' . hj_t( $ja, $en ) . '</a></li>';
}
$nav .= '<li class="hd__ev"><a href="' . esc_url( hj_link( '/cosmoprof-asia/' ) ) . '">Cosmoprof Asia</a></li>';
foreach ( $pages as $i => $item ) {
	[ $key, $path, $ja, $en, $kids ] = $item;
	$sub = '';
	if ( $kids ) {
		$sub = '<ul class="menu__sub">';
		foreach ( $kids as $kid ) {
			$sub .= '<li><a href="' . esc_url( hj_link( $kid[0] ) ) . '">' . hj_t( $kid[1], $kid[2] ) . '</a></li>';
		}
		$sub .= '</ul>';
	}
	$mlist .= '<li><a href="' . esc_url( hj_link( $path ) ) . '"' . ( hj_page_key() === $key ? ' aria-current="page"' : '' ) . '><i>' . sprintf( '%02d', $i ) . '</i><b>' . hj_t( $ja, $en ) . '</b>' . ( hj_is_en() ? '' : '<small>' . $en . '</small>' ) . '</a>' . $sub . '</li>';
}
$lng = '<span class="lng" role="group" aria-label="Language"><a href="' . esc_url( hj_switch_url( 'ja' ) ) . '" class="' . ( hj_is_en() ? '' : 'on' ) . '" lang="ja">JA</a><a href="' . esc_url( hj_switch_url( 'en' ) ) . '" class="' . ( hj_is_en() ? 'on' : '' ) . '" lang="en">EN</a></span>';
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip" href="#main"><?php echo hj_t( '本文へスキップ', 'Skip to content' ); ?></a>
<header class="hd" data-hd>
<div class="hd__in">
<a class="hd__logo" href="<?php echo esc_url( hj_link( '/' ) ); ?>"><img src="<?php echo esc_url( hj_img( 'logo_v15.svg' ) ); ?>" alt="花印 HANAJIRUSHI" width="132" height="35"></a>
<nav class="hd__nav" aria-label="<?php echo esc_attr( hj_t( 'メインメニュー', 'Main menu' ) ); ?>"><ul><?php echo $nav; ?></ul></nav>
<div class="hd__r"><?php echo $lng; ?>
<a class="hd__cta" href="<?php echo esc_url( hj_link( '/contact/' ) ); ?>"><?php echo hj_t( 'お問い合わせ', 'Contact' ); ?></a>
<button class="hd__menu" type="button" aria-expanded="false" aria-controls="menu"><span class="bars"><i></i><i></i></span><span class="m">Menu</span><span class="c">Close</span></button>
</div></div>
</header>
<div class="menu" id="menu" aria-hidden="true"><div class="menu__in">
<ul class="menu__l"><?php echo $mlist; ?></ul>
<div class="menu__side">
<p class="menu__tel"><a href="<?php echo esc_attr( hj_tel_href() ); ?>"><?php echo esc_html( hj_tel() ); ?></a><small><?php echo esc_html( hj_hours() ); ?></small></p>
<?php echo hj_menu_exh(); ?>
</div>
</div></div>
<main id="main">
