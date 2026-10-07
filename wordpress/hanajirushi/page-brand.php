<?php
/**
 * ブランド /brand/ (mockup: p_brand14()): the client's text (ブランドページ文字案, 2026-10-07) —
 * header lead, brand concept, OUR VALUES (five values, in place of the free-from circles),
 * brand story, research, online stores. The values and the story come from the mockup through
 * inc/copy.json (VALUES14, STORY14). The IP collaborations block is on the products page now.
 */

defined( 'ABSPATH' ) || exit;

get_header();

echo hj_phero( 'Brand', 'ブランド', 'Brand',
	hj_t( '一人ひとりの肌に寄り添い、その人らしい美しさを育む。<br>花印は、毎日のスキンケアを通じて、一人ひとりが自分らしい美しさを楽しめる毎日を届けるブランドです。',
		'Close to every skin, nurturing a beauty that is truly one\'s own. Through everyday skincare, Hanajirushi helps each person enjoy a beauty of their own, every day.' ),
	hj_img( 'h_brand_top_p.jpg' ), '花印', array(),
	array( 'anchors' => array( array( 'concept', hj_t( 'ブランドコンセプト', 'Concept' ) ), array( 'values', hj_t( '5つの価値観', 'Our values' ) ), array( 'story', hj_t( 'ブランドストーリー', 'Our story' ) ),
		array( 'research', hj_t( '研究への取り組み', 'Research' ) ), array( '/products/', hj_t( '製品一覧', 'All products' ) ) ) ) );

// ------------------------------------------------------------------ 01 brand concept
// EN_ONLY: the English slogan is re-written, not translated; the Japanese line stays as an accent.
$slogan = hj_is_en()
	? '<h2 class="phil__h">' . hj_lines( 'Clean formula.<br><em>Gentle by design.</em><br>Made in Japan.' ) . '</h2><p class="phil__jp" aria-hidden="true">ひとりに、ひとつの、キレイを咲かせる。</p>'
	: '<h2 class="phil__tate">' . hj_lines( 'ひとりに、ひとつの、<br>キレイを咲かせる。' ) . '</h2>';
?>
<section class="sec phil" id="concept"><div class="wrap phil__g">
<div class="phil__s rv"><?php echo hj_eb( 'Brand concept', '01' ) . $slogan; ?></div>
<div class="phil__txt rv"><p class="phil__lead"><?php echo hj_t( '美しさのかたちは、人それぞれ。', 'Beauty takes as many forms as there are people.' ); ?></p>
<p><?php echo hj_t( '肌質も、年齢も、ライフスタイルも、理想とする美しさも、一人ひとり違います。だから花印は、誰かの美しさをそのまま当てはめるのではなく、一人ひとりの肌と向き合い、その人に合った美しさを育むことを大切にしています。',
	'Skin type, age, lifestyle, the beauty you hope for — no two people are alike. So rather than fitting anyone to someone else\'s idea of beauty, Hanajirushi starts from each person\'s skin and helps the beauty that suits them grow.' ); ?></p>
<p><?php echo hj_t( '毎日使うものだからこそ、品質にこだわり、使いやすく、無理なく続けられること。特別な日のためだけではなく、何気ない毎日の中で、自分の肌を大切にする時間を届けること。それが、花印が考えるスキンケアです。',
	'Because it is something you use every day, it should be well made, easy to use and easy to keep up — not only for special days, but as everyday time to look after your skin. That is what skincare means to Hanajirushi.' ); ?></p></div>
<div class="phil__img rv"><div class="arch"><img src="<?php echo esc_url( hj_img( 'h_brand_top_p.jpg' ) ); ?>" alt="" loading="lazy" style="object-position:0% center"></div></div>
</div></section>
<?php
// ------------------------------------------------------------------ 02 our values, 03 brand story
$vals = '';
foreach ( hj_c( 'VALUES14' ) as $i => $v ) {
	$vals .= '<li class="rv"><span class="vals__n">' . sprintf( '%02d', $i + 1 ) . '</span><span class="vals__w">' . $v[0] . '</span><h3>' . $v[1] . '</h3><p>' . $v[2] . '</p></li>';
}
$story = '';
foreach ( hj_c( 'STORY14' ) as $i => $st ) {
	$story .= '<li class="rv"><span class="story13__n">' . sprintf( '%02d', $i + 1 ) . '</span><p class="story13__k">' . $st[0] . '</p><h3>' . $st[1] . '</h3><p>' . $st[2] . '</p></li>';
}
?>
<section class="sec sec--t vals-sec" id="values"><div class="wrap">
<?php echo hj_shd( '02', 'Our values', '花印が大切にする、<br>5つの価値観。', 'Five values<br><em>we hold to</em>', '5つの価値観', null, 'shd--c' ); ?>
<ol class="vals"><?php echo $vals; ?></ol></div></section>
<section class="sec sec--t blush" id="story"><div class="wrap">
<?php echo hj_shd( '03', 'Brand story', '美しさは、<br>一人ひとり違う。', 'Every beauty<br><em>is different.</em>', 'ブランドストーリー',
	hj_t( 'だからこそ、私たちは一人ひとりの肌と向き合い、その人らしい美しさを育むスキンケアを届けたい。それが、花印のものづくりの原点です。',
		'That is why we want to offer skincare that meets each person\'s skin and nurtures a beauty of their own — the starting point of everything Hanajirushi makes.' ), 'shd--c' ); ?>
<ol class="story13 story13--full"><?php echo $story; ?></ol></div></section>
<section class="sec" id="research"><div class="wrap split__g">
<div class="split__img split__img--win rv"><?php echo hj_win( hj_img( 'h_campany_lab.jpg' ), hj_t( '銀座本社の研究室', 'Our laboratory in Ginza' ), 'win--m' ); ?></div>
<div class="split__txt rv"><?php echo hj_shd( '04', 'Research', '銀座の研究室から、<br>確かな処方を。', 'Reliable formulas<br><em>from our Ginza lab.</em>', '研究への取り組み' ); ?>
<p class="pd__cp"><?php echo hj_c( 'RD_CATCH' ); ?></p><p><?php echo hj_c( 'RD_P1' ); ?></p>
<div class="ctas"><?php echo hj_btn( hj_link( '/rd/' ), '研究開発・品質管理', 'R&amp;D and quality' ) . hj_lnk( hj_link( '/products/' ), '製品一覧', 'All products' ); ?></div></div></div></section>
<?php
get_template_part( 'template-parts/stores' );
get_footer();
