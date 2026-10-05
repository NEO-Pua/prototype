<?php
/**
 * Contact band and site footer (mockup: contact_band(), footer()).
 */

defined( 'ABSPATH' ) || exit;

$cols = '';
foreach ( hj_footer_cols() as $col ) {
	$cols .= '<div><h3>' . $col[0] . '</h3><ul>';
	foreach ( $col[1] as $l ) {
		$cols .= '<li><a href="' . esc_url( hj_link( $l[0] ) ) . '">' . $l[1] . '</a></li>';
	}
	$cols .= '</ul></div>';
}
$company = (string) ( hj_opt( 'company' ) ?: hj_t( '花印粧業研究所株式会社', 'Hanajirushi Institute of Cosmetics, Inc.' ) );
?>
</main>
<?php if ( 'contact' !== hj_page_key() ) { echo hj_contact_band(); } ?>
<footer class="ft"><div class="wrap">
<div class="ft__top">
<div class="ft__co"><a class="ft__logo" href="<?php echo esc_url( hj_link( '/' ) ); ?>"><img src="<?php echo esc_url( hj_img( 'logo.svg' ) ); ?>" alt="花印 HANAJIRUSHI" width="150" height="40"></a><?php echo hj_seal( '花印', 'seal--s' ); ?>
<p class="ft__name"><?php echo esc_html( $company ); ?></p>
<p><?php echo hj_text( hj_opt( 'address' ) ); ?></p><p class="ft__tel">TEL <?php echo esc_html( hj_tel() ); ?><br>FAX <?php echo esc_html( (string) hj_opt( 'fax' ) ); ?></p></div>
<nav class="ft__nav" aria-label="<?php echo esc_attr( hj_t( 'フッターメニュー', 'Footer menu' ) ); ?>"><?php echo $cols; ?></nav>
</div>
<div class="ft__btm"><p>© <?php echo esc_html( wp_date( 'Y' ) ); ?> Hanajirushi Institute of Cosmetics, Inc.</p>
<div><a href="<?php echo esc_url( hj_link( '/privacy-policy/' ) ); ?>"><?php echo hj_t( 'プライバシーポリシー', 'Privacy policy' ); ?></a><a href="<?php echo esc_url( hj_switch_url( hj_is_en() ? 'ja' : 'en' ) ); ?>"><?php echo hj_t( 'English', '日本語' ); ?></a></div></div>
</div></footer>
<button class="totop" type="button" aria-label="<?php echo esc_attr( hj_t( 'ページトップへ', 'Back to top' ) ); ?>"><?php echo HJ_UP; ?></button>
<div class="toast" role="status" aria-live="polite"></div>
<?php wp_footer(); ?>
</body></html>
