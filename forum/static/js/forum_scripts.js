/**
 * Created by arran on 17/09/16.
 */


$('#add_chat_message').on('submit', function(event) {
    event.preventDefault();
    create_message();
});

// AJAX for creating messages
function create_message() {
    $.ajax({
        url: '/forum/ajax/add_chat_message/',
        type: 'POST',
        data: {chat_message_text: $('#chat_message_text').val()},

        // handle a successful response
        success : function(json){
            if (json.result == 'created') {
                $('#chat_message_text').val('');
                var $chat_messages = $('.chat_message');
                // only remove the last message if there are already 10
                if ($chat_messages.length == 10){
                    $chat_messages.last().remove();
                }
                $('#chat_messages')
                    .prepend('<div class="chat_message"> <div class="chat_user">'
                        + json.owner + ': </div> <div class="chat_comment">' + json.text
                        + '<span class="chat_date">' + json.created + '</span></div></div>');
            }
        }
    });
}

// AJAX for refreshing the chat
function refresh_chat() {
    $.ajax({
        url: '/forum/ajax/refresh_chat/',
        type: 'POST',
        data: {last_message: $('.chat_message:first').val()},

        // handle successful response
        success : function(json){
            if (json.result == 'refreshed') {
                var $chat_messages = $('#chat_messages');
                $('.chat_message').remove();
                var messages = json.messages;
                for (i = 0; i < messages.length; i++) {
                    $chat_messages.append('<div class="chat_message"> <div class="chat_user">'
                        + messages[i]['owner__username'] + ': </div> <div class="chat_comment">' + messages[i]['content']
                        + '<span class="chat_date">' + messages[i]['created'] + '</span></div></div>')
                }
            }
        }
    });
}

var refreshId = setInterval(function () {
    refresh_chat();
}, 9000);


// AJAX for liking posts
$('.like_post_button').on('click', function(event) {
    event.preventDefault();
    var $this = $(this);
    $.ajax({
        url: '/forum/ajax/update_likes/',
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

                // remove any text after an unlike if there are no likes
                if (total_likes == 0){
                    $post_likes.text('');
                } else {
                    var users_pluralize;
                    // pluralize the text based on single or multiple likes
                    if (total_likes == 1) {
                        users_pluralize = ' user likes';
                    } else {
                        users_pluralize = ' users like';
                    }
                    $post_likes.text(total_likes + users_pluralize + ' this post');
                }
                // Set the new action and text
                $this.data('action', previous_action == 'like' ? 'unlike' : 'like');
                $this.val(previous_action == 'like' ? 'Unlike' : 'Like');
            }
        }
    });
});