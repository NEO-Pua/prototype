<?php
/**
 * Home first view: the slider of トップスライド posts (mockup: hero13()).
 * Each slide is fields only; the layout, motion and phone behaviour come from the design.
 */

defined( 'ABSPATH' ) || exit;

$slides = hj_slides();
if ( ! $slides ) {
	return;
}
$n    = count( $slides );
$out  = '';
$tabs = '';
foreach ( $slides as $i => $s ) {
	$id     = $s->ID;
	$on     = 0 === $i;
	$visual = (string) ( hj_raw( 'visual', $id ) ?: 'none' );
	$kind   = array( 'none' => 'brand', 'kanji' => 'exh', 'products' => 'new', 'product' => 'patent' )[ $visual ] ?? 'brand';
	$bg_id  = (int) hj_raw( 'bg', $id );
	$bg     = $bg_id
		? '<div class="hs13__bg" aria-hidden="true"><img src="' . esc_url( (string) wp_get_attachment_image_url( $bg_id, 'full' ) ) . '" alt="" style="object-position:' . esc_attr( (string) ( hj_raw( 'bg_pos', $id ) ?: 'center' ) ) . '"></div>'
		: '<div class="hs13__bg hs13__bg--plain" aria-hidden="true"></div>';
	$label  = (string) hj_get( 'label', $id );
	$k      = $label ? '<p class="hs__k">' . esc_html( $label ) . '</p>' : hj_eb( esc_html( (string) hj_raw( 'eyebrow', $id ) ) );
	$tag    = $on ? 'h1' : 'h2';
	$ctas   = '';
	if ( hj_get( 'btn1', $id ) ) {
		$ctas .= '<a class="btn btn--fill" href="' . esc_url( hj_link( hj_raw( 'btn1_link', $id ) ) ) . '"><span>' . esc_html( hj_get( 'btn1', $id ) ) . '</span>' . HJ_ARR . '</a>';
	}
	if ( hj_get( 'btn2', $id ) ) {
		$ctas .= '<a class="lnk" href="' . esc_url( hj_link( hj_raw( 'btn2_link', $id ) ) ) . '"><span>' . esc_html( hj_get( 'btn2', $id ) ) . '</span>' . HJ_ARR . '</a>';
	}

	$vis = '';
	if ( 'kanji' === $visual ) {
		$vis = '<figure class="win win--xl win--kj"><div class="win__c"><span class="win__kj">' . esc_html( (string) hj_raw( 'kanji', $id ) ) . '</span><small>' . esc_html( (string) hj_raw( 'kanji_caption', $id ) ) . '</small></div></figure>';
	} elseif ( 'product' === $visual && ( $p = get_post( (int) hj_raw( 'product', $id ) ) ) ) {
		$vis = hj_win( hj_product_photo( $p->ID ), hj_title( $p ), 'win--xl' );
	} elseif ( 'products' === $visual ) {
		$vis = '<ul class="hs13__panels">';
		foreach ( (array) hj_raw( 'products', $id ) as $pid ) {
			if ( $p = get_post( (int) $pid ) ) {
				$vis .= '<li>' . hj_pimg( $p ) . '<p>' . esc_html( hj_title( $p ) ) . '<small>' . esc_html( (string) hj_raw( 'size', $p->ID ) ) . '</small></p></li>';
			}
		}
		$vis .= '</ul>';
	}
	if ( $vis && hj_raw( 'seal', $id ) ) {
		$vis .= hj_seal( esc_html( (string) hj_raw( 'seal', $id ) ), 'seal--l seal--txt' );
	}
	$vis = $vis ? '<div class="hs13__vis">' . $vis . '</div>' : '';

	$out .= '
<div class="hs__s hs13 hs13--' . $kind . ( $on ? ' is-on' : '' ) . '" role="group" aria-roledescription="slide" aria-label="' . ( $i + 1 ) . ' / ' . $n . '"' . ( $on ? '' : ' aria-hidden="true"' ) . '>' . $bg . '
<div class="wrap hs13__in"><div class="hs__txt">' . $k . '<' . $tag . ' class="hs__h">' . hj_heading( hj_get( 'heading', $id ), (bool) hj_get( 'accent', $id ) ) . '</' . $tag . '>
<p class="hero__lead">' . hj_text( hj_get( 'text', $id ) ) . '</p><div class="hero__ctas">' . $ctas . '</div></div>' . $vis . '</div></div>';

	$tab   = hj_is_en() ? hj_title( $s ) : ( (string) hj_raw( 'tab', $id ) ?: get_the_title( $s ) );
	$tabs .= '<li><button type="button" data-go="' . $i . '"' . ( $on ? ' aria-current="true"' : '' ) . '><span>' . esc_html( $tab ) . '</span><i></i></button></li>';
}
?>
<section class="hero hero--slides hero13" data-first aria-roledescription="carousel" aria-label="<?php echo esc_attr( hj_t( 'メインビジュアル', 'Highlights' ) ); ?>">
<div class="hs"><div class="hs__track"><?php echo $out; ?></div></div>
<div class="hs__ui"><p class="hs__n"><b>01</b><span>/ <?php echo sprintf( '%02d', $n ); ?></span></p>
<ol class="hs__tabs"><?php echo $tabs; ?></ol>
<div class="hs__btns"><button type="button" class="hs__play" aria-label="<?php echo esc_attr( hj_t( '一時停止', 'Pause' ) ); ?>" data-pause="<?php echo esc_attr( hj_t( '一時停止', 'Pause' ) ); ?>" data-play="<?php echo esc_attr( hj_t( '再生', 'Play' ) ); ?>"><i></i></button></div></div>
</section>
