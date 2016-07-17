from django import forms
from .models import Post

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
