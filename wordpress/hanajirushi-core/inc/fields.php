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

/** Pages whose header (タイトルの横の写真) can be set in サイト設定: page key => name in the admin. */
const HJ_HEADER_PAGES = array(
	'brand'         => 'ブランド',
	'collaboration' => 'IPコラボレーション',
	'products'      => '製品一覧',
	'company'       => '会社概要',
	'rd'            => '研究開発・品質',
	'news'          => 'お知らせ',
	'partners'      => 'パートナーシップ',
	'exhibition'    => '展示会情報',
	'contact'       => 'お問い合わせ',
);

/** サイト設定 → ページ上部の画像: a photo and its focus for each page header. */
function hj_header_fields(): array {
	$out = array(
		hj_f( 'photos_note', '', 'message', array( 'message' => '<strong>写真は3つの形だけです。</strong>どの画面でも同じ形で表示されるので、1枚の写真がパソコンでもスマートフォンでも使えます。<br>'
			. '・16:9（横長）2400×1350px ／ ・4:5（縦長）1600×2000px ／ ・1:1（正方形）1600×1600px<br>'
			. 'JPG 300〜500KB、カラープロファイルは sRGB、文字は入れないでください。空欄の欄は今の写真のまま表示します。<br>'
			. '製品写真（1:1・白背景）は各製品の「アイキャッチ画像」、IPコラボの画像（1:1）は各IPコラボの「アイキャッチ画像」で設定します。' ) ),
		hj_f( 'header_note', '', 'message', array( 'message' => '<strong>■ ページ上部の写真（16:9）</strong><br>各ページのタイトルの横に表示する写真です。空欄のページは今の写真（写真のないページは写真なし）のまま表示します。<br>'
			. '写真は 16:9 の枠に表示され、パソコンでもスマートフォンでも全体が見えます（とても横長の大画面では上下が少しだけ切れます）。<br>'
			. '推奨：16:9、2400×1350px（最小 1920×1080px）、JPG 300〜500KB、カラープロファイルは sRGB。文字は入れないでください。<br>'
			. 'パソコンでは左端の約1/6、スマートフォンでは上端の約1/10を白くぼかして文字側になじませるため、そこには大事なものを置かないでください。' ) ),
	);
	foreach ( HJ_HEADER_PAGES as $key => $label ) {
		$out[] = hj_f( 'header_' . $key, $label, 'image', array( 'return_format' => 'id', 'preview_size' => 'medium', 'wrapper' => array( 'width' => '60' ) ) );
		$out[] = hj_f( 'header_' . $key . '_pos', '見せたい位置', 'select', array(
			'choices'       => array( 'center' => '中央', 'center top' => '上寄り', 'center bottom' => '下寄り', '30% center' => '左寄り', '70% center' => '右寄り' ),
			'default_value' => 'center',
			'wrapper'       => array( 'width' => '40' ),
			'instructions'  => '16:9 でない写真や、とても横長の画面で切り取られるときに残す位置。',
		) );
	}
	// v1.7: the brand header as a slideshow (client 2026-10-21)
	$out[] = hj_f( 'brand_slides', 'ブランドのヘッダー（スライドショー）', 'repeater', array(
		'instructions' => '2枚以上入れると、ブランドページのヘッダー写真がスライドショーになり、上の「ブランド」の写真より優先されます。'
			. '写真は 16:9（2400×1350px）、文字は写真に入れずに下の欄に入力します（写真の左側に表示、スマートフォンでは写真の下）。改行で2行に分けられます。',
		'layout'       => 'block',
		'max'          => 5,
		'button_label' => 'スライドを追加',
		'sub_fields'   => array(
			hj_f( 'image', '写真（16:9）', 'image', array( 'return_format' => 'id', 'preview_size' => 'medium', 'wrapper' => array( 'width' => '34' ) ), 'brand_slides' ),
			hj_f( 'copy', 'キャッチコピー', 'textarea', array( 'rows' => 2, 'new_lines' => '', 'wrapper' => array( 'width' => '33' ) ), 'brand_slides' ),
			hj_f( 'copy_en', 'キャッチコピー（英語）', 'textarea', array( 'rows' => 2, 'new_lines' => '', 'wrapper' => array( 'width' => '33' ) ), 'brand_slides' ),
			hj_f( 'sub', '製品名の行', 'text', array( 'instructions' => '例）花印 ハトムギスキンケア（前後の「—」は自動で付きます）', 'wrapper' => array( 'width' => '50' ) ), 'brand_slides' ),
			hj_f( 'sub_en', '製品名の行（英語）', 'text', array( 'wrapper' => array( 'width' => '50' ) ), 'brand_slides' ),
		),
	) );
	return $out;
}

/** Photos inside the pages (サイト設定 → 写真): slot => [admin label, shape, has a caption]. */
const HJ_PHOTOS = array(
	'home_company'        => array( 'トップ：会社情報', '4:5', false ),
	'brand_concept'       => array( 'ブランド：ブランドコンセプト', '4:5', false ),
	'brand_research'      => array( 'ブランド：研究への取り組み（円形）', '1:1', false ),
	'company_business_1'  => array( '会社概要：事業内容 一（研究開発）', '4:5', false ),
	'company_business_2'  => array( '会社概要：事業内容 二（製造）', '4:5', false ),
	'company_business_3'  => array( '会社概要：事業内容 三（販売・輸出入）', '4:5', false ),
	'company_office_main' => array( '会社概要：オフィス紹介 上段1（本社ビル）', '4:5', true ),
	'company_office_p2'   => array( '会社概要：オフィス紹介 上段2', '4:5', true ),
	'company_office_p3'   => array( '会社概要：オフィス紹介 上段3', '4:5', true ),
	'company_office_w1'   => array( '会社概要：オフィス紹介 下段1', '16:9', true ),
	'company_office_w2'   => array( '会社概要：オフィス紹介 下段2', '16:9', true ),
	'company_office_w3'   => array( '会社概要：オフィス紹介 下段3', '16:9', true ),
	'rd_lab'              => array( '研究開発・品質：研究室（円形）', '1:1', false ),
	'product_lab'         => array( '製品ページ（全製品共通）：研究室（円形）', '1:1', false ),
);
const HJ_SHAPES = array( '16:9' => '2400×1350px', '4:5' => '1600×2000px', '1:1' => '1600×1600px' );

/** サイト設定 → 写真: the photos inside the pages, each with its shape in the label. */
function hj_photo_fields(): array {
	$out = array(
		hj_f( 'photo_note', '', 'message', array( 'message' => '<strong>■ ページ内の写真</strong><br>形と大きさは各欄の名前のとおりです。4:5 の写真は上部が丸く、1:1 の写真は円形に切り取られるので、主役は中央に置いてください。' ) ),
	);
	foreach ( HJ_PHOTOS as $slot => $p ) {
		$out[] = hj_f( 'photo_' . $slot, $p[0] . '（' . $p[1] . '・' . HJ_SHAPES[ $p[1] ] . '）', 'image', array( 'return_format' => 'id', 'preview_size' => 'medium', 'wrapper' => array( 'width' => $p[2] ? '40' : '100' ) ) );
		if ( $p[2] ) {
			$out[] = hj_f( 'photo_' . $slot . '_cap', '写真の説明', 'text', array( 'wrapper' => array( 'width' => '30' ), 'instructions' => '空欄なら今の説明のまま。' ) );
			$out[] = hj_f( 'photo_' . $slot . '_cap_en', '写真の説明（英語）', 'text', array( 'wrapper' => array( 'width' => '30' ) ) );
		}
	}
	return $out;
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
				hj_f( 'rakuten_code', '楽天市場の商品コード', 'text', array( 'instructions' => '日本語ページの「この製品を購入する」で選べるストアのうち、楽天市場の商品ページに使います（英語ページには購入ボタンを表示しません）。例）10001008-set' ) ),
				hj_f( 'amazon_url', 'Amazon の商品ページ', 'url', array( 'placeholder' => 'https://www.amazon.co.jp/…', 'instructions' => '空欄のストアは、確認用サイトでは「要確認」、公開サイトでは表示しません。' ) ),
				hj_f( 'yahoo_url', 'Yahoo!ショッピングの商品ページ', 'url', array( 'placeholder' => 'https://store.shopping.yahoo.co.jp/…' ) ),
				hj_f( 'qoo10_url', 'Qoo10 の商品ページ', 'url', array( 'placeholder' => 'https://www.qoo10.jp/…' ) ),
				hj_f( 'image_temp', '仮の製品画像URL', 'url', array( 'instructions' => 'アイキャッチ画像が未設定の間だけ使います。正式な製品写真はアイキャッチ画像に設定してください。' ) ),
			),
			array( hj_tab( 'product_ja', '日本語' ) ), $lang_fields( '' ),
			array( hj_tab( 'product_en', 'English' ) ), $lang_fields( '_en' ),
			array( hj_tab( 'product_trade', '取引情報' ),
				hj_f( 'jan', 'JANコード', 'text' ),
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
				hj_f( 'visual', '右側の画像', 'select', array( 'choices' => array( 'none' => 'なし（背景写真だけ）', 'product' => '製品（円窓）', 'products' => '製品3点（パネル）', 'kanji' => '漢字（円窓）', 'banner' => 'バナー画像（背景写真をそのまま表示）' ), 'default_value' => 'none',
					'instructions' => 'バナー画像：背景写真を色そのままで表示し、スマートフォンでは文字の上に写真として表示します。本文の1行目は製品名として表示されます。' ) ),
				hj_f( 'product', '製品', 'post_object', array( 'post_type' => array( 'product' ), 'return_format' => 'id', 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'product' ) ) ) ) ),
				hj_f( 'products', '製品（3点まで）', 'relationship', array( 'post_type' => array( 'product' ), 'max' => 3, 'return_format' => 'id', 'filters' => array( 'search' ), 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'products' ) ) ) ) ),
				hj_f( 'kanji', '漢字（1〜2文字）', 'text', array( 'maxlength' => 2, 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'kanji' ) ) ) ) ),
				hj_f( 'kanji_en', '英語ページで漢字の代わりに出す語（例：Hong Kong）', 'text', array( 'maxlength' => 12, 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'kanji' ) ) ) ) ),
				hj_f( 'kanji_caption', '漢字の下の英字', 'text', array( 'maxlength' => 20, 'conditional_logic' => array( array( array( 'field' => 'field_hj_slide_visual', 'operator' => '==', 'value' => 'kanji' ) ) ) ) ),
				hj_f( 'seal', '落款（1〜2文字）', 'text', array( 'maxlength' => 2, 'instructions' => '任意。画像に押す赤い印（例：特許）。' ) ),
				hj_f( 'bg', '背景写真', 'image', array( 'return_format' => 'id', 'preview_size' => 'medium', 'instructions' => '横長の写真（幅2000px程度）。空欄なら淡い無地。' ) ),
				hj_f( 'bg_pos', '背景写真の位置', 'select', array( 'choices' => array( 'center' => '中央', '70% center' => 'やや右', '30% center' => 'やや左', 'center 40%' => 'やや上', 'center 70%' => 'やや下' ), 'default_value' => 'center' ) ),
				hj_f( 'btn1_link', 'ボタンのリンク先', 'text', array( 'placeholder' => '/products/', 'instructions' => 'サイト内は「/products/」のように入力（英語ページでは自動で /en/ が付きます）。外部サイトは https:// から。' ) ),
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
			array( hj_tab( 'settings_msg', '代表メッセージ' ),
				hj_f( 'message_lead', '見出し', 'text', array( 'instructions' => '本文の最初に大きく表示する一文。' ) ),
				hj_f( 'message_lead_en', '見出し（英語）', 'text' ),
				hj_f( 'message', '本文', 'textarea', array( 'rows' => 10, 'new_lines' => '', 'instructions' => '段落の間は1行あけてください。代表者の氏名は表示しません（役職のみ）。' ) ),
				hj_f( 'message_en', '本文（英語）', 'textarea', array( 'rows' => 10, 'new_lines' => '' ) ),
				hj_f( 'rep_title', '役職', 'text' ),
				hj_f( 'rep_title_en', '役職（英語）', 'text' ),
			),
			array( hj_tab( 'settings_hist', '沿革' ),
				hj_f( 'show_history', '表示', 'true_false', array( 'ui' => 1, 'message' => '会社概要ページに沿革を表示する（現在は保留中のため非表示）' ) ),
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
			array( hj_tab( 'settings_photos', '写真' ) ), hj_header_fields(), hj_photo_fields(),
			array( hj_tab( 'settings_film', 'ブランドムービー' ),
				hj_f( 'film', '動画ファイル（MP4）', 'file', array( 'return_format' => 'id', 'mime_types' => 'mp4,webm',
					'instructions' => 'トップページのブランド欄の下に表示します。再生ボタンを押したときだけ読み込み、音声付きで再生します。上下に黒帯のある横長の映像（約2.5:1）は、黒帯を切って表示します。' ) ),
				hj_f( 'film_url', '動画のURL', 'url', array( 'instructions' => '動画ファイルをメディアに置けない場合のみ。ファイルとURLがどちらも空欄なら、ムービー欄は表示しません。' ) ),
				hj_f( 'film_poster', '再生前に表示する場面（秒）', 'number', array( 'default_value' => 12, 'min' => 0, 'step' => 0.5 ) ),
				hj_f( 'film_title', 'タイトル', 'text' ),
				hj_f( 'film_title_en', 'タイトル（英語）', 'text' ),
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
