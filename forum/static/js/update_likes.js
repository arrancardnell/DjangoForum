/**
 * Created by arran on 15/09/16.
 */

$('.like_post_button').on('submit', function(event) {
    event.preventDefault();
    var $this = $this
    update_likes($this);
});

function update_likes(post){
    $.ajax({
        url: 'update_likes/$',
        type: 'POST',
        data: {
            post_id: post.data('id'),
            post_action: post.data('action')
        },

        // handle a successful response
        success : function(json){
            if (json.result == 'updated'){
                var $post_id = post.data('id');
                
            }
        }

    });
}