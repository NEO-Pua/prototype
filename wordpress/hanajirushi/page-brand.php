<?php
/**
 * ブランド /brand/ (mockup: p_brand13()): philosophy, brand story (text from the client to
 * come), research, IP collaborations, online stores.
 */

defined( 'ABSPATH' ) || exit;

get_header();

echo hj_phero( 'Brand', 'ブランド', 'Brand',
	hj_t( '人の肌を想い、ひとりの悩みを見つめる、日本製のスキンケア。', 'Gentle, honest skincare — formulated and made in Japan.' ),
	hj_img( 'h_brand_top_p.jpg' ), '花印', array(),
	array( 'anchors' => array( array( 'philosophy', hj_t( 'ブランド理念', 'Philosophy' ) ), array( 'story', hj_t( 'ブランドストーリー', 'Our story' ) ), array( 'research', hj_t( '研究への取り組み', 'Research' ) ),
		array( 'collab', hj_t( 'IPコラボレーション', 'Collaborations' ) ), array( '/products/', hj_t( '製品一覧', 'All products' ) ) ) ) );

// ------------------------------------------------------------------ 01 philosophy (mockup: brand_phil())
$slogan = hj_is_en()
	? '<h2 class="phil__h">' . hj_lines( 'Clean formula.<br><em>Gentle by design.</em><br>Made in Japan.' ) . '</h2><p class="phil__jp" aria-hidden="true">ひとりに、ひとつの、キレイを咲かせる。</p>'
	: '<h2 class="phil__tate">' . hj_lines( 'ひとりに、ひとつの、<br>キレイを咲かせる。' ) . '</h2>';
$rings = '';
foreach ( hj_free_from() as $f ) {
	$rings .= '<li><span>' . $f[0] . '</span><small>' . $f[1] . '</small></li>';
}
?>
<section class="sec phil" id="philosophy"><div class="wrap phil__g">
<div class="phil__s rv"><?php echo hj_eb( 'Philosophy', '01' ) . $slogan; ?></div>
<div class="phil__txt rv"><p class="phil__lead"><?php echo hj_t( '人の肌を想い、ひとりの悩みを見つめ、ひとつしかないキレイを、メイド・イン・ジャパンのスキンケアの力で届けていく。', 'We look closely at each person\'s skin and each individual concern, and deliver a beauty that is theirs alone — with the power of Japanese-made skincare.' ); ?></p>
<p><?php echo hj_t( '「花印」の名には、ひとりひとりの肌に咲く花の印という想いを込めています。日本ならではの上質で誠実なものづくりが認められ、花印は国内はもとより世界12ヵ国で販売されています。', 'The name HANAJIRUSHI, “flower seal”, stands for the mark of a flower blooming on each person\'s skin. Recognised for the quality and honesty of Japanese manufacturing, our products are sold in Japan and 12 countries worldwide.' ); ?></p>
<div class="name"><?php echo hj_seal( '花印', 'seal--l' ); ?><p><b><?php echo hj_t( '花印 — 肌に咲く、花の印。', 'Hana-jirushi — “flower seal”.' ); ?></b><?php echo hj_t( 'ひとりひとりの肌に咲く花の印という想いを、名前に込めています。', 'The mark of a flower blooming on each person\'s skin.' ); ?></p></div></div>
<div class="phil__img rv"><div class="arch"><img src="<?php echo esc_url( hj_img( 'h_brand_top_p.jpg' ) ); ?>" alt="" loading="lazy" style="object-position:0% center"></div></div>
</div>
<div class="wrap"><ul class="rings rv"><?php echo $rings; ?></ul></div>
</section>
<?php
// ------------------------------------------------------------------ 02 story: the page's own text once the client sends it
$story = trim( (string) get_post_field( 'post_content', get_queried_object_id() ) );
if ( $story && ! hj_is_en() ) :
	?>
<section class="sec sec--t blush" id="story"><div class="wrap">
	<?php echo hj_shd( '02', 'Our story', 'ブランドストーリー', 'Our story', 'ブランドストーリー', null, 'shd--c' ); ?>
<div class="entry entry--story rv"><?php echo apply_filters( 'the_content', $story ); ?></div></div></section>
	<?php
else :
	$slots = array(
		array( hj_t( 'ブランドの背景', 'Background' ), hj_t( '花印が生まれた背景と、名前に込めた想い。', 'How Hanajirushi began, and what the name stands for.' ) ),
		array( hj_t( '大切にしていること', 'What we value' ), hj_t( '肌へのやさしさと、日本ならではのものづくり。', 'Gentleness, and Japanese craftsmanship.' ) ),
		array( hj_t( '花印の魅力', 'What sets us apart' ), hj_t( '製品づくりへのこだわりと、お客様に選ばれている理由。', 'How we make our products, and why customers choose them.' ) ),
	);
	$li = '';
	foreach ( $slots as $i => $sl ) {
		$li .= '<li class="rv"><span class="story13__n">' . sprintf( '%02d', $i + 1 ) . '</span><h3>' . $sl[0] . '</h3><p>' . $sl[1] . '</p>' . hj_tbd( '原稿受領後に掲載', 'Text to come' ) . '</li>';
	}
	?>
<section class="sec sec--t blush" id="story"><div class="wrap">
	<?php echo hj_shd( '02', 'Our story', 'ブランドストーリー', 'Our story', 'ブランドストーリー', hj_t( 'ブランドの背景や魅力をお伝えする本文は、ご提供いただく原稿を掲載します。', 'The full brand story will be added from the text being supplied.' ), 'shd--c' ); ?>
<ol class="story13"><?php echo $li; ?></ol></div></section>
	<?php
endif;
?>
<section class="sec" id="research"><div class="wrap split__g">
<div class="split__img split__img--win rv"><?php echo hj_win( hj_img( 'h_campany_lab.jpg' ), hj_t( '銀座本社の研究室', 'Our laboratory in Ginza' ), 'win--m' ); ?></div>
<div class="split__txt rv"><?php echo hj_shd( '03', 'Research', '銀座の研究室から、<br>確かな処方を。', 'Reliable formulas<br><em>from our Ginza lab.</em>', '研究への取り組み' ); ?>
<p class="pd__cp"><?php echo hj_c( 'RD_CATCH' ); ?></p><p><?php echo hj_c( 'RD_P1' ); ?></p>
<div class="ctas"><?php echo hj_btn( hj_link( '/rd/' ), '研究開発・品質管理', 'R&amp;D and quality' ) . hj_lnk( hj_link( '/products/' ), '製品一覧', 'All products' ); ?></div></div></div></section>
<?php
echo hj_brand_collab( '04', 'collab' );
get_template_part( 'template-parts/stores' );
get_footer();
