<?php
/**
 * 研究開発・品質 /rd/ (mockup: p_rd()): laboratory, process, quality, export documents,
 * registration support.
 */

defined( 'ABSPATH' ) || exit;

get_header();

echo hj_phero( 'R&amp;D / Quality', '研究開発・<br>品質管理', 'R&amp;D &amp; Quality',
	hj_t( '銀座の自社研究室から、確かな処方を。', 'Reliable formulas, from our own laboratory in Ginza.' ), '', '研究',
	array( array( hj_link( '/company/' ), hj_t( '会社情報', 'Company' ) ) ),
	array( 'anchors' => array( array( 'lab', hj_t( '自社研究室', 'Laboratory' ) ), array( 'process', hj_t( '開発から出荷まで', 'Process' ) ), array( 'quality', hj_t( '品質管理体制', 'Quality' ) ),
		array( 'docs', hj_t( '輸出書類', 'Export documents' ) ), array( 'regist', hj_t( '各国登録の支援', 'Registration' ) ) ) ) );

$trio = '';
for ( $i = 1; $i <= 3; $i++ ) {
	$trio .= '<li class="rv"><p class="craft__n"><span>' . hj_kan( $i - 1 ) . '</span></p><h3>' . hj_c( "RD_POINT{$i}_T" ) . '</h3><p>' . hj_c( "RD_POINT{$i}_D" ) . '</p></li>';
}
$tags = implode( '', array_map( fn( $x ) => '<li>' . $x . '</li>', hj_c( 'RD_TAGS' ) ) );
$q    = '';
for ( $i = 1; $i <= 3; $i++ ) {
	$q .= '<li class="rv">' . ( hj_is_en() ? '' : '<small>' . hj_c( "QUALITY{$i}_S" ) . '</small>' ) . '<h3>' . hj_c( "QUALITY{$i}_T" ) . '</h3><p>' . hj_c( "QUALITY{$i}_B" ) . '</p></li>';
}
?>
<section class="sec split" id="lab"><div class="wrap split__g">
<div class="split__img split__img--win rv"><?php echo hj_win( hj_img( 'h_campany_lab.jpg' ), hj_t( '銀座本社の研究室', 'Our laboratory in Ginza' ), 'win--m' ); ?></div>
<div class="split__txt rv"><?php echo hj_shd( '01', 'Laboratory', '銀座の自社研究室', 'Our laboratory in Ginza', '自社研究室' ); ?>
<p class="pd__cp"><?php echo hj_c( 'RD_CATCH' ); ?></p><p><?php echo hj_c( 'RD_P1' ); ?></p><p><?php echo hj_c( 'RD_P2' ); ?></p>
<ul class="tags tags--ink"><?php echo $tags; ?></ul>
<div class="ctas"><?php echo hj_cta_btn( 'oem', 'btn--fill' ); ?></div></div>
</div>
<div class="wrap"><ol class="trio"><?php echo $trio; ?></ol></div></section>
<section class="sec sec--t blush" id="process"><div class="wrap">
<?php echo hj_shd( '02', 'Process', '開発から出荷まで', 'From formulation<br><em>to shipment</em>', '開発プロセス', null, 'shd--c' ) . hj_flow( hj_c( 'RD_STEPS' ) ); ?></div></section>
<section class="sec" id="quality"><div class="wrap">
<?php echo hj_shd( '03', 'Quality', '品質管理体制', 'Quality management', '品質管理', hj_show_tbc() ? hj_t( '工場情報・認証・生産能力は確認のうえ掲載します。', 'Factory details, certifications and capacity will be published once confirmed.' ) : null ); ?>
<ul class="cells cells--3"><?php echo $q; ?></ul></div></section>
<section class="sec dark" id="docs"><div class="wrap docs__g">
<div><?php echo hj_shd( '04', 'Export documents', '輸出書類への対応', 'Export<br><em>documentation</em>', '輸出書類', hj_t( '海外のお取引先の輸入・登録手続きに必要な書類を、製品ごとにご用意します。', 'The documents your importer and regulator will ask for — prepared for each product.' ) ); ?></div>
<?php echo hj_docs_list(); ?></div></section>
<section class="sec sec--t" id="regist"><div class="wrap">
<?php echo hj_shd( '05', 'Registration', '各国登録の技術支援', 'Registration support<br><em>by market</em>', '各国登録', hj_t( '登録実績の有無にかかわらず、現地登録に必要な技術資料の提供でパートナー様の手続きを支援します。', 'Whether or not we have registered in your market before, we support your local registration with the technical documentation it requires.' ) ); ?>
<div class="rv"><?php echo hj_reg_table(); ?></div>
<div class="ctr ctr--2"><?php echo hj_cta_btn( 'product', 'btn--fill' ) . hj_lnk( hj_link( '/partners/' ), '代理店募集について', 'Partnership programme' ); ?></div></div></section>
<?php
get_footer();
