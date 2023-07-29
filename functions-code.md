# Codes for you WordPress

Place it on functions.php or create a new plugin for this.

- WordPress general Codes
- 1: Filters
- 2: Actions
- 3: Shortcodes

### WordPress general Codes


#### 1: Filters

/* Enable shortcode in menu ---------- */
add_filter('wp_nav_menu_items', 'do_shortcode');

/*  Enable logout url masked eg: /$VALUE=1 ---------- */
add_filter('logout_url', 'custom_logout_url', 10, 2);
add_action('wp_loaded', 'custom_logout_action');

/* Custom logout URL ---------- */
function custom_logout_url($logout_url, $redirect){
    $url = add_query_arg('NEW_VALUE', 1, home_url()); // example: bye
    if(! empty( $redirect )){
        $url = add_query_arg('redirect', $redirect, $url);
    }
    return esc_url( $url );
}
add_filter( 'logout_url', 'custom_logout_url', 10, 2 );

/* Custom logout URL redirection ---------- */
function custom_logout_action(){
    $user_id = get_current_user_id();
    if(isset( $_GET['NEW_VALUE'])){
        wp_logout();
        $loc = isset( $_GET['redirect'] ) ? $_GET['redirect'] : home_url();
        wp_redirect(esc_url( $loc ), 302);
        exit;
    }
}
add_action( 'template_redirect', 'custom_logout_action' );

/* WordPress - Remove emojis ---------- */
function remove_emoji(){
    remove_action( 'wp_head', 'print_emoji_detection_script', 10 );
    remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
    remove_action( 'admin_print_styles', 'print_emoji_styles' );
    remove_filter( 'the_content_feed', 'wp_staticize_emoji' );
    remove_filter( 'comment_text_rss', 'wp_staticize_emoji' );
    remove_filter( 'wp_mail', 'wp_staticize_emoji_for_email' );
}
add_action( 'init', 'remove_emoji' );

/* Remove amp validation ---------- */
add_filter(
    'amp_validation_error_sanitized',
    fn( $sanitized, $error ) => (
        $error['node_name'] === 'script'
        && strpos( $error['text'], 'WFAJAXWatcherVars' ) !== false
    ) ? true : $sanitized,
    10,
    2
);

/* Change author base url: domain/author to your domain/$NEW_SLUG ---------- */
function wp_custom_author_urlbase($wp_rewrite){
    global $wp_rewrite;
    $author_slug = 'NEW_SLUG'; // the new slug name
    $wp_rewrite->author_base = $author_slug;
    flush_rewrite_rules();
}
add_action( 'init', 'wp_custom_author_urlbase' );

/* Limit access to media library ( users can only see/select own media ) ---------- */
function wpsnippet_show_current_user_attachments( $query ){
    $user_id = get_current_user_id();
    if( $user_id && !current_user_can( 'activate_plugins' ) && !current_user_can( 'edit_others_posts' ) ){
        $query['author'] = $user_id;
    }
    return $query;
}
add_filter( 'ajax_query_attachments_args', 'wpsnippet_show_current_user_attachments' );

/* Change query search 's' to other value ---------- */
add_action('init', function(){
    add_rewrite_tag('%search_query%', '([^&]+)');
    remove_query_arg('s');
});

add_filter('request', function($request){
    if(isset($_REQUEST['search'])){
        $search_query = sanitize_text_field( $_REQUEST['search']);
        $request['s'] = $search_query;
    }
    return $request;
} );

/* Disable default search on WordPress ---------- */
add_action( 'init', function(){
    add_rewrite_tag( '%search_query%', '([^&]+)');
    remove_query_arg('s');
});

add_filter('request', function( $request){
    if(isset($_REQUEST['search'])){
        $search_query = sanitize_text_field($_REQUEST['search']);
        $request['s'] = $search_query;
    }

    return $request;
});

/* Remove WP version from css & scripts ---------- */
function my_remove_wp_ver_css_js($src){
    if(strpos($src, 'ver=')){
        $src = remove_query_arg('ver', $src);
    }
    return $src;
}
add_filter('style_loader_src', 'my_remove_wp_ver_css_js', 9999);
add_filter('script_loader_src', 'my_remove_wp_ver_css_js', 9999);

* Remove WP version from RSS ---------- */
add_filter('the_generator', '__return_empty_string');

/* Remove Admin Bar  ---------- */
add_filter('show_admin_bar', '__return_false');

/* Remove WP version from head ---------- */
remove_action('wp_head', 'wp_generator');

/* Disable Gutemberg  ---------- */
add_filter('use_block_editor_for_post', '__return_false');

/* WordPress - Disable FontAwesome ---------- */
add_action('wp_enqueue_scripts', function(){ wp_dequeue_style('font-awesome'); }, 50);

/* To remove the Font Awesome http request as well on elementor  ---------- */
add_action('elementor/frontend/after_enqueue_styles', function (){ wp_dequeue_style('font-awesome');});

/* Remove Gutenberg block library CSS ---------- */
function remove_wp_block_library_css(){
    wp_dequeue_style(array('wp-block-library', 'wp-block-library-theme', 'wc-block-style', 'global-styles'));
}
add_action('wp_enqueue_scripts', 'remove_wp_block_library_css');

/* Clean WordPress ---------- */
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
    add_filter('emoji_svg_url', '__return_false' );
    add_filter('enable_post_by_email_configuration', '__return_false', 999);
    add_filter('feed_links_show_comments_feed', '__return_false');
    add_filter('get_image_tag_class', function( $c, $i, $align, $s ){ return 'align'.esc_attr( $align ); }, 10, 4);
    add_filter('jpeg_quality', function( $v ){ return 95;});
    add_filter('the_generator', '__return_empty_string');
    remove_action( 'welcome_panel', 'wp_welcome_panel');
    }
}

/* WordPress - Enable WEBP in Media ---------- */
add_filter('mime_types', function($mimes){ $mimes['webp'] = 'image/webp'; return $mimes;});

/*  Enable preview for webp image files ---------- */
function webp_is_displayable($result, $path){
    if($result === false){
        $info = getimagesize($path, $image_info);
        $displayable_image_types = array(iMAGETYPE_WEBp);
        if($info !== false && in_array( $info[2], $displayable_image_types)){
            $result = true;
        } else {
            $result = false;
        }
    }
    return $result;
}
add_filter('file_is_displayable_image', 'webp_is_displayable', 10, 2);

/* Enable RSS on Header ---------- */
add_theme_support('automatic-feed-links');

/* Hide admin ajax from no-admin users ---------- */
function redirect_non_admin_users(){
    // Check if user is not an admin and not accessing admin-ajax.php
    if( ! current_user_can('manage_options') && '/wp-admin/admin-ajax.php' !== $_SERVER['PHP_SELF']){
        // Redirect user to homepage
        wp_redirect(home_url());
        exit;
    }
}
add_action('admin_init', 'redirect_non_admin_users');

/* Change footer name ---------- */
function replace_footer_text(){
    echo 'YOUR NEW FOOTER';
}
add_action('admin_footer_text', 'replace_footer_text');

/* Prevent upload from no staff users ---------- */
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
            if(!current_user_can('manage_options') ){
            $redirect_to = home_url();
            wp_redirect( $redirect_to, 302 );
        }
    }
}
add_action('admin_init', 'pws_block_admin', 0);

/* Remove default inclusion of jQuery and jQuery Migrate ---------- */
function remove_default_jquery(){
    if(!is_admin()){
        wp_deregister_script('jquery');
        wp_deregister_script('jquery-migrate');
    }
}
add_action('wp_enqueue_scripts', 'remove_default_jquery');

// Include jQuery and jQuery Migrate in the footer ---------- */
function include_jquery_in_footer() {
    if(!is_admin()){
        wp_enqueue_script('jquery', 'https://code.jquery.com/jquery-3.6.0.min.js', array(), null, true);
        wp_enqueue_script('jquery-migrate', 'https://code.jquery.com/jquery-migrate-3.3.2.min.js', array('jquery'), null, true);
    }
}
add_action('wp_enqueue_scripts', 'include_jquery_in_footer');


#### 2: Actions

/* Add custom js external scripts ---------- */
function add_scripts(){

    // Use this for javascripts
    wp_enqueue_script( 'example-name', 'external_url', array(), null, true );
    
    // Use this for css scripts
    wp_register_style( 'example-name', 'external_url', array(), '1.0' );
    
    // Enable css scripts
    wp_enqueue_style( 'example-name' );

}
add_action( 'wp_enqueue_scripts', 'add_scripts' );


/* Insert tags on body ---------- */
function tags_body() { ?>

Insert here the code you want, Google ADS, Analytic etc

<?php }
add_action('wp_footer', 'tags_body');

#### 3: Shortcodes
