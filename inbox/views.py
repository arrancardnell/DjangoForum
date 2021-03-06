from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q
from django.shortcuts import render, redirect

from inbox.forms import PrivateConversationForm, PrivateMessageForm
from inbox.models import PrivateConversation, PrivateMessage


# inbox views
@login_required
def inbox(request):
    user = request.user

    # get all the conversations where user is either an owner or recipient
    conversations = PrivateConversation.objects.filter(Q(owner=user) | Q(recipient=user))
    sorted_consersations = conversations.annotate(
        latest_message=Max('pconv_messages__created')).order_by('-latest_message')

    return render(request,
                  'inbox/inbox.html',
                  {'conversations': sorted_consersations})


@login_required
def new_conversation(request):
    if request.method == 'POST':
        private_conversation_form = PrivateConversationForm(data=request.POST)
        private_message_form = PrivateMessageForm(request.POST)

        if private_conversation_form.is_valid() and private_message_form.is_valid():
            # create new conversation
            new_private_conversation = private_conversation_form.save(commit=False)

            # assign an owner
            new_private_conversation.owner=request.user

            # save the form
            new_private_conversation.save()

            # get the conversation object
            conversation = PrivateConversation.objects.filter(owner=request.user).latest()

            # add the new private message to the form
            new_private_message = private_message_form.save(commit=False)
            # link the message to the form
            new_private_message.sender = request.user
            new_private_message.conversation = conversation
            # save the message
            new_private_message.save()
            return redirect('inbox:inbox')
    else:
        private_conversation_form = PrivateConversationForm(user=request.user)
        private_message_form = PrivateMessageForm
    return render(request,
                  'inbox/new_conversation.html',
                  {'private_conversation_form': private_conversation_form,
                   'private_message_form': private_message_form})

def view_conversation(request, conversation_id):

    conversation = PrivateConversation.objects.get(id=conversation_id)

    if request.user == conversation.owner or request.user == conversation.recipient:
        messages = PrivateMessage.objects.filter(conversation=conversation)

        return render(request,
                      'inbox/conversation.html',
                      {'conversation': conversation,
                       'messages': messages})