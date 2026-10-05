<?php
/**
 * 展示会情報 /exhibition/ (mockup: exh_list()): upcoming exhibitions with their buyer pages,
 * then past ones. Each exhibition is a 展示会 post; it moves to "past" after its last day.
 */

defined( 'ABSPATH' ) || exit;

get_header();

echo hj_phero( 'Exhibition', '展示会情報', 'Exhibitions',
	hj_t( '出展予定の展示会と、これまでの出展。', 'Where to meet us: upcoming and past exhibitions.' ), '', '出展', array(),
	array( 'anchors' => array( array( 'upcoming', hj_t( '開催予定', 'Upcoming' ) ), array( 'past', hj_t( '過去の出展', 'Past exhibitions' ) ) ) ) );

/** One exhibition row (mockup: the exl article). */
$row = function ( WP_Post $e, bool $upcoming ): string {
	$page = (string) hj_raw( 'page', $e->ID );
	$dl   = '';
	foreach ( array( array( 'booth', 'ブース', 'Booth' ), array( 'onshow', '出展内容', 'On show' ), array( 'languages', '対応言語', 'Languages' ) ) as $f ) {
		$v = hj_ex( $e, $f[0] );
		if ( '' !== trim( wp_strip_all_tags( $v ) ) || str_contains( $v, 'tbd' ) ) {
			$dl .= '<div><dt>' . hj_t( $f[1], $f[2] ) . '</dt><dd>' . $v . '</dd></div>';
		}
	}
	$status = hj_ex( $e, 'status' );
	$dates  = hj_ex( $e, 'dates' );
	$acts   = ( $upcoming && $page ) ? '<div class="exl__a">' . hj_btn( hj_link( $page ), '展示会専用ページへ', 'Open the event page', 'btn--fill' ) . hj_lnk( hj_link( $page ) . '#booking', '商談を予約する', 'Book a meeting' ) . '</div>' : '';
	return '<article class="exl rv">
<p class="exl__d"><b>' . esc_html( (string) hj_raw( 'year', $e->ID ) ) . '</b><span>' . hj_ex( $e, 'month' ) . '</span>' . ( $upcoming && str_contains( $dates, 'tbd' ) ? preg_replace( '/^.*?(<span class="tbd">.*?<\/span>).*$/s', '$1', $dates ) : '' ) . '</p>
<div class="exl__b">' . ( $upcoming && $status ? '<p class="exl__st">' . $status . '</p>' : '' ) . '<h3>' . esc_html( hj_title( $e ) ) . '</h3><p class="exl__v">' . hj_ex( $e, 'venue' ) . '</p>
<dl class="dl">' . $dl . '</dl></div>' . $acts . '
</article>';
};

$up   = implode( '', array_map( fn( $e ) => $row( $e, true ), hj_exhibitions( 'upcoming' ) ) );
$past = implode( '', array_map( fn( $e ) => $row( $e, false ), hj_exhibitions( 'past' ) ) );
?>
<section class="sec sec--t" id="upcoming"><div class="wrap">
<?php echo hj_shd( '01', 'Upcoming', '開催予定の展示会', 'Upcoming exhibitions', '開催予定', hj_t( '会期中の商談は、各展示会の専用ページからご予約いただけます。', 'Meetings during a show are booked on that show\'s own page.' ) ); ?>
<?php if ( $up ) : ?>
<div class="exl__l"><?php echo $up; ?></div>
<?php else : ?>
<p class="exl__none rv"><?php echo hj_t( '現在、出展予定の展示会はありません。', 'No exhibitions are scheduled at the moment.' ); ?></p>
<?php endif; ?>
</div></section>
<section class="sec sec--t blush" id="past"><div class="wrap">
<?php echo hj_shd( '02', 'Past exhibitions', '過去の出展', 'Past exhibitions', '出展実績' ); ?>
<?php if ( $past ) : ?>
<div class="exl__l"><?php echo $past; ?></div>
<?php else : ?>
<p class="exl__none rv"><?php echo hj_t( '過去の出展実績は、確認のうえ掲載します。', 'Past exhibitions will be listed once confirmed.' ) . ' ' . hj_tbd(); ?></p>
<?php endif; ?>
</div></section>
<?php
get_footer();
