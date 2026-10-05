<?php
/**
 * Japanese line breaking (the same as the mockup's add_wbr()).
 *
 * Japanese has no spaces, so browsers may break a line in the middle of a word. BudouX
 * (Google, Apache-2.0, https://github.com/google/budoux) splits Japanese text into phrases;
 * a <wbr> between phrases plus the theme's CSS `word-break: keep-all` makes every browser,
 * Safari on iPhone included, wrap between phrases. This is a PHP port of BudouX's parser
 * using its default Japanese model (budoux-ja.json, copied by wordpress/dev/sync.py).
 *
 * Applied to the whole Japanese page as it is sent, so staff never type <wbr> themselves.
 */

defined( 'ABSPATH' ) || exit;

final class HJ_BudouX {
	private array $m;
	private float $base;

	public function __construct( array $model ) {
		$this->m = $model;
		$sum     = 0;
		foreach ( $model as $group ) {
			$sum += array_sum( $group );
		}
		$this->base = -$sum * 0.5;
	}

	/** Splits a sentence into phrases. */
	public function parse( string $s ): array {
		$c = mb_str_split( $s );
		$n = count( $c );
		if ( ! $n ) {
			return array();
		}
		$m      = $this->m;
		$chunks = array( $c[0] );
		for ( $i = 1; $i < $n; $i++ ) {
			$sc = $this->base;
			if ( $i > 2 ) {
				$sc += $m['UW1'][ $c[ $i - 3 ] ] ?? 0;
			}
			if ( $i > 1 ) {
				$sc += $m['UW2'][ $c[ $i - 2 ] ] ?? 0;
			}
			$sc += $m['UW3'][ $c[ $i - 1 ] ] ?? 0;
			$sc += $m['UW4'][ $c[ $i ] ] ?? 0;
			if ( $i + 1 < $n ) {
				$sc += $m['UW5'][ $c[ $i + 1 ] ] ?? 0;
			}
			if ( $i + 2 < $n ) {
				$sc += $m['UW6'][ $c[ $i + 2 ] ] ?? 0;
			}
			if ( $i > 1 ) {
				$sc += $m['BW1'][ $c[ $i - 2 ] . $c[ $i - 1 ] ] ?? 0;
			}
			$sc += $m['BW2'][ $c[ $i - 1 ] . $c[ $i ] ] ?? 0;
			if ( $i + 1 < $n ) {
				$sc += $m['BW3'][ $c[ $i ] . $c[ $i + 1 ] ] ?? 0;
			}
			if ( $i > 2 ) {
				$sc += $m['TW1'][ $c[ $i - 3 ] . $c[ $i - 2 ] . $c[ $i - 1 ] ] ?? 0;
			}
			if ( $i > 1 ) {
				$sc += $m['TW2'][ $c[ $i - 2 ] . $c[ $i - 1 ] . $c[ $i ] ] ?? 0;
			}
			if ( $i + 1 < $n ) {
				$sc += $m['TW3'][ $c[ $i - 1 ] . $c[ $i ] . $c[ $i + 1 ] ] ?? 0;
			}
			if ( $i + 2 < $n ) {
				$sc += $m['TW4'][ $c[ $i ] . $c[ $i + 1 ] . $c[ $i + 2 ] ] ?? 0;
			}
			if ( $sc > 0 ) {
				$chunks[] = $c[ $i ];
			} else {
				$chunks[ count( $chunks ) - 1 ] .= $c[ $i ];
			}
		}
		return $chunks;
	}

	public static function ja(): self {
		static $p = null;
		if ( null === $p ) {
			$json = file_get_contents( HJ_CORE_DIR . 'inc/budoux-ja.json' );
			$p    = new self( json_decode( (string) $json, true ) ?: array() );
		}
		return $p;
	}
}

/** Adds <wbr> between Japanese phrases in the text of an HTML page (body only, not in tags). */
function hj_add_wbr( string $html ): string {
	$at = stripos( $html, '<body' );
	if ( false === $at ) {
		return $html;
	}
	$head   = substr( $html, 0, $at );
	$tokens = preg_split( '/(<[^>]+>)/', substr( $html, $at ), -1, PREG_SPLIT_DELIM_CAPTURE );
	$skip   = 0;
	$parser = HJ_BudouX::ja();
	$out    = '';
	foreach ( $tokens as $tok ) {
		if ( '' !== $tok && '<' === $tok[0] ) {
			if ( preg_match( '#^<(/?)(script|style|title|textarea|select|option)\b#i', $tok, $mm ) ) {
				$skip += '/' === $mm[1] ? -1 : 1;
			}
			$out .= $tok;
		} elseif ( '' !== $tok && ! $skip && preg_match( '/[\x{3040}-\x{30FF}\x{4E00}-\x{9FFF}]/u', $tok ) ) {
			$joined = implode( '<wbr>', $parser->parse( $tok ) );
			// never split an HTML entity such as &amp;
			$out .= preg_replace( '/(&[#a-zA-Z0-9]*)<wbr>([#a-zA-Z0-9]*;)/', '$1$2', $joined );
		} else {
			$out .= $tok;
		}
	}
	return $head . $out;
}

// Japanese pages only (English text has spaces).
add_action( 'template_redirect', function () {
	if ( hj_is_en() || is_feed() || is_robots() || is_trackback() || wp_doing_ajax() ) {
		return;
	}
	ob_start( 'hj_add_wbr' );
}, 99 );
