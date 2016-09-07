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
            $('#chat_message_text').val('');
            $('.chat_message:first').remove();
            $('#chat_messages')
                .append('<p class="chat_message">'+json.owner+' ('+json.created+')'+': '+json.text+'</p>');
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
                $chat_messages.append('<p class="chat_message">'
                    +messages[i]['owner__username']+' ('+messages[i]['created']+')'+': '+messages[i]['content']+'</p>')
            };
        }
    });
};

var refreshId = setInterval(function () {
    refresh_chat();
}, 9000);