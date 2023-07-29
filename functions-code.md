Codes for you WordPress
place it on functions.php or create a new plugin for this.

1 - WordPress general Codes
- 1.1 - Filters
- 1.2 - Shortcodes

2 - Plugins codes

---------- Filter: Enable Shortcode in menu
add_filter('wp_nav_menu_items', 'do_shortcode');

---------- Filter: WordPress - Enable logout url masked eg: /$VALUE=1
add_filter( 'logout_url', 'custom_logout_url', 10, 2 );
add_action( 'wp_loaded', 'custom_logout_action' );
function custom_logout_url( $logout_url, $redirect ){

  $url = add_query_arg( 'saindo', 1, home_url( '/' ) );

  if ( ! empty ( $redirect ) )
  $url = add_query_arg( 'redirect', $redirect, $url );

  return $url;
}

function custom_logout_action(){
 if ( ! isset ( $_GET['saindo'] ) )
  return;

  wp_logout();

  $loc = isset ( $_GET['redirect'] ) ? $_GET['redirect'] : home_url( '/' );
  wp_redirect( $loc );
  exit;
}

---------- Filter: WordPress - Add Category Id to WordPress Body and Post Class
function category_id_class($classes) {
  global $post;
  foreach((get_the_category($post->ID)) as $category)
    $classes [] = 'cat-' . $category->cat_ID . '-id';           
  return $classes;
}
add_filter('post_class', 'category_id_class');
add_filter('body_class', 'category_id_class');

---------- Shortcode: Count posts from a taxonamy
---------- Usage: [cat_count]
function cat_count() {
  $args = array(
    'post_type' => 'post',
    'post_status' => 'published',
    'product_cat' => $catpage, // $catpage == your category slug name
    'numberposts' => -1
  ); ?>
  <div>Showing <b>10</b> of <b><?php $num = count( get_posts( $args ) ) ?></b> articles.</div>
<?php }
add_shortcode( 'cat_count' , 'cat_count' );


