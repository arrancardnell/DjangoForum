/**
 * Created by arran on 05/09/16.
 */

$('#add_chat_message').on('submit', function(event) {
    event.preventDefault();
    create_message();
})

// AJAX for creating messages
function create_message() {
    $.ajax({
        url: 'add_chat_message/',
        type: 'POST',
        data: {chat_message_text: $('#chat_message_text').val()},

        // handle a successful response
        success : function(json){
            if (json.result == 'created') {
                $('#chat_message_text').val('');
                $('.chat_message:last').remove();
                $('#chat_messages')
                    .prepend('<div class="chat_message"> <div class="chat_user">'
                        + json.owner + ': </div> <div class="chat_comment">' + json.text
                        + '<span class="chat_date">' + json.created + '</span></div></div>');
            }
        }
    });
};

// AJAX for refreshing the chat
function refresh_chat() {
    $.ajax({
        url: 'refresh_chat/',
        type: 'POST',

        // handle successful response
        success : function(json){
            var $chat_messages = $('#chat_messages');
            $('.chat_message').remove();
            var messages = json.messages;
            for (i=0; i < messages.length; i++){
                $chat_messages.append('<div class="chat_message"> <div class="chat_user">'
                    +messages[i]['owner__username']+': </div> <div class="chat_comment">'+messages[i]['content']
                    +'<span class="chat_date">'+messages[i]['created']+'</span></div></div>')
            };
        }
    });
};

var refreshId = setInterval(function () {
    refresh_chat();
}, 9000);