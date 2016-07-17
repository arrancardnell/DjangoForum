from django import forms
from .models import Post, Topic

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)


class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'description',)