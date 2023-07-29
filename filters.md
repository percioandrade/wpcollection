# Filters codes for you WordPress

Place it on functions.php or create a new plugin for this.

**WordPress - Enable shortcode in menu**

	add_filter('wp_nav_menu_items', 'do_shortcode');

    **Enable logout url masked eg: /$VALUE=1**

	add_filter('logout_url', 'custom_logout_url', 10, 2);
	add_action('wp_loaded', 'custom_logout_action');

**WordPress - Custom logout URL**

	function custom_logout_url($logout_url, $redirect){
		$url = add_query_arg('NEW_VALUE', 1, home_url()); // example: bye
		if(! empty($redirect)){
			$url = add_query_arg('redirect', $redirect, $url);
		}
		return esc_url($url);
	}
	add_filter('logout_url', 'custom_logout_url', 10, 2);

**WordPress - Custom logout URL redirection**

	function custom_logout_action(){
		$user_id = get_current_user_id();
		if(isset($_GET['NEW_VALUE'])){
			wp_logout();
			$loc = isset($_GET['redirect'] ) ? $_GET['redirect'] : home_url();
			wp_redirect(esc_url($loc), 302);
			exit;
		}
	}
	add_action('template_redirect', 'custom_logout_action');

**WordPress - Remove amp validation**

	add_filter(
		'amp_validation_error_sanitized',
		fn($sanitized, $error) => (
			$error['node_name'] === 'script'
			&& strpos($error['text'], 'WFAJAXWatcherVars') !== false
		) ? true : $sanitized,
		10,
		2
	);

**WordPress - Limit access to media library ( users can only see/select own media)**

	function wpsnippet_show_current_user_attachments($query){
		$user_id = get_current_user_id();
		if($user_id && !current_user_can('activate_plugins') && !current_user_can('edit_others_posts')){
			$query['author'] = $user_id;
		}
		return $query;
	}
	add_filter('ajax_query_attachments_args', 'wpsnippet_show_current_user_attachments');

**WordPress - Remove version from css & scripts**

	function my_remove_wp_ver_css_js($src){
		if(strpos($src, 'ver=')){
			$src = remove_query_arg('ver', $src);
		}
		return $src;
	}
	add_filter('style_loader_src', 'my_remove_wp_ver_css_js', 9999);
	add_filter('script_loader_src', 'my_remove_wp_ver_css_js', 9999);

**WordPress - Remove WP version from RSS**

	add_filter('the_generator', '__return_empty_string');

**WordPress - Remove admin bar**

	add_filter('show_admin_bar', '__return_false');

**WordPress - Disable Gutemberg**

	add_filter('use_block_editor_for_post', '__return_false');

**WordPress - Clean WordPress**

	final class remove_trash_wp {
		public function __construct(){
		add_action('admin_bar_menu', [$this, 'remove_admin_bar_items'], 999);
		add_action('wp_dashboard_setup', [$this, 'clean_wp_admin']);
		add_action('wp_loaded', [$this, 'clean_wp_head']);
		add_filter('body_class', [$this, 'add_slug_to_body_class']);
		add_filter('contextual_help', [$this, 'remove_contextual_help'], 999, 3);
		add_action('widgets_init', [$this, 'remove_default_widgets']);
		add_filter('wp_headers', [$this, 'remove_pingback_header']);
		add_filter('wp_headers', [$this, 'remove_json_api']);
		add_action('login_headerurl', function(){ return home_url(); });
		add_filter('admin_footer_text', '__return_null');
		add_filter('emoji_svg_url', '__return_false');
		add_filter('enable_post_by_email_configuration', '__return_false', 999);
		add_filter('feed_links_show_comments_feed', '__return_false');
		add_filter('get_image_tag_class', function($c, $i, $align, $s){ return 'align'.esc_attr($align); }, 10, 4);
		add_filter('jpeg_quality', function($v){ return 95;});
		add_filter('the_generator', '__return_empty_string');
		remove_action('welcome_panel', 'wp_welcome_panel');
		}
	}

**WordPress - Enable WEBP in Media**

	add_filter('mime_types', function($mimes){ $mimes['webp'] = 'image/webp'; return $mimes;});

**WordPress - Enable preview for webp image files**

	function webp_is_displayable($result, $path){
		if($result === false){
			$info = getimagesize($path, $image_info);
			$displayable_image_types = array(iMAGETYPE_WEBp);
			if($info !== false && in_array($info[2], $displayable_image_types)){
				$result = true;
			} else {
				$result = false;
			}
		}
		return $result;
	}
	add_filter('file_is_displayable_image', 'webp_is_displayable', 10, 2);

**Elementor - Remove Google Fonts in Elementor**

    add_filter('elementor/frontend/print_google_fonts', '__return_false');

**Rankmath - Custom URL on sitemap**

	add_filter('rank_math/sitemap/xml_img_src', function( $src, $post){
		$src = str_replace('http://URL', 'https://URL', $src);
		return $src;
	}, 10, 2);

**Rankmath - Remove sitemap credit**

    add_filter('rank_math/sitemap/remove_credit', '__return_true');