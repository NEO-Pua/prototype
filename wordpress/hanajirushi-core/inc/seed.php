<?php
/**
 * 初期データ: fills a fresh site with the mockup's content (products from the Rakuten store,
 * home slides, IP collaborations, news, company details), so it looks like the mockup at
 * once. Tools → 花印 初期データ. Running it again updates the same items; nothing is
 * duplicated and nothing else is touched.
 *
 * The data is seed/seed.json (made by wordpress/dev/sync.py from the mockup); photos come
 * from seed/img and go into the media library.
 */

defined( 'ABSPATH' ) || exit;

add_action( 'admin_menu', function () {
	add_management_page( '花印 初期データ', '花印 初期データ', 'manage_options', 'hj-seed', 'hj_seed_page' );
} );

function hj_seed_page(): void {
	$done = null;
	if ( isset( $_POST['hj_seed'] ) && check_admin_referer( 'hj_seed' ) ) {
		$done = hj_seed_import();
	}
	echo '<div class="wrap"><h1>花印 初期データ</h1>';
	if ( is_array( $done ) ) {
		printf( '<div class="notice notice-success"><p>取り込みました：ページ %d件、製品 %d件、スライド %d件、IPコラボ %d件、展示会 %d件、お知らせ %d件、サイト設定。</p></div>',
			(int) $done['pages'], (int) $done['products'], (int) $done['slides'], (int) $done['collabs'], (int) $done['exhibitions'], (int) $done['news'] );
	}
	echo '<p>モックアップと同じ内容（楽天市場の製品情報、トップスライド、IPコラボ、展示会、お知らせ、会社情報・沿革・取引条件・よくあるご質問）を取り込みます。<br>';
	echo 'テーマ用のページ（ブランド、会社概要、お問い合わせなど）が無ければ作成し、トップページとお知らせページを設定します。<br>';
	echo 'もう一度実行すると同じ項目を上書きします（重複はしません）。既存ページの本文や、それ以外の投稿には触れません。</p>';
	echo '<form method="post">';
	wp_nonce_field( 'hj_seed' );
	submit_button( '初期データを取り込む', 'primary', 'hj_seed' );
	echo '</form></div>';
}

/** Imports seed/seed.json. Returns counts per kind. */
function hj_seed_import(): array {
	if ( ! function_exists( 'update_field' ) ) {
		return array( 'pages' => 0, 'products' => 0, 'slides' => 0, 'collabs' => 0, 'exhibitions' => 0, 'news' => 0 );
	}
	$data = json_decode( (string) file_get_contents( HJ_CORE_DIR . 'seed/seed.json' ), true );
	$ids  = array();

	foreach ( $data['products'] as $p ) {
		$id = hj_seed_post( 'product', $p['slug'], $p['ja']['title'], $p['order'] );
		$ids[ $p['slug'] ] = $id;
		foreach ( array( 'category', 'series', 'size', 'kind', 'rakuten_code', 'image_temp', 'amazon_url', 'yahoo_url', 'qoo10_url' ) as $k ) {
			hj_seed_set( 'product', $k, $p[ $k ], $id );
		}
		hj_seed_set( 'product', 'is_new', $p['is_new'] ? 1 : 0, $id );
		hj_seed_set( 'product', 'coming_soon', $p['coming_soon'] ? 1 : 0, $id );
		hj_seed_set( 'product', 'show_on_home', $p['show_on_home'] ? 1 : 0, $id );
		foreach ( array( '' => $p['ja'], '_en' => $p['en'] ) as $sfx => $l ) {
			foreach ( array( 'sub', 'short', 'catch', 'desc', 'usage', 'inci', 'badges', 'free', 'points' ) as $k ) {
				hj_seed_set( 'product', $k . $sfx, $l[ $k ], $id );
			}
		}
		hj_seed_set( 'product', 'title_en', $p['en']['title'], $id );
		if ( $p['image'] ) {
			set_post_thumbnail( $id, hj_seed_media( $p['image'], $p['ja']['title'] ) );
		}
	}

	foreach ( $data['slides'] as $i => $s ) {
		$id = hj_seed_post( 'kv_slide', 'slide-' . $s['order'], $s['ja']['tab'], $s['order'] );
		hj_seed_set( 'slide', 'tab', $s['ja']['tab'], $id );
		hj_seed_set( 'slide', 'title_en', $s['en']['tab'], $id );
		foreach ( array( '' => $s['ja'], '_en' => $s['en'] ) as $sfx => $l ) {
			foreach ( array( 'label', 'heading', 'text', 'btn1' ) as $k ) {
				hj_seed_set( 'slide', $k . $sfx, $l[ $k ], $id );
			}
			hj_seed_set( 'slide', 'accent' . $sfx, $l['accent'] ? 1 : 0, $id );
		}
		foreach ( array( 'eyebrow', 'visual', 'kanji', 'kanji_caption', 'seal', 'bg_pos', 'btn1_link' ) as $k ) {
			hj_seed_set( 'slide', $k, $s[ $k ] ?? '', $id );
		}
		hj_seed_set( 'slide', 'product', isset( $s['product'] ) ? ( $ids[ $s['product'] ] ?? 0 ) : '', $id );
		hj_seed_set( 'slide', 'products', array_values( array_filter( array_map( fn( $x ) => $ids[ $x ] ?? 0, $s['products'] ?? array() ) ) ), $id );
		hj_seed_set( 'slide', 'bg', $s['bg'] ? hj_seed_media( $s['bg'], '' ) : '', $id );
	}

	foreach ( $data['collabs'] as $c ) {
		$id = hj_seed_post( 'collab', 'collab-' . $c['order'], $c['ja']['title'], $c['order'] );
		foreach ( array( 'product', 'label', 'channel' ) as $k ) {
			hj_seed_set( 'collab', $k, $c['ja'][ $k ], $id );
			hj_seed_set( 'collab', $k . '_en', $c['en'][ $k ], $id );
		}
		hj_seed_set( 'collab', 'title_en', $c['en']['title'], $id );
		set_post_thumbnail( $id, hj_seed_media( $c['image'], $c['ja']['title'] ) );
	}

	$cats = array();
	foreach ( $data['news_cats'] as $nc ) {
		[ $slug, $ja, $en ] = $nc;
		$term = get_term_by( 'slug', $slug, 'category' );
		$tid  = $term ? $term->term_id : (int) ( wp_insert_term( $ja, 'category', array( 'slug' => $slug ) )['term_id'] ?? 0 );
		update_term_meta( $tid, 'name_en', $en );
		$cats[ $slug ] = $tid;
	}
	foreach ( $data['news'] as $i => $n ) {
		$slug = 'news-' . str_replace( '-', '', $n['date'] ) . '-' . ( $i + 1 );
		$id   = hj_seed_post( 'post', $slug, $n['ja']['title'], 0, $n['date'] . ' 10:00:00' );
		wp_set_post_categories( $id, array( $cats[ $n['cat'] ] ?? 0 ) );
		hj_seed_set( 'post', 'title_en', $n['en']['title'], $id );
	}

	foreach ( array( '' => $data['settings']['ja'], '_en' => $data['settings']['en'] ) as $sfx => $l ) {
		foreach ( $l as $k => $v ) {
			hj_seed_set( 'settings', $k . $sfx, $v, 'option' );
		}
	}
	hj_seed_set( 'settings', 'show_tbc', $data['settings']['show_tbc'] ? 1 : 0, 'option' );
	foreach ( $data['settings_more'] as $k => $v ) {
		hj_seed_set( 'settings', $k, $v, 'option' );
	}
	hj_seed_set( 'settings', 'autoreply', 1, 'option' );

	foreach ( $data['exhibitions'] as $e ) {
		$id = hj_seed_post( 'exhibition', $e['slug'], $e['title'], 0 );
		hj_seed_set( 'exhibition', 'title_en', $e['title'], $id );
		foreach ( $e as $k => $v ) {
			if ( ! in_array( $k, array( 'slug', 'title' ), true ) ) {
				hj_seed_set( 'exhibition', $k, $v, $id );
			}
		}
	}

	// The pages the theme has templates for (page-<slug>.php). Existing pages keep their content.
	$page_ids = array();
	foreach ( $data['pages'] as $pg ) {
		[ $slug, $ja, $en, $parent ] = $pg;
		$found = get_page_by_path( $parent ? $parent . '/' . $slug : $slug );
		$found = $found ?: get_page_by_path( $slug );
		$id    = $found ? $found->ID : (int) wp_insert_post( array(
			'post_type'   => 'page',
			'post_name'   => $slug,
			'post_title'  => $ja,
			'post_status' => 'publish',
			'post_parent' => $parent ? ( $page_ids[ $parent ] ?? 0 ) : 0,
		) );
		update_post_meta( $id, 'title_en', $en );
		$page_ids[ $slug ] = $id;
	}
	// Home page = the トップ page (front-page.php); news list = the お知らせ page (home.php).
	update_option( 'show_on_front', 'page' );
	update_option( 'page_on_front', $page_ids['home'] );
	update_option( 'page_for_posts', $page_ids['news'] );

	return array( 'pages' => count( $data['pages'] ), 'products' => count( $data['products'] ), 'slides' => count( $data['slides'] ),
		'collabs' => count( $data['collabs'] ), 'exhibitions' => count( $data['exhibitions'] ), 'news' => count( $data['news'] ) );
}

/** Saves a field by its key (field_hj_<group>_<name>), so same-named fields in other groups never mix. */
function hj_seed_set( string $group, string $name, $value, $id ): void {
	update_field( 'field_hj_' . $group . '_' . $name, $value, $id );
}

/** Creates or updates the post with this slug; returns its ID. */
function hj_seed_post( string $type, string $slug, string $title, int $order, string $date = '' ): int {
	$found = get_posts( array( 'post_type' => $type, 'name' => $slug, 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids' ) );
	$post  = array(
		'post_type'   => $type,
		'post_name'   => $slug,
		'post_title'  => $title,
		'post_status' => 'publish',
		'menu_order'  => $order,
	);
	if ( $date ) {
		$post['post_date'] = $date;
	}
	if ( $found ) {
		$post['ID'] = $found[0];
		return (int) wp_update_post( $post );
	}
	return (int) wp_insert_post( $post );
}

/** Adds a seed photo to the media library once; returns the attachment ID. */
function hj_seed_media( string $file, string $alt ): int {
	$have = get_posts( array( 'post_type' => 'attachment', 'meta_key' => '_hj_seed_file', 'meta_value' => $file, 'numberposts' => 1, 'fields' => 'ids', 'post_status' => 'any' ) );
	if ( $have ) {
		return (int) $have[0];
	}
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	$tmp = wp_tempnam( $file );
	copy( HJ_CORE_DIR . 'seed/img/' . $file, $tmp );
	$id = media_handle_sideload( array( 'name' => $file, 'tmp_name' => $tmp ), 0, $alt );
	if ( is_wp_error( $id ) ) {
		@unlink( $tmp );
		return 0;
	}
	update_post_meta( $id, '_hj_seed_file', $file );
	if ( $alt ) {
		update_post_meta( $id, '_wp_attachment_image_alt', $alt );
	}
	return (int) $id;
}
