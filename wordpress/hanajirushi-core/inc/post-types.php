<?php
/**
 * Post types: 製品 (product, with its own pages), トップスライド (kv_slide) and
 * IPコラボ (collab). News uses WordPress's own 投稿 (posts).
 */

defined( 'ABSPATH' ) || exit;

function hj_register_post_types(): void {
	register_post_type( 'product', array(
		'labels'        => array(
			'name'          => '製品',
			'singular_name' => '製品',
			'add_new'       => '新規追加',
			'add_new_item'  => '製品を追加',
			'edit_item'     => '製品を編集',
			'all_items'     => '製品一覧',
			'search_items'  => '製品を検索',
		),
		'public'        => true,
		'has_archive'   => 'products',
		'rewrite'       => array( 'slug' => 'products', 'with_front' => false ),
		'menu_position' => 5,
		'menu_icon'     => 'dashicons-products',
		'supports'      => array( 'title', 'thumbnail', 'page-attributes' ),
		'show_in_rest'  => true,
	) );

	register_post_type( 'kv_slide', array(
		'labels'        => array(
			'name'          => 'トップスライド',
			'singular_name' => 'スライド',
			'add_new'       => '新規追加',
			'add_new_item'  => 'スライドを追加',
			'edit_item'     => 'スライドを編集',
			'all_items'     => 'スライド一覧',
		),
		'public'        => false,
		'show_ui'       => true,
		'menu_position' => 6,
		'menu_icon'     => 'dashicons-images-alt2',
		'supports'      => array( 'title', 'page-attributes' ),
	) );

	register_post_type( 'collab', array(
		'labels'        => array(
			'name'          => 'IPコラボ',
			'singular_name' => 'IPコラボ',
			'add_new'       => '新規追加',
			'add_new_item'  => 'IPコラボを追加',
			'edit_item'     => 'IPコラボを編集',
			'all_items'     => 'IPコラボ一覧',
		),
		'public'        => false,
		'show_ui'       => true,
		'menu_position' => 7,
		'menu_icon'     => 'dashicons-star-filled',
		'supports'      => array( 'title', 'thumbnail', 'page-attributes' ),
	) );

	register_post_type( 'exhibition', array(
		'labels'        => array(
			'name'          => '展示会',
			'singular_name' => '展示会',
			'add_new'       => '新規追加',
			'add_new_item'  => '展示会を追加',
			'edit_item'     => '展示会を編集',
			'all_items'     => '展示会一覧',
		),
		'public'        => false,
		'show_ui'       => true,
		'menu_position' => 8,
		'menu_icon'     => 'dashicons-calendar-alt',
		'supports'      => array( 'title' ),
	) );

	// Every form sent from the site is kept here too, in case an email does not arrive.
	register_post_type( 'hj_enquiry', array(
		'labels'          => array(
			'name'          => 'お問い合わせ履歴',
			'singular_name' => 'お問い合わせ',
			'all_items'     => 'お問い合わせ履歴',
			'edit_item'     => 'お問い合わせ',
		),
		'public'          => false,
		'show_ui'         => true,
		'menu_position'   => 25,
		'menu_icon'       => 'dashicons-email-alt',
		'supports'        => array( 'title', 'editor' ),
		'capability_type' => 'post',
		'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
		'map_meta_cap'    => true,
	) );
}
add_action( 'init', 'hj_register_post_types' );

// Admin lists in display order (the 順序 box), like the site shows them.
add_action( 'pre_get_posts', function ( WP_Query $q ) {
	if ( is_admin() && $q->is_main_query() && in_array( $q->get( 'post_type' ), array( 'product', 'kv_slide', 'collab' ), true ) && ! $q->get( 'orderby' ) ) {
		$q->set( 'orderby', array( 'menu_order' => 'ASC', 'title' => 'ASC' ) );
	}
} );

// Products page: every product in display order, no paging.
add_action( 'pre_get_posts', function ( WP_Query $q ) {
	if ( ! is_admin() && $q->is_main_query() && $q->is_post_type_archive( 'product' ) ) {
		$q->set( 'orderby', array( 'menu_order' => 'ASC', 'title' => 'ASC' ) );
		$q->set( 'posts_per_page', -1 );
	}
} );
