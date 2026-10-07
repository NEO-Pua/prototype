<?php
/**
 * Cosmoprof Asia buyer page /cosmoprof-asia/ (mockup: lp_page()), for visitors who scan the
 * booth QR code: its own slim header and footer, no site menu. The QR code opens the English
 * page (/en/cosmoprof-asia/). Show facts come from the next 展示会 post; contacts, QR images
 * and PDFs from サイト設定 → 展示会担当; the booking form is sent by the plugin.
 */

defined( 'ABSPATH' ) || exit;

$e    = hj_next_exhibition();
$exf  = fn( string $f ) => $e ? hj_ex( $e, $f ) : '';
$name = $e ? esc_html( hj_title( $e ) ) : 'Cosmoprof Asia';
$st   = hj_form();
$lng  = '<span class="lng" role="group" aria-label="Language"><a href="' . esc_url( strtok( hj_switch_url( 'ja' ), '?' ) ) . '" class="' . ( hj_is_en() ? '' : 'on' ) . '" lang="ja">JA</a><a href="' . esc_url( strtok( hj_switch_url( 'en' ), '?' ) ) . '" class="' . ( hj_is_en() ? 'on' : '' ) . '" lang="en">EN</a></span>';
$qr   = strtok( hj_switch_url( 'en' ), '?' );
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class( 'pg-lp' ); ?>>
<?php wp_body_open(); ?>
<a class="skip" href="#main"><?php echo hj_t( '本文へスキップ', 'Skip to content' ); ?></a>
<header class="lp-hd" data-hd><div class="lp-hd__in">
<a class="hd__logo" href="<?php echo esc_url( hj_link( '/' ) ); ?>"><img src="<?php echo esc_url( hj_img( 'logo.svg' ) ); ?>" alt="花印 HANAJIRUSHI" width="132" height="35"></a>
<p class="lp-hd__ev"><b><?php echo $name; ?></b><span><?php echo hj_t( '香港・2026年11月', 'Hong Kong · November 2026' ); ?></span></p>
<div class="hd__r"><?php echo $lng; ?><a class="hd__cta" href="#booking"><?php echo hj_t( '商談を予約', 'Book a meeting' ); ?></a></div>
</div></header>
<main id="main">
<?php
// ------------------------------------------------------------------ hero
$facts = array( array( hj_t( '会期', 'Dates' ), $exf( 'dates' ) ), array( hj_t( '会場', 'Venue' ), $exf( 'venue' ) ), array( hj_t( 'ブース', 'Booth' ), $exf( 'booth' ) ), array( hj_t( '対応言語', 'Languages' ), $exf( 'languages' ) ) );
$dl    = implode( '', array_map( fn( $f ) => '<div><dt>' . $f[0] . '</dt><dd>' . $f[1] . '</dd></div>', $facts ) );
$shown = array_values( array_filter( hj_home_products(), 'has_post_thumbnail' ) );
$hero  = $shown[1] ?? ( $shown[0] ?? null );
?>
<section class="lp-hero"><div class="wrap lp-hero__g">
<div class="lp-hero__txt rv"><?php echo hj_eb( $name . ' · Hong Kong' ); ?>
<h1 class="lp-hero__h"><?php echo hj_lines( hj_t( '<span class="nw"><span class="lat">' . $name . '</span>で、</span><br>お会いしましょう。', 'Meet us at<br><em>' . $name . '</em>' ) ); ?></h1>
<p class="lp-hero__lead"><?php echo hj_t( '東京・銀座の日本製スキンケアメーカー、花印です。', 'HANAJIRUSHI — Japanese skincare, developed in our own laboratory in Ginza, Tokyo. ' ) . hj_c( 'EXH_INTRO' ); ?></p>
<dl class="dl"><?php echo $dl; ?></dl>
<div class="ctas"><?php echo hj_btn( '#booking', '商談を予約する', 'Book a meeting', 'btn--fill' ) . hj_lnk( '#products', '出展製品を見る', 'See the products' ); ?></div></div>
<div class="lp-hero__vis rv"><?php echo ( $hero ? hj_win( hj_product_photo( $hero->ID ), hj_title( $hero ), 'win--l' ) : '' ) . hj_seal( '花印', 'seal--l' ); ?></div>
</div></section>
<nav class="anc" aria-label="<?php echo esc_attr( hj_t( 'ページ内リンク', 'On this page' ) ); ?>"><div class="wrap">
<?php
foreach ( array( array( 'products', '出展製品', 'Products' ), array( 'strengths', '日本製の強み', 'Strengths' ), array( 'business', 'お取引', 'Business' ), array( 'booking', '商談予約', 'Book a meeting' ), array( 'contact', '展示会担当', 'Show contacts' ) ) as $a ) {
	echo '<a href="#' . $a[0] . '">' . hj_t( $a[1], $a[2] ) . '</a>';
}
?>
</div></nav>
<?php
// ------------------------------------------------------------------ figures, products, strengths
$rs   = hj_c( 'REASONS' );
$nums = '';
foreach ( array( 0, 2, 1, 4 ) as $i ) {
	$nums .= '<li class="rv"><small>' . $rs[ $i ][0] . '</small><b class="' . ( ctype_digit( substr( $rs[ $i ][1], 0, 1 ) ) ? 'num' : 'word' ) . '">' . $rs[ $i ][1] . '</b><p>' . $rs[ $i ][3] . '</p></li>';
}
$cards = '';
foreach ( $shown as $i => $p ) {
	$cards .= '<li class="rv">' . hj_win( hj_product_photo( $p->ID ), hj_title( $p ) ) . '
<p class="col__no">No.' . sprintf( '%02d', $i + 1 ) . '<span>' . esc_html( hj_product_cat( $p ) ) . '</span></p><h3>' . hj_pname( hj_title( $p ) ) . '</h3><p class="col__d">' . esc_html( (string) hj_get( 'short', $p->ID ) ) . '</p>
<p class="lp-prod__a"><a class="lnk lnk--s" href="#booking" data-pick="' . esc_attr( $p->post_name ) . '"><span>' . hj_t( 'この製品を相談する', 'Discuss this product' ) . '</span>' . HJ_ARR . '</a>
<a class="lnk lnk--s" href="' . esc_url( get_permalink( $p ) ) . '"><span>' . hj_t( '製品の詳細', 'Product details' ) . '</span>' . HJ_ARR . '</a></p></li>';
}
$j4  = '';
$kan = array( '研', '造', '質', '績' );
foreach ( hj_c( 'JAPAN4' ) as $i => $j ) {
	$j4 .= '<li class="rv">' . hj_j4_mark( $i, $kan[ $i ] ) . '<p class="j4__n">' . sprintf( '%02d', $i + 1 ) . '</p><h3>' . $j[1] . '</h3><p>' . $j[2] . '</p>' . $j[3] . '</li>';
}
?>
<section class="nums lp-nums"><div class="wrap"><ul class="nums__l"><?php echo $nums; ?></ul></div></section>
<section class="sec col lp-prod" id="products"><div class="wrap">
<?php echo hj_shd( '01', 'On display', '出展製品', 'On display', '出展製品', hj_t( '無香料・無着色・オイルフリー・アルコールフリー。ブースでお試しいただけます。', 'Fragrance-free, colorant-free, oil-free, alcohol-free. Try them at our booth.' ), 'shd--c' ); ?>
<ul class="col__l col__l--3"><?php echo $cards; ?></ul>
<div class="ctr"><?php echo hj_lnk( hj_link( '/products/' ), 'すべての製品を見る', 'All products' ); ?></div></div></section>
<section class="sec sec--t dark j4" id="strengths"><div class="wrap">
<?php echo hj_shd( '02', 'Made in Japan', '「日本製」4つの強み', 'Made in Japan —<br><em>four strengths</em>', '日本製の強み', null, 'shd--c' ); ?>
<ol class="j4__l"><?php echo $j4; ?></ol>
<div class="ctr"><?php echo hj_lnk( hj_link( '/rd/' ), '研究開発・品質管理', 'R&amp;D and quality' ); ?></div></div></section>
<?php
// ------------------------------------------------------------------ business, steps
$terms = hj_pairs( 'terms', 'label', 'value' );
$rows  = '';
foreach ( array( 0, 1, 2, 3, 6 ) as $i ) {
	if ( isset( $terms[ $i ] ) ) {
		$rows .= '<div><dt>' . esc_html( $terms[ $i ][0] ) . '</dt><dd>' . hj_text( $terms[ $i ][1] ) . '</dd></div>';
	}
}
$docs = implode( '', array_map( fn( $d ) => '<li>' . $d[0] . '</li>', hj_c( 'EXPORT_DOCS' ) ) );
?>
<section class="sec sec--t blush" id="business"><div class="wrap lp-biz__g">
<div class="rv"><?php echo hj_shd( '03', 'Working together', '市場に合わせた<br>お取引', 'A model that<br><em>fits your market</em>', 'お取引について' ); ?>
<ul class="models"><?php echo hj_c( 'MODELS_MINI' ); ?></ul>
<?php echo hj_lnk( hj_link( '/partners/' ), '代理店募集の詳細', 'Partnership programme' ); ?></div>
<div class="rv"><p class="pform__h"><?php echo hj_t( '主な取引条件', 'Trade terms at a glance' ); ?></p>
<dl class="dl"><?php echo $rows; ?></dl>
<p class="pform__h lp-biz__h"><?php echo hj_t( 'ご用意できる輸出書類', 'Export documents we prepare' ); ?></p>
<ul class="tags tags--ink"><?php echo $docs; ?></ul>
<?php echo hj_show_tbc() ? '<p class="note">' . hj_t( '※ 数値・対応範囲は確認のうえ掲載します。', 'Figures and scope to be confirmed before publishing.' ) . '</p>' : ''; ?></div>
</div></section>
<section class="sec sec--t" id="steps"><div class="wrap">
<?php echo hj_shd( '04', 'Next steps', 'お取引開始までの流れ', 'From first meeting<br><em>to first order</em>', 'お取引の流れ', null, 'shd--c' ) . hj_flow( hj_c( 'PARTNER_STEPS' ) ); ?></div></section>
<?php
// ------------------------------------------------------------------ booking (one step) and show contacts
$f      = 'booking';
$action = esc_url( strtok( hj_switch_url( hj_lang() ), '?' ) ) . '#form';
$qr_img = function ( string $field, string $cap ): string {
	$u = hj_file_url( hj_opt_raw( $field ) );
	return '<figure>' . ( $u ? '<img src="' . esc_url( $u ) . '" alt="' . esc_attr( $cap ) . ' QR" width="96" height="96">' : '<span>QR</span>' ) . '<figcaption>' . $cap . '</figcaption></figure>';
};
$pdf = function ( string $field, string $ja, string $en ): string {
	$u = hj_file_url( hj_opt_raw( $field ) );
	return '<li><a href="' . esc_url( $u ?: '#' ) . '"' . ( $u ? ' target="_blank" rel="noopener"' : '' ) . '>' . hj_t( $ja, $en ) . '<small>PDF</small></a></li>';
};
?>
<section class="sec sec--t blush" id="booking"><div class="wrap book__g">
<div class="rv"><?php echo hj_shd( '05', 'Book a meeting', '商談のご予約・お問い合わせ', 'Book a meeting<br><em>or send an enquiry</em>', '商談のご予約', hj_t( 'ご希望の日時をお知らせください。展示会担当者より日時を確定してご連絡します。お問い合わせだけでも承ります。', 'Tell us when suits you and our show team will confirm the time. You can also just send an enquiry.' ) ); ?>
<?php if ( 'done' === $st['step'] ) : ?>
<div class="pform pform--main pform--done" id="form"><p class="pform__h"><?php echo hj_t( 'ご予約・お問い合わせを受け付けました。', 'Thank you — your request has been sent.' ); ?></p>
<p><?php echo hj_t( '展示会担当者より、日時を確定してご連絡いたします。', 'Our show team will confirm the time with you.' ); ?></p></div>
<?php else : ?>
<form class="pform pform--main" id="form" method="post" action="<?php echo $action; ?>" novalidate>
	<?php echo ! empty( $st['errors'] ) ? '<p class="ferr ferr--top" role="alert">' . esc_html( $st['errors']['_'] ?? hj_t( '入力内容をご確認ください。', 'Please check the highlighted fields.' ) ) . '</p>' : ''; ?>
<p class="pform__h"><?php echo hj_t( 'ご希望の日時', 'Preferred day and time' ); ?></p>
<div class="fgrid fgrid--when">
<?php
echo hj_fld( 'day', hj_t( 'ご希望の日', 'Preferred day' ), hj_select( 'day', hj_form_opt( 'days' ) ), hj_req( $f, 'day' ) );
echo hj_fld( 'time', hj_t( 'ご希望の時間帯', 'Preferred time' ), hj_input( 'time', 'text', hj_t( '例）14:00頃、午後、いつでも可', 'e.g. around 14:00, afternoon, any time' ) ), hj_req( $f, 'time' ) );
?>
</div>
<p class="note"><?php echo hj_t( '会期：', 'Show dates: ' ) . $exf( 'dates' ) . '　' . hj_t( '担当者より日時を確定してご連絡します。', 'Our show team will confirm the time by reply.' ); ?></p>
<p class="pform__h lp-who"><?php echo hj_t( 'お客様情報', 'Your details' ); ?></p>
<div class="fgrid">
<?php
echo hj_fld( 'company', hj_t( '会社名', 'Company' ), hj_input( 'company', 'text', '', ' autocomplete="organization"' ), hj_req( $f, 'company' ) );
echo hj_fld( 'country', hj_t( '国・地域', 'Country / region' ), hj_input( 'country', 'text', '', ' autocomplete="country-name"' ), hj_req( $f, 'country' ) );
echo hj_fld( 'name', hj_t( 'お名前', 'Name' ), hj_input( 'name', 'text', '', ' autocomplete="name"' ), hj_req( $f, 'name' ) );
echo hj_fld( 'email', hj_t( 'メールアドレス', 'Business email' ), hj_input( 'email', 'email', '', ' autocomplete="email"' ), hj_req( $f, 'email' ) );
echo hj_fld( 'chat', 'WhatsApp / WeChat', hj_input( 'chat' ), hj_req( $f, 'chat' ) );
echo hj_fld( 'biz', hj_t( '事業形態', 'Business type' ), hj_select( 'biz', hj_form_opt( 'biz' ) ), hj_req( $f, 'biz' ) );
?>
<fieldset class="fld fld--full"><legend><?php echo hj_t( 'ご関心の製品', 'Products of interest' ); ?><em class="opt"><?php echo hj_t( '任意', 'Optional' ); ?></em></legend><div class="opts"><?php echo hj_form_lines_html(); ?></div></fieldset>
<?php echo hj_fld( 'message', hj_t( 'ご相談内容', 'Message' ), '<textarea name="f_message" rows="4">' . esc_textarea( (string) hj_form_value( 'message' ) ) . '</textarea>', hj_req( $f, 'message' ), true ); ?>
</div>
<label class="agree"><input type="checkbox" name="f_agree" value="1"<?php checked( (bool) hj_form_value( 'agree' ) ); ?>><?php echo hj_t( '個人情報の取り扱いに同意する', 'I agree to the handling of my personal information' ); ?></label>
<?php echo hj_form_error( 'agree' ) . hj_form_hidden( $f, 'send' ); ?>
<div class="pform__sub"><button class="btn btn--fill" type="submit"><span><?php echo hj_t( '予約・お問い合わせを送信', 'Send my request' ); ?></span><?php echo HJ_ARR; ?></button></div>
<p class="note ctr-t"><?php echo hj_t( '内容を確認のうえ、展示会担当者よりご連絡します。', 'Our show team will get back to you.' ); ?></p>
</form>
<?php endif; ?>
</div>
<aside class="book__side rv" id="contact"><p class="pform__h"><?php echo hj_t( '展示会担当者', 'Your contact at the show' ); ?></p>
<dl class="dl">
<div><dt><?php echo hj_t( '担当者', 'Contact' ); ?></dt><dd><?php echo hj_text( hj_opt_raw( 'show_contact' ) ); ?></dd></div>
<div><dt>WhatsApp</dt><dd><?php echo hj_text( hj_opt_raw( 'show_whatsapp' ) ); ?></dd></div>
<div><dt>WeChat</dt><dd><?php echo hj_text( hj_opt_raw( 'show_wechat' ) ); ?></dd></div>
<div><dt><?php echo hj_t( 'メール', 'Email' ); ?></dt><dd><?php echo hj_text( hj_opt_raw( 'show_email' ) ); ?></dd></div>
<div><dt><?php echo hj_t( '東京本社', 'Tokyo office' ); ?></dt><dd><a href="<?php echo esc_attr( hj_tel_href() ); ?>"><?php echo esc_html( hj_tel() ); ?></a></dd></div></dl>
<div class="qrs"><?php echo $qr_img( 'qr_wechat', 'WeChat' ) . $qr_img( 'qr_whatsapp', 'WhatsApp' ); ?></div>
<p class="pform__h"><?php echo hj_t( '資料ダウンロード', 'Downloads' ); ?></p>
<ul class="dlist"><?php echo $pdf( 'pdf_profile', '会社案内', 'Company profile' ) . $pdf( 'pdf_catalog', '製品カタログ', 'Product catalogue' ); ?></ul></aside>
</div></section>
<section class="sec sec--t lp-share" id="share"><div class="wrap lp-share__g">
<figure class="lp-qr rv"><div id="lp-qr" data-qr="<?php echo esc_attr( $qr ); ?>" aria-label="<?php echo esc_attr( hj_t( 'このページのQRコード', 'QR code for this page' ) ); ?>"><span>QR</span></div></figure>
<div class="rv"><?php echo hj_shd( '06', 'Share', 'このページを共有', 'Share<br><em>this page</em>', 'ページを共有', hj_t( '同僚の方への共有や、後で見返すときにご利用ください。QRコードを読み取ると英語版が開きます（右上で日本語に切り替えられます）。', 'Pass it to a colleague, or keep it for after the show. The QR code opens the English page; switch to Japanese at the top.' ) ); ?>
<p class="lp-url" data-share-url></p>
<div class="ctas"><button class="btn" type="button" data-copy><span><?php echo hj_t( 'リンクをコピー', 'Copy link' ); ?></span><?php echo HJ_ARR; ?></button>
<button class="lnk" type="button" data-qr-dl><span><?php echo hj_t( 'QRコードを保存（PNG）', 'Save QR code (PNG)' ); ?></span><?php echo HJ_ARR; ?></button></div></div>
</div></section>
</main>
<footer class="ft lp-ft"><div class="wrap">
<div class="lp-ft__g"><div class="ft__co"><a class="ft__logo" href="<?php echo esc_url( hj_link( '/' ) ); ?>"><img src="<?php echo esc_url( hj_img( 'logo.svg' ) ); ?>" alt="花印 HANAJIRUSHI" width="150" height="40"></a><?php echo hj_seal( '花印', 'seal--s' ); ?>
<p class="ft__name"><?php echo esc_html( (string) hj_opt( 'company' ) ); ?></p>
<p><?php echo hj_text( hj_opt( 'address' ) ); ?></p><p class="ft__tel">TEL <?php echo esc_html( hj_tel() ); ?></p></div>
<ul class="lp-ft__l"><li><a href="<?php echo esc_url( hj_link( '/' ) ); ?>"><?php echo hj_t( '公式サイト トップ', 'Main website' ); ?></a></li><li><a href="<?php echo esc_url( hj_link( '/products/' ) ); ?>"><?php echo hj_t( '製品', 'Products' ); ?></a></li>
<li><a href="<?php echo esc_url( hj_link( '/partners/' ) ); ?>"><?php echo hj_t( '代理店募集', 'Partnership programme' ); ?></a></li><li><a href="<?php echo esc_url( hj_link( '/company/' ) ); ?>"><?php echo hj_t( '会社概要', 'Company profile' ); ?></a></li></ul></div>
<div class="ft__btm"><p>© <?php echo esc_html( wp_date( 'Y' ) ); ?> Hanajirushi Institute of Cosmetics, Inc.</p><div><a href="<?php echo esc_url( hj_link( '/privacy-policy/' ) ); ?>"><?php echo hj_t( 'プライバシーポリシー', 'Privacy policy' ); ?></a><a href="<?php echo esc_url( strtok( hj_switch_url( hj_is_en() ? 'ja' : 'en' ), '?' ) ); ?>"><?php echo hj_t( 'English', '日本語' ); ?></a></div></div>
</div></footer>
<div class="lp-bar"><a class="btn btn--fill" href="#booking"><span><?php echo hj_t( '商談を予約する', 'Book a meeting' ); ?></span><?php echo HJ_ARR; ?></a><a class="btn" href="#contact"><span><?php echo hj_t( '担当者に連絡', 'Contact us' ); ?></span></a></div>
<button class="totop" type="button" aria-label="<?php echo esc_attr( hj_t( 'ページトップへ', 'Back to top' ) ); ?>"><?php echo HJ_UP; ?></button>
<div class="toast" role="status" aria-live="polite"></div>
<?php wp_footer(); ?>
</body></html>
