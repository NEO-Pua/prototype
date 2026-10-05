<?php
/**
 * IPコラボレーション /collaboration/ (mockup: p_collaboration()): about, portfolio (IPコラボ
 * posts), value for partners.
 */

defined( 'ABSPATH' ) || exit;

get_header();

echo hj_phero( 'Collaboration', 'IP<br>コラボレーション', 'Licensed IP Collaborations',
	hj_t( '日本の人気IPとの正規ライセンス商品。', 'Officially licensed products with leading Japanese IP.' ), '', '協創',
	array( array( hj_link( '/brand/' ), hj_t( 'ブランド', 'Brand' ) ) ),
	array( 'anchors' => array( array( 'about', hj_t( 'コラボレーションについて', 'About' ) ), array( 'works', hj_t( 'コラボレーション実績', 'Portfolio' ) ), array( 'value', hj_t( 'パートナー様へのメリット', 'Value for partners' ) ) ) ) );

$values = array_map( fn( $v ) => array( $v[0], $v[1] ), hj_c( 'COLLAB_VALUES' ) );
?>
<section class="sec" id="about"><div class="wrap about__g">
<div class="rv"><?php echo hj_shd( '01', 'About', 'コラボレーションについて', 'About our collaborations', 'コラボレーション' ); ?><p class="pd__cp"><?php echo hj_c( 'COLLAB_CATCH' ); ?></p></div>
<div class="about__txt rv"><p><?php echo hj_c( 'COLLAB_P1' ); ?></p><p><?php echo hj_c( 'COLLAB_P2' ); ?></p></div>
</div></section>
<section class="sec sec--t blush collab" id="works"><div class="wrap">
<?php echo hj_shd( '02', 'Portfolio', 'コラボレーション実績', 'Collaboration portfolio', 'コラボレーション実績', null, 'shd--c' ); ?>
<ul class="ipcards"><?php echo hj_ip_cards( true ); ?></ul>
<p class="note ctr-t"><?php echo hj_ipnote(); ?><br><?php echo hj_t( '※ IP名称・画像の公開範囲は各ライセンス契約を確認のうえ掲載します', 'IP names and images will be published within the scope of each licence agreement' ) . ' ' . hj_tbd(); ?></p>
</div></section>
<section class="sec" id="value"><div class="wrap why__g">
<div class="why__h rv"><?php echo hj_shd( '03', 'Merit', 'パートナー様への<br>メリット', 'What this means<br><em>for distributors</em>', 'パートナー様へのメリット' ); ?>
<div class="ctas"><?php echo hj_cta_btn( 'oem', 'btn--fill' ) . hj_lnk( hj_link( '/partners/' ), '代理店募集について', 'Partnership programme' ); ?></div></div>
<?php echo hj_numbered( $values ); ?>
</div></section>
<?php
get_footer();
