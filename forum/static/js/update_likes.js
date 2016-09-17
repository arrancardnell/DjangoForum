/**
 * Created by arran on 15/09/16.
 */

$('.like_post_button').on('click', function(event) {
    event.preventDefault();
    var $this = $(this);
    $.ajax({
        url: 'update_likes/',
        type: 'POST',
        data: {
            post_id: $this.data('id'),
            post_action: $this.data('action')
        },

        // handle a successful response
        success : function(json){
            if (json.result == 'updated'){

                var previous_action = $this.data('action');
                var $post = $('#post_'+json.post_id);
                var $post_likes = $post.find('.post_likes');
                var total_likes = parseInt(json.post_likes);
                if (total_likes == 0){
                    $post_likes.text('');
                } else {
                    if (total_likes == 1) {
                        var users_pluralize = ' user likes';
                    } else {
                        var users_pluralize = ' users like';
                    }
                    $post_likes.text(total_likes + users_pluralize + ' this post');
                }
                $this.data('action', previous_action == 'like' ? 'unlike' : 'like');
                $this.val(previous_action == 'like' ? 'Unlike' : 'Like');
                console.log('success');
            }
        }

    });
});