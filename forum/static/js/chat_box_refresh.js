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
            $('.chat_messages_list').append('<li class="chat_message">'+json.text+'</li>');
        }
    });
};