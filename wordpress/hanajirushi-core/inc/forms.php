<?php
/**
 * The site's two forms, without a form plugin:
 *
 *  - お問い合わせ (/contact/): 入力 → 確認 → 完了
 *  - 商談予約 (/cosmoprof-asia/): one step (the visitor is usually on a phone at the booth)
 *
 * The theme prints the fields (names below) and reads the state with hj_form(); this file
 * checks, keeps a copy in お問い合わせ履歴, emails the staff (サイト設定 → お問い合わせ) and,
 * if switched on, sends the visitor a confirmation. After sending, the page reloads with
 * ?sent=1 so a refresh never sends twice.
 *
 * Choices (enquiry types, business types, volumes…) are in form-options.json, made from the
 * mockup by wordpress/dev/sync.py, so the form says exactly what the mockup says.
 */

defined( 'ABSPATH' ) || exit;

/**
 * The name a field has in the page: f_<name>. Plain names such as name, day or year are
 * WordPress's own address variables, and posting them makes WordPress look for a post of that
 * name (a 404). The enquiry type keeps `k`: the design's script pre-selects it from ?topic=.
 */
function hj_fname( string $name ): string {
	return 'k' === $name ? 'k' : 'f_' . $name;
}

/** Form choices: topics (keys) plus labels per language. */
function hj_form_options(): array {
	static $o = null;
	if ( null === $o ) {
		$o = json_decode( (string) file_get_contents( HJ_CORE_DIR . 'inc/form-options.json' ), true ) ?: array();
	}
	return $o + array( hj_lang() => array() );
}

function hj_form_opt( string $key ): array {
	return hj_form_options()[ hj_lang() ][ $key ] ?? array();
}

/**
 * Fields of a form: name => [Japanese label, English label, required (JA), required (EN), kind].
 * English enquiries ask a little more (position, WhatsApp/WeChat, market, volume): they qualify
 * overseas leads (the mockup's EN_ONLY rule).
 */
function hj_form_fields( string $form ): array {
	$common = array(
		'company' => array( '会社名', 'Company name', 1, 1, 'text' ),
		'country' => array( '国・地域', 'Country / region', 1, 1, 'text' ),
		'name'    => array( 'お名前', 'Contact person', 1, 1, 'text' ),
		'email'   => array( 'メールアドレス', 'Business email', 1, 1, 'email' ),
		'chat'    => array( 'WhatsApp / WeChat', 'WhatsApp / WeChat', 0, 1, 'text' ),
		'biz'     => array( '事業形態', 'Business type', 1, 1, 'choice:biz' ),
	);
	if ( 'booking' === $form ) {
		return array(
			'day'      => array( 'ご希望の日', 'Preferred day', 0, 0, 'choice:days' ),
			'time'     => array( 'ご希望の時間帯', 'Preferred time', 0, 0, 'text' ),
		) + $common + array(
			'products' => array( 'ご関心の製品', 'Products of interest', 0, 0, 'lines' ),
			'message'  => array( 'ご相談内容', 'Message', 0, 0, 'textarea' ),
			'agree'    => array( '個人情報の取り扱い', 'Personal information', 1, 1, 'agree' ),
		);
	}
	return array(
		'k'        => array( 'お問い合わせ種別', 'Enquiry type', 1, 1, 'topic' ),
		'company'  => $common['company'],
		'country'  => $common['country'],
		'name'     => $common['name'],
		'position' => array( '役職', 'Position', 0, 1, 'text' ),
		'email'    => $common['email'],
		'phone'    => array( '電話番号', 'Phone', 0, 0, 'text' ),
		'chat'     => $common['chat'],
		'biz'      => $common['biz'],
		'market'   => array( '対象市場', 'Target market', 0, 1, 'text' ),
		'volume'   => array( '年間予定仕入数量', 'Estimated annual volume', 0, 1, 'choice:volumes' ),
		'products' => array( 'ご関心の製品', 'Products of interest', 0, 0, 'lines' ),
		'website'  => array( '会社ウェブサイト', 'Company website', 0, 0, 'text' ),
		'channels' => array( '現在の販売チャネル', 'Current channels', 0, 0, 'text' ),
		'message'  => array( 'お問い合わせ内容', 'Message', 1, 1, 'textarea' ),
		'at_show'  => array( '展示会', 'Exhibition', 0, 0, 'check' ),
		'agree'    => array( '個人情報の取り扱い', 'Personal information', 1, 1, 'agree' ),
	);
}

/** Product lines for the 「ご関心の製品」 boxes: key => [label, data-items (product slugs)]. */
function hj_form_lines(): array {
	$out = array();
	foreach ( hj_categories() as $k => $label ) {
		$slugs     = array_map( fn( $p ) => $p->post_name, hj_products( array( 'meta_query' => array( array( 'key' => 'category', 'value' => $k ) ) ) ) );
		$out[ $k ] = array( $label, implode( ' ', $slugs ) );
	}
	$extra = hj_form_opt( 'lines' );
	$out['ip']  = array( $extra[0] ?? hj_t( 'IPコラボ商品', 'IP collaborations' ), '' );
	$out['oem'] = array( $extra[1] ?? 'OEM/ODM', '' );
	return $out;
}

/** The current form state for the theme: step (input|confirm|done), values, errors. */
function hj_form(): array {
	return $GLOBALS['hj_form'] ?? array( 'step' => 'input', 'values' => array(), 'errors' => array(), 'form' => '' );
}

function hj_form_value( string $name ) {
	return hj_form()['values'][ $name ] ?? ( 'products' === $name ? array() : '' );
}

function hj_form_error( string $name ): string {
	$e = hj_form()['errors'][ $name ] ?? '';
	return $e ? '<small class="ferr" role="alert">' . esc_html( $e ) . '</small>' : '';
}

/** A field value as the visitor will read it back (confirm step, emails). */
function hj_form_display( string $name, $v ): string {
	$kind = hj_form_fields( hj_form()['form'] ?: 'contact' )[ $name ][4] ?? 'text';
	if ( 'topic' === $kind ) {
		$i = array_search( $v, hj_form_options()['topics'] ?? array(), true );
		return false === $i ? '' : ( hj_form_opt( 'kinds' )[ $i ] ?? '' );
	}
	if ( 'lines' === $kind ) {
		$lines = hj_form_lines();
		return implode( '、', array_map( fn( $k ) => $lines[ $k ][0] ?? $k, (array) $v ) );
	}
	if ( 'check' === $kind || 'agree' === $kind ) {
		return $v ? hj_t( 'はい', 'Yes' ) : '';
	}
	return (string) $v;
}

/** Reads and checks the posted fields. */
function hj_form_read( string $form ): array {
	$values = array();
	$errors = array();
	foreach ( hj_form_fields( $form ) as $name => $f ) {
		[ $ja, $en, $req_ja, $req_en, $kind ] = $f;
		$raw = wp_unslash( $_POST[ hj_fname( $name ) ] ?? '' );
		if ( 'lines' === $kind ) {
			$v = array_values( array_intersect( array_map( 'sanitize_key', (array) $raw ), array_keys( hj_form_lines() ) ) );
		} elseif ( 'check' === $kind || 'agree' === $kind ) {
			$v = ! empty( $raw ) ? 1 : 0;
		} elseif ( 'textarea' === $kind ) {
			$v = sanitize_textarea_field( (string) $raw );
		} elseif ( 'email' === $kind ) {
			$v = sanitize_email( (string) $raw );
		} elseif ( 'topic' === $kind ) {
			$v = in_array( $raw, hj_form_options()['topics'] ?? array(), true ) ? $raw : '';
		} elseif ( str_starts_with( $kind, 'choice:' ) ) {
			$v = in_array( $raw, hj_form_opt( substr( $kind, 7 ) ), true ) ? $raw : '';
		} else {
			$v = sanitize_text_field( (string) $raw );
		}
		$values[ $name ] = $v;
		$required = hj_is_en() ? $req_en : $req_ja;
		if ( $required && ( '' === $v || 0 === $v || array() === $v ) ) {
			$errors[ $name ] = 'agree' === $kind ? hj_t( '個人情報の取り扱いへの同意が必要です。', 'Please agree to the handling of your personal information.' )
				: hj_t( '入力してください。', 'This field is required.' );
		} elseif ( 'email' === $kind && '' !== $v && ! is_email( $v ) ) {
			$errors[ $name ] = hj_t( 'メールアドレスの形式をご確認ください。', 'Please check the email address.' );
		}
	}
	return array( $values, $errors );
}

add_action( 'template_redirect', function () {
	$form = is_page( 'contact' ) ? 'contact' : ( is_page( 'cosmoprof-asia' ) ? 'booking' : '' );
	if ( ! $form ) {
		return;
	}
	$GLOBALS['hj_form'] = array( 'step' => isset( $_GET['sent'] ) ? 'done' : 'input', 'values' => array(), 'errors' => array(), 'form' => $form );
	if ( 'POST' !== ( $_SERVER['REQUEST_METHOD'] ?? '' ) || ( $_POST['hj_form'] ?? '' ) !== $form ) {
		return;
	}
	[ $values, $errors ] = hj_form_read( $form );
	$step  = sanitize_key( $_POST['hj_step'] ?? 'confirm' );
	$state = array( 'values' => $values, 'errors' => $errors, 'form' => $form );

	if ( 'back' === $step ) {
		$GLOBALS['hj_form'] = $state + array( 'step' => 'input' );
		$GLOBALS['hj_form']['errors'] = array();
		return;
	}
	if ( $errors ) {
		$GLOBALS['hj_form'] = $state + array( 'step' => 'input' );
		return;
	}
	if ( 'confirm' === $step && 'contact' === $form ) {
		$GLOBALS['hj_form'] = $state + array( 'step' => 'confirm' );
		return;
	}
	// send: a real visitor (nonce, empty trap field, not instant), then keep, mail and reload
	$bot = ! empty( $_POST['hj_url'] ) || ( time() - (int) ( $_POST['hj_t'] ?? 0 ) ) < 3;
	if ( ! wp_verify_nonce( $_POST['_hjnonce'] ?? '', 'hj_form_' . $form ) || $bot ) {
		$GLOBALS['hj_form'] = $state + array( 'step' => 'input' );
		$GLOBALS['hj_form']['errors']['_'] = hj_t( '送信できませんでした。お手数ですが、もう一度お試しください。', 'Your message could not be sent. Please try again.' );
		return;
	}
	hj_form_deliver( $form, $values );
	wp_safe_redirect( add_query_arg( 'sent', '1', hj_switch_url( hj_lang() ) ) . '#form' );
	exit;
}, 4 );

/** Keeps the enquiry in お問い合わせ履歴 and sends the emails. */
function hj_form_deliver( string $form, array $values ): void {
	$GLOBALS['hj_form']['form'] = $form;
	$lines = array();
	foreach ( hj_form_fields( $form ) as $name => $f ) {
		$v = hj_form_display( $name, $values[ $name ] ?? '' );
		if ( '' !== $v && 'agree' !== $f[4] ) {
			$lines[] = '■ ' . $f[0] . "\n" . $v;
		}
	}
	$kind  = 'booking' === $form ? '商談予約' : ( hj_form_display( 'k', $values['k'] ?? '' ) ?: 'お問い合わせ' );
	$body  = implode( "\n\n", $lines ) . "\n\n---\n" . sprintf( '言語: %s / ページ: %s / 日時: %s', strtoupper( hj_lang() ), hj_switch_url( hj_lang() ), wp_date( 'Y-m-d H:i' ) );
	$title = sprintf( '[%s] %s／%s', $kind, $values['company'] ?? '', $values['name'] ?? '' );

	wp_insert_post( array( 'post_type' => 'hj_enquiry', 'post_status' => 'private', 'post_title' => $title, 'post_content' => $body ) );

	$to = array_filter( array_map( 'trim', explode( ',', (string) hj_opt_raw( 'mail_to' ) ) ), 'is_email' ) ?: array( get_option( 'admin_email' ) );
	wp_mail( $to, '【花印サイト】' . $title, $body, array( 'Reply-To: ' . $values['name'] . ' <' . $values['email'] . '>' ) );

	if ( hj_opt_raw( 'autoreply' ) && is_email( $values['email'] ?? '' ) ) {
		$pdf   = hj_file_url( hj_opt_raw( 'pdf_profile' ) );
		$reply = hj_t(
			$values['name'] . " 様\n\n花印粧業研究所株式会社です。お問い合わせありがとうございます。\n以下の内容で承りました。3営業日以内に担当者よりご連絡いたします。\n" . ( $pdf ? "\n会社案内（PDF）: " . $pdf . "\n" : '' ),
			'Dear ' . $values['name'] . ",\n\nThank you for contacting Hanajirushi Institute of Cosmetics. We have received your message below and will reply within 3 business days.\n" . ( $pdf ? "\nCompany profile (PDF): " . $pdf . "\n" : '' )
		);
		wp_mail( $values['email'], hj_t( '【花印】お問い合わせを受け付けました', 'Hanajirushi — we have received your message' ), $reply . "\n" . implode( "\n\n", $lines ) );
	}
}

/** Hidden fields every form sends: which form, step, nonce, the spam trap and the start time. */
function hj_form_hidden( string $form, string $step ): string {
	return '<input type="hidden" name="hj_form" value="' . esc_attr( $form ) . '"><input type="hidden" name="hj_step" value="' . esc_attr( $step ) . '">'
		. wp_nonce_field( 'hj_form_' . $form, '_hjnonce', false, false )
		. '<input type="hidden" name="hj_t" value="' . esc_attr( (string) ( $_POST['hj_t'] ?? time() ) ) . '">'
		. '<div class="hj-trap" aria-hidden="true"><label>URL<input type="text" name="hj_url" tabindex="-1" autocomplete="off"></label></div>';
}
