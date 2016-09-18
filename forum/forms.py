from django import forms
from django.contrib.auth.models import User

from .models import Post, PrivateConversation, PrivateMessage, Profile, Topic


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)


class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PrivateConversationForm(forms.ModelForm):
    class Meta:
        model = PrivateConversation
        fields = ('recipient', 'title')


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ('content')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']