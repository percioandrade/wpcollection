# Shortcode codes for you WordPress

Place it on functions.php or create a new plugin for this.

**Show post title - Usage: [page_title]**

    function show_page_title(){
        $title = get_transient('show_page_title');
        if (false === $title){
            $title = get_the_title();
            set_transient('show_page_title', $title, 1 * HOUR_IN_SECONDs);
        }
        return esc_html($title) ?: 'Untitled'; // Return 'Untitled' if $title is empty
    }
    add_shortcode('page_title', 'show_page_title');

**Get page/post URL - Usage: [page_url]**

    function show_page_url(){
        $url = get_transient('show_page_url');
        if (false === $url ){
            $url = get_permalink();
            $url = rtrim($url, '/');
            set_transient('show_page_url', $url, 1 * HOUR_IN_SECONDs);
        }
        return esc_url($url );
    }
    add_shortcode('page_url', 'show_page_url');

**Show featured image from post - Usage: [thumb size="thumbnail"]**

    function show_thumb($atts){
        $atts = shortcode_atts(array(
            'size' => 'thumbnail',
        ), $atts);

        $thumbnail_id = get_post_thumbnail_id();
        $thumbnail = wp_get_attachment_image($thumbnail_id, $atts['size'] );
        $caption = wp_get_attachment_caption($thumbnail_id);
        $link = get_permalink();

        return '<div class="featured-image">'
            . $thumbnail . '<span class="caption imgPerfil">' . esc_html($caption) . '</span>'
            . '</div>';
    }
    add_shortcode('thumb', 'show_thumb');

**Show latest posts - Usage: [latest_post]**

    function latest_post(){
    $the_query = new WP_Query(array(
    'category_name' => 'noticias',
    'posts_per_page' => 3,
    ));
    $output = ''; // initialize output variable

    if($the_query->have_posts()) :
        $output .= '<div class="latest-posts">'; // start a container div
        while($the_query->have_posts()) : $the_query->the_post();
            $output .= '<div class="latest-post">';
            $output .= '<a href="' . get_permalink() . '">' . get_the_post_thumbnail($post->ID, array(80, 80)) . '</a>';
            $output .= '<h3><a href="' . get_permalink() . '">' . get_the_title() . '</a></h3>';
            $output .= '</div>';
        endwhile;
        $output .= '</div>'; // close the container div
        wp_reset_postdata();
    else :
        $output .= '<p>' . __('No News') . '</p>';
    endif;
    return $output;
    }
    add_shortcode('latest_post', 'latest_post');

**Show latest post updated time - Usage: [update_time]**

    function update_time(){
        $u_time = get_the_time('U');
        $u_modified_time = get_the_modified_time('U');
        
        // Only display modified date if 24hrs have passed since the post was published.
        if ($u_modified_time >= $u_time + 86400){
            
            $updated_date = get_the_modified_time('d/m/Y');
            $updated_time = get_the_modified_time('h:i a');
            
            $description = '';
            $description .= $desc ? $desc . ' ' : '';
            $description .= $updated_date . ' ' . $updated_time;
            
            return wp_kses_post($description);
        }
    }
    add_shortcode('update_time', 'update_time');

**Count total posts for category taxonomy - Usage: [cat_count]**

    function cat_count(){
        $cat = get_queried_object();
        $args = array(
            'post_type' => 'post',
            'post_status' => 'publish',
            'tax_query' => array(
                array(
                    'taxonomy' => 'category',
                    'field' => 'slug',
                    'terms' => $cat->slug,
                ),
            ),
            'posts_per_page' => -1, // set to -1 to retrieve all posts
        );

        $num_posts = count(get_posts($args));
        $num_displayed = 10;
        $count_text = sprintf( __('Showing <b>%s</b> of <b>%s</b> articles.'), $num_displayed, $num_posts);
        return '<div>' . $count_text . '</div>';
    }
    add_shortcode('cat_count' , 'cat_count');

**Get imagems from template dir - Usage: [get_the image="/path/image"]**

    add_shortcode('get_the', function($atts){
        global $bndurl;
        // Check if 'image' attribute exists
        if ( ! isset($atts['image'] )){
            return 'Error: image attribute missing';
        }
        // Use string interpolation to create image URL
        $image_url = "{$bndurl}/assets/img{$atts['image']}";
        return $image_url;
    });


**Get actual user url - Usage: [user_url]**

    function user_url(){
        $base_url = get_bloginfo('url');
        $current_user = wp_get_current_user();
        $username = $current_user->user_login;
        // Create a URL-friendly slug by removing special characters and spaces
        $username_slug = sanitize_title($username);
        $wordpress_url = $base_url . '/author/' . $username_slug;
        return $wordpress_url;
    }
    add_shortcode('user_url', 'user_url');

**Generate a url from random post - Usage: [random_post]**

    function random_post(){
        ob_start();
        $random_post = get_posts(array(
            'post_type'      => 'post',  // substitua 'post' pelo tipo de postagem que deseja usar
            'orderby'        => 'rand',
            'posts_per_page' => 1,
            'post_status'    => 'publish'
        ));
        if ($random_post){
            $permalink = get_permalink($random_post[0]->ID);
            echo $permalink;
        }
        return ob_get_clean();
    }
    add_shortcode('random_post', 'random_post');