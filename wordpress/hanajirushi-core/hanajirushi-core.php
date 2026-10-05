<?php
/**
 * Plugin Name:       花印 HANAJIRUSHI Core
 * Description:       花印サイトのコンテンツ（製品・スライド・IPコラボ・展示会・お知らせの英語欄・サイト設定）、お問い合わせ・商談予約フォーム、日本語／英語の切り替え（/en/）、和文の改行調整、初期データの取り込み。テーマ「花印 HANAJIRUSHI」と組み合わせて使います。
 * Version:           0.2.0
 * Requires at least: 6.6
 * Requires PHP:      8.1
 * Requires Plugins:  secure-custom-fields
 * License:           GPL-2.0-or-later
 * Text Domain:       hanajirushi-core
 *
 * The content structure lives here, not in the theme, so a later redesign keeps the content.
 * Fields are defined in code (inc/fields.php) with Secure Custom Fields, the free plugin
 * maintained on WordPress.org.
 */

defined( 'ABSPATH' ) || exit;

define( 'HJ_CORE_VERSION', '0.2.0' );
define( 'HJ_CORE_DIR', plugin_dir_path( __FILE__ ) );
define( 'HJ_CORE_URL', plugin_dir_url( __FILE__ ) );

require HJ_CORE_DIR . 'inc/lang.php';
require HJ_CORE_DIR . 'inc/budoux.php';
require HJ_CORE_DIR . 'inc/post-types.php';
require HJ_CORE_DIR . 'inc/fields.php';
require HJ_CORE_DIR . 'inc/data.php';
require HJ_CORE_DIR . 'inc/forms.php';
require HJ_CORE_DIR . 'inc/seed.php';

hj_detect_lang();

register_activation_hook( __FILE__, function () {
	hj_register_post_types();
	flush_rewrite_rules();
} );
register_deactivation_hook( __FILE__, 'flush_rewrite_rules' );
