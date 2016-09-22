from django import forms

from inbox.models import PrivateConversation, PrivateMessage


class PrivateConversationForm(forms.ModelForm):
    class Meta:
        model = PrivateConversation
        fields = ('recipient', 'title')


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ('content',)