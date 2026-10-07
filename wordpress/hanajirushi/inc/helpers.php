<?php
/**
 * Small pieces of markup the design repeats (the mockup's eb(), shd(), lines(), lnk(),
 * btn(), seal(), win() … in mockup/_build/build_premium.py). They return HTML strings.
 * Arguments that are fixed copy are trusted HTML; anything typed by staff is escaped by
 * the caller or with hj_text().
 */

defined( 'ABSPATH' ) || exit;

const HJ_ARR = '<svg class="arr" viewBox="0 0 40 10" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true"><path d="M0 5h38M33 1l5 4-5 4"/></svg>';
const HJ_UP  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg>';

/** URL of a file in the theme's assets/img. */
function hj_img( string $file ): string {
	return get_template_directory_uri() . '/assets/img/' . $file;
}

/** Staff-typed text: escaped, new lines kept as <br>. */
function hj_text( $s ): string {
	return hj_marks( implode( '<br>', array_map( 'esc_html', preg_split( '/\R/u', trim( (string) $s ) ) ) ) );
}

/**
 * Fixed page copy shared with the mockup (inc/copy.json, made by wordpress/dev/sync.py from
 * mockup/_build/build.py): the item in the language being shown, ［…］ marks applied.
 */
function hj_c( string $key ) {
	static $copy = null;
	if ( null === $copy ) {
		$copy = json_decode( (string) file_get_contents( get_template_directory() . '/inc/copy.json' ), true ) ?: array();
	}
	$m = function ( $x ) use ( &$m ) {
		return is_array( $x ) ? array_map( $m, $x ) : ( is_string( $x ) ? hj_marks( $x ) : $x );
	};
	return $m( $copy[ hj_lang() ][ $key ] ?? '' );
}

/** The 花印 seal (落款). */
function hj_seal( string $txt = '花印', string $cls = '' ): string {
	// Only the official logo may stand for 花印 (client, 2026-10-07): the square mark, with the
	// white-square version for the crimson contact band (premium-v14.css picks one).
	if ( '花印' === $txt ) {
		return '<span class="seal seal--logo ' . esc_attr( $cls ) . '" aria-hidden="true"><img class="lm" src="' . esc_url( hj_img( 'logo_mark.png' ) ) . '" alt="">'
			. '<img class="lm-w" src="' . esc_url( hj_img( 'logo_mark_w.png' ) ) . '" alt=""></span>';
	}
	return '<span class="seal ' . esc_attr( $cls ) . '" aria-hidden="true"><span>' . $txt . '</span></span>';
}

/** Small Latin label above a heading, with its section number. */
function hj_eb( string $word, string $num = '' ): string {
	return '<p class="eb">' . ( $num ? '<i>' . $num . '</i>' : '' ) . '<span>' . $word . '</span></p>';
}

/**
 * One masked span per heading line (split on <br>), so lines can be revealed in turn
 * (premium-v11). An <em> that runs across a break is closed and reopened.
 */
function hj_lines( string $html ): string {
	$html  = str_replace( '<em>HANAJIRUSHI', '<em>Hanajirushi', $html );
	$out   = '';
	$carry = false;
	foreach ( explode( '<br>', $html ) as $i => $seg ) {
		if ( $carry ) {
			$seg = '<em>' . $seg;
		}
		$carry = substr_count( $seg, '<em>' ) > substr_count( $seg, '</em>' );
		if ( $carry ) {
			$seg .= '</em>';
		}
		$out .= '<span class="ln" style="--i:' . $i . '"><span>' . $seg . '</span></span>';
	}
	return $out;
}

/**
 * A staff-typed heading (one line per row) as heading HTML: line 2 in the accent colour
 * when $accent, and in Japanese, Latin words (e.g. Cosmoprof Asia 2026) set in Bodoni and
 * kept together with the next character.
 */
function hj_heading( $text, bool $accent ): string {
	$out = array();
	foreach ( hj_split_lines( $text ) as $i => $line ) {
		$line = esc_html( $line );
		if ( ! hj_is_en() ) {
			$line = preg_replace( '/([A-Za-z0-9][A-Za-z0-9 .\-]*[A-Za-z0-9])(\S?)/u', '<span class="nw"><span class="lat">$1</span>$2</span>', $line );
		}
		$out[] = ( $accent && 1 === $i ) ? '<em>' . $line . '</em>' : $line;
	}
	return hj_lines( implode( '<br>', $out ) );
}

/** Section heading: Japanese title in Mincho; English title in Bodoni with a small kanji accent. */
function hj_shd( string $num, string $word, string $ja, string $en, ?string $kj = null, ?string $lead = null, string $cls = '' ): string {
	$k = ( hj_is_en() && $kj ) ? '<p class="kj">' . $kj . '</p>' : '';
	$l = $lead ? '<p class="lead">' . $lead . '</p>' : '';
	return '<div class="shd ' . $cls . '">' . hj_eb( $word, $num ) . '<h2 class="h2">' . hj_lines( hj_t( $ja, $en ) ) . '</h2>' . $k . $l . '</div>';
}

function hj_lnk( string $href, string $ja, string $en, string $cls = '' ): string {
	return '<a class="lnk ' . $cls . '" href="' . esc_url( $href ) . '"><span>' . hj_t( $ja, $en ) . '</span>' . HJ_ARR . '</a>';
}

function hj_btn( string $href, string $ja, string $en, string $cls = '' ): string {
	return '<a class="btn ' . $cls . '" href="' . esc_url( $href ) . '"><span>' . hj_t( $ja, $en ) . '</span>' . HJ_ARR . '</a>';
}

/** 円窓 — round window frame with an offset gold ring. */
function hj_win( string $src, string $alt = '', string $cls = '' ): string {
	$inner = $src
		? '<img src="' . esc_url( $src ) . '" alt="' . esc_attr( $alt ) . '" loading="lazy">'
		: '<span class="win__ph">' . hj_seal() . '<small>' . hj_t( '近日公開', 'Coming soon' ) . '</small></span>';
	return '<figure class="win ' . $cls . '"><div class="win__c">' . $inner . '</div></figure>';
}

/** 要確認 / TBC mark for facts awaiting confirmation; only while サイト設定 → 表示 is on. */
function hj_tbd( string $ja = '要確認', string $en = 'TBC' ): string {
	return hj_show_tbc() ? '<span class="tbd">' . hj_t( $ja, $en ) . '</span>' : '';
}

// ------------------------------------------------------------------ enquiry entry points
const HJ_TOPICS = array(
	'partner'  => array( '販売パートナーについて相談する', 'Become a sales partner' ),
	'product'  => array( '商品について相談する', 'Ask about our products' ),
	'oem'      => array( 'OEM・共同開発について相談する', 'Discuss OEM &amp; co-development' ),
	'business' => array( 'ビジネスについて相談する', 'Discuss your business' ),
);

/** Contact page address that pre-selects the enquiry type (and product). */
function hj_topic_url( string $topic, ?string $item = null ): string {
	return hj_link( '/contact/?topic=' . rawurlencode( $topic ) . ( $item ? '&item=' . rawurlencode( $item ) : '' ) . '#form' );
}

function hj_cta_btn( string $topic, string $cls = '', ?string $item = null, ?array $label = null ): string {
	[ $ja, $en ] = $label ?: HJ_TOPICS[ $topic ];
	return hj_btn( hj_topic_url( $topic, $item ), $ja, $en, $cls );
}

function hj_cta_lnk( string $topic, string $cls = '', ?string $item = null, ?array $label = null ): string {
	[ $ja, $en ] = $label ?: HJ_TOPICS[ $topic ];
	return hj_lnk( hj_topic_url( $topic, $item ), $ja, $en, $cls );
}

/** Which page of the design this is (body class pg-…, menu highlight). */
function hj_page_key(): string {
	if ( is_front_page() ) {
		return 'home';
	}
	if ( is_post_type_archive( 'product' ) ) {
		return 'products';
	}
	if ( is_singular( 'product' ) ) {
		return 'product';
	}
	if ( is_home() || is_singular( 'post' ) || is_category() || is_date() ) {
		return 'news';
	}
	if ( is_page() ) {
		return get_post_field( 'post_name', get_queried_object_id() );
	}
	return 'page';
}

/** Free-from list ("無香料 ・ 無着色 …") shown under product grids. */
function hj_free_from(): array {
	return hj_t(
		array( array( '無香料', 'FRAGRANCE FREE' ), array( '無着色', 'COLORANT FREE' ), array( 'オイル<br>フリー', 'OIL FREE' ), array( 'アルコール<br>フリー', 'ALCOHOL FREE' ), array( '日本製', 'MADE IN JAPAN' ) ),
		array( array( 'Fragrance<br>free', '無香料' ), array( 'Colorant<br>free', '無着色' ), array( 'Oil<br>free', 'オイルフリー' ), array( 'Alcohol<br>free', 'アルコールフリー' ), array( 'Made in<br>Japan', '日本製' ) )
	);
}

function hj_free_list(): string {
	$li = '';
	foreach ( hj_free_from() as $f ) {
		$li .= '<li>' . str_replace( '<br>', hj_is_en() ? ' ' : '', $f[0] ) . '</li>';
	}
	return '<ul class="free rv">' . $li . '</ul>';
}

/** One news line (home and news list): date, category, title, New for 14 days. */
function hj_news_row( WP_Post $np ): string {
	$cat = get_the_category( $np->ID );
	$new = ( time() - (int) get_post_time( 'U', true, $np ) ) < 14 * DAY_IN_SECONDS;
	return '<li><a href="' . esc_url( get_permalink( $np ) ) . '"><time datetime="' . esc_attr( get_the_date( 'Y-m-d', $np ) ) . '">' . esc_html( get_the_date( 'Y.m.d', $np ) ) . '</time><span class="cat">'
		. esc_html( $cat ? hj_term_name( $cat[0] ) : '' ) . '</span><span class="tt">' . esc_html( hj_title( $np ) ) . ( $new ? '<span class=new>New</span>' : '' ) . '</span></a></li>';
}

/**
 * Lower-page header (mockup: phero()): title on paper, optional photo on the right, large
 * decorative kanji, then the breadcrumb. $crumbs: [[url, label]…] between Home and the title.
 */
function hj_phero( string $label, string $ja, string $en, string $sub, string $img, string $kanji, array $crumbs = array(), array $opt = array() ): string {
	$title = hj_t( $ja, $en );
	$pic   = $img ? '<div class="phero__img"><img src="' . esc_url( $img ) . '" alt="" style="object-position:' . esc_attr( $opt['pos'] ?? 'center' ) . '"></div>' : '';
	// in-page links: [id, label]; an id starting with / is a child page (last, with an arrow)
	$anc = '';
	foreach ( $opt['anchors'] ?? array() as $a ) {
		$anc .= str_starts_with( $a[0], '/' ) ? '<a class="anc__pg" href="' . esc_url( hj_link( $a[0] ) ) . '">' . $a[1] . '</a>' : '<a href="#' . esc_attr( $a[0] ) . '">' . $a[1] . '</a>';
	}
	$navs = $anc ? '<nav class="anc" aria-label="' . esc_attr( hj_t( 'ページ内リンク', 'On this page' ) ) . '"><div class="wrap">' . $anc . '</div></nav>' : '';
	$cls  = ( $img ? '' : ' phero--plain' ) . ( ! empty( $opt['variant'] ) ? ' phero--' . $opt['variant'] : '' );
	$up    = '';
	foreach ( $crumbs as $c ) {
		$up .= '<a href="' . esc_url( $c[0] ) . '">' . $c[1] . '</a>';
	}
	return '<section class="phero' . $cls . '">
<div class="phero__txt"><div class="phero__t rv">' . hj_eb( $label ) . '<h1>' . hj_lines( $title ) . '</h1>' . ( hj_is_en() ? '<p class="kj">' . str_replace( '<br>', '', $ja ) . '</p>' : '' ) . '<p class="phero__sub">' . $sub . '</p></div>
<p class="phero__kj" aria-hidden="true">' . $kanji . '</p></div>
' . $pic . '
</section>
<nav class="crumb" aria-label="breadcrumb"><div class="wrap"><a href="' . esc_url( hj_link( '/' ) ) . '">' . hj_t( 'ホーム', 'Home' ) . '</a>' . $up . '<span>' . str_replace( '<br>', '', $title ) . '</span></div></nav>
' . $navs;
}

// ------------------------------------------------------------------ blocks shared by the lower pages

/** Numbered steps (mockup: flow()). */
function hj_flow( array $steps ): string {
	$out = '';
	foreach ( $steps as $i => $s ) {
		$out .= '<li class="rv"><i>' . sprintf( '%02d', $i + 1 ) . '</i><h3>' . $s[0] . '</h3><p>' . $s[1] . '</p></li>';
	}
	return '<ol class="flow">' . $out . '</ol>';
}

/** Numbered pairs: title, text[, extra] (mockup: numbered()). */
function hj_numbered( array $items, string $cls = '' ): string {
	$out = '';
	foreach ( $items as $i => $it ) {
		$out .= '<li class="rv"><span class="nums2__n">' . sprintf( '%02d', $i + 1 ) . '</span><div><h3>' . $it[0] . '</h3>' . ( ! empty( $it[1] ) ? '<p>' . $it[1] . '</p>' : '' ) . ( $it[2] ?? '' ) . '</div></li>';
	}
	return '<ol class="nums2 ' . $cls . '">' . $out . '</ol>';
}

/** Export documents list (mockup: docs_list()). */
function hj_docs_list(): string {
	$out = '';
	foreach ( hj_c( 'EXPORT_DOCS' ) as $d ) {
		$out .= '<li class="rv"><b>' . $d[0] . '</b><span>' . $d[1] . '</span></li>';
	}
	return '<ul class="docl">' . $out . '</ul>';
}

/** Registration support by market (mockup: reg_table()). */
function hj_reg_table(): string {
	$regs = hj_c( 'REGS' );
	$rows = '';
	foreach ( $regs as $i => $r ) {
		$rows .= '<tr><th>' . $r[0] . ( hj_is_en() ? '' : '<small>' . $r[1] . '</small>' ) . '</th><td>' . $r[2] . '</td>'
			. ( 0 === $i ? '<td rowspan="' . count( $regs ) . '" class="mtbl__m">' . hj_c( 'REG_SUPPORT' ) . '</td>' : '' ) . '</tr>';
	}
	return '<div class="sx"><table class="mtbl"><thead><tr><th>' . hj_t( '対象市場', 'Market' ) . '</th><th>' . hj_t( '主な手続き・必要資料', 'Typical requirement' ) . '</th><th>' . hj_t( '花印の対応', 'Our support' ) . '</th></tr></thead><tbody>' . $rows . '</tbody></table></div>';
}

/** IP collaboration cards (mockup: ip_cards()); $detail adds product / channel / type. */
function hj_ip_cards( bool $detail = false ): string {
	$out = '';
	foreach ( hj_collabs() as $c ) {
		$prod = esc_html( (string) hj_get( 'product', $c->ID ) );
		$ch   = esc_html( (string) hj_get( 'channel', $c->ID ) );
		$dl   = $detail
			? '<dl><div><dt>' . hj_t( '商品', 'Product' ) . '</dt><dd>' . $prod . '</dd></div><div><dt>' . hj_t( '販売', 'Channel' ) . '</dt><dd>' . ( $ch ?: hj_tbd() ) . '</dd></div>'
				. '<div><dt>' . hj_t( '区分', 'Type' ) . '</dt><dd>' . hj_t( '正規ライセンス商品', 'Officially licensed' ) . '</dd></div></dl>'
			: '<small>' . $prod . '</small>';
		$out .= '<li class="rv"><figure><img src="' . esc_url( (string) get_the_post_thumbnail_url( $c, 'large' ) ) . '" alt="' . esc_attr( hj_title( $c ) ) . '" loading="lazy"></figure><p><b>'
			. esc_html( hj_title( $c ) ) . '</b>' . $dl . '</p><span class="tag">' . esc_html( (string) hj_get( 'label', $c->ID ) ) . '</span></li>';
	}
	return $out;
}

function hj_ipnote(): string {
	return hj_t( 'すべてのコラボレーション商品は正規ライセンス品です。ライセンス証明書類はお取引先にご提示できます。', 'All collaboration products are officially licensed. Proof of licence is available to trade partners.' );
}

/** IP collaborations band (brand page; mockup: brand_collab()). */
function hj_brand_collab( string $num, string $id = '' ): string {
	return '<section class="sec blush collab collab--row"' . ( $id ? ' id="' . esc_attr( $id ) . '"' : '' ) . '><div class="wrap">
' . hj_shd( $num, 'Collaboration', 'IPコラボレーション商品', 'Licensed IP collaborations', 'IPコラボレーション', null, 'shd--c' ) . '
<ul class="collab__l collab__l--4">' . hj_ip_cards() . '</ul>
<div class="ctr ctr--2">' . hj_lnk( hj_link( '/collaboration/' ), 'コラボレーションについて', 'About our collaborations' ) . hj_cta_lnk( 'oem' ) . '</div></div></section>';
}

/** A field of an exhibition post in the language being shown, with ［…］ marks. */
function hj_ex( WP_Post $e, string $field ): string {
	return hj_text( (string) hj_get( $field, $e->ID ) );
}

/** The next exhibition (news sidebar, buyer page), or null. */
function hj_next_exhibition(): ?WP_Post {
	$up = hj_exhibitions( 'upcoming' );
	return $up[0] ?? null;
}

/** Exhibition card (news sidebar; mockup: exh_card()). */
function hj_exh_card(): string {
	$e = hj_next_exhibition();
	if ( ! $e ) {
		return '';
	}
	$page = (string) hj_raw( 'page', $e->ID );
	return '<aside class="exh rv">' . hj_seal( '出展', 'seal--txt' ) . '
' . hj_eb( 'Exhibition' ) . '<h3>' . esc_html( hj_title( $e ) ) . '</h3><p>' . hj_c( 'EXH_INTRO' ) . '</p>
<dl><div><dt>' . hj_t( '会期', 'Dates' ) . '</dt><dd>' . hj_ex( $e, 'dates' ) . '</dd></div>
<div><dt>' . hj_t( '会場', 'Venue' ) . '</dt><dd>' . hj_ex( $e, 'venue' ) . '</dd></div>
<div><dt>' . hj_t( 'ブース', 'Booth' ) . '</dt><dd>' . hj_ex( $e, 'booth' ) . '</dd></div></dl>
' . ( $page ? hj_btn( hj_link( $page ) . '#booking', '商談を予約する', 'Book a meeting', 'btn--light' ) : '' ) . '</aside>';
}

/** Product lines for form check boxes: <label><input …>…</label> (keys from the plugin). */
function hj_form_lines_html( string $name = 'products' ): string {
	if ( ! function_exists( 'hj_form_lines' ) ) {
		return '';
	}
	$sel = (array) hj_form_value( $name );
	$out = '';
	foreach ( hj_form_lines() as $k => $l ) {
		$out .= '<label><input type="checkbox" name="' . hj_fname( $name ) . '[]" value="' . esc_attr( $k ) . '" data-items="' . esc_attr( $l[1] ) . '"' . checked( in_array( $k, $sel, true ), true, false ) . '>' . esc_html( $l[0] ) . '</label>';
	}
	return $out;
}

/** A form field wrapper (mockup: fld()), with the error under it. */
function hj_fld( string $name, string $label, string $inner, bool $required, bool $full = false, string $hint = '' ): string {
	$mark = $required ? '<em class="req">' . hj_t( '必須', 'Required' ) . '</em>' : '<em class="opt">' . hj_t( '任意', 'Optional' ) . '</em>';
	return '<label class="fld' . ( $full ? ' fld--full' : '' ) . '"><span>' . $label . $mark . '</span>' . $inner . ( $hint ? '<small class="hint">' . $hint . '</small>' : '' ) . ( function_exists( 'hj_form_error' ) ? hj_form_error( $name ) : '' ) . '</label>';
}

/** Whether a form field is required in the language being shown. */
function hj_req( string $form, string $name ): bool {
	$f = function_exists( 'hj_form_fields' ) ? ( hj_form_fields( $form )[ $name ] ?? null ) : null;
	return $f ? (bool) ( hj_is_en() ? $f[3] : $f[2] ) : false;
}

function hj_input( string $name, string $type = 'text', string $placeholder = '', string $extra = '' ): string {
	return '<input type="' . $type . '" name="' . hj_fname( $name ) . '" value="' . esc_attr( (string) hj_form_value( $name ) ) . '"' . ( $placeholder ? ' placeholder="' . esc_attr( $placeholder ) . '"' : '' ) . $extra . '>';
}

function hj_select( string $name, array $options ): string {
	$cur = (string) hj_form_value( $name );
	$out = '<select name="' . hj_fname( $name ) . '"><option value="">' . hj_t( '選択してください', 'Please select' ) . '</option>';
	foreach ( $options as $o ) {
		$out .= '<option' . selected( $cur, $o, false ) . '>' . esc_html( $o ) . '</option>';
	}
	return $out . '</select>';
}
