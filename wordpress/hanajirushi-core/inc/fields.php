<?php
/**
 * Edit screens, defined in code with Secure Custom Fields (free, WordPress.org).
 *
 * Every text a visitor reads exists twice: the Japanese field (name) and the English field
 * (name_en), on 日本語 / English tabs. The Japanese product name is the post title; the
 * English one is `title_en`. A product, slide, IP collaboration or news item with an empty
 * English title is left out of the English site.
 *
 * Defined in code, not in the SCF screens, so the structure travels with the plugin.
 */

defined( 'ABSPATH' ) || exit;

/**
 * One field. Keys are field_hj_<group>_<name> (unique across the site; the group is set with
 * hj_fgroup() before a group's fields are built); sub-fields add the parent's name.
 */
function hj_f( string $name, string $label, string $type = 'text', array $extra = array(), string $prefix = '' ): array {
	return array_merge( array(
		'key'   => 'field_hj_' . ( $GLOBALS['hj_fgroup'] ?? '' ) . '_' . ( $prefix ? $prefix . '_' : '' ) . $name,
		'name'  => $name,
		'label' => $label,
		'type'  => $type,
	), $extra );
}

function hj_fgroup( string $g ): void {
	$GLOBALS['hj_fgroup'] = $g;
}

function hj_tab( string $key, string $label ): array {
	return array( 'key' => 'field_hj_tab_' . $key, 'label' => $label, 'name' => '', 'type' => 'tab', 'placement' => 'top' );
}

/** "One per line" text area. */
function hj_lines_field( string $name, string $label, string $hint = '1行に1つ入力します。' ): array {
	return hj_f( $name, $label, 'textarea', array( 'rows' => 3, 'new_lines' => '', 'instructions' => $hint ) );
}

function hj_points_field( string $name, string $label ): array {
	return hj_f( $name, $label, 'repeater', array(
		'instructions' => '製品ページの「製品の特長」。3つが基本です。',
		'layout'       => 'block',
		'max'          => 4,
		'button_label' => '特長を追加',
		'sub_fields'   => array(
			hj_f( 'title', '見出し', 'text', array( 'maxlength' => 40 ), $name ),
			hj_f( 'text', '説明', 'textarea', array( 'rows' => 2, 'new_lines' => '' ), $name ),
		),
	) );
}

const HJ_CATS = array(
	'cleansing' => array( 'クレンジング', 'Cleansing' ),
	'lotion'    => array( '化粧水・美容液', 'Lotions & serums' ),
	'cream'     => array( 'クリーム・ジェル', 'Creams & gels' ),
	'mask'      => array( 'マスク・パック', 'Masks & packs' ),
	'uv'        => array( 'UV・化粧下地', 'UV & primer' ),
	'mens'      => array( 'メンズ', 'Men' ),
);
const HJ_SERIES = array(
	'hatomugi' => array( 'ハトムギシリーズ', 'Hatomugi series' ),
	'amino'    => array( 'アミノ酸保湿シリーズ', 'Amino acid series' ),
);
const HJ_KINDS = array(
	'cosmetic' => array( '化粧品', 'Cosmetic' ),
	'quasi'    => array( '医薬部外品', 'Quasi-drug' ),
);

function hj_choices( array $map, bool $empty = false ): array {
	$out = $empty ? array( '' => '—' ) : array();
	foreach ( $map as $k => $v ) {
		$out[ $k ] = $v[0];
	}
	return $out;
}

add_action( 'acf/include_fields', function () {
	if ( ! function_exists( 'acf_add_local_field_group' ) ) {
		return;
	}

	// ------------------------------------------------------------------ 製品
	hj_fgroup( 'product' );
	$lang_fields = function ( string $sfx ) {
		$en = '_en' === $sfx;
		return array(
			$en ? hj_f( 'title_en', '製品名（英語）', 'text', array( 'instructions' => '空欄の場合、この製品は英語サイトに表示されません。' ) ) : null,
			hj_f( 'sub' . $sfx, $en ? 'サブタイトル（英語ページ）' : 'サブタイトル', 'text', array( 'instructions' => $en ? '製品名の下に小さく表示。通常は日本語の製品名。' : '製品名の下に小さく表示。通常は英語名。' ) ),
			hj_f( 'short' . $sfx, '一覧用の説明（1文）', 'textarea', array( 'rows' => 2, 'new_lines' => '', 'maxlength' => $en ? 130 : 60 ) ),
			hj_f( 'catch' . $sfx, 'キャッチコピー', 'textarea', array( 'rows' => 2, 'new_lines' => '', 'instructions' => '改行した位置で行が分かれます（2行まで）。' ) ),
			hj_f( 'desc' . $sfx, '説明文', 'textarea', array( 'rows' => 4, 'new_lines' => '' ) ),
			hj_lines_field( 'badges' . $sfx, '特徴ラベル', '製品名の下の枠付きラベル。1行に1つ。' ),
			hj_lines_field( 'free' . $sfx, '処方の特徴（〇〇フリーなど）', '1行に1つ。' ),
			hj_points_field( 'points' . $sfx, '製品の特長' ),
			hj_f( 'usage' . $sfx, '使い方', 'textarea', array( 'rows' => 3, 'new_lines' => '' ) ),
			hj_f( 'inci' . $sfx, $en ? '全成分（英文 INCI 表記）' : '全成分', 'textarea', array( 'rows' => 4, 'new_lines' => '', 'instructions' => $en ? '空欄の場合、英語ページには日本語の全成分を参考として表示します。' : '' ) ),
		);
	};
	acf_add_local_field_group( array(
		'key'      => 'group_hj_product',
		'title'    => '製品の内容',
		'location' => array( array( array( 'param' => 'post_type', 'operator' => '==', 'value' => 'product' ) ) ),
		'position' => 'acf_after_title',
		'style'    => 'seamless',
		'fields'   => array_values( array_filter( array_merge(
			array( hj_tab( 'product_basic', '基本情報' ),
				hj_f( 'category', 'カテゴリー', 'select', array( 'choices' => hj_choices( HJ_CATS ), 'required' => 1 ) ),
				hj_f( 'series', 'シリーズ', 'select', array( 'choices' => hj_choices( HJ_SERIES, true ), 'allow_null' => 1 ) ),
				hj_f( 'size', '内容量', 'text', array( 'placeholder' => '例）500mL' ) ),
				hj_f( 'kind', '区分', 'select', array( 'choices' => hj_choices( HJ_KINDS ), 'default_value' => 'cosmetic' ) ),
				hj_f( 'is_new', '新商品', 'true_false', array( 'ui' => 1, 'message' => '「新商品」のラベルを付ける' ) ),
				hj_f( 'coming_soon', '近日公開', 'true_false', array( 'ui' => 1, 'message' => '一覧に「近日公開」として表示し、製品ページは作らない' ) ),
				hj_f( 'show_on_home', 'トップページに表示', 'true_false', array( 'ui' => 1 ) ),
				hj_f( 'rakuten_code', '楽天市場の商品コード', 'text', array( 'instructions' => '日本語ページの「楽天市場で購入する」ボタンに使います（英語ページには表示しません）。例）10001008-set' ) ),
				hj_f( 'image_temp', '仮の製品画像URL', 'url', array( 'instructions' => 'アイキャッチ画像が未設定の間だけ使います。正式な製品写真はアイキャッチ画像に設定してください。' ) ),
			),
			array( hj_tab( 'product_ja', '日本語' ) ), $lang_fields( '' ),
			array( hj_tab( 'product_en', 'English' ) ), $lang_fields( '_en' ),
			array( hj_tab( 'product_trade', '取引情報' ),
				hj_f( 'shelf_unopened', '使用期限（未開封）', 'text' ),
				hj_f( 'shelf_opened', '使用期限（開封後）', 'text' ),
				hj_f( 'jan', 'JANコード', 'text' ),
				hj_f( 'case_pack', '入数・ケースサイズ', 'text' ),
				hj_f( 'maker', '製造販売元', 'text' ),
				hj_f( 'cautions', '使用上の注意', 'textarea', array( 'rows' => 3, 'new_lines' => '' ) ),
				hj_f( 'cautions_en', '使用上の注意（英語）', 'textarea', array( 'rows' => 3, 'new_lines' => '' ) ),
			)
		) ) ),
	) );

	// ------------------------------------------------------------------ トップスライド
	hj_fgroup( 'slide' );
	$slide_lang = function ( string $sfx ) {
		$en = '_en' === $sfx;
		return array(
			$en ? hj_f( 'title_en', 'タブの文字（英語）', 'text', array( 'maxlength' => 24, 'instructions' => 'スライド下のタブ。空欄の場合、このスライドは英語サイトに表示されません。' ) )
				: hj_f( 'tab', 'タブの文字', 'text', array( 'maxlength' => 12, 'instructions' => 'スライド下のタブ。空欄ならタイトルを使います。' ) ),
			hj_f( 'label' . $sfx, 'ラベル', 'text', array( 'maxlength' => $en ? 16 : 8, 'instructions' => '見出しの上の小さな赤いラベル（例：新商品、特許、展示会）。空欄なら「英字の小見出し」を表示。' ) ),
			hj_f( 'heading' . $sfx, '見出し', 'textarea', array( 'rows' => 3, 'new_lines' => '', 'instructions' => $en ? '1行ずつ改行して入力（3行まで、1行32文字まで）。' : '1行ずつ改行して入力（3行まで、1行14文字まで）。' ) ),
			hj_f( 'accent' . $sfx, '2行目の色', 'true_false', array( 'ui' => 1, 'default_value' => 1, 'message' => '見出しの2行目をアクセント色にする' ) ),
			hj_f( 'text' . $sfx, '本文', 'textarea', array( 'rows' => 2, 'new_lines' => '', 'maxlength' => $en ? 130 : 60 ) ),
			hj_f( 'btn1' . $sfx, 'ボタンの文字', 'text', array( 'maxlength' => $en ? 24 : 12 ) ),
			hj_f( 'btn2' . $sfx, '2つ目のリンクの文字', 'text', array( 'maxlength' => $en ? 24 : 12, 'instructions' => '任意。ボタンの横に文字リンクとして表示。' ) ),
		);
	};
	acf_add_local_field_group( array(
		'key'      => 'group_hj_slide',
		'title'    => 'スライドの内容',
		'location' => array( array( array( 'param' => 'post_type', 'operator' => '==', 'value' => 'kv_slide' ) ) ),
		'position' => 'acf_after_title',
		'style'    => 'seamless',
		'fields'   => array_values( array_filter( array_merge(
			array( hj_tab( 'slide_ja', '日本語' ) ), $slide_lang( '' ),
			array( hj_tab( 'slide_en', 'English' ) ), $slide_lang( '_en' ),
			array( hj_tab( 'slide_look', '画像・リンク' ),
				hj_f( 'eyebrow', '英字の小見出し', 'text', array( 'instructions' => 'ラベルが空欄のときに表示（例：Hanajirushi · Ginza, Tokyo）。' ) ),
				hj_f( 'visual', '右側の画像', 'select', array( 'choices' => array( 'none' => 'なし（背景写真だけ）', 'product' => '製品（円窓）', 'products' => '製品3点（パネル）', 'kanji' => '漢字（円窓）' ), 'default_value' => 'none' ) ),
				hj_f( 'product', '製品', 'post_object', array( 'post_type' => array( 'product' ), 'return_format' => 'id', 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'product' ) ) ) ) ),
				hj_f( 'products', '製品（3点まで）', 'relationship', array( 'post_type' => array( 'product' ), 'max' => 3, 'return_format' => 'id', 'filters' => array( 'search' ), 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'products' ) ) ) ) ),
				hj_f( 'kanji', '漢字（1〜2文字）', 'text', array( 'maxlength' => 2, 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'kanji' ) ) ) ) ),
				hj_f( 'kanji_caption', '漢字の下の英字', 'text', array( 'maxlength' => 20, 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'kanji' ) ) ) ) ),
				hj_f( 'seal', '落款（1〜2文字）', 'text', array( 'maxlength' => 2, 'instructions' => '任意。画像に押す赤い印（例：特許）。' ) ),
				hj_f( 'bg', '背景写真', 'image', array( 'return_format' => 'id', 'preview_size' => 'medium', 'instructions' => '横長の写真（幅2000px程度）。空欄なら淡い無地。' ) ),
				hj_f( 'bg_pos', '背景写真の位置', 'select', array( 'choices' => array( 'center' => '中央', '70% center' => 'やや右', '30% center' => 'やや左', 'center 40%' => 'やや上', 'center 70%' => 'やや下' ), 'default_value' => 'center' ) ),
				hj_f( 'btn1_link', 'ボタンのリンク先', 'text', array( 'placeholder' => '/products/', 'instructions' => 'サイト内は「/products/」のように入力（英語ページでは自動で /en/ が付きます）。外部サイトは https:// から。' ) ),
				hj_f( 'btn2_link', '2つ目のリンク先', 'text', array( 'placeholder' => '/brand/' ) ),
				hj_f( 'start', '表示開始日', 'date_picker', array( 'display_format' => 'Y/m/d', 'return_format' => 'Ymd', 'instructions' => '任意。' ) ),
				hj_f( 'end', '表示終了日', 'date_picker', array( 'display_format' => 'Y/m/d', 'return_format' => 'Ymd', 'instructions' => '任意。この日を過ぎると自動で非表示（例：展示会の終了日）。' ) ),
			)
		) ) ),
	) );

	// ------------------------------------------------------------------ IPコラボ
	hj_fgroup( 'collab' );
	acf_add_local_field_group( array(
		'key'      => 'group_hj_collab',
		'title'    => 'IPコラボの内容',
		'location' => array( array( array( 'param' => 'post_type', 'operator' => '==', 'value' => 'collab' ) ) ),
		'position' => 'acf_after_title',
		'style'    => 'seamless',
		'fields'   => array(
			hj_tab( 'collab_ja', '日本語' ),
			hj_f( 'product', '商品', 'text', array( 'placeholder' => '例）クレンジングローション' ) ),
			hj_f( 'label', 'ラベル', 'text', array( 'maxlength' => 8, 'placeholder' => '例）中国限定、専売品、販売終了' ) ),
			hj_f( 'channel', '販売', 'text' ),
			hj_tab( 'collab_en', 'English' ),
			hj_f( 'title_en', 'IP名（英語）', 'text', array( 'instructions' => '空欄の場合、英語サイトに表示されません。' ) ),
			hj_f( 'product_en', '商品（英語）', 'text' ),
			hj_f( 'label_en', 'ラベル（英語）', 'text', array( 'maxlength' => 16 ) ),
			hj_f( 'channel_en', '販売（英語）', 'text' ),
		),
	) );

	// ------------------------------------------------------------------ お知らせ（投稿）の英語欄
	hj_fgroup( 'post' );
	acf_add_local_field_group( array(
		'key'      => 'group_hj_post_en',
		'title'    => 'English（英語サイト）',
		'location' => array( array( array( 'param' => 'post_type', 'operator' => '==', 'value' => 'post' ) ) ),
		'position' => 'normal',
		'fields'   => array(
			hj_f( 'title_en', 'タイトル（英語）', 'text', array( 'instructions' => '空欄の場合、このお知らせは英語サイトに表示されません。' ) ),
			hj_f( 'body_en', '本文（英語）', 'wysiwyg', array( 'tabs' => 'visual', 'toolbar' => 'basic', 'media_upload' => 0 ) ),
		),
	) );

	// ------------------------------------------------------------------ サイト設定
	hj_fgroup( 'settings' );
	$co = function ( string $sfx ) {
		$en = '_en' === $sfx;
		return array(
			hj_f( 'company' . $sfx, '会社名', 'text' ),
			hj_f( 'address' . $sfx, '住所', 'textarea', array( 'rows' => 2, 'new_lines' => '', 'instructions' => $en ? '英語の住所（銀座から）。' : '郵便番号から。改行した位置で行が分かれます。' ) ),
			hj_f( 'tel' . $sfx, '電話番号', 'text', array( 'placeholder' => $en ? '+81-3-6264-2154' : '03-6264-2154' ) ),
			hj_f( 'fax' . $sfx, 'FAX', 'text' ),
			hj_f( 'hours' . $sfx, '受付時間', 'text' ),
			hj_f( 'founded' . $sfx, '創業', 'text' ),
		);
	};
	acf_add_local_field_group( array(
		'key'      => 'group_hj_settings',
		'title'    => 'サイト設定',
		'location' => array( array( array( 'param' => 'options_page', 'operator' => '==', 'value' => 'hj-settings' ) ) ),
		'style'    => 'seamless',
		'fields'   => array_merge(
			array( hj_tab( 'settings_ja', '会社情報（日本語）' ) ), $co( '' ),
			array( hj_tab( 'settings_en', '会社情報（English）' ) ), $co( '_en' ),
			array( hj_tab( 'settings_rows', '会社概要の表' ),
				hj_pairs_field( 'profile_rows', '会社概要の表', '会社概要ページの表。英語の項目名が空欄の行は英語ページに表示しません（資本金・取引銀行など）。', 'label', '項目', 'value', '内容' ),
			),
			array( hj_tab( 'settings_msg', '代表挨拶' ),
				hj_f( 'message', '代表挨拶', 'textarea', array( 'rows' => 6, 'new_lines' => '' ) ),
				hj_f( 'message_en', '代表挨拶（英語）', 'textarea', array( 'rows' => 6, 'new_lines' => '', 'instructions' => '空欄の場合、英語ページでは日本語の本文の代わりに準備中の表示になります。' ) ),
				hj_f( 'rep_title', '役職', 'text' ),
				hj_f( 'rep_title_en', '役職（英語）', 'text' ),
				hj_f( 'rep_name', '氏名', 'text' ),
				hj_f( 'rep_name_en', '氏名（英語）', 'text' ),
				hj_f( 'rep_photo', '代表者写真', 'image', array( 'return_format' => 'id', 'preview_size' => 'medium', 'instructions' => '縦長（3:4程度）。未設定の間は落款と「代表者写真」の枠を表示します。' ) ),
			),
			array( hj_tab( 'settings_hist', '沿革' ),
				hj_pairs_field( 'history', '沿革', '上から古い順に表示します。', 'date', '年月', 'text', '出来事' ),
			),
			array( hj_tab( 'settings_terms', '取引条件' ),
				hj_pairs_field( 'terms', '取引条件', 'パートナー募集ページ・展示会商談ページに表示します。', 'label', '項目', 'value', '内容' ),
			),
			array( hj_tab( 'settings_faq', 'よくあるご質問' ),
				hj_pairs_field( 'faq', 'よくあるご質問', 'パートナー募集ページに表示します。最初の質問は開いた状態で表示されます。', 'q', '質問', 'a', '回答' ),
			),
			array( hj_tab( 'settings_access', 'アクセス' ),
				hj_f( 'stations', '最寄駅', 'textarea', array( 'rows' => 3, 'new_lines' => '' ) ),
				hj_f( 'stations_en', '最寄駅（英語）', 'textarea', array( 'rows' => 3, 'new_lines' => '' ) ),
			),
			array( hj_tab( 'settings_show', '展示会担当' ),
				hj_f( 'show_contact', '担当者', 'text', array( 'instructions' => '展示会の商談ページに表示する連絡先。' ) ),
				hj_f( 'show_whatsapp', 'WhatsApp', 'text' ),
				hj_f( 'show_wechat', 'WeChat ID', 'text' ),
				hj_f( 'show_email', 'メール', 'text' ),
				hj_f( 'qr_wechat', 'WeChat の QR コード', 'image', array( 'return_format' => 'id', 'preview_size' => 'thumbnail' ) ),
				hj_f( 'qr_whatsapp', 'WhatsApp の QR コード', 'image', array( 'return_format' => 'id', 'preview_size' => 'thumbnail' ) ),
				hj_f( 'pdf_profile', '会社案内（PDF）', 'file', array( 'return_format' => 'id', 'mime_types' => 'pdf', 'instructions' => '商談ページの「資料ダウンロード」と、お問い合わせの自動返信メールに使います。' ) ),
				hj_f( 'pdf_catalog', '製品カタログ（PDF）', 'file', array( 'return_format' => 'id', 'mime_types' => 'pdf' ) ),
			),
			array( hj_tab( 'settings_mail', 'お問い合わせ' ),
				hj_f( 'mail_to', '通知先メールアドレス', 'text', array( 'instructions' => 'お問い合わせ・商談予約の通知先。複数はカンマ区切り。空欄の場合はサイト管理者のメールアドレス。送信内容は「お問い合わせ履歴」にも保存されます。' ) ),
				hj_f( 'autoreply', '自動返信', 'true_false', array( 'ui' => 1, 'default_value' => 1, 'message' => '送信者に受付確認メールを送る（会社案内PDFがあればリンクを付けます）' ) ),
			),
			array( hj_tab( 'settings_site', '表示' ),
				hj_f( 'show_tbc', '要確認マーク', 'true_false', array( 'ui' => 1, 'message' => '未確認の項目に「要確認」マークを表示する（確認用サイトのみ。公開前にオフ）',
					'instructions' => 'どの入力欄でも［要確認］や［氏名］のように全角の角かっこで囲んだ部分が、確認用マークになります。オフにすると表示されません。' ) ),
			)
		),
	) );

	// ------------------------------------------------------------------ 展示会
	hj_fgroup( 'exhibition' );
	$ex = function ( string $name, string $label, string $type = 'text', array $extra = array() ) {
		return array( hj_f( $name, $label, $type, $extra ), hj_f( $name . '_en', $label . '（英語）', $type, $extra ) );
	};
	acf_add_local_field_group( array(
		'key'      => 'group_hj_exhibition',
		'title'    => '展示会の内容',
		'location' => array( array( array( 'param' => 'post_type', 'operator' => '==', 'value' => 'exhibition' ) ) ),
		'position' => 'acf_after_title',
		'style'    => 'seamless',
		'fields'   => array_merge(
			array(
				hj_f( 'title_en', '展示会名（英語）', 'text', array( 'instructions' => '空欄の場合、英語サイトに表示されません。' ) ),
				hj_f( 'year', '年', 'text', array( 'placeholder' => '2026' ) ),
			),
			$ex( 'month', '月', 'text', array( 'placeholder' => '11月 / Nov' ) ),
			$ex( 'dates', '会期' ),
			$ex( 'venue', '会場' ),
			$ex( 'booth', 'ブース' ),
			$ex( 'onshow', '出展内容', 'textarea', array( 'rows' => 2, 'new_lines' => '' ) ),
			$ex( 'languages', '対応言語' ),
			$ex( 'status', '状況ラベル', 'text', array( 'placeholder' => '商談予約受付中' ) ),
			array(
				hj_f( 'page', '専用ページ', 'text', array( 'placeholder' => '/cosmoprof-asia/', 'instructions' => '商談予約ページのアドレス（任意）。' ) ),
				hj_f( 'end', '最終日', 'date_picker', array( 'display_format' => 'Y/m/d', 'return_format' => 'Ymd', 'instructions' => 'この日を過ぎると「過去の出展」に移ります。' ) ),
			)
		),
	) );
} );

/** A repeater of label/value pairs in both languages (company table, history, terms, FAQ). */
function hj_pairs_field( string $name, string $label, string $hint, string $a, string $a_label, string $b, string $b_label ): array {
	return hj_f( $name, $label, 'repeater', array(
		'instructions' => $hint,
		'layout'       => 'table',
		'button_label' => '行を追加',
		'sub_fields'   => array(
			hj_f( $a, $a_label, 'text', array(), $name ),
			hj_f( $b, $b_label, 'textarea', array( 'rows' => 2, 'new_lines' => '' ), $name ),
			hj_f( $a . '_en', $a_label . '（英語）', 'text', array(), $name ),
			hj_f( $b . '_en', $b_label . '（英語）', 'textarea', array( 'rows' => 2, 'new_lines' => '' ), $name ),
		),
	) );
}

add_action( 'acf/init', function () {
	if ( function_exists( 'acf_add_options_page' ) ) {
		acf_add_options_page( array(
			'page_title' => 'サイト設定',
			'menu_title' => 'サイト設定',
			'menu_slug'  => 'hj-settings',
			'capability' => 'edit_pages',
			'icon_url'   => 'dashicons-admin-site-alt3',
			'position'   => 59,
			'redirect'   => false,
		) );
	}
} );

// Without Secure Custom Fields the edit screens are missing: say so.
add_action( 'admin_notices', function () {
	if ( ! function_exists( 'acf_add_local_field_group' ) && current_user_can( 'activate_plugins' ) ) {
		echo '<div class="notice notice-error"><p><b>花印 HANAJIRUSHI Core:</b> プラグイン「Secure Custom Fields」を有効にしてください（プラグイン → 新規追加 で検索できます）。製品やスライドの入力欄はこのプラグインで表示します。</p></div>';
	}
} );
