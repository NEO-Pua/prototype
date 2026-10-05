<?php
/**
 * お問い合わせ /contact/ (mockup: p_contact()): topics, channels, the enquiry form
 * (入力 → 確認 → 完了). The plugin checks and sends it (hanajirushi-core/inc/forms.php);
 * ?topic=…&item=… pre-select the form (premium.js).
 */

defined( 'ABSPATH' ) || exit;

get_header();

echo hj_phero( 'Contact', 'お問い合わせ', 'Contact',
	hj_t( 'お取引・代理店・製品に関するご相談はこちらから。', 'Distribution, trade, product and OEM enquiries.' ), '', '相談' );

$st     = hj_form();
$step   = $st['step'];
$kinds  = function_exists( 'hj_form_opt' ) ? hj_form_opt( 'kinds' ) : array();
$keys   = array_keys( HJ_TOPICS );
$blurbs = array(
	hj_t( '独占代理店・販売代理店・モダントレード・越境ECのご相談。', 'Exclusive or authorised distribution, modern trade and cross-border e-commerce.' ),
	hj_t( '製品仕様・サンプル・成分・輸出書類についてのお問い合わせ。', 'Specifications, samples, ingredients and export documents.' ),
	hj_t( '自社ブランド製品の開発、IPコラボレーション商品の企画。', 'Private-label development and licensed IP collaborations.' ),
	hj_t( '展示会での商談、その他のご相談。', 'Meetings at exhibitions, and anything else.' ),
);
$topics = '';
foreach ( $keys as $i => $k ) {
	$topics .= '<li class="rv"><a href="' . esc_url( hj_topic_url( $k ) ) . '"><i>' . sprintf( '%02d', $i + 1 ) . '</i><b>' . esc_html( $kinds[ $i ] ?? '' ) . '</b><small>' . $blurbs[ $i ] . '</small>' . HJ_ARR . '</a></li>';
}
$chat = trim( (string) hj_opt_raw( 'show_wechat' ) . ' ' . (string) hj_opt_raw( 'show_whatsapp' ) );

// step bar
$bar = '<ol class="fstep">';
foreach ( array( array( 'input', '入力', 'Enter' ), array( 'confirm', '確認', 'Confirm' ), array( 'done', '完了', 'Done' ) ) as $i => $s ) {
	$bar .= '<li' . ( $s[0] === $step ? ' class="on"' : '' ) . '><i>' . sprintf( '%02d', $i + 1 ) . '</i>' . hj_t( $s[1], $s[2] ) . '</li>';
}
$bar .= '</ol>';

$action = esc_url( strtok( hj_switch_url( hj_lang() ), '?' ) ) . '#form';   // no ?topic=: the visitor's own choice stays after 戻る
?>
<section class="sec sec--t"><div class="wrap">
<?php echo hj_shd( '01', 'Topics', 'ご相談内容から選ぶ', 'Choose<br><em>a topic</em>', 'ご相談内容', hj_t( 'ご相談内容を選ぶと、フォームの種別が選択された状態になります。', 'Pick a topic and the form below opens with it selected.' ) ); ?>
<ul class="topics"><?php echo $topics; ?></ul>
<ul class="cells cells--3 chan">
<li class="rv"><small><?php echo hj_t( 'お電話', 'Telephone' ); ?></small><h3><a href="<?php echo esc_attr( hj_tel_href() ); ?>"><?php echo esc_html( hj_tel() ); ?></a></h3><p><?php echo esc_html( hj_hours() ); ?></p></li>
<li class="rv"><small><?php echo hj_t( 'フォーム', 'Enquiry form' ); ?></small><h3><?php echo hj_t( '3営業日以内にご返信', 'Reply within 3 business days' ); ?></h3><p><?php echo hj_t( '下記フォームより送信ください。', 'Use the form below.' ); ?></p></li>
<li class="rv"><small>WhatsApp / WeChat</small><h3><?php echo hj_t( '海外のお客様', 'Overseas partners' ); ?></h3><p><?php echo hj_t( 'こちらからもご連絡いただけます。', 'Message us directly.' ) . ' ' . hj_text( 'WeChat ' . hj_opt_raw( 'show_wechat' ) . ' / WhatsApp ' . hj_opt_raw( 'show_whatsapp' ) ); ?></p></li></ul>
</div></section>
<section class="sec sec--t blush"><div class="wrap wrap--form">
<?php echo hj_shd( '02', 'Enquiry form', 'お問い合わせフォーム', 'Enquiry form', 'お問い合わせフォーム', null, 'shd--c' ); ?>
<?php if ( 'done' === $step ) : ?>
<div class="pform pform--main pform--done" id="form"><?php echo $bar; ?>
<p class="pform__h"><?php echo hj_t( 'お問い合わせを受け付けました。', 'Thank you — your enquiry has been sent.' ); ?></p>
<p><?php echo hj_t( '内容を確認のうえ、3営業日以内に担当者よりご連絡いたします。受付確認のメールをお送りしましたので、あわせてご確認ください。', 'We will reply within 3 business days. A confirmation has been sent to your email address.' ); ?></p>
<div class="pform__sub"><?php echo hj_btn( hj_link( '/' ), 'トップページへ', 'Back to the home page' ); ?></div></div>
<?php elseif ( 'confirm' === $step ) : ?>
<form class="pform pform--main" id="form" method="post" action="<?php echo $action; ?>"><?php echo $bar; ?>
<p class="pform__h"><?php echo hj_t( '以下の内容で送信します。よろしければ「送信する」を押してください。', 'Please check your enquiry, then send it.' ); ?></p>
<dl class="dl cfm">
<?php
foreach ( hj_form_fields( 'contact' ) as $name => $f ) {
	$v = hj_form_value( $name );
	if ( 'agree' === $f[4] ) {
		continue;
	}
	$shown = hj_form_display( $name, $v );
	echo '<div><dt>' . esc_html( hj_t( $f[0], $f[1] ) ) . '</dt><dd>' . ( '' !== $shown ? nl2br( esc_html( $shown ) ) : '—' ) . '</dd></div>';
}
?>
</dl>
<?php
foreach ( hj_form()['values'] as $name => $v ) {
	foreach ( (array) $v as $one ) {
		echo '<input type="hidden" name="' . esc_attr( hj_fname( $name ) . ( is_array( $v ) ? '[]' : '' ) ) . '" value="' . esc_attr( (string) $one ) . '">';
	}
}
echo hj_form_hidden( 'contact', 'send' );
?>
<div class="pform__sub cfm__b"><button class="btn" type="submit" name="hj_step" value="back"><span><?php echo hj_t( '入力画面に戻る', 'Edit' ); ?></span></button><button class="btn btn--fill" type="submit"><span><?php echo hj_t( '送信する', 'Send' ); ?></span><?php echo HJ_ARR; ?></button></div>
</form>
<?php else : ?>
<form class="pform pform--main" id="form" method="post" action="<?php echo $action; ?>" novalidate><?php echo $bar; ?>
	<?php echo ! empty( $st['errors'] ) ? '<p class="ferr ferr--top" role="alert">' . esc_html( $st['errors']['_'] ?? hj_t( '入力内容をご確認ください。', 'Please check the highlighted fields.' ) ) . '</p>' : ''; ?>
<?php
$cur_k = (string) hj_form_value( 'k' ) ?: $keys[0];
$kind  = '';
foreach ( $keys as $i => $k ) {
	$kind .= '<label><input type="radio" name="k" value="' . esc_attr( $k ) . '"' . checked( $cur_k, $k, false ) . '>' . esc_html( $kinds[ $i ] ?? '' ) . '</label>';
}
$c = 'contact';
?>
<fieldset class="fld fld--full"><legend><?php echo hj_t( 'お問い合わせ種別', 'Enquiry type' ); ?><em class="req"><?php echo hj_t( '必須', 'Required' ); ?></em></legend><div class="opts"><?php echo $kind; ?></div></fieldset>
<div class="fgrid">
<?php
echo hj_fld( 'company', hj_t( '会社名', 'Company name' ), hj_input( 'company', 'text', hj_t( '例）花印粧業研究所株式会社', 'e.g. ABC Trading Co., Ltd.' ), ' autocomplete="organization"' ), hj_req( $c, 'company' ) );
echo hj_fld( 'country', hj_t( '国・地域', 'Country / region' ), hj_input( 'country', 'text', hj_t( '例）日本、ベトナム', 'e.g. Vietnam' ), ' autocomplete="country-name"' ), hj_req( $c, 'country' ) );
echo hj_fld( 'name', hj_t( 'お名前', 'Contact person' ), hj_input( 'name', 'text', hj_t( '例）山田 花子', 'e.g. Jane Tan' ), ' autocomplete="name"' ), hj_req( $c, 'name' ) );
echo hj_fld( 'position', hj_t( '役職', 'Position' ), hj_input( 'position' ), hj_req( $c, 'position' ) );
echo hj_fld( 'email', hj_t( 'メールアドレス', 'Business email' ), hj_input( 'email', 'email', hj_t( '例）info@example.com', 'e.g. jane@company.com' ), ' autocomplete="email"' ), hj_req( $c, 'email' ), false, hj_t( 'フリーメールではなく、会社ドメインのアドレスをご記入ください。', 'Please use your company domain rather than a free webmail address.' ) );
echo hj_fld( 'phone', hj_t( '電話番号', 'Phone' ), hj_input( 'phone', 'tel', hj_t( '例）03-1234-5678', 'e.g. +84 28 1234 5678' ), ' autocomplete="tel"' ), hj_req( $c, 'phone' ) );
echo hj_fld( 'chat', 'WhatsApp / WeChat', hj_input( 'chat' ), hj_req( $c, 'chat' ), false, hj_t( '海外のお客様はいずれかをご記入ください。', 'Either one is fine.' ) );
echo hj_fld( 'biz', hj_t( '事業形態', 'Business type' ), hj_select( 'biz', hj_form_opt( 'biz' ) ), hj_req( $c, 'biz' ) );
echo hj_fld( 'market', hj_t( '対象市場', 'Target market' ), hj_input( 'market', 'text', hj_t( '例）タイ、マレーシア', 'e.g. Thailand, Malaysia' ) ), hj_req( $c, 'market' ) );
echo hj_fld( 'volume', hj_t( '年間予定仕入数量', 'Estimated annual volume' ), hj_select( 'volume', hj_form_opt( 'volumes' ) ), hj_req( $c, 'volume' ) );
?>
<fieldset class="fld fld--full"><legend><?php echo hj_t( 'ご関心の製品', 'Products of interest' ); ?><em class="opt"><?php echo hj_t( '任意', 'Optional' ); ?></em></legend><div class="opts"><?php echo hj_form_lines_html(); ?></div></fieldset>
<?php
echo hj_fld( 'website', hj_t( '会社ウェブサイト', 'Company website' ), hj_input( 'website', 'url', 'https://' ), hj_req( $c, 'website' ) );
echo hj_fld( 'channels', hj_t( '現在の販売チャネル', 'Current channels' ), hj_input( 'channels' ), hj_req( $c, 'channels' ) );
echo hj_fld( 'message', hj_t( 'お問い合わせ内容', 'Message' ), '<textarea name="f_message" rows="6">' . esc_textarea( (string) hj_form_value( 'message' ) ) . '</textarea>', hj_req( $c, 'message' ), true );
?>
<fieldset class="fld fld--full"><legend><?php echo hj_t( '展示会', 'Exhibition' ); ?><em class="opt"><?php echo hj_t( '任意', 'Optional' ); ?></em></legend><div class="opts"><label><input type="checkbox" name="f_at_show" value="1"<?php checked( (bool) hj_form_value( 'at_show' ) ); ?>><?php echo hj_t( '展示会会場からのお問い合わせです', 'I am contacting you from the exhibition floor' ); ?></label></div></fieldset>
</div>
<div class="pp"><b><?php echo hj_t( '個人情報の取り扱いについて', 'Handling of personal information' ); ?></b><?php echo hj_t( '花印粧業研究所株式会社は、お問い合わせいただいた個人情報を、お問い合わせへの回答およびご連絡のためにのみ利用し、法令に基づく場合を除き、ご本人の同意なく第三者に提供することはありません。', 'Hanajirushi Institute of Cosmetics, Inc. uses the personal information you provide only to respond to your enquiry, and does not share it with third parties without your consent except where required by law.' ); ?></div>
<label class="agree"><input type="checkbox" name="f_agree" value="1"<?php checked( (bool) hj_form_value( 'agree' ) ); ?>><?php echo hj_t( '個人情報の取り扱いに同意する', 'I agree to the handling of my personal information' ); ?></label>
<?php echo function_exists( 'hj_form_error' ) ? hj_form_error( 'agree' ) : ''; ?>
<?php echo function_exists( 'hj_form_hidden' ) ? hj_form_hidden( 'contact', 'confirm' ) : ''; ?>
<div class="pform__sub"><button class="btn btn--fill" type="submit"><span><?php echo hj_t( '入力内容を確認する', 'Review my enquiry' ); ?></span><?php echo HJ_ARR; ?></button></div>
<p class="note ctr-t"><?php echo hj_t( '送信後、自動返信メールにて受付確認をお送りします。', 'After sending, you will receive an automatic confirmation by email.' ); ?></p>
</form>
<?php endif; ?>
</div></section>
<?php
get_footer();
