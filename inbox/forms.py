from django import forms
from django.contrib.auth.models import User

from inbox.models import PrivateConversation, PrivateMessage


class PrivateConversationForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        # exclude the current user so they can't message themselves
        super(PrivateConversationForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = User.objects.exclude(username=user.username)

    class Meta:
        model = PrivateConversation
        fields = ('recipient', 'title')


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ('content',)