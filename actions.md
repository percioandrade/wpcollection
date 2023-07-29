# Actions codes for you WordPress

Place it on functions.php or create a new plugin for this.

**WordPress - Remove emojis**

	function remove_emoji(){
		remove_action('wp_head', 'print_emoji_detection_script', 10);
		remove_action('admin_print_scripts', 'print_emoji_detection_script');
		remove_action('admin_print_styles', 'print_emoji_styles');
		remove_filter('the_content_feed', 'wp_staticize_emoji');
		remove_filter('comment_text_rss', 'wp_staticize_emoji');
		remove_filter('wp_mail', 'wp_staticize_emoji_for_email');
	}
	add_action('init', 'remove_emoji');

**WordPress - Change author base url: domain/author to your domain/$NEW_SLUG**

	function wp_custom_author_urlbase($wp_rewrite){
		global $wp_rewrite;
		$author_slug = 'NEW_SLUG'; // the new slug name
		$wp_rewrite->author_base = $author_slug;
		flush_rewrite_rules();
	}
	add_action('init', 'wp_custom_author_urlbase');

**WordPress - Change query search 's' to other value**

	add_action('init', function(){
		add_rewrite_tag('%search_query%', '([^&]+)');
		remove_query_arg('s');
	});

	add_filter('request', function($request){
		if(isset($_REQUEST['search'])){
			$search_query = sanitize_text_field($_REQUEST['search']);
			$request['s'] = $search_query;
		}
		return $request;
	} );

**WordPress - Disable default search on WordPress**

	add_action('init', function(){
		add_rewrite_tag('%search_query%', '([^&]+)');
		remove_query_arg('s');
	});

	add_filter('request', function($request){
		if(isset($_REQUEST['search'])){
			$search_query = sanitize_text_field($_REQUEST['search']);
			$request['s'] = $search_query;
		}

		return $request;
	});

**WordPress - Remove WP version from head**

	remove_action('wp_head', 'wp_generator');

**WordPress - Disable FontAwesome**

	add_action('wp_enqueue_scripts', function(){ wp_dequeue_style('font-awesome'); }, 50);

**WordPress - Remove the Font Awesome http request as well on elementor**

	add_action('elementor/frontend/after_enqueue_styles', function (){ wp_dequeue_style('font-awesome');});

**WordPress - Remove Gutenberg block library CSS**

	function remove_wp_block_library_css(){
		wp_dequeue_style(array('wp-block-library', 'wp-block-library-theme', 'wc-block-style', 'global-styles'));
	}
	add_action('wp_enqueue_scripts', 'remove_wp_block_library_css');

**Theme - Enable RSS on Header**

	add_theme_support('automatic-feed-links');

**WordPress - Hide admin ajax from no-admin users**

	function redirect_non_admin_users(){
		// Check if user is not an admin and not accessing admin-ajax.php
		if( ! current_user_can('manage_options') && '/wp-admin/admin-ajax.php' !== $_SERVER['PHP_SELF']){
			// Redirect user to homepage
			wp_redirect(home_url());
			exit;
		}
	}
	add_action('admin_init', 'redirect_non_admin_users');

**WordPress - Change footer text**

	function replace_footer_text(){
		echo 'YOUR NEW FOOTER';
	}
	add_action('admin_footer_text', 'replace_footer_text');

**WordPress - Prevent upload from no staff users**

	function pws_block_admin(){
		if(
			// Look for the presence of /wp-admin/ in the url
			stripos($_SERVER['REQUEST_URI'],'/wp-admin/') !== false
			&&
			// Allow calls to async-upload.php
			stripos($_SERVER['REQUEST_URI'],'async-upload.php') === false
			&&
			// Allow calls to admin-ajax.php
			stripos($_SERVER['REQUEST_URI'],'admin-ajax.php') === false
			){
				if(!current_user_can('manage_options')){
				$redirect_to = home_url();
				wp_redirect($redirect_to, 302);
			}
		}
	}
	add_action('admin_init', 'pws_block_admin', 0);

**WordPress - Remove default inclusion of jQuery and jQuery Migrate**

	function remove_default_jquery(){
		if(!is_admin()){
			wp_deregister_script('jquery');
			wp_deregister_script('jquery-migrate');
		}
	}
	add_action('wp_enqueue_scripts', 'remove_default_jquery');

**WordPress - Include jQuery and jQuery Migrate in the footer**

	function include_jquery_in_footer(){
		if(!is_admin()){
			wp_enqueue_script('jquery', 'https://code.jquery.com/jquery-3.6.0.min.js', array(), null, true);
			wp_enqueue_script('jquery-migrate', 'https://code.jquery.com/jquery-migrate-3.3.2.min.js', array('jquery'), null, true);
		}
	}
	add_action('wp_enqueue_scripts', 'include_jquery_in_footer');

**WordPress - Add custom js external scripts**

	function add_scripts(){
		// Use this for javascripts
		wp_enqueue_script('example-name', 'external_url', array(), null, true);
		
		// Use this for css scripts
		wp_register_style('example-name', 'external_url', array(), '1.0');
		
		// Enable css scripts
		wp_enqueue_style('example-name');
	}
	add_action('wp_enqueue_scripts', 'add_scripts');

**WordPress - Insert tags on body**

	function tags_body(){ ?>

	Insert here the code you want, Google ADS, Analytic etc

	<?php }
	add_action('wp_footer', 'tags_body');

**Elementor - Remove Font Awesome**

	add_action('elementor/frontend/after_register_styles',function(){
		foreach( [ 'solid', 'regular', 'brands' ] as $style){
			wp_deregister_style('elementor-icons-fa-' . $style);
		}
	}, 20);

**Elementor - Remove Eicons in Elementor**

	function disable_eicons(){
		wp_dequeue_style('elementor-icons');
		wp_deregister_style('elementor-icons');
	}
	add_action('wp_enqueue_scripts', 'disable_eicons', 11);

**Elementor - Remove Animations**

	function remove_animation(){
		wp_deregister_style('elementor-animations');
		wp_dequeue_style('elementor-animations');
		wp_dequeue_style('elementor-frontend');
	}
	add_action('wp_enqueue_scripts', 'remove_animation', 100);